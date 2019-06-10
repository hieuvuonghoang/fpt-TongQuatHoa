import arcpy
import os

class Demo:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        self.fDBienGioiDiaGioi = "BienGioiDiaGioi"
        self.fCDuongBienGioi = "DuongBienGioi"
        self.fCDuongDiaGioi = "DuongDiaGioi"
        self.fCDiaPhan = "DiaPhan"
        # Path Process
        self.pathDuongBienGioiProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDuongBienGioi)
        self.pathDuongDiaGioiProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDuongDiaGioi)
        self.pathDiaPhanProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDiaPhan)
        # Path Final
        self.pathDuongBienGioiFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDuongBienGioi)
        self.pathDuongDiaGioiFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDuongDiaGioi)
        self.pathDiaPhanFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDiaPhan)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.fCDiaPhanFinalInMemory = "in_memory\\DiaPhanFinalInMemory"
        arcpy.CopyFeatures_management(in_features = self.pathDiaPhanFinal,
                                      out_feature_class = self.fCDiaPhanFinalInMemory)
        self.fCDiaPhanProcessInMemory = "in_memory\\DiaPhanProcessInMemory"
        arcpy.CopyFeatures_management(in_features = self.pathDiaPhanProcess,
                                      out_feature_class = self.fCDiaPhanProcessInMemory)
        self.fCDuongDiaGioiFinalInMemory = "in_memory\\DuongDiaGioiFinalInMemory"
        arcpy.CopyFeatures_management(in_features = self.pathDuongDiaGioiFinal,
                                      out_feature_class = self.fCDuongDiaGioiFinalInMemory)
        self.fCDuongDiaGioiProcessInMemory = "in_memory\\DuongDiaGioiProcessInMemory"
        arcpy.CopyFeatures_management(in_features = self.pathDuongDiaGioiProcess,
                                      out_feature_class = self.fCDuongDiaGioiProcessInMemory)
        # Create Feature Final
        diaPhanFinalLayer = "DiaPhanFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCDiaPhanFinalInMemory,
                                          out_layer = diaPhanFinalLayer)
        duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCDuongDiaGioiFinalInMemory,
                                          out_layer = duongDiaGioiFinalLayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 3")
        arcpy.CopyFeatures_management(in_features = diaPhanFinalLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DiaPhanXaFinal"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 2")
        arcpy.CopyFeatures_management(in_features = diaPhanFinalLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DiaPhanHuyenFinal"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 1")
        arcpy.CopyFeatures_management(in_features = diaPhanFinalLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DiaPhanTinhFinal"))
        
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 3")
        arcpy.CopyFeatures_management(in_features = duongDiaGioiFinalLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DuongDiaGioiXaFinal"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 2")
        arcpy.CopyFeatures_management(in_features = duongDiaGioiFinalLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DuongDiaGioiHuyenFinal"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 1")
        arcpy.CopyFeatures_management(in_features = duongDiaGioiFinalLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DuongDiaGioiTinhFinal"))
        # Create Feature Process
        diaPhanProcessLayer = "DiaPhanProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCDiaPhanProcessInMemory,
                                          out_layer = diaPhanProcessLayer)
        duongDiaGioiProcessLayer = "DuongDiaGioiProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCDuongDiaGioiProcessInMemory,
                                          out_layer = duongDiaGioiProcessLayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = diaPhanProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 3")
        arcpy.CopyFeatures_management(in_features = diaPhanProcessLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DiaPhanXaProcess"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = diaPhanProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 2")
        arcpy.CopyFeatures_management(in_features = diaPhanProcessLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DiaPhanHuyenProcess"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = diaPhanProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 1")
        arcpy.CopyFeatures_management(in_features = diaPhanProcessLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DiaPhanTinhProcess"))
        
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongDiaGioiProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 3")
        arcpy.CopyFeatures_management(in_features = duongDiaGioiProcessLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DuongDiaGioiXaProcess"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongDiaGioiProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 2")
        arcpy.CopyFeatures_management(in_features = duongDiaGioiProcessLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DuongDiaGioiHuyenProcess"))
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongDiaGioiProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "doiTuong = 1")
        arcpy.CopyFeatures_management(in_features = duongDiaGioiProcessLayer,
                                      out_feature_class = os.path.join(self.pathDefaultGDB, "DuongDiaGioiTinhProcess"))
        pass

if __name__ == "__main__":
    demo = Demo()
    demo.Execute()
    pass