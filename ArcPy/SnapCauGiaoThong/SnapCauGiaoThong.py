
print " ______   _____    _______                _______                   _       "
print "|  ____| |  __ \  |__   __|              |__   __|                 | |      "
print "| |__    | |__) |    | |       ______       | |      ___     ___   | |  ___ "
print "|  __|   |  ___/     | |      |______|      | |     / _ \   / _ \  | | / __|"
print "| |      | |         | |                    | |    | (_) | | (_) | | | \\__ \\"
print "|_|      |_|         |_|                    |_|     \___/   \___/  |_| |___/"

import arcpy
import os
import sys

class CauGiaoThongP:

    def __init__(self, distance):
        # Distance Snap
        self.distance = distance
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        # Feature DataSet Name
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        # Feature Class Name
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fCCauGiaoThongP = "CauGiaoThongP"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCSongSuoiL = "SongSuoiL"
        self.fCKenhMuongA = "KenhMuongA"
        self.fCKenhMuongL = "KenhMuongL"
        self.fCMangDanNuocA = "MangDanNuocA"
        self.fCMangDanNuocL = "MangDanNuocL"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        # Path Feature Class
        ## Path Process
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCauGiaoThongPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathKenhMuongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathMangDanNuocAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocA)
        self.pathMangDanNuocLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocL)
        self.pathDuongBoNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCauGiaoThongPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongP)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathKenhMuongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathMangDanNuocAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocA)
        self.pathMangDanNuocLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocL)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.CopyFromProcessToFinal()
        self.CreateFeatureClassPointSnapA()
        self.SnapCauGiaoThongPVsPointSnapA()
        self.CreateFeatureClassPointSnapB()
        self.SnapCauGiaoThongPVsPointSnapB()
        self.DeleteCongGiaoThongP()
        pass

    def CopyFromProcessToFinal(self):
        arcpy.CopyFeatures_management(in_features = self.pathCauGiaoThongPProcess,
                                      out_feature_class = self.pathCauGiaoThongPFinal)
        pass

    def CreateFeatureClassPointSnapA(self):
        # CreateFeatureclass self.pointSnapA
        self.pointSnapA = "in_memory\\PointSnapA"
        arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                            out_name = "PointSnapA",
                                            geometry_type = "MULTIPOINT")
        # DoanTimDuongBo Final vs SongSuoiL Final
        self.IntersectAndInsertPointSnapA(self.pathDoanTimDuongBoFinal, self.pathSongSuoiLFinal)
        # DoanTimDuongBo Final vs KenhMuongL Final
        self.IntersectAndInsertPointSnapA(self.pathDoanTimDuongBoFinal, self.pathKenhMuongLFinal)
        # DoanTimDuongBo Final vs MangDanNuocL Final
        self.IntersectAndInsertPointSnapA(self.pathDoanTimDuongBoFinal, self.pathMangDanNuocLFinal)
        pass

    def SnapCauGiaoThongPVsPointSnapA(self):
        snapEnv = [self.pointSnapA, "END", self.distance]
        arcpy.Snap_edit(in_features = self.pathCauGiaoThongPFinal,
                        snap_environment = [snapEnv])
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

    def CreateFeatureClassPointSnapB(self):
        # CreateFeatureclass self.pointSnapB
        self.pointSnapB = "in_memory\\PointSnapB"
        arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                            out_name = "PointSnapB",
                                            geometry_type = "POINT")
        # Dissolve DoanTimDuongBoFinal
        self.doanTimDuongBoFinalTemp = "in_memory\\doanTimDuongBoFinalTemp"
        arcpy.CopyFeatures_management(in_features = self.pathDoanTimDuongBoFinal,
                                      out_feature_class = self.doanTimDuongBoFinalTemp)
        arcpy.AddField_management(in_table = self.doanTimDuongBoFinalTemp,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        self.doanTimDuongBoFinalTempDissolve = "in_memory\\doanTimDuongBoFinalTempDissolve"
        arcpy.Dissolve_management(in_features = self.doanTimDuongBoFinalTemp,
                                  out_feature_class = self.doanTimDuongBoFinalTempDissolve,
                                  dissolve_field = "Dissolve")
        # DoanTimDuongBo vs SuongSuoiA (Line vs Polygon)
        self.InsertPointSnapB(self.pathSongSuoiAFinal)
        # DoanTimDuongBo vs KenhMuongA (Line vs Polygon)
        self.InsertPointSnapB(self.pathKenhMuongAFinal)
        # DoanTimDuongBo vs MatNuocTinh (Line vs Polygon)
        self.InsertPointSnapB(self.pathMatNuocTinhFinal)
        # DoanTimDuongBo vs MangDanNuocA (Line vs Polygon)
        self.InsertPointSnapB(self.pathMangDanNuocAFinal)
        pass

    def SnapCauGiaoThongPVsPointSnapB(self):
        # Make Feature Layer
        self.pointSnapALayer = "pointSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapA,
                                          out_layer = self.pointSnapALayer)
        self.cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = self.cauGiaoThongPFinalLayer)
        # Select
        arcpy.SelectLayerByLocation_management(in_layer = self.cauGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        # Snap
        snapEnv = [self.pointSnapB, "END", self.distance]
        arcpy.Snap_edit(in_features = self.cauGiaoThongPFinalLayer,
                        snap_environment = [snapEnv])
        pass

    def InsertPointSnapB(self, fCPolygon):
        ## Intersect
        outputIntersect = "in_memory\\outputIntersect"
        arcpy.Intersect_analysis(in_features = [self.doanTimDuongBoFinalTempDissolve, fCPolygon],
                                 out_feature_class = outputIntersect,
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

    def DeleteCongGiaoThongP(self):
        # Make Feature Layer
        self.cauGiaoThongPFinalLayer = "cauGiaoThongPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCauGiaoThongPFinal,
                                          out_layer = self.cauGiaoThongPFinalLayer)
        self.pointSnapALayer = "pointSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapA,
                                          out_layer = self.pointSnapALayer)
        self.pointSnapBLayer = "pointSnapBLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapB,
                                          out_layer = self.pointSnapBLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = self.cauGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.cauGiaoThongPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapBLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.DeleteFeatures_management(in_features = self.cauGiaoThongPFinalLayer)
        pass

class CauGiaoThongL:
    
    def __init__(self, distance):
        # Distance Snap
        self.distance = distance
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        # Feature DataSet Name
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        # Feature Class Name
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fCCauGiaoThongL = "CauGiaoThongL"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCKenhMuongA = "KenhMuongA"
        self.fCMangDanNuocA = "MangDanNuocA"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        # Path Feature Class
        ## Path Process
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCauGiaoThongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCCauGiaoThongL)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMangDanNuocAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMangDanNuocA)
        self.pathDuongBoNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCauGiaoThongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCCauGiaoThongL)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMangDanNuocAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMangDanNuocA)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.CopyFromProcessToFinal()
        self.CreateFeatureClassLineSnap()
        self.SnapCauGiaoThongLVsLineSnap()
        pass

    def CopyFromProcessToFinal(self):
        arcpy.CopyFeatures_management(in_features = self.pathCauGiaoThongLProcess,
                                      out_feature_class = self.pathCauGiaoThongLFinal)
        pass

    def CreateFeatureClassLineSnap(self):
        # CreateFeatureclass self.pointSnapB
        self.lineSnap = "in_memory\\lineSnap"
        arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                            out_name = "lineSnap",
                                            geometry_type = "POLYLINE")
        # Dissolve DoanTimDuongBoFinal
        self.doanTimDuongBoFinalTemp = "in_memory\\doanTimDuongBoFinalTemp"
        arcpy.CopyFeatures_management(in_features = self.pathDoanTimDuongBoFinal,
                                      out_feature_class = self.doanTimDuongBoFinalTemp)
        arcpy.AddField_management(in_table = self.doanTimDuongBoFinalTemp,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        self.doanTimDuongBoFinalTempDissolve = "in_memory\\doanTimDuongBoFinalTempDissolve"
        arcpy.Dissolve_management(in_features = self.doanTimDuongBoFinalTemp,
                                  out_feature_class = self.doanTimDuongBoFinalTempDissolve,
                                  dissolve_field = "Dissolve")
        # DoanTimDuongBo vs SuongSuoiA (Line vs Polygon)
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
        arcpy.Intersect_analysis(in_features = [self.doanTimDuongBoFinalTempDissolve, fCPolygon],
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

    def SnapCauGiaoThongLVsLineSnap(self):
        snapEnv = [self.lineSnap, "VERTEX", self.distance]
        arcpy.Snap_edit(in_features = self.pathCauGiaoThongLFinal,
                        snap_environment = [snapEnv])
        pass

if __name__ == "__main__":
    print "Distance: {}".format(sys.argv[1])
    print "CauGiaoThongP"
    cauGiaoThongP = CauGiaoThongP(sys.argv[1])
    cauGiaoThongP.Execute()
    print "CauGiaoThongL"
    cauGiaoThongL = CauGiaoThongL(sys.argv[1])
    cauGiaoThongL.Execute()