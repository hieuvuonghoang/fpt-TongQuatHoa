import sys
import os
import arcpy
import json

class SimplifyPolygon:

    def __init__(self, pathFileConfigOne, pathFileConfigTwo):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        self.configTools = ConfigTools()
        if os.path.isfile(pathFileConfigOne):
            self.ReadFileConfig(pathFileConfigOne)
        else:
            print "Not Found: " + pathFileConfigOne + "?\n Create FileConfig..."
            self.CreateFileConfig(pathFileConfigOne)

    def Excute(self):
        self.MergeTools()
        self.SimplifyTools()
        self.UpdateShapeAfterSimplify()
        #self.GetGenerateNearTable("in_memory\\ThuyHeSongSuoiALayer")

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

    def ReadFileConfig(self, pathFile):
        file = open(pathFile, "r")
        textConfig = file.read()
        file.close()
        self.configTools.InitFromDict(json.loads(textConfig))

    def MergeTools(self):
        print "MergeTools..."
        inFeatureClassMerges = []
        for featureDataSetTemp in self.configTools.listConfig:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            #print featureDataSetTemp.featureDataSet + ":"
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False:
                    continue
                #print "\t" + featureClassTemp.featureClass
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
                #featureClassTemp.SetFeatureLayerInMemory(featureDataSetTemp.featureDataSet)
                #arcpy.MakeFeatureLayer_management(in_features = featureClassTemp.featureClassInMemory, out_layer = featureClassTemp.featureLayerInMemory)
                inFeatureClassMerges.append(featureClassTemp.featureClassInMemory)
        # Merge
        self.outputMerge = os.path.join(self.pathDefaultGDB, "FeatureClassMerge")
        self.outputMergeLayer = "FeatureClassMergeLayer"
        #"in_memory\\FeatureClassMerge"
        #os.path.join(self.pathDefaultGDB, "FeatureClassMerge")
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = self.outputMerge)
        arcpy.MakeFeatureLayer_management(in_features = self.outputMerge,
                                          out_layer = self.outputMergeLayer)

    def SimplifyTools(self):
        print "SimplifyTools..."
        #self.outputSimplifyPolygon = "in_memory\\FeatureClassSimplifyPolygon"
        self.outputSimplifyPolygon = os.path.join(self.pathDefaultGDB, "FeatureClassSimplifyPolygon")
        #self.outputSimplifyPolygonPnt = os.path.join(self.pathDefaultGDB, "FeatureClassSimplifyPolygon_Pnt")
        arcpy.SimplifyPolygon_cartography (in_features = self.outputMergeLayer,
                                            out_feature_class = self.outputSimplifyPolygon,
                                            algorithm = "BEND_SIMPLIFY",
                                            tolerance = "50 Meters",
                                            minimum_area = "#",
                                            error_option = "RESOLVE_ERRORS",
                                            collapsed_point_option = "NO_KEEP")

    def UpdateShapeAfterSimplify(self):
        print "UpdateShapeAfterSimplify..."
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

    def GetGenerateNearTable(self, inFeatureLayer):
        nearFeatures = []
        for featureDataSetTemp in self.configTools.listConfig:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False or featureClassTemp.featureLayerInMemory == inFeatureLayer:
                    continue
                nearFeatures.append(featureClassTemp.featureLayerInMemory)
        outTableTemp = os.path.join(self.pathDefaultGDB, "TableTemp")
        # os.path.join(self.pathDefaultGDB, "TableTemp")
        # "in_memory\\OutTableTemp"
        arcpy.GenerateNearTable_analysis(in_features = inFeatureLayer,
                                         near_features = nearFeatures,
                                         out_table = outTableTemp,
                                         search_radius = "0 Meters",
                                         closest = "ALL",
                                         closest_count = "0")
        nearFeatureLayers = [inFeatureLayer]
        with arcpy.da.SearchCursor(outTableTemp, ['NEAR_FC']) as cursor:
            for row in cursor:
                if row[0] not in nearFeatureLayers:
                    nearFeatureLayers.append(row[0])
        
        for nearFeatureLayerTemp in nearFeatureLayers:
            arcpy.SelectLayerByAttribute_management(nearFeatureLayerTemp, "CLEAR_SELECTION")
        
        with arcpy.da.SearchCursor(outTableTemp, ['NEAR_FID', 'NEAR_FC']) as cursor:
            for row in cursor:
                sqlQuery = "OBJECTID = " + str(row[0])
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = row[1],
                                                        selection_type = "ADD_TO_SELECTION",
                                                        where_clause = sqlQuery)
        arcpy.Merge_management(nearFeatureLayers, os.path.join(self.pathDefaultGDB, "FeatureClassMerge"))
        
    def GetFieldFID(self, featureClass, fieldType):
        return "FID_" + featureClass, fieldType

    def SimplifyPolygonVersion4(self):
        pass

    def SimplifyPolygonVersion6(self):
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

if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fileConfigNameOne = "ConfigSimplifyPolygon.json"
    pathFileConfigOne = os.path.join(dir_path, fileConfigNameOne)
    simplifyPolygon = SimplifyPolygon(pathFileConfigOne, pathFileConfigOne)
    simplifyPolygon.Excute()