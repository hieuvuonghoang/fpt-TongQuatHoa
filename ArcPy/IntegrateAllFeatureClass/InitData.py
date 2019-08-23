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
        # Read File Config Simplify
        if not os.path.isfile(self.pathFileConfig):
            print "... Not Found: " + self.pathFileConfig + "?\n  ... Create File ConfigSimplify..."
            self.CreateFileConfig()
        self.ReadFileConfig()
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