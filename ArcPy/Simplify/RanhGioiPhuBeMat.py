# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime
import subprocess

class RanhGioiPhuBeMat:

    def __init__(self, distanceSnap):
        self.distanceSnap = distanceSnap
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDPhuBeMat = "PhuBeMat"
        self.fCPhuBeMat = "PhuBeMat"
        self.fCRanhGioiPhuBeMat = "RanhGioiPhuBeMat"
        # Path Process
        self.pathPhuBeMatProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDPhuBeMat), self.fCPhuBeMat)
        self.pathRanhGioiPhuBeMatProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDPhuBeMat), self.fCRanhGioiPhuBeMat)
        # Path Final
        self.pathPhuBeMatFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDPhuBeMat), self.fCPhuBeMat)
        self.pathRanhGioiPhuBeMatFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDPhuBeMat), self.fCRanhGioiPhuBeMat)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Copy Feature Class
        arcpy.CopyFeatures_management(in_features = self.pathRanhGioiPhuBeMatProcess,
                                      out_feature_class = self.pathRanhGioiPhuBeMatFinal)
        self.CreateFCPointRemove()
        self.AddFieldSelectUpdateField()
        self.RemovePoint(str(self.fieldRemovePoint) + " = 1")
        #self.SelectLineSnap()
        #self.SnapRanhGioiPhuBeMatFinal()
        pass

    def CreateFCPointRemove(self):
        # Add Point For RanhGioiPhuBeMat Final
        ## Make Feature Layer
        self.phuBeMatProcessLayer = "PhuBeMatProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathPhuBeMatProcess,
                                          out_layer = self.phuBeMatProcessLayer)
        self.ranhGioiPhuBeMatFinalLayer = "RanhGioiPhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatFinal,
                                          out_layer = self.ranhGioiPhuBeMatFinalLayer)
        ## Feature Vertices To Points: fCPhuBeMat
        fCPhuBeMatProcessPoints = "in_memory\\PhuBeMatProcessPoints"
        arcpy.FeatureVerticesToPoints_management(in_features = self.phuBeMatProcessLayer,
                                                 out_feature_class = fCPhuBeMatProcessPoints,
                                                 point_location = "ALL")
        ## Add Point For RanhGioiPhuBeMat using Integrate Tool
        arcpy.Integrate_management(in_features = [[self.ranhGioiPhuBeMatFinalLayer, 1], [fCPhuBeMatProcessPoints, 2]],
                                   cluster_tolerance = "0 Meters")
        
        # Create Feature Class Point Remove
        ## Make Feature Layer
        self.phuBeMatFinalLayer = "PhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathPhuBeMatFinal,
                                          out_layer = self.phuBeMatFinalLayer)
        ## Feature To Line
        self.fCPhuBeMatFinalFeatureToLine = "in_memory\\PhuBeMatFinalFeatureToLine"
        arcpy.FeatureToLine_management(in_features = self.phuBeMatFinalLayer,
                                       out_feature_class = self.fCPhuBeMatFinalFeatureToLine,
                                       cluster_tolerance = "0 Meters")
        self.phuBeMatFinalFeatureToLineLayer = "PhuBeMatFinalFeatureToLineLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCPhuBeMatFinalFeatureToLine,
                                          out_layer = self.phuBeMatFinalFeatureToLineLayer)
        ## Feature Vertices To Points: RanhGioiPhuBeMat Final
        fCRanhGioiPhuBeMatFinalPointsALL = "in_memory\\RanhGioiPhuBeMatFinalPointsALL"
        arcpy.FeatureVerticesToPoints_management(in_features = self.ranhGioiPhuBeMatFinalLayer,
                                                 out_feature_class = fCRanhGioiPhuBeMatFinalPointsALL,
                                                 point_location = "ALL")
        fCRanhGioiPhuBeMatFinalPointsBOTHENDS = "in_memory\\RanhGioiPhuBeMatFinalPointsBOTHENDS"
        arcpy.FeatureVerticesToPoints_management(in_features = self.ranhGioiPhuBeMatFinalLayer,
                                                 out_feature_class = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                                                 point_location = "BOTH_ENDS")
        fCRanhGioiPhuBeMatFinalPoints = "in_memory\\RanhGioiPhuBeMatFinalPoints"
        arcpy.Erase_analysis(in_features = fCRanhGioiPhuBeMatFinalPointsALL,
                             erase_features = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                             out_feature_class = fCRanhGioiPhuBeMatFinalPoints)
        ranhGioiPhuBeMatFinalPointsLayer = "RanhGioiPhuBeMatFinalPointsLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCRanhGioiPhuBeMatFinalPoints,
                                          out_layer = ranhGioiPhuBeMatFinalPointsLayer)
        ## Select fCRanhGioiPhuBeMatFinalPoints
        arcpy.SelectLayerByLocation_management(in_layer = ranhGioiPhuBeMatFinalPointsLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.phuBeMatFinalFeatureToLineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        self.ranhGioiPhuBeMatPointRemoveName = "RanhGioiPhuBeMatPointRemove"
        self.ranhGioiPhuBeMatPointRemove = os.path.join(self.pathProcessGDB, self.ranhGioiPhuBeMatPointRemoveName)
        arcpy.CopyFeatures_management(in_features = ranhGioiPhuBeMatFinalPointsLayer,
                                      out_feature_class = self.ranhGioiPhuBeMatPointRemove)
        pass

    def AddFieldSelectUpdateField(self):
        self.fieldRemovePoint = "RemovePoint"
        arcpy.AddField_management(in_table = self.pathRanhGioiPhuBeMatFinal,
                                  field_name = self.fieldRemovePoint,
                                  field_type = "SHORT")
        self.ranhGioiPhuBeMatPointRemoveLayer = "ranhGioiPhuBeMatPointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.ranhGioiPhuBeMatPointRemove,
                                          out_layer = self.ranhGioiPhuBeMatPointRemoveLayer)
        self.ranhGioiPhuBeMatFinalLayer = "RanhGioiPhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatFinal,
                                          out_layer = self.ranhGioiPhuBeMatFinalLayer)
        arcpy.SelectLayerByLocation_management(in_layer = self.ranhGioiPhuBeMatFinalLayer,
                                               select_features = self.ranhGioiPhuBeMatPointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        arcpy.CalculateField_management(in_table = self.ranhGioiPhuBeMatFinalLayer,
                                        field = self.fieldRemovePoint,
                                        expression = "1",
                                        expression_type = "PYTHON_9.3")
        pass

    def RemovePoint(self, whereClause):
        subprocess.call(["RemovePointOnLine.exe", r"C:\Generalize_25_50\50K_Final.gdb", "RanhGioiPhuBeMat", whereClause, r"C:\Generalize_25_50\50K_Process.gdb", self.ranhGioiPhuBeMatPointRemoveName])
        pass

    def SelectLineSnap(self):
        self.ranhGioiPhuBeMatFinalLayer = "RanhGioiPhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatFinal,
                                          out_layer = self.ranhGioiPhuBeMatFinalLayer)
        fCRanhGioiPhuBeMatFinalPointsBOTHENDS = "in_memory\\RanhGioiPhuBeMatFinalPointsBOTHENDS"
        arcpy.FeatureVerticesToPoints_management(in_features = self.ranhGioiPhuBeMatFinalLayer,
                                                 out_feature_class = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                                                 point_location = "BOTH_ENDS")
        ranhGioiPhuBeMatFinalPointsBOTHENDSLayer = "RanhGioiPhuBeMatFinalPointsBOTHENDSLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                                          out_layer = ranhGioiPhuBeMatFinalPointsBOTHENDSLayer)
        arcpy.SelectLayerByLocation_management(in_layer = ranhGioiPhuBeMatFinalPointsBOTHENDSLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.phuBeMatFinalFeatureToLineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.ranhGioiPhuBeMatFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = ranhGioiPhuBeMatFinalPointsBOTHENDSLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        pass

    def SnapRanhGioiPhuBeMatFinal(self):
        snapEnv = [self.phuBeMatFinalLayer, "EDGE", self.distanceSnap]
        arcpy.Snap_edit(self.ranhGioiPhuBeMatFinalLayer, [snapEnv])
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
    ranhGioiPhuBeMat = RanhGioiPhuBeMat(sys.argv[1])
    print "Running..."
    ranhGioiPhuBeMat.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass