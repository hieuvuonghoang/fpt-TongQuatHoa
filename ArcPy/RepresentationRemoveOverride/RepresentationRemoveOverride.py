# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime

class RepresentationRemoveOverride:

    def __init__(self, pathGDB, featureClass, representationName, removeOption):
        self.pathGDB = pathGDB
        self.featureClass = featureClass
        self.representationName = representationName
        self.removeOption = removeOption
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.pathGDB
        arcpy.RemoveOverride_cartography(in_features = self.featureClass, representation = self.representationName, remove_option = self.removeOption)
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
    print "pathGDB: {0}, featureClass: {1}, representationName: {2}, removeOption: {3}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    representationRemoveOverride = RepresentationRemoveOverride(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print "Running..."
    representationRemoveOverride.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass