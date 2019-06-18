# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import codecs
import datetime
from arcpy.sa import *

class CreateDuongBinhDoPhu:

    def __init__(self, contourInterval, baseContour, zFactor):
        self.contourInterval = contourInterval
        self.baseContour = baseContour
        self.zFactor = zFactor
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.fDDiaHinh = "DiaHinh"
        self.fCDuongBinhDo = "DuongBinhDo"
        self.fCDuongBinhDoPhu = "DuongBinhDo_Phu"
        self.pathRaster = "C:\\Generalize_25_50\\Input.tif"
        self.pathDiaHinh = os.path.join(self.pathProcessGDB, self.fDDiaHinh)
        self.pathDuongBinhDoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDDiaHinh), self.fCDuongBinhDo)
        self.pathDuongBinhDoPhuProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDDiaHinh), self.fCDuongBinhDoPhu)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = self.pathProcessGDB
        self.RunContourTool()
        self.InitFeatureDuongBinhDoPhu()
        self.InsertDuongBinhDoPhu()
        #self.DeleteTempFeatureClass()
        pass

    def RunContourTool(self):
        self.duongBinhDoPhuTemp = os.path.join(self.pathProcessGDB, "outcontours")
        Contour(in_raster = self.pathRaster,
                out_polyline_features = self.duongBinhDoPhuTemp,
                contour_interval = self.contourInterval,
                base_contour = self.baseContour,
                z_factor = self.zFactor)
        pass

    def InitFeatureDuongBinhDoPhu(self):
        arcpy.CreateFeatureclass_management(out_path = self.pathDiaHinh,
                                            out_name = self.fCDuongBinhDoPhu,
                                            geometry_type = "POLYLINE",
                                            template = [self.pathDuongBinhDoProcess])
        pass

    def InsertDuongBinhDoPhu(self):
        duongBinhDoPhuTempLayer = "duongBinhDoPhuTempLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.duongBinhDoPhuTemp,
                                          out_layer = duongBinhDoPhuTempLayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongBinhDoPhuTempLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "Contour > 0")
        with arcpy.da.SearchCursor(duongBinhDoPhuTempLayer, ["Shape@", "Contour"]) as sCur:
            with arcpy.da.InsertCursor(self.pathDuongBinhDoPhuProcess, ["Shape@", "doCaoH", "loaiKieuDuongBinhDo", "loaiDuongBinhDo", "doiTuong", "DuongBinhDo_Rep_ID"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], row[1], 2, 3, 1, 4))
        pass

    def DeleteTempFeatureClass(self):
        arcpy.Delete_management(in_data = self.duongBinhDoPhuTemp)
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
    print "Contour Interval = {0}\nBase Contour = {1}\nZFactor = {2}".format(sys.argv[1], sys.argv[2], sys.argv[3])
    createDuongBinhDoPhu = CreateDuongBinhDoPhu(sys.argv[1], sys.argv[2], sys.argv[3])
    print "Running..."
    createDuongBinhDoPhu.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass