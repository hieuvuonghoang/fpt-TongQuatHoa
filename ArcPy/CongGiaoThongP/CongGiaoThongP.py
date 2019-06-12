import arcpy
import os
import sys

class CongGiaoThongP:

    def __init__(self):
        # Distance Snap
        self.distance = "50 Meters"
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        # Feature DataSet Name
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        # Feature Class Name
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fCCongGiaoThongP = "CongGiaoThongP"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCSongSuoiL = "SongSuoiL"
        self.fCKenhMuongA = "KenhMuongA"
        self.fCKenhMuongL = "KenhMuongL"
        self.fCMangDanNuocA = "MangDanNuocA"
        self.fCMangDanNuocL = "MangDanNuocL"
        # Path Feature Class
        ## Path Process
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCongGiaoThongPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathKenhMuongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathMangDanNuocAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocA)
        self.pathMangDanNuocLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocL)
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCongGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCongGiaoThongP)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathKenhMuongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathMangDanNuocAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocA)
        self.pathMangDanNuocLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocL)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.CopyFromProcessToFinal()
        # Sinh ra lop Point la giao cua Line vs Line (DoanTimDuongBo vs [SongSuoiL, KenhMuongL, MangDanNuocL]): self.pointEnvSnapA
        self.CreatePointByIntersectLine()
        # Snap CongGiaoThongP vs FeatureClass: self.pointEnvSnapA
        self.SnapVsPointByIntersectLine()
        # Sinh ra lop Point la giao cua Line vs Polygon (DoanTimDuongBo vs [SongSuoiA, KenhMuongA, MangDanNuocA, MatNuocTinh]): self.pointEnvSnapB
        self.CreatePointByIntersectLineVsPolygon()
        # Snap CongGiaoThongP vs FeatureClass: self.pointEnvSnapB
        self.SnapVsPointByIntersectLineVsPolygon()
        # Delete CongGiaoThongP khong the Snap
        self.DeleteCongGiaoThongP()
        pass

    def CopyFromProcessToFinal(self):
        print "\tCopyFromProcessToFinal"
        arcpy.CopyFeatures_management(in_features = self.pathCongGiaoThongPProcess,
                                      out_feature_class = self.pathCongGiaoThongPFinal)
        pass

    def CreatePointByIntersectLine(self):
        print "\tCreatePointByIntersectLine"
        inputMerge = [self.pathSongSuoiLFinal, self.pathKenhMuongLFinal, self.pathMangDanNuocLFinal]
        outputMerge = "in_memory\\OutputMerge"
        arcpy.Merge_management(inputs = inputMerge,
                               output = outputMerge)
        inputIntersectLine = [self.pathDoanTimDuongBoFinal, outputMerge]
        self.pointEnvSnapA = "in_memory\\OutputIntersectLine"
        arcpy.Intersect_analysis(in_features = inputIntersectLine,
                                 out_feature_class = self.pointEnvSnapA,
                                 output_type = "POINT")
        pass

    def SnapVsPointByIntersectLine(self):
        print "\tSnapVsPointByIntersectLine"
        # Make Feature Layer
        self.congGiaoThongPFinalLayer = "CongGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongPFinal,
                                          out_layer = self.congGiaoThongPFinalLayer)
        # Snap
        snapEnv = [self.pointEnvSnapA, "END", self.distance]
        arcpy.Snap_edit(in_features = self.congGiaoThongPFinalLayer,
                        snap_environment = [snapEnv])
        pass

    def CreatePointByIntersectLineVsPolygon(self):
        print "\tCreatePointByIntersectLineVsPolygon"
        # Merge Polygon
        inputMerge = [self.pathKenhMuongAFinal, self.pathSongSuoiAFinal, self.pathMangDanNuocAFinal, self.pathMatNuocTinhFinal]
        outputMerge = "in_memory\\OutputMerge"
        arcpy.Merge_management(inputs = inputMerge,
                               output = outputMerge)
        # AddField And Dissolve
        arcpy.AddField_management(in_table = outputMerge,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        outputDissolve = "in_memory\\OutputDissolve"
        arcpy.Dissolve_management(in_features = outputMerge,
                                  out_feature_class = outputDissolve,
                                  dissolve_field = "Dissolve")
        # Feature To Line
        outputFeatureToLine = "in_memory\\OutputFeatureToLine"
        arcpy.FeatureToLine_management(in_features = outputDissolve,
                                       out_feature_class = outputFeatureToLine)
        # Create doanTimDuongBoFinalTemp
        doanTimDuongBoFinalTemp = "in_memory\\DoanTimDuongBoFinalTemp"
        arcpy.CopyFeatures_management(in_features = self.pathDoanTimDuongBoFinal,
                                      out_feature_class = doanTimDuongBoFinalTemp)
        # AddField And Dissolve
        arcpy.AddField_management(in_table = doanTimDuongBoFinalTemp,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        outputDissolveA = "in_memory\\OutputDissolveA"
        arcpy.Dissolve_management(in_features = doanTimDuongBoFinalTemp,
                                  out_feature_class = outputDissolveA,
                                  dissolve_field = "Dissolve")
        # Intersect And Erase
        outputIntersect = "in_memory\\OutputIntersect"
        arcpy.Intersect_analysis(in_features = [outputDissolve, outputDissolveA],
                                 out_feature_class = outputIntersect,
                                 output_type = "LINE")
        outputErase = "in_memory\\OutputErase"
        arcpy.Erase_analysis(in_features = outputIntersect,
                             erase_features = outputFeatureToLine,
                             out_feature_class = outputErase)
        # Multipart To Singlepart
        outputMultipartToSinglepart = "in_memory\\OutputMultipartToSinglepart"
        arcpy.MultipartToSinglepart_management(in_features = outputErase,
                                               out_feature_class = outputMultipartToSinglepart)
        # FeatureVerticesToPoints: MID (diem chinh giua cua moi Polyline)
        self.pointEnvSnapB = "in_memory\\PointEnvSnapB"
        arcpy.FeatureVerticesToPoints_management(in_features = outputMultipartToSinglepart,
                                                 out_feature_class = self.pointEnvSnapB,
                                                 point_location = "MID")
        pass

    def SnapVsPointByIntersectLineVsPolygon(self):
        print "\tSnapVsPointByIntersectLineVsPolygon"
        # Make Feature Layer
        self.congGiaoThongPFinalLayer = "CongGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongPFinal,
                                          out_layer = self.congGiaoThongPFinalLayer)
        self.pointEnvSnapALayer = "PointEnvSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointEnvSnapA,
                                          out_layer = self.pointEnvSnapALayer)
        # Select By Location
        ## Chon nhung CongGiaoThongP chua duoc Snap o buoc Snap truoc
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointEnvSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        # Snap
        snapEnv = [self.pointEnvSnapB, "END", self.distance]
        arcpy.Snap_edit(in_features = self.congGiaoThongPFinalLayer,
                        snap_environment = [snapEnv])
        pass

    def DeleteCongGiaoThongP(self):
        print "\tDeleteCongGiaoThongP"
        # Make Feature Layer
        self.congGiaoThongPFinalLayer = "CongGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongGiaoThongPFinal,
                                          out_layer = self.congGiaoThongPFinalLayer)
        self.pointEnvSnapALayer = "PointEnvSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointEnvSnapA,
                                          out_layer = self.pointEnvSnapALayer)
        self.pointEnvSnapBLayer = "PointEnvSnapBLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointEnvSnapB,
                                          out_layer = self.pointEnvSnapBLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointEnvSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointEnvSnapBLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.DeleteFeatures_management(in_features = self.congGiaoThongPFinalLayer)
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointEnvSnapBLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.congGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointEnvSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.DeleteFeatures_management(in_features = self.congGiaoThongPFinalLayer)
        pass

if __name__ == "__main__":
    congGiaoThongP = CongGiaoThongP()
    congGiaoThongP.Execute()