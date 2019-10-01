# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime

class SnapTools:

    def __init__(self, distance):
        # 
        print "CongThuyLoi (P, L)\nCongGiaoThong (P, L)\nCauGiaoThong (P, L)\nDoanVuotSongSuoi (P, L)\nHam (P)"
        # Distance Snap
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
        self.fCHamDiBoP = "HamDiBoP"
        self.fCDeo = "Deo"
        # GiaoThong Line
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fCCauGiaoThongL = "CauGiaoThongL"
        self.fCCongGiaoThongL = "CongGiaoThongL"
        self.fCDoanVuotSongSuoiL = "DoanVuotSongSuoiL"
        # ThuyHe Point
        self.fCCongThuyLoiP = "CongThuyLoiP"
        # ThuyHe Line
        self.fCCongThuyLoiL = "CongThuyLoiL"
        self.fCSongSuoiL = "SongSuoiL"
        self.fCKenhMuongL = "KenhMuongL"
        self.fCMangDanNuocL = "MangDanNuocL"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        # ThuyHe Area
        self.fCSongSuoiA = "SongSuoiA"
        self.fCKenhMuongA = "KenhMuongA"
        self.fCMangDanNuocA = "MangDanNuocA"
        self.fCMatNuocTinh = "MatNuocTinh"

        # Path Feature Class
        ## Path Process
        ### GiaoThong Point
        self.pathCauGiaoThongPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathCongGiaoThongPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathDoanVuotSongSuoiPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanVuotSongSuoiP)
        self.pathHamDiBoPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCHamDiBoP)
        ### GiaoThong Line
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCauGiaoThongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCauGiaoThongL)
        self.pathCongThuyLoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCCongThuyLoiL)
        self.pathCongGiaoThongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCongGiaoThongL)
        self.pathDoanVuotSongSuoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanVuotSongSuoiL)
        ### ThuyHe Point
        self.pathCongThuyLoiPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        ### ThuyHe Line
        self.pathCongThuyLoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCCongThuyLoiL)
        self.pathSongSuoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathMangDanNuocLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocL)
        self.pathDuongBoNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        ### ThuyHe Area
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMangDanNuocAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocA)
        ## Path Final
        ### GiaoThong Line
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCauGiaoThongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongL)
        self.pathCongGiaoThongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCongGiaoThongL)
        self.pathDoanVuotSongSuoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanVuotSongSuoiL)
        ### GiaoThong Point
        self.pathCauGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathCongGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathDoanVuotSongSuoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanVuotSongSuoiP)
        self.pathHamDiBoPFinal = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCHamDiBoP)
        self.pathDeoFinal = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDeo)
        ### ThuyHe Point
        self.pathCongThuyLoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        ### ThuyHe Area
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMangDanNuocAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocA)
        ### ThuyHe Line
        self.pathCongThuyLoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiL)
        self.pathSongSuoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathMangDanNuocLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocL)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Dissolve DoanTimDuongBo
        self.DissolveDoanTimDuongBo()

        # Copy
        #self.CopyFromProcessToFinal()

        # Snap FeatureClass Point
        ## Snap vs FeatureClassPointSnapA (Point = Line Intersect Line)
        self.CreateFeatureClassPointSnapA()
        self.SnapVsPointSnapA()
        ## Snap vs FeatureClassPointSnapB (Midpoint of (Line = Line Intersect Polygon))
        self.CreateFeatureClassPointSnapB()
        self.SnapVsPointSnapB()

        # Snap FeatureClass Line
        self.CreateFeatureClassLineSnap()
        self.SnapVsLineSnap()

        # Delete FeaturePoint Not Snap
        self.DeleteFeatureClassP()
        
        # Delete FeatureLine Not Snap
        self.DeleteFeatureClassL()
        pass

    def XuLyDeo(self):
        self.deoFinalLayer = "deoFinalLayer"
        self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDeoFinal,
                                          out_layer = self.deoFinalLayer)
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer)
        snapEnv = [self.doanTimDuongBoFinalLayer, "EDGE", self.distance]
        arcpy.Snap_edit(in_features = self.deoFinalLayer, snap_environment = snapEnv)
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer,
                                          where_clause = "phanLoaiDuong = 3 OR phanLoaiDuong = 2 OR phanLoaiDuong = 1 OR phanLoaiDuong = 11 OR phanLoaiDuong = 4")
        arcpy.SelectLayerByLocation_management(in_layer = self.deoFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.doanTimDuongBoFinalLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.DeleteFeatures_management(in_features = self.deoFinalLayer)
        pass

    def XuLyHamP(self):
        self.hamDiBoPFinalLayer = "hamDiBoPFinalLayer"
        self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathHamDiBoPFinal,
                                          out_layer = self.hamDiBoPFinalLayer)
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer)
        snapEnv = [self.doanTimDuongBoFinalLayer, "EDGE", self.distance]
        arcpy.Snap_edit(in_features = self.hamDiBoPFinalLayer, snap_environment = snapEnv)
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer,
                                          where_clause = "phanLoaiDuong = 3 OR phanLoaiDuong = 2 OR phanLoaiDuong = 1 OR phanLoaiDuong = 11 OR phanLoaiDuong = 4")
        arcpy.SelectLayerByLocation_management(in_layer = self.hamDiBoPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.doanTimDuongBoFinalLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.DeleteFeatures_management(in_features = self.hamDiBoPFinalLayer)

    def CopyFromProcessToFinal(self):
        # Point
        arcpy.CopyFeatures_management(in_features = self.pathCongThuyLoiPProcess,
                                      out_feature_class = self.pathCongThuyLoiPFinal)
        arcpy.CopyFeatures_management(in_features = self.pathCauGiaoThongPProcess,
                                      out_feature_class = self.pathCauGiaoThongPFinal)
        arcpy.CopyFeatures_management(in_features = self.pathCongGiaoThongPProcess,
                                      out_feature_class = self.pathCongGiaoThongPFinal)
        arcpy.CopyFeatures_management(in_features = self.pathDoanVuotSongSuoiPProcess,
                                      out_feature_class = self.pathDoanVuotSongSuoiPFinal)
        # Line
        arcpy.CopyFeatures_management(in_features = self.pathCongThuyLoiLProcess,
                                      out_feature_class = self.pathCongThuyLoiLFinal)
        arcpy.CopyFeatures_management(in_features = self.pathCauGiaoThongLProcess,
                                      out_feature_class = self.pathCauGiaoThongLFinal)
        arcpy.CopyFeatures_management(in_features = self.pathCongGiaoThongLProcess,
                                      out_feature_class = self.pathCongGiaoThongLFinal)
        arcpy.CopyFeatures_management(in_features = self.pathDoanVuotSongSuoiLProcess,
                                      out_feature_class = self.pathDoanVuotSongSuoiLFinal)
        pass

    def DissolveDoanTimDuongBo(self):
        # Copy To Memory
        doanTimDuongBoInMemory = "in_memory\\doanTimDuongBoInMemory"
        arcpy.CopyFeatures_management(in_features = self.pathDoanTimDuongBoFinal,
                                      out_feature_class = doanTimDuongBoInMemory)
        # Add Fields And Dissolve
        arcpy.AddField_management(in_table = doanTimDuongBoInMemory,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        self.doanTimDuongBoInMemoryDissolve = "in_memory\\doanTimDuongBoInMemoryDissolve"
        arcpy.Dissolve_management(in_features = doanTimDuongBoInMemory,
                                  out_feature_class = self.doanTimDuongBoInMemoryDissolve,
                                  dissolve_field = "Dissolve")
        pass

    def CreateFeatureClassPointSnapA(self):
        # CreateFeatureclass self.pointSnapA
        self.pointSnapA = "in_memory\\PointSnapA"
        arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                            out_name = "PointSnapA",
                                            geometry_type = "MULTIPOINT",
                                            spatial_reference = arcpy.Describe(self.pathDoanTimDuongBoFinal).spatialReference)
        # DoanTimDuongBo Final vs SongSuoiL Final
        self.IntersectAndInsertPointSnapA(self.doanTimDuongBoInMemoryDissolve, self.pathSongSuoiLFinal)
        # DoanTimDuongBo Final vs KenhMuongL Final
        self.IntersectAndInsertPointSnapA(self.doanTimDuongBoInMemoryDissolve, self.pathKenhMuongLFinal)
        # DoanTimDuongBo Final vs MangDanNuocL Final
        self.IntersectAndInsertPointSnapA(self.doanTimDuongBoInMemoryDissolve, self.pathMangDanNuocLFinal)
        # SongSuoiL Final vs KenhMuongL Final
        self.IntersectAndInsertPointSnapA(self.pathSongSuoiLFinal, self.pathKenhMuongLFinal)
        #
        tempFc = "in_memory\\tempFc"
        arcpy.MultipartToSinglepart_management(in_features = self.pointSnapA,
                                               out_feature_class = tempFc)
        arcpy.Dissolve_management(in_features = tempFc,
                                  out_feature_class = self.pointSnapA,
                                  multi_part = "SINGLE_PART")
        pass

    def IntersectAndInsertPointSnapA(self, fCOne, fCTwo):
        outputIntersect = "in_memory\\outputIntersect"
        arcpy.Intersect_analysis(in_features = [fCOne, fCTwo],
                                 out_feature_class = outputIntersect,
                                 output_type = "POINT")
        with arcpy.da.SearchCursor(outputIntersect, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(self.pointSnapA, ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], ))
        pass

    def SnapVsPointSnapA(self):
        snapEnv = [self.pointSnapA, "END", self.distance]
        # CongThuyLoiP
        arcpy.Snap_edit(in_features = self.pathCongThuyLoiPFinal,
                        snap_environment = [snapEnv])
        # CauGiaoThongP
        arcpy.Snap_edit(in_features = self.pathCauGiaoThongPFinal,
                        snap_environment = [snapEnv])
        # CongGiaoThongP
        arcpy.Snap_edit(in_features = self.pathCongGiaoThongPFinal,
                        snap_environment = [snapEnv])
        # DoanVuotSongSuoiP
        arcpy.Snap_edit(in_features = self.pathDoanVuotSongSuoiPFinal,
                        snap_environment = [snapEnv])
        pass

    def CreateFeatureClassPointSnapB(self):
        # CreateFeatureclass self.pointSnapB
        self.pointSnapB = "in_memory\\PointSnapB"
        arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                            out_name = "PointSnapB",
                                            geometry_type = "POINT",
                                            spatial_reference = arcpy.Describe(self.pathDoanTimDuongBoFinal).spatialReference)
        # DoanTimDuongBo vs SongSuoiA (Line vs Polygon)
        self.InsertPointSnapB(self.doanTimDuongBoInMemoryDissolve, self.pathSongSuoiAFinal)
        # DoanTimDuongBo vs KenhMuongA (Line vs Polygon)
        self.InsertPointSnapB(self.doanTimDuongBoInMemoryDissolve, self.pathKenhMuongAFinal)
        # DoanTimDuongBo vs MatNuocTinh (Line vs Polygon)
        self.InsertPointSnapB(self.doanTimDuongBoInMemoryDissolve, self.pathMatNuocTinhFinal)
        # DoanTimDuongBo vs MangDanNuocA (Line vs Polygon)
        self.InsertPointSnapB(self.doanTimDuongBoInMemoryDissolve, self.pathMangDanNuocAFinal)
        # SongSuoiL vs MatNuocTinh
        self.InsertPointSnapBTwo(self.pathSongSuoiLFinal, self.pathMatNuocTinhFinal)
        # SongSuoiL vs SongSuoiA
        self.InsertPointSnapBTwo(self.pathSongSuoiLFinal, self.pathSongSuoiAFinal)
        # KenhMuongL vs MatNuocTinh
        self.InsertPointSnapBTwo(self.pathKenhMuongLFinal, self.pathMatNuocTinhFinal)
        # KenhMuongL vs SongSuoiA
        self.InsertPointSnapBTwo(self.pathKenhMuongLFinal, self.pathSongSuoiAFinal)
        pass

    def InsertPointSnapB(self, pathLine, fCPolygon):
        ## Intersect
        outputIntersect = "in_memory\\outputIntersect"
        arcpy.Intersect_analysis(in_features = [pathLine, fCPolygon],
                                 out_feature_class = outputIntersect,
                                 cluster_tolerance = "0 Meters",
                                 output_type = "LINE")
        outputErase = "in_memory\\outputErase"
        arcpy.Erase_analysis(in_features = outputIntersect,
                             erase_features = self.pathDuongBoNuocFinal,
                             out_feature_class = outputErase)
        ## MultipartToSinglepart And FeatureVerticesToPoints
        outputMultipartToSinglepart = "in_memory\\OutputMultipartToSinglepart"
        arcpy.MultipartToSinglepart_management(in_features = outputErase,
                                               out_feature_class = outputMultipartToSinglepart)
        outputFeatureVerticesToPoints = "in_memory\\outputFeatureVerticesToPoints"
        arcpy.FeatureVerticesToPoints_management(in_features = outputMultipartToSinglepart,
                                                 out_feature_class = outputFeatureVerticesToPoints,
                                                 point_location = "MID")
        with arcpy.da.SearchCursor(outputFeatureVerticesToPoints, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(self.pointSnapB, ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], ))
        pass

    def InsertPointSnapBTwo(self, pathLine, fCPolygon):
        ## Intersect
        outputIntersect = "in_memory\\outputIntersect"
        arcpy.Intersect_analysis(in_features = [pathLine, fCPolygon],
                                 out_feature_class = outputIntersect,
                                 cluster_tolerance = "0 Meters",
                                 output_type = "POINT")
        ## MultipartToSinglepart And FeatureVerticesToPoints
        outputMultipartToSinglepart = "in_memory\\OutputMultipartToSinglepart"
        arcpy.MultipartToSinglepart_management(in_features = outputIntersect,
                                               out_feature_class = outputMultipartToSinglepart)
        with arcpy.da.SearchCursor(outputMultipartToSinglepart, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(self.pointSnapB, ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], ))
        pass

    def SnapVsPointSnapB(self):
        # Make Feature Layer
        ## pointSnapALayer
        self.pointSnapALayer = "pointSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapA,
                                          out_layer = self.pointSnapALayer)
        ## congThuyLoiPFinalLayer
        self.congThuyLoiPFinalLayer = "congThuyLoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiPFinal,
                                          out_layer = self.congThuyLoiPFinalLayer)
        ## cauGiaoThongPFinalLayer
        self.cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = self.cauGiaoThongPFinalLayer)
        ## congGiaoThongPFinalLayer
        self.congGiaoThongPFinalLayer = "congGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongPFinal,
                                          out_layer = self.congGiaoThongPFinalLayer)
        ## doanVuotSongSuoiPFinalLayer
        self.doanVuotSongSuoiPFinalLayer = "doanVuotSongSuoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanVuotSongSuoiPFinal,
                                          out_layer = self.doanVuotSongSuoiPFinalLayer)

        # Select
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.cauGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")

        # Snap
        snapEnv = [self.pointSnapB, "END", self.distance]
        arcpy.Snap_edit(in_features = self.congThuyLoiPFinalLayer,
                        snap_environment = [snapEnv])
        arcpy.Snap_edit(in_features = self.cauGiaoThongPFinalLayer,
                        snap_environment = [snapEnv])
        arcpy.Snap_edit(in_features = self.congGiaoThongPFinalLayer,
                        snap_environment = [snapEnv])
        arcpy.Snap_edit(in_features = self.doanVuotSongSuoiPFinalLayer,
                        snap_environment = [snapEnv])
        pass

    def CreateFeatureClassLineSnap(self):
        # CreateFeatureclass self.pointSnapB
        self.lineSnap = "in_memory\\lineSnap"
        #arcpy.CreateFeatureclass_management(out_path = "in_memory",
        #                                    out_name = "lineSnap",
        #                                    geometry_type = "POLYLINE")
        self.lineSnap = os.path.join(self.pathProcessGDB, "LineSnap")
        arcpy.CreateFeatureclass_management(out_path = self.pathProcessGDB,
                                            out_name = "LineSnap",
                                            geometry_type = "POLYLINE",
                                            spatial_reference = arcpy.Describe(self.pathDoanTimDuongBoFinal).spatialReference)
        # DoanTimDuongBo vs SongSuoiA (Line vs Polygon)
        self.InsertLineSnap(self.pathSongSuoiAFinal)
        # DoanTimDuongBo vs KenhMuongA (Line vs Polygon)
        self.InsertLineSnap(self.pathKenhMuongAFinal)
        # DoanTimDuongBo vs MatNuocTinh (Line vs Polygon)
        self.InsertLineSnap(self.pathMatNuocTinhFinal)
        # DoanTimDuongBo vs MangDanNuocA (Line vs Polygon)
        self.InsertLineSnap(self.pathMangDanNuocAFinal)
        pass

    def InsertLineSnap(self, fCPolygon):
        ## Intersect
        outputIntersect = "in_memory\\outputIntersect"
        arcpy.Intersect_analysis(in_features = [self.doanTimDuongBoInMemoryDissolve, fCPolygon],
                                 out_feature_class = outputIntersect,
                                 output_type = "LINE")
        outputErase = "in_memory\\outputErase"
        arcpy.Erase_analysis(in_features = outputIntersect,
                             erase_features = self.pathDuongBoNuocFinal,
                             out_feature_class = outputErase)
        with arcpy.da.SearchCursor(outputErase, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(self.lineSnap, ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0], ))
        pass

    def SnapVsLineSnap(self):
        snapEnv = [self.lineSnap, "VERTEX", self.distance]
        arcpy.Snap_edit(in_features = self.pathCongThuyLoiLFinal,
                        snap_environment = [snapEnv])
        arcpy.Snap_edit(in_features = self.pathCauGiaoThongLFinal,
                        snap_environment = [snapEnv])
        arcpy.Snap_edit(in_features = self.pathCongGiaoThongLFinal,
                        snap_environment = [snapEnv])
        arcpy.Snap_edit(in_features = self.pathDoanVuotSongSuoiLFinal,
                        snap_environment = [snapEnv])
        pass

    def DeleteFeatureClassP(self):
        # Make Feature Layer
        ## 
        self.congThuyLoiPFinalLayer = "congThuyLoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiPFinal,
                                          out_layer = self.congThuyLoiPFinalLayer)
        self.cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = self.cauGiaoThongPFinalLayer)
        self.congGiaoThongPFinalLayer = "congGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongPFinal,
                                          out_layer = self.congGiaoThongPFinalLayer)
        self.doanVuotSongSuoiPFinalLayer = "doanVuotSongSuoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanVuotSongSuoiPFinal,
                                          out_layer = self.doanVuotSongSuoiPFinalLayer)
        ## 
        #self.pointSnapALayer = "pointSnapALayer"
        #arcpy.MakeFeatureLayer_management(in_features = self.pointSnapA,
        #                                  out_layer = self.pointSnapALayer)
        #self.pointSnapBLayer = "pointSnapBLayer"
        #arcpy.MakeFeatureLayer_management(in_features = self.pointSnapB,
        #                                  out_layer = self.pointSnapBLayer)

        # Select By Location
        ##
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathSongSuoiAFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathSongSuoiLFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathMatNuocTinhFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathKenhMuongAFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathKenhMuongLFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.DeleteFeatures_management(in_features = self.congThuyLoiPFinalLayer)
        ##
        arcpy.SelectLayerByLocation_management(in_layer = self.cauGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathDoanTimDuongBoFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.DeleteFeatures_management(in_features = self.cauGiaoThongPFinalLayer)
        ##
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathDoanTimDuongBoFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.DeleteFeatures_management(in_features = self.congGiaoThongPFinalLayer)
        ## DoanVuotSongSuoiP
        ### Rule 1
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathDoanTimDuongBoFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.DeleteFeatures_management(in_features = self.doanVuotSongSuoiPFinalLayer)
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathSongSuoiAFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathSongSuoiLFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathMatNuocTinhFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.doanVuotSongSuoiPFinalLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pathKenhMuongLFinal,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.DeleteFeatures_management(in_features = self.doanVuotSongSuoiPFinalLayer)
        ### Rule 2
        self.doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer"
        self.doanVuotSongSuoiPFinalLayer = "doanVuotSongSuoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanVuotSongSuoiPFinal,
                                          out_layer = self.doanVuotSongSuoiPFinalLayer)
        arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal,
                                          out_layer = self.doanTimDuongBoFinalLayer,
                                          where_clause = "phanLoaiDuong = 3 OR phanLoaiDuong = 2 OR phanLoaiDuong = 1 OR phanLoaiDuong = 11 OR phanLoaiDuong = 4")
        arcpy.SelectLayerByLocation_management(in_layer = self.doanVuotSongSuoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.doanTimDuongBoFinalLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.DeleteFeatures_management(in_features = self.doanVuotSongSuoiPFinalLayer)
        pass

    def DeleteFeatureClassL(self):
        # Make Feature Layer
        ##
        self.congThuyLoiLFinalLayer = arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiLFinal)
        self.cauGiaoThongLFinalLayer = arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongLFinal)
        self.congGiaoThongLFinalLayer = arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongLFinal)
        ##
        self.doanTimDuongBoFinalLayer = arcpy.MakeFeatureLayer_management(in_features = self.pathDoanTimDuongBoFinal)
        #
        arcpy.SelectLayerByLocation_management(in_layer = self.cauGiaoThongLFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.doanTimDuongBoFinalLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        print " ### Count Delte CauGiaoThongL {}".format(arcpy.GetCount_management(self.cauGiaoThongLFinalLayer).getOutput(0))
        arcpy.DeleteFeatures_management(in_features = self.cauGiaoThongLFinalLayer)
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongLFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.doanTimDuongBoFinalLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        print " ### Count Delte CongGiaoThongL {}".format(arcpy.GetCount_management(self.congGiaoThongLFinalLayer).getOutput(0))
        arcpy.DeleteFeatures_management(in_features = self.congGiaoThongLFinalLayer)
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
    print "Snap Distance: {}".format(sys.argv[1])
    snapTools = SnapTools(sys.argv[1])
    print "Running..."
    snapTools.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass