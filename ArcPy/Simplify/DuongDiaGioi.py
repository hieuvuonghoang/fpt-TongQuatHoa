# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime
import subprocess

class DuongDiaGioi:

    def __init__(self, distanceSnap):
        self.distanceSnap = distanceSnap
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDBienGioiDiaGioi = "BienGioiDiaGioi"
        self.fCDuongDiaGioi = "DuongDiaGioi"
        self.fCDiaPhan = "DiaPhan"
        # Path Process
        self.pathDuongDiaGioiProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDuongDiaGioi)
        self.pathDiaPhanProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDiaPhan)
        # Path Final
        self.pathDuongDiaGioiFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDuongDiaGioi)
        self.pathDiaPhanFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDiaPhan)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Copy Feature Class
        arcpy.CopyFeatures_management(in_features = self.pathDuongDiaGioiProcess,
                                      out_feature_class = self.pathDuongDiaGioiFinal)
        # doiTuong = 3 (C?p xã)
        self.CreateFCPointRemove("3")
        self.RemovePoint("doiTuong = 3")
        self.SnapDuongDiaGioi("3")
        # doiTuong = 2 (C?p huy?n)
        self.CreateFCPointRemove("2")
        self.RemovePoint("doiTuong = 2")
        self.SnapDuongDiaGioi("2")
        # doiTuong = 1 (C?p t?nh)
        self.CreateFCPointRemove("1")
        self.RemovePoint("doiTuong = 1")
        self.SnapDuongDiaGioi("1")
        pass

    def CreateFCPointRemove(self, doiTuong):
        # Add Point For DuongDiaGioi Final
        ## Make Feature Layer
        self.diaPhanProcessLayer = "DiaPhanProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDiaPhanProcess,
                                          out_layer = self.diaPhanProcessLayer)
        self.duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongDiaGioiFinal,
                                          out_layer = self.duongDiaGioiFinalLayer)
        ## Select Layer
        sqlQuery = "doiTuong = " + doiTuong
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.diaPhanProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        ## Feature Vertices To Points: fCDiaPhan
        fCDiaPhanToProcessPoints = "in_memory\\DiaPhanToProcessPoints"
        arcpy.FeatureVerticesToPoints_management(in_features = self.diaPhanProcessLayer,
                                                 out_feature_class = fCDiaPhanToProcessPoints,
                                                 point_location = "ALL")
        ## Add Point For fCDuongDiaGioi using Integrate Tool
        arcpy.Integrate_management(in_features = [[self.duongDiaGioiFinalLayer, 1], [fCDiaPhanToProcessPoints, 2]],
                                   cluster_tolerance = "0 Meters")
        
        # Create Feature Class Point Remove
        ## Make Feature Layer
        self.diaPhanFinalLayer = "DiaPhanFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDiaPhanFinal,
                                          out_layer = self.diaPhanFinalLayer)
        ## Select Layer
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        ## Feature To Line
        fCDiaPhanFinalFeatureToLine = "in_memory\\DiaPhanFinalFeatureToLine"
        arcpy.FeatureToLine_management(in_features = self.diaPhanFinalLayer,
                                       out_feature_class = fCDiaPhanFinalFeatureToLine,
                                       cluster_tolerance = "0 Meters")
        diaPhanFinalFeatureToLineLayer = "DiaPhanFinalFeatureToLineLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCDiaPhanFinalFeatureToLine,
                                          out_layer = diaPhanFinalFeatureToLineLayer)
        ## Feature Vertices To Points: DuongDiaGioi Final
        fCDuongDiaGioiFinalPointsALL = "in_memory\\DuongDiaGioiFinalPointsALL"
        arcpy.FeatureVerticesToPoints_management(in_features = self.duongDiaGioiFinalLayer,
                                                 out_feature_class = fCDuongDiaGioiFinalPointsALL,
                                                 point_location = "ALL")
        fCDuongDiaGioiFinalPointsBOTHENDS = "in_memory\\DuongDiaGioiFinalPointsBOTHENDS"
        arcpy.FeatureVerticesToPoints_management(in_features = self.duongDiaGioiFinalLayer,
                                                 out_feature_class = fCDuongDiaGioiFinalPointsBOTHENDS,
                                                 point_location = "BOTH_ENDS")
        fCDuongDiaGioiFinalPoints = "in_memory\\DuongDiaGioiFinalPoints"
        arcpy.Erase_analysis(in_features = fCDuongDiaGioiFinalPointsALL,
                             erase_features = fCDuongDiaGioiFinalPointsBOTHENDS,
                             out_feature_class = fCDuongDiaGioiFinalPoints)
        duongDiaGioiFinalPointsLayer = "DuongDiaGioiFinalPointsLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCDuongDiaGioiFinalPoints,
                                          out_layer = duongDiaGioiFinalPointsLayer)
        ## Select fCDuongDiaGioiFinalPoints
        arcpy.SelectLayerByLocation_management(in_layer = duongDiaGioiFinalPointsLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = diaPhanFinalFeatureToLineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        self.duongDiaGioiPointRemoveName = "DuongDiaGioiPointRemove"
        self.duongDiaGioiPointRemove = os.path.join(self.pathProcessGDB, self.duongDiaGioiPointRemoveName)
        arcpy.CopyFeatures_management(in_features = duongDiaGioiFinalPointsLayer,
                                      out_feature_class = self.duongDiaGioiPointRemove)
        pass

    def RemovePoint(self, whereClause):
        subprocess.call(["RemovePointOnLine.exe", r"C:\Generalize_25_50\50K_Final.gdb", "DuongDiaGioi", whereClause, r"C:\Generalize_25_50\50K_Process.gdb", self.duongDiaGioiPointRemoveName])
        pass

    def SnapDuongDiaGioi(self, doiTuong):
        self.duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongDiaGioiFinal,
                                          out_layer = self.duongDiaGioiFinalLayer)
        sqlQuery = "doiTuong = " + doiTuong
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        self.diaPhanFinalLayer = "DiaPhanFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.diaPhanFinalLayer,
                                          out_layer = self.diaPhanFinalLayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        snapEnv = [self.diaPhanFinalLayer, "EDGE", self.distanceSnap]
        arcpy.Snap_edit(self.duongDiaGioiFinalLayer, [snapEnv])
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
    duongDiaGioi = DuongDiaGioi(sys.argv[1])
    print "Running..."
    duongDiaGioi.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass