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
        self.distanceDoanTimDuongBoMeter = 10.0
        self.distanceDoanTimDuongBo = str(self.distanceDoanTimDuongBoMeter) + " Meters"
        self.radiusMoveNhaPMaxMeter = 50.0
        self.radiusMoveNhaPMax = str(self.radiusMoveNhaPMaxMeter) + " Meters"
        self.radiusNhaPMeter = 50.0
        self.radiusNhaP = str(self.radiusNhaPMeter) + " Meters"
        self.pathFCNhaP = os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), self.fCNhaP)
        self.pathDoanTimDuongBo = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)

    def Excute(self):
        self.CopyNhaPToMemory()
        self.CreateBufferDoanTimDuongBo()
        self.CreateFeatureNhaPCanDich()
        self.CreateBufferNhaPCanDich()
        self.CreatePolygonContains()
        self.CreatePointRandomInPolygonContains()
        self.UpdateShapeNhaPCanDichInFinal()

    def CopyNhaPToMemory(self):
        print "CopyNhaPToMemory"
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
        # Delete Fields self.fCNhaPInMemory
        fields = arcpy.ListFields(self.fCNhaPInMemory)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.name != "FID_NhaP" and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = self.fCNhaPInMemory,
                                     drop_field = fieldsDelete)
        # Delete Fields "FID_NhaP" in self.pathFCNhaP
        arcpy.DeleteField_management(in_table = self.pathFCNhaP,
                                     drop_field = ["FID_NhaP"])
        # Copy self.fCNhaPInMemory To DefaultGDB
        arcpy.CopyFeatures_management(in_features = self.fCNhaPInMemory,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "NhaP"))

    def CreateBufferDoanTimDuongBo(self):
        print "CreateBufferDoanTimDuongBo"
        # Create Buffer DoanTimDuongBo
        self.bufferDoanTimDuongBo = "in_memory\\BufferDoanTimDuongBo"
        arcpy.Buffer_analysis(in_features = self.pathDoanTimDuongBo,
                              out_feature_class = self.bufferDoanTimDuongBo,
                              buffer_distance_or_field = self.distanceDoanTimDuongBo)
        # Delete Fields self.bufferDoanTimDuongBo
        fields = arcpy.ListFields(self.bufferDoanTimDuongBo)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = self.bufferDoanTimDuongBo,
                                     drop_field = fieldsDelete)
        # Add Field Dissolve
        arcpy.AddField_management(in_table = self.bufferDoanTimDuongBo,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        # Dissolve
        #self.bufferDoanTimDuongBoDissolve = "in_memory\\BufferDoanTimDuongBoDissolve"
        self.bufferDoanTimDuongBoDissolve = os.path.join(self.pathDefaultGDB, "BufferDoanTimDuongBoDissolve")
        arcpy.Dissolve_management(in_features = self.bufferDoanTimDuongBo,
                                  out_feature_class = self.bufferDoanTimDuongBoDissolve,
                                  dissolve_field = "Dissolve")
        # Create Layer BufferDoanTimDuongBoDissolve
        self.bufferDoanTimDuongBoDissolveLayer = "BufferDoanTimDuongBoDissolveLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.bufferDoanTimDuongBoDissolve,
                                          out_layer = self.bufferDoanTimDuongBoDissolveLayer)
        # Create Layer BufferDoanTimDuongBo
        self.bufferDoanTimDuongBoLayer = "BufferDoanTimDuongBoLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.bufferDoanTimDuongBo,
                                          out_layer = self.bufferDoanTimDuongBoLayer)
        # Copy self.bufferDoanTimDuongBoLayer To DefaultGDB
        #arcpy.CopyFeatures_management(in_features = self.bufferDoanTimDuongBoLayer,
        #                              out_feature_class = os.path.join(self.pathDefaultGDB, "BufferDoanTimDuongBoLayer"))

    def CreateFeatureNhaPCanDich(self):
        print "CreateFeatureNhaPCanDich"
        # Create Layer NhaP
        self.nhaPLayer = "NhaPLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCNhaPInMemory,
                                          out_layer = self.nhaPLayer)
        # Select NhaP nam trong bufferDoanTimDuongBoDissolve
        #self.fCNhaPCanDich = "in_memory\\NhaPCanDich"
        self.fCNhaPCanDich = os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), "NhaPCanDich")
        arcpy.SelectLayerByLocation_management(in_layer = self.nhaPLayer,
                                               overlap_type = "WITHIN",
                                               select_features = self.bufferDoanTimDuongBo,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        arcpy.CopyFeatures_management(in_features = self.nhaPLayer,
                                      out_feature_class = self.fCNhaPCanDich)
        # Create Layer NhaPCanDich
        self.nhaPCanDichLayer = "NhaPCanDichLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCNhaPCanDich,
                                          out_layer = self.nhaPCanDichLayer)

    def CreateBufferNhaPCanDich(self):
        print "CreateBufferNhaPCanDich"
        self.bufferNhaPCanDich = "in_memory\\BufferNhaPCanDich"
        arcpy.Buffer_analysis(in_features = self.fCNhaPCanDich,
                              out_feature_class = self.bufferNhaPCanDich,
                              buffer_distance_or_field = self.radiusNhaP)
        self.bufferNhaPCanDichLayer = "BufferNhaPCanDichLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.bufferNhaPCanDich,
                                          out_layer = self.bufferNhaPCanDichLayer)
        #arcpy.Delete_management(self.fCNhaPCanDich)
        pass

    def CreatePolygonContains(self):
        print "CreatePolygonContains"
        polygonTempA = os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), "PolygonTempA")
        arcpy.Erase_analysis(in_features = self.bufferNhaPCanDichLayer,
                             erase_features = self.bufferDoanTimDuongBoDissolveLayer,
                             out_feature_class = polygonTempA)
        # Delete Fields
        fields = arcpy.ListFields(polygonTempA)
        fieldsDelete = []
        for fieldTemp in fields:
            if fieldTemp.name != "FID_NhaP" and fieldTemp.name != "Shape_Area" and fieldTemp.name != "Shape_Length" and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                fieldsDelete.append(fieldTemp.name)
        arcpy.DeleteField_management(in_table = polygonTempA,
                                     drop_field = fieldsDelete)
        polygonTempALayer = "PolygonTempALayer"
        arcpy.MakeFeatureLayer_management(in_features = polygonTempA,
                                          out_layer = polygonTempALayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = polygonTempALayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "Shape_Area <> 0")
        polygonTempB = os.path.join(os.path.join(self.pathProcessGDB, self.fDDanCuCoSoHaTang), "PolygonTempB")
        arcpy.MultipartToSinglepart_management(in_features = polygonTempALayer,
                                               out_feature_class = polygonTempB)
        polygonTempBLayer = "PolygonTempBLayer"
        arcpy.MakeFeatureLayer_management(in_features = polygonTempB,
                                          out_layer = polygonTempBLayer)
        tableTempA = "in_memory\\TableTempA"
        arcpy.Statistics_analysis(in_table = polygonTempB,
                                  out_table = tableTempA,
                                  statistics_fields = [["Shape_Area", "MAX"]],
                                  case_field = ["FID_NhaP"])
        tableTempB = "in_memory\\TableTempB"
        arcpy.TableSelect_analysis(in_table = tableTempA,
                                   out_table = tableTempB,
                                   where_clause = "FREQUENCY > 1")
        arcpy.AddJoin_management(in_layer_or_view = polygonTempBLayer,
                                 in_field = "FID_NhaP",
                                 join_table = tableTempB,
                                 join_field = "FID_NhaP")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = polygonTempBLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "(MAX_Shape_Area IS NULL) OR (MAX_Shape_Area IS NOT NULL AND Shape_Area = MAX_Shape_Area)")
        arcpy.RemoveJoin_management(in_layer_or_view = polygonTempBLayer,
                                    join_name = tableTempB.split("\\")[1])
        arcpy.SelectLayerByLocation_management(in_layer = self.nhaPLayer,
                                               overlap_type = "WITHIN",
                                               select_features = self.bufferDoanTimDuongBoLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        polygonTempC = "in_memory\\PolygonTempC"
        arcpy.Buffer_analysis(in_features = self.nhaPLayer,
                              out_feature_class = polygonTempC,
                              buffer_distance_or_field = self.radiusNhaP)
        self.resultPolygonContains = os.path.join(self.pathDefaultGDB, "ResultPolygonContains")
        arcpy.Erase_analysis(in_features = polygonTempBLayer,
                             erase_features = polygonTempC,
                             out_feature_class = self.resultPolygonContains)
        #arcpy.Delete_management(polygonTempB)
        #arcpy.Delete_management(polygonTempA)
        pass

    def CreatePointRandomInPolygonContains(self):
        print "CreatePointRandomInPolygonContains"
        self.pointRandom = os.path.join(self.pathDefaultGDB, "PointRandom")
        arcpy.CreateRandomPoints_management(out_path = self.pathDefaultGDB,
                                            out_name = "PointRandom",
                                            constraining_feature_class = self.resultPolygonContains,
                                            number_of_points_or_field = "1",
                                            minimum_allowed_distance = "0 Meters")
        tableATemp = "in_memory\\TableATemp"
        arcpy.TableSelect_analysis(in_table = self.resultPolygonContains,
                                   out_table = tableATemp)
        arcpy.JoinField_management(in_data = self.pointRandom,
                                   in_field = "CID",
                                   join_table = tableATemp,
                                   join_field = "OBJECTID",
                                   fields = ["FID_NhaP"])
        self.pointRandomJoin = os.path.join(self.pathDefaultGDB, "PointRandomJoin")
        arcpy.CopyFeatures_management(in_features = self.pointRandom,
                                      out_feature_class = self.pointRandomJoin)
    
    def UpdateShapeNhaPCanDichInFinal(self):
        print "UpdateShapeNhaPCanDichInFinal"
        self.nhaPProcessLayer = "NhaPProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = os.path.join(os.path.join(self.pathFinalGDB, self.fDDanCuCoSoHaTang), self.fCNhaP),
                                          out_layer = self.nhaPProcessLayer)
        tableATemp = "in_memory\\TableATemp"
        arcpy.TableSelect_analysis(in_table = self.pointRandomJoin,
                                   out_table = tableATemp)
        arcpy.AddJoin_management(in_layer_or_view = self.nhaPProcessLayer,
                                 in_field = "OBJECTID",
                                 join_table = tableATemp,
                                 join_field = "FID_NhaP")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.nhaPProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "FID_NhaP IS NOT NULL")
        arcpy.RemoveJoin_management(in_layer_or_view = self.nhaPProcessLayer,
                                    join_name = tableATemp.split("\\")[1])
        with arcpy.da.UpdateCursor(self.nhaPProcessLayer, ["OID@", "Shape@"]) as cursor:
            for row in cursor:
                #print "\tOID: " + str(row[0])
                found = False;
                with arcpy.da.UpdateCursor(self.pointRandomJoin, ["FID_NhaP", "Shape@"]) as cursorSub:
                    for rowSub in cursorSub:
                        if row[0] == rowSub[0]:
                            found = True;
                            row[1] = rowSub[1]
                            cursor.updateRow(row)
                            cursorSub.deleteRow()
                            break
                if found == False:
                    cursor.deleteRow()
        arcpy.SelectLayerByLocation_management(in_layer = self.nhaPProcessLayer,
                                               overlap_type = "WITHIN",
                                               select_features = self.bufferDoanTimDuongBoLayer,
                                               search_distance = self.distanceDoanTimDuongBo,
                                               selection_type = "NEW_SELECTION")
        with arcpy.da.UpdateCursor(self.nhaPProcessLayer) as cursor:
            for row in cursor:
                cursor.deleteRow()

        

if __name__ == '__main__':
    print "DichNhaP Tools"
    arcpy.env.overwriteOutput = True
    dichNhaP = DichNhaP()
    dichNhaP.Excute()
    print "Success!!!"