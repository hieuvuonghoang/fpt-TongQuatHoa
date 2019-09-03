#C:\Users\vuong\AppData\Local\Temp\scratch.gdb\GenShareFDS_140826
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import ctypes
import datetime

class SimplifyProduction:

    def __init__(self):
        #
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfigPolygon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigPolygon.json")
        self.pathFileConfigPolyline = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigPolyline.json")
        self.pathFileGSFPolygons = os.path.join(os.path.dirname(os.path.realpath(__file__)), "GeneralizeSharedFeaturesPolygons.json")
        #
        self.configToolPolyline = ConfigToolPolyline()
        self.configToolPolygon = ConfigToolPolygon()
        # Read File Config
        #if not os.path.isfile(self.pathFileConfigPolyline):
        #    print "... Not Found: " + self.pathFileConfigPolyline
        #    #self.CreateFileConfig()
        #self.configToolPolyline.InitFromDict(self.ReadFileConfig(self.pathFileConfigPolyline))
        # Read File Config
        if not os.path.isfile(self.pathFileGSFPolygons):
            print "... Not Found: " + self.pathFileGSFPolygons
            #self.CreateFileConfig()
        self.configToolPolygon.InitFromDict(self.ReadFileConfig(self.pathFileGSFPolygons))
        print "OK"
        pass

    def Execute(self):
        #arcpy.env.workspace = self.pathFinalGDB
        arcpy.env.overwriteOutput = True
        ## Integrate
        #ctypes.windll.kernel32.SetConsoleTitleA("Integrate ProcessGDB")
        #arrPolygon, arrPolyline = self.ReadAllPolygonAllPolylineInGDB(self.pathProcessGDB)
        #self.Integrate(arrPolygon, arrPolyline)
        #self.Integrate(arrPolyline, arrPolygon)
        #ctypes.windll.kernel32.SetConsoleTitleA("Integrate FinalGDB")
        #arrPolygon, arrPolyline = self.ReadAllPolygonAllPolylineInGDB(self.pathFinalGDB)
        #self.Integrate(arrPolygon, arrPolyline)
        #self.Integrate(arrPolyline, arrPolygon)
        #os.system('cls')
        # Generalize Shared Features Polygons
        ctypes.windll.kernel32.SetConsoleTitleA("Generalize Shared Features Polygons")
        self.GeneralizeSharedFeaturesPolygon()
        arcpy.Delete_management("in_memory")
        os.system('cls')
        # Generalize Shared Features Polylines
        #ctypes.windll.kernel32.SetConsoleTitleA("Generalize Shared Features Polylines")
        #self.CreateFeaturePoint()
        #self.GeneralizeSharedFeaturesPolyline()
        #arcpy.Delete_management("in_memory")
        #self.CreateFeaturePointRemove()
        #os.system('cls')
        pass
    
    def CreateFeaturePointRemove(self):
        pathPointTemp = os.path.join(self.pathProcessGDB, "PointTemp")
        pathPointTempLayer = "pathPointTempLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathPointTemp,
                                          out_layer = pathPointTempLayer)
        for featureDataSetTemp in self.configToolPolyline.listConfigTools:
            if len(featureDataSetTemp.listPolyline) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolyline:
                if featureClassTemp.runSimplify == False:
                    continue
                featureClass = FeatureClass(featureClassTemp.featureClass)
                featureClass.SetFeatureCloneA()
                pathPolyline = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClass.featureClass)
                pathPolylineA = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClass.featureClassCloneA)
                if not arcpy.Exists(pathPolylineA) or int(arcpy.GetCount_management(pathPolylineA).getOutput(0)) == 0:
                    continue
                pathPolylineALayer = "pathPolylineALayer"
                arcpy.MakeFeatureLayer_management(in_features = pathPolylineA,
                                                  out_layer = pathPolylineALayer)
                pathPolylineAllPoint = "in_memory\\pathPolylineAllPoint"
                arcpy.FeatureVerticesToPoints_management(in_features = pathPolyline,
                                                         out_feature_class = pathPolylineAllPoint,
                                                         point_location = "ALL")
                arcpy.SelectLayerByLocation_management(in_layer = pathPolylineAllPoint,
                                                       overlap_type = "INTERSECT",
                                                       select_features = pathPolylineALayer,
                                                       search_distance = "0 Meters",
                                                       invert_spatial_relationship = "INVERT")
                arcpy.SelectLayerByLocation_management(in_layer = pathPolylineAllPoint,
                                                       overlap_type = "INTERSECT",
                                                       select_features = pathPointTemp,
                                                       search_distance = "0 Meters",
                                                       selection_type = "REMOVE_FROM_SELECTION")
                featureClass.SetFeatureClassPointRemove()
                arcpy.CopyFeatures_management(in_features = pathPolylineAllPoint,
                                              out_feature_class = os.path.join(self.pathProcessGDB, featureClass.featureClassPointRemove))
        pass

    def GeneralizeSharedFeaturesPolygon(self):
        for featureDataSetTemp in self.configToolPolygon.listConfigTools:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False:
                    continue
                pathPolygon = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                if not arcpy.Exists(pathPolygon) or int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
                    continue
                print "\n# Simplify: {}".format(str(os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)))
                arrPolygon = self.GetArrPolygon(featureClassTemp.featureClass)
                print "# ListTopo:"
                for polygon in arrPolygon:
                    print "   # {}".format(str(polygon))
                arcpy.GeneralizeSharedFeatures_production(Input_Features = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass),
                                                          Generalize_Operation = "SIMPLIFY",
                                                          Simplify_Tolerance = "50 Meters",
                                                          Topology_Feature_Classes = arrPolygon,
                                                          Simplification_Algorithm = "BEND_SIMPLIFY")
        pass

    def GeneralizeSharedFeaturesPolyline(self):
        for featureDataSetTemp in self.configToolPolyline.listConfigTools:
            if len(featureDataSetTemp.listPolyline) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolyline:
                if featureClassTemp.runSimplify == False:
                    continue
                featureClass = FeatureClass(featureClassTemp.featureClass)
                featureClass.SetFeatureCloneA()
                pathPolyline = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClass.featureClassCloneA)
                if not arcpy.Exists(pathPolyline) or int(arcpy.GetCount_management(pathPolyline).getOutput(0)) == 0:
                    continue
                print "\n# Simplify: {}".format(str(pathPolyline))
                arrPolyline = self.GetArrPolylineB(featureClass.featureClass)
                print "# ListTopo:"
                for polyline in arrPolyline:
                    print "   # {}".format(str(polyline))
                arcpy.GeneralizeSharedFeatures_production(Input_Features = pathPolyline,
                                                          Generalize_Operation = "SIMPLIFY",
                                                          Simplify_Tolerance = "50 Meters",
                                                          Topology_Feature_Classes = arrPolyline,
                                                          Simplification_Algorithm = "BEND_SIMPLIFY")
        pass

    def GetArrPolygon(self, differentPolygon):
        arrPolygon = []
        for featureDataSetTemp in self.configToolPolygon.listConfigTools:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolygon:
                if featureClassTemp.runSimplify == False or featureClassTemp.featureClass == differentPolygon:
                    continue
                pathPolygon = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                if not arcpy.Exists(pathPolygon) or int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
                    continue
                arrPolygon.append(pathPolygon)
        return arrPolygon
        pass

    def GetArrPolyline(self):
        arrPolyline = []
        for featureDataSetTemp in self.configToolPolyline.listConfigTools:
            if len(featureDataSetTemp.listPolyline) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolyline:
                if featureClassTemp.processTopo == False:
                    continue
                pathPolyline = os.path.join(os.path.join(self.pathFinalGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                if not arcpy.Exists(pathPolyline) or int(arcpy.GetCount_management(pathPolyline).getOutput(0)) == 0:
                    continue
                arrPolyline.append(pathPolyline)
        return arrPolyline
        pass

    def GetArrPolylineB(self, differentPolygon):
        arrPolyline = []
        for featureDataSetTemp in self.configToolPolyline.listConfigTools:
            if len(featureDataSetTemp.listPolyline) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolyline:
                if featureClassTemp.runSimplify == False or featureClassTemp.featureClass == differentPolygon:
                    continue
                featureClass = FeatureClass(featureClassTemp.featureClass)
                featureClass.SetFeatureCloneA()
                pathPolyline = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClass.featureClassCloneA)
                if not arcpy.Exists(pathPolyline) or int(arcpy.GetCount_management(pathPolyline).getOutput(0)) == 0:
                    continue
                arrPolyline.append(pathPolyline)
        return arrPolyline
        pass

    def CreateFeaturePoint(self):
        allPolygon = self.MergePolygon()
        allPolygonPoint = "in_memory\\allPolygonPoint"
        arcpy.FeatureVerticesToPoints_management(in_features = allPolygon,
                                                 out_feature_class = allPolygonPoint,
                                                 point_location = "ALL")
        allPolygonPointLayer = "allPolygonPointLayer"
        arcpy.MakeFeatureLayer_management(in_features = allPolygonPoint,
                                          out_layer = allPolygonPointLayer)
        allPolyline = self.MergePolyline()
        allPolylineLayer = "allPolylineLayer"
        arcpy.MakeFeatureLayer_management(in_features = allPolyline,
                                          out_layer = allPolylineLayer)
        arcpy.SelectLayerByLocation_management(in_layer = allPolygonPointLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = allPolylineLayer,
                                               search_distance = "0 Meters")
        arcpy.CopyFeatures_management(in_features = allPolygonPointLayer,
                                      out_feature_class = os.path.join(self.pathProcessGDB, "PointTemp"))
        pass

    def MakeFeatureLayer(self, pathGDB):
        arrLayerPolygon = []
        arrLayerPolyline = []
        # Polygon
        for tempConfig in self.configToolPolygon.listConfigTools:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runSimplify == False:
                    continue
                featureClass = FeatureClass(tempPolygon.featureClass)
                featureClass.SetFeatureLayer()
                pathPolygon = os.path.join(pathGDB, os.path.join(tempConfig.featureDataSet, featureClass.featureClass))
                if not arcpy.Exists(pathPolygon) or int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
                    continue
                arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                                  out_layer = featureClass.featureLayer)
                arrLayerPolygon.append(featureClass.featureLayer)
        # Polyline
        
        return arrLayerPolygon, arrLayerPolyline
        pass

    def ReadAllPolygonAllPolylineInGDB(self, pathGDB):
        arrPolygon = []
        arrPolyline = []
        for fcDataSetTemp in arcpy.Describe(pathGDB).children:
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    pathPolyline = os.path.join(os.path.join(pathGDB, fcDataSetTemp.baseName), fcTemp.baseName)
                    if int(arcpy.GetCount_management(pathPolyline).getOutput(0)) == 0:
                        continue
                    arrPolyline.append(pathPolyline)
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    pathPolygon = os.path.join(os.path.join(pathGDB, fcDataSetTemp.baseName), fcTemp.baseName)
                    if int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
                        continue
                    arrPolygon.append(pathPolyline)
        return arrPolygon, arrPolyline
        pass

    def Integrate(self, arrOne, arrTwo):
        arrInput = []
        for item in arrOne:
            arrInput.append([item, "1"])
        for item in arrTwo:
            arrInput.append([item, "2"])
        arcpy.Integrate_management(in_features = arrInput,
                                   cluster_tolerance = "0 Meters")
        pass

    def MergePolygon(self):
        print "# Merge Polygon"
        inFeatureClassMerges = []
        for featureDataSetTemp in self.configToolPolygon.listConfigTools:
            if len(featureDataSetTemp.listPolygon) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolygon:
                # Add Field FID_XXX For Feature Class
                if featureClassTemp.runSimplify == False:
                    continue
                pathPolygon = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                if not arcpy.Exists(pathPolygon) or int(arcpy.GetCount_management(pathPolygon).getOutput(0)) == 0:
                    continue
                featureClass = FeatureClass(featureClassTemp.featureClass)
                print "   # {0}".format(pathPolygon)
                fieldFID, fieldType = self.GetFieldFID(featureClassTemp.featureClass, "LONG")
                arcpy.AddField_management(pathPolygon, fieldFID, fieldType)
                # Update Field FID_XXX
                with arcpy.da.UpdateCursor(pathPolygon, ['OID@', fieldFID]) as cursor:
                    for row in cursor:
                        row[1] = row[0]
                        cursor.updateRow(row)
                # Copy FeatureClass to in_memory
                featureClass.SetFeatureClassInMemory()
                arcpy.CopyFeatures_management(in_features = pathPolygon,
                                              out_feature_class = featureClass.featureClassInMemory)
                # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                fields = arcpy.ListFields(featureClass.featureClassInMemory)
                fieldsDelete = []
                for fieldTemp in fields:
                    if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                        fieldsDelete.append(fieldTemp.name)
                arcpy.DeleteField_management(in_table = featureClass.featureClassInMemory,
                                             drop_field = fieldsDelete)
                # FeatureClass Delete Field FID_XXX
                arcpy.DeleteField_management(in_table = pathPolygon,
                                             drop_field = fieldFID)
                # Maker Layer
                inFeatureClassMerges.append(featureClass.featureClassInMemory)
        outputMerge = "in_memory\\FeatureClassPolygonMerge"
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = outputMerge)
        return outputMerge
        pass

    def MergePolyline(self):
        print "# Merge Polyline"
        inFeatureClassMerges = []
        for featureDataSetTemp in self.configToolPolyline.listConfigTools:
            if len(featureDataSetTemp.listPolyline) == 0:
                continue
            for featureClassTemp in featureDataSetTemp.listPolyline:
                # Add Field FID_XXX For Feature Class
                if featureClassTemp.runSimplify == False:
                    continue
                pathPolyline = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClassTemp.featureClass)
                if not arcpy.Exists(pathPolyline) or int(arcpy.GetCount_management(pathPolyline).getOutput(0)) == 0:
                    continue
                featureClass = FeatureClass(featureClassTemp.featureClass)
                print "   # {0}".format(pathPolyline)
                fieldFID, fieldType = self.GetFieldFID(featureClassTemp.featureClass, "LONG")
                arcpy.AddField_management(pathPolyline, fieldFID, fieldType)
                # Update Field FID_XXX
                with arcpy.da.UpdateCursor(pathPolyline, ['OID@', fieldFID]) as cursor:
                    for row in cursor:
                        row[1] = row[0]
                        cursor.updateRow(row)
                # Copy FeatureClass to in_memory
                featureClass.SetFeatureClassInMemory()
                arcpy.CopyFeatures_management(in_features = pathPolyline,
                                              out_feature_class = featureClass.featureClassInMemory)
                # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                fields = arcpy.ListFields(featureClass.featureClassInMemory)
                fieldsDelete = []
                for fieldTemp in fields:
                    if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                        fieldsDelete.append(fieldTemp.name)
                arcpy.DeleteField_management(in_table = featureClass.featureClassInMemory,
                                             drop_field = fieldsDelete)
                # FeatureClass Delete Field FID_XXX
                arcpy.DeleteField_management(in_table = pathPolyline,
                                             drop_field = fieldFID)
                # Clone Polyline
                featureClass.SetFeatureCloneA()
                pathPolylineCloneA = os.path.join(os.path.join(self.pathProcessGDB, featureDataSetTemp.featureDataSet), featureClass.featureClassCloneA)
                arcpy.CopyFeatures_management(in_features = featureClass.featureClassInMemory,
                                              out_feature_class = pathPolylineCloneA)
                # Maker Layer
                inFeatureClassMerges.append(featureClass.featureClassInMemory)
        outputMerge = "in_memory\\FeatureClassPolylineMerge"
        #outputMerge = os.path.join(self.pathFinalGDB, "FeatureClassMerge")
        arcpy.Merge_management(inputs = inFeatureClassMerges,
                               output = outputMerge)
        return outputMerge
        pass

    def ReadFileConfig(self, pathFile):
        file = open(pathFile, "r")
        textConfig = file.read()
        file.close()
        return json.loads(textConfig)
        pass

    def GetFieldFID(self, featureClass, typeData):
        return "FID_" + featureClass, typeData
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

    def SetFeatureCloneA(self):
        self.featureClassCloneA = self.featureClass + "CloneA"
        pass

    def SetFeatureClassPointRemove(self):
        self.featureClassPointRemove = self.featureClass + "PointRemove"
        pass

# Polyline
class ConfigToolPolyline:
    
    def __init__(self):
        self.listConfigTools = []
        pass

    def ListConfigToolAppend(self, elem):
        self.listConfigTools.append(elem)
        pass

    def GetDict(self):
        listConfigTemp = []
        for elem in self.listConfigTools:
            listConfigTemp.append(elem.GetDict())
        return listConfigTemp;
        pass

# ElemAConfigToolPolyline is Element of ConfigToolPolyline.listConfigTools
class ElemAConfigToolPolyline:

    def __init__(self):
        self.featureDataSet = ""
        self.listPolyline = []
        pass

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolyline = []
        pass

    def ListPolylineAppend(self, elem):
        self.listPolyline.append(elem)
        pass

    def GetDict(self):
        listPolylineTemp = []
        for elem in self.listPolyline:
            listPolylineTemp.append(elem.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolyline": listPolylineTemp
        }

# ElemBConfigToolPolyline is Element of ElemAConfigToolPolyline.listPolyline
class ElemBConfigToolPolyline:

    def __init__(self):
        self.featureClass = ""
        self.processTopo = False
        self.runSimplify = False
        pass

    def __init__(self, featureClass, processTopo, runSimplify):
        self.featureClass = featureClass
        self.processTopo = processTopo
        self.runSimplify = runSimplify
        pass

    def SetProcessTopo(self, processTopo):
        self.processTopo = processTopo
        pass

    def SetRunSimplify(self, runSimplify):
        self.runSimplify = runSimplify
        pass

#Polygon
class ConfigToolPolygon:
    
    def __init__(self):
        self.listConfigTools = []
        pass

    def ListConfigToolAppend(self, elem):
        self.listConfigTools.append(elem)
        pass

    def GetDict(self):
        listConfigTemp = []
        for elem in self.listConfigTools:
            listConfigTemp.append(elem.GetDict())
        return listConfigTemp;
        pass

    def InitFromDict(self, dataJson):
        self.listConfigTools = []
        for elemListConfigTemp in dataJson:
            elemAConfigToolPolygon = ElemAConfigToolPolygon(elemListConfigTemp['featureDataSet'])
            for elemListPolygonTemp in elemListConfigTemp['listPolygon']:
                elemBConfigToolPolygon = ElemBConfigToolPolygon(elemListPolygonTemp['featureClass'], elemListPolygonTemp['runSimplify'])
                for elemListToposTemp in elemListPolygonTemp['polylineProcessTopos']:
                    elemCConfigToolPolygon = ElemCConfigToolPolygon(elemListToposTemp['featureDataSet'])
                    for elemListPolyline in elemListToposTemp['listPolyline']:
                        elemDConfigToolPolygon = ElemDConfigToolPolygon(elemListPolyline['featureClass'], elemListPolyline['processTopo'])
                        elemCConfigToolPolygon.ListPolylineAppend(elemDConfigToolPolygon)
                    if len(elemCConfigToolPolygon.listPolyline) == 0:
                        continue
                    elemBConfigToolPolygon.PolylineProcessToposAppend(elemCConfigToolPolygon)
                if len(elemBConfigToolPolygon.polylineProcessTopos) == 0:
                    continue
                elemAConfigToolPolygon.ListPolygonAppend(elemBConfigToolPolygon)
            self.ListConfigToolAppend(elemAConfigToolPolygon)

# ElemAConfigToolPolygon is Element of ConfigToolPolygon.listConfigTools
class ElemAConfigToolPolygon:

    def __init__(self):
        self.featureDataSet = ""
        self.listPolygon = []
        pass

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolygon = []
        pass

    def ListPolygonAppend(self, elem):
        self.listPolygon.append(elem)
        pass

    def GetDict(self):
        listPolygonTemp = []
        for elem in self.listPolygon:
            listPolygonTemp.append(elem.GetDict())
        return {
            "featureDataSet": self.featureDataSet,
            "listPolygon": listPolygonTemp
        }

# ElemBConfigToolPolygon is Element of ElemAConfigToolPolyline.listPolygon
class ElemBConfigToolPolygon:

    def __init__(self):
        self.featureClass = ""
        self.runSimplify = False
        self.polylineProcessTopos = []
        pass

    def __init__(self, featureClass, runSimplify):
        self.featureClass = featureClass
        self.runSimplify = runSimplify
        self.polylineProcessTopos = []
        pass

    def PolylineProcessToposAppend(self, elem):
        self.polylineProcessTopos.append(elem)
        pass

    def SetProcessTopo(self, processTopo):
        self.processTopo = processTopo
        pass

    def SetRunSimplify(self, runSimplify):
        self.runSimplify = runSimplify
        pass

    def GetDict(self):
        polylineProcessToposTemp = []
        for elem in self.polylineProcessTopos:
            polylineProcessToposTemp.append(elem.GetDict())
        return {
            "featureClass": self.featureClass,
            "runSimplify": self.runSimplify,
            "polylineProcessTopos": polylineProcessToposTemp
        }
        pass

# ElemCConfigToolPolygon is Element of ElemBConfigToolPolygon.polylineProcessTopos
class ElemCConfigToolPolygon:

    def __init__(self):
        self.featureDataSet = ""
        self.listPolyline = []
        pass

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolyline = []
        pass

    def ListPolylineAppend(self, elem):
        self.listPolyline.append(elem)
        pass

    def GetDict(self):
        listPolylineTemp = []
        for elem in self.listPolyline:
            listPolylineTemp.append(elem.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolyline": listPolylineTemp
        }

# ElemDConfigToolPolygon is Element of ElemCConfigToolPolygon.listPolyline
class ElemDConfigToolPolygon:

    def __init__(self):
        self.featureClass = ""
        self.processTopo = False
        pass

    def __init__(self, featureClass, processTopo):
        self.featureClass = featureClass
        self.processTopo = processTopo
        pass

    def SetProcessTopo(self, processTopo):
        self.processTopo = processTopo
        pass

    def SetRunSimplify(self, runSimplify):
        self.runSimplify = runSimplify
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
    simplifyProduction = SimplifyProduction()
    print "Running..."
    simplifyProduction.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass
