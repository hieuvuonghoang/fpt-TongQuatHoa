# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import hashlib
import datetime

class NutDoanTimDuongBo:

   def __init__(self):
       self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
       self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
       self.fDGiaoThong = "GiaoThong"
       self.fCDoanTimDuongBo = "DoanTimDuongBo"
       self.fCDoanDuongSat = "DoanDuongSat"
       self.fCNutMangDuongBo = "NutMangDuongBo"
       self.fCNutDuongSat = "NutDuongSat"
       self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
       self.pathDoanDuongSatFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanDuongSat)
       self.pathNutMangDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCNutMangDuongBo)
       self.pathNutDuongSatFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCNutDuongSat)
       pass

   def Execute(self):
       #
       arcpy.env.overwriteOutput = True
       #
       doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
       arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                         out_layer = doanTimDuongBoFinalLayer)
       fCNodeA, fCNodeB = self.CreateFeaturePointIntersectLine(doanTimDuongBoFinalLayer)
       fCNodeC = self.CreatePointRemove(doanTimDuongBoFinalLayer)
       fCNodeD = self.CreateFeaturePoint(doanTimDuongBoFinalLayer, fCNodeA, fCNodeB, fCNodeC)
       self.UpdateNode(doanTimDuongBoFinalLayer, self.pathNutMangDuongBoFinal, fCNodeD, "HA10", self.fCDoanTimDuongBo)
       #
       doanDuongSatFinalLayer = "doanDuongSatFinalLayer"
       arcpy.MakeFeatureLayer_management(in_features = self.pathDoanDuongSatFinal,
                                         out_layer = doanDuongSatFinalLayer)
       fCNodeA, fCNodeB = self.CreateFeaturePointIntersectLine(doanDuongSatFinalLayer)
       fCNodeC = self.CreatePointRemove(doanDuongSatFinalLayer)
       fCNodeD = self.CreateFeaturePoint(doanDuongSatFinalLayer, fCNodeA, fCNodeB, fCNodeC)
       self.UpdateNode(doanDuongSatFinalLayer, self.pathNutDuongSatFinal, fCNodeD, "HB04", self.fCDoanDuongSat)
       pass

   def CreateFeaturePointIntersectLine(self, lineLayer):
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       # Intersect
       fCPointIntersectLine = "in_memory\\fCPointIntersectLine"
       arcpy.Intersect_analysis(in_features = [lineLayer, lineLayer],
                                out_feature_class = fCPointIntersectLine,
                                join_attributes = "ONLY_FID",
                                output_type = "POINT")
       # MultipartToSinglepart
       fCMultiPointToPoint = "in_memory\\fCMultiPointToPoint"
       arcpy.MultipartToSinglepart_management(in_features =fCPointIntersectLine,
                                              out_feature_class = fCMultiPointToPoint)
       # Add Field MD5
       arcpy.AddField_management(in_table = fCMultiPointToPoint,
                                 field_name = "MD5",
                                 field_type = "TEXT",
                                 field_length = "32")
       # Update Field MD5
       with arcpy.da.UpdateCursor(fCMultiPointToPoint, ["Shape@XY", "MD5"]) as cursor:
           for row in cursor:
               x, y = row[0]
               strPoint = str(x) + str(y)
               row[1] = str(hashlib.md5(strPoint.encode()).hexdigest())
               cursor.updateRow(row)
       # Statistics
       tableTemp = "in_memory\\tableTemp"
       arcpy.Statistics_analysis(in_table = fCMultiPointToPoint,
                                 out_table = tableTemp,
                                 statistics_fields = [["OBJECTID", "FIRST"]],
                                 case_field = "MD5")
       # 
       multiPointToPointLayer = "multiPointToPointLayer"
       arcpy.MakeFeatureLayer_management(in_features = fCMultiPointToPoint,
                                         out_layer = multiPointToPointLayer)
       arcpy.AddJoin_management(in_layer_or_view = multiPointToPointLayer,
                                in_field = "OBJECTID",
                                join_table = tableTemp,
                                join_field = "FIRST_OBJECTID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = multiPointToPointLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tableTemp.FIRST_OBJECTID IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = multiPointToPointLayer,
                                   join_name = "tableTemp")
       fCPointTemp = "in_memory\\fCPointTemp"
       #fCPointTemp = os.path.join(self.pathProcessGDB, "fCPointTemp")
       arcpy.CopyFeatures_management(in_features = multiPointToPointLayer,
                                     out_feature_class = fCPointTemp)
       #
       fCPointTempLayer = "fCPointTempLayer"
       arcpy.MakeFeatureLayer_management(in_features = fCPointTemp,
                                         out_layer = fCPointTempLayer)
       tableTempNear = "in_memory\\tableTempNear"
       arcpy.GenerateNearTable_analysis(in_features = fCPointTempLayer,
                                        near_features = lineLayer,
                                        out_table = tableTempNear,
                                        search_radius = "0 Meters",
                                        closest = "ALL")
       tableTempNearStatistics = "in_memory\\tableTempNearStatistics"
       arcpy.Statistics_analysis(in_table = tableTempNear,
                                 out_table = tableTempNearStatistics,
                                 statistics_fields = [["NEAR_FID", "COUNT"]],
                                 case_field = "IN_FID")
       tableSelectTemp = "in_memory\\tableSelectTemp"
       arcpy.TableSelect_analysis(in_table = tableTempNearStatistics,
                                  out_table = tableSelectTemp,
                                  where_clause = "FREQUENCY > 2")
       #
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCPointTempLayer,
                                               selection_type = "CLEAR_SELECTION")
       arcpy.AddJoin_management(in_layer_or_view = fCPointTempLayer,
                                in_field = "OBJECTID",
                                join_table = tableSelectTemp,
                                join_field = "IN_FID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCPointTempLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tableSelectTemp.IN_FID IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = fCPointTempLayer,
                                   join_name = "tableSelectTemp")
       fCNodeA = "in_memory\\fCNodeA"
       #fCNodeA = os.path.join(self.pathProcessGDB, "fCNodeA")
       arcpy.CopyFeatures_management(in_features = fCPointTempLayer,
                                     out_feature_class = fCNodeA)
       #
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCPointTempLayer,
                                               selection_type = "CLEAR_SELECTION")
       arcpy.AddJoin_management(in_layer_or_view = fCPointTempLayer,
                                in_field = "OBJECTID",
                                join_table = tableSelectTemp,
                                join_field = "IN_FID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCPointTempLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tableSelectTemp.IN_FID IS NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = fCPointTempLayer,
                                   join_name = "tableSelectTemp")
       fCNodeB = "in_memory\\fCNodeB"
       #fCNodeB = os.path.join(self.pathProcessGDB, "fCNodeB")
       arcpy.CopyFeatures_management(in_features = fCPointTempLayer,
                                     out_feature_class = fCNodeB)
       #
       return fCNodeA, fCNodeB
       pass

   def CreateFeaturePoint(self, lineLayer, fCNodeA, fCNodeB, fCNodeC):
       #
       fCNodeD = "in_memory\\fCNodeD"
       arcpy.Erase_analysis(in_features = fCNodeB,
                            erase_features = fCNodeC,
                            out_feature_class = fCNodeD,
                            cluster_tolerance = "0 Meters")
       #
       fCNodeE = "in_memory\\fCNodeE"
       #fCNodeE = os.path.join(self.pathProcessGDB, fCNameClassPoint)
       arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                           out_name = "fCNodeE",
                                           geometry_type = "POINT",
                                           spatial_reference = arcpy.Describe(lineLayer).spatialReference)
       #
       with arcpy.da.SearchCursor(fCNodeA, ["Shape@"]) as cursorA:
           with arcpy.da.InsertCursor(fCNodeE, ["Shape@"]) as cursorB:
               for rowA in cursorA:
                   cursorB.insertRow((rowA[0], ))
       with arcpy.da.SearchCursor(fCNodeD, ["Shape@"]) as cursorA:
           with arcpy.da.InsertCursor(fCNodeE, ["Shape@"]) as cursorB:
               for rowA in cursorA:
                   cursorB.insertRow((rowA[0], ))
       #
       return fCNodeE
       pass

   def CreatePointRemove(self, lineLayer):
       #
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       #
       fCPointBothEnds = "in_memory\\fCPointBothEnds"
       #fCPointBothEnds = os.path.join(self.pathProcessGDB, "fCPointBothEnds")
       arcpy.FeatureVerticesToPoints_management(in_features = lineLayer,
                                                out_feature_class = fCPointBothEnds,
                                                point_location = "BOTH_ENDS")
       #
       arcpy.AddField_management(in_table = fCPointBothEnds,
                                 field_name = "MD5",
                                 field_type = "TEXT",
                                 field_length = "32")
       with arcpy.da.UpdateCursor(fCPointBothEnds, ["Shape@XY", "MD5"]) as cursor:
           for row in cursor:
               x, y = row[0]
               strPoint = str(x) + str(y)
               row[1] = str(hashlib.md5(strPoint.encode()).hexdigest())
               cursor.updateRow(row)
       #
       tableTemp = "in_memory\\tableTemp"
       arcpy.Statistics_analysis(in_table = fCPointBothEnds,
                                 out_table = tableTemp,
                                 statistics_fields = [["OBJECTID", "FIRST"]],
                                 case_field = "MD5")
       tableTempFinal = "in_memory\\tableTempFinal"
       arcpy.TableSelect_analysis(in_table = tableTemp,
                                  out_table = tableTempFinal,
                                  where_clause = "FREQUENCY = 2")
       #
       fCPointBothEndsLayer = "fCPointBothEndsLayer"
       arcpy.MakeFeatureLayer_management(in_features = fCPointBothEnds,
                                         out_layer = fCPointBothEndsLayer)
       arcpy.AddJoin_management(in_layer_or_view = fCPointBothEndsLayer,
                                in_field = "OBJECTID",
                                join_table = tableTempFinal,
                                join_field = "FIRST_OBJECTID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCPointBothEndsLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tableTempFinal.FIRST_OBJECTID IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = fCPointBothEndsLayer,
                                   join_name = "tableTempFinal")
       fCPointBothEndsFinal = "in_memory\\fCPointBothEndsFinal"
       #fCPointBothEndsFinal = os.path.join(self.pathProcessGDB, "fCPointBothEndsFinal")
       arcpy.CopyFeatures_management(in_features = fCPointBothEndsLayer,
                                     out_feature_class = fCPointBothEndsFinal)
       #
       return fCPointBothEndsFinal
       pass

   def UpdateNode(self, lineLayer, fCNodeA, fCNodeB, maDoiTuong, fCLineName):
       #
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       #
       #tableTempNear = os.path.join(self.pathProcessGDB, "tableTempNear")
       tableTempNear = "in_memory\\tableTempNear"
       arcpy.GenerateNearTable_analysis(in_features = fCNodeB,
                                        near_features = lineLayer,
                                        out_table = tableTempNear,
                                        search_radius = "0 Meters")
       #
       arcpy.AddJoin_management(in_layer_or_view = lineLayer,
                                in_field = "OBJECTID",
                                join_table = tableTempNear,
                                join_field = "NEAR_FID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "NEAR_FID IS NOT NULL")
       fCTempA = "in_memory\\fCTempA"
       #fCTempA = os.path.join(self.pathProcessGDB, "fCTempA")
       arcpy.CopyFeatures_management(in_features = lineLayer,
                                     out_feature_class = fCTempA)
       arcpy.RemoveJoin_management(in_layer_or_view = lineLayer,
                                   join_name = "tableTempNear")
       #
       tableTempA = "in_memory\\tableTempA"
       #tableTempA = os.path.join(self.pathProcessGDB, "tableTempA")
       arcpy.TableSelect_analysis(in_table = fCTempA,
                                  out_table = tableTempA,
                                  where_clause = "OBJECTID IS NOT NULL")
       #
       arcpy.DeleteRows_management(in_rows = fCNodeA)
       #
       with arcpy.da.SearchCursor(tableTempNear, ["IN_FID", "NEAR_FID"]) as cursorTempNear:
           with arcpy.da.SearchCursor(fCNodeB, ["OID@", "Shape@"]) as cursorNodeB:
               with arcpy.da.SearchCursor(tableTempA, ["OID@", fCLineName + "_ngayThuNhan", fCLineName + "_ngayCapNhat", fCLineName + "_nguonDuLieu", fCLineName + "_maTrinhBay", fCLineName + "_tenManh", fCLineName + "_soPhienHieuManhBanDo", "tableTempNear_NEAR_FID"]) as cursorTempA:
                   with arcpy.da.InsertCursor(fCNodeA, ["Shape@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "maTrinhBay", "tenManh", "soPhienHieuManhBanDo", "maDoiTuong", "maNhanDang"]) as cursorNodeA:
                       for rowTempNear in cursorTempNear:
                           cursorNodeB.reset()
                           for rowNodeB in cursorNodeB:
                               if rowTempNear[0] == rowNodeB[0]:
                                   cursorTempA.reset()
                                   for rowTempA in cursorTempA:
                                       if rowTempA[7] == rowTempNear[1]:
                                           cursorNodeA.insertRow((rowNodeB[1], rowTempA[1], rowTempA[2], rowTempA[3], rowTempA[4], rowTempA[5], rowTempA[6], maDoiTuong, "Auto"))
                                           break
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

if __name__ == "__main__":
    runTime = RunTime()
    nutDoanTimDuongBo = NutDoanTimDuongBo()
    print "Running..."
    nutDoanTimDuongBo.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass