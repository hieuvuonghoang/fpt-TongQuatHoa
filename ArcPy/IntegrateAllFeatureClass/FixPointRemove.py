# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import hashlib
import datetime

class FixPointRemove:

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
        # CreatePointRemoveUnique
        #self.CreatePointRemoveUnique()
        #arcpy.Delete_management("in_memory")
        #
        #self.UpdatePoint()
        self.CreatePoint(292585.8117, 2347403.0036, 292511.87, 2347387.1542, 292553.5659, 2347399.6376)
        pass

    def CreatePointRemoveUnique(self):
        for elemConfigTopo in self.configTopoTools.listConfig:
            featureDataSetPolyLine = elemConfigTopo.featureDataSet
            for elemPolyline in elemConfigTopo.listPolyline:
                featureClassPolyLine = FeatureClass(elemPolyline.featureClass)
                featureClassPolyLine.SetFeatureClassPointRemoveDissolve()
                inPathFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolve)
                if not arcpy.Exists(inPathFc) or int(arcpy.GetCount_management(inPathFc).getOutput(0)) == 0:
                    continue
                fCTemp = "in_memory\\fCTemp"
                arcpy.MultipartToSinglepart_management(in_features = inPathFc,
                                                       out_feature_class = fCTemp)
                if int(arcpy.GetCount_management(fCTemp).getOutput(0)) == 0:
                    continue
                # MD5 Shape@XY: Point
                arcpy.AddField_management(in_table = fCTemp,
                                          field_name = "MD5",
                                          field_type = "Text",
                                          field_length = "32")
                with arcpy.da.UpdateCursor(fCTemp, ["Shape@XY", "MD5"]) as cursor:
                    for row in cursor:
                       x, y = row[0]
                       strPoint = str(x) + str(y)
                       row[1] = str(hashlib.md5(strPoint.encode()).hexdigest())
                       cursor.updateRow(row)
                # Statistics
                tableTemp = "in_memory\\tableTemp"
                arcpy.Statistics_analysis(in_table = fCTemp,
                                          out_table = tableTemp,
                                          statistics_fields = [["OBJECTID", "FIRST"]],
                                          case_field = "MD5")
                # Join
                fCTempLayer = "fCTempLayer"
                arcpy.MakeFeatureLayer_management(in_features = fCTemp,
                                                  out_layer = fCTempLayer)
                arcpy.AddJoin_management(in_layer_or_view = fCTempLayer,
                                        in_field = "OBJECTID",
                                        join_table = tableTemp,
                                        join_field = "FIRST_OBJECTID")
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "tableTemp.FIRST_OBJECTID IS NOT NULL")
                arcpy.RemoveJoin_management(in_layer_or_view = fCTempLayer,
                                            join_name = "tableTemp")
                #
                featureClassPolyLine.SetFeatureClassPointRemoveDissolveSingelUnique()
                outPutUniqueFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolveSingelUnique)
                arcpy.CopyFeatures_management(in_features = fCTempLayer,
                                              out_feature_class = outPutUniqueFc)
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempLayer,
                                                        selection_type = "CLEAR_SELECTION")
                featureClassPolyLine.SetFeatureClassPointRemoveDissolveSingel()
                outPutFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolveSingel)
                arcpy.CopyFeatures_management(in_features = fCTempLayer,
                                              out_feature_class = outPutFc)
        pass

    def UpdatePoint(self):
        for elemConfigTopo in self.configTopoTools.listConfig:
            featureDataSetPolyLine = elemConfigTopo.featureDataSet
            for elemPolyline in elemConfigTopo.listPolyline:
                featureClassPolyLine = FeatureClass(elemPolyline.featureClass)
                featureClassPolyLine.SetFeatureClassPointRemoveDissolveSingelUnique()
                inPathFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolveSingelUnique)
                if not arcpy.Exists(inPathFc) or int(arcpy.GetCount_management(inPathFc).getOutput(0)) == 0:
                    continue
                #
                fCUniqueLayer = "fCUniqueLayer"
                arcpy.MakeFeatureLayer_management(in_features = inPathFc,
                                                  out_layer = fCUniqueLayer)
                for elemPolygonTopo in elemPolyline.polygonTopos:
                    featureDataSetPolygon = elemPolygonTopo.featureDataSet
                    for elemPolygon in elemPolygonTopo.listPolygon:
                        if elemPolygon.processTopo == True:
                            featureClassPolygon = FeatureClass(elemPolygon.featureClass)
                            pathPolygon = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClass)
                            polygonLayer = "polygonLayer"
                            arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                                              out_layer = polygonLayer)
                            featureClassPolygon.SetFeatureClassPointRemove()
                            pathPolygonPointRemove = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClassPointRemove)
                            polygonPointRemoveLayer = "polygonPointRemoveLayer"
                            arcpy.MakeFeatureLayer_management(in_features = pathPolygonPointRemove,
                                                              out_layer = polygonPointRemoveLayer)
                            with arcpy.da.SearchCursor(fCUniqueLayer, ["OID@", "Shape@XY"]) as cursor:
                                for row in cursor:
                                    strQuery = "OBJECTID = " + str(row[0])
                                    x, y = row[1]
                                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCUniqueLayer,
                                                                            selection_type = "NEW_SELECTION",
                                                                            where_clause = strQuery)
                                    arcpy.SelectLayerByLocation_management(in_layer = polygonLayer,
                                                                           overlap_type = "INTERSECT",
                                                                           select_features = fCUniqueLayer,
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
                                    print strQuery
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
                                    print "{}, {}".format(str(x), str(y))
                                    print "{}, {}".format(str(pntBefore.X), str(pntBefore.Y))
                                    print "{}, {}".format(str(pntAfter.X), str(pntAfter.Y))
                            pass
        pass

    def CreatePoint(self, xA, yA, xB, yB, xC, yC):
        a = round((yB - yA) / (xB - xA), 10)
        b = round(yA - (a * xA), 10)
        c = -xC - (a*yC);
        print "x + {}*y + {} = 0".format(str(a), str(c))
        x = round((xC + (a*yC) - (a*b)) / (a*a + 1), 10)
        y = round(a*x + b, 10)
        print "{}, {}".format(x, y)
        return x, x
        pass

    def Fix(self):
        for elemConfigTopo in self.configTopoTools.listConfig:
            featureDataSetPolyLine = elemConfigTopo.featureDataSet
            for elemPolyline in elemConfigTopo.listPolyline:
                featureClassPolyLine = FeatureClass(elemPolyline.featureClass)
                featureClassPolyLine.SetFeatureClassPointRemoveDissolve()
                inPathFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolve)
                if not arcpy.Exists(inPathFc) or int(arcpy.GetCount_management(inPathFc).getOutput(0)) == 0:
                    continue
                fCTemp = "in_memory\\fCTemp"
                arcpy.MultipartToSinglepart_management(in_features = inPathFc,
                                                       out_feature_class = fCTemp)
                if int(arcpy.GetCount_management(fCTemp).getOutput(0)) == 0:
                    continue
                # MD5 Shape@XY: Point
                arcpy.AddField_management(in_table = fCTemp,
                                          field_name = "MD5",
                                          field_type = "Text",
                                          field_length = "32")
                with arcpy.da.UpdateCursor(fCTemp, ["Shape@XY", "MD5"]) as cursor:
                    for row in cursor:
                       x, y = row[0]
                       strPoint = str(x) + str(y)
                       row[1] = str(hashlib.md5(strPoint.encode()).hexdigest())
                       cursor.updateRow(row)
                # Statistics
                tableTemp = "in_memory\\tableTemp"
                arcpy.Statistics_analysis(in_table = fCTemp,
                                          out_table = tableTemp,
                                          statistics_fields = [["OBJECTID", "FIRST"]],
                                          case_field = "MD5")
                # Join
                fCTempLayer = "fCTempLayer"
                arcpy.MakeFeatureLayer_management(in_features = fCTemp,
                                                  out_layer = fCTempLayer)
                arcpy.AddJoin_management(in_layer_or_view = fCTempLayer,
                                        in_field = "OBJECTID",
                                        join_table = tableTemp,
                                        join_field = "FIRST_OBJECTID")
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "tableTemp.FIRST_OBJECTID IS NOT NULL")
                arcpy.RemoveJoin_management(in_layer_or_view = fCTempLayer,
                                            join_name = "tableTemp")
                #
                featureClassPolyLine.SetFeatureClassPointRemoveDissolveSingelUnique()
                outPutUniqueFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolveSingelUnique)
                arcpy.CopyFeatures_management(in_features = fCTempLayer,
                                              out_feature_class = outPutUniqueFc)
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempLayer,
                                                        selection_type = "CLEAR_SELECTION")
                featureClassPolyLine.SetFeatureClassPointRemoveDissolveSingel()
                outPutFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolveSingel)
                arcpy.CopyFeatures_management(in_features = fCTempLayer,
                                              out_feature_class = outPutFc)
                #
                fCUniqueLayer = "fCUniqueLayer"
                arcpy.MakeFeatureLayer_management(in_features = outPutUniqueFc,
                                                  out_layer = fCUniqueLayer)
                for elemPolygonTopo in elemPolyline.polygonTopos:
                    featureDataSetPolygon = elemPolygonTopo.featureDataSet
                    for elemPolygon in elemPolygonTopo.listPolygon:
                        if elemPolygon.processTopo == True:
                            featureClassPolygon = FeatureClass(elemPolygon.featureClass)
                            pathPolygon = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClass)
                            polygonLayer = "polygonLayer"
                            arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                                              out_layer = polygonLayer)
                            featureClassPolygon.SetFeatureClassPointRemove()
                            pathPolygonPointRemove = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolygon), featureClassPolygon.featureClassPointRemove)
                            polygonPointRemoveLayer = "polygonPointRemoveLayer"
                            arcpy.MakeFeatureLayer_management(in_features = pathPolygonPointRemove,
                                                              out_layer = polygonPointRemoveLayer)
                            with arcpy.da.SearchCursor(fCUniqueLayer, ["OID@", "Shape@XY"]) as cursor:
                                for row in cursor:
                                    strQuery = "OBJECTID = " + str(row[0])
                                    x, y = row[1]
                                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCUniqueLayer,
                                                                            selection_type = "NEW_SELECTION",
                                                                            where_clause = strQuery)
                                    arcpy.SelectLayerByLocation_management(in_layer = polygonLayer,
                                                                           overlap_type = "INTERSECT",
                                                                           select_features = fCUniqueLayer,
                                                                           search_distance = "0 Meters")
                                    if int(arcpy.GetCount_management(polygonLayer).getOutput(0)) == 0:
                                        continue
                                    arrPoint = None
                                    fIDPolygon = None
                                    with arcpy.da.SearchCursor(polygonLayer, ["Shape@", "OID@"]) as cursorPolgonLayer:
                                        for rowPolygonLayer in cursorPolgonLayer:
                                            for part in rowPolygonLayer[0]:
                                                indexPnt = 0
                                                for pnt in part:
                                                    if pnt.X == x and pnt.Y == y:
                                                        #print "{}, {}; {}, {}".format(str(x), str(y), str(pnt.X), str(pnt.Y))
                                                        arrPoint = part
                                                        fIDPolygon = rowPolygonLayer[1]
                                                        break
                                                    indexPnt += 1
                                    if arrPoint == None:
                                        continue

                                    for pnt in arrPoint:
                                        print "{}, {}".format(str(pnt.X), str(pnt.Y))
                                    continue

                                    fieldName = self.GetFieldFID(featureClassPolygon.featureClass)
                                    strQuery = str(fieldName) + " = " + str(fIDPolygon)
                                    print strQuery
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
                                    print arrIndexRemove
                                    print "Leng arr Before: {}".format(str(arrPoint.count))
                                    indexRemoveSub = 0
                                    for indexRemove in arrIndexRemove:
                                        arrPoint.remove(indexRemove - indexRemoveSub)
                                        indexRemoveSub += 1
                                    print "Leng arr After: {}".format(str(arrPoint.count))
                                    indexPnt = 0
                                    for pnt in arrPoint:
                                        if x == pnt.X and y == pnt.Y:
                                            indexPnt += 1
                                            break
                                    pntBefore = arrPoint.getObject(indexPnt - 1)
                                    pntAfter = arrPoint.getObject(indexPnt + 1)
                                    print type(pntBefore)
                                    print type(pntAfter)
                                    print "{}, {}".format(str(pntBefore.X), str(pntBefore.X))
                                    print "{}, {}".format(str(pntAfter.X), str(pntAfter.X))
                            pass
                #featureClassPolyLine.SetFeatureClassPointRemoveDissolve()
                #outputDissolve = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolve)
                #fieldName = self.GetFieldFID(featureClassPolyLine.featureClass)
                #self.Dissolve(fCTemp, outputDissolve, fieldName)
                #arcpy.Delete_management("in_memory")
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

    def SetFeatureClassPointRemoveDissolveSingel(self):
        self.featureClassPointRemoveDissolveSingel = self.featureClass + "_PointRemove_Dissolve_Singel"
        pass

    def SetFeatureClassPointRemoveDissolveSingelUnique(self):
        self.featureClassPointRemoveDissolveSingelUnique = self.featureClass + "_PointRemove_Dissolve_Singel_Unique"
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

    def SetFeatureClassPointRemoveDissolveSingel(self):
        self.featureClassPointRemoveDissolveSingel = self.featureClass + "_PointRemove_Dissolve_Singel"
        pass

    def SetFeatureClassPointRemoveDissolveSingelUnique(self):
        self.featureClassPointRemoveDissolveSingelUnique = self.featureClass + "_PointRemove_Dissolve_Singel_Unique"
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
    fixPointRemove = FixPointRemove()
    print "Running..."
    fixPointRemove.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass