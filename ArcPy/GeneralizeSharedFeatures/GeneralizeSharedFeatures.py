# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class GeneralizeSharedFeatures:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDDiaHinh = "DiaHinh"
        self.fCDuongBinhDo = "DuongBinhDo"
        self.fDThuyHe = "ThuyHe"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        self.fCSongSuoiA = "SongSuoiA"
        self.pathDuongBinhDoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDDiaHinh), self.fCDuongBinhDo)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        pass

    def Execute(self):
        #
        duongBinhDoFinalLayer = "duongBinhDoFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongBinhDoFinal,
                                          out_layer = duongBinhDoFinalLayer)
        #songSuoiAFinalLayer = "songSuoiAFinalLayer"
        #arcpy.MakeFeatureLayer_management(in_features = self.pathSongSuoiAFinal,
        #                                  out_layer = songSuoiAFinalLayer)
        #duongBoNuocFinalLayer = "duongBoNuocFinalLayer"
        #arcpy.MakeFeatureLayer_management(in_features = self.pathDuongBoNuocFinal,
        #                                  out_layer = duongBoNuocFinalLayer)
        #
        #Generalize_Operation
        ##SIMPLIFY ?Runs Simplify only once on the line or polygon features.
        ##SMOOTH ?Runs Smooth only once on the line or polygon features.
        ##SIMPLIFY_SMOOTH ?Runs Simplify and Smooth once on the line or polygon features.
        ##SIMPLIFY_SMOOTH_SIMPLIFY ?Runs Simplify, Smooth, and Simplify on the line or polygon features.
        ##SIMPLIFY_SMOOTH_SIMPLIFY_SMOOTH ?Runs Simplify and Smooth twice on the line or polygon features in the order listed.
        #Simplification_Algorithm
        ##POINT_REMOVE ?Retains critical points that depict the essential shape of a line and removes all other points. This is the default.
        ##BEND_SIMPLIFY ?Retains the critical bends in a line and removes extraneous bends.
        #Smoothing_Algorithm
        ##PAEK ?Acronym for Polynominal Approximation with Exponential Kernel. It calculates a smoothed line that will not pass through the input line vertices. This is the default.
        ##BEZIER_INTERPOLATION ?Fits Bezier curves between vertices. The resulting line passes through the vertices of the input line. This algorithm does not require a tolerance. Bezier curves will be approximated when the output is a shapefile.

        arcpy.GeneralizeSharedFeatures_production(Input_Features = duongBinhDoFinalLayer,
                                                  Generalize_Operation = "SIMPLIFY",
                                                  Simplify_Tolerance = "50 Meters",
                                                  #Smooth_Tolerance = "50 Meters",
                                                  Topology_Feature_Classes = [],
                                                  Simplification_Algorithm = "BEND_SIMPLIFY")
                                                  #Smoothing_Algorithm = "PAEK")
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
    generalizeSharedFeatures = GeneralizeSharedFeatures()
    print "Running..."
    generalizeSharedFeatures.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass