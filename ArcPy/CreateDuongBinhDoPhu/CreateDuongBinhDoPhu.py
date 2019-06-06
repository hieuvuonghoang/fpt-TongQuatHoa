import arcpy
import os

class CreateDuongBinhDoPhu:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.fDDiaHinh = "DiaHinh"
        self.fCDuongBinhDo = "DuongBinhDo"
        self.fCDuongBinhDoPhu = "DuongBinhDo_Phu"
        self.pathRaster = "C:\\Generalize_25_50\\Input.tif"
        self.pathDiaHinh = os.path.join(self.pathProcessGDB, self.fDDiaHinh)
        self.pathDuongBinhDoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDDiaHinh), self.fCDuongBinhDo)
        self.pathDuongBinhDoPhuProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDDiaHinh), self.fCDuongBinhDoPhu)
        pass

    def Excute(self):
        arcpy.env.overwriteOutput = True
        self.RunContourTool()
        self.InitFeatureDuongBinhDoPhu()
        self.InsertDuongBinhDoPhu()
        pass

    def RunContourTool(self):
        print "\tRunContourTool"
        self.duongBinhDoPhuTemp = "in_memory\\DuongBinhDoPhuTemp"
        arcpy.sa.Contour(in_raster = self.pathRaster,
                         out_polyline_features = self.duongBinhDoPhuTemp,
                         contour_interval = "5",
                         base_contour = "2.5",
                         z_factor = "1")
        pass

    def InitFeatureDuongBinhDoPhu(self):
        print "\tInitFeatureDuongBinhDoPhu"
        arcpy.CreateFeatureclass_management(out_path = self.pathDiaHinh,
                                            out_name = self.fCDuongBinhDoPhu,
                                            geometry_type = "POLYLINE",
                                            template = [self.pathDuongBinhDoProcess])
        pass

    def InsertDuongBinhDoPhu(self):
        print "\tInsertDuongBinhDoPhu"
        with arcpy.da.SearchCursor(self.duongBinhDoPhuTemp, ["Shape@", "Contour"]) as sCur:
            with arcpy.da.InsertCursor(self.pathDuongBinhDoPhuProcess, ["Shape@", "doCaoH", "loaiKieuDuongBinhDo", "loaiDuongBinhDo", "doiTuong"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], row[1], 2, 3, 1))
        pass

if __name__ == "__main__":
    print "CreateDuongBinhDoPhu:"
    createDuongBinhDoPhu = CreateDuongBinhDoPhu()
    createDuongBinhDoPhu.Excute()
    print "Success!!!"