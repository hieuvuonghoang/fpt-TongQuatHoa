# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import codecs
import datetime
import subprocess

class DichNhaPRep:

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
        self.AlignMarkerToStrokeOrFill()
        self.AddField()
        self.ResolveBuildingConflict()
        self.CallToolSetEmptyShape()
        self.DeleteField()
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

    def AlignMarkerToStrokeOrFill(self):
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = self.nhaPFinalLayer,
                                                    in_line_or_polygon_features = self.doanTimDuongBoFinalLayer,
                                                    search_distance = self.distanceAlign,
                                                    marker_orientation = "PERPENDICULAR")
        pass

    def AddField(self):
        arcpy.AddField_management(in_table = self.nhaPFinalLayer,
                                  field_name = self.invisibilityField,
                                  field_type = "Short")
        pass

    def ResolveBuildingConflict(self):
        arcpy.ResolveBuildingConflicts_cartography(in_buildings = self.nhaPFinalLayer,
                                                   in_barriers = [[self.doanTimDuongBoFinalLayer, "False", self.distanceNhaP]],
                                                   invisibility_field = self.invisibilityField,
                                                   building_gap = self.buildingGap,
                                                   minimum_size = self.minimumSize)
        pass

    def DeleteField(self):
        arcpy.DeleteField_management(in_table = self.nhaPFinalLayer,
                                     drop_field = [self.invisibilityField])
        pass

    def CallToolSetEmptyShape(self):
        #args [] = {pathGDB, featureClassName, representationName, whereClause}
        subprocess.call(["SetEmptyShapeRepresentation.exe", r"C:\Generalize_25_50\50K_Final.gdb", "NhaP", "NhaP_Rep1", "invisibility_field = 1"])
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

if __name__ == "__main__":
    runTime = RunTime()
    dichNhaPRep = DichNhaPRep(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print "Running..."
    dichNhaPRep.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass