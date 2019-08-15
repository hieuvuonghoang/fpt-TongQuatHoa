# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class SimplifyProduction:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfigPolygon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigToolPolygon.json")
        self.pathFileConfigPolyline = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigToolPolyline.json")
        
        pass

    def Execute(self):
        arcpy.env.workspace = self.pathFinalGDB
        arcpy.env.overwriteOutput = True
        #self.ScanFeatureClassIsPolygon()
        outputMerge = self.MergePolygon()
        outputMergeLayer = "outputMergeLayer"
        arcpy.MakeFeatureLayer_management(in_features = outputMerge,
                                          out_layer = outputMergeLayer)
        arrPolylineLayer = self.MakeFeatureLayerPolyline()
        arcpy.GeneralizeSharedFeatures_production(Input_Features = outputMergeLayer,
                                                  Generalize_Operation = "SIMPLIFY",
                                                  Simplify_Tolerance = "50 Meters",
                                                  Topology_Feature_Classes = arrPolylineLayer,
                                                  Simplification_Algorithm = "BEND_SIMPLIFY")
        pass

    def MergePolygon(self):
        configTools = ConfigTools()
        configTools.InitFromDict(self.ReadFileConfig(self.pathFileConfigPolygon))
        inFeatureClassMerges = []
        for featureDataSetTemp in configTools.listConfig:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False:
                    continue
                # Add Field FID_XXX For Feature Class
                pathFc = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                fieldFID, fieldType = self.GetFieldFID(featureClassTemp.featureClass, "LONG")
                arcpy.AddField_management(pathFc, fieldFID, fieldType)
                # Update Field FID_XXX
                with arcpy.da.UpdateCursor(pathFc, ['OID@', fieldFID]) as cursor:
                    for row in cursor:
                        row[1] = row[0]
                        cursor.updateRow(row)
                # Copy FeatureClass to in_memory
                featureClassTemp.SetFeatureClassInMemory(featureDataSetTemp.featureDataSet)
                arcpy.CopyFeatures_management(in_features = pathFc, out_feature_class = featureClassTemp.featureClassInMemory)
                # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                fields = arcpy.ListFields(featureClassTemp.featureClassInMemory)
                fieldsDelete = []
                for fieldTemp in fields:
                    if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                        fieldsDelete.append(fieldTemp.name)
                arcpy.DeleteField_management(in_table = featureClassTemp.featureClassInMemory, drop_field = fieldsDelete)
                # FeatureClass Delete Field FID_XXX
                arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                # Maker Layer
                inFeatureClassMerges.append(featureClassTemp.featureClassInMemory)
        #outputMerge = "in_memory\\FeatureClassMerge"
        outputMerge = os.path.join(self.pathFinalGDB, "FeatureClassMerge")
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = outputMerge)
        return outputMerge
        #outputMergeLayer = "outputMergeLayer"
        #arcpy.MakeFeatureLayer_management(in_features = outputMerge,
        #                                  out_layer = outputMergeLayer)
        pass

    def MakeFeatureLayerPolyline(self):
        configTools = ConfigTools()
        configTools.InitFromDict(self.ReadFileConfig(self.pathFileConfigPolygon))
        arrPolylineLayer = []
        for featureDataSetTemp in configTools.listConfig:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False:
                    continue
                # Add Field FID_XXX For Feature Class
                pathFc = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                featureLayer = featureClassTemp.featureClass + "Layer"
                arcpy.MakeFeatureLayer_management(in_features = pathFc,
                                          out_layer = featureLayer)
                arrPolylineLayer.append(featureLayer)
        return arrPolylineLayer
        pass

    def ScanFeatureClassIsPolygon(self):
        pass

    def ReadFileConfig(self, pathFile):
        file = open(pathFile, "r")
        textConfig = file.read()
        file.close()
        return json.loads(textConfig)
        pass

    def GetFieldFID(self, featureClass, fieldType):
        return "FID_" + featureClass, fieldType
        pass

class ConfigTools:

    def __init__(self):
        self.listConfig = []

    def InsertElemListConfig(self, elemListConfig):
        self.listConfig.insert(0, elemListConfig)

    def GetDict(self):
        listTemp = []
        for elemListConfig in self.listConfig:
            listTemp.insert(0, elemListConfig.GetDict())
        return listTemp;

    def InitFromDict(self, dataJson):
        self.listConfig = []
        for elemListConfigTemp in dataJson:
            elemListConfig = ElemListConfig(elemListConfigTemp['featureDataSet'])
            for elemListPolygonTemp in elemListConfigTemp['listPolygon']:
                elemListPolygon = ElemListPolygon(elemListPolygonTemp['featureClass'])
                elemListPolygon.runSimplify = elemListPolygonTemp['runSimplify']
                elemListConfig.InsertElemListPolygon(elemListPolygon)
            self.InsertElemListConfig(elemListConfig)

class ElemListConfig:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolygon = []

    def InsertElemListPolygon(self, elemListPolygon):
        self.listPolygon.insert(0, elemListPolygon)

    def GetDict(self):
        listTemp = []
        for elemListPolygon in self.listPolygon:
            listTemp.insert(0, elemListPolygon.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolygon": listTemp
        }

class ElemListPolygon:

    def __init__(self, featureClass):
        self.featureClass = featureClass
        self.runSimplify = True
    
    def SetFeatureClassInMemory(self, featureDataSet):
        self.featureClassInMemory = "in_memory\\" + featureDataSet + self.featureClass

    def SetFeatureLayerInMemory(self, featureDataSet):
        self.featureLayerInMemory = "in_memory\\" + featureDataSet + self.featureClass + "Layer"

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

if __name__ == "__main__":
    runTime = RunTime()
    simplifyProduction = SimplifyProduction()
    print "Running..."
    simplifyProduction.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass
