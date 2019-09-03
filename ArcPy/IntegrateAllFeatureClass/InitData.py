# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class InitData:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigSimplify.json")
        self.pathFileConfigTopo = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigTopo.json")
        # Read File Config Simplify
        if not os.path.isfile(self.pathFileConfig):
            print "... Not Found: " + self.pathFileConfig + "?\n  ... Create File ConfigSimplify..."
            self.CreateFileConfig()
        self.ReadFileConfig()
        # Read File Config Process Topo
        if not os.path.isfile(self.pathFileConfigTopo):
            print "... Not Found: " + self.pathFileConfigTopo + "?\n  ... Create File ConfigTopo..."
            self.CreateFileConfigTopo()
        self.ReadFileConfigTopo()
        print "OK init: InitData"
        pass

    def Execute(self):
        # Init Workspace
        arcpy.env.overwriteOutput = True

        # Integrate
        print "# Integrate"
        ## Process
        print "   ## Process"
        arrLayerPolygon, arrLayerPolyline = self.MakeFeatureLayer(self.pathProcessGDB)
        self.Integrate(arrLayerPolyline, arrLayerPolygon)
        self.Integrate(arrLayerPolygon, arrLayerPolyline)
        ## Clean InMemory
        print "   ## Clean InMemory"
        arcpy.Delete_management(in_data = "in_memory")
        ## Final
        print "   ## Final"
        arrLayerPolygon, arrLayerPolyline = self.MakeFeatureLayer(self.pathFinalGDB)
        self.Integrate(arrLayerPolyline, arrLayerPolygon)
        self.Integrate(arrLayerPolygon, arrLayerPolyline)
        ## Clean InMemory
        print "   ## Clean InMemory"
        arcpy.Delete_management(in_data = "in_memory")

        # PolyLine
        print "# PolyLine"
        ## Merge All Polyline
        print "   ## Merge All Polyline"
        inFC_SimplifyAllPolyline = self.MergeFeatureClass("Polyline")
        ## Simplify All Polyline
        print "   ## Simplify All Polyline"
        inFC_ExportFC = self.SimplifyAllPolyline(inFC_SimplifyAllPolyline)
        ## Export FeatureClass After Simplify
        print "   ## Export FeatureClass After Simplify"
        self.ExportFeatureClassAfterSimplify("Polyline", inFC_ExportFC)
        ## Create FeatureClass PointRemove
        print "   ## Create FeatureClass PointRemove"
        self.FeatureClassSimplifyToPoint("Polyline")
        self.ErasePoint("Polyline")
        ## Clean InMemory
        print "   ## Clean InMemory"
        arcpy.Delete_management(in_data = "in_memory")

        # Polygon
        print "# Polygon"
        ## Merge All Polygon
        print "   ## Merge All Polygon"
        inFC_SimplifyAllPolygon = self.MergeFeatureClass("Polygon")
        ## Simplify All Polygon
        print "   ## Simplify All Polygon"
        inFC_ExportFC = self.SimplifyAllPolygon(inFC_SimplifyAllPolygon)
        ## Export FeatureClass After Simplify
        print "   ## Export FeatureClass After Simplify"
        self.ExportFeatureClassAfterSimplify("Polygon", inFC_ExportFC)
        ## Create FeatureClass PointRemove
        print "   ## Create FeatureClass PointRemove"
        self.FeatureClassSimplifyToPoint("Polygon")
        self.ErasePoint("Polygon")
        ## Clean InMemory
        print "   ## Clean InMemory"
        arcpy.Delete_management(in_data = "in_memory")
        pass

    # Point ma Polygon remove ma Polyline phai update
    def UpdatePointPolyline(self):
        for elemConfigTopo in self.configTopoTools.listConfig:
            featureDataSetPolyLine = elemConfigTopo.featureDataSet
            for elemPolyline in elemConfigTopo.listPolyline:
                featureClassPolyLine = FeatureClass(elemPolyline.featureClass)
                print "# {}".format(featureClassPolyLine.featureClass)
                pathFinalPolyline = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetPolyLine), featureClassPolyLine.featureClass)
                if not arcpy.Exists(pathFinalPolyline) or int(arcpy.GetCount_management(pathFinalPolyline).getOutput(0)) == 0 \
                    or not arcpy.Exists(inPathPointRemove) or int(arcpy.GetCount_management(inPathPointRemove).getOutput(0)) == 0:
                    continue
                pathFinalPolylineAllPoint = "in_memory\\polylineAllPoint"
                arcpy.FeatureVerticesToPoints_management(in_features = pathFinalPolyline,
                                                         out_feature_class = pathFinalPolylineAllPoint,
                                                         point_location = "ALL")
                pathFinalPolylineAllPointLayer = "pathFinalPolylineAllPointLayer"
                arcpy.MakeFeatureLayer_management(in_features = pathFinalPolylineAllPoint,
                                                  out_layer = pathFinalPolylineAllPointLayer)
                for elemPolygonTopo in elemPolyline.polygonTopos:
                    featureDataSetPolygon = elemPolygonTopo.featureDataSet
                    for elemPolygon in elemPolygonTopo.listPolygon:
                        featureClassPolygon = FeatureClass(elemPolygon.featureClass)
                        if elemPolygon.processTopo == True:
                            featureClassPolygon.SetFeatureClassPointRemove()
                            polygonPointRemove = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClassPointRemove)
                            polygonPointRemoveLayer = "polygonPointRemoveLayer"
                            arcpy.MakeFeatureLayer_management(in_features = polygonPointRemove,
                                                              out_layer = polygonPointRemoveLayer)
                            arcpy.SelectLayerByLocation_management(in_layer = polygonPointRemoveLayer,
                                                                   overlap_type = "INTERSECT",
                                                                   select_features = pathFinalPolylineAllPointLayer,
                                                                   search_distance = "0 Meters")
        pass

    def ProcessPointInLine(self, inPathPolylineFC, inPathPolygonPointRemove, featureDataSetPolygon, featureClassPolygon, fID):
        # ORIG_FID
        outPutPoint = "in_memory\\outPutPoint"
        arcpy.FeatureVerticesToPoints_management(in_features = inPathPolylineFC,
                                                 out_feature_class = outPutPoint,
                                                 point_location = "ALL")
        if int(arcpy.GetCount_management(outPutPoint).getOutput(0)) == 0:
            return
        outPutPointLayer = "outPutPointLayer"
        arcpy.MakeFeatureLayer_management(in_features = outPutPoint,
                                          out_layer = outPutPointLayer)
        inPathPolygonPointRemoveLayer = "inPathPolygonPointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = inPathPolygonPointRemove,
                                          out_layer = inPathPolygonPointRemoveLayer)
        #
        arcpy.SelectLayerByLocation_management(in_layer = outPutPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = inPathPolygonPointRemoveLayer,
                                               search_distance = "0 Meters")
        if int(arcpy.GetCount_management(outPutPointLayer).getOutput(0)) == 0:
            return
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
        # Remove Point in arrPolygon
        indexPartNum = 0
        for indexPart in arrIndexPart:
            indexPointInPartNum = 0
            for indexPointInPart in indexPart:
                arrPolygon[indexPartNum].remove(indexPointInPart - indexPointInPartNum)
                indexPointInPartNum += 1
            indexPartNum += 1
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
                return None, None
            elif round(lengthDA, 5) < round(lengthDB, 5):
                return xA, yA
            elif round(lengthDA, 5) > round(lengthDB, 5):
                return xB, yB
        except:
            return None, None
        pass

    def ErasePoint(self, option):
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if (tempPolygon.runFeatureClass == False):
                        continue
                    tempPolygon.SetFeatureClassAllPoint()
                    tempPolygon.SetFeatureClassSimplifyAllPoint()
                    tempPolygon.SetFeatureClassPointRemove()
                    pathInFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassAllPoint)
                    pathEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplifyAllPoint)
                    pathOutEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassPointRemove)
                    if not arcpy.Exists(pathInFeature):
                        continue
                    if not arcpy.Exists(pathEraseFeature):
                        continue
                    #print pathOutEraseFeature
                    arcpy.Erase_analysis(in_features = pathInFeature,
                                         erase_features = pathEraseFeature,
                                         out_feature_class = pathOutEraseFeature,
                                         cluster_tolerance = "0.00000 Meters")
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if (tempPolyline.runFeatureClass == False):
                        continue
                    tempPolyline.SetFeatureClassAllPoint()
                    tempPolyline.SetFeatureClassSimplifyAllPoint()
                    tempPolyline.SetFeatureClassPointRemove()
                    pathInFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassAllPoint)
                    pathEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplifyAllPoint)
                    pathOutEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassPointRemove)
                    if not arcpy.Exists(pathInFeature):
                        continue
                    if not arcpy.Exists(pathEraseFeature):
                        continue
                    #print pathOutEraseFeature
                    arcpy.Erase_analysis(in_features = pathInFeature,
                                         erase_features = pathEraseFeature,
                                         out_feature_class = pathOutEraseFeature,
                                         cluster_tolerance = "0.00000 Meters")
        pass

    def FeatureClassSimplifyToPoint(self, option):
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if (tempPolygon.runFeatureClass == False):
                        continue
                    tempPolygon.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplify)
                    if not arcpy.Exists(pathFcOrigin):
                        continue
                    if int(arcpy.GetCount_management(pathFcOrigin).getOutput(0)) == 0:
                        continue
                    tempPolygon.SetFeatureClassSimplifyAllPoint()
                    pathOutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplifyAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = pathFcOrigin,
                                                             out_feature_class = pathOutFVToPoint,
                                                             point_location = "ALL")
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if (tempPolyline.runFeatureClass == False):
                        continue
                    tempPolyline.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplify)
                    if not arcpy.Exists(pathFcOrigin):
                        continue
                    if int(arcpy.GetCount_management(pathFcOrigin).getOutput(0)) == 0:
                        continue
                    if not arcpy.Exists(pathFcOrigin):
                        continue
                    if int(arcpy.GetCount_management(pathFcOrigin).getOutput(0)) == 0:
                        continue
                    tempPolyline.SetFeatureClassSimplifyAllPoint()
                    pathOutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplifyAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = pathFcOrigin,
                                                             out_feature_class = pathOutFVToPoint,
                                                             point_location = "ALL")
        pass

    def SimplifyAllPolyline(self, inFC_SimplifyAllPolyline):
        outPutSimplify = os.path.join(self.pathProcessGDB, "AllPolyline_Simplify")
        arcpy.SimplifyLine_cartography(in_features = inFC_SimplifyAllPolyline,
                                       out_feature_class = outPutSimplify,
                                       algorithm = "BEND_SIMPLIFY",
                                       tolerance = "50 Meters",
                                       collapsed_point_option = "NO_KEEP")
        return outPutSimplify
        pass

    def SimplifyAllPolygon(self, inFC_SimplifyAllPolygon):
        outPutSimplify = os.path.join(self.pathProcessGDB, "AllPolygon_Simplify")
        arcpy.SimplifyPolygon_cartography(in_features = inFC_SimplifyAllPolygon,
                                          out_feature_class = outPutSimplify,
                                          algorithm = "BEND_SIMPLIFY",
                                          tolerance = "50 Meters",
                                          error_option = "RESOLVE_ERRORS",
                                          collapsed_point_option = "NO_KEEP")
        return outPutSimplify
        pass

    def ExportFeatureClassAfterSimplify(self, option, inFC_ExportFC):
        outMergeSimplifyLayer = "outMergeSimplifyLayer"
        arcpy.MakeFeatureLayer_management(in_features = inFC_ExportFC,
                                          out_layer = outMergeSimplifyLayer)
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if tempPolygon.runFeatureClass == False:
                        continue
                    # Create Feature Class
                    tempPolygon.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                    if not arcpy.Exists(pathFcOrigin):
                        continue
                    if int(arcpy.GetCount_management(pathFcOrigin).getOutput(0)) == 0:
                        continue
                    outPath = os.path.join(self.pathProcessGDB, tempConfig.featureDataSet)
                    outName = tempPolygon.featureClassSimplify
                    pathFcSimplify = os.path.join(outPath, outName)
                    arcpy.CreateFeatureclass_management(out_path = outPath,
                                                        out_name = outName,
                                                        geometry_type = "Polygon",
                                                        spatial_reference = arcpy.Describe(pathFcOrigin).spatialReference)
                    fieldFID, fieldType = self.GetFieldFID(tempPolygon.featureClass, "LONG")
                    arcpy.AddField_management(pathFcSimplify, fieldFID, fieldType)
                    # Select
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "CLEAR_SELECTION")
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "NEW_SELECTION",
                                                            where_clause = fieldFID + " IS NOT NULL")
                    #print pathFcSimplify
                    with arcpy.da.SearchCursor(outMergeSimplifyLayer, ["Shape@", fieldFID]) as cursorSearch:
                        with arcpy.da.InsertCursor(pathFcSimplify, ["Shape@", fieldFID]) as cursorInsert:
                            for rowSearch in cursorSearch:
                                cursorInsert.insertRow((rowSearch[0], rowSearch[1]))
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if tempPolyline.runFeatureClass == False:
                        continue
                    # Create Feature Class
                    tempPolyline.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClass)
                    if not arcpy.Exists(pathFcOrigin):
                        continue
                    if int(arcpy.GetCount_management(pathFcOrigin).getOutput(0)) == 0:
                        continue
                    outPath = os.path.join(self.pathProcessGDB, tempConfig.featureDataSet)
                    outName = tempPolyline.featureClassSimplify
                    pathFcSimplify = os.path.join(outPath, outName)
                    arcpy.CreateFeatureclass_management(out_path = outPath,
                                                        out_name = outName,
                                                        geometry_type = "Polyline",
                                                        spatial_reference = arcpy.Describe(pathFcOrigin).spatialReference)
                    fieldFID, fieldType = self.GetFieldFID(tempPolyline.featureClass, "LONG")
                    arcpy.AddField_management(pathFcSimplify, fieldFID, fieldType)
                    # Select
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "CLEAR_SELECTION")
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "NEW_SELECTION",
                                                            where_clause = fieldFID + " IS NOT NULL")
                    #print pathFcSimplify
                    with arcpy.da.SearchCursor(outMergeSimplifyLayer, ["Shape@", fieldFID]) as cursorSearch:
                        with arcpy.da.InsertCursor(pathFcSimplify, ["Shape@", fieldFID]) as cursorInsert:
                            for rowSearch in cursorSearch:
                                cursorInsert.insertRow((rowSearch[0], rowSearch[1]))
        pass

    def MergeFeatureClass(self, option):
        inFeatureClassMerges = []
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if tempPolygon.runFeatureClass == False:
                        continue
                    # Add Field FID_XXX For Feature Class
                    pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                    if not arcpy.Exists(pathFc):
                        continue
                    if int(arcpy.GetCount_management(pathFc).getOutput(0)) == 0:
                        continue
                    #print pathFc
                    fieldFID, fieldType = self.GetFieldFID(tempPolygon.featureClass, "LONG")
                    arcpy.AddField_management(pathFc, fieldFID, fieldType)
                    # Update Field FID_XXX
                    with arcpy.da.UpdateCursor(pathFc, ['OID@', fieldFID]) as cursor:
                        for row in cursor:
                            row[1] = row[0]
                            cursor.updateRow(row)
                    # Copy FeatureClass to in_memory
                    tempPolygon.SetFeatureClassInMemory()
                    arcpy.CopyFeatures_management(in_features = pathFc, out_feature_class = tempPolygon.featureClassInMemory)
                    # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                    fields = arcpy.ListFields(tempPolygon.featureClassInMemory)
                    fieldsDelete = []
                    for fieldTemp in fields:
                        if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                            fieldsDelete.append(fieldTemp.name)
                    arcpy.DeleteField_management(in_table = tempPolygon.featureClassInMemory, drop_field = fieldsDelete)
                    # Feature Vertices To Point
                    tempPolygon.SetFeatureClassAllPoint()
                    outPutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = tempPolygon.featureClassInMemory,
                                                             out_feature_class = outPutFVToPoint,
                                                             point_location = "ALL")
                    # FeatureClass Delete Field FID_XXX
                    arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                    # Maker Layer
                    inFeatureClassMerges.append(tempPolygon.featureClassInMemory)
            # Merge
            outputMerge = os.path.join(self.pathProcessGDB, "PolygonMerge")
            arcpy.Merge_management(inputs = inFeatureClassMerges,
                                   output = outputMerge)
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if tempPolyline.runFeatureClass == False:
                        continue
                    # Add Field FID_XXX For Feature Class
                    pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClass)
                    if not arcpy.Exists(pathFc):
                        continue
                    if int(arcpy.GetCount_management(pathFc).getOutput(0)) == 0:
                        continue
                    #print pathFc
                    fieldFID, fieldType = self.GetFieldFID(tempPolyline.featureClass, "LONG")
                    arcpy.AddField_management(pathFc, fieldFID, fieldType)
                    # Update Field FID_XXX
                    with arcpy.da.UpdateCursor(pathFc, ['OID@', fieldFID]) as cursor:
                        for row in cursor:
                            row[1] = row[0]
                            cursor.updateRow(row)
                    # Copy FeatureClass to in_memory
                    tempPolyline.SetFeatureClassInMemory()
                    arcpy.CopyFeatures_management(in_features = pathFc, out_feature_class = tempPolyline.featureClassInMemory)
                    # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                    fields = arcpy.ListFields(tempPolyline.featureClassInMemory)
                    fieldsDelete = []
                    for fieldTemp in fields:
                        if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                            fieldsDelete.append(fieldTemp.name)
                    arcpy.DeleteField_management(in_table = tempPolyline.featureClassInMemory, drop_field = fieldsDelete)
                    # Feature Vertices To Point
                    tempPolyline.SetFeatureClassAllPoint()
                    outPutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = tempPolyline.featureClassInMemory,
                                                             out_feature_class = outPutFVToPoint,
                                                             point_location = "ALL")
                    # FeatureClass Delete Field FID_XXX
                    arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                    # Maker Layer
                    inFeatureClassMerges.append(tempPolyline.featureClassInMemory)
            # Merge
            outputMerge = os.path.join(self.pathProcessGDB, "PolylineMerge")
            arcpy.Merge_management(inputs = inFeatureClassMerges,
                                   output = outputMerge)
        return outputMerge
        pass

    def MakeFeatureLayer(self, pathGDB):
        arrLayerPolygon = []
        arrLayerPolyline = []
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runFeatureClass == False:
                    continue
                tempPolygon.SetFeatureLayer()
                pathPolygon = os.path.join(pathGDB, os.path.join(tempConfig.featureDataSet, tempPolygon.featureClass))
                if not arcpy.Exists(pathPolygon):
                    continue
                if int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
                    continue
                arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                                  out_layer = tempPolygon.featureLayer)
                arrLayerPolygon.append(tempPolygon.featureLayer)
            for tempPolyline in tempConfig.listPolyline:
                if tempPolyline.runFeatureClass == False:
                    continue
                tempPolyline.SetFeatureLayer()
                pathPolyline = os.path.join(pathGDB, os.path.join(tempConfig.featureDataSet, tempPolyline.featureClass))
                if not arcpy.Exists(pathPolyline):
                    continue
                if int(arcpy.GetCount_management(pathPolyline).getOutput(0)) == 0:
                    continue
                arcpy.MakeFeatureLayer_management(in_features = pathPolyline,
                                                  out_layer = tempPolyline.featureLayer)
                arrLayerPolyline.append(tempPolyline.featureLayer)
        return arrLayerPolygon, arrLayerPolyline
        pass

    def Integrate(self, arrOne, arrTwo):
        arrInput = []
        for item in arrOne:
            arrInput.append([item, "1"])
        for item in arrTwo:
            arrInput.append([item, "2"])
        arcpy.Integrate_management(in_features = arrInput,
                                   cluster_tolerance = "0.00000 Meters")
        pass

    def GetFieldFID(self, featureClass, fieldType):
        return "FID_" + featureClass, fieldType
        pass

    def CreateFileConfig(self):
        self.configTools = ConfigTools()
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemListConfig = ElemListConfig(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemListPolygon = ElemList(fcTemp.baseName, True)
                    elemListConfig.InsertElemListPolygon(elemListPolygon)
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    elemListPolyline = ElemList(fcTemp.baseName, True)
                    elemListConfig.InsertElemListPolyline(elemListPolyline)
            if len(elemListConfig.listPolygon) > 0:
                self.configTools.InsertElemListConfig(elemListConfig)
        textConfig = json.dumps(obj = self.configTools.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileConfig, "w")
        file.write(textConfig)
        file.close()
        pass

    def ReadFileConfig(self):
        self.configTools = ConfigTools()
        file = open(self.pathFileConfig, "r")
        textConfig = file.read()
        file.close()
        self.configTools.InitFromDict(json.loads(textConfig))
        pass

    def ReadFileConfigTopo(self):
        self.configTopoTools = ConfigTopoTools()
        file = open(self.pathFileConfigTopo, "r")
        textConfig = file.read()
        file.close()
        self.configTopoTools.InitFromDict(json.loads(textConfig))
        pass

class ConfigTools:

    def __init__(self):
        self.listConfig = []

    def InsertElemListConfig(self, elemListConfig):
        self.listConfig.append(elemListConfig)

    def GetDict(self):
        listTemp = []
        for elemListConfig in self.listConfig:
            listTemp.append(elemListConfig.GetDict())
        return listTemp;

    def InitFromDict(self, dataJson):
        self.listConfig = []
        for elemListConfigTemp in dataJson:
            elemListConfig = ElemListConfig(elemListConfigTemp['featureDataSet'])
            for elemListPolygonTemp in elemListConfigTemp['listPolygon']:
                elemListPolygon = ElemList(elemListPolygonTemp['featureClass'], elemListPolygonTemp['runFeatureClass'])
                elemListConfig.InsertElemListPolygon(elemListPolygon)
            for elemListPolygonTemp in elemListConfigTemp['listPolyline']:
                elemListPolyline = ElemList(elemListPolygonTemp['featureClass'], elemListPolygonTemp['runFeatureClass'])
                elemListConfig.InsertElemListPolyline(elemListPolyline)
            self.InsertElemListConfig(elemListConfig)

class ElemListConfig:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolygon = []
        self.listPolyline = []

    def InsertElemListPolygon(self, elemListPolygon):
        self.listPolygon.append(elemListPolygon)

    def InsertElemListPolyline(self, elemListPolyline):
        self.listPolyline.append(elemListPolyline)

    def GetDict(self):
        listTempPolygon = []
        listTempPolyline = []
        for elemList in self.listPolygon:
            listTempPolygon.append(elemList.__dict__)
        for elemList in self.listPolyline:
            listTempPolyline.append(elemList.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolygon": listTempPolygon,
            "listPolyline": listTempPolyline
        }

class ElemList:

    def __init__(self, featureClass, runFeatureClass):
        self.featureClass = featureClass
        self.runFeatureClass = runFeatureClass
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

    def SetFeatureClassPointRemoveOne(self):
        self.featureClassPointRemoveOne = self.featureClass + "_PointRemove_One"
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
    initData = InitData()
    print "Running..."
    initData.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass