# -*- coding: utf-8 -*- 
import os
import sys
import json
import arcpy
import codecs
import subprocess

class ResolveConflictNhaP:

    def __init__(self, pathFileConfig, conflictDistance, lineConnectionAllowance):
        # Parameter
        print "pathFileConfig = {0} conflictDistance = {1}, lineConnectionAllowance = {2}".format(pathFileConfig, conflictDistance, lineConnectionAllowance)
        self.pathFileConfig = pathFileConfig
        self.conflictDistance = conflictDistance
        self.lineConnectionAllowance = lineConnectionAllowance
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        # Feature DataSet Name
        self.fDDanCuCoSoHaTang = "DanCuCoSoHaTang"
        # Feature Class Name
        self.fCNhaP = "NhaP"
        # Path Feature Class
        ## Path Final
        self.pathNhaPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDDanCuCoSoHaTang), self.fCNhaP)
        # Representation Name
        self.repNhaP = "NhaP_Rep1"
        # Field Name
        self.invisibilityField = "invisibility_field"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.referenceScale = "50000"

        # MakeFeatureLayer
        self.nhaPFinalLayer = "nhaPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathNhaPFinal,
                                          out_layer = self.nhaPFinalLayer)
        # SetLayerRepresentation
        arcpy.SetLayerRepresentation_cartography(in_layer = self.nhaPFinalLayer,
                                                 representation = self.repNhaP)

        # Read File Config
        with open(self.pathFileConfig) as json_file:
            dataConfig = json.load(json_file)

        # For
        for dataSet in dataConfig:
            for featureClass in dataSet["listFeature"]:
                pathFeatureClass = os.path.join(os.path.join(self.pathFinalGDB, dataSet["featureDataSet"]), featureClass["featureClassName"])
                print pathFeatureClass
                self.MakeFeatureLayerAndSetLayerRepresentation(pathFeatureClass, featureClass["representationName"])
                self.DetectGraphicConflict()
                self.AddJoinAndMarkInvisibility()

        # 
        self.CallToolSetEmptyShape()
        self.DeleteField()
        pass

    def MakeFeatureLayerAndSetLayerRepresentation(self, pathFeatureClass, representationName):
        # MakeFeatureLayer
        self.tempLayer = "tempLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathFeatureClass,
                                          out_layer = self.tempLayer)
        # SetLayerRepresentation
        arcpy.SetLayerRepresentation_cartography(in_layer = self.tempLayer,
                                                 representation = representationName)
        pass

    def DetectGraphicConflict(self):
        self.outDetect = "in_memory\\outDetect"
        arcpy.DetectGraphicConflict_cartography(in_features = self.nhaPFinalLayer,
                                                conflict_features = self.tempLayer,
                                                out_feature_class = self.outDetect,
                                                conflict_distance = self.conflictDistance,
                                                line_connection_allowance = self.lineConnectionAllowance)
        pass

    def AddJoinAndMarkInvisibility(self):
        self.outTableTemp = "in_memory\\outTableTemp"
        arcpy.TableSelect_analysis(in_table = self.outDetect,
                                   out_table = self.outTableTemp)
        arcpy.AddJoin_management(in_layer_or_view = self.nhaPFinalLayer,
                                 in_field = "OBJECTID",
                                 join_table = self.outTableTemp,
                                 join_field = "FID_NhaP")
        sqlQuery = "outTableTemp.FID_NhaP IS NOT NULL"
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.nhaPFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        arcpy.RemoveJoin_management(in_layer_or_view = self.nhaPFinalLayer,
                                    join_name = "outTableTemp")
        with arcpy.da.UpdateCursor(self.nhaPFinalLayer, [self.invisibilityField]) as cursor:
            for feature in cursor:
                feature[0] = 1
                cursor.updateRow(feature)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.nhaPFinalLayer,
                                                selection_type = "CLEAR_SELECTION")
        pass

    def CallToolSetEmptyShape(self):
        #args [] = {pathGDB, featureClassName, representationName, whereClause}
        subprocess.call(["SetEmptyShapeRepresentation.exe", self.pathFinalGDB, "NhaP", "NhaP_Rep1", self.invisibilityField + " = 1"])
        pass

    def DeleteField(self):
        arcpy.DeleteField_management(in_table = self.nhaPFinalLayer,
                                     drop_field = [self.invisibilityField])
        pass

if __name__ == "__main__":
    resolveConflictNhaP = ResolveConflictNhaP(sys.argv[1], sys.argv[2], sys.argv[3])
    resolveConflictNhaP.Execute()
    pass