# -*- coding: utf-8 -*-
import os
import sys
import time
import arcpy
import datetime
import subprocess

class DuongBoNuoc:

    def __init__(self, distanceSnap):
        self.distanceSnap = distanceSnap
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
        arcpy.env.overwriteOutput = True
        self.CreateFeaturePointRemove()
        self.RemovePoint()
        self.SelectLineSnap()
        self.SnapDuongBoNuoc()

    def CreateFeaturePointRemove(self):
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
        self.duongBoNuocPointRemoveName = "DuongBoNuocPointRemove"
        self.duongBoNuocPointRemove = os.path.join(self.pathProcessGDB, self.duongBoNuocPointRemoveName)
        arcpy.CopyFeatures_management(in_features = outLayerTempB,
                                      out_feature_class = self.duongBoNuocPointRemove)

    def RemovePoint(self):
        subprocess.call(["RemovePointOnLine.exe", r"C:\Generalize_25_50\50K_Final.gdb", "", "DuongBoNuoc", r"C:\Generalize_25_50\50K_Process.gdb", self.duongBoNuocPointRemoveName])
        pass

    def SelectLineSnap(self):
        outPutFeatureVerticesToPointsTempC = "in_memory\\OutPutFeatureVerticesToPointsTempC"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongBoNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempC,
                                                 point_location = "BOTH_ENDS")
        outLayerTemp = "OutPutFeatureVerticesToPointsTempCLayer"
        arcpy.MakeFeatureLayer_management(in_features = outPutFeatureVerticesToPointsTempC,
                                          out_layer = outLayerTemp)
        self.duongBoNuocLayer = "duongBoNuocLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongBoNuocFinal,
                                          out_layer = self.duongBoNuocLayer)
        arcpy.SelectLayerByLocation_management(in_layer = outLayerTemp,
                                               overlap_type = "INTERSECT",
                                               select_features = self.outLayerTempA,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.duongBoNuocLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outLayerTemp,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        pass

    def SnapDuongBoNuoc(self):
        outPutFeatureToLineTempALayer = "outPutFeatureToLineTempALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.outPutFeatureToLineTempA,
                                          out_layer = outPutFeatureToLineTempALayer)
        snapEnv = [outPutFeatureToLineTempALayer, "EDGE", self.distanceSnap]
        arcpy.Snap_edit(self.duongBoNuocLayer, [snapEnv])
        #with arcpy.da.UpdateCursor(self.duongBoNuocLayer, ["OID@", "SHAPE@"]) as cursorA:
        #    for rowA in cursorA:
        #        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongBoNuocLayer,
        #                                                selection_type = "NEW_SELECTION",
        #                                                where_clause = "OBJECTID = " + str(rowA[0]))
        #        arcpy.Snap_edit(self.duongBoNuocLayer, [snapEnv])
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
    duongBoNuoc = DuongBoNuoc(sys.argv[1])
    print "Running..."
    duongBoNuoc.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass