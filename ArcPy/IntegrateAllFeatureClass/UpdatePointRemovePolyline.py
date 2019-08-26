# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class UpdatePointRemovePolyline:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfigTopo = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigTopo.json")
        # Read File Config Process Topo
        if not os.path.isfile(self.pathFileConfigTopo):
            print "... Not Found: " + self.pathFileConfigTopo + "?\n  ... Create File ConfigTopo..."
            self.CreateFileConfigTopo()
        self.ReadFileConfigTopo()
        pass

    def Execute(self):
        # Init Workspace
        arcpy.env.overwriteOutput = True
        # ProcessFeatureClassPointRemove
        self.ProcessFeatureClassPointRemove()
        pass

    def ProcessFeatureClassPointRemove(self):
        for elemConfigTopo in self.configTopoTools.listConfig:
            featureDataSetPolyLine = elemConfigTopo.featureDataSet
            for elemPolyline in elemConfigTopo.listPolyline:
                featureClassPolyLine = FeatureClass(elemPolyline.featureClass)
                if featureClassPolyLine.featureClass != "DoanTimDuongBo":
                    continue
                print "# {}".format(featureClassPolyLine.featureClass)
                featureClassPolyLine.SetFeatureClassPointRemove()
                inPathFC = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemove)
                if not arcpy.Exists(inPathFC) or int(arcpy.GetCount_management(inPathFC).getOutput(0)) == 0:
                    continue
                fCTemp = "in_memory\\fCTemp"
                arcpy.CopyFeatures_management(in_features = inPathFC,
                                              out_feature_class = fCTemp)
                for elemPolygonTopo in elemPolyline.polygonTopos:
                    featureDataSetPolygon = elemPolygonTopo.featureDataSet
                    for elemPolygon in elemPolygonTopo.listPolygon:
                        featureClassPolygon = FeatureClass(elemPolygon.featureClass)
                        if elemPolygon.processTopo == True:
                            self.ProcessFeatureClassPointRemoveSubOne(featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp)
                            self.ProcessFeatureClassPointRemoveSubTwo(featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp)
                            pass

                # Dissolve
                featureClassPolyLine.SetFeatureClassPointRemoveDissolve()
                outputDissolve = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolve)
                fieldName = self.GetFieldFID(featureClassPolyLine.featureClass)
                self.Dissolve(fCTemp, outputDissolve, fieldName)
                # Add Field
                arcpy.AddField_management(in_table = outputDissolve,
                                          field_type = "TEXT",
                                          field_name = "startPoint",
                                          field_length = "100")
                arcpy.AddField_management(in_table = outputDissolve,
                                          field_type = "TEXT",
                                          field_name = "endPoint",
                                          field_length = "100")

                # Xu ly neu diem dau hoac diem cua cua Polyline bi Remove:
                inPathPolylineFC = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClass)
                for elemPolygonTopo in elemPolyline.polygonTopos:
                    featureDataSetPolygon = elemPolygonTopo.featureDataSet
                    for elemPolygon in elemPolygonTopo.listPolygon:
                        featureClassPolygon = FeatureClass(elemPolygon.featureClass)
                        if elemPolygon.processTopo == True:
                            ## Diem dau
                            #print "# Diem dau"
                            self.ProcessPointStartEnd(fCTemp, inPathPolylineFC, outputDissolve, "START", featureDataSetPolygon, featureClassPolygon, fieldName)
                            ## Diem cuoi
                            #print "# Diem cuoi"
                            self.ProcessPointStartEnd(fCTemp, inPathPolylineFC, outputDissolve, "END", featureDataSetPolygon, featureClassPolygon, fieldName)
                            pass
                arcpy.Delete_management("in_memory")
        pass

    def ProcessPointStartEnd(self, fCTemp, inPathPolylineFC, pathFCDissolve, option, featureDataSetPolygon, featureClassPolygon, fID):
        fCTempLayer = "fCTempLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCTemp,
                                          out_layer = fCTempLayer)
        # ORIG_FID
        outPutPoint = "in_memory\\outPutPoint"
        arcpy.FeatureVerticesToPoints_management(in_features = inPathPolylineFC,
                                                 out_feature_class = outPutPoint,
                                                 point_location = option)
        arcpy.AddField_management(in_table = outPutPoint,
                                  field_name = "pointStr",
                                  field_type = "Text",
                                  field_length = "100")
        if int(arcpy.GetCount_management(outPutPoint).getOutput(0)) == 0:
            return
        outPutPointLayer = "outPutPointLayer"
        arcpy.MakeFeatureLayer_management(in_features = outPutPoint,
                                          out_layer = outPutPointLayer)
        arcpy.SelectLayerByLocation_management(in_layer = outPutPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = fCTempLayer,
                                               search_distance = "0 Meters")
        if int(arcpy.GetCount_management(outPutPointLayer).getOutput(0)) == 0:
            return
        #print "# ProcessPointStartEnd"
        #
        pathPolygon = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClass)
        if not arcpy.Exists(pathPolygon) or int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
            return
        polygonLayer = "polygonLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                          out_layer = polygonLayer)
        featureClassPolygon.SetFeatureClassPointRemove()
        pathPolygonPointRemove = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClassPointRemove)
        if not arcpy.Exists(pathPolygonPointRemove) or int(arcpy.GetCount_management(pathPolygonPointRemove).getOutput(0)) == 0:
            return
        polygonPointRemoveLayer = "polygonPointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathPolygonPointRemove,
                                          out_layer = polygonPointRemoveLayer)
        arcpy.SelectLayerByLocation_management(in_layer = outPutPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = polygonPointRemoveLayer,
                                               search_distance = "0 Meters")
        if int(arcpy.GetCount_management(outPutPointLayer).getOutput(0)) == 0:
            return
        with arcpy.da.UpdateCursor(outPutPointLayer, ["OID@", "Shape@XY", "ORIG_FID", "pointStr"]) as cursor:
            for row in cursor:
                strQuery = "OBJECTID = " + str(row[0])
                x, y = row[1]
                pntUpdate = arcpy.Point(round(x, 10), round(y, 10))
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = outPutPointLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = strQuery)
                arcpy.SelectLayerByLocation_management(in_layer = polygonLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = outPutPointLayer,
                                                       search_distance = "0 Meters")
                if int(arcpy.GetCount_management(polygonLayer).getOutput(0)) == 0:
                    continue
                fIDPolygon = None
                arrPolygon = arcpy.Array()
                with arcpy.da.SearchCursor(polygonLayer, ["Shape@", "OID@"]) as cursorPolgonLayer:
                    for rowPolygonLayer in cursorPolgonLayer:
                        fIDPolygon = rowPolygonLayer[1]
                        partPolygon = arcpy.Array()
                        for part in rowPolygonLayer[0]:
                            for pnt in part:
                                partPolygon.add(pnt)
                        arrPolygon.add(partPolygon)
                        break
                fieldName = self.GetFieldFID(featureClassPolygon.featureClass)
                strQuery = str(fieldName) + " = " + str(fIDPolygon)
                print row[2]
                print strQuery
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = polygonPointRemoveLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = strQuery)
                if int(arcpy.GetCount_management(polygonPointRemoveLayer).getOutput(0)) == 0:
                    continue
                arrPointRemove = arcpy.Array()
                with arcpy.da.SearchCursor(polygonPointRemoveLayer, ["Shape@XY"]) as cursorPolygonPointRemove:
                    for rowPolygonPointRemove in cursorPolygonPointRemove:
                        xPointRemove, yPointRemove = rowPolygonPointRemove[0]
                        if xPointRemove != x and yPointRemove != y:
                            arrPointRemove.add(arcpy.Point(xPointRemove, yPointRemove))
                if arrPointRemove.count == 0:
                    continue
                xT, yT = self.ReturnPointUpdate(pntUpdate, arrPointRemove, arrPolygon)
                if xT and yT:
                    row[3] = str(xT) + ", " + str(yT)
                    cursor.updateRow(row)

        arcpy.SelectLayerByLocation_management(in_layer = outPutPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = fCTempLayer,
                                               search_distance = "0 Meters")

        with arcpy.da.SearchCursor(outPutPointLayer, ["OID@", "Shape@XY", "ORIG_FID", "pointStr"]) as cursorA:
            with arcpy.da.UpdateCursor(pathFCDissolve, ["OID@", fID, "startPoint", "endPoint"]) as cursorB:
                for rowA in cursorA:
                    #print "# ORIG_FID: {}".format(str(rowA[2]))
                    if rowA[3]:
                        cursorB.reset()
                        for rowB in cursorB:
                            #print "   # {}: {}".format(fID, str(rowB[1]))
                            if rowA[2] == rowB[1]:
                                if option == "START":
                                    #print "# Update START"
                                    rowB[2] = rowA[3]
                                elif option == "END":
                                    #print "# Update END"
                                    rowB[3] = rowA[3]
                                cursorB.updateRow(rowB)
                                break
        pass

    def ReturnPointUpdate(self, pntUpdate, arrPointRemove, arrPolygon):
        # Remove pntUpdate in arrPointRemove
        arrIndexPointRemove = []
        indexPointRemove = 0
        for pntRemove in arrPointRemove:
            if round(pntRemove.X, 5) == round(pntUpdate.X, 5) and round(pntRemove.Y, 5) == round(pntUpdate.Y, 5):
                arrIndexPointRemove.append(indexPointRemove)
            indexPointRemove += 1
        indexLoop = 0
        for indexPointRemvoe in arrIndexPointRemove:
            arrPointRemove.remove(indexPointRemvoe - indexLoop)
            indexLoop += 1
        # Mark Index Remove Point in arrPolygon
        arrIndexPart = []
        for part in arrPolygon:
            arrIndexPointOfPart = []
            indexPointOfPart = 0
            for pnt in part:
                if pnt:
                    if arrPointRemove.count == 0:
                        continue
                    foundPoint = False
                    indexPointRemove = 0
                    for pntRemove in arrPointRemove:
                        if round(pntRemove.X, 5) == round(pnt.X, 5) and round(pntRemove.Y, 5) == round(pnt.Y, 5):
                            foundPoint = True
                            break
                        indexPointRemove += 1
                    if foundPoint:
                        arrPointRemove.remove(indexPointRemove)
                        arrIndexPointOfPart.append(indexPointOfPart)
                indexPointOfPart += 1
            arrIndexPart.append(arrIndexPointOfPart)
        #print arrIndexPart
        #print "arrIndexPart[0] count: {}".format(len(arrIndexPart[0]))
        # Remove Point in arrPolygon
        indexPartNum = 0
        for indexPart in arrIndexPart:
            indexPointInPartNum = 0
            for indexPointInPart in indexPart:
                arrPolygon[indexPartNum].remove(indexPointInPart - indexPointInPartNum)
                indexPointInPartNum += 1
            indexPartNum += 1
        #print "arrPolygon[0] Count: {}".format(str(arrPolygon[0].count))
        # Find Point
        indexPartNum = 0
        indexPointInPartNum = 0
        found = False
        for part in arrPolygon:
            indexPointInPartNum = 0
            found = False
            for pnt in part:
                if pnt:
                    if round(pnt.X, 5) == round(pntUpdate.X, 5) and round(pnt.Y, 5) == round(pntUpdate.Y, 5):
                        found = True
                        break
                indexPointInPartNum += 1
            if found:
                break
            indexPartNum += 1
        # Print
        #for part in arrPolygon:
        #    for pnt in part:
        #        if pnt:
        #            print "{}, {}".format(pnt.X, pnt.Y)
        # Process IndexPoint
        if not found:
            return None, None
        arrPolygonCount = arrPolygon[indexPartNum].count
        if indexPointInPartNum == 0:
            pntBefore = arrPolygon[indexPartNum].getObject(indexPointInPartNum + 1)
            pntAfter = arrPolygon[indexPartNum].getObject(arrPolygonCount - 2)
        elif indexPointInPartNum == arrPolygonCount - 1:
            pntBefore = arrPolygon[indexPartNum].getObject(0)
            pntAfter = arrPolygon[indexPartNum].getObject(arrPolygonCount - 2)
        else:
            pntBefore = arrPolygon[indexPartNum].getObject(indexPointInPartNum + 1)
            pntAfter = arrPolygon[indexPartNum].getObject(indexPointInPartNum - 1)
        x, y = self.CreatePoint(pntBefore.X, pntBefore.Y, pntAfter.X, pntAfter.Y, pntUpdate.X, pntUpdate.Y)
        return x, y
        pass

    def ProcessPointStartEndOld(self, fCTemp, inPathPolylineFC, pathFCDissolve, option, featureDataSetPolygon, featureClassPolygon, fID):
        fCTempLayer = "fCTempLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCTemp,
                                          out_layer = fCTempLayer)
        # ORIG_FID
        outPutPoint = "in_memory\\outPutPoint"
        arcpy.FeatureVerticesToPoints_management(in_features = inPathPolylineFC,
                                                 out_feature_class = outPutPoint,
                                                 point_location = option)
        arcpy.AddField_management(in_table = outPutPoint,
                                  field_name = "pointStr",
                                  field_type = "Text",
                                  field_length = "100")
        if int(arcpy.GetCount_management(outPutPoint).getOutput(0)) == 0:
            return
        outPutPointLayer = "outPutPointLayer"
        arcpy.MakeFeatureLayer_management(in_features = outPutPoint,
                                          out_layer = outPutPointLayer)
        arcpy.SelectLayerByLocation_management(in_layer = outPutPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = fCTempLayer,
                                               search_distance = "0 Meters")
        if int(arcpy.GetCount_management(outPutPointLayer).getOutput(0)) == 0:
            return
        #print "# ProcessPointStartEnd"
        #
        pathPolygon = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClass)
        polygonLayer = "polygonLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                          out_layer = polygonLayer)
        featureClassPolygon.SetFeatureClassPointRemove()
        pathPolygonPointRemove = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClassPointRemove)
        if not arcpy.Exists(pathPolygonPointRemove) or int(arcpy.GetCount_management(inPathFC).getOutput(0)) == 0:
            return
        polygonPointRemoveLayer = "polygonPointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathPolygonPointRemove,
                                          out_layer = polygonPointRemoveLayer)
        with arcpy.da.UpdateCursor(outPutPointLayer, ["OID@", "Shape@XY", "ORIG_FID", "pointStr"]) as cursor:
            for row in cursor:
                strQuery = "OBJECTID = " + str(row[0])
                x, y = row[1]
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = outPutPointLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = strQuery)
                arcpy.SelectLayerByLocation_management(in_layer = polygonLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = outPutPointLayer,
                                                       search_distance = "0 Meters")
                if int(arcpy.GetCount_management(polygonLayer).getOutput(0)) == 0:
                    continue
                arrPoint = None
                fIDPolygon = None
                with arcpy.da.SearchCursor(polygonLayer, ["Shape@", "OID@"]) as cursorPolgonLayer:
                    for rowPolygonLayer in cursorPolgonLayer:
                        for part in rowPolygonLayer[0]:
                            for pnt in part:
                                if pnt.X == x and pnt.Y == y:
                                    #print "{}, {}; {}, {}".format(str(x), str(y), str(pnt.X), str(pnt.Y))
                                    arrPoint = part
                                    fIDPolygon = rowPolygonLayer[1]
                                    break
                if arrPoint == None:
                    continue
                #print "Len arrPointPolygon Before Simplify {}".format(str(len(arrPoint)))
                fieldName = self.GetFieldFID(featureClassPolygon.featureClass)
                strQuery = str(fieldName) + " = " + str(fIDPolygon)
                #print strQuery
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = polygonPointRemoveLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = strQuery)
                if int(arcpy.GetCount_management(polygonPointRemoveLayer).getOutput(0)) == 0:
                    continue
                arrIndexRemove = []
                with arcpy.da.SearchCursor(polygonPointRemoveLayer, ["Shape@XY"]) as cursorPolygonPointRemove:
                    for rowPolygonPointRemove in cursorPolygonPointRemove:
                        xPointRemove, yPointRemove = rowPolygonPointRemove[0]
                        indexRemove = 0
                        for pnt in arrPoint:
                            if xPointRemove == pnt.X and yPointRemove == pnt.Y and xPointRemove != x and yPointRemove != y:
                                arrIndexRemove.append(indexRemove)
                                break;
                            indexRemove += 1
                if len(arrIndexRemove) == 0:
                    continue
                arrIndexRemove.sort()
                #print arrIndexRemove
                #print "Leng arr Before Remove: {}".format(str(arrPoint.count))
                indexRemoveSub = 0
                for indexRemove in arrIndexRemove:
                    arrPoint.remove(indexRemove - indexRemoveSub)
                    indexRemoveSub += 1
                #print "Leng arr After Remove: {}".format(str(arrPoint.count))
                indexPnt = 0
                for pnt in arrPoint:
                    if x == pnt.X and y == pnt.Y:
                        break
                    indexPnt += 1
                pntBefore = arrPoint.getObject(indexPnt - 1)
                pntAfter = arrPoint.getObject(indexPnt + 1)
                #print type(pntBefore)
                #print type(pntAfter)
                #print "# {}, {}".format(str(x), str(y))
                #print "# {}, {}".format(str(pntBefore.X), str(pntBefore.Y))
                #print "# {}, {}".format(str(pntAfter.X), str(pntAfter.Y))
                xT, yT = self.CreatePoint(pntBefore.X, pntBefore.Y, pntAfter.X, pntAfter.Y, x, y)
                row[3] = str(xT) + ", " + str(yT)
                #print "xT, yT: {}, {}".format(str(xT), str(yT))
                cursor.updateRow(row)
        #print "# Option: {}".format(option)
        arcpy.SelectLayerByLocation_management(in_layer = outPutPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = fCTempLayer,
                                               search_distance = "0 Meters")
        print "outPutPointLayer: {}".format(str(int(arcpy.GetCount_management(outPutPointLayer).getOutput(0))))
        with arcpy.da.SearchCursor(outPutPointLayer, ["OID@", "Shape@XY", "ORIG_FID", "pointStr"]) as cursorA:
            with arcpy.da.UpdateCursor(pathFCDissolve, ["OID@", fID, "startPoint", "endPoint"]) as cursorB:
                for rowA in cursorA:
                    #print "# ORIG_FID: {}".format(str(rowA[2]))
                    cursorB.reset()
                    for rowB in cursorB:
                        #print "   # {}: {}".format(fID, str(rowB[1]))
                        if rowA[2] == rowB[1]:
                            if option == "START":
                                #print "# Update START"
                                rowB[2] = rowA[3]
                            elif option == "END":
                                #print "# Update END"
                                rowB[3] = rowA[3]
                            cursorB.updateRow(rowB)
                            break
        pass

    def CreatePoint(self, xA, yA, xB, yB, xC, yC):
        try:
            # Duong thang di qua 2 diem A(xA, yA) va B(xB, yB)
            ## Vecto AB(xB - xA, yB- yA) => VTCP u(xU, yU)
            xU = xB - xA
            yU = yB - yA
            ## VTPT n = (-yU, xU)
            xN = -yU
            yN = xU
            ## PT duong thang di qua A nhan n lam VTPT la: xN(x - xA) + yN(y - yA) = 0 => cA = xN*-xA + yN*-yA
            cA = (xN*(-xA) + yN*(-yA))
            #print "cA: {}".format(cA)
            #print "{}x + {}y + {} = 0".format(str(xN), str(yN), str(cA))
            # Duong thang di qua C(xC, yC) song song voi AB:
            ## PT duong thang di qua C(xC, yC) song song voi AB: xU(x - xC) + yU(y - yC) = 0 => cC = xU*(-xC) + yU*(-yC)
            cC = xU*(-xC) + yU*(-yC)
            #print "cC: {}".format(cC)
            #print "{}x + {}y + {} = 0".format(str(xU), str(yU), str(cC))
            # Tim D(xD, yD) la giao diem cua hai duong thang:
            ## x = (-cA - yN*y) / xN
            ## xU*((-cA - yN*y) / xN) + yU*y + cC = 0 => xU*(-cA - yN*y) + yU*xN*y + cC*xN = 0 => -xU*cA - xU*yN*y + yU*xN*y + cC*xN = 0 => y*(yU*xN - xU*yN) + xU*(-cA) + cC*xN = 0 => y = (xU*cA - cC*xN) / (yU*xN - xU*yN)
            yD = (xU*cA - cC*xN) / (yU*xN - xU*yN)
            xD = (-cA - yN*yD) / xN
            # Tinh Vecto DA(xA - xD, yA - yD), DB(xB - xD, yB - yD)
            xDA = xA - xD
            yDA = yA - yD
            xDB = xB - xD
            yDB = yB - yD
            #print "{}, {}".format(xD, yD)
            #print "DA({}, {}), DB({}, {})".format(str(xDA), str(yDA), str(xDB), str(yDB))
            lengthDA = math.sqrt(math.pow(xDA, 2) + math.pow(yDA, 2))
            lengthDB = math.sqrt(math.pow(xDB, 2) + math.pow(yDB, 2))
            lengthAB = math.sqrt(math.pow(xU, 2) + math.pow(yU, 2))
            #print "lengthDA: {}".format(lengthDA)
            #print "lengthDB: {}".format(lengthDB)
            #print "lengthAB: {}".format(lengthAB)
            if round(lengthDA + lengthDB, 5) == round(lengthAB, 5):
                return xD, yD
            elif round(lengthDA, 5) < round(lengthDB, 5):
                return xA, yA
            elif round(lengthDA, 5) > round(lengthDB, 5):
                return xB, yB
        except:
            return None, None
        pass

    def Dissolve(self, fCTemp, outputDissolve, dissolveField):
        arcpy.Dissolve_management(in_features = fCTemp,
                                  out_feature_class = outputDissolve,
                                  dissolve_field = [dissolveField])
        pass

    # Xu ly nhung Point ma PolyLine da Remove, nhung de du quan he Topo voi Polygon thi nhung Point do can duoc giu lai
    def ProcessFeatureClassPointRemoveSubOne(self, featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp):
        # Make Feature Layer
        featureClassPolygon.SetFeatureClassSimplify()
        inFCPolygonSimplify = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolygon, featureClassPolygon.featureClassSimplify))
        if not arcpy.Exists(inFCPolygonSimplify) or int(arcpy.GetCount_management(inFCPolygonSimplify).getOutput(0)) == 0:
            return
        inFCPolygonSimplifyLayer = "inFCPolygonSimplifyLayer"
        #print inFCPolygonSimplify
        arcpy.MakeFeatureLayer_management(in_features = inFCPolygonSimplify,
                                          out_layer = inFCPolygonSimplifyLayer)
        featureClassPolyLine.SetFeatureClassPointRemove()
        inFCPolylinePointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassPointRemove))
        if not arcpy.Exists(inFCPolylinePointRemove) or int(arcpy.GetCount_management(inFCPolylinePointRemove).getOutput(0)) == 0:
            return
        inFCPolylinePointRemoveLayer = "inFCPolylinePointRemoveLayer"
        #print inFCPolylinePointRemove
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylinePointRemove,
                                          out_layer = inFCPolylinePointRemoveLayer)
        # Polygon To Polyline
        outFCPolygonToPolyline = "in_memory\\outFCPolygonToPolyline"
        #arcpy.FeatureToLine_management(in_features = inFCPolygonSimplifyLayer,
        #                               out_feature_class = outFCPolygonToPolyline,
        #                               cluster_tolerance = "0 Meters")
        arcpy.PolygonToLine_management(in_features = inFCPolygonSimplifyLayer,
                                       out_feature_class = outFCPolygonToPolyline)
        # Make Feature Layer
        outFCPolygonToPolylineLayer = "outFCPolygonToPolylineLayer"
        arcpy.MakeFeatureLayer_management(in_features = outFCPolygonToPolyline,
                                          out_layer = outFCPolygonToPolylineLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolylinePointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outFCPolygonToPolylineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Copy Feature Class
        outFCCopy = "in_memory\\outFCCopy"
        arcpy.CopyFeatures_management(in_features = inFCPolylinePointRemoveLayer,
                                      out_feature_class = outFCCopy)
        # Erase
        outErase = "in_memory\\outErase"
        arcpy.Erase_analysis(in_features = fCTemp,
                             erase_features = outFCCopy,
                             out_feature_class = outErase)
        # Copy Override
        arcpy.CopyFeatures_management(in_features = outErase,
                                      out_feature_class = fCTemp)
        pass

    # Xu ly nhung Point ma Polyline da khong Remove, nhung de du quan he Topo voi Polygon thi nhung Point do can duoc Remove
    def ProcessFeatureClassPointRemoveSubTwo(self, featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp):
        # Make Feature Layer
        featureClassPolyLine.SetFeatureClassSimplify()
        inFCPolylineSimplify = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassSimplify))
        if not arcpy.Exists(inFCPolylineSimplify) or int(arcpy.GetCount_management(inFCPolylineSimplify).getOutput(0)) == 0:
            return
        inFCPolylineSimplifyLayer = "inFCPolylineSimplifyLayer"
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylineSimplify,
                                          out_layer = inFCPolylineSimplifyLayer)
        featureClassPolygon.SetFeatureClassPointRemove()
        inFCPolygonPointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolygon, featureClassPolygon.featureClassPointRemove))
        if not arcpy.Exists(inFCPolygonPointRemove) or int(arcpy.GetCount_management(inFCPolygonPointRemove).getOutput(0)) == 0:
            return
        inFCPolygonPointRemoveLayer = "inFCPolygonPointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = inFCPolygonPointRemove,
                                          out_layer = inFCPolygonPointRemoveLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolygonPointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = inFCPolylineSimplifyLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Copy Feature Class
        outFCCopy = "in_memory\\outFCCopy"
        arcpy.CopyFeatures_management(in_features = inFCPolygonPointRemoveLayer,
                                      out_feature_class = outFCCopy)
        # Make Feature Layer
        outFCCopyLayer = "outFCCopyLayer"
        arcpy.MakeFeatureLayer_management(in_features = outFCCopy,
                                          out_layer = outFCCopyLayer)
        featureClassPolyLine.SetFeatureClassSimplifyAllPoint()
        inFCPolylineSimplifyAllPoint = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassSimplifyAllPoint))
        if not arcpy.Exists(inFCPolylineSimplifyAllPoint) or int(arcpy.GetCount_management(inFCPolylineSimplifyAllPoint).getOutput(0)) == 0:
            return
        inFCPolylineSimplifyAllPointLayer = "inFCPolylineSimplifyAllPointLayer"
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylineSimplifyAllPoint,
                                          out_layer = inFCPolylineSimplifyAllPointLayer)
        # Select Feature
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolylineSimplifyAllPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outFCCopyLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Insert Cursor
        fieldName = self.GetFieldFID(featureClassPolyLine.featureClass)
        with arcpy.da.SearchCursor(inFCPolylineSimplifyAllPointLayer, ["Shape@", fieldName]) as cursorA:
            with arcpy.da.InsertCursor(fCTemp, ["Shape@", fieldName]) as cursorB:
                for rowA in cursorA:
                    cursorB.insertRow((rowA[0], rowA[1]))
        pass

    def GetFieldFID(self, featureClass):
        return "FID_" + featureClass
        pass

    def CreateFileConfigTopo(self):
        arrTemp = []
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemConfigTopoC = ElemConfigTopoC(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemConfigTopoD = ElemConfigTopoD(fcTemp.baseName, False)
                    elemConfigTopoC.InsertElemListPolygon(elemConfigTopoD)
            if elemConfigTopoC.GetLength() > 0:
                arrTemp.append(elemConfigTopoC)

        configTopoTools = ConfigTopoTools()
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemConfigTopoA = ElemConfigTopoA(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    elemConfigTopoB = ElemConfigTopoB(fcTemp.baseName)
                    for itemTemp in arrTemp:
                        elemConfigTopoB.InsertElemListPolygon(itemTemp)
                    if elemConfigTopoB.GetLength() > 1:
                        elemConfigTopoA.InsertElemListPolyline(elemConfigTopoB)
            if elemConfigTopoA.GetLength() > 1:
                configTopoTools.InsertElemListConfig(elemConfigTopoA)

        textConfig = json.dumps(obj = configTopoTools.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileConfigTopo, "w")
        file.write(textConfig)
        file.close()
        pass

    def ReadFileConfigTopo(self):
        self.configTopoTools = ConfigTopoTools()
        file = open(self.pathFileConfigTopo, "r")
        textConfig = file.read()
        file.close()
        self.configTopoTools.InitFromDict(json.loads(textConfig))
        pass

class ConfigTopoTools:

    def __init__(self):
        self.listConfig = []

    def InsertElemListConfig(self, elemListConfig):
        self.listConfig.append(elemListConfig)

    def GetLength(self):
        return len(self.listConfig)
        pass

    def GetDict(self):
        listTemp = []
        for elemListConfig in self.listConfig:
            listTemp.append(elemListConfig.GetDict())
        return listTemp;

    def InitFromDict(self, dataJson):
        self.listConfig = []
        for elemListConfigTemp in dataJson:
            elemConfigTopoA = ElemConfigTopoA(elemListConfigTemp['featureDataSet'])
            for elemListPolylineTemp in elemListConfigTemp['listPolyline']:
                elemConfigTopoB = ElemConfigTopoB(elemListPolylineTemp['featureClass'])
                for elemListPolygonTopoTemp in elemListPolylineTemp['polygonTopos']:
                    elemConfigTopoC = ElemConfigTopoC(elemListPolygonTopoTemp['featureDataSet'])
                    for elemListPolygonTemp in elemListPolygonTopoTemp['listPolygon']:
                        elemConfigTopoD = ElemConfigTopoD(elemListPolygonTemp['featureClass'], elemListPolygonTemp['processTopo'])
                        elemConfigTopoC.InsertElemListPolygon(elemConfigTopoD)
                    elemConfigTopoB.InsertElemListPolygon(elemConfigTopoC)
                elemConfigTopoA.InsertElemListPolyline(elemConfigTopoB)
            self.InsertElemListConfig(elemConfigTopoA)

# Elem of ConfigTopoTools.listConfig
class ElemConfigTopoA:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolyline = []
        pass

    def InsertElemListPolyline(self, elemListPolyline):
        self.listPolyline.append(elemListPolyline)

    def GetLength(self):
        return len(self.listPolyline)
        pass

    def GetDict(self):
        listTempPolyline = []
        for elemList in self.listPolyline:
            listTempPolyline.append(elemList.GetDict())
        return {
            "featureDataSet": self.featureDataSet,
            "listPolyline": listTempPolyline
        }

# Elem of ElemConfigTopoA.listPolyline
class ElemConfigTopoB:

    def __init__(self, featureClass):
        self.featureClass = featureClass
        self.polygonTopos = []
        pass

    def InsertElemListPolygon(self, polygonTopo):
        self.polygonTopos.append(polygonTopo)
    
    def GetLength(self):
        return len(self.polygonTopos)
        pass

    def GetDict(self):
        listTempPolygon = []
        for elemList in self.polygonTopos:
            listTempPolygon.append(elemList.GetDict())
        return {
            "featureClass": self.featureClass,
            "polygonTopos": listTempPolygon
        }

# Elem of ElemConfigTopoB.listPolygon
class ElemConfigTopoC:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolygon = []
        pass

    def SetFeatureDataSet(self, featureDataSet):
        self.featureDataSet = featureDataSet
        pass

    def InsertElemListPolygon(self, elemListPolygon):
        self.listPolygon.append(elemListPolygon)

    def GetLength(self):
        return len(self.listPolygon)
        pass

    def GetDict(self):
        listTempPolygon = []
        for elemList in self.listPolygon:
            listTempPolygon.append(elemList.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolygon": listTempPolygon
        }

# Elem of ElemConfigTopoC.listPolygon
class ElemConfigTopoD:

    def __init__(self, featureClass, processTopo):
        self.featureClass = featureClass
        self.processTopo = processTopo
        pass
    
    def SetFeatureClassInMemory(self):
        self.featureClassInMemory = "in_memory\\" + self.featureClass
        pass

    def SetFeatureLayer(self):
        self.featureLayer = self.featureClass + "Layer"
        pass

    def SetFeatureClassAllPoint(self):
        self.featureClassAllPoint = self.featureClass + "_AllPoint"
        pass

    def SetFeatureClassSimplify(self):
        self.featureClassSimplify = self.featureClass + "_Simplify"
        pass

    def SetFeatureClassSimplifyAllPoint(self):
        self.featureClassSimplifyAllPoint = self.featureClass + "_Simplify_AllPoint"
        pass

    def SetFeatureClassPointRemove(self):
        self.featureClassPointRemove = self.featureClass + "_PointRemove"
        pass

    def SetFeatureClassPointRemoveDissolve(self):
        self.featureClassPointRemoveDissolve = self.featureClass + "_PointRemove_Dissolve"
        pass

class FeatureClass:

    def __init__(self, featureClass):
        self.featureClass = featureClass
        pass
    
    def SetFeatureClassInMemory(self):
        self.featureClassInMemory = "in_memory\\" + self.featureClass
        pass

    def SetFeatureLayer(self):
        self.featureLayer = self.featureClass + "Layer"
        pass

    def SetFeatureClassAllPoint(self):
        self.featureClassAllPoint = self.featureClass + "_AllPoint"
        pass

    def SetFeatureClassSimplify(self):
        self.featureClassSimplify = self.featureClass + "_Simplify"
        pass

    def SetFeatureClassSimplifyAllPoint(self):
        self.featureClassSimplifyAllPoint = self.featureClass + "_Simplify_AllPoint"
        pass

    def SetFeatureClassPointRemove(self):
        self.featureClassPointRemove = self.featureClass + "_PointRemove"
        pass

    def SetFeatureClassPointRemoveDissolve(self):
        self.featureClassPointRemoveDissolve = self.featureClass + "_PointRemove_Dissolve"
        pass

class RunTime:

    def __init__(self):
        self.startTime = time.time()
        print "Start time: {}".format(datetime.datetime.now())
        pass

    def GetTotalRunTime(self):
        self.totalRunTime = int(time.time() - self.startTime)
        self.ConvertTime()
        self.strHours = ""
        self.strMinute = ""
        self.strSeconds = ""
        if self.hours / 10 == 0:
            self.strHours = "0" + str(self.hours)
        else:
            self.strHours = str(self.hours)
        if self.minute / 10 == 0:
            self.strMinute = "0" + str(self.minute)
        else:
            self.strMinute = str(self.minute)
        if self.seconds / 10 == 0:
            self.strSeconds = "0" + str(self.seconds)
        else:
            self.strSeconds = str(self.seconds)
        print "Total time: {0}:{1}:{2}".format(self.strHours, self.strMinute, self.strSeconds)
        pass

    def ConvertTime(self):
        self.hours = self.totalRunTime / (60 * 60)
        self.totalRunTime = self.totalRunTime - (self.hours * 60 * 60)
        self.minute = self.totalRunTime / 60
        self.totalRunTime = self.totalRunTime - (self.minute * 60)
        self.seconds = self.totalRunTime
        pass

if __name__ == '__main__':
    runTime = RunTime()
    updatePointRemovePolyline = UpdatePointRemovePolyline()
    print "Running..."
    updatePointRemovePolyline.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass