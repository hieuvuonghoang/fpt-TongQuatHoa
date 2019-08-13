# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime
import subprocess

class DemoCreateFeatureClass:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        self.fCCongThuyLoiP = "CongThuyLoiP"
        self.fCCauGiaoThongP = "CauGiaoThongP"
        self.fCCongGiaoThongP = "CongGiaoThongP"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.cauGiaoThongPRepName = self.fCCauGiaoThongP + "_Rep"
        self.congGiaoThongPRepPhaiName = self.fCCongGiaoThongP + "_RepPhai"
        self.congGiaoThongPRepTraiName = self.fCCongGiaoThongP + "_RepTrai"
        self.congThuyLoiPRepName = self.fCCongThuyLoiP + "_Rep"
        self.pathCongThuyLoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        self.pathCauGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathCongGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.dirPathArcObject = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Release"), "SetAngleRepresentationPoint.exe")
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Update RuleID theo DoanTimDuongBo
        self.UpdateRuleIDCauGiaoThong()
        self.UpdateRuleIDCongGiaoThong()
        #
        #"PERPENDICULAR" 90
        #"PARALLEL" 0
        print self.dirPathArcObject
        self.UpdateAngle(self.pathDoanTimDuongBoFinal, self.pathCauGiaoThongPFinal, 0)
        subprocess.call([self.dirPathArcObject, self.pathFinalGDB, self.fCCauGiaoThongP, self.cauGiaoThongPRepName, ""])
        self.UpdateAngle(self.pathDoanTimDuongBoFinal, self.pathCongGiaoThongPFinal, 90)
        subprocess.call([self.dirPathArcObject, self.pathFinalGDB, self.fCCongGiaoThongP, self.congGiaoThongPRepPhaiName, ""])
        subprocess.call([self.dirPathArcObject, self.pathFinalGDB, self.fCCongGiaoThongP, self.congGiaoThongPRepTraiName, ""])
        self.UpdateAngle(self.pathDoanTimDuongBoFinal, self.pathCongThuyLoiPFinal, 0)
        subprocess.call([self.dirPathArcObject, self.pathFinalGDB, self.fCCongThuyLoiP, self.congThuyLoiPRepName, ""])
        pass

    def UpdateAngle(self, fCLine, fCPoint, angleTemp):
        #
        lineLayer = "lineLayer";
        arcpy.MakeFeatureLayer_management(fCLine, lineLayer)
        pointLayer = "pointLayer"
        arcpy.MakeFeatureLayer_management(fCPoint, pointLayer)

        #
        arcpy.AddField_management(in_table = pointLayer,
                                  field_name = "ANGLE",
                                  field_type = "DOUBLE")

        #
        with arcpy.da.UpdateCursor(pointLayer, ["OID@", "ANGLE"]) as cursorA:
            for rowA in cursorA:
                #
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = pointLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = lineLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = pointLayer,
                                                       selection_type = "NEW_SELECTION")
                fCTempPoint = "in_memory\\fCTempPoint"
                arcpy.FeatureVerticesToPoints_management(in_features = lineLayer,
                                                         out_feature_class = fCTempPoint,
                                                         point_location = "ALL")
                tableNearTemp = "in_memory\\tableNearTemp"
                arcpy.GenerateNearTable_analysis(in_features = pointLayer,
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
                        rowA[1] = rowB[0] - angleTemp
                        cursorA.updateRow(rowA)
                        break

        pass

    def UpdateRuleIDCauGiaoThong(self):
        #
        cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = cauGiaoThongPFinalLayer)
        doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.doanTimDuongBoFinalLayer,
                                          out_layer = doanTimDuongBoFinalLayer)
        # Generate Near Table
        outTableTempA = "in_memory\\OutTabelTempA"
        arcpy.GenerateNearTable_analysis(in_features = cauGiaoThongPFinalLayer,
                                         near_features = doanTimDuongBoFinalLayer,
                                         out_table = outTableTempA,
                                         search_radius = "0 Meters",
                                         closest = "CLOSEST",
                                         method = "PLANAR")
        # Add Field DoanTimDuongBo
        arcpy.AddField_management(in_table = cauGiaoThongPFinalLayer,
                                  field_name = "FID_DoanTimDuongBo",
                                  field_type = "LONG")
        arcpy.AddField_management(in_table = cauGiaoThongPFinalLayer,
                                  field_name = "RepIDTemp",
                                  field_type = "SHORT")
        # Table Select
        outTableTempB = "in_memory\\OutTabelTempB"
        arcpy.TableSelect_analysis(in_table = doanTimDuongBoFinalLayer,
                                   out_table = outTableTempB)
        fields = arcpy.ListFields(outTableTempB)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.name != "DoanTimDuongBo_Rep_ID" and fieldTemp.type != "OID":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = outTableTempB,
                                     drop_field = fieldsDelete)
        # Join
        arcpy.AddJoin_management(in_layer_or_view = cauGiaoThongPFinalLayer,
                                 in_field = "OBJECTID",
                                 join_table = outTableTempA,
                                 join_field = "IN_FID")
        arcpy.CalculateField_management(in_table = cauGiaoThongPFinalLayer,
                                        field = "FID_DoanTimDuongBo",
                                        expression = "!NEAR_FID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = cauGiaoThongPFinalLayer,
                                    join_name = outTableTempA.split("\\")[1])
        arcpy.AddJoin_management(in_layer_or_view = cauGiaoThongPFinalLayer,
                                 in_field = "FID_DoanTimDuongBo",
                                 join_table = outTableTempB,
                                 join_field = "OBJECTID")
        arcpy.CalculateField_management(in_table = cauGiaoThongPFinalLayer,
                                        field = "RepIDTemp",
                                        expression = "!DoanTimDuongBo_Rep_ID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = cauGiaoThongPFinalLayer,
                                    join_name = outTableTempB.split("\\")[1])
        # Update RuleID Using File Config:
        dataConfig = self.dictConfig[0]["dataConfig"]
        with arcpy.da.UpdateCursor(cauGiaoThongPFinalLayer, ["CauGiaoThongP_Rep_ID", "RepIDTemp"]) as cursor:
            for row in cursor:
                for elem in dataConfig:
                    if row[1] == int(elem["doanTimDuongBoRepID"]):
                        row[0] = int(elem["cauGiaoThongPRepID"])
                        cursor.updateRow(row)
                        break
        # Delete Filed
        arcpy.DeleteField_management(in_table = cauGiaoThongPFinalLayer,
                                     drop_field = ["FID_DoanTimDuongBo", "RepIDTemp"])
        pass

    def UpdateRuleIDCongGiaoThong(self):
        #
        congGiaoThongPFinalLayer = "congGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = congGiaoThongPFinalLayer)
        doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.doanTimDuongBoFinalLayer,
                                          out_layer = doanTimDuongBoFinalLayer)
        # Generate Near Table
        outTableTempA = "in_memory\\OutTabelTempA"
        arcpy.GenerateNearTable_analysis(in_features = congGiaoThongPFinalLayer,
                                         near_features = doanTimDuongBoFinalLayer,
                                         out_table = outTableTempA,
                                         search_radius = "0 Meters",
                                         closest = "CLOSEST",
                                         method = "PLANAR")
        # Add Field DoanTimDuongBo
        arcpy.AddField_management(in_table = congGiaoThongPFinalLayer,
                                  field_name = "FID_DoanTimDuongBo",
                                  field_type = "LONG")
        arcpy.AddField_management(in_table = congGiaoThongPFinalLayer,
                                  field_name = "RepIDTemp",
                                  field_type = "SHORT")
        # Table Select
        outTableTempB = "in_memory\\OutTabelTempB"
        arcpy.TableSelect_analysis(in_table = doanTimDuongBoFinalLayer,
                                   out_table = outTableTempB)
        fields = arcpy.ListFields(outTableTempB)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.name != "DoanTimDuongBo_Rep_ID" and fieldTemp.type != "OID":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = outTableTempB,
                                     drop_field = fieldsDelete)
        # Join
        arcpy.AddJoin_management(in_layer_or_view = congGiaoThongPFinalLayer,
                                 in_field = "OBJECTID",
                                 join_table = outTableTempA,
                                 join_field = "IN_FID")
        arcpy.CalculateField_management(in_table = congGiaoThongPFinalLayer,
                                        field = "FID_DoanTimDuongBo",
                                        expression = "!NEAR_FID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = congGiaoThongPFinalLayer,
                                    join_name = outTableTempA.split("\\")[1])
        arcpy.AddJoin_management(in_layer_or_view = congGiaoThongPFinalLayer,
                                 in_field = "FID_DoanTimDuongBo",
                                 join_table = outTableTempB,
                                 join_field = "OBJECTID")
        arcpy.CalculateField_management(in_table = congGiaoThongPFinalLayer,
                                        field = "RepIDTemp",
                                        expression = "!DoanTimDuongBo_Rep_ID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = congGiaoThongPFinalLayer,
                                    join_name = outTableTempB.split("\\")[1])
        # Update RuleID Using File Config:
        dataConfig = self.dictConfig[1]["dataConfig"]
        with arcpy.da.UpdateCursor(congGiaoThongPFinalLayer, ["CongGiaoThongP_RepTrai_ID", "CongGiaoThongP_RepPhai_ID", "RepIDTemp"]) as cursor:
            for row in cursor:
                for elem in dataConfig:
                    if row[2] == int(elem["doanTimDuongBoRepID"]) and elem["congGiaoThongPRepID"] != "NA":
                        row[0] = int(elem["congGiaoThongPRepID"])
                        row[1] = int(elem["congGiaoThongPRepID"])
                        cursor.updateRow(row)
                        break
        # Delete Filed
        arcpy.DeleteField_management(in_table = congGiaoThongPFinalLayer,
                                     drop_field = ["FID_DoanTimDuongBo", "RepIDTemp"])
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