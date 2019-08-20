# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class IntegrateAllFeatureClass:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Config.json")
        self.outPutMerge = os.path.join(self.pathProcessGDB, "FeatureClassMerge")
        self.outPutSimplify = os.path.join(self.pathProcessGDB, "FeatureClassMerge_Simplify")
        if os.path.isfile(self.pathFileConfig):
            self.ReadFileConfig()
        else:
            print "Not Found: " + self.pathFileConfig + "?\n Create FileConfig..."
            self.CreateFileConfig()
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.ReadFileConfig()
        #arrLayerPolygon, arrLayerPolyline = self.MakeFeatureLayer()
        #self.Integrate(arrLayerPolyline, arrLayerPolygon)
        #self.Integrate(arrLayerPolygon, arrLayerPolyline)
        #self.MergePolygon()
        #self.SimplifyAllPolygon()
        #self.ExportPolygonAfterSimplify()
        #self.PolygonToMultiPoint()
        self.ErasePoint()
        pass

    def ErasePoint(self):
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if (tempPolygon.runFeatureClass == False):
                    continue
                pathInFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass + "_AllPoint")
                pathEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass + "_Simplify_AllPoint")
                pathOutEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass + "_PointRemove")
                arcpy.Erase_analysis(in_features = pathInFeature,
                                     erase_features = pathEraseFeature,
                                     out_feature_class = pathOutEraseFeature,
                                     cluster_tolerance = "0 Meters")
        pass

    def PolygonToMultiPoint(self):
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if (tempPolygon.runFeatureClass == False):
                    continue
                pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass + "_Simplify")
                pathFc = "in_memory\\FeatureClassTemp"
                arcpy.FeatureVerticesToPoints_management(in_features = pathFcOrigin,
                                                         out_feature_class = pathFc,
                                                         point_location = "ALL")
                fieldFID, fieldType = self.GetFieldFID(tempPolygon.featureClass, "LONG")
                pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass + "_Simplify_AllPoint")
                arcpy.Dissolve_management(in_features = pathFc,
                                          out_feature_class = pathDissolve,
                                          dissolve_field = [fieldFID])
        pass

    def SimplifyAllPolygon(self):
        self.outPutSimplify = os.path.join(self.pathProcessGDB, "FeatureClassMerge_Simplify")
        arcpy.SimplifyPolygon_cartography(in_features = self.outPutMerge,
                                          out_feature_class = self.outPutSimplify,
                                          algorithm = "BEND_SIMPLIFY",
                                          tolerance = "50 Meters",
                                          error_option = "RESOLVE_ERRORS",
                                          collapsed_point_option = "NO_KEEP")
        pass

    def ExportPolygonAfterSimplify(self):
        outMergeSimplifyLayer = "outMergeSimplifyLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.outPutSimplify,
                                          out_layer = outMergeSimplifyLayer)
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runFeatureClass == False:
                    continue
                # Create Feature Class
                pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                outPath = os.path.join(self.pathProcessGDB, tempConfig.featureDataSet)
                outName = tempPolygon.featureClass + "_Simplify"
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
                with arcpy.da.SearchCursor(outMergeSimplifyLayer, ["Shape@", fieldFID]) as cursorSearch:
                    with arcpy.da.InsertCursor(pathFcSimplify, ["Shape@", fieldFID]) as cursorInsert:
                        for rowSearch in cursorSearch:
                            cursorInsert.insertRow((rowSearch[0], rowSearch[1]))
        pass

    def MergePolygon(self):
        inFeatureClassMerges = []
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runFeatureClass == False:
                    continue
                # Add Field FID_XXX For Feature Class
                pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                print pathFc
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
                outPutFVToPoint = "in_memory\\outPutFVToPoint"
                arcpy.FeatureVerticesToPoints_management(in_features = tempPolygon.featureClassInMemory,
                                                         out_feature_class = outPutFVToPoint,
                                                         point_location = "ALL")
                pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass + "_AllPoint")
                arcpy.Dissolve_management(in_features = outPutFVToPoint,
                                          out_feature_class = pathDissolve,
                                          dissolve_field = [fieldFID])
                # FeatureClass Delete Field FID_XXX
                arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                # Maker Layer
                inFeatureClassMerges.append(tempPolygon.featureClassInMemory)
        # Merge
        #self.outputMergeLayer = "FeatureClassMergeLayer"
        #self.outputMerge = "in_memory\\FeatureClassMerge"
        outputMerge = os.path.join(self.pathProcessGDB, "FeatureClassMerge")
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = outputMerge)
        #arcpy.MakeFeatureLayer_management(in_features = self.outputMerge,
        #                                  out_layer = self.outputMergeLayer
        return outputMerge
        pass

    def MakeFeatureLayer(self):
        arrLayerPolygon = []
        arrLayerPolyline = []
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runFeatureClass == False:
                    continue
                tempPolygon.SetFeatureLayer()
                pathPolygon = os.path.join(self.pathProcessGDB, os.path.join(tempConfig.featureDataSet, tempPolygon.featureClass))
                arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                                  out_layer = tempPolygon.featureLayer)
                arrLayerPolygon.append(tempPolygon.featureLayer)
            for tempPolyline in tempConfig.listPolyline:
                if tempPolyline.runFeatureClass == False:
                    continue
                tempPolyline.SetFeatureLayer()
                pathPolyline = os.path.join(self.pathProcessGDB, os.path.join(tempConfig.featureDataSet, tempPolyline.featureClass))
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
                                   cluster_tolerance = "0 Meters")
        pass

    def GeneralizeSharedFeatures(self):
        outputMerge = self.MergePolyLine()
        outputMergeLayer = "outputMergeLayer"
        arcpy.MakeFeatureLayer_management(in_features = outputMerge,
                                          out_layer = outputMergeLayer)
        arrPolygonLayer = self.MakeFeatureLayerPolygon()
        arcpy.GeneralizeSharedFeatures_production(Input_Features = outputMergeLayer,
                                                  Generalize_Operation = "SIMPLIFY",
                                                  Simplify_Tolerance = "50 Meters",
                                                  Topology_Feature_Classes = arrPolygonLayer,
                                                  Simplification_Algorithm = "BEND_SIMPLIFY")
        pass

    def MergePolyLine(self):
        inFeatureClassMerges = []
        for tempConfig in self.configTools.listConfig:
            for tempPolyline in tempConfig.listPolyline:
                if tempPolyline.runFeatureClass == False:
                    continue
                # Add Field FID_XXX For Feature Class
                pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClass)
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
                # FeatureClass Delete Field FID_XXX
                arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                # Maker Layer
                inFeatureClassMerges.append(tempPolyline.featureClassInMemory)
        # Merge
        #self.outputMergeLayer = "FeatureClassMergeLayer"
        #self.outputMerge = "in_memory\\FeatureClassMerge"
        outputMerge = os.path.join(self.pathProcessGDB, "FeatureClassMerge")
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = outputMerge)
        #arcpy.MakeFeatureLayer_management(in_features = self.outputMerge,
        #                                  out_layer = self.outputMergeLayer
        return outputMerge
        pass

    def MakeFeatureLayerPolygon(self):
        arrPolylineLayer = []
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runFeatureClass == False:
                    continue
                pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                featureLayer = tempPolygon.featureClass + "Layer"
                print featureLayer
                arcpy.MakeFeatureLayer_management(in_features = pathFc,
                                          out_layer = featureLayer)
                arrPolylineLayer.append(featureLayer)
        return arrPolylineLayer
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
    
    def SetFeatureClassInMemory(self):
        self.featureClassInMemory = "in_memory\\" + self.featureClass

    def SetFeatureLayer(self):
        self.featureLayer = self.featureClass + "Layer"

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
    integrateAllFeatureClass = IntegrateAllFeatureClass()
    print "Running..."
    integrateAllFeatureClass.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass