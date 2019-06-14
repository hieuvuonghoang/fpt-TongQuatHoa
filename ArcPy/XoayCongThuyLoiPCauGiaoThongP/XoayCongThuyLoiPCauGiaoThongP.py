# -*- coding: utf-8 -*-
# Xoay Representation CongThuyLoiP, CauGiaoThongP theo DoanTimDuongBo

import arcpy
import os
import json
import io

class XoayCongThuyLoiPCauGiaoThongP:

    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fileConfigName = "ConfigToolXoayCongThuyLoiPCauGiaoThongP.json"
        self.pathFileConfig = os.path.join(self.dir_path, self.fileConfigName)
        if os.path.isfile(self.pathFileConfig) == False:
            print "Not Found: " + self.pathFileConfig + "?\nCreate FileConfig..."
            self.CreateFileConfig(self.pathFileConfig)
        self.ReadFileConfig(self.pathFileConfig)
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        self.fCCongThuyLoiP = "CongThuyLoiP"
        self.fCCauGiaoThongP = "CauGiaoThongP"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.pathCongThuyLoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        self.pathCauGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)

    def ReadFileConfig(self, pathFile):
        file = open(pathFile, "r")
        textConfig = file.read()
        file.close()
        self.configTool = json.loads(textConfig)

    def CreateFileConfig(self, pathFile):
        configTool = [
          {
            "doanTimDuongBoRepID": "1",
            "doanTimDuongBoRepName": "47-a-3-Tim đường cao tốc TL",
            "cauGiaoThongPRepID": "7",
            "cauGiaoThongPRepName": "60-1-a-2-Cầu trên đường cao tốc PTL"
          },
          {
            "doanTimDuongBoRepID": "2",
            "doanTimDuongBoRepName": "47-b-Đường cao tốc nửaTL",
            "cauGiaoThongPRepID": "7",
            "cauGiaoThongPRepName": "60-1-a-2-Cầu trên đường cao tốc PTL"
          },
          {
            "doanTimDuongBoRepID": "3",
            "doanTimDuongBoRepName": "48-2-Đường QL lát nhựa nửa TL",
            "cauGiaoThongPRepID": "8",
            "cauGiaoThongPRepName": "60-1-a-3-Cầu trên đg quốc lộ PTL"
          },
          {
            "doanTimDuongBoRepID": "4",
            "doanTimDuongBoRepName": "49-Tỉnh lộ lát nhựa nửa TL",
            "cauGiaoThongPRepID": "9",
            "cauGiaoThongPRepName": "60-1-a-4-Cầu trên đg tỉnh lộ PTL"
          },
          {
            "doanTimDuongBoRepID": "5",
            "doanTimDuongBoRepName": "50-b-Đường ô tô khác",
            "cauGiaoThongPRepID": "1",
            "cauGiaoThongPRepName": "60-1-b-Cầu trên đường sắt hoặc đg ô tô PTL"
          },
          {
            "doanTimDuongBoRepID": "6",
            "doanTimDuongBoRepName": "51-Đường ô tô đang làm nửa TL",
            "cauGiaoThongPRepID": "11",
            "cauGiaoThongPRepName": "N/A"
          },
          {
            "doanTimDuongBoRepID": "7",
            "doanTimDuongBoRepName": "52-Đường nhỏ",
            "cauGiaoThongPRepID": "5",
            "cauGiaoThongPRepName": "60-4-b-Cầu ô tô không qua được PTL"
          },
          {
            "doanTimDuongBoRepID": "8",
            "doanTimDuongBoRepName": "53-Đường mòn",
            "cauGiaoThongPRepID": "6",
            "cauGiaoThongPRepName": "58-2-b-Cầu chui không theo tỷ lệ"
          },
          {
            "doanTimDuongBoRepID": "9",
            "doanTimDuongBoRepName": "54-Đường chia lô",
            "cauGiaoThongPRepID": "6",
            "cauGiaoThongPRepName": "58-2-b-Cầu chui không theo tỷ lệ"
          },
          {
            "doanTimDuongBoRepID": "10",
            "doanTimDuongBoRepName": "55-a-Đường phố chính",
            "cauGiaoThongPRepID": "9",
            "cauGiaoThongPRepName": "60-1-a-4-Cầu trên đg tỉnh lộ PTL"
          },
          {
            "doanTimDuongBoRepID": "11",
            "doanTimDuongBoRepName": "55-b-Đường phố phụ, ngõ phố",
            "cauGiaoThongPRepID": "5",
            "cauGiaoThongPRepName": "60-4-b-Cầu ô tô không qua được PTL"
          },
          {
            "doanTimDuongBoRepID": "12",
            "doanTimDuongBoRepName": "65-2-b-Đường ô tô khác đắp cao",
            "cauGiaoThongPRepID": "5",
            "cauGiaoThongPRepName": "60-4-b-Cầu ô tô không qua được PTL"
          },
          {
            "doanTimDuongBoRepID": "13",
            "doanTimDuongBoRepName": "8-2-Đường QL lát nhựa nửa TL đắp cao 2 bên",
            "cauGiaoThongPRepID": "8",
            "cauGiaoThongPRepName": "60-1-a-3-Cầu trên đg quốc lộ PTL"
          },
          {
            "doanTimDuongBoRepID": "14",
            "doanTimDuongBoRepName": "49-Tỉnh lộ lát nhựa nửa TL đắp cao 2 bên",
            "cauGiaoThongPRepID": "9",
            "cauGiaoThongPRepName": "60-1-a-4-Cầu trên đg tỉnh lộ PTL"
          },
        ]
        textConfig = json.dumps(obj = configTool, indent = 1, sort_keys = True)
        file = open(pathFile, "w")
        file.write(textConfig)
        file.close()

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.referenceScale = "50000"
        self.UpdateCauGiaoThongPRuleIDByDoanTimDuongBoRuleID()
        self.XoayCongThuyLoiPCauGiaoThongP()

    def UpdateCauGiaoThongPRuleIDByDoanTimDuongBoRuleID(self):
        # Make Feature Layer
        cauGiaoThongPLayer = "CauGiaoThongPLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = cauGiaoThongPLayer)
        doanTimDuongBoLayer = "DoanTimDuongBoLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = doanTimDuongBoLayer)
        # Generate Near Table
        outTableTempA = "in_memory\\OutTabelTempA"
        arcpy.GenerateNearTable_analysis(in_features = cauGiaoThongPLayer,
                                         near_features = doanTimDuongBoLayer,
                                         out_table = outTableTempA,
                                         search_radius = "0 Meters",
                                         closest = "CLOSEST",
                                         method = "PLANAR")
        # Add Field DoanTimDuongBo
        arcpy.AddField_management(in_table = cauGiaoThongPLayer,
                                  field_name = "FID_DoanTimDuongBo",
                                  field_type = "LONG")
        arcpy.AddField_management(in_table = cauGiaoThongPLayer,
                                  field_name = "RepIDTemp",
                                  field_type = "SHORT")
        # Table Select
        outTableTempB = "in_memory\\OutTabelTempB"
        arcpy.TableSelect_analysis(in_table = doanTimDuongBoLayer,
                                   out_table = outTableTempB)
        fields = arcpy.ListFields(outTableTempB)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.name != "DoanTimDuongBo_Rep_ID" and fieldTemp.type != "OID":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = outTableTempB,
                                     drop_field = fieldsDelete)
        # Join
        arcpy.AddJoin_management(in_layer_or_view = cauGiaoThongPLayer,
                                 in_field = "OBJECTID",
                                 join_table = outTableTempA,
                                 join_field = "IN_FID")
        arcpy.CalculateField_management(in_table = cauGiaoThongPLayer,
                                        field = "FID_DoanTimDuongBo",
                                        expression = "!NEAR_FID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = cauGiaoThongPLayer,
                                    join_name = outTableTempA.split("\\")[1])
        arcpy.AddJoin_management(in_layer_or_view = cauGiaoThongPLayer,
                                 in_field = "FID_DoanTimDuongBo",
                                 join_table = outTableTempB,
                                 join_field = "OBJECTID")
        arcpy.CalculateField_management(in_table = cauGiaoThongPLayer,
                                        field = "RepIDTemp",
                                        expression = "!DoanTimDuongBo_Rep_ID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.RemoveJoin_management(in_layer_or_view = cauGiaoThongPLayer,
                                    join_name = outTableTempB.split("\\")[1])
        # Update RuleID
        with arcpy.da.UpdateCursor(cauGiaoThongPLayer, ["CauGiaoThongP_Rep_ID", "RepIDTemp"]) as cursor:
            for row in cursor:
                for elem in self.configTool:
                    if row[1] == int(elem["doanTimDuongBoRepID"]):
                        row[0] = int(elem["cauGiaoThongPRepID"])
                        cursor.updateRow(row)
                        break
        arcpy.DeleteField_management(in_table = cauGiaoThongPLayer,
                                     drop_field = ["FID_DoanTimDuongBo", "RepIDTemp"])

    def XoayCongThuyLoiPCauGiaoThongP(self):
        congThuyLoiPLayer = "CongThuyLoiPLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiPFinal,
                                            out_layer = congThuyLoiPLayer)
        cauGiaoThongPLayer = "CauGiaoThongPLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                            out_layer = cauGiaoThongPLayer)
        doanTimDuongBoLayer = "DoanTimDuongBoLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                            out_layer = doanTimDuongBoLayer)
        arcpy.SetLayerRepresentation_cartography(in_layer = congThuyLoiPLayer,
                                                 representation = "CongThuyLoiP_Rep")
        arcpy.SetLayerRepresentation_cartography(in_layer = cauGiaoThongPLayer,
                                                 representation = "CauGiaoThongP_Rep")
        arcpy.SetLayerRepresentation_cartography(in_layer = doanTimDuongBoLayer,
                                                 representation = "DoanTimDuongBo_Rep")
        #PERPENDICULAR: aligns representation markers perpendicularly to the stroke or fill edge. This is the default.
        #PARALLEL: aligns representation markers parallel to the stroke or fill edge.
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = congThuyLoiPLayer,
                                                    in_line_or_polygon_features = doanTimDuongBoLayer,
                                                    search_distance = "50 Meters",
                                                    marker_orientation = "PERPENDICULAR")
        arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = cauGiaoThongPLayer,
                                                    in_line_or_polygon_features = doanTimDuongBoLayer,
                                                    search_distance = "50 Meters",
                                                    marker_orientation = "PERPENDICULAR")
        pass

if __name__ == '__main__':
    xoayCongThuyLoiPCauGiaoThongP = XoayCongThuyLoiPCauGiaoThongP()
    xoayCongThuyLoiPCauGiaoThongP.Execute()
