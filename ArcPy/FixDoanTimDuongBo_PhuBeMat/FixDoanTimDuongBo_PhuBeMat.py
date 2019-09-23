# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class FixDoanTimDuongBoPBM:

    def __init__(self):
        self.pathFinalGDB = r"C:\Generalize_25_50_B\50K_Final.gdb"
        self.pathProcessGDB = r"C:\Generalize_25_50_B\50K_Process.gdb"
        pass

    def Execute(self):
        #
        arcpy.env.overwriteOutput = True
        doanTimDuongBo = os.path.join(os.path.join(self.pathFinalGDB, "GiaoThong"), "DoanTimDuongBo")
        phuBeMat = os.path.join(os.path.join(self.pathFinalGDB, "PhuBeMat"), "PhuBeMat")
        # Create ProcessGDB\PhuBeMat\PhuBeMatLine
        phuBeMatToLine = os.path.join(os.path.join(self.pathProcessGDB, "PhuBeMat"), "PhuBeMatToLine")
        if arcpy.Exists(phuBeMatToLine):
            arcpy.Delete_management(phuBeMatToLine)
        arcpy.PolygonToLine_management(in_features = phuBeMat,
                                       out_feature_class = phuBeMatToLine)
        # Create ProcessGDB\PhuBeMat\PhuBeMatLineIntersectDoanTimDuongBo
        phuBeMatLineIntersectDoanTimDuongBo = os.path.join(os.path.join(self.pathProcessGDB, "PhuBeMat"), "PhuBeMatLineIntersectDoanTimDuongBo")
        if arcpy.Exists(phuBeMatLineIntersectDoanTimDuongBo):
            arcpy.Delete_management(phuBeMatLineIntersectDoanTimDuongBo)
        arcpy.Intersect_analysis(in_features = [phuBeMatToLine, doanTimDuongBo],
                                 out_feature_class = phuBeMatLineIntersectDoanTimDuongBo,
                                 join_attributes = "ONLY_FID",
                                 cluster_tolerance = "0.5 Meters",
                                 output_type = "LINE")
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

if __name__ == '__main__':
    runTime = RunTime()
    fixDoanTimDuongBoPBM = FixDoanTimDuongBoPBM()
    print "Running..."
    fixDoanTimDuongBoPBM.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass