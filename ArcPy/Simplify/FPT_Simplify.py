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
        # Init WorkSpase #
        arcpy.env.overwriteOutput = 1
        duongDanNguon = "C:/Generalize_25_50/50K_Process.gdb"
        duongDanDich = "C:/Generalize_25_50/50K_Final.gdb"
        urlFile = '/ConfigSimplify.json'
        _algorithm = "BEND_SIMPLIFY"
        _tolerance = "30 Meters"
        _error_option = "NO_CHECK"
        _collapsed_point_option = "NO_KEEP"
        _checkExitLayer = False
        if arcpy.Exists(duongDanNguon + "/ThuyHe/SongSuoiL_KenhMuongL_SnapPBM") and arcpy.Exists(duongDanNguon + "/PhuBeMat/PhuBeMat_Full"):
            _checkExitLayer = True
        #Doc file config
        s1 = inspect.getfile(inspect.currentframe())
        s2 = os.path.dirname(s1)
        urlFile = s2 + urlFile
        urlFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigSimplify.json")
        arcpy.AddMessage("\n# Doc file cau hinh: \"{0}\"".format(urlFile))
        if os.path.exists(urlFile):
            fileConfig = open(urlFile)
            listLayerConfig = json.load(fileConfig)
            fileConfig.close()
            ############################### Simplify Polygon ########################################
            #arcpy.Integrate_management([[duongDanNguon + "/PhuBeMat/PhuBeMat", 1]], "2 Meters")
            arcpy.AddMessage("\n# Bat dau Simplify Polygon")
            listPolygon = []
            fieldMappings = arcpy.FieldMappings()
            enableFields = []
            inputsMerge = []
            for objConfig in listLayerConfig:
                if objConfig["LayerType"] == "Polygon" and objConfig["RunStatus"] == "True":
                    if not(_checkExitLayer == False and objConfig["LayerName"] == "PhuBeMat_Full"):
                        if arcpy.Exists(duongDanNguon + "/" +  objConfig["DatasetName"] + "/" + objConfig["LayerName"]):
                            temp = {
                                "LayerType": objConfig["LayerType"],
                                "DatasetName": objConfig["DatasetName"],
                                "LayerName": objConfig["LayerName"],
                                "featureLayer": "in_memory\\" + objConfig["LayerName"] + "_Layer",
                                "featureCopy": "in_memory\\" + objConfig["LayerName"] + "_Copy",
                                "featureCopyLayer": "in_memory\\" + objConfig["LayerName"] + "_Copy_Layer",
                                "FID_XXX": "FID_" + objConfig["LayerName"]
                            }
                            listPolygon.append(temp)
                elif objConfig["LayerType"] == "Polyline" and objConfig["RunStatus"] == "True" and objConfig["DatasetName"] <> "DiaHinh":
                    if not(_checkExitLayer == False and objConfig["LayerName"] == "SongSuoiL_KenhMuongL_SnapPBM"):
                        if arcpy.Exists(duongDanNguon + "/" +  objConfig["DatasetName"] + "/" + objConfig["LayerName"]):
                            arcpy.AddMessage("\n# Buffer lop: \"{0}\"".format(objConfig["LayerName"]))
                            layerPath = duongDanNguon + "/" +  objConfig["DatasetName"] + "/" + objConfig["LayerName"]
                            arcpy.Buffer_analysis(in_features = layerPath, out_feature_class = layerPath + "_Buffer", 
                                buffer_distance_or_field = "0.5 Meters", line_side = "RIGHT")
                            
                            temp = {
                                "LayerType": objConfig["LayerType"],
                                "DatasetName": objConfig["DatasetName"],
                                "LayerName": objConfig["LayerName"] + "_Buffer",
                                "featureLayer": "in_memory\\" + objConfig["LayerName"] + "_Buffer_Layer",
                                "featureCopy": "in_memory\\" + objConfig["LayerName"] + "_Buffer_Copy",
                                "featureCopyLayer": "in_memory\\" + objConfig["LayerName"] + "_Buffer_Copy_Layer",
                                "FID_XXX": "FID_" + objConfig["LayerName"]
                            }
                            listPolygon.append(temp)
            
            for element in listPolygon:
                arcpy.AddMessage("\n# Xu ly lop: {0}".format(element["LayerName"]))
                layerPath = duongDanNguon + "/" +  element["DatasetName"] + "/" + element["LayerName"]
                arcpy.MakeFeatureLayer_management(layerPath, element["featureLayer"])
                if element["LayerType"] == "Polygon" and element["DatasetName"] == "DiaHinh":
                    arcpy.AddField_management(layerPath, "OLD_OBJECTID", "LONG", None, None, None,"OLD_OBJECTID", "NULLABLE")
                    arcpy.CalculateField_management(layerPath, "OLD_OBJECTID", "!OBJECTID!", "PYTHON_9.3")
                    outPathSimplify = "in_memory\\outPathSimplifyTemp"
                    arcpy.SimplifyPolygon_cartography(in_features = element["featureLayer"],
                                            out_feature_class = outPathSimplify,
                                            algorithm = _algorithm,
                                            tolerance = _tolerance,
                                            minimum_area = "0 SquareMeters",
                                            error_option = _error_option,
                                            collapsed_point_option = _collapsed_point_option)
                    arcpy.CopyFeatures_management(outPathSimplify, layerPath)
                else:
                    arcpy.AddField_management(element["featureLayer"], element["FID_XXX"], "LONG")
                    print "#### {}, {}".format(str(element["featureLayer"]), str(element["FID_XXX"]))
                    # Add Field #
                    arcpy.AddField_management(element["featureLayer"], "IS_Buffer", "LONG")
                    # End Add Field #
                    if element["LayerType"] == "Polyline":
                        with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", element["FID_XXX"], "IS_Buffer"]) as cursor:
                            for row in cursor:
                                row[1] = row[0]
                                row[2] = 1
                                cursor.updateRow(row)
                    else:
                        with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", element["FID_XXX"]]) as cursor:
                            for row in cursor:
                                row[1] = row[0]
                                cursor.updateRow(row)
                    arcpy.CopyFeatures_management(layerPath, element["featureCopy"])
                    arcpy.MakeFeatureLayer_management(element["featureCopy"], element["featureCopyLayer"])
                    ## Field Mappings ##
                    enableFields.append(element["FID_XXX"])
                    fieldMappings.addTable(element["featureCopyLayer"])
                    inputsMerge.append(element["featureCopyLayer"])
            enableFields.append("IS_Buffer")
            for field in fieldMappings.fields:
                if field.name not in enableFields:
                    fieldMappings.removeFieldMap(fieldMappings.findFieldMapIndex(field.name))
            ## Merge ##
            arcpy.AddMessage("\n# Merge Polygon...")
            # outPathMerge = "in_memory\\outPathMergeTemp"
            outPathMerge = os.path.join(duongDanNguon, "outPathMerge")
            #outPathMerge = "C:/Generalize_25_50/50K_Process.gdb/DanCuCoSoHaTang/outPathMergeTemp"
            arcpy.Merge_management (inputsMerge, outPathMerge, fieldMappings)
            ## Simplify Polygon ##
            arcpy.AddMessage("\n# Simplify Polygon...")
            outPathSimplify = "in_memory\\outPathSimplifyTemp"
            arcpy.SimplifyPolygon_cartography(in_features = outPathMerge,
                                            out_feature_class = outPathSimplify,
                                            algorithm = _algorithm,
                                            tolerance = _tolerance,
                                            minimum_area = "0 SquareMeters",
                                            error_option = _error_option,
                                            collapsed_point_option = _collapsed_point_option)
            outPathSimplifyPolygon = os.path.join(duongDanNguon, "outPathSimplifyPolygon")
            arcpy.CopyFeatures_management(outPathSimplify, outPathSimplifyPolygon)
            ## MakeLayerFeature ##
            outPathSimplifyLayer = "in_memory\\outPathSimplifyTempLayer"
            arcpy.MakeFeatureLayer_management(outPathSimplify, outPathSimplifyLayer)
            ## Update Shape Feature Class ##
            arcpy.AddMessage("\n# Update Shape Feature Class:")
            for element in listPolygon:
                if element["DatasetName"] <> "DiaHinh":
                    arcpy.AddMessage("\n\t# Update {0}...".format(element["LayerName"]))
                    ### MakeLayerFeature ###
                    layerPath = duongDanNguon + "/" +  element["DatasetName"] + "/" + element["LayerName"]
                    arcpy.MakeFeatureLayer_management(layerPath, element["featureLayer"])
                    ### Select ###
                    strQuery = element["FID_XXX"] + " IS NOT NULL"
                    arcpy.SelectLayerByAttribute_management(outPathSimplifyLayer, "NEW_SELECTION", strQuery)
                    ### Copy To Table Temp ###
                    outTableTemp = "in_memory\\outTableTemp"
                    arcpy.CopyFeatures_management(outPathSimplifyLayer, outTableTemp)
                    ### ... ###
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
            arcpy.AddMessage("\n# Hoan thanh Simplify Polygon!!!")
            ############################################## Simplify Line #############################
            
            arcpy.AddMessage("\n# Bat dau Simplify Line")
            listPolyLine = []
            fieldMappingLine = arcpy.FieldMappings()
            enableFieldLine = []
            inputsMergeLine = []
            for objConfig in listLayerConfig:
                if objConfig["LayerType"] == "Polyline" and objConfig["RunStatus"] == "True":
                    if not(_checkExitLayer == False and objConfig["LayerName"] == "SongSuoiL_KenhMuongL_SnapPBM"):
                        if arcpy.Exists(duongDanNguon + "/" +  objConfig["DatasetName"] + "/" + objConfig["LayerName"]):
                            temp = {
                                "LayerType": objConfig["LayerType"],
                                "DatasetName": objConfig["DatasetName"],
                                "LayerName": objConfig["LayerName"],
                                "featureLayer": "in_memory\\" + objConfig["LayerName"] + "_Layer",
                                "featureCopy": "in_memory\\" + objConfig["LayerName"] + "_Copy",
                                "featureCopyLayer": "in_memory\\" + objConfig["LayerName"] + "_Copy_Layer",
                                "FID_XXX": "FID_" + objConfig["LayerName"]
                            }
                            listPolyLine.append(temp)
            for element in listPolyLine:
                arcpy.AddMessage("\n# Xu ly lop: {0}".format(element["LayerName"]))
                layerPath = duongDanNguon + "/" +  element["DatasetName"] + "/" + element["LayerName"]
                arcpy.MakeFeatureLayer_management(layerPath, element["featureLayer"])
                if element["DatasetName"] == "DiaHinh":
                    arcpy.AddField_management(layerPath, "OLD_OBJECTID", "LONG", None, None, None,"OLD_OBJECTID", "NULLABLE")
                    arcpy.CalculateField_management(layerPath, "OLD_OBJECTID", "!OBJECTID!", "PYTHON_9.3")
                    outPathSimplify = "in_memory\\outPathSimplifyTemp"
                    arcpy.SimplifyLine_cartography(in_features = element["featureLayer"], 
                        out_feature_class = outPathSimplify, 
                        algorithm = _algorithm, 
                        tolerance = _tolerance,  
                        collapsed_point_option = _collapsed_point_option)
                    arcpy.CopyFeatures_management(outPathSimplify, layerPath)
                else:
                    arcpy.AddField_management(element["featureLayer"], element["FID_XXX"], "LONG")
                    with arcpy.da.UpdateCursor(element["featureLayer"], ["OID@", element["FID_XXX"]]) as cursor:
                        for row in cursor:
                            row[1] = row[0]
                            cursor.updateRow(row)
                    arcpy.CopyFeatures_management(layerPath, element["featureCopy"])
                    arcpy.MakeFeatureLayer_management(element["featureCopy"], element["featureCopyLayer"])
                    enableFieldLine.append(element["FID_XXX"])
                    fieldMappingLine.addTable(element["featureCopyLayer"])
                    inputsMergeLine.append(element["featureCopyLayer"])
            for field in fieldMappingLine.fields:
                if field.name not in enableFieldLine:
                    fieldMappingLine.removeFieldMap(fieldMappingLine.findFieldMapIndex(field.name))
            ## Merge ##
            arcpy.AddMessage("\n# Merge Polyline...")
            outPathMerge = "in_memory\\outPathMergeTemp"
            arcpy.Merge_management (inputsMergeLine, outPathMerge, fieldMappingLine)
            ## Simplify Polyline ##
            arcpy.AddMessage("\n# Simplify Polyline...")
            outPathSimplify = "in_memory\\outPathSimplifyTemp"
            arcpy.SimplifyLine_cartography(in_features = outPathMerge, 
                    out_feature_class = outPathSimplify, 
                    algorithm = _algorithm, 
                    tolerance = _tolerance,  
                    collapsed_point_option = _collapsed_point_option)
            ## MakeLayerFeature ##
            outPathSimplifyLayer = "in_memory\\outPathSimplifyTempLayer"
            arcpy.MakeFeatureLayer_management(outPathSimplify, outPathSimplifyLayer)
            ## Update Shape Feature Class ##
            arcpy.AddMessage("\n# Update Shape Feature Class:")
            for element in listPolyLine:
                if element["DatasetName"] <> "DiaHinh":
                    arcpy.AddMessage("\n\t# Update {0}...".format(element["LayerName"]))
                    ### MakeLayerFeature ###
                    layerPath = duongDanNguon + "/" +  element["DatasetName"] + "/" + element["LayerName"]
                    arcpy.MakeFeatureLayer_management(layerPath, element["featureLayer"])
                    ### Select ###
                    strQuery = element["FID_XXX"] + " IS NOT NULL"
                    arcpy.SelectLayerByAttribute_management(outPathSimplifyLayer, "NEW_SELECTION", strQuery)
                    ### Copy To Table Temp ###
                    outTableTemp = "in_memory\\outTableTemp"
                    arcpy.CopyFeatures_management(outPathSimplifyLayer, outTableTemp)
                    ### ... ###
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
            arcpy.AddMessage("\n# Hoan thanh Simplify Polyline!!!")
            
            ############################################## Snap Line to Polygon #############################
            arcpy.AddMessage("\n# Bat dau Snap")

            self.SnapLineVsPhuBeMat()

            ##
            distanceArr = self.snap_distance.split(" ")
            distanceNumber = float(distanceArr[0])

            ## Add Code ##
            # 1. Chuyen dong Polygon sau Simplify thanh line (in_features = outPathSimplify, out_feature_class = )
            print "PolygonToLine_management"
            # Khong chon nhung Feature cua PhuBeMat
            outLayer = "outLayer"
            arcpy.MakeFeatureLayer_management(in_features = outPathSimplifyPolygon,
                                              out_layer = outLayer)
            arcpy.SelectLayerByAttribute_management(in_layer_or_view = outLayer,
                                                    selection_type = "NEW_SELECTION",
                                                    where_clause = "IS_Buffer IS NULL")
            #arcpy.SelectLayerByAttribute_management(in_layer_or_view = outLayer,
            #                                        selection_type = "REMOVE_FROM_SELECTION",
            #                                        where_clause = "FID_PhuBeMat IS NOT NULL")                                       
            polygonToLine = os.path.join(duongDanNguon, "polygonToLine")
            #polygonToLine = "in_memory\\polygonToLine"
            arcpy.PolygonToLine_management(in_features = outLayer,
                                           out_feature_class = polygonToLine)
            print "DeleteIdentical_management"                               
            arcpy.DeleteIdentical_management(in_dataset = polygonToLine,
                                             fields = "Shape")
            # temp = {
                # "LayerType": objConfig["LayerType"],
                # "DatasetName": objConfig["DatasetName"],
                # "LayerName": objConfig["LayerName"],
                # "featureLayer": "in_memory\\" + objConfig["LayerName"] + "_Layer",
                # "featureCopy": "in_memory\\" + objConfig["LayerName"] + "_Copy",
                # "featureCopyLayer": "in_memory\\" + objConfig["LayerName"] + "_Copy_Layer",
                # "FID_XXX": "FID_" + objConfig["LayerName"]
            # }
            ## End ##
            
            for elementPolygon in listPolygon:
                if elementPolygon["LayerType"] == "Polyline":
                    lineLayerName = elementPolygon["LayerName"][:elementPolygon["LayerName"].find('_Buffer')]
                    print "#### {}".format(str(lineLayerName))
                    if (elementPolygon["DatasetName"] <> "DiaHinh"):
                        arcpy.AddMessage("\n\t# Snap: {0}".format(lineLayerName))
                        layerBufferPath = duongDanNguon + "/" +  elementPolygon["DatasetName"] + "/" + elementPolygon["LayerName"]
                        print "#### {}".format(str(layerBufferPath))
                        if not arcpy.Exists(layerBufferPath) or int(arcpy.GetCount_management(layerBufferPath).getOutput(0)) == 0:
                            continue
                        # Chuyển từng buffer thành line:
                        layerBufferPathLine = "in_memory\\layerBufferPathLine"
                        arcpy.PolygonToLine_management(layerBufferPath, layerBufferPathLine)
                        # Intersect
                        outPutIntersect = "in_memory\\outPutIntersect"
                        arcpy.Intersect_analysis(in_features = [layerBufferPathLine, polygonToLine],
                                                 out_feature_class = outPutIntersect,
                                                 join_attributes = "#",
                                                 cluster_tolerance = "#",
                                                 output_type = "#")
                        outPutDissolve = os.path.join(duongDanNguon, lineLayerName + "Intersect")
                        arcpy.Dissolve_management(in_features = outPutIntersect,
                                                  out_feature_class = outPutDissolve,
                                                  dissolve_field = None,
                                                  statistics_fields = None,
                                                  multi_part = "SINGLE_PART",
                                                  unsplit_lines = None)
                        #
                        layerLinePath = duongDanNguon + "/" +  elementPolygon["DatasetName"] + "/" + lineLayerName
                        if lineLayerName != "DoanTimDuongBo" and lineLayerName != "SongSuoiL" and lineLayerName != "KenhMuongL":
                            print "{}".format(str(lineLayerName))
                            arcpy.Densify_edit(layerLinePath, "DISTANCE", str(distanceNumber / 4) + " " + distanceArr[1])
                        arcpy.Snap_edit(layerLinePath, [[outPutDissolve, "EDGE", str(distanceNumber) + " " + distanceArr[1]]])
                        arcpy.Snap_edit(layerLinePath, [[outPutDissolve, "VERTEX", str(distanceNumber / 2) + " " + distanceArr[1]]])
                        arcpy.Snap_edit(layerLinePath, [[outPutDissolve, "END", str(distanceNumber / 8) + " " + distanceArr[1]]])
        else:
            arcpy.AddMessage("\n# Khong tim thay file cau hinh: \"{0}\"".format(urlFile))
    
    # Snap: DoanTimDuongBo, SongSuoiL, KenhMuongL vs PhuBeMat
    def SnapLineVsPhuBeMat(self):
        print "# def SnapLineVsPhuBeMat"
        # Init Variable
        pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        fDPhuBeMat = "PhuBeMat"
        fDGiaoThong = "GiaoThong"
        fDThuyHe = "ThuyHe"
        fCDoanTimDuongBo = "DoanTimDuongBo"
        fCSongSuoiL = "SongSuoiL"
        fCKenhMuongL = "KenhMuongL"
        fCPhuBeMat = "PhuBeMat"
        pathDoanTimDuongBoProcess = os.path.join(os.path.join(pathProcessGDB, fDGiaoThong), fCDoanTimDuongBo)
        pathSongSuoiLProcess = os.path.join(os.path.join(pathProcessGDB, fDThuyHe), fCSongSuoiL)
        pathKenhMuongLProcess = os.path.join(os.path.join(pathProcessGDB, fDThuyHe), fCKenhMuongL)
        pathPhuBeMatProcess = os.path.join(os.path.join(pathProcessGDB, fDPhuBeMat), fCPhuBeMat)

        # Densify DoanTimDuongBo, SongSuoiL, KenhMuongL
        print "   ## Densify DoanTimDuongBo, SongSuoiL, KenhMuongL"
        distanceDensify = "2 Meters"
        arcpy.Densify_edit(in_features = pathDoanTimDuongBoProcess,
                           densification_method = "DISTANCE",
                           distance = distanceDensify)
        arcpy.Densify_edit(in_features = pathSongSuoiLProcess,
                           densification_method = "DISTANCE",
                           distance = distanceDensify)
        arcpy.Densify_edit(in_features = pathKenhMuongLProcess,
                           densification_method = "DISTANCE",
                           distance = distanceDensify)
        # Snap
        distanceSnap = "1 Meters"
        snapEnvironmentA = [pathPhuBeMatProcess, "EDGE", distanceSnap]
        snapEnvironmentB = [pathPhuBeMatProcess, "VERTEX", distanceSnap]
        snapEnvironmentC = [pathPhuBeMatProcess, "END", distanceSnap]
        ## DoanTimDuongBo
        print "   ## Snap DoanTimDuongBo"
        print "      ### Env Snap: {}".format(snapEnvironmentA)
        arcpy.Snap_edit(in_features  = pathDoanTimDuongBoProcess,
                        snap_environment = [snapEnvironmentA])
        print "      ### Env Snap: {}".format(snapEnvironmentB)
        arcpy.Snap_edit(in_features  = pathDoanTimDuongBoProcess,
                        snap_environment = [snapEnvironmentB])
        print "      ### Env Snap: {}".format(snapEnvironmentC)
        arcpy.Snap_edit(in_features  = pathDoanTimDuongBoProcess,
                        snap_environment = [snapEnvironmentC])
        ## SongSuoiL
        print "   ## Snap SongSuoiL"
        print "      ### Env Snap: {}".format(snapEnvironmentA)
        arcpy.Snap_edit(in_features  = pathSongSuoiLProcess,
                        snap_environment = [snapEnvironmentA])
        print "      ### Env Snap: {}".format(snapEnvironmentB)
        arcpy.Snap_edit(in_features  = pathSongSuoiLProcess,
                        snap_environment = [snapEnvironmentB])
        print "      ### Env Snap: {}".format(snapEnvironmentC)
        arcpy.Snap_edit(in_features  = pathSongSuoiLProcess,
                        snap_environment = [snapEnvironmentC])
        ## KenhMuongL
        print "   ## Snap KenhMuongL"
        print "      ### Env Snap: {}".format(snapEnvironmentA)
        arcpy.Snap_edit(in_features  = pathKenhMuongLProcess,
                        snap_environment = [snapEnvironmentA])
        print "      ### Env Snap: {}".format(snapEnvironmentB)
        arcpy.Snap_edit(in_features  = pathKenhMuongLProcess,
                        snap_environment = [snapEnvironmentB])
        print "      ### Env Snap: {}".format(snapEnvironmentC)
        arcpy.Snap_edit(in_features  = pathKenhMuongLProcess,
                        snap_environment = [snapEnvironmentC])
        pass
    
if __name__=='__main__':
    fPTSimplify = FPT_Simplify("8 Meters")
    fPTSimplify.simplify()
    #fPTSimplify.SnapLineVsPhuBeMat()
