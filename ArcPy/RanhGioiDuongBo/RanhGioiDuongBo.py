# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import hashlib
import datetime

class RanhGioiDuongBo:
    
    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDGiaoThong = "GiaoThong"
        self.fCMatDuongBo = "MatDuongBo"
        self.fCRanhGioiDuongBo = "RanhGioiDuongBo"
        self.fCCauGiaoThongA = "CauGiaoThongA"
        self.fCHamGiaoThongA = "HamGiaoThongA"
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = "C:\\Generalize_25_50\\50K_Final.gdb"
        pathRanhGioiDuongBoFianl = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCRanhGioiDuongBo)
        # Merge
        outPutMerge = "in_memory\\outPutMerge"
        pathMatDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCMatDuongBo)
        pathCauGiaoThongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongA)
        pathHamGiaoThongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCHamGiaoThongA)
        arcpy.Merge_management(inputs = [pathMatDuongBoFinal, pathCauGiaoThongAFinal, pathHamGiaoThongAFinal],
                               output = outPutMerge)
        if int(arcpy.GetCount_management(outPutMerge).getOutput(0)) == 0:
            return
        # Dissolve
        outPutMatDuongBoDissolve = "in_memory\\outPutMatDuongBoDissolve"
        arcpy.Dissolve_management(in_features = outPutMerge,
                                  out_feature_class = outPutMatDuongBoDissolve,
                                  multi_part = "SINGLE_PART")
        # Polygon To Line
        outPolygonToLine = "in_memory\\outPolygonToLine"
        arcpy.PolygonToLine_management(in_features = outPutMatDuongBoDissolve,
                                       out_feature_class = outPolygonToLine)
        # LoaiKhac
        outEraseLoaiKhacA = "in_memory\\outEraseLoaiKhacA"
        arcpy.Erase_analysis(in_features = outPolygonToLine,
                             erase_features = pathCauGiaoThongAFinal,
                             out_feature_class = outEraseLoaiKhacA)
        outEraseLoaiKhacB = "in_memory\\outEraseLoaiKhacB"
        arcpy.Erase_analysis(in_features = outEraseLoaiKhacA,
                             erase_features = pathHamGiaoThongAFinal,
                             out_feature_class = outEraseLoaiKhacB)
        outLoaiKhac = "in_memory\\outLoaiKhac"
        arcpy.Dissolve_management(in_features = outEraseLoaiKhacB,
                                  out_feature_class = outLoaiKhac,
                                  multi_part = "SINGLE_PART")
        outTable = "in_memory\\outTable"
        arcpy.GenerateNearTable_analysis(in_features = outLoaiKhac,
                                         near_features = pathMatDuongBoFinal,
                                         search_radius = "0 Meters",
                                         out_table = outTable)
        # Delete
        with arcpy.da.UpdateCursor(pathRanhGioiDuongBoFianl, ["OID@"]) as cursor:
            for row in cursor:
                cursor.deleteRow()
        # Insert Loai Khac
        with arcpy.da.SearchCursor(outTable, ["OID@", "IN_FID", "NEAR_FID"]) as cursorA:
            with arcpy.da.SearchCursor(pathMatDuongBoFinal, ["OID@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "tenManh", "soPhienHieuManhBanDo"]) as cursorB:
                with arcpy.da.SearchCursor(outLoaiKhac, ["OID@", "Shape@"]) as cursorC:
                    with arcpy.da.InsertCursor(pathRanhGioiDuongBoFianl, ["Shape@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "tenManh", "soPhienHieuManhBanDo", "maDoiTuong", "doiTuong", "loaiRanhGioiDuongBo"]) as cursorD:
                        for rowA in cursorA:
                            #
                            inFID = rowA[1]
                            nearFID = rowA[2]
                            #
                            rowMatDuongBo = None
                            cursorB.reset()
                            for rowB in cursorB:
                                if nearFID == rowB[0]:
                                    rowMatDuongBo = rowB
                                    break
                            #
                            rowLoaiKhac = None
                            cursorC.reset()
                            for rowC in cursorC:
                                if inFID == rowC[0]:
                                    rowLoaiKhac = rowC
                                    break
                            #
                            if rowLoaiKhac != None and rowMatDuongBo != None:
                                cursorD.insertRow((rowLoaiKhac[1], rowMatDuongBo[1], rowMatDuongBo[2], rowMatDuongBo[3], rowMatDuongBo[4], rowMatDuongBo[5], "HA15", 2, 3))
        # Loai Thanh Cau, Loai Thanh Ham
        outPutLine = "in_memory\\outPutLine"
        arcpy.Erase_analysis(in_features = outPolygonToLine,
                             erase_features = outLoaiKhac,
                             out_feature_class = outPutLine,
                             cluster_tolerance = "0 Meters")
        outPutLineSingle = "in_memory\\outPutLineSingle"
        arcpy.MultipartToSinglepart_management(in_features = outPutLine,
                                               out_feature_class = outPutLineSingle)
        ## Loai Thanh Cau
        outTable = "in_memory\\outTable"
        arcpy.GenerateNearTable_analysis(in_features = outPutLineSingle,
                                         near_features = pathCauGiaoThongAFinal,
                                         search_radius = "0 Meters",
                                         out_table = outTable)
        ## Insert Loai Thanh Cau
        with arcpy.da.SearchCursor(outTable, ["OID@", "IN_FID", "NEAR_FID"]) as cursorA:
            with arcpy.da.SearchCursor(pathCauGiaoThongAFinal, ["OID@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "tenManh", "soPhienHieuManhBanDo"]) as cursorB:
                with arcpy.da.SearchCursor(outPutLineSingle, ["OID@", "Shape@"]) as cursorC:
                    with arcpy.da.InsertCursor(pathRanhGioiDuongBoFianl, ["Shape@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "tenManh", "soPhienHieuManhBanDo", "maDoiTuong", "doiTuong", "loaiRanhGioiDuongBo"]) as cursorD:
                        for rowA in cursorA:
                            #
                            inFID = rowA[1]
                            nearFID = rowA[2]
                            #
                            rowMatDuongBo = None
                            cursorB.reset()
                            for rowB in cursorB:
                                if nearFID == rowB[0]:
                                    rowMatDuongBo = rowB
                                    break
                            #
                            rowLoaiKhac = None
                            cursorC.reset()
                            for rowC in cursorC:
                                if inFID == rowC[0]:
                                    rowLoaiKhac = rowC
                                    break
                            #
                            if rowLoaiKhac != None and rowMatDuongBo != None:
                                cursorD.insertRow((rowLoaiKhac[1], rowMatDuongBo[1], rowMatDuongBo[2], rowMatDuongBo[3], rowMatDuongBo[4], rowMatDuongBo[5], "HA15", 2, 1))

        ## Loai Thanh Ham
        outTable = "in_memory\\outTable"
        arcpy.GenerateNearTable_analysis(in_features = outPutLineSingle,
                                         near_features = pathHamGiaoThongAFinal,
                                         search_radius = "0 Meters",
                                         out_table = outTable)
        ## Insert Loai Thanh Cau
        with arcpy.da.SearchCursor(outTable, ["OID@", "IN_FID", "NEAR_FID"]) as cursorA:
            with arcpy.da.SearchCursor(pathHamGiaoThongAFinal, ["OID@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "tenManh", "soPhienHieuManhBanDo"]) as cursorB:
                with arcpy.da.SearchCursor(outPutLineSingle, ["OID@", "Shape@"]) as cursorC:
                    with arcpy.da.InsertCursor(pathRanhGioiDuongBoFianl, ["Shape@", "ngayThuNhan", "ngayCapNhat", "nguonDuLieu", "tenManh", "soPhienHieuManhBanDo", "maDoiTuong", "doiTuong", "loaiRanhGioiDuongBo"]) as cursorD:
                        for rowA in cursorA:
                            #
                            inFID = rowA[1]
                            nearFID = rowA[2]
                            #
                            rowMatDuongBo = None
                            cursorB.reset()
                            for rowB in cursorB:
                                if nearFID == rowB[0]:
                                    rowMatDuongBo = rowB
                                    break
                            #
                            rowLoaiKhac = None
                            cursorC.reset()
                            for rowC in cursorC:
                                if inFID == rowC[0]:
                                    rowLoaiKhac = rowC
                                    break
                            #
                            if rowLoaiKhac != None and rowMatDuongBo != None:
                                cursorD.insertRow((rowLoaiKhac[1], rowMatDuongBo[1], rowMatDuongBo[2], rowMatDuongBo[3], rowMatDuongBo[4], rowMatDuongBo[5], "HA15", 2, 2))
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

if __name__ == '__main__':
    runTime = RunTime()
    ranhGioiDuongBo = RanhGioiDuongBo()
    print "Running..."
    ranhGioiDuongBo.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass