# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class DeleteFeature:

    def __init__(self):
        self.pathProcessGDB = "C:\\QuanSuA\\5651_4_TB.gdb"
        pass

    def Execute(self):
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and (fcTemp.shapeType == "Polyline" or fcTemp.shapeType == "Polygon"):
                    if fcTemp.baseName == "QuanSuA" or fcTemp.baseName == "SongSuoiA" or fcTemp.baseName == "SongSuoiL" or fcTemp.baseName == "KenhMuongA" or fcTemp.baseName == "KenhMuongL" or fcTemp.baseName == "DoanTimDuongBo" or fcTemp.baseName == "QuanSuP":
                        continue
                    with arcpy.da.UpdateCursor(os.path.join(self.pathProcessGDB, os.path.join(fcDataSetTemp.baseName, fcTemp.baseName)), ["OID@"]) as cursor:
                        for row in cursor:
                            cursor.deleteRow()
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
    deleteFeature = DeleteFeature()
    print "Running..."
    deleteFeature.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass
