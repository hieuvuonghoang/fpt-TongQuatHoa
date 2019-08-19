# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import codecs
import datetime

class ReadIDPhuBeMat:

    def __init__(self):
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDPhuBeMat = "PhuBeMat"
        self.fCPhuBeMat = "PhuBeMat"
        self.pathFCPhuBeMatFinal = os.path.join(self.pathFinalGDB, os.path.join(self.fDPhuBeMat, self.fCPhuBeMat))
        pass

    def Execute(self):
        phuBeMatFinalLayer = "phuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathFCPhuBeMatFinal,
                                          out_layer = phuBeMatFinalLayer)
        #with arcpy.da.UpdateCursor(phuBeMatFinalLayer, ["PhuBeMat_Rep_ID"]) as cursor:
        #    for row in cursor:
        #        row[0] = None
        #        cursor.updateRow(row)
        arrListRuleIDPhuBeMatCay = range(0, 5)
        arrListRuleIDPhuBeMatCay.append(-1)
        for ruleID in arrListRuleIDPhuBeMatCay:
            print "... {0} ".format(str(ruleID))
            querySQL = "PhuBeMat_Rep_ID = " + str(ruleID)
            #querySQL = "PhuBeMat_Nen_ID = " + str(ruleID)
            arcpy.SelectLayerByAttribute_management(in_layer_or_view = phuBeMatFinalLayer,
                                                    selection_type = "CLEAR_SELECTION")
            arcpy.SelectLayerByAttribute_management(in_layer_or_view = phuBeMatFinalLayer,
                                                    selection_type = "NEW_SELECTION",
                                                    where_clause = querySQL)
            with arcpy.da.SearchCursor(phuBeMatFinalLayer, ["loaiPhuBeMat", "doiTuong", "phanLoaiVung"]) as cursor:
                for row in cursor:
                    print "\t... loaiPhuBeMat: {0}, doiTuong: {1}, phanLoaiVung: {2}".format(str(row[0]), str(row[1]), str(row[2]))
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
    readIDPhuBeMat = ReadIDPhuBeMat()
    print "Running..."
    readIDPhuBeMat.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass