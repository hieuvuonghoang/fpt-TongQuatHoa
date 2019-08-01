# -*- coding: utf-8 -*- 
import os
import sys
import json
import arcpy
import codecs
import subprocess

class ResolveBuildingConflict:

    def __init__(self, distanceAlign, distanceNhaP, buildingGap, minimumSize):
        # Set distance
        print "distanceAlign = {0}, distanceNhaP = {1}, buildingGap = {2}, minimumSize = {3}".format(distanceAlign, distanceNhaP, buildingGap, minimumSize)
        self.distanceAlign = distanceAlign
        self.distanceNhaP = distanceNhaP
        self.buildingGap = buildingGap
        self.minimumSize = minimumSize
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        # Feature DataSet Name
        self.fDDanCuCoSoHaTang = "DanCuCoSoHaTang"
        self.fDGiaoThong = "GiaoThong"
        # Feature Class Name
        self.fCNhaP = "NhaP"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        # Path Feature Class
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathNhaPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDDanCuCoSoHaTang), self.fCNhaP)
        # Representation Name
        self.repDoanTimDuongBo = "DoanTimDuongBo_Rep"
        self.repNhaP = "NhaP_Rep1"
        # Field Name
        self.invisibilityField = "invisibility_field"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.referenceScale = "50000"
        #
        self.MakeFeatureLayerAndSetLayerRepresentation()
        self.AddField()
        self.ResolveBuildingConflict()
        pass

    def MakeFeatureLayerAndSetLayerRepresentation(self):
        # MakeFeatureLayer
        self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer)
        self.nhaPFinalLayer = "nhaPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathNhaPFinal,
                                          out_layer = self.nhaPFinalLayer)
        # SetLayerRepresentation
        arcpy.SetLayerRepresentation_cartography(in_layer = self.doanTimDuongBoFinalLayer,
                                                 representation = self.repDoanTimDuongBo)
        arcpy.SetLayerRepresentation_cartography(in_layer = self.nhaPFinalLayer,
                                                 representation = self.repNhaP)
        pass

    def AddField(self):
        arcpy.AddField_management(in_table = self.nhaPFinalLayer,
                                  field_name = self.invisibilityField,
                                  field_type = "Short")
        pass

    def ResolveBuildingConflict(self):
        arcpy.ResolveBuildingConflicts_cartography(in_buildings = self.nhaPFinalLayer,
                                                   in_barriers = [[self.doanTimDuongBoFinalLayer, "True", self.distanceNhaP]],
                                                   invisibility_field = self.invisibilityField,
                                                   building_gap = self.buildingGap,
                                                   minimum_size = self.minimumSize)
        pass

if __name__ == "__main__":
    resolveBuildingConflict = ResolveBuildingConflict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    resolveBuildingConflict.Execute()
    pass