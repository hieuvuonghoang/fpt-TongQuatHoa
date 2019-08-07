# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime
import ArcHydroTools

class Count:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDGiaoThong = "GiaoThong"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.field_FromNode = "FROM_NODE"
        self.field_ToNode = "TO_NODE"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer)
        #ArcHydroTools.GenerateFNodeTNode(self.doanTimDuongBoFinalLayer)
        #self.NumberMax()
        #self.UpdateFromNodeAndToNode()
        self.CreateFeatureClassPoint()
        self.RemovePoints()
        pass

    def NumberMax(self):
        self.out_table_Statistics = "in_memory\\out_table_Statistics"
        arcpy.Statistics_analysis (in_table = self.pathDoanTimDuongBoFinal,
                                   out_table = self.out_table_Statistics,
                                   statistics_fields = [[self.field_FromNode, "MAX"], [self.field_ToNode, "MAX"]])
        self.numberMax = 0
        with arcpy.da.SearchCursor(self.out_table_Statistics, ["MAX_" + self.field_FromNode, "MAX_" + self.field_ToNode]) as cursor:
            for feature in cursor:
                if feature[0] > feature[1]:
                    self.numberMax = int(feature[0])
                else:
                    self.numberMax = int(feature[1])
                break
        pass

    def UpdateFromNodeAndToNode(self):
        #C1
        for index in range(1, self.numberMax):
            arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.doanTimDuongBoFinalLayer,
                                                    selection_type = "NEW_SELECTION",
                                                    where_clause = self.field_FromNode + " = " + str(index) + " or " + self.field_ToNode + " = " + str(index))
            if int(arcpy.GetCount_management(self.doanTimDuongBoFinalLayer).getOutput(0)) == 2:
                with arcpy.da.UpdateCursor(self.doanTimDuongBoFinalLayer, [self.field_FromNode, self.field_ToNode]) as cursor:
                    for feature in cursor:
                        if int(feature[0]) == index:
                            feature[0] = 0
                        elif int(feature[1]) == index:
                            feature[1] = 0
                        cursor.updateRow(feature)
        #C2
        #for index in range(1, self.numberMax):
        #    count = 0
        #    arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.doanTimDuongBoFinalLayer,
        #                                            selection_type = "CLEAR_SELECTION")
        #    with arcpy.da.SearchCursor(self.doanTimDuongBoFinalLayer, [self.field_FromNode, self.field_ToNode]) as cursor:
        #        for feature in cursor:
        #            if int(feature[0]) == index or int(feature[1]) == index:
        #                count += 1
        #    if count == 2:
        #        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.doanTimDuongBoFinalLayer,
        #                                                selection_type = "NEW_SELECTION",
        #                                                where_clause = self.field_FromNode + " = " + str(index) + " or " + self.field_ToNode + " = " + str(index))
        #        with arcpy.da.UpdateCursor(self.doanTimDuongBoFinalLayer, [self.field_FromNode, self.field_ToNode]) as cursor:
        #            for feature in cursor:
        #                if int(feature[0]) == index:
        #                    feature[0] = 0
        #                elif int(feature[1]) == index:
        #                    feature[1] = 0
        #                cursor.updateRow(feature)
        pass

    def CreateFeatureClassPoint(self):
        self.pointStart = "in_memory\\pointStart"
        self.pointEnd = "in_memory\\pointEnd"
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.doanTimDuongBoFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = self.field_FromNode + " <> 0")
        arcpy.FeatureVerticesToPoints_management(in_features = self.doanTimDuongBoFinalLayer,
                                                 out_feature_class = self.pointStart,
                                                 point_location = "START")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.doanTimDuongBoFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = self.field_ToNode + " <> 0")
        arcpy.FeatureVerticesToPoints_management(in_features = self.doanTimDuongBoFinalLayer,
                                                 out_feature_class = self.pointEnd,
                                                 point_location = "END")
        self.pointTemp = os.path.join(self.pathProcessGDB, "PointTemp")
        arcpy.CreateFeatureclass_management(out_path = self.pathProcessGDB,
                                            out_name = "PointTemp",
                                            geometry_type = "POINT",
                                            spatial_reference = arcpy.Describe(self.pathDoanTimDuongBoFinal).spatialReference)
        with arcpy.da.SearchCursor(self.pointStart, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(self.pointTemp, ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], ))
        with arcpy.da.SearchCursor(self.pointEnd, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(self.pointTemp, ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], ))
        pass

    def RemovePoints(self):
        self.pointTemp = os.path.join(self.pathProcessGDB, "PointTemp")
        self.tempTableA = "in_memory\\tempTableA"
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.doanTimDuongBoFinalLayer,
                                                selection_type = "CLEAR_SELECTION")
        arcpy.GenerateNearTable_analysis(in_features = self.pointTemp,
                                         near_features = self.doanTimDuongBoFinalLayer,
                                         out_table = self.tempTableA,
                                         search_radius = "0 Meters",
                                         closest = "ALL",
                                         closest_count = "0");
        self.tempTableB = "in_memory\\tempTableB"
        arcpy.Statistics_analysis(in_table = self.tempTableA,
                            out_table = self.tempTableB,
                            statistics_fields = [["OBJECTID", "COUNT"]],
                            case_field = ["IN_FID"])
        self.tempTableC = "in_memory\\tempTableC"
        arcpy.TableSelect_analysis(in_table = self.tempTableB,
                                   out_table = self.tempTableC,
                                   where_clause = "FREQUENCY = 1")
        self.pointTempLayer = "pointTempLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointTemp,
                                          out_layer = self.pointTempLayer)
        arcpy.AddJoin_management(in_layer_or_view = self.pointTempLayer,
                                 in_field = "OBJECTID",
                                 join_table = self.tempTableC,
                                 join_field = "IN_FID")
        sqlQuery = "tempTableC." + str("IN_FID") + " IS NOT NULL"
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.pointTempLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        arcpy.RemoveJoin_management(in_layer_or_view = self.pointTempLayer,
                                    join_name = "tempTableC")
        with arcpy.da.UpdateCursor(self.pointTempLayer, ["OID@"]) as cursor:
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
    count = Count()
    print "Running..."
    count.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass