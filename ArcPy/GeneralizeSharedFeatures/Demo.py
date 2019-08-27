import os
import json
import arcpy

class Demo:
    
    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfigPolyline = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigPolyline.json")
        self.pathFileConfigPolygon = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigPolygon.json")
        self.pathFileGSFPolygons = os.path.join(os.path.dirname(os.path.realpath(__file__)), "GeneralizeSharedFeaturesPolygons.json")
        pass

    def Execute(self):
        self.CreateFileConfigGSFPolygons()
        pass

    def CreateFileConfig(self):
        self.configToolPolyline = ConfigToolPolyline()
        self.configToolPolygon = ConfigToolPolygon()
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemAConfigToolPolyline = ElemAConfigToolPolyline(fcDataSetTemp.baseName)
            elemAConfigToolPolygon = ElemAConfigToolPolygon(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    elemBConfigToolPolyline = ElemBConfigToolPolyline(fcTemp.baseName, False, False)
                    elemAConfigToolPolyline.ListPolylineAppend(elemBConfigToolPolyline)
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemBConfigToolPolygon = ElemBConfigToolPolygon(fcTemp.baseName, True)
                    elemAConfigToolPolygon.ListPolygonAppend(elemBConfigToolPolygon)
            if len(elemAConfigToolPolyline.listPolyline) > 0:
                self.configToolPolyline.ListConfigToolAppend(elemAConfigToolPolyline)
            if len(elemAConfigToolPolygon.listPolygon) > 0:
                self.configToolPolygon.ListConfigToolAppend(elemAConfigToolPolygon)
        #
        textConfig = json.dumps(obj = self.configToolPolyline.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileConfigPolyline, "w")
        file.write(textConfig)
        file.close()
        #
        textConfig = json.dumps(obj = self.configToolPolygon.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileConfigPolygon, "w")
        file.write(textConfig)
        file.close()
        pass

    def CreateFileConfigGSFPolygons(self):
        #
        arrElemCConfigToolPolygon = self.ReadAllPolyline()
        self.configToolPolygon = ConfigToolPolygon()
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemAConfigToolPolygon = ElemAConfigToolPolygon(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemBConfigToolPolygon = ElemBConfigToolPolygon(fcTemp.baseName, True)
                    for elemCConfigToolPolygonTemp in arrElemCConfigToolPolygon:
                        elemBConfigToolPolygon.PolylineProcessToposAppend(elemCConfigToolPolygonTemp)
                    if len(elemBConfigToolPolygon.polylineProcessTopos) == 0:
                        continue
                    elemAConfigToolPolygon.ListPolygonAppend(elemBConfigToolPolygon)
            if len(elemAConfigToolPolygon.listPolygon) == 0:
                continue
            self.configToolPolygon.ListConfigToolAppend(elemAConfigToolPolygon)
        #
        textConfig = json.dumps(obj = self.configToolPolygon.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileGSFPolygons, "w")
        file.write(textConfig)
        file.close()
        pass

    def ReadAllPolyline(self):
        arrElemCConfigToolPolygon = []
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemCConfigToolPolygon = ElemCConfigToolPolygon(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    elemDConfigToolPolygon = ElemDConfigToolPolygon(fcTemp.baseName, False)
                    elemCConfigToolPolygon.ListPolylineAppend(elemDConfigToolPolygon)
            if len(elemCConfigToolPolygon.listPolyline) == 0:
                continue
            arrElemCConfigToolPolygon.append(elemCConfigToolPolygon)
        return arrElemCConfigToolPolygon
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

if __name__ == "__main__":
    demo = Demo()
    demo.Execute()
    pass