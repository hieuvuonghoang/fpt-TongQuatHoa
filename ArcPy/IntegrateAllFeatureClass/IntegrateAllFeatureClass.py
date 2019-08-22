# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

class IntegrateAllFeatureClass:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathFileConfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigSimplify.json")
        self.pathFileConfigTopo = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigTopo.json")
        self.pathFileConfigTopoCopy = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ConfigTopo_Copy.json")
        self.outPutMerge = os.path.join(self.pathProcessGDB, "FeatureClassMerge")
        self.outPutSimplify = os.path.join(self.pathProcessGDB, "FeatureClassMerge_Simplify")
        # Read File Config Simplify
        if not os.path.isfile(self.pathFileConfig):
            print "... Not Found: " + self.pathFileConfig + "?\n  ... Create File ConfigSimplify..."
            self.CreateFileConfig()
        self.ReadFileConfig()
        # Read File Config Process Topo
        if not os.path.isfile(self.pathFileConfigTopo):
            print "... Not Found: " + self.pathFileConfigTopo + "?\n  ... Create File ConfigTopo..."
            self.CreateFileConfigTopo()
        self.ReadFileConfigTopo()
        pass

    def Execute(self):
        # Init Workspace
        arcpy.env.overwriteOutput = True

        ## Integrate
        #print "# Integrate"
        #arrLayerPolygon, arrLayerPolyline = self.MakeFeatureLayer()
        #self.Integrate(arrLayerPolyline, arrLayerPolygon)
        #self.Integrate(arrLayerPolygon, arrLayerPolyline)

        ## Clean InMemory
        #arcpy.Delete_management(in_data = "in_memory")

        ## PolyLine
        #print "# PolyLine"
        #inFC_SimplifyAllPolyline = self.MergeFeatureClass("Polyline")
        #inFC_ExportFC = self.SimplifyAllPolyline(inFC_SimplifyAllPolyline)
        #self.ExportFeatureClassAfterSimplify("Polyline", inFC_ExportFC)
        #self.FeatureClassSimplifyToMultiPoint("Polyline")
        #self.ErasePoint("Polyline")

        ## Clean InMemory
        #arcpy.Delete_management(in_data = "in_memory")

        ## Polygon
        #print "# Polygon"
        #inFC_SimplifyAllPolygon = self.MergeFeatureClass("Polygon")
        #inFC_ExportFC = self.SimplifyAllPolygon(inFC_SimplifyAllPolygon)
        #self.ExportFeatureClassAfterSimplify("Polygon", inFC_ExportFC)
        #self.FeatureClassSimplifyToMultiPoint("Polygon")
        #self.ErasePoint("Polygon")

        ## Clean InMemory
        #arcpy.Delete_management(in_data = "in_memory")

        ## CreateFeaturePointRemoveOne
        #print "# CreateFeaturePointRemoveOne"
        self.ProcessFeatureClassPointRemove()
        pathFc = os.path.join(os.path.join(self.pathProcessGDB, "ThuyHe"), "DuongBoNuoc_PointRemove")
        pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, "ThuyHe"), "DuongBoNuoc_PointRemove_Dissolve")
        print pathDissolve
        arcpy.Dissolve_management(in_features = pathFc,
                                  out_feature_class = pathDissolve,
                                  dissolve_field = ["FID_DuongBoNuoc"])
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
                            self.ProcessFeatureClassPointRemoveSubOne(featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine)
                            self.ProcessFeatureClassPointRemoveSubTwo(featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine)
                            pass
        pass

    # Xu ly nhung Point ma PolyLine da Remove, nhung de du quan he Topo voi Polygon thi nhung Point do can duoc giu lai
    def ProcessFeatureClassPointRemoveSubOne(self, featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine):
        # Make Feature Layer
        featureClassPolygon.SetFeatureClassSimplify()
        inFCPolygonSimplify = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolygon, featureClassPolygon.featureClassSimplify))
        inFCPolygonSimplifyLayer = "inFCPolygonSimplifyLayer"
        print inFCPolygonSimplify
        arcpy.MakeFeatureLayer_management(in_features = inFCPolygonSimplify,
                                          out_layer = inFCPolygonSimplifyLayer)
        featureClassPolyLine.SetFeatureClassPointRemove()
        inFCPolylinePointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassPointRemove))
        inFCPolylinePointRemoveLayer = "inFCPolylinePointRemoveLayer"
        print inFCPolylinePointRemove
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylinePointRemove,
                                          out_layer = inFCPolylinePointRemoveLayer)
        # Polygon To Polyline
        outFCPolygonToPolyline = "in_memory\\outFCPolygonToPolyline"
        arcpy.FeatureToLine_management(in_features = inFCPolygonSimplifyLayer,
                                       out_feature_class = outFCPolygonToPolyline,
                                       cluster_tolerance = "0.00000 Meters")
        #arcpy.PolygonToLine_management(in_features = inFCPolygonSimplifyLayer,
        #                               out_feature_class = outFCPolygonToPolyline)
        # Make Feature Layer
        outFCPolygonToPolylineLayer = "outFCPolygonToPolylineLayer"
        arcpy.MakeFeatureLayer_management(in_features = outFCPolygonToPolyline,
                                          out_layer = outFCPolygonToPolylineLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolylinePointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outFCPolygonToPolylineLayer,
                                               search_distance = "0.00000 Meters",
                                               selection_type = "NEW_SELECTION")
        # Copy Feature Class
        outFCCopy = "in_memory\\outFCCopy"
        arcpy.CopyFeatures_management(in_features = inFCPolylinePointRemoveLayer,
                                      out_feature_class = outFCCopy)
        # Erase
        featureClassPolyLine.SetFeatureClassPointRemoveOne()
        outErase = "in_memory\\outErase"
        #outErase = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassPointRemoveOne))
        arcpy.Erase_analysis(in_features = inFCPolylinePointRemove,
                             erase_features = outFCCopy,
                             out_feature_class = outErase)
        # Copy Override
        arcpy.CopyFeatures_management(in_features = outErase,
                                      out_feature_class = inFCPolylinePointRemove)
        # Clean InMemory
        arcpy.Delete_management("in_memory")
        pass

    # Xu ly nhung Point ma Polyline da khong Remove, nhung de du quan he Topo voi Polygon thi nhung Point do can duoc Remove
    def ProcessFeatureClassPointRemoveSubTwo(self, featureDataSetPolygon, featureClassPolygon, featureDataSetPolyLine, featureClassPolyLine):
        # Make Feature Layer
        featureClassPolyLine.SetFeatureClassSimplify()
        inFCPolylineSimplify = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassSimplify))
        inFCPolylineSimplifyLayer = "inFCPolylineSimplifyLayer"
        print inFCPolylineSimplify
        arcpy.MakeFeatureLayer_management(in_features = inFCPolylineSimplify,
                                          out_layer = inFCPolylineSimplifyLayer)
        featureClassPolygon.SetFeatureClassPointRemove()
        inFCPolygonPointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolygon, featureClassPolygon.featureClassPointRemove))
        inFCPolygonPointRemoveLayer = "inFCPolygonPointRemoveLayer"
        print inFCPolygonPointRemove
        arcpy.MakeFeatureLayer_management(in_features = inFCPolygonPointRemove,
                                          out_layer = inFCPolygonPointRemoveLayer)
        # Select By Location
        arcpy.SelectLayerByLocation_management(in_layer = inFCPolygonPointRemoveLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = inFCPolylineSimplifyLayer,
                                               search_distance = "0.00000 Meters",
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
                                               search_distance = "0.00000 Meters",
                                               selection_type = "NEW_SELECTION")
        # Insert Cursor
        fieldName, fieldType = self.GetFieldFID(featureClassPolyLine.featureClass, "")
        featureClassPolyLine.SetFeatureClassPointRemove()
        inFCPolylineSimplifyPointRemove = os.path.join(self.pathProcessGDB, os.path.join(featureDataSetPolyLine, featureClassPolyLine.featureClassPointRemove))
        with arcpy.da.SearchCursor(inFCPolylineSimplifyAllPointLayer, ["Shape@", fieldName]) as cursorA:
            with arcpy.da.InsertCursor(inFCPolylineSimplifyPointRemove, ["Shape@", fieldName]) as cursorB:
                for rowA in cursorA:
                    cursorB.insertRow((rowA[0], rowA[1]))
        # Clean InMemory
        arcpy.Delete_management("in_memory")
        pass

    def ErasePoint(self, option):
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if (tempPolygon.runFeatureClass == False):
                        continue
                    tempPolygon.SetFeatureClassAllPoint()
                    tempPolygon.SetFeatureClassSimplifyAllPoint()
                    tempPolygon.SetFeatureClassPointRemove()
                    pathInFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassAllPoint)
                    pathEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplifyAllPoint)
                    pathOutEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassPointRemove)
                    print pathOutEraseFeature
                    arcpy.Erase_analysis(in_features = pathInFeature,
                                         erase_features = pathEraseFeature,
                                         out_feature_class = pathOutEraseFeature,
                                         cluster_tolerance = "0.00000 Meters")
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if (tempPolyline.runFeatureClass == False):
                        continue
                    tempPolyline.SetFeatureClassAllPoint()
                    tempPolyline.SetFeatureClassSimplifyAllPoint()
                    tempPolyline.SetFeatureClassPointRemove()
                    pathInFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassAllPoint)
                    pathEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplifyAllPoint)
                    pathOutEraseFeature = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassPointRemove)
                    print pathOutEraseFeature
                    arcpy.Erase_analysis(in_features = pathInFeature,
                                         erase_features = pathEraseFeature,
                                         out_feature_class = pathOutEraseFeature,
                                         cluster_tolerance = "0.00000 Meters")
        pass

    def FeatureClassSimplifyToMultiPoint(self, option):
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if (tempPolygon.runFeatureClass == False):
                        continue
                    tempPolygon.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplify)
                    tempPolygon.SetFeatureClassSimplifyAllPoint()
                    pathOutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplifyAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = pathFcOrigin,
                                                             out_feature_class = pathOutFVToPoint,
                                                             point_location = "ALL")
                    #fieldFID, fieldType = self.GetFieldFID(tempPolygon.featureClass, "LONG")
                    #tempPolygon.SetFeatureClassSimplifyAllPoint()
                    #pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassSimplifyAllPoint)
                    #print pathDissolve
                    #arcpy.Dissolve_management(in_features = pathFc,
                    #                          out_feature_class = pathDissolve,
                    #                          dissolve_field = [fieldFID])
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if (tempPolyline.runFeatureClass == False):
                        continue
                    tempPolyline.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplify)
                    tempPolyline.SetFeatureClassSimplifyAllPoint()
                    pathOutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplifyAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = pathFcOrigin,
                                                             out_feature_class = pathOutFVToPoint,
                                                             point_location = "ALL")
                    #fieldFID, fieldType = self.GetFieldFID(tempPolyline.featureClass, "LONG")
                    #tempPolyline.SetFeatureClassSimplifyAllPoint()
                    #pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassSimplifyAllPoint)
                    #print pathDissolve
                    #arcpy.Dissolve_management(in_features = pathFc,
                    #                          out_feature_class = pathDissolve,
                    #                          dissolve_field = [fieldFID])
        pass

    def SimplifyAllPolyline(self, inFC_SimplifyAllPolyline):
        outPutSimplify = os.path.join(self.pathProcessGDB, "AllPolyline_Simplify")
        arcpy.SimplifyLine_cartography(in_features = inFC_SimplifyAllPolyline,
                                       out_feature_class = outPutSimplify,
                                       algorithm = "BEND_SIMPLIFY",
                                       tolerance = "50 Meters",
                                       collapsed_point_option = "NO_KEEP")
        return outPutSimplify
        pass

    def SimplifyAllPolygon(self, inFC_SimplifyAllPolygon):
        outPutSimplify = os.path.join(self.pathProcessGDB, "AllPolygon_Simplify")
        arcpy.SimplifyPolygon_cartography(in_features = inFC_SimplifyAllPolygon,
                                          out_feature_class = outPutSimplify,
                                          algorithm = "BEND_SIMPLIFY",
                                          tolerance = "50 Meters",
                                          error_option = "RESOLVE_ERRORS",
                                          collapsed_point_option = "NO_KEEP")
        return outPutSimplify
        pass

    def ExportFeatureClassAfterSimplify(self, option, inFC_ExportFC):
        outMergeSimplifyLayer = "outMergeSimplifyLayer"
        arcpy.MakeFeatureLayer_management(in_features = inFC_ExportFC,
                                          out_layer = outMergeSimplifyLayer)
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if tempPolygon.runFeatureClass == False:
                        continue
                    # Create Feature Class
                    tempPolygon.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                    outPath = os.path.join(self.pathProcessGDB, tempConfig.featureDataSet)
                    outName = tempPolygon.featureClassSimplify
                    pathFcSimplify = os.path.join(outPath, outName)
                    arcpy.CreateFeatureclass_management(out_path = outPath,
                                                        out_name = outName,
                                                        geometry_type = "Polygon",
                                                        spatial_reference = arcpy.Describe(pathFcOrigin).spatialReference)
                    fieldFID, fieldType = self.GetFieldFID(tempPolygon.featureClass, "LONG")
                    arcpy.AddField_management(pathFcSimplify, fieldFID, fieldType)
                    # Select
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "CLEAR_SELECTION")
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "NEW_SELECTION",
                                                            where_clause = fieldFID + " IS NOT NULL")
                    print pathFcSimplify
                    with arcpy.da.SearchCursor(outMergeSimplifyLayer, ["Shape@", fieldFID]) as cursorSearch:
                        with arcpy.da.InsertCursor(pathFcSimplify, ["Shape@", fieldFID]) as cursorInsert:
                            for rowSearch in cursorSearch:
                                cursorInsert.insertRow((rowSearch[0], rowSearch[1]))
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if tempPolyline.runFeatureClass == False:
                        continue
                    # Create Feature Class
                    tempPolyline.SetFeatureClassSimplify()
                    pathFcOrigin = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClass)
                    outPath = os.path.join(self.pathProcessGDB, tempConfig.featureDataSet)
                    outName = tempPolyline.featureClassSimplify
                    pathFcSimplify = os.path.join(outPath, outName)
                    arcpy.CreateFeatureclass_management(out_path = outPath,
                                                        out_name = outName,
                                                        geometry_type = "Polyline",
                                                        spatial_reference = arcpy.Describe(pathFcOrigin).spatialReference)
                    fieldFID, fieldType = self.GetFieldFID(tempPolyline.featureClass, "LONG")
                    arcpy.AddField_management(pathFcSimplify, fieldFID, fieldType)
                    # Select
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "CLEAR_SELECTION")
                    arcpy.SelectLayerByAttribute_management(in_layer_or_view = outMergeSimplifyLayer,
                                                            selection_type = "NEW_SELECTION",
                                                            where_clause = fieldFID + " IS NOT NULL")
                    print pathFcSimplify
                    with arcpy.da.SearchCursor(outMergeSimplifyLayer, ["Shape@", fieldFID]) as cursorSearch:
                        with arcpy.da.InsertCursor(pathFcSimplify, ["Shape@", fieldFID]) as cursorInsert:
                            for rowSearch in cursorSearch:
                                cursorInsert.insertRow((rowSearch[0], rowSearch[1]))
        pass

    def MergeFeatureClass(self, option):
        inFeatureClassMerges = []
        if option == "Polygon":
            for tempConfig in self.configTools.listConfig:
                for tempPolygon in tempConfig.listPolygon:
                    if tempPolygon.runFeatureClass == False:
                        continue
                    # Add Field FID_XXX For Feature Class
                    pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClass)
                    print pathFc
                    fieldFID, fieldType = self.GetFieldFID(tempPolygon.featureClass, "LONG")
                    arcpy.AddField_management(pathFc, fieldFID, fieldType)
                    # Update Field FID_XXX
                    with arcpy.da.UpdateCursor(pathFc, ['OID@', fieldFID]) as cursor:
                        for row in cursor:
                            row[1] = row[0]
                            cursor.updateRow(row)
                    # Copy FeatureClass to in_memory
                    tempPolygon.SetFeatureClassInMemory()
                    arcpy.CopyFeatures_management(in_features = pathFc, out_feature_class = tempPolygon.featureClassInMemory)
                    # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                    fields = arcpy.ListFields(tempPolygon.featureClassInMemory)
                    fieldsDelete = []
                    for fieldTemp in fields:
                        if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                            fieldsDelete.append(fieldTemp.name)
                    arcpy.DeleteField_management(in_table = tempPolygon.featureClassInMemory, drop_field = fieldsDelete)
                    # Feature Vertices To Point
                    tempPolygon.SetFeatureClassAllPoint()
                    outPutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = tempPolygon.featureClassInMemory,
                                                             out_feature_class = outPutFVToPoint,
                                                             point_location = "ALL")
                    #tempPolygon.SetFeatureClassAllPoint()
                    #pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolygon.featureClassAllPoint)
                    #arcpy.Dissolve_management(in_features = outPutFVToPoint,
                    #                          out_feature_class = pathDissolve,
                    #                          dissolve_field = [fieldFID])
                    # FeatureClass Delete Field FID_XXX
                    arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                    # Maker Layer
                    inFeatureClassMerges.append(tempPolygon.featureClassInMemory)
            # Merge
            outputMerge = os.path.join(self.pathProcessGDB, "PolygonMerge")
            arcpy.Merge_management(inputs = inFeatureClassMerges,
                                   output = outputMerge)
        elif option == "Polyline":
            for tempConfig in self.configTools.listConfig:
                for tempPolyline in tempConfig.listPolyline:
                    if tempPolyline.runFeatureClass == False:
                        continue
                    # Add Field FID_XXX For Feature Class
                    pathFc = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClass)
                    print pathFc
                    fieldFID, fieldType = self.GetFieldFID(tempPolyline.featureClass, "LONG")
                    arcpy.AddField_management(pathFc, fieldFID, fieldType)
                    # Update Field FID_XXX
                    with arcpy.da.UpdateCursor(pathFc, ['OID@', fieldFID]) as cursor:
                        for row in cursor:
                            row[1] = row[0]
                            cursor.updateRow(row)
                    # Copy FeatureClass to in_memory
                    tempPolyline.SetFeatureClassInMemory()
                    arcpy.CopyFeatures_management(in_features = pathFc, out_feature_class = tempPolyline.featureClassInMemory)
                    # FeatureClassTemp Delete Field Not FID_XXX, OBJECTID, Shape
                    fields = arcpy.ListFields(tempPolyline.featureClassInMemory)
                    fieldsDelete = []
                    for fieldTemp in fields:
                        if fieldTemp.name != fieldFID and fieldTemp.type != "OID" and fieldTemp.type != "Geometry":
                            fieldsDelete.append(fieldTemp.name)
                    arcpy.DeleteField_management(in_table = tempPolyline.featureClassInMemory, drop_field = fieldsDelete)
                    # Feature Vertices To Point
                    tempPolyline.SetFeatureClassAllPoint()
                    outPutFVToPoint = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassAllPoint)
                    arcpy.FeatureVerticesToPoints_management(in_features = tempPolyline.featureClassInMemory,
                                                             out_feature_class = outPutFVToPoint,
                                                             point_location = "ALL")
                    #tempPolyline.SetFeatureClassAllPoint()
                    #pathDissolve = os.path.join(os.path.join(self.pathProcessGDB, tempConfig.featureDataSet), tempPolyline.featureClassAllPoint)
                    #arcpy.Dissolve_management(in_features = outPutFVToPoint,
                    #                          out_feature_class = pathDissolve,
                    #                          dissolve_field = [fieldFID])
                    # FeatureClass Delete Field FID_XXX
                    arcpy.DeleteField_management(in_table = pathFc, drop_field = fieldFID)
                    # Maker Layer
                    inFeatureClassMerges.append(tempPolyline.featureClassInMemory)
            # Merge
            outputMerge = os.path.join(self.pathProcessGDB, "PolylineMerge")
            arcpy.Merge_management(inputs = inFeatureClassMerges,
                                   output = outputMerge)
        return outputMerge
        pass

    def MakeFeatureLayer(self):
        arrLayerPolygon = []
        arrLayerPolyline = []
        for tempConfig in self.configTools.listConfig:
            for tempPolygon in tempConfig.listPolygon:
                if tempPolygon.runFeatureClass == False:
                    continue
                tempPolygon.SetFeatureLayer()
                pathPolygon = os.path.join(self.pathProcessGDB, os.path.join(tempConfig.featureDataSet, tempPolygon.featureClass))
                arcpy.MakeFeatureLayer_management(in_features = pathPolygon,
                                                  out_layer = tempPolygon.featureLayer)
                arrLayerPolygon.append(tempPolygon.featureLayer)
            for tempPolyline in tempConfig.listPolyline:
                if tempPolyline.runFeatureClass == False:
                    continue
                tempPolyline.SetFeatureLayer()
                pathPolyline = os.path.join(self.pathProcessGDB, os.path.join(tempConfig.featureDataSet, tempPolyline.featureClass))
                arcpy.MakeFeatureLayer_management(in_features = pathPolyline,
                                                  out_layer = tempPolyline.featureLayer)
                arrLayerPolyline.append(tempPolyline.featureLayer)
        return arrLayerPolygon, arrLayerPolyline
        pass

    def Integrate(self, arrOne, arrTwo):
        arrInput = []
        for item in arrOne:
            arrInput.append([item, "1"])
        for item in arrTwo:
            arrInput.append([item, "2"])
        arcpy.Integrate_management(in_features = arrInput,
                                   cluster_tolerance = "0.00000 Meters")
        pass

    def GetFieldFID(self, featureClass, fieldType):
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

    def CreateFileConfig(self):
        self.configTools = ConfigTools()
        for fcDataSetTemp in arcpy.Describe(self.pathProcessGDB).children:
            elemListConfig = ElemListConfig(fcDataSetTemp.baseName)
            for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polygon":
                    elemListPolygon = ElemList(fcTemp.baseName, True)
                    elemListConfig.InsertElemListPolygon(elemListPolygon)
                if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                    elemListPolyline = ElemList(fcTemp.baseName, True)
                    elemListConfig.InsertElemListPolyline(elemListPolyline)
            if len(elemListConfig.listPolygon) > 0:
                self.configTools.InsertElemListConfig(elemListConfig)
        textConfig = json.dumps(obj = self.configTools.GetDict(), indent = 4, sort_keys = True)
        file = open(self.pathFileConfig, "w")
        file.write(textConfig)
        file.close()
        pass

    def ReadFileConfig(self):
        self.configTools = ConfigTools()
        file = open(self.pathFileConfig, "r")
        textConfig = file.read()
        file.close()
        self.configTools.InitFromDict(json.loads(textConfig))
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

    def SetFeatureClassPointRemoveOne(self):
        self.featureClassPointRemoveOne = self.featureClass + "_PointRemove_One"
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

    def SetFeatureClassPointRemoveOne(self):
        self.featureClassPointRemoveOne = self.featureClass + "_PointRemove_One"
        pass

