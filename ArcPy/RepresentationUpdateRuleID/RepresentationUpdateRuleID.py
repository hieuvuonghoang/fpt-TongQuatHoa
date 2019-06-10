import os
import sys
import json
import arcpy
import codecs

class RepresentationUpdateRuleID:
    
    def __init__(self):
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigTools.json")
        self.ReadFile(self.pathFileConfig)
        pass

    def ReadFile(self, pathFile):
        inputFile = open(pathFile, "r")
        self.dictConfig = json.loads(inputFile.read().decode("utf-8-sig"))
        pass

    def Execute(self):
        self.UpdateRuleID()
        pass

    def UpdateRuleID(self):
        for elemConfig in self.dictConfig:
            pathFeatureDataSet = os.path.join(self.pathFinalGDB, elemConfig["nameFeatureDataset"])
            for elemFeatureClass in elemConfig["listFeatureClass"]:
                pathFeatureClass = os.path.join(pathFeatureDataSet, elemFeatureClass["nameFeatureClass"])
                outLayer = elemFeatureClass["nameFeatureClass"] + "Layer"
                arcpy.MakeFeatureLayer_management(in_features = pathFeatureClass,
                                                  out_layer = outLayer)
                desc = arcpy.Describe(pathFeatureClass)
                for child in desc.representations:
                    if child.datasetType == "RepresentationClass":
                        for elemRepresentation in elemFeatureClass["listRepresentation"]:
                            if child.name == elemRepresentation["nameRepresentation"]:
                                for elemRule in elemRepresentation["listRule"]:
                                    if elemRule["querySQL"] == "":
                                        continue
                                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outLayer,
                                                                            selection_type = "NEW_SELECTION",
                                                                            where_clause = elemRule["querySQL"])
                                    arcpy.CalculateField_management(in_table = outLayer,
                                                                    field = child.ruleIDFieldName,
                                                                    expression = elemRule["ruleID"],
                                                                    expression_type = "PYTHON_9.3")
        pass

if __name__ == "__main__":
   representationUpdateRuleID = RepresentationUpdateRuleID()
   representationUpdateRuleID.Execute()
