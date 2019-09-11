# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import codecs
import datetime
import subprocess

class RepresentationUpdateRuleID:
    
    def __init__(self, pathFileConfig):
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfig = pathFileConfig
        self.dirPathArcObject = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Release"), "SetEmptyShapeRepresentation.exe")
        pass

    def ReadFile(self):
        inputFile = open(self.pathFileConfig, "r")
        self.dictConfig = json.loads(inputFile.read().decode("utf-8-sig"))
        pass

    def Execute(self):
        self.ReadFile()
        self.UpdateRuleID()
        pass

    def UpdateRuleID(self):
        for elemConfig in self.dictConfig:
            pathFeatureDataSet = os.path.join(self.pathFinalGDB, elemConfig["nameFeatureDataset"])
            for elemFeatureClass in elemConfig["listFeatureClass"]:
                pathFeatureClass = os.path.join(pathFeatureDataSet, elemFeatureClass["nameFeatureClass"])
                if not arcpy.Exists(pathFeatureClass) or int(arcpy.GetCount_management(pathFeatureClass).getOutput(0)) == 0:
                    continue
                print " # {}".format(str(pathFeatureClass))
                desc = arcpy.Describe(pathFeatureClass)
                for child in desc.representations:
                    if child.datasetType == "RepresentationClass":
                        for elemRepresentation in elemFeatureClass["listRepresentation"]:
                            if child.name == elemRepresentation["nameRepresentation"]:
                                print "    ## {}".format(str(child.name))
                                outLayer = arcpy.MakeFeatureLayer_management(in_features = pathFeatureClass)
                                arcpy.CalculateField_management(in_table = outLayer,
                                                                field = child.ruleIDFieldName,
                                                                expression = "None",
                                                                expression_type = "PYTHON_9.3")
                                for elemRule in elemRepresentation["listRule"]:
                                    if elemRule["querySQL"] == "":
                                        continue
                                    print "       ### {}".format(elemRule["querySQL"])
                                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outLayer,
                                                                            selection_type = "NEW_SELECTION",
                                                                            where_clause = elemRule["querySQL"])
                                    print "           #### Count Select {}".format(arcpy.GetCount_management(outLayer).getOutput(0))
                                    arcpy.CalculateField_management(in_table = outLayer,
                                                                    field = child.ruleIDFieldName,
                                                                    expression = elemRule["ruleID"],
                                                                    expression_type = "PYTHON_9.3")
                                break
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
    print "Path File Config: {}".format(sys.argv[1])
    representationUpdateRuleID = RepresentationUpdateRuleID(sys.argv[1])
    print "Running..."
    representationUpdateRuleID.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass
