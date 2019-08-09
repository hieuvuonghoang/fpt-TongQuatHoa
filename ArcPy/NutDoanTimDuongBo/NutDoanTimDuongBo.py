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
       #
       arcpy.env.overwriteOutput = True
       #
       doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
       arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                         out_layer = doanTimDuongBoFinalLayer)
       fCNodeA, fCNodeB = self.CreateFeaturePointIntersectLine(doanTimDuongBoFinalLayer)
       fCNodeC = self.CreatePointRemove(doanTimDuongBoFinalLayer)
       self.CreateFeaturePoint(doanTimDuongBoFinalLayer, fCNodeA, fCNodeB, fCNodeC)
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
       #tableTempProessNode = os.path.join(self.pathProcessGDB, "tableTempProessNode")
       arcpy.CreateTable_management(out_path = self.pathProcessGDB,
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
       # Insert Data tableTempProessNode
       ##
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
                       if (findRowA == True and rowA[1] == 1 and toNodeCount == 1):
                           cursorC.insertRow((rowA[0], rowA[1], rowA[0], toNodeCount))
                       elif (findRowA == False and rowA[1] == 2):
                            cursorC.insertRow((rowA[0], rowA[1], 0, 0))
       ##
       with arcpy.da.SearchCursor(tableTempFromNode, ["FROM_NODE", "FREQUENCY"]) as cursorA:
           with arcpy.da.SearchCursor(tableTempToNode, ["TO_NODE", "FREQUENCY"]) as cursorB:
               with arcpy.da.InsertCursor(tableTempProessNode, ["FROM_NODE", "FROM_NODE_COUNT", "TO_NODE", "TO_NODE_COUNT"]) as cursorC:
                   for rowB in cursorB:
                       cursorA.reset()
                       findRowB = False
                       for rowA in cursorA:
                           if rowB[0] == rowA[0]:
                               findRowB = True
                               break
                       if (findRowB == False and rowB[1] == 2):
                            cursorC.insertRow((0, 0, rowB[0], rowB[1]))
       #
       tempTableFinalFromNode = "in_memory\\tempTableFinalFromNode"
       arcpy.TableSelect_analysis(in_table = tableTempProessNode,
                                  out_table = tempTableFinalFromNode,
                                  where_clause = "FROM_NODE <> 0 AND TO_NODE = 0")
       tempTableFinalFromNodeToNode = "in_memory\\tempTableFinalFromNodeToNode"
       arcpy.TableSelect_analysis(in_table = tableTempProessNode,
                                  out_table = tempTableFinalFromNodeToNode,
                                  where_clause = "FROM_NODE <> 0 AND TO_NODE <> 0")
       tempTableFinalToNode = "in_memory\\tempTableFinalToNode"
       arcpy.TableSelect_analysis(in_table = tableTempProessNode,
                                  out_table = tempTableFinalToNode,
                                  where_clause = "FROM_NODE = 0 AND TO_NODE <> 0")
       # FromNode
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       arcpy.AddJoin_management(in_layer_or_view = lineLayer,
                                in_field = "FROM_NODE",
                                join_table = tempTableFinalFromNode,
                                join_field = "FROM_NODE")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tempTableFinalFromNode.FROM_NODE IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = lineLayer,
                                   join_name = "tempTableFinalFromNode")
       fCTempA = "in_memory\\fCTempA"
       arcpy.CopyFeatures_management(in_features = lineLayer,
                                     out_feature_class = fCTempA)
       fCTempALayer = "fCTempALayer"
       arcpy.MakeFeatureLayer_management(in_features = fCTempA,
                                         out_layer = fCTempALayer)
       tempTableFromNodeID = "in_memory\\tempTableFromNodeID"
       arcpy.Statistics_analysis(in_table = fCTempALayer,
                                 out_table = tempTableFromNodeID,
                                 statistics_fields = [["OBJECTID", "FIRST"]],
                                 case_field = ["FROM_NODE"])
       arcpy.AddJoin_management(in_layer_or_view = fCTempALayer,
                                in_field = "OBJECTID",
                                join_table = tempTableFromNodeID,
                                join_field = "FIRST_OBJECTID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempALayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tempTableFromNodeID.FIRST_OBJECTID IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = fCTempALayer,
                                   join_name = "tempTableFromNodeID")
       fCPointFromNode = "in_memory\\fCPointFromNode"
       arcpy.FeatureVerticesToPoints_management(in_features = fCTempALayer,
                                                out_feature_class = fCPointFromNode,
                                                point_location = "START")
       #
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       arcpy.AddJoin_management(in_layer_or_view = lineLayer,
                                in_field = "FROM_NODE",
                                join_table = tempTableFinalFromNodeToNode,
                                join_field = "FROM_NODE")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tempTableFinalFromNodeToNode.FROM_NODE IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = lineLayer,
                                   join_name = "tempTableFinalFromNodeToNode")
       fCTempB = "in_memory\\fCTempB"
       arcpy.CopyFeatures_management(in_features = lineLayer,
                                     out_feature_class = fCTempB)
       fCTempBLayer = "fCTempBLayer"
       arcpy.MakeFeatureLayer_management(in_features = fCTempB,
                                         out_layer = fCTempBLayer)
       tempTableFromNodeToNodeID = "in_memory\\tempTableFromNodeToNodeID"
       arcpy.Statistics_analysis(in_table = fCTempBLayer,
                                 out_table = tempTableFromNodeToNodeID,
                                 statistics_fields = [["OBJECTID", "FIRST"]],
                                 case_field = ["FROM_NODE"])
       arcpy.AddJoin_management(in_layer_or_view = fCTempBLayer,
                                in_field = "OBJECTID",
                                join_table = tempTableFromNodeToNodeID,
                                join_field = "FIRST_OBJECTID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempBLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tempTableFromNodeToNodeID.FIRST_OBJECTID IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = fCTempBLayer,
                                   join_name = "tempTableFromNodeToNodeID")
       fCPointFromNodeToNode = "in_memory\\fCPointFromNodeToNode"
       arcpy.FeatureVerticesToPoints_management(in_features = fCTempBLayer,
                                                out_feature_class = fCPointFromNodeToNode,
                                                point_location = "START")
       #
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "CLEAR_SELECTION")
       arcpy.AddJoin_management(in_layer_or_view = lineLayer,
                                in_field = "TO_NODE",
                                join_table = tempTableFinalToNode,
                                join_field = "TO_NODE")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = lineLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tempTableFinalToNode.TO_NODE IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = lineLayer,
                                   join_name = "tempTableFinalToNode")
       fCTempC = "in_memory\\fCTempC"
       arcpy.CopyFeatures_management(in_features = lineLayer,
                                     out_feature_class = fCTempC)
       fCTempCLayer = "fCTempCLayer"
       arcpy.MakeFeatureLayer_management(in_features = fCTempC,
                                         out_layer = fCTempCLayer)
       tempTableToNodeID = "in_memory\\tempTableToNodeID"
       arcpy.Statistics_analysis(in_table = fCTempCLayer,
                                 out_table = tempTableToNodeID,
                                 statistics_fields = [["OBJECTID", "FIRST"]],
                                 case_field = ["TO_NODE"])
       arcpy.AddJoin_management(in_layer_or_view = fCTempCLayer,
                                in_field = "OBJECTID",
                                join_table = tempTableToNodeID,
                                join_field = "FIRST_OBJECTID")
       arcpy.SelectLayerByAttribute_management(in_layer_or_view = fCTempCLayer,
                                               selection_type = "NEW_SELECTION",
                                               where_clause = "tempTableToNodeID.FIRST_OBJECTID IS NOT NULL")
       arcpy.RemoveJoin_management(in_layer_or_view = fCTempCLayer,
                                   join_name = "tempTableToNodeID")
       fCPointToNode = "in_memory\\fCPointToNode"
       arcpy.FeatureVerticesToPoints_management(in_features = fCTempCLayer,
                                                out_feature_class = fCPointToNode,
                                                point_location = "END")
       #
       fCNode = "in_memory\\fCNode"
       #fCNode = os.path.join(self.pathProcessGDB, "fCNode")
       arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                           out_name = "fCNode",
                                           geometry_type = "POINT",
                                           spatial_reference = arcpy.Describe(lineLayer).spatialReference)
       with arcpy.da.SearchCursor(fCPointFromNode, ["Shape@"]) as cursorA:
           with arcpy.da.InsertCursor(fCNode, ["Shape@"]) as cursorB:
               for rowA in cursorA:
                   cursorB.insertRow((rowA[0], ))
       with arcpy.da.SearchCursor(fCPointFromNodeToNode, ["Shape@"]) as cursorA:
           with arcpy.da.InsertCursor(fCNode, ["Shape@"]) as cursorB:
               for rowA in cursorA:
                   cursorB.insertRow((rowA[0], ))
       with arcpy.da.SearchCursor(fCPointToNode, ["Shape@"]) as cursorA:
           with arcpy.da.InsertCursor(fCNode, ["Shape@"]) as cursorB:
               for rowA in cursorA:
                   cursorB.insertRow((rowA[0], ))
       #
       return fCNode
       pass

   def CreateFeaturePoint(self, lineLayer, fCNodeA, fCNodeB, fCNodeC):
       #
       fCNodeD = "in_memory\\fCNodeD"
       arcpy.Erase_analysis(in_features = fCNodeB,
                            erase_features = fCNodeC,
                            out_feature_class = fCNodeD,
                            cluster_tolerance = "0 Meters")
       #
       fCNodeE = os.path.join(self.pathProcessGDB, "fCNodeE")
       arcpy.CreateFeatureclass_management(out_path = self.pathProcessGDB,
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