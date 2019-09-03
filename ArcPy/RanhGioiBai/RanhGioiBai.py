# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import hashlib
import datetime

class RanhGioiBai:
    
    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fCRanhGioiBai = "RanhGioiBai"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        self.fCDuongMepNuoc = "DuongMepNuoc"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = "C:\\Generalize_25_50\\50K_Final.gdb"
        pathBaiBoiFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCRanhGioiBai)
        outPutFeatureToLine = "in_memory\\outPutFeatureToLine"
        arcpy.PolygonToLine_management(in_features = pathBaiBoiFinal,
                                       out_feature_class = outPutFeatureToLine)
        pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        #
        outPutEraseBoNuoc = "in_memory\\outPutEraseBoNuoc"
        arcpy.Erase_analysis(in_features = outPutFeatureToLine,
                             erase_features = pathDuongBoNuocFinal,
                             out_feature_class = outPutEraseBoNuoc,
                             cluster_tolerance = "0 Meters")
        outPutEraseMepNuoc = "in_memory\\outPutEraseMepNuoc"
        arcpy.Erase_analysis(in_features = outPutEraseBoNuoc,
                             erase_features = outPutEraseMepNuoc,
                             out_feature_class = outPutEraseMepNuoc,
                             cluster_tolerance = "0 Meters")
        
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
    ranhGioiBai = RanhGioiBai()
    print "Running..."
    ranhGioiBai.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass