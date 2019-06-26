import arcpy
import os
import sys

class DuongBoNuoc:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCBaiBoiA = "BaiBoiA"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        self.fCKenhMuongA = "KenhMuongA"
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathBaiBoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCBaiBoiA)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathBaiBoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCBaiBoiA)
        self.pathDuongBoNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongBoNuoc)

    def Execute(self):
        print "DuongBoNuoc:"
        self.CreateFeaturePointRemove()

    def CreateFeaturePointRemove(self):
        print "\tCreateFeaturePointRemove"
        # Using Merge Tool
        inputsMerge = [self.pathBaiBoiAFinal, self.pathMatNuocTinhFinal, self.pathSongSuoiAFinal, self.pathKenhMuongAFinal]
        self.outPutMergeTempA = "in_memory\\OutPutMergeTempA"
        arcpy.Merge_management(inputs = inputsMerge,
                               output = self.outPutMergeTempA)
        # Using Feature To Line
        self.outPutFeatureToLineTempA = "in_memory\\OutPutFeatureToLineTempA"
        arcpy.FeatureToLine_management(in_features = self.outPutMergeTempA,
                                       out_feature_class = self.outPutFeatureToLineTempA)
        # Using Merge Tool
        inputsMerge = [self.pathBaiBoiAProcess, self.pathMatNuocTinhProcess, self.pathSongSuoiAProcess, self.pathKenhMuongAProcess]
        outPutMergeTempB = "in_memory\\OutPutMergeTempB"
        arcpy.Merge_management(inputs = inputsMerge,
                               output = outPutMergeTempB)
        # Using Feature To Line
        outPutFeatureToLineTempB = "in_memory\\OutPutFeatureToLineTempB"
        arcpy.FeatureToLine_management(in_features = outPutMergeTempB,
                                       out_feature_class = outPutFeatureToLineTempB)
        # Using Feature Vertices To Points
        outPutFeatureVerticesToPointsTempA = "in_memory\\OutPutFeatureVerticesToPointsTempA"
        arcpy.FeatureVerticesToPoints_management(in_features = outPutFeatureToLineTempB,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempA,
                                                 point_location = "ALL")
        # Using Integrate
        inputsIntegrate = [[self.pathDuongBoNuocProcess, 1], [outPutFeatureVerticesToPointsTempA, 2]]
        arcpy.Integrate_management(in_features = inputsIntegrate,
                                   cluster_tolerance = "0 Meters")
        # Using Copy Feature
        arcpy.CopyFeatures_management(in_features = self.pathDuongBoNuocProcess,
                                      out_feature_class = self.pathDuongBoNuocFinal)
        # Using Feature Vertices To Points
        outPutFeatureVerticesToPointsTempB = "in_memory\\OutPutFeatureVerticesToPointsTempB"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongBoNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempB,
                                                 point_location = "ALL")
        outPutFeatureVerticesToPointsTempC = "in_memory\\OutPutFeatureVerticesToPointsTempC"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongBoNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempC,
                                                 point_location = "BOTH_ENDS")
        # Using Erase
        outPutEraseA = "in_memory\\OutPutEraseA"
        arcpy.Erase_analysis(in_features = outPutFeatureVerticesToPointsTempB,
                             erase_features = outPutFeatureVerticesToPointsTempC,
                             out_feature_class = outPutEraseA)
        # Using Select Feature Layer By Location
        self.outLayerTempA = "OutLayerTempA"
        arcpy.MakeFeatureLayer_management(in_features = self.outPutFeatureToLineTempA,
                                          out_layer = self.outLayerTempA)
        outLayerTempB = "OutLayerTempB"
        arcpy.MakeFeatureLayer_management(in_features = outPutEraseA,
                                          out_layer = outLayerTempB)
        arcpy.SelectLayerByLocation_management(in_layer = outLayerTempB,
                                               overlap_type = "INTERSECT",
                                               select_features = self.outLayerTempA,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        #self.duongBoNuocPointRemove = "in_memory\\DuongBoNuocPointRemove"
        self.duongBoNuocPointRemove = os.path.join(self.pathProcessGDB, "PointRemove")
        arcpy.CopyFeatures_management(in_features = outLayerTempB,
                                      out_feature_class = self.duongBoNuocPointRemove)
        pass


if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    duongBoNuoc = DuongBoNuoc()
    duongBoNuoc.Execute()