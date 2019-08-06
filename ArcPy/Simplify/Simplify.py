# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class SimplifyPolygon:

    def __init__(self, pathFileConfig, algorithm, tolerance, minimum_area, error_option, collapsed_point_option):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.algorithm = algorithm
        self.tolerance = tolerance
        self.minimum_area = minimum_area
        self.error_option = error_option
        self.collapsed_point_option = collapsed_point_option
        self.configTools = ConfigTools()
        if os.path.isfile(pathFileConfig):
            self.ReadFileConfig(pathFileConfig)
        else:
            print "Not Found: " + pathFileConfig + "?\n Create FileConfig..."
            self.CreateFileConfig(pathFileConfig)
        pass

    def Excute(self):
        arcpy.env.overwriteOutput = True
        print "MergeTools"
        self.MergeTools()
        print "SimplifyTools"
        self.SimplifyTools()
        print "UpdateShapeAfterSimplify"
        self.UpdateShapeAfterSimplify()
        pass

    def CreateFileConfig(self, pathFile):
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemListConfig = ElemListConfig(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemListPolygon = ElemListPolygon(fcTemp.baseName)
                    elemListConfig.InsertElemListPolygon(elemListPolygon)
            if len(elemListConfig.listPolygon) > 0:
                self.configTools.InsertElemListConfig(elemListConfig)
        textConfig = json.dumps(obj = self.configTools.GetDict(), indent = 1, sort_keys = True)
        file = open(pathFile, "w")
        file.write(textConfig)
        file.close()
        pass

    def ReadFileConfig(self, pathFile):
        file = open(pathFile, "r")
        textConfig = file.read()
        file.close()
        self.configTools.InitFromDict(json.loads(textConfig))
        pass

    def MergeTools(self):
        inFeatureClassMerges = []
        for featureDataSetTemp in self.configTools.listConfig:
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
        # Merge
        self.outputMergeLayer = "FeatureClassMergeLayer"
        self.outputMerge = "in_memory\\FeatureClassMerge"
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = self.outputMerge)
        arcpy.MakeFeatureLayer_management(in_features = self.outputMerge,
                                          out_layer = self.outputMergeLayer)
        pass

    def SimplifyTools(self):
        self.outputSimplifyPolygon = "in_memory\\FeatureClassSimplifyPolygon"
        arcpy.SimplifyPolygon_cartography (in_features = self.outputMergeLayer,
                                            out_feature_class = self.outputSimplifyPolygon,
                                            algorithm = self.algorithm,
                                            tolerance = self.tolerance,
                                            minimum_area = self.minimum_area,
                                            error_option = self.error_option,
                                            collapsed_point_option = self.collapsed_point_option)
        pass

    def UpdateShapeAfterSimplify(self):
        outputSimplifyPolygonLayer = "FeatureClassSimplifyPolygonLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.outputSimplifyPolygon,
                                          out_layer = outputSimplifyPolygonLayer)
        for featureDataSetTemp in self.configTools.listConfig:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            #print featureDataSetTemp.featureDataSet + ":"
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False:
                    continue
                print featureClassTemp.featureClass
                fieldName, fieldType = self.GetFieldFID(featureClass = featureClassTemp.featureClass, fieldType = None)
                querySQL = fieldName + " IS NOT NULL"
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = outputSimplifyPolygonLayer, selection_type = "NEW_SELECTION", where_clause = querySQL)
                outTableTemp = "in_memory\\OutTableTemp"
                arcpy.CopyFeatures_management(in_features = outputSimplifyPolygonLayer,
                                              out_feature_class = outTableTemp)
                updateShapeByOID = UpdateShapeByOID(sFC = outTableTemp, dFC = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass), fID_XXX = fieldName)
                updateShapeByOID.Excute()
        pass

    def GetFieldFID(self, featureClass, fieldType):
        return "FID_" + featureClass, fieldType
        pass

class UpdateShapeByOID:

    def __init__(self, sFC, dFC, fID_XXX):
        self.sFC = sFC
        self.dFC = dFC
        self.fID_XXX = fID_XXX

    def Excute(self):
        with arcpy.da.UpdateCursor(self.dFC, ['OID@', 'SHAPE@']) as cursor:
            for row in cursor:
                found = False
                with arcpy.da.UpdateCursor(self.sFC, [self.fID_XXX, 'SHAPE@']) as cursorSub:
                    for rowSub in cursorSub:
                        if row[0] == rowSub[0]:
                            row[1] = rowSub[1]
                            cursor.updateRow(row)
                            cursorSub.deleteRow()
                            found = True
                            break
                if found == False:
                    cursor.deleteRow()

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

if __name__ == '__main__':
    runTime = RunTime()
    simplifyPolygon = SimplifyPolygon(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    print "Running..."
    simplifyPolygon.Excute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass