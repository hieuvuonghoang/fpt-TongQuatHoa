# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime
import subprocess

class RemoveFeatureRanhGioiPhuBeMat:

    def __init__(self):
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
        self.AddField()
        self.FeatureToLine()
        self.Erase()
        self.JoinAndRemove()
        pass

    def AddField(self):
        self.fieldFID_RanhGioiPhuBeMat = "FID_RanhGioiPhuBeMat"
        arcpy.AddField_management(in_table = self.pathRanhGioiPhuBeMatProcess,
                                  field_name = self.fieldFID_RanhGioiPhuBeMat,
                                  field_type = "LONG")
        arcpy.CalculateField_management(in_table = self.pathRanhGioiPhuBeMatProcess,
                                        field = self.fieldFID_RanhGioiPhuBeMat,
                                        expression = "!OBJECTID!",
                                        expression_type = "PYTHON_9.3")
        pass

    def FeatureToLine(self):
        self.phuBeMatProcessFeatureToLine = "in_memory\\phuBeMatProcessFeatureToLine"
        arcpy.FeatureToLine_management(in_features = self.pathPhuBeMatProcess,
                                       out_feature_class = self.phuBeMatProcessFeatureToLine)
        pass

    def Erase(self):
        self.outPutErase = "in_memory\\outPutErase"
        arcpy.Erase_analysis(in_features = self.pathRanhGioiPhuBeMatProcess,
                             erase_features = self.phuBeMatProcessFeatureToLine,
                             out_feature_class = self.outPutErase)
        pass

    def JoinAndRemove(self):
        self.outTableTemp = "in_memory\\outTableTemp"
        arcpy.TableSelect_analysis(in_table = self.outPutErase,
                                   out_table = self.outTableTemp)
        self.ranhGioiPhuBeMatLayer = "RanhGioiPhuBeMatLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatProcess,
                                          out_layer = self.ranhGioiPhuBeMatLayer)
        arcpy.AddJoin_management(in_layer_or_view = self.ranhGioiPhuBeMatLayer,
                                 in_field = "OBJECTID",
                                 join_table = self.outTableTemp,
                                 join_field = self.fieldFID_RanhGioiPhuBeMat)
        sqlQuery = "outTableTemp." + str(self.fieldFID_RanhGioiPhuBeMat) + " IS NOT NULL"
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.ranhGioiPhuBeMatLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        arcpy.RemoveJoin_management(in_layer_or_view = self.ranhGioiPhuBeMatLayer,
                                    join_name = "outTableTemp")
        with arcpy.da.UpdateCursor(self.ranhGioiPhuBeMatLayer, ["OID@"]) as cursor:
            for row in cursor:
                cursor.deleteRow()
        arcpy.DeleteField_management(in_table = self.pathRanhGioiPhuBeMatProcess,
                                     drop_field = [self.fieldFID_RanhGioiPhuBeMat])
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
    removeFeatureRanhGioiPhuBeMat = RemoveFeatureRanhGioiPhuBeMat()
    print "Running..."
    removeFeatureRanhGioiPhuBeMat.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass