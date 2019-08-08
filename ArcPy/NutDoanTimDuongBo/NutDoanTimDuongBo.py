# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import hashlib
import datetime
import ArcHydroTools


class NutDoanTimDuongBo:

   def __init__(self):
       self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
       self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
       self.fDGiaoThong = "GiaoThong"
       self.fCDoanTimDuongBo = "DoanTimDuongBo"
       self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
       pass

   def Execute(self):
       arcpy.env.overwriteOutput = True
       self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
       arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                         out_layer = self.doanTimDuongBoFinalLayer)
       #fCNodeA, fCNodeB = self.CreateFeaturePointIntersectLine(self.doanTimDuongBoFinalLayer)
       self.ProcessFromToNode(self.doanTimDuongBoFinalLayer)
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

   def ProcessFromToNode(self, lineLayer):
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       #
       ArcHydroTools.GenerateFNodeTNode(lineLayer)
       #
       tableTempFromNode = "in_memory\\tableTempFromNode"
       arcpy.Statistics_analysis(in_table = lineLayer,
                                 out_table = tableTempFromNode,
                                 statistics_fields = [["OBJECTID", "COUNT"]],
                                 case_field = "FROM_NODE")
       tableTempToNode = "in_memory\\tableTempToNode"
       arcpy.Statistics_analysis(in_table = lineLayer,
                                 out_table = tableTempToNode,
                                 statistics_fields = [["OBJECTID", "COUNT"]],
                                 case_field = "TO_NODE")
       #
       tableTempProessNode = "in_memory\\tableTempProessNode"
       arcpy.CreateTable_management(out_path = "in_memory",
                                    out_name = "tableTempProessNode")
       arcpy.AddField_management(in_table = tableTempProessNode,
                                 field_name = "FROM_NODE",
                                 field_type = "LONG")
       arcpy.AddField_management(in_table = tableTempProessNode,
                                 field_name = "FROM_NODE_COUNT",
                                 field_type = "LONG")
       arcpy.AddField_management(in_table = tableTempProessNode,
                                 field_name = "TO_NODE",
                                 field_type = "LONG")
       arcpy.AddField_management(in_table = tableTempProessNode,
                                 field_name = "TO_NODE_COUNT",
                                 field_type = "LONG")
       #
       with arcpy.da.SearchCursor(tableTempFromNode, ["FROM_NODE", "FREQUENCY"]) as cursorA:
           with arcpy.da.SearchCursor(tableTempToNode, ["TO_NODE", "FREQUENCY"]) as cursorB:
               with arcpy.da.InsertCursor(tableTempProessNode, ["FROM_NODE", "FROM_NODE_COUNT", "TO_NODE", "TO_NODE_COUNT"]) as cursorC:
                   for rowA in cursorA:
                       cursorB.reset()
                       findRowA = False
                       toNodeCount = 0
                       for rowB in cursorB:
                           if rowA[0] == rowB[0]:
                               findRowA = True
                               toNodeCount = rowB[1]
                               break
                       if (findRowA == True and rowA[1] == 2 and toNodeCount == 0) or (findRowA == True and rowA[1] == 1 and toNodeCount == 1):
                           cursorC.insertRow((rowA[0], rowA[1], rowA[0], toNodeCount))
                       elif (findRowA == False and rowA[1] == 2):
                            cursorC.insertRow((rowA[0], rowA[1], 0, toNodeCount))
       #
       with arcpy.da.SearchCursor(tableTempFromNode, ["FROM_NODE", "FREQUENCY"]) as cursorA:
           with arcpy.da.SearchCursor(tableTempToNode, ["TO_NODE", "FREQUENCY"]) as cursorB:
               with arcpy.da.InsertCursor(tableTempProessNode, ["FROM_NODE", "FROM_NODE_COUNT", "TO_NODE", "TO_NODE_COUNT"]) as cursorC:
                   for rowA in cursorA:
                       cursorB.reset()
                       findRowA = False
                       toNodeCount = 0
                       for rowB in cursorB:
                           if rowA[0] == rowB[0]:
                               findRowA = True
                               toNodeCount = rowB[1]
                               break
                       if (findRowA == True and rowA[1] == 2 and toNodeCount == 0) or (findRowA == True and rowA[1] == 1 and toNodeCount == 1):
                           cursorC.insertRow((rowA[0], rowA[1], rowA[0], toNodeCount))
                       elif (findRowA == False and rowA[1] == 2):
                            cursorC.insertRow((rowA[0], rowA[1], 0, toNodeCount))
       #
       with arcpy.da.SearchCursor(tableTempProessNode, ["FROM_NODE", "FROM_NODE_COUNT", "TO_NODE", "TO_NODE_COUNT"]) as cursorA:
            for rowA in cursorA:
                print "{0}, {1}, {2}, {3}".format(str(rowA[0]), str(rowA[1]), str(rowA[2]), str(rowA[3]))      
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