class ConfigTools:

    def __init__(self):
        self.listConfig = []

    def InsertElemListConfig(self, elemListConfig):
        self.listConfig.append(elemListConfig)

    def GetDict(self):
        listTemp = []
        for elemListConfig in self.listConfig:
            listTemp.append(elemListConfig.GetDict())
        return listTemp;

    def InitFromDict(self, dataJson):
        self.listConfig = []
        for elemListConfigTemp in dataJson:
            elemListConfig = ElemListConfig(elemListConfigTemp['featureDataSet'])
            for elemListPolygonTemp in elemListConfigTemp['listPolygon']:
                elemListPolygon = ElemList(elemListPolygonTemp['featureClass'], elemListPolygonTemp['runFeatureClass'])
                elemListConfig.InsertElemListPolygon(elemListPolygon)
            for elemListPolygonTemp in elemListConfigTemp['listPolyline']:
                elemListPolyline = ElemList(elemListPolygonTemp['featureClass'], elemListPolygonTemp['runFeatureClass'])
                elemListConfig.InsertElemListPolyline(elemListPolyline)
            self.InsertElemListConfig(elemListConfig)

class ElemListConfig:

    def __init__(self, featureDataSet):
        self.featureDataSet = featureDataSet
        self.listPolygon = []
        self.listPolyline = []

    def InsertElemListPolygon(self, elemListPolygon):
        self.listPolygon.append(elemListPolygon)

    def InsertElemListPolyline(self, elemListPolyline):
        self.listPolyline.append(elemListPolyline)

    def GetDict(self):
        listTempPolygon = []
        listTempPolyline = []
        for elemList in self.listPolygon:
            listTempPolygon.append(elemList.__dict__)
        for elemList in self.listPolyline:
            listTempPolyline.append(elemList.__dict__)
        return {
            "featureDataSet": self.featureDataSet,
            "listPolygon": listTempPolygon,
            "listPolyline": listTempPolyline
        }

class ElemList:

    def __init__(self, featureClass, runFeatureClass):
        self.featureClass = featureClass
        self.runFeatureClass = runFeatureClass
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

    def SetFeatureClassPointRemoveOne(self):
        self.featureClassPointRemoveOne = self.featureClass + "_PointRemove_One"
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
    integrateAllFeatureClass = IntegrateAllFeatureClass()
    print "Running..."
    integrateAllFeatureClass.Execute()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass