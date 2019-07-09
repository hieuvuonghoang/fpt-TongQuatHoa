# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import codecs
import datetime

class Contour:

    def __init__(self, contourInterval, baseContour, zFactor):
        self.contourInterval = contourInterval
        self.baseContour = baseContour
        self.zFactor = zFactor
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathRaster = "C:\\Generalize_25_50\\Input.tif"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.pathProcessGDB
        self.RunContourTool()
        pass

    def RunContourTool(self):
        self.duongBinhDoPhuTemp = os.path.join(self.pathProcessGDB, "OutContours")
        arcpy.sa.Contour(in_raster = self.pathRaster,
                out_polyline_features = self.duongBinhDoPhuTemp,
                contour_interval = self.contourInterval,
                base_contour = self.baseContour,
                z_factor = self.zFactor)
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
    print "Contour Interval = {0}, Base Contour = {1}, ZFactor = {2}".format(sys.argv[1], sys.argv[2], sys.argv[3])
    contour = Contour(sys.argv[1], sys.argv[2], sys.argv[3])
    #contour = Contour("5", "2.5", "1")
    print "Running..."
    contour.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass