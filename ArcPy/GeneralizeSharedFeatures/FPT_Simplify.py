# -*- coding: utf-8 -*-
import arcpy
import os
import json
import sys
import inspect

class FPT_Simplify:
    def __init__(self, snap_distance):
        self.snap_distance = snap_distance
        
    def simplify(self):
        try:
            arcpy.env.overwriteOutput = 1
            duongDanNguon = "C:/Generalize_25_50/50K_Process.gdb"
            duongDanDich = "C:/Generalize_25_50/50K_Final.gdb"
            urlFile = '/ConfigSimplify.json'
            _generalize_Operation = "SIMPLIFY"
            _algorithm = "BEND_SIMPLIFY"
            _tolerance = "50 Meters"
            _error_option = "NO_CHECK"
            _collapsed_point_option = "NO_KEEP"
            _checkExitLayer = False
            if arcpy.Exists(duongDanNguon + "/ThuyHe/SongSuoiL_KenhMuongL_SnapPBM") and arcpy.Exists(duongDanNguon + "/PhuBeMat/PhuBeMat_Full"):
                _checkExitLayer = True
                
            #Doc file config
            s1 = inspect.getfile(inspect.currentframe())
            s2 = os.path.dirname(s1)
            urlFile = s2 + urlFile
            arcpy.AddMessage("\n# Doc file cau hinh: \"{0}\"".format(urlFile))
            if os.path.exists(urlFile):
                fileConfig = open(urlFile)
                listLayerConfig = json.load(fileConfig)
                fileConfig.close()
                arcpy.Integrate_management([[duongDanNguon + "/PhuBeMat/PhuBeMat", 1]], "2 Meters")
                listPolygon = []
                listPolyline = []
                #compareFeaturesPolygon = []
                #compareFeaturesPolyline = []
                for objConfig in listLayerConfig:
                    if objConfig["RunStatus"] == "True":
                        if not(_checkExitLayer == False and objConfig["LayerName"] == "PhuBeMat_Full"):
                            if arcpy.Exists(duongDanNguon + "/" +  objConfig["DatasetName"] + "/" + objConfig["LayerName"]):
                                temp = {
                                    "LayerType": objConfig["LayerType"],
                                    "DatasetName": objConfig["DatasetName"],
                                    "LayerName": objConfig["LayerName"],
                                    "featureLayer": "in_memory\\" + objConfig["LayerName"] + "_Layer",
                                    "featureCopy": "in_memory\\" + objConfig["LayerName"] + "_Copy",
                                    "featureCopyLayer": "in_memory\\" + objConfig["LayerName"] + "_Copy_Layer",
                                    "FID_XXX": "FID_" + objConfig["LayerName"],
                                    "layerPath": duongDanNguon + "/" +  objConfig["DatasetName"] + "/" + objConfig["LayerName"]
                                }
                                if objConfig["LayerType"] == "Polygon":
                                    listPolygon.append(temp)
                                else:
                                    listPolyline.append(temp)
                ###Polygon
                fieldMappingPolygon = arcpy.FieldMappings()
                enableFieldPolygon = []
                inputsMergePolygon = []                
                for element in listPolygon:
                    if element["LayerName"] <> "PhuBeMat" and element["LayerName"] <> "PhuBeMat_Full" and element["LayerName"] <> "DiaPhan":                 
                        arcpy.MakeFeatureLayer_management(element["layerPath"], element["featureLayer"])
                        arcpy.AddField_management(element["featureLayer"], element["FID_XXX"], "LONG")
                        with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", element["FID_XXX"]]) as cursor:
                            for row in cursor:
                                row[1] = row[0]
                                cursor.updateRow(row)
                        arcpy.CopyFeatures_management(element["layerPath"], element["featureCopy"])
                        arcpy.MakeFeatureLayer_management(element["featureCopy"], element["featureCopyLayer"])
                        enableFieldPolygon.append(element["FID_XXX"])
                        fieldMappingPolygon.addTable(element["featureCopyLayer"])
                        inputsMergePolygon.append(element["featureCopyLayer"])
                for field in fieldMappingPolygon.fields:
                    if field.name not in enableFieldPolygon:
                        fieldMappingPolygon.removeFieldMap(fieldMappingPolygon.findFieldMapIndex(field.name))
                outPathMerge_Polygon = duongDanNguon + "/BienGioiDiaGioi/outPathMergeTemp_Polygon"
                arcpy.Merge_management (inputsMergePolygon, outPathMerge_Polygon, fieldMappingPolygon)
                ####Line
                fieldMappingLine = arcpy.FieldMappings()
                enableFieldLine = []
                inputsMergeLine = []
                for element in listPolyline:    
                    if element["DatasetName"] <> "DiaHinh":            
                        arcpy.MakeFeatureLayer_management(element["layerPath"], element["featureLayer"])
                        arcpy.AddField_management(element["featureLayer"], element["FID_XXX"], "LONG")
                        with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", element["FID_XXX"]]) as cursor:
                            for row in cursor:
                                row[1] = row[0]
                                cursor.updateRow(row)
                        arcpy.CopyFeatures_management(element["layerPath"], element["featureCopy"])
                        arcpy.MakeFeatureLayer_management(element["featureCopy"], element["featureCopyLayer"])
                        enableFieldLine.append(element["FID_XXX"])
                        fieldMappingLine.addTable(element["featureCopyLayer"])
                        inputsMergeLine.append(element["featureCopyLayer"])
                for field in fieldMappingLine.fields:
                    if field.name not in enableFieldLine:
                        fieldMappingLine.removeFieldMap(fieldMappingLine.findFieldMapIndex(field.name))
                outPathMerge_Line = duongDanNguon + "/BienGioiDiaGioi/outPathMergeTemp_Line"
                arcpy.AddMessage("\n# Simplify: Polygon")
                arcpy.Merge_management (inputsMergeLine, outPathMerge_Line, fieldMappingLine)
                arcpy.GeneralizeSharedFeatures_production(Input_Features = outPathMerge_Polygon, Generalize_Operation = _generalize_Operation, Simplify_Tolerance = _tolerance, 
                        Topology_Feature_Classes = outPathMerge_Line, Simplification_Algorithm = _algorithm)
                arcpy.AddMessage("\n# Simplify: Polyline")
                arcpy.Merge_management (inputsMergeLine, outPathMerge_Line, fieldMappingLine)
                arcpy.GeneralizeSharedFeatures_production(Input_Features = outPathMerge_Line, Generalize_Operation = _generalize_Operation, Simplify_Tolerance = _tolerance, 
                        Topology_Feature_Classes = outPathMerge_Polygon, Simplification_Algorithm = _algorithm)
                outPathSimplifyLayer_Polygon = "in_memory\\outPathSimplifyTempLayer_Polygon"
                arcpy.MakeFeatureLayer_management(outPathMerge_Polygon, outPathSimplifyLayer_Polygon)
                outPathSimplifyLayer_Line = "in_memory\\outPathSimplifyTempLayer_Line"
                arcpy.MakeFeatureLayer_management(outPathMerge_Line, outPathSimplifyLayer_Line)
                for element in listPolygon:
                    if element["LayerName"] == "PhuBeMat" or element["LayerName"] == "PhuBeMat_Full" or element["LayerName"] == "DiaPhan":
                        arcpy.GeneralizeSharedFeatures_production(Input_Features = element["layerPath"], Generalize_Operation = _generalize_Operation, Simplify_Tolerance = _tolerance, 
                            Simplification_Algorithm = _algorithm)
                for element in listPolyline:    
                    if element["DatasetName"] == "DiaHinh":
                        arcpy.GeneralizeSharedFeatures_production(Input_Features = element["layerPath"], Generalize_Operation = _generalize_Operation, Simplify_Tolerance = _tolerance, 
                            Simplification_Algorithm = _algorithm)
                ## Update Shape Feature Class Polygon ##
                arcpy.AddMessage("\n# Update Shape Feature Class Polygon:")
                for element in listPolygon:
                    if element["LayerName"] <> "PhuBeMat" and element["LayerName"] <> "PhuBeMat_Full" and element["LayerName"] <> "DiaPhan": 
                        arcpy.AddMessage("\n\t# Update {0}...".format(element["LayerName"]))
                        arcpy.MakeFeatureLayer_management(element["layerPath"], element["featureLayer"])
                        strQuery = element["FID_XXX"] + " IS NOT NULL"
                        arcpy.SelectLayerByAttribute_management(outPathSimplifyLayer_Polygon, "NEW_SELECTION", strQuery)
                        outTableTemp = "in_memory\\outTableTemp"
                        arcpy.CopyFeatures_management(outPathSimplifyLayer_Polygon, outTableTemp)
                        with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", "SHAPE@"]) as cursor:
                            for row in cursor:
                                found = False
                                with arcpy.da.UpdateCursor(outTableTemp, [element["FID_XXX"], "SHAPE@"]) as cursorSub:
                                    for rowSub in cursorSub:
                                        if row[0] == rowSub[0]:
                                            found = True
                                            row[1] = rowSub[1]
                                            cursor.updateRow(row)
                                            cursorSub.deleteRow()
                                            break
                                if found == False:
                                    cursor.deleteRow()
                arcpy.AddMessage("\n# Update Shape Feature Class Line:")
                for element in listPolyline:
                    if element["DatasetName"] <> "DiaHinh":
                        arcpy.AddMessage("\n\t# Update {0}...".format(element["LayerName"]))
                        arcpy.MakeFeatureLayer_management(element["layerPath"], element["featureLayer"])
                        strQuery = element["FID_XXX"] + " IS NOT NULL"
                        arcpy.SelectLayerByAttribute_management(outPathSimplifyLayer_Line, "NEW_SELECTION", strQuery)
                        outTableTemp = "in_memory\\outTableTemp"
                        arcpy.CopyFeatures_management(outPathSimplifyLayer_Line, outTableTemp)
                        with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", "SHAPE@"]) as cursor:
                            for row in cursor:
                                found = False
                                with arcpy.da.UpdateCursor(outTableTemp, [element["FID_XXX"], "SHAPE@"]) as cursorSub:
                                    for rowSub in cursorSub:
                                        if row[0] == rowSub[0]:
                                            found = True
                                            row[1] = rowSub[1]
                                            cursor.updateRow(row)
                                            cursorSub.deleteRow()
                                            break
                                if found == False:
                                    cursor.deleteRow()
            else:
                arcpy.AddMessage("\n# Khong tim thay file cau hinh: \"{0}\"".format(urlFile))
        except OSError as error:
            arcpy.AddMessage("Error" + error.message)
        except ValueError as error:
            arcpy.AddMessage("Error" + error.message)
        except arcpy.ExecuteError as error:
            arcpy.AddMessage("Error" + error.message)
        finally:
            arcpy.Delete_management("in_memory")

if __name__=='__main__':
    obj = FPT_Simplify("25 Meters")
    obj.simplify()
