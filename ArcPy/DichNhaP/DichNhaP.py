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
        self.distanceDoanTimDuongBoMeter = 20.0
        self.distanceDoanTimDuongBo = str(self.distanceDoanTimDuongBoMeter) + " Meters"
        self.radiusMoveNhaPMaxMeter = 21.0
        self.radiusMoveNhaPMax = str(self.radiusMoveNhaPMaxMeter) + " Meters"
        self.radiusNhaPMeter = 2.0
        self.radiusNhaP = str(self.radiusNhaPMeter) + " Meters"
        self.pathFCNhaP = os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), self.fCNhaP)
        self.pathDoanTimDuongBo = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)

    def Excute(self):
        self.CopyNhaPToMemory()
        self.CreateBufferDoanTimDuongBo()
        self.CreateFeatureNhaPCanDich()
        self.CreateBufferNhaPCanDich()
        self.CreatePolygonContainsA()

    def CopyNhaPToMemory(self):
        self.fCNhaPInMemory = "in_memory\\NhaPInMemory"
        arcpy.AddField_management(in_table = self.pathFCNhaP,
                                  field_name = "FID_NhaP",
                                  field_type = "LONG")
        arcpy.CalculateField_management(in_table = self.pathFCNhaP,
                                        field = "FID_NhaP",
                                        expression = "!OBJECTID!",
                                        expression_type = "PYTHON_9.3")
        arcpy.CopyFeatures_management(in_features = self.pathFCNhaP,
                                      out_feature_class = self.fCNhaPInMemory)
        arcpy.DeleteField_management(in_table = self.pathFCNhaP,
                                     drop_field = ["FID_NhaP"])

    def CreateBufferDoanTimDuongBo(self):
        # Create Buffer DoanTimDuongBo
        self.bufferDoanTimDuongBo = "in_memory\\BufferDoanTimDuongBo"
        arcpy.Buffer_analysis(in_features = self.pathDoanTimDuongBo,
                              out_feature_class = self.bufferDoanTimDuongBo,
                              buffer_distance_or_field = self.distanceDoanTimDuongBo)
        # Create Layer BufferDoanTimDuongBo
        self.bufferDoanTimDuongBoLayer = "BufferDoanTimDuongBoLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.bufferDoanTimDuongBo,
                                          out_layer = self.bufferDoanTimDuongBoLayer)

    def CreateFeatureNhaPCanDich(self):
        # Create Layer NhaP
        self.nhaPLayer = "NhaPLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCNhaPInMemory,
                                          out_layer = self.nhaPLayer)
        # Select NhaP nam trong bufferDoanTimDuongBo
        self.fCNhaPCanDich = "in_memory\\NhaPCanDich"
        #self.fCNhaPCanDich = os.path.join(self.pathDefaultGDB, "NhaPCanDich")
        arcpy.SelectLayerByLocation_management(in_layer = self.nhaPLayer,
                                               overlap_type = "WITHIN",
                                               select_features = self.bufferDoanTimDuongBoLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        arcpy.CopyFeatures_management(in_features = self.nhaPLayer,
                                      out_feature_class = self.fCNhaPCanDich)
        # Create Layer NhaPCanDich
        self.nhaPCanDichLayer = "NhaPCanDichLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCNhaPCanDich,
                                          out_layer = self.nhaPCanDichLayer)

    def CreateBufferNhaPCanDich(self):
        self.NearTableNhaPDoanTimDuongBo = "in_memory\\NearTableNhaPDoanTimDuongBo"
        #self.NearTableNhaPDoanTimDuongBo = os.path.join(self.pathDefaultGDB, "NearTableNhaPDoanTimDuongBo")
        arcpy.GenerateNearTable_analysis(in_features = self.fCNhaPCanDich,
                                         near_features = self.pathDoanTimDuongBo,
                                         out_table = self.NearTableNhaPDoanTimDuongBo,
                                         search_radius = self.distanceDoanTimDuongBo)
        codeBlock = """def CalculateFieldRadiusBuffer(distance):
            return str(""" + str(self.radiusMoveNhaPMaxMeter) + """ - distance) + \" Meters\""""
        arcpy.AddField_management(in_table = self.fCNhaPCanDich,
                                  field_name = "RadiusBuffer",
                                  field_type = "Text")
        arcpy.JoinField_management(in_data = self.fCNhaPCanDich,
                                   in_field = "OBJECTID",
                                   join_table = self.NearTableNhaPDoanTimDuongBo,
                                   join_field = "IN_FID")
        arcpy.CalculateField_management(in_table = self.fCNhaPCanDich,
                                        field = "RadiusBuffer",
                                        expression = "CalculateFieldRadiusBuffer(!NEAR_DIST!)",
                                        expression_type = "PYTHON_9.3",
                                        code_block = codeBlock)
        #self.bufferNhaPCanDich = "in_memory\\BufferNhaPCanDich"
        self.bufferNhaPCanDich = os.path.join(self.pathDefaultGDB, "BufferNhaPCanDich")
        arcpy.Buffer_analysis(in_features = self.fCNhaPCanDich,
                              out_feature_class = self.bufferNhaPCanDich,
                              buffer_distance_or_field = "RadiusBuffer")

    def CreatePolygonContainsA(self):
        self.PolygonContains = os.path.join(self.pathDefaultGDB, "PolygonContains")
        arcpy.Erase_analysis(in_features = self.bufferNhaPCanDich,
                             erase_features = self.bufferDoanTimDuongBo,
                             out_feature_class = self.PolygonContains)

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
        # Generate Near Table
        outNearTable = "in_memory\\OutNearTable"
        arcpy.GenerateNearTable_analysis(in_features = nhaPLayer,
                                         near_features = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo),
                                         out_table = outNearTable,
                                         search_radius = self.distanceDoanTimDuongBo)
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