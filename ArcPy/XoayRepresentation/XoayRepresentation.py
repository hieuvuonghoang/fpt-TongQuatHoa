# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime

class XoayRepresentation:

    def __init__(self, distance):
        self.distance = distance
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        # Feature DataSet Name
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        # GiaoThong Point
        self.fCCongGiaoThongP = "CongGiaoThongP"
        self.fCCauGiaoThongP = "CauGiaoThongP"
        self.fCDoanVuotSongSuoiP = "DoanVuotSongSuoiP"
        # GiaoThong Line
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        # ThuyHe Point
        self.fCCongThuyLoiP = "CongThuyLoiP"
        # Path Feature Class
        ## Path Process
        ### GiaoThong Point
        self.pathCauGiaoThongPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathCongGiaoThongPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathDoanVuotSongSuoiPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanVuotSongSuoiP)
        ### GiaoThong Line
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        ### ThuyHe Point
        self.pathCongThuyLoiPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        ### GiaoThong Point
        self.pathCauGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathCongGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathDoanVuotSongSuoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanVuotSongSuoiP)
        ### ThuyHe Point
        self.pathCongThuyLoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        # Representation Name
        self.repCongThuyLoiP = "CongThuyLoiP_Rep"
        self.repCauGiaoThongP = "CauGiaoThongP_Rep"
        self.repDoanTimDuongBo = "DoanTimDuongBo_Rep"
        self.repCongGiaoThongPRight = "CongGiaoThongP_RepPhai"
        self.repCongGiaoThongPLeft = "CongGiaoThongP_RepTrai"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Set Scale: 50K
        arcpy.env.referenceScale = "50000"
        # AlignMarkerToStrokeOrFill Tools
        self.AlignMarkerToStrokeOrFill()
        # UpdateRuleIDCauGiaoThong
        self.UpdateRuleIDCauGiaoThong()
        pass

    def AlignMarkerToStrokeOrFill(self):
        # Make Feature Layer
        self.congThuyLoiPFinalLayer = "congThuyLoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiPFinal,
                                            out_layer = self.congThuyLoiPFinalLayer)
        self.cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                            out_layer = self.cauGiaoThongPFinalLayer)
        self.congGiaoThongPFinalLayer = "congGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongPFinal,
                                            out_layer = self.congGiaoThongPFinalLayer)
        self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                            out_layer = self.doanTimDuongBoFinalLayer)
        # Set Layer Representation And AlignMarkerToStrokeOrFill
        ## Set Layer Representation DoanTimDuongBo
        arcpy.SetLayerRepresentation_cartography(in_layer = self.doanTimDuongBoFinalLayer,
                                                 representation = self.repDoanTimDuongBo)
        ## Set Layer Representation After Using AlignMarkerToStrokeOrFill
        ###
        arcpy.SetLayerRepresentation_cartography(in_layer = self.congThuyLoiPFinalLayer,
                                                 representation = self.repCongThuyLoiP)
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = self.congThuyLoiPFinalLayer,
                                                    in_line_or_polygon_features = self.doanTimDuongBoFinalLayer,
                                                    search_distance = self.distance,
                                                    marker_orientation = "PERPENDICULAR")
        ###
        arcpy.SetLayerRepresentation_cartography(in_layer = self.cauGiaoThongPFinalLayer,
                                                 representation = self.repCauGiaoThongP)
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = self.cauGiaoThongPFinalLayer,
                                                    in_line_or_polygon_features = self.doanTimDuongBoFinalLayer,
                                                    search_distance = self.distance,
                                                    marker_orientation = "PERPENDICULAR")
        ###
        arcpy.SetLayerRepresentation_cartography(in_layer = self.congGiaoThongPFinalLayer,
                                                 representation = self.repCongGiaoThongPRight)
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = self.congGiaoThongPFinalLayer,
                                                    in_line_or_polygon_features = self.doanTimDuongBoFinalLayer,
                                                    search_distance = self.distance,
                                                    marker_orientation = "PARALLEL")
        ###
        arcpy.SetLayerRepresentation_cartography(in_layer = self.congGiaoThongPFinalLayer,
                                                 representation = self.repCongGiaoThongPLeft)
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = self.congGiaoThongPFinalLayer,
                                                    in_line_or_polygon_features = self.doanTimDuongBoFinalLayer,
                                                    search_distance = self.distance,
                                                    marker_orientation = "PARALLEL")
        pass

    def UpdateRuleIDCauGiaoThong(self):
        # Generate Near Table
        outTableTempA = "in_memory\\OutTabelTempA"
        arcpy.GenerateNearTable_analysis(in_features = self.cauGiaoThongPFinalLayer,
                                         near_features = self.doanTimDuongBoFinalLayer,
                                         out_table = outTableTempA,
                                         search_radius = "0 Meters",
                                         closest = "CLOSEST",
                                         method = "PLANAR")
        # Add Field DoanTimDuongBo
        arcpy.AddField_management(in_table = self.cauGiaoThongPFinalLayer,
                                  field_name = "FID_DoanTimDuongBo",
                                  field_type = "LONG")
        arcpy.AddField_management(in_table = self.cauGiaoThongPFinalLayer,
                                  field_name = "RepIDTemp",
                                  field_type = "SHORT")
        # Table Select
        outTableTempB = "in_memory\\OutTabelTempB"
        arcpy.TableSelect_analysis(in_table = self.doanTimDuongBoFinalLayer,
                                   out_table = outTableTempB)
        fields = arcpy.ListFields(outTableTempB)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.name != "DoanTimDuongBo_Rep_ID" and fieldTemp.type != "OID":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = outTableTempB,
                                     drop_field = fieldsDelete)
        # Join
        arcpy.AddJoin_management(in_layer_or_view = self.cauGiaoThongPFinalLayer,
                                 in_field = "OBJECTID",
                                 join_table = outTableTempA,
                                 join_field = "IN_FID")
        arcpy.CalculateField_management(in_table = self.cauGiaoThongPFinalLayer,
                                        field = "FID_DoanTimDuongBo",
                                        expression = "!NEAR_FID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = self.cauGiaoThongPFinalLayer,
                                    join_name = outTableTempA.split("\\")[1])
        arcpy.AddJoin_management(in_layer_or_view = self.cauGiaoThongPFinalLayer,
                                 in_field = "FID_DoanTimDuongBo",
                                 join_table = outTableTempB,
                                 join_field = "OBJECTID")
        arcpy.CalculateField_management(in_table = self.cauGiaoThongPFinalLayer,
                                        field = "RepIDTemp",
                                        expression = "!DoanTimDuongBo_Rep_ID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = self.cauGiaoThongPFinalLayer,
                                    join_name = outTableTempB.split("\\")[1])
        # Update RuleID Using File Config:

        # Delete Filed
        arcpy.DeleteField_management(in_table = self.cauGiaoThongPFinalLayer,
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

if __name__ == "__main__":
    runTime = RunTime()
    print "Distance: {}".format(sys.argv[1])
    xoayRepresentation = XoayRepresentation(sys.argv[1])
    print "Running..."
    xoayRepresentation.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass