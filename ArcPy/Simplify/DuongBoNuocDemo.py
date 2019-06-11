import arcpy
import os
import sys

class DuongBoNuoc:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCSongSuoiA = "SongSuoiA"
        self.fCBaiBoiA = "BaiBoiA"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        self.fCKenhMuongA = "KenhMuongA"
        self.pathKenhMuongAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMatNuocTinhFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathBaiBoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCBaiBoiA)
        self.pathDuongBoNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        self.pathKenhMuongAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCKenhMuongA)
        self.pathMatNuocTinhProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCMatNuocTinh)
        self.pathSongSuoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCSongSuoiA)
        self.pathBaiBoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCBaiBoiA)
        self.pathDuongBoNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongBoNuoc)

    def Execute(self):
        print "DuongBoNuoc:"
        self.CreateFeaturePointRemove()
        self.UpdateShapeDuongBoNuocFinal()
        self.SelectLineSnap()
        self.SnapDuongBoNuoc()

    def CreateFeaturePointRemove(self):
        print "\tCreateFeaturePointRemove"
        # Using Merge Tool
        inputsMerge = [self.pathBaiBoiAFinal, self.pathMatNuocTinhFinal, self.pathSongSuoiAFinal, self.pathKenhMuongAFinal]
        self.outPutMergeTempA = "in_memory\\OutPutMergeTempA"
        arcpy.Merge_management(inputs = inputsMerge,
                               output = self.outPutMergeTempA)
        # Using Feature To Line
        self.outPutFeatureToLineTempA = "in_memory\\OutPutFeatureToLineTempA"
        arcpy.FeatureToLine_management(in_features = self.outPutMergeTempA,
                                       out_feature_class = self.outPutFeatureToLineTempA)
        # Using Merge Tool
        inputsMerge = [self.pathBaiBoiAProcess, self.pathMatNuocTinhProcess, self.pathSongSuoiAProcess, self.pathKenhMuongAProcess]
        outPutMergeTempB = "in_memory\\OutPutMergeTempB"
        arcpy.Merge_management(inputs = inputsMerge,
                               output = outPutMergeTempB)
        # Using Feature To Line
        outPutFeatureToLineTempB = "in_memory\\OutPutFeatureToLineTempB"
        arcpy.FeatureToLine_management(in_features = outPutMergeTempB,
                                       out_feature_class = outPutFeatureToLineTempB)
        # Using Feature Vertices To Points
        outPutFeatureVerticesToPointsTempA = "in_memory\\OutPutFeatureVerticesToPointsTempA"
        arcpy.FeatureVerticesToPoints_management(in_features = outPutFeatureToLineTempB,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempA,
                                                 point_location = "ALL")
        # Using Integrate
        inputsIntegrate = [[self.pathDuongBoNuocProcess, 1], [outPutFeatureVerticesToPointsTempA, 2]]
        arcpy.Integrate_management(in_features = inputsIntegrate,
                                   cluster_tolerance = "0 Meters")
        # Using Copy Feature
        arcpy.CopyFeatures_management(in_features = self.pathDuongBoNuocProcess,
                                      out_feature_class = self.pathDuongBoNuocFinal)
        # Using Feature Vertices To Points
        outPutFeatureVerticesToPointsTempB = "in_memory\\OutPutFeatureVerticesToPointsTempB"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongBoNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempB,
                                                 point_location = "ALL")
        outPutFeatureVerticesToPointsTempC = "in_memory\\OutPutFeatureVerticesToPointsTempC"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongBoNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempC,
                                                 point_location = "BOTH_ENDS")
        # Using Erase
        outPutEraseA = "in_memory\\OutPutEraseA"
        arcpy.Erase_analysis(in_features = outPutFeatureVerticesToPointsTempB,
                             erase_features = outPutFeatureVerticesToPointsTempC,
                             out_feature_class = outPutEraseA)
        # Using Select Feature Layer By Location
        self.outLayerTempA = "OutLayerTempA"
        arcpy.MakeFeatureLayer_management(in_features = self.outPutFeatureToLineTempA,
                                          out_layer = self.outLayerTempA)
        outLayerTempB = "OutLayerTempB"
        arcpy.MakeFeatureLayer_management(in_features = outPutEraseA,
                                          out_layer = outLayerTempB)
        arcpy.SelectLayerByLocation_management(in_layer = outLayerTempB,
                                               overlap_type = "INTERSECT",
                                               select_features = self.outLayerTempA,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        self.duongBoNuocPointRemove = "in_memory\\DuongBoNuocPointRemove"
        arcpy.CopyFeatures_management(in_features = outLayerTempB,
                                      out_feature_class = self.duongBoNuocPointRemove)

    def UpdateShapeDuongBoNuocFinal(self):
        print "\tUpdateShapeDuongBoNuocFinal"
        self.duongBoNuocLayer = "DuongBoNuocLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongBoNuocFinal,
                                          out_layer = self.duongBoNuocLayer)
        self.duongBoNuocPointRemoveInMemoryLayer = "DuongBoNuocPointRemoveInMemoryLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.duongBoNuocPointRemove,
                                          out_layer = self.duongBoNuocPointRemoveInMemoryLayer)
        with arcpy.da.UpdateCursor(self.duongBoNuocLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongBoNuocLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = self.duongBoNuocPointRemoveInMemoryLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = self.duongBoNuocLayer,
                                                       search_distance = "0 Meters",
                                                       selection_type = "NEW_SELECTION")
                if int(arcpy.GetCount_management(self.duongBoNuocPointRemoveInMemoryLayer).getOutput(0)) == 0:
                    continue
                listPart = []
                for rowASub in rowA[1]:
                    listPoint = []
                    for rowASubSub in rowASub:
                        found = False
                        with arcpy.da.UpdateCursor(self.duongBoNuocPointRemoveInMemoryLayer, ["OID@", "SHAPE@"]) as cursorB:
                            for rowB in cursorB:
                                pointB = rowB[1].centroid
                                if rowASubSub.X == pointB.X and rowASubSub.Y == pointB.Y:
                                    found = True
                                    cursorB.deleteRow()
                                    break
                        if found == False:
                            listPoint.append(rowASubSub)
                    if len(listPoint) > 0:
                        listPart.append(listPoint)
                rowA[1] = arcpy.Polyline(arcpy.Array(listPart))
                cursorA.updateRow(rowA)

    def SelectLineSnap(self):
        print "\tSelectLineSnap"
        outPutFeatureVerticesToPointsTempC = "in_memory\\OutPutFeatureVerticesToPointsTempC"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongBoNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempC,
                                                 point_location = "BOTH_ENDS")
        outLayerTemp = "OutPutFeatureVerticesToPointsTempCLayer"
        arcpy.MakeFeatureLayer_management(in_features = outPutFeatureVerticesToPointsTempC,
                                          out_layer = outLayerTemp)
        arcpy.SelectLayerByLocation_management(in_layer = outLayerTemp,
                                               overlap_type = "INTERSECT",
                                               select_features = self.outLayerTempA,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.duongBoNuocLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outLayerTemp,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        pass

    def SnapDuongBoNuoc(self):
        print "\tSnapDuongBoNuoc"
        outPutMergeTempALayer = "outPutMergeTempALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.outPutMergeTempA,
                                          out_layer = outPutMergeTempALayer)
        snapEnv = [outPutMergeTempALayer, "EDGE", "100 Meters"]
        with arcpy.da.UpdateCursor(self.duongBoNuocLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongBoNuocLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.Snap_edit(self.duongBoNuocLayer, [snapEnv])

class DuongMepNuoc:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fCBaiBoiA = "BaiBoiA"
        self.fCDuongMepNuoc = "DuongMepNuoc"
        self.pathBaiBoiAFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCBaiBoiA)
        self.pathDuongMepNuocFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongMepNuoc)
        self.pathBaiBoiAProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCBaiBoiA)
        self.pathDuongMepNuocProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), self.fCDuongMepNuoc)

    def Execute(self):
        print "DuongMepNuoc:"
        self.CreateFeaturePointRemove()
        self.UpdateShapeDuongMepNuocFinal()
        self.SelectLineSnap()
        self.SnapDuongMepNuoc()

    def CreateFeaturePointRemove(self):
        print "\tCreateFeaturePointRemove"
        # Using Feature To Line
        self.outPutFeatureToLineTempA = "in_memory\\OutPutFeatureToLineTempA"
        arcpy.FeatureToLine_management(in_features = self.pathBaiBoiAFinal,
                                       out_feature_class = self.outPutFeatureToLineTempA)
        # Using Feature To Line
        self.outPutFeatureToLineTempB = "in_memory\\OutPutFeatureToLineTempB"
        arcpy.FeatureToLine_management(in_features = self.pathBaiBoiAProcess,
                                       out_feature_class = self.outPutFeatureToLineTempB)
        # Using Feature Vertices To Points
        self.outPutFeatureVerticesToPointsTempA = "in_memory\\OutPutFeatureVerticesToPointsTempA"
        arcpy.FeatureVerticesToPoints_management(in_features = self.outPutFeatureToLineTempB,
                                                 out_feature_class = self.outPutFeatureVerticesToPointsTempA,
                                                 point_location = "ALL")
        # Using Integrate
        inputsIntegrate = [[self.pathDuongMepNuocProcess, 1], [self.outPutFeatureVerticesToPointsTempA, 2]]
        arcpy.Integrate_management(in_features = inputsIntegrate,
                                   cluster_tolerance = "0 Meters")
        # Using Copy Feature
        arcpy.CopyFeatures_management(in_features = self.pathDuongMepNuocProcess,
                                      out_feature_class = self.pathDuongMepNuocFinal)
        # Using Feature Vertices To Points
        outPutFeatureVerticesToPointsTempB = "in_memory\\OutPutFeatureVerticesToPointsTempB"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongMepNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempB,
                                                 point_location = "ALL")
        outPutFeatureVerticesToPointsTempC = "in_memory\\OutPutFeatureVerticesToPointsTempC"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongMepNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempC,
                                                 point_location = "BOTH_ENDS")
        # Using Erase
        outPutEraseA = "in_memory\\OutPutEraseA"
        arcpy.Erase_analysis(in_features = outPutFeatureVerticesToPointsTempB,
                             erase_features = outPutFeatureVerticesToPointsTempC,
                             out_feature_class = outPutEraseA)
        # Using Select Feature Layer By Location
        self.outLayerTempA = "OutLayerTempA"
        arcpy.MakeFeatureLayer_management(in_features = self.outPutFeatureToLineTempA,
                                          out_layer = self.outLayerTempA)
        outLayerTempB = "OutLayerTempB"
        arcpy.MakeFeatureLayer_management(in_features = outPutEraseA,
                                          out_layer = outLayerTempB)
        arcpy.SelectLayerByLocation_management(in_layer = outLayerTempB,
                                               overlap_type = "INTERSECT",
                                               select_features = self.outLayerTempA,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        self.duongMepNuocPointRemove = "in_memory\\DuongMepNuocPointRemove"
        arcpy.CopyFeatures_management(in_features = outLayerTempB,
                                      out_feature_class = self.duongMepNuocPointRemove)

    def UpdateShapeDuongMepNuocFinal(self):
        print "\tUpdateShapeDuongBoNuocFinal"
        self.duongMepNuocLayer = "DuongMepNuocLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongMepNuocFinal,
                                          out_layer = self.duongMepNuocLayer)
        self.duongMepNuocPointRemoveInMemoryLayer = "DuongMepNuocPointRemoveInMemoryLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.duongMepNuocPointRemove,
                                          out_layer = self.duongMepNuocPointRemoveInMemoryLayer)
        with arcpy.da.UpdateCursor(self.duongMepNuocLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongMepNuocLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = self.duongMepNuocPointRemoveInMemoryLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = self.duongMepNuocLayer,
                                                       search_distance = "0 Meters",
                                                       selection_type = "NEW_SELECTION")
                if int(arcpy.GetCount_management(self.duongMepNuocPointRemoveInMemoryLayer).getOutput(0)) == 0:
                    continue
                listPart = []
                for rowASub in rowA[1]:
                    listPoint = []
                    for rowASubSub in rowASub:
                        found = False
                        with arcpy.da.UpdateCursor(self.duongMepNuocPointRemoveInMemoryLayer, ["OID@", "SHAPE@"]) as cursorB:
                            for rowB in cursorB:
                                pointB = rowB[1].centroid
                                if rowASubSub.X == pointB.X and rowASubSub.Y == pointB.Y:
                                    found = True
                                    cursorB.deleteRow()
                                    break
                        if found == False:
                            listPoint.append(rowASubSub)
                    if len(listPoint) > 0:
                        listPart.append(listPoint)
                rowA[1] = arcpy.Polyline(arcpy.Array(listPart))
                cursorA.updateRow(rowA)

    def SelectLineSnap(self):
        print "\tSelectLineSnap"
        outPutFeatureVerticesToPointsTempC = "in_memory\\OutPutFeatureVerticesToPointsTempC"
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDuongMepNuocFinal,
                                                 out_feature_class = outPutFeatureVerticesToPointsTempC,
                                                 point_location = "BOTH_ENDS")
        outLayerTemp = "OutPutFeatureVerticesToPointsTempCLayer"
        arcpy.MakeFeatureLayer_management(in_features = outPutFeatureVerticesToPointsTempC,
                                          out_layer = outLayerTemp)
        arcpy.SelectLayerByLocation_management(in_layer = outLayerTemp,
                                               overlap_type = "INTERSECT",
                                               select_features = self.outLayerTempA,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.duongMepNuocLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = outLayerTemp,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        pass

    def SnapDuongMepNuoc(self):
        print "\tSnapDuongMepNuoc"
        baiBoiALayer = "BaiBoiALayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathBaiBoiAFinal,
                                          out_layer = baiBoiALayer)
        snapEnv = [baiBoiALayer, "EDGE", "100 Meters"]
        with arcpy.da.UpdateCursor(self.duongMepNuocLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongMepNuocLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.Snap_edit(self.duongMepNuocLayer, [snapEnv])

if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    duongBoNuoc = DuongBoNuoc()
    duongBoNuoc.Execute()
    duongMepNuoc = DuongMepNuoc()
    duongMepNuoc.Execute()