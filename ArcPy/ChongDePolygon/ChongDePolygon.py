# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import arcpy
import datetime

class ChongDePolygon:

    def __init__(self, pathFeature, pathFeatureClass):
        self.pathFeature = pathFeature
        self.pathFeatureClass = pathFeatureClass
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        readFileGeometry_Feature = ReadFileGeometry(self.pathFeature)
        readFileGeometry_FeatureClass = ReadFileGeometry(self.pathFeatureClass)
        createFeaturePolygonFromGeometry_Feature = CreateFeaturePolygonFromGeometry(readFileGeometry_Feature.dataJson, "Feature")
        createFeaturePolygonFromGeometry_FeatureClass = CreateFeaturePolygonFromGeometry(readFileGeometry_FeatureClass.dataJson, "FeatureClass")
        self.outPutIntersect = "in_memory\\outPutIntersect"
        arcpy.Intersect_analysis(in_features = [createFeaturePolygonFromGeometry_Feature.pathFeatureClass, createFeaturePolygonFromGeometry_FeatureClass.pathFeatureClass],
                                 out_feature_class = self.outPutIntersect)
        self.outPutErase = "in_memory\\outPutErase"
        arcpy.Erase_analysis(in_features = createFeaturePolygonFromGeometry_Feature.pathFeatureClass,
                             erase_features = self.outPutIntersect,
                             out_feature_class = self.outPutErase)
        self.outPutMultipartToSinglepart = "in_memory\\outPutMultipartToSinglepart"
        arcpy.MultipartToSinglepart_management(in_features = self.outPutErase,
                                               out_feature_class = self.outPutMultipartToSinglepart)
        arcpy.CreateFeatureclass_management(out_path = r"C:\Users\vuong\Documents\ArcGIS\Default.gdb", out_name = "PolygonOut", geometry_type = "POLYGON")
        with arcpy.da.SearchCursor(self.outPutIntersect, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(r"C:\Users\vuong\Documents\ArcGIS\Default.gdb\PolygonOut", ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0],))
        with arcpy.da.SearchCursor(self.outPutMultipartToSinglepart, ["Shape@"]) as sCur:
            with arcpy.da.InsertCursor(r"C:\Users\vuong\Documents\ArcGIS\Default.gdb\PolygonOut", ["Shape@"]) as iCur:
                for row in sCur:
                    iCur.insertRow((row[0],))
        pass

class ReadFileGeometry:

    def __init__(self, pathFile):
        self.pathFile = pathFile
        file = open(self.pathFile, "r")
        textConfig = file.read()
        file.close()
        self.dataJson = json.loads(textConfig)
        pass


class CreateFeaturePolygonFromGeometry:

    def __init__(self, dataJson, featureClassName):
        self.dataJson = dataJson
        self.featureClassName = featureClassName
        self.pathDefaultGDB = r"C:\Users\vuong\Documents\ArcGIS\Default.gdb"
        self.pathFeatureClass = os.path.join(self.pathDefaultGDB, self.featureClassName)
        featureArcgis = []
        for featureTemp in self.dataJson:
            arrayPart = arcpy.Array()
            for ringTemp in featureTemp["rings"]:
                arrayPoint = arcpy.Array()
                for pointTemp in ringTemp:
                    pnt = arcpy.Point(pointTemp[0], pointTemp[1])
                    arrayPoint.add(pnt)
                arrayPart.add(arrayPoint)
            featureArcgis.append(arcpy.Polygon(arrayPart))
        arcpy.CopyFeatures_management(featureArcgis, self.pathFeatureClass)
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
    chongDePolygon = ChongDePolygon(sys.argv[1], sys.argv[2])
    print "Running..."
    chongDePolygon.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass