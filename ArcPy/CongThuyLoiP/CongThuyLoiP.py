
print " ______   _____    _______                _______                   _       "
print "|  ____| |  __ \  |__   __|              |__   __|                 | |      "
print "| |__    | |__) |    | |       ______       | |      ___     ___   | |  ___ "
print "|  __|   |  ___/     | |      |______|      | |     / _ \   / _ \  | | / __|"
print "| |      | |         | |                    | |    | (_) | | (_) | | | \\__ \\"
print "|_|      |_|         |_|                    |_|     \___/   \___/  |_| |___/"
                                                                             
                                                                             


#   + IntersectPoint:
#       ++ KenhMuongL vs MatNuocTinh (Line vs Polygon)
#       ++ KenhMuongL vs SongSuoiA (Line vs Polygon)
#       ++ SongSuoiL vs MatNuocTinh (Line vs Polygon)
#       ++ SongSuoiL vs SongSuoiA (Line vs Polygon)
#       ++ SongSuoiL vs KenhMuongL (Line vs Line)
#       ++ DoanTimDuongBo vs SongSuoiL (Line vs Line)
#       ++ DoanTimDuongBo vs KenhMuongL (Line vs Line)
#       ++ DapL vs KenhMuongL
#       ++ DapL vs SongSuoiL
#   + IntersectLine:
#       ++ DoanTimDuongBo vs SuongSuoiA (Line vs Polygon)
#       ++ DoanTimDuongBo vs KenhMuongA (Line vs Polygon)
#       ++ DoanTimDuongBo vs MatNuocTinh (Line vs Polygon)

#- CongThuyLoiL:
#   + IntersectLine:
#       ++ DoanTimDuongBo vs SongSuoiA
#       ++ DoanTimDuongBo vs KenhMuongA
#       ++ DoanTimDuongBo vs MatNuocTinh

import arcpy
import os
import sys

class CongThuyLoiP:

    def __init__(self, distance):
        # Distance Snap
        self.distance = distance
        print "Distance: {}".format(distance)
        # Path GDB
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        # Feature DataSet Name
        self.fDThuyHe = "ThuyHe"
        self.fDGiaoThong = "GiaoThong"
        # Feature Class Name
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fCCongThuyLoiP = "CongThuyLoiP"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCSongSuoiL = "SongSuoiL"
        self.fCKenhMuongA = "KenhMuongA"
        self.fCKenhMuongL = "KenhMuongL"
        self.fCDapL = "DapL"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        # Path Feature Class
        ## Path Process
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCongThuyLoiPProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathKenhMuongLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathDapLProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDapL)
        self.pathDuongBoNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        ## Path Final
        self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        self.pathCongThuyLoiPFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCCongThuyLoiP)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathSongSuoiLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiL)
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathKenhMuongLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongL)
        self.pathDapLFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDapL)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        self.CopyFromProcessToFinal()
        self.CreateFeatureClassPointSnapA()
        self.SnapCongThuyLoiPVsPointSnapA()
        self.CreateFeatureClassPointSnapB()
        self.SnapCongThuyLoiPVsPointSnapB()
        self.DeleteCongThuyLoiP()
        pass

    def CopyFromProcessToFinal(self):
        print "Copy CongThuyLoiP From Process To Final"
        arcpy.CopyFeatures_management(in_features = self.pathCongThuyLoiPProcess,
                                      out_feature_class = self.pathCongThuyLoiPFinal)
        pass

    def CreateFeatureClassPointSnapA(self):
        print "CreateFeatureClassPointSnapA"
        # CreateFeatureclass self.pointSnapA
        self.pointSnapA = "in_memory\\PointSnapA"
        arcpy.CreateFeatureclass_management(out_path = "in_memory",
                                            out_name = "PointSnapA",
                                            geometry_type = "MULTIPOINT")
        # KenhMuongL vs MatNuocTinh (Line vs Polygon)
        self.IntersectAndInsertPointSnapA(self.pathKenhMuongLFinal, self.pathMatNuocTinhFinal)
        # KenhMuongL vs SongSuoiA (Line vs Polygon)
        self.IntersectAndInsertPointSnapA(self.pathKenhMuongLFinal, self.pathSongSuoiAFinal)
        # SongSuoiL vs MatNuocTinh (Line vs Polygon)
        self.IntersectAndInsertPointSnapA(self.pathSongSuoiLFinal, self.pathMatNuocTinhFinal)
        # SongSuoiL vs SongSuoiA (Line vs Polygon)
        self.IntersectAndInsertPointSnapA(self.pathSongSuoiLFinal, self.pathSongSuoiAFinal)
        # SongSuoiL vs KenhMuongL (Line vs Line)
        self.IntersectAndInsertPointSnapA(self.pathSongSuoiLFinal, self.pathKenhMuongLFinal)
        # DoanTimDuongBo vs SongSuoiL (Line vs Line)
        self.IntersectAndInsertPointSnapA(self.pathDoanTimDuongBoFinal, self.pathSongSuoiLFinal)
        # DoanTimDuongBo vs KenhMuongL (Line vs Line)
        self.IntersectAndInsertPointSnapA(self.pathDoanTimDuongBoFinal, self.pathKenhMuongLFinal)
        # DapL vs KenhMuongL
        self.IntersectAndInsertPointSnapA(self.pathDapLFinal, self.pathKenhMuongLFinal)
        # DapL vs SongSuoiL
        self.IntersectAndInsertPointSnapA(self.pathDapLFinal, self.pathSongSuoiLFinal)
        # CopyFeatures
        #arcpy.CopyFeatures_management(in_features = self.pointSnapA,
        #                              out_feature_class = os.path.join(self.pathDefaultGDB, "PointSnapA"))
        pass

    def SnapCongThuyLoiPVsPointSnapA(self):
        print "SnapCongThuyLoiPVsPointSnapA"
        snapEnv = [self.pointSnapA, "END", self.distance]
        arcpy.Snap_edit(in_features = self.pathCongThuyLoiPFinal,
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
        print "CreateFeatureClassPointSnapB"
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
        # DoanTimDuongBo vs SuongSuoiA Merge KenhMuongA (Line vs Polygon)
        outputMerge = "in_memory\\outputMerge"
        arcpy.Merge_management(inputs = [self.pathSongSuoiAFinal, self.pathKenhMuongAFinal],
                               output = outputMerge)
        self.InsertPointSnapB(outputMerge)
        # Copy Feature
        #arcpy.CopyFeatures_management(in_features = self.pointSnapB,
        #                              out_feature_class = os.path.join(self.pathDefaultGDB, "PointSnapB"))
        pass

    def SnapCongThuyLoiPVsPointSnapB(self):
        print "SnapCongThuyLoiPVsPointSnapB"
        # Make Feature Layer
        self.pointSnapALayer = "pointSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapA,
                                          out_layer = self.pointSnapALayer)
        self.congThuyLoiPFinalLayer = "congThuyLoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiPFinal,
                                          out_layer = self.congThuyLoiPFinalLayer)
        # Select
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        # Snap
        snapEnv = [self.pointSnapB, "END", self.distance]
        arcpy.Snap_edit(in_features = self.congThuyLoiPFinalLayer,
                        snap_environment = [snapEnv])
        pass

    def InsertPointSnapB(self, fCPolygon):
        ## Dissolve fCPolygon
        fCPolygonTemp = "in_memory\\fCPolygonTemp"
        arcpy.CopyFeatures_management(in_features = fCPolygon,
                                      out_feature_class = fCPolygonTemp)
        arcpy.AddField_management(in_table = fCPolygonTemp,
                                  field_name = "Dissolve",
                                  field_type = "Short")
        fCPolygonTempDissolve = "in_memory\\fCPolygonTempDissolve"
        arcpy.Dissolve_management(in_features = fCPolygonTemp,
                                  out_feature_class = fCPolygonTempDissolve,
                                  dissolve_field = "Dissolve")
        ## Feature To Line
        fCPolygonTempDissolveFeatureToLine = "in_memory\\fCPolygonTempDissolveFeatureToLine"
        arcpy.FeatureToLine_management(in_features = fCPolygonTempDissolve,
                                       out_feature_class = fCPolygonTempDissolveFeatureToLine)
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

    def DeleteCongThuyLoiP(self):
        print "DeleteCongThuyLoiP"
        # Make Feature Layer
        self.congThuyLoiPFinalLayer = "congThuyLoiPFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathCongThuyLoiPFinal,
                                          out_layer = self.congThuyLoiPFinalLayer)
        self.pointSnapALayer = "pointSnapALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapA,
                                          out_layer = self.pointSnapALayer)
        self.pointSnapBLayer = "pointSnapBLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pointSnapB,
                                          out_layer = self.pointSnapBLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapALayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.congThuyLoiPFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointSnapBLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION")
        arcpy.DeleteFeatures_management(in_features = self.congThuyLoiPFinalLayer)
        pass

if __name__ == "__main__":
    congThuyLoiP = CongThuyLoiP(sys.argv[1])
    congThuyLoiP.Execute()
    pass