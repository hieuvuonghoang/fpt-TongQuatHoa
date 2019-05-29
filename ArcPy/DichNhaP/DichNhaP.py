import sys
import os
import arcpy

class DichNhaP:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        self.fDDanCuCoSoHaTang = "DanCuCoSoHaTang"
        self.fDGiaoThong = "GiaoThong"
        self.fCNhaP = "NhaP"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.distanceDoanTimDuongBo = "30 Meters"
        self.radiusMoveNhaP = "35 Meters"
        self.radiusNhaP = "2 Meters"

    def Excute(self):
        self.CreatePolygonContains()

    def CreatePolygonContains(self):
        # Create Buffer DoanTimDuongBo
        bufferDoanTimDuongBo = "in_memory\\BufferDoanTimDuongBo"
        arcpy.Buffer_analysis(in_features = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo),
                              out_feature_class = bufferDoanTimDuongBo,
                              buffer_distance_or_field = self.distanceDoanTimDuongBo)
        # MakeFeatureLayer outLayerBufferFCDoanTimDuongBo
        bufferDoanTimDuongBoLayer = "BufferDoanTimDuongBoLayer"
        arcpy.MakeFeatureLayer_management(in_features = bufferDoanTimDuongBo,
                                          out_layer = bufferDoanTimDuongBoLayer)
        # MakeFeatureLayer NhaP
        nhaPLayer = "NhaPLayer"
        arcpy.MakeFeatureLayer_management(in_features = os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), self.fCNhaP),
                                          out_layer = nhaPLayer)
        # Chon NhaP can dich chuyen (NhaP nam trong bufferDoanTimDuongBo)
        arcpy.SelectLayerByLocation_management(in_layer = nhaPLayer,
                                               overlap_type = "WITHIN",
                                               select_features = bufferDoanTimDuongBoLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Buffer NhaP can dich chuyen
        nhaPCanDichChuyenBuffer = "in_memory\\NhaPCanDichChuyenBuffer"
        arcpy.Buffer_analysis(in_features = nhaPLayer,
                              out_feature_class = nhaPCanDichChuyenBuffer,
                              buffer_distance_or_field = self.radiusMoveNhaP)
        # Create Polygon de dich chuyen NhaP vao ben trong Polygon
        polygonContains = "in_memory\\PolygonContains"
        #polygonContains = os.path.join(self.pathDefaultGDB, "PolygonContains")
        arcpy.Erase_analysis(in_features = nhaPCanDichChuyenBuffer,
                             erase_features = bufferDoanTimDuongBoLayer,
                             out_feature_class = polygonContains)
        # Add Filed FID_NhaP
        arcpy.AddField_management(in_table = polygonContains,
                                  field_type = "Long",
                                  field_name = "FID_NhaP")
        arcpy.CalculateField_management(in_table = polygonContains,
                                        field = "FID_NhaP",
                                        expression = "!ORIG_FID!",
                                        expression_type = "PYTHON_9.3")
        # Doi voi moi NhaP co the co nhieu polygonContains ("ORIG_FID"), can chon polygonContains co Shape_Area lon nhat trong cac polygonContains
        ## Convert polygonContains Multipart to Singlepart
        polygonContainsSinglepart = "in_memory\\PolygonContainsSinglepart"
        #polygonContainsSinglepart = os.path.join(self.pathDefaultGDB, "PolygonContainsSinglepart")
        arcpy.MultipartToSinglepart_management(in_features = polygonContains,
                                               out_feature_class = polygonContainsSinglepart)
        # AddField Shape_Area
        arcpy.AddField_management(in_table = polygonContainsSinglepart,
                                  field_type = "Double",
                                  field_name = "Shape_Area")
        arcpy.CalculateField_management(in_table = polygonContainsSinglepart,
                                        field = "Shape_Area",
                                        expression = "!shape.geodesicArea@SQUAREMETERS!",
                                        expression_type = "PYTHON_9.3")
        ## Tu nhung Feature polygonContains co chung FID_NhaP chon Feature Shape_Area lon nhat
        polygonContainsSinglepartStatistics = "in_memory\\PolygonContainsSinglepartStatistics"
        #polygonContainsSinglepartStatistics = os.path.join(self.pathDefaultGDB, "PolygonContainsSinglepartStatistics")
        arcpy.Statistics_analysis(in_table = polygonContainsSinglepart,
                                  out_table = polygonContainsSinglepartStatistics,
                                  statistics_fields = [["Shape_Area", "MAX"]],
                                  case_field = ["FID_NhaP"])
        outTableSelect = "in_memory\\outTableSelect"
        arcpy.TableSelect_analysis(in_table = polygonContainsSinglepartStatistics,
                                   out_table = outTableSelect,
                                   where_clause = "FREQUENCY > 1")
        arcpy.MakeFeatureLayer_management(in_features = polygonContainsSinglepart,
                                          out_layer = "PolygonContainsSinglepartLayer")
        arcpy.AddJoin_management(in_layer_or_view = "PolygonContainsSinglepartLayer",
                                 in_field = "FID_NhaP",
                                 join_table = outTableSelect,
                                 join_field = "FID_NhaP")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = "PolygonContainsSinglepartLayer",
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "(MAX_Shape_Area IS NOT NULL) AND (Shape_Area <> MAX_Shape_Area)")
        arcpy.RemoveJoin_management("PolygonContainsSinglepartLayer")
        sqlQueryErasePolygon = ""
        with arcpy.da.SearchCursor("PolygonContainsSinglepartLayer", ["OID@"]) as cursor:
            for row in cursor:
                sqlQueryErasePolygon += "OBJECTID <> " + str(row[0]) + " AND "
        sqlQueryErasePolygon = sqlQueryErasePolygon[slice(len(sqlQueryErasePolygon) - 5)]
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = "PolygonContainsSinglepartLayer",
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQueryErasePolygon)
        arcpy.CopyFeatures_management(in_features = "PolygonContainsSinglepartLayer",
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "ResultPolygonContains"))
        #outPolygonTempALayer = "OutPolygonTempALayer"
        #arcpy.MakeFeatureLayer_management(in_features = outPolygonTempA,
        #                                  out_layer = outPolygonTempALayer)
        ## Chon NhaP nam trong OutPolygonTempALayer
        #arcpy.SelectLayerByLocation_management(in_layer = nhaPLayer,
        #                                       overlap_type = "WITHIN",
        #                                       select_features = outPolygonTempALayer,
        #                                       search_distance = "0 Meters",
        #                                       selection_type = "NEW_SELECTION")
        #outBufferNhaPSelect = "in_memory\\OutBufferNhaPSelect"
        #arcpy.Buffer_analysis(in_features = nhaPLayer,
        #                      out_feature_class = outBufferNhaPSelect,
        #                      buffer_distance_or_field = self.radiusNhaP)
        #arcpy.Erase_analysis(in_features = outPolygonTempA,
        #                     erase_features = outBufferNhaPSelect,
        #                     out_feature_class = os.path.join(self.pathDefaultGDB, "resultPolygonContains"))

if __name__ == '__main__':
    print "DichNhaP Tools"
    arcpy.env.overwriteOutput = True
    dichNhaP = DichNhaP()
    dichNhaP.Excute()