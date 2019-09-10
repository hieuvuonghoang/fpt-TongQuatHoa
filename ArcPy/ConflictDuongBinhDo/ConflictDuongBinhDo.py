# -*- coding: utf-8 -*-
import arcpy
import os

class ConflictDuongBinhDo:

    def __init__(self):
        self.pathProcessGDB = r"C:\Generalize_25_50\50K_Process.gdb"
        self.pathDuongBoNuoc = r"C:\Generalize_25_50\50K_Process.gdb\ThuyHe\DuongBoNuoc"
        self.pathDuongBoNuocTemp = r"C:\Generalize_25_50\50K_Process.gdb\ThuyHe\DuongBoNuocTemp"
        self.pathDuongBinhDo = r"C:\Generalize_25_50\50K_Process.gdb\DiaHinh\DuongBinhDo"
        self.pathDuongBinhDoTemp = r"C:\Generalize_25_50\50K_Process.gdb\DiaHinh\DuongBinhDoTemp"
        self.pathDuongBinhDoTempSinglePart = r"C:\Generalize_25_50\50K_Process.gdb\DiaHinh\DuongBinhDoTempSinglePart"
        self.pathDuongBinhDoFinal = r"C:\Generalize_25_50\50K_Final.gdb\DiaHinh\DuongBinhDo"
        pass

    def Execute(self):
        # Init WorksSpace
        arcpy.env.workspace = self.pathProcessGDB
        arcpy.env.overwriteOutput = True
        arcpy.env.referenceScale = "50000"
        #
        print "Copy from \"{}\" to \"{}\"".format(self.pathDuongBinhDo, self.pathDuongBinhDoFinal)
        arcpy.CopyFeatures_management(self.pathDuongBinhDo, self.pathDuongBinhDoFinal)
        #
        self.CreateBufferConflict(self.pathDuongBoNuoc, "DuongBoNuoc_Rep")
        # Resolve Road Conflicts
        print "Run: Resolve Road Conflicts"
        duongBoNuocTempSinglePartLayer = arcpy.MakeFeatureLayer_management(self.pathDuongBoNuoc + "TempSinglePart")
        duongBinhDoTempSinglePartLayer = arcpy.MakeFeatureLayer_management(self.pathDuongBinhDoTempSinglePart)
        # Add Field
        arcpy.AddField_management(duongBoNuocTempSinglePartLayer, "hierarchy", "LONG")
        arcpy.AddField_management(duongBinhDoTempSinglePartLayer, "hierarchy", "LONG")
        # Update Field
        arcpy.CalculateField_management(duongBoNuocTempSinglePartLayer, "hierarchy", "0", "PYTHON_9.3")
        arcpy.CalculateField_management(duongBinhDoTempSinglePartLayer, "hierarchy", "1", "PYTHON_9.3")
        # Set Layer
        arcpy.SetLayerRepresentation_cartography(duongBoNuocTempSinglePartLayer, self.GetAndSetRepresentation(duongBoNuocTempSinglePartLayer))
        arcpy.SetLayerRepresentation_cartography(duongBinhDoTempSinglePartLayer, self.GetAndSetRepresentation(duongBinhDoTempSinglePartLayer))
        # Run ResolveRoadConflicts
        outPutResolveRoadConflicts = os.path.join(self.pathProcessGDB, "OutputResolveRoadConflicts")
        arcpy.ResolveRoadConflicts_cartography([duongBoNuocTempSinglePartLayer, duongBinhDoTempSinglePartLayer], "hierarchy", outPutResolveRoadConflicts)
        # Run Propagate Displacement
        print "Run: Propagate Displacement"
        duongBinhDoFinalLayer = arcpy.MakeFeatureLayer_management(self.pathDuongBinhDoFinal)
        arcpy.SetLayerRepresentation_cartography(duongBinhDoFinalLayer, self.GetAndSetRepresentation(duongBinhDoFinalLayer))
        arcpy.PropagateDisplacement_cartography(duongBinhDoFinalLayer, outPutResolveRoadConflicts, "AUTO")
        pass

    def ClipByBufferDuongBinhDo(self, duongBinhDoBuffer, inFeatureProcess):
        outputClip = "in_memory\\outputClip"
        arcpy.Clip_analysis(inFeatureProcess, duongBinhDoBuffer, outputClip, "0 Meters")
        return outputClip
        pass
    
    def CreateBufferConflict(self, inFeatureProcess, representationName):
        #
        featureProcessLayer = arcpy.MakeFeatureLayer_management(inFeatureProcess)
        duongBinhDoLayer = arcpy.MakeFeatureLayer_management("DuongBinhDo")
        arcpy.SetLayerRepresentation_cartography(featureProcessLayer, self.GetAndSetRepresentation(featureProcessLayer))
        arcpy.SetLayerRepresentation_cartography(duongBinhDoLayer, self.GetAndSetRepresentation(duongBinhDoLayer))
        #
        print "Run: Detect Graphic Conflict"
        outFeatureClass = self.RunDetectGraphicConflict(featureProcessLayer, duongBinhDoLayer)
        #
        outFeatureClassConflictBuffer = "in_memory\\featureClassConflictBuffer"
        print "Create Feature: {}".format(outFeatureClassConflictBuffer)
        arcpy.Buffer_analysis(outFeatureClass, outFeatureClassConflictBuffer, "100 Meters", None, None, "ALL")
        print "Delete {}".format(str(outFeatureClass))
        arcpy.Delete_management(outFeatureClass)
        #
        print "Create Feature: {}".format(self.pathDuongBinhDoTemp)
        arcpy.Clip_analysis("DuongBinhDo", outFeatureClassConflictBuffer, self.pathDuongBinhDoTemp)
        print "Create Feature: {}".format(inFeatureProcess + "Temp")
        arcpy.Clip_analysis(inFeatureProcess, outFeatureClassConflictBuffer, inFeatureProcess + "Temp")
        #
        print "Create Feature: {}".format(self.pathDuongBinhDoTempSinglePart)
        if arcpy.Exists(self.pathDuongBinhDoTempSinglePart):
            arcpy.Delete_management(self.pathDuongBinhDoTempSinglePart)
        arcpy.MultipartToSinglepart_management(self.pathDuongBinhDoTemp, self.pathDuongBinhDoTempSinglePart)
        print "Create Feature: {}".format(inFeatureProcess + "TempSinglePart")
        if arcpy.Exists(inFeatureProcess + "TempSinglePart"):
            arcpy.Delete_management(inFeatureProcess + "TempSinglePart")
        arcpy.MultipartToSinglepart_management(inFeatureProcess + "Temp", inFeatureProcess + "TempSinglePart")
        pass

    def RunDetectGraphicConflict(self, inFeature, conflictFeature):
        outFeatureClass = "in_memory\\outFeatureClass"
        arcpy.DetectGraphicConflict_cartography(in_features = inFeature,
                                                conflict_features = conflictFeature,
                                                out_feature_class = outFeatureClass,
                                                conflict_distance = "0 Meters",
                                                line_connection_allowance = "1 Points")
        return outFeatureClass
        pass

    def GetAndSetRepresentation(self, inFeature):
        desc = arcpy.Describe(inFeature)
        if len(desc.representations) == 0:
            return None
        elif len(desc.representations) == 1:
            return desc.representations[0].name
        else:
            arrRepresentation = []
            for child in desc.representations:
                if child.datasetType == "RepresentationClass":
                    arrRepresentation.append(child.name)
            print "# Select Representation:"
            index = 0
            for rep in arrRepresentation:
                print "    {}. {}".format(str(index), str(rep))
                index += 1
            print "# Select: "
            while(True):
                strKey = raw_input()
                try:
                    intKey = int(strKey)
                    if intKey >= 0 and intKey <= (len(arrRepresentation) - 1):
                        break
                    else:
                        print "# Out of range?"
                except ValueError:
                    print "# Could not convert data to an integer?"
            return arrRepresentation[intKey]
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
    conflictDuongBinhDo = ConflictDuongBinhDo()
    print "Running..."
    conflictDuongBinhDo.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass
