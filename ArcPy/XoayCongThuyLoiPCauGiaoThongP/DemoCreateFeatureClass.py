# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class DemoCreateFeatureClass:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        self.fCCongThuyLoiP = "CongThuyLoiP"
        self.fCCauGiaoThongP = "CauGiaoThongP"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.pathCongThuyLoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        self.pathCauGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.UpdateAngle()
        pass

    def UpdateAngle(self):

        #
        doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(self.pathDoanTimDuongBoFinal, doanTimDuongBoFinalLayer)
        cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(self.pathCauGiaoThongPFinal, cauGiaoThongPFinalLayer)

        #
        arcpy.AddField_management(in_table = cauGiaoThongPFinalLayer,
                                  field_name = "ANGLE",
                                  field_type = "DOUBLE")
        #
        with arcpy.da.UpdateCursor(cauGiaoThongPFinalLayer, ["OID@", "ANGLE"]) as cursorA:
            for rowA in cursorA:
                #
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = cauGiaoThongPFinalLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = doanTimDuongBoFinalLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = cauGiaoThongPFinalLayer,
                                                       selection_type = "NEW_SELECTION")
                fCTempPoint = "in_memory\\fCTempPoint"
                arcpy.FeatureVerticesToPoints_management(in_features = doanTimDuongBoFinalLayer,
                                                         out_feature_class = fCTempPoint,
                                                         point_location = "ALL")
                tableNearTemp = "in_memory\\tableNearTemp"
                arcpy.GenerateNearTable_analysis(in_features = cauGiaoThongPFinalLayer,
                                                 near_features = fCTempPoint,
                                                 out_table = tableNearTemp,
                                                 search_radius = "#",
                                                 angle = "ANGLE",
                                                 closest = "ALL")
                tableNearSortTemp = "in_memory\\tableNearSortTemp"
                arcpy.Sort_management(in_dataset = tableNearTemp,
                                      out_dataset = tableNearSortTemp,
                                      sort_field = [["NEAR_DIST", "ASCENDING"]])
                tableNearSortSelectTemp = "in_memory\\tableNearSortSelectTemp"
                arcpy.TableSelect_analysis(in_table = tableNearSortTemp,
                                           out_table = tableNearSortSelectTemp,
                                           where_clause = "OBJECTID = 2")
                with arcpy.da.SearchCursor(tableNearSortSelectTemp, ["NEAR_ANGLE"]) as cursorB:
                    for rowB in cursorB:
                        rowA[1] = rowB[0]
                        cursorA.updateRow(rowA)
                        break

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
    demoCreateFeatureClass = DemoCreateFeatureClass()
    print "Running..."
    demoCreateFeatureClass.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass