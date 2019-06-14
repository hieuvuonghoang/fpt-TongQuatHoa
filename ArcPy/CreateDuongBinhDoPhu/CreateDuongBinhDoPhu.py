import os
import sys
import arcpy

class CreateDuongBinhDoPhu:

    def __init__(self, contourInterval, baseContour, zFactor):
        self.contourInterval = contourInterval
        self.baseContour = baseContour
        self.zFactor = zFactor
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.fDDiaHinh = "DiaHinh"
        self.fCDuongBinhDo = "DuongBinhDo"
        self.fCDuongBinhDoPhu = "DuongBinhDo_Phu"
        self.pathRaster = "C:\\Generalize_25_50\\Input.tif"
        self.pathDiaHinh = os.path.join(self.pathProcessGDB, self.fDDiaHinh)
        self.pathDuongBinhDoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDDiaHinh), self.fCDuongBinhDo)
        self.pathDuongBinhDoPhuProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDDiaHinh), self.fCDuongBinhDoPhu)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.RunContourTool()
        self.InitFeatureDuongBinhDoPhu()
        self.InsertDuongBinhDoPhu()
        self.DeleteTempFeatureClass()
        pass

    def RunContourTool(self):
        self.duongBinhDoPhuTemp = os.path.join(self.pathProcessGDB, "OutPutContuor")
        arcpy.sa.Contour(in_raster = self.pathRaster,
                         out_polyline_features = self.duongBinhDoPhuTemp,
                         contour_interval = self.contourInterval,
                         base_contour = self.baseContour,
                         z_factor = self.zFactor)
        pass

    def InitFeatureDuongBinhDoPhu(self):
        arcpy.CreateFeatureclass_management(out_path = self.pathDiaHinh,
                                            out_name = self.fCDuongBinhDoPhu,
                                            geometry_type = "POLYLINE",
                                            template = [self.pathDuongBinhDoProcess])
        pass

    def InsertDuongBinhDoPhu(self):
        duongBinhDoPhuTempLayer = "duongBinhDoPhuTempLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.duongBinhDoPhuTemp,
                                          out_layer = duongBinhDoPhuTempLayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = duongBinhDoPhuTempLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = "Contour > 0")
        with arcpy.da.SearchCursor(duongBinhDoPhuTempLayer, ["Shape@", "Contour"]) as sCur:
            with arcpy.da.InsertCursor(self.pathDuongBinhDoPhuProcess, ["Shape@", "doCaoH", "loaiKieuDuongBinhDo", "loaiDuongBinhDo", "doiTuong", "DuongBinhDo_Rep_ID"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], row[1], 2, 3, 1, 4))
        pass

    def DeleteTempFeatureClass(self):
        arcpy.Delete_management(in_data = self.duongBinhDoPhuTemp)
        pass

if __name__ == "__main__":
    print "Contour Interval = {0}\nBase Contour = {1}\nZFactor = {2}".format(sys.argv[1], sys.argv[2], sys.argv[3])
    createDuongBinhDoPhu = CreateDuongBinhDoPhu(sys.argv[1], sys.argv[2], sys.argv[3])
    print "Running..."
    createDuongBinhDoPhu.Execute()
    print "Success..."