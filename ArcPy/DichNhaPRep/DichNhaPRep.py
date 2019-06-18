# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import codecs
import datetime

class DichNhaPRep:

    def __init__(self, distanceAlign, distanceConflict):
        # Set distance
        self.distanceAlign = distanceAlign
        self.distanceConflict = distanceConflict
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
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.referenceScale = "50000"
        #
        self.MakeFeatureLayerAndSetLayerRepresentation()
        self.AlignMarkerToStrokeOrFill()
        self.DetectGraphicConflict()
        self.AddJoin()
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

    def DetectGraphicConflict(self):
        self.fCOutPutConflict = "in_memory\\fCOutPutConflict"
        arcpy.DetectGraphicConflict_cartography(in_features = self.nhaPFinalLayer,
                                                conflict_features = self.doanTimDuongBoFinalLayer,
                                                out_feature_class = self.fCOutPutConflict,
                                                conflict_distance = self.distanceConflict)
        self.tableOutPutSelect = "in_memory\\tableOutPutSelect"
        arcpy.TableSelect_analysis(in_table = self.fCOutPutConflict,
                                   out_table = self.tableOutPutSelect,
                                   where_clause = "OBJECTID IS NOT NULL")
        pass

    def AddJoin(self):
        arcpy.AddJoin_management(in_layer_or_view = self.nhaPFinalLayer,
                                 in_field = "OBJECTID",
                                 join_table = self.tableOutPutSelect,
                                 join_field = "FID_NhaP")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.nhaPFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "FID_NhaP IS NOT NULL")
        self.fCNhaPConflict = os.path.join(r"C:\Users\vuong\Documents\ArcGIS\Default.gdb", "fCNhaPConflict")
        arcpy.CopyFeatures_management(in_features = self.nhaPFinalLayer,
                                      out_feature_class = self.fCNhaPConflict)
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
    dichNhaPRep = DichNhaPRep("50 Meters", "0 Meters")
    print "Running..."
    dichNhaPRep.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass