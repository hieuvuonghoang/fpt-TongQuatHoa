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
        print "distanceAlign = {}, distanceNhaP = {}, buildingGap = {}, minimumSize = {}".format(distanceAlign, distanceNhaP, buildingGap, minimumSize)
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
        self.fDThuyHe = "ThuyHe"
        # Feature Class Name
        self.fCNhaP = "NhaP"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCSongSuoiL = "SongSuoiL"
        # Path Feature Class
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathNhaPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDDanCuCoSoHaTang), self.fCNhaP)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiL)
        ## Path Process
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathSongSuoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        # Representation Name
        self.repDoanTimDuongBo = "DoanTimDuongBo_Rep"
        self.repNhaP = "NhaP_Rep1"
        self.repMatNuocTinh = "MatNuocTinh_Rep"
        self.repSongSuoiA = "SongSuoiA_Rep"
        self.repSongSuoiL = "SongSuoiL_Rep"
        # Field Name
        self.invisibilityField = "invisibility_field"
        #
        self.dirPathArcObject = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ReleaseRemoveShapeOverride"), "RemoveShapeOverride.exe")
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.referenceScale = "50000"
        #
        #arcpy.CopyFeatures_management(os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), self.fCNhaP), self.pathNhaPFinal)
        print self.dirPathArcObject
        subprocess.call([self.dirPathArcObject, self.pathFinalGDB, self.fCNhaP, self.repNhaP, ""])
        #
        arcpy.CalculateField_management(in_table = self.pathNhaPFinal,
                                        field = "NhaP_Rep1_ID",
                                        expression = "1",
                                        expression_type = "PYTHON_9.3")
        #
        self.MakeFeatureLayerAndSetLayerRepresentation()
        self.AddField()
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = self.nhaPFinalLayer, 
                                                    in_line_or_polygon_features = self.doanTimDuongBoFinalLayer,
                                                    search_distance = self.distanceAlign,
                                                    marker_orientation = "PARALLEL")
        arcpy.ResolveBuildingConflicts_cartography(in_buildings = self.nhaPFinalLayer,
                                                   in_barriers = [[self.doanTimDuongBoFinalLayer, "False", self.distanceNhaP]],
                                                   invisibility_field = self.invisibilityField,
                                                   building_gap = self.buildingGap,
                                                   minimum_size = self.minimumSize)
        #print self.dirPathArcObject
        #subprocess.call([self.dirPathArcObject, self.pathFinalGDB, self.fCNhaP, self.repNhaP, self.invisibilityField + " = 1"])
        pass

    def MakeFeatureLayerAndSetLayerRepresentation(self):
        # MakeFeatureL ayer
        self.doanTimDuongBoFinalLayer = arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal)
        self.nhaPFinalLayer = arcpy.MakeFeatureLayer_management(in_features = self.pathNhaPFinal)
        # SetLayerRepresentation
        arcpy.SetLayerRepresentation_cartography(in_layer = self.doanTimDuongBoFinalLayer,
                                                 representation = self.repDoanTimDuongBo)
        arcpy.SetLayerRepresentation_cartography(in_layer = self.nhaPFinalLayer,
                                                 representation = self.repNhaP)
        pass

    def AddField(self):
        arcpy.AddField_management(in_table = self.nhaPFinalLayer,
                                  field_name = self.invisibilityField,
                                  field_type = "SHORT")
        pass

if __name__ == "__main__":
    resolveBuildingConflict = ResolveBuildingConflict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    resolveBuildingConflict.Execute()
    pass