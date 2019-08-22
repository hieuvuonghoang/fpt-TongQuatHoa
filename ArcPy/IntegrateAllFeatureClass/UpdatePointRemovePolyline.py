# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class UpdatePointRemovePolyline:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfigTopo = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigTopo.json")
        # Read File Config Process Topo
        if not os.path.isfile(self.pathFileConfigTopo):
            print "... Not Found: " + self.pathFileConfigTopo + "?\n  ... Create File ConfigTopo..."
            self.CreateFileConfigTopo()
        self.ReadFileConfigTopo()
        pass

    def Execute(self):
        # Init Workspace
        arcpy.env.overwriteOutput = True

        ## CreateFeaturePointRemoveOne
        #print "# CreateFeaturePointRemoveOne"
        #self.ProcessFeatureClassPointRemove()
        #pathFc = os.path.join(os.path.join(self.pathProcessGDB, "ThuyHe"), "DuongBoNuoc_PointRemove")
        #pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, "ThuyHe"), "DuongBoNuoc_PointRemove_Dissolve")
        #print pathDissolve
        #arcpy.Dissolve_management(in_features = pathFc,
        #                          out_feature_class = pathDissolve,
        #                          dissolve_field = ["FID_DuongBoNuoc"])
        pass

    def ProcessFeatureClassPointRemove(self):
        for elemConfigTopo in self.configTopoTools.listConfig:
            featureDataSetPolyLine = elemConfigTopo.featureDataSet
            for elemPolyline in elemConfigTopo.listPolyline:
                featureClassPolyLine = FeatureClass(elemPolyline.featureClass)
                for elemPolygonTopo in elemPolyline.polygonTopos:
                    featureDataSetPolygon = elemPolygonTopo.featureDataSet
                    for elemPolygon in elemPolygonTopo.listPolygon:
                        featureClassPolygon = FeatureClass(elemPolygon.featureClass)
                        if elemPolygon.processTopo == True:
                            featureClassPolyLine.SetFeatureClassPointRemove()
                            inPathFC = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemove)
                            fCTemp = "in_memory\\fCTemp"
                            arcpy.CopyFeatures_management(in_features = inPathFC,
                                                          out_feature_class = fCTemp)
                            self.ProcessFeatureClassPointRemoveSubOne(featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp)
                            self.ProcessFeatureClassPointRemoveSubTwo(featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp)
                            featureClassPolyLine.SetFeatureClassPointRemoveDissolve()
                            outputDissolve = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetPolyLine), featureClassPolyLine.featureClassPointRemoveDissolve)
                            fieldName = self.GetFieldFID(featureClassPolyLine.featureClass)
                            self.Dissolve(fCTemp, outputDissolve, fieldName)
                            arcpy.Delete_management("in_memory")
                            pass
        pass

    def Dissolve(self, fCTemp, outputDissolve, dissolveField):
        arcpy.Dissolve_management(in_features = fCTemp,
                                  out_feature_class = outputDissolve,
                                  dissolve_field = [dissolveField])
        pass

    # Xu ly nhung Point ma PolyLine da Remove, nhung de du quan he Topo voi Polygon thi nhung Point do can duoc giu lai
    def ProcessFeatureClassPointRemoveSubOne(self, featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp):
        # Make Feature Layer
        featureClassPolygon.SetFeatureClassSimplify()
        inFCPolygonSimplify = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolygon, featureClassPolygon.featureClassSimplify))
        inFCPolygonSimplifyLayer = "inFCPolygonSimplifyLayer"
        #print inFCPolygonSimplify
        arcpy.MakeFeatureLayer_management(in_features = inFCPolygonSimplify,
                                          out_layer = inFCPolygonSimplifyLayer)
        featureClassPolyLine.SetFeatureClassPointRemove()
        inFCPolylinePointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassPointRemove))
        inFCPolylinePointRemoveLayer = "inFCPolylinePointRemoveLayer"
        #print inFCPolylinePointRemove
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylinePointRemove,
                                          out_layer = inFCPolylinePointRemoveLayer)
        # Polygon To Polyline
        outFCPolygonToPolyline = "in_memory\\outFCPolygonToPolyline"
        #arcpy.FeatureToLine_management(in_features = inFCPolygonSimplifyLayer,
        #                               out_feature_class = outFCPolygonToPolyline,
        #                               cluster_tolerance = "0 Meters")
        arcpy.PolygonToLine_management(in_features = inFCPolygonSimplifyLayer,
                                       out_feature_class = outFCPolygonToPolyline)
        # Make Feature Layer
        outFCPolygonToPolylineLayer = "outFCPolygonToPolylineLayer"
        arcpy.MakeFeatureLayer_management(in_features = outFCPolygonToPolyline,
                                          out_layer = outFCPolygonToPolylineLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolylinePointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outFCPolygonToPolylineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Copy Feature Class
        outFCCopy = "in_memory\\outFCCopy"
        arcpy.CopyFeatures_management(in_features = inFCPolylinePointRemoveLayer,
                                      out_feature_class = outFCCopy)
        # Erase
        featureClassPolyLine.SetFeatureClassPointRemoveOne()
        outErase = "in_memory\\outErase"
        arcpy.Erase_analysis(in_features = inFCPolylinePointRemove,
                             erase_features = outFCCopy,
                             out_feature_class = outErase)
        # Copy Override
        arcpy.CopyFeatures_management(in_features = outErase,
                                      out_feature_class = fCTemp)
        pass

    # Xu ly nhung Point ma Polyline da khong Remove, nhung de du quan he Topo voi Polygon thi nhung Point do can duoc Remove
    def ProcessFeatureClassPointRemoveSubTwo(self, featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine, fCTemp):
        # Make Feature Layer
        featureClassPolyLine.SetFeatureClassSimplify()
        inFCPolylineSimplify = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassSimplify))
        inFCPolylineSimplifyLayer = "inFCPolylineSimplifyLayer"
        #print inFCPolylineSimplify
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylineSimplify,
                                          out_layer = inFCPolylineSimplifyLayer)
        featureClassPolygon.SetFeatureClassPointRemove()
        inFCPolygonPointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolygon, featureClassPolygon.featureClassPointRemove))
        inFCPolygonPointRemoveLayer = "inFCPolygonPointRemoveLayer"
        #print inFCPolygonPointRemove
        arcpy.MakeFeatureLayer_management(in_features = inFCPolygonPointRemove,
                                          out_layer = inFCPolygonPointRemoveLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolygonPointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = inFCPolylineSimplifyLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Copy Feature Class
        outFCCopy = "in_memory\\outFCCopy"
        arcpy.CopyFeatures_management(in_features = inFCPolygonPointRemoveLayer,
                                      out_feature_class = outFCCopy)
        # Make Feature Layer
        outFCCopyLayer = "outFCCopyLayer"
        arcpy.MakeFeatureLayer_management(in_features = outFCCopy,
                                          out_layer = outFCCopyLayer)
        featureClassPolyLine.SetFeatureClassSimplifyAllPoint()
        inFCPolylineSimplifyAllPoint = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassSimplifyAllPoint))
        inFCPolylineSimplifyAllPointLayer = "inFCPolylineSimplifyAllPointLayer"
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylineSimplifyAllPoint,
                                          out_layer = inFCPolylineSimplifyAllPointLayer)
        # Select Feature
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolylineSimplifyAllPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outFCCopyLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        # Insert Cursor
        fieldName = self.GetFieldFID(featureClassPolyLine.featureClass)
        with arcpy.da.SearchCursor(inFCPolylineSimplifyAllPointLayer, ["Shape@", fieldName]) as cursorA:
            with arcpy.da.InsertCursor(fCTemp, ["Shape@", fieldName]) as cursorB:
                for rowA in cursorA:
                    cursorB.insertRow((rowA[0], rowA[1]))
        pass

    def GetFieldFID(self, featureClass):
        return "FID_" + featureClass, fieldType
        pass

    def CreateFileConfigTopo(self):
        arrTemp = []
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemConfigTopoC = ElemConfigTopoC(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemConfigTopoD = ElemConfigTopoD(fcTemp.baseName, False)
                    elemConfigTopoC.InsertElemListPolygon(elemConfigTopoD)
            if elemConfigTopoC.GetLength() > 0:
                arrTemp.append(elemConfigTopoC)

        configTopoTools = ConfigTopoTools()
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemConfigTopoA = ElemConfigTopoA(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    elemConfigTopoB = ElemConfigTopoB(fcTemp.baseName)
                    for itemTemp in arrTemp:
                        elemConfigTopoB.InsertElemListPolygon(itemTemp)
                    if elemConfigTopoB.GetLength() > 1:
                        elemConfigTopoA.InsertElemListPolyline(elemConfigTopoB)
            if elemConfigTopoA.GetLength() > 1:
                configTopoTools.InsertElemListConfig(elemConfigTopoA)

        textConfig = json.dumps(obj = configTopoTools.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileConfigTopo, "w")
        file.write(textConfig)
        file.close()
        pass

    def ReadFileConfigTopo(self):
        self.configTopoTools = ConfigTopoTools()
        file = open(self.pathFileConfigTopo, "r")
        textConfig = file.read()
        file.close()
        self.configTopoTools.InitFromDict(json.loads(textConfig))
        pass

class ConfigTopoTools:

    def __init__(self):
        self.listConfig = []

    def InsertElemListConfig(self, elemListConfig):
        self.listConfig.append(elemListConfig)

    def GetLength(self):
        return len(self.listConfig)
        pass

    def GetDict(self):
        listTemp = []
        for elemListConfig in self.listConfig:
            listTemp.append(elemListConfig.GetDict())
        return listTemp;

    def InitFromDict(self, dataJson):
        self.listConfig = []
        for elemListConfigTemp in dataJson:
            elemConfigTopoA = ElemConfigTopoA(elemListConfigTemp['featureDataSet'])
            for elemListPolylineTemp in elemListConfigTemp['listPolyline']:
                elemConfigTopoB = ElemConfigTopoB(elemListPolylineTemp['featureClass'])
                for elemListPolygonTopoTemp in elemListPolylineTemp['polygonTopos']:
                    elemConfigTopoC = ElemConfigTopoC(elemListPolygonTopoTemp['featureDataSet'])
                    for elemListPolygonTemp in elemListPolygonTopoTemp['listPolygon']:
                        elemConfigTopoD = ElemConfigTopoD(elemListPolygonTemp['featureClass'], elemListPolygonTemp['processTopo'])
                        elemConfigTopoC.InsertElemListPolygon(elemConfigTopoD)
                    elemConfigTopoB.InsertElemListPolygon(elemConfigTopoC)
                elemConfigTopoA.InsertElemListPolyline(elemConfigTopoB)
            self.InsertElemListConfig(elemConfigTopoA)

# Elem of ConfigTopoTools.listConfig
class ElemConfigTopoA:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolyline = []
        pass

    def InsertElemListPolyline(self, elemListPolyline):
        self.listPolyline.append(elemListPolyline)

    def GetLength(self):
        return len(self.listPolyline)
        pass

    def GetDict(self):
        listTempPolyline = []
        for elemList in self.listPolyline:
            listTempPolyline.append(elemList.GetDict())
        return {
            "featureDataSet": self.featureDataSet,
            "listPolyline": listTempPolyline
        }

# Elem of ElemConfigTopoA.listPolyline
class ElemConfigTopoB:

    def __init__(self, featureClass):
        self.featureClass = featureClass
        self.polygonTopos = []
        pass

    def InsertElemListPolygon(self, polygonTopo):
        self.polygonTopos.append(polygonTopo)
    
    def GetLength(self):
        return len(self.polygonTopos)
        pass

    def GetDict(self):
        listTempPolygon = []
        for elemList in self.polygonTopos:
            listTempPolygon.append(elemList.GetDict())
        return {
            "featureClass": self.featureClass,
            "polygonTopos": listTempPolygon
        }

# Elem of ElemConfigTopoB.listPolygon
class ElemConfigTopoC:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolygon = []
        pass

    def SetFeatureDataSet(self, featureDataSet):
        self.featureDataSet = featureDataSet
        pass

    def InsertElemListPolygon(self, elemListPolygon):
        self.listPolygon.append(elemListPolygon)

    def GetLength(self):
        return len(self.listPolygon)
        pass

    def GetDict(self):
        listTempPolygon = []
        for elemList in self.listPolygon:
            listTempPolygon.append(elemList.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolygon": listTempPolygon
        }

# Elem of ElemConfigTopoC.listPolygon
class ElemConfigTopoD:

    def __init__(self, featureClass, processTopo):
        self.featureClass = featureClass
        self.processTopo = processTopo
        pass
    
    def SetFeatureClassInMemory(self):
        self.featureClassInMemory = "in_memory\\" + self.featureClass
        pass

    def SetFeatureLayer(self):
        self.featureLayer = self.featureClass + "Layer"
        pass

    def SetFeatureClassAllPoint(self):
        self.featureClassAllPoint = self.featureClass + "_AllPoint"
        pass

    def SetFeatureClassSimplify(self):
        self.featureClassSimplify = self.featureClass + "_Simplify"
        pass

    def SetFeatureClassSimplifyAllPoint(self):
        self.featureClassSimplifyAllPoint = self.featureClass + "_Simplify_AllPoint"
        pass

    def SetFeatureClassPointRemove(self):
        self.featureClassPointRemove = self.featureClass + "_PointRemove"
        pass

    def SetFeatureClassPointRemoveDissolve(self):
        self.featureClassPointRemoveDissolve = self.featureClass + "_PointRemove_Dissolve"
        pass

class FeatureClass:

    def __init__(self, featureClass):
        self.featureClass = featureClass
        pass
    
    def SetFeatureClassInMemory(self):
        self.featureClassInMemory = "in_memory\\" + self.featureClass
        pass

    def SetFeatureLayer(self):
        self.featureLayer = self.featureClass + "Layer"
        pass

    def SetFeatureClassAllPoint(self):
        self.featureClassAllPoint = self.featureClass + "_AllPoint"
        pass

    def SetFeatureClassSimplify(self):
        self.featureClassSimplify = self.featureClass + "_Simplify"
        pass

    def SetFeatureClassSimplifyAllPoint(self):
        self.featureClassSimplifyAllPoint = self.featureClass + "_Simplify_AllPoint"
        pass

    def SetFeatureClassPointRemove(self):
        self.featureClassPointRemove = self.featureClass + "_PointRemove"
        pass

    def SetFeatureClassPointRemoveDissolve(self):
        self.featureClassPointRemoveDissolve = self.featureClass + "_PointRemove_Dissolve"
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
    updatePointRemovePolyline = UpdatePointRemovePolyline()
    print "Running..."
    updatePointRemovePolyline.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass