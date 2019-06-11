# -*- coding: utf-8 -*-

import arcpy
import os
import json

class RanhGioiPhuBeMat:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDPhuBeMat = "PhuBeMat"
        self.fCPhuBeMat = "PhuBeMat"
        self.fCRanhGioiPhuBeMat = "RanhGioiPhuBeMat"
        # Path Process
        self.pathPhuBeMatProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDPhuBeMat), self.fCPhuBeMat)
        self.pathRanhGioiPhuBeMatProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDPhuBeMat), self.fCRanhGioiPhuBeMat)
        # Path Final
        self.pathPhuBeMatFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDPhuBeMat), self.fCPhuBeMat)
        self.pathRanhGioiPhuBeMatFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDPhuBeMat), self.fCRanhGioiPhuBeMat)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Copy Feature Class
        arcpy.CopyFeatures_management(in_features = self.pathRanhGioiPhuBeMatProcess,
                                      out_feature_class = self.pathRanhGioiPhuBeMatFinal)
        self.CreateFCPointRemove()
        self.UpdateShapeRanhGioiPhuBeMatFinal()
        self.SelectLineSnap()
        self.SnapRanhGioiPhuBeMatFinal()
        pass

    def CreateFCPointRemove(self):
        print "\tCreateFCPointRemove"
        # Add Point For RanhGioiPhuBeMat Final
        ## Make Feature Layer
        self.phuBeMatProcessLayer = "PhuBeMatProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathPhuBeMatProcess,
                                          out_layer = self.phuBeMatProcessLayer)
        self.ranhGioiPhuBeMatFinalLayer = "RanhGioiPhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatFinal,
                                          out_layer = self.ranhGioiPhuBeMatFinalLayer)
        ## Feature Vertices To Points: fCPhuBeMat
        fCPhuBeMatProcessPoints = "in_memory\\PhuBeMatProcessPoints"
        arcpy.FeatureVerticesToPoints_management(in_features = self.phuBeMatProcessLayer,
                                                 out_feature_class = fCPhuBeMatProcessPoints,
                                                 point_location = "ALL")
        ## Add Point For RanhGioiPhuBeMat using Integrate Tool
        arcpy.Integrate_management(in_features = [[self.ranhGioiPhuBeMatFinalLayer, 1], [fCPhuBeMatProcessPoints, 2]],
                                   cluster_tolerance = "0 Meters")
        
        # Create Feature Class Point Remove
        ## Make Feature Layer
        self.phuBeMatFinalLayer = "PhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathPhuBeMatFinal,
                                          out_layer = self.phuBeMatFinalLayer)
        ## Feature To Line
        self.fCPhuBeMatFinalFeatureToLine = "in_memory\\PhuBeMatFinalFeatureToLine"
        arcpy.FeatureToLine_management(in_features = self.phuBeMatFinalLayer,
                                       out_feature_class = self.fCPhuBeMatFinalFeatureToLine,
                                       cluster_tolerance = "0 Meters")
        self.phuBeMatFinalFeatureToLineLayer = "PhuBeMatFinalFeatureToLineLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCPhuBeMatFinalFeatureToLine,
                                          out_layer = self.phuBeMatFinalFeatureToLineLayer)
        ## Feature Vertices To Points: RanhGioiPhuBeMat Final
        fCRanhGioiPhuBeMatFinalPointsALL = "in_memory\\RanhGioiPhuBeMatFinalPointsALL"
        arcpy.FeatureVerticesToPoints_management(in_features = self.ranhGioiPhuBeMatFinalLayer,
                                                 out_feature_class = fCRanhGioiPhuBeMatFinalPointsALL,
                                                 point_location = "ALL")
        fCRanhGioiPhuBeMatFinalPointsBOTHENDS = "in_memory\\RanhGioiPhuBeMatFinalPointsBOTHENDS"
        arcpy.FeatureVerticesToPoints_management(in_features = self.ranhGioiPhuBeMatFinalLayer,
                                                 out_feature_class = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                                                 point_location = "BOTH_ENDS")
        fCRanhGioiPhuBeMatFinalPoints = "in_memory\\RanhGioiPhuBeMatFinalPoints"
        arcpy.Erase_analysis(in_features = fCRanhGioiPhuBeMatFinalPointsALL,
                             erase_features = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                             out_feature_class = fCRanhGioiPhuBeMatFinalPoints)
        ranhGioiPhuBeMatFinalPointsLayer = "RanhGioiPhuBeMatFinalPointsLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCRanhGioiPhuBeMatFinalPoints,
                                          out_layer = ranhGioiPhuBeMatFinalPointsLayer)
        ## Select fCRanhGioiPhuBeMatFinalPoints
        arcpy.SelectLayerByLocation_management(in_layer = ranhGioiPhuBeMatFinalPointsLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.phuBeMatFinalFeatureToLineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        self.fCPointRemove = "in_memory\\PointRemove"
        arcpy.CopyFeatures_management(in_features = ranhGioiPhuBeMatFinalPointsLayer,
                                      out_feature_class = self.fCPointRemove)
        pass

    def UpdateShapeRanhGioiPhuBeMatFinal(self):
        print "\tUpdateShapeRanhGioiPhuBeMatFinal"
        self.ranhGioiPhuBeMatFinalLayer = "RanhGioiPhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatFinal,
                                          out_layer = self.ranhGioiPhuBeMatFinalLayer)
        self.pointRemoveLayer = "PointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCPointRemove,
                                          out_layer = self.pointRemoveLayer)
        arcpy.SelectLayerByLocation_management(in_layer = self.ranhGioiPhuBeMatFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.pointRemoveLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION")
        with arcpy.da.UpdateCursor(self.ranhGioiPhuBeMatFinalLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.ranhGioiPhuBeMatFinalLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = self.pointRemoveLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = self.ranhGioiPhuBeMatFinalLayer,
                                                       search_distance = "0 Meters",
                                                       selection_type = "NEW_SELECTION")
                if int(arcpy.GetCount_management(self.pointRemoveLayer).getOutput(0)) == 0:
                    continue
                listPart = []
                for rowASub in rowA[1]:
                    listPoint = []
                    for rowASubSub in rowASub:
                        found = False
                        with arcpy.da.UpdateCursor(self.pointRemoveLayer, ["OID@", "SHAPE@"]) as cursorB:
                            for rowB in cursorB:
                                if rowB[1].equals(rowASubSub):
                                    found = True
                                    cursorB.deleteRow()
                                    break
                        if found == False:
                            listPoint.append(rowASubSub)
                    if len(listPoint) > 0:
                        listPart.append(listPoint)
                rowA[1] = arcpy.Polyline(arcpy.Array(listPart))
                cursorA.updateRow(rowA)
        pass

    def SelectLineSnap(self):
        print "\tSelectLineSnap"
        self.ranhGioiPhuBeMatFinalLayer = "RanhGioiPhuBeMatFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathRanhGioiPhuBeMatFinal,
                                          out_layer = self.ranhGioiPhuBeMatFinalLayer)
        fCRanhGioiPhuBeMatFinalPointsBOTHENDS = "in_memory\\RanhGioiPhuBeMatFinalPointsBOTHENDS"
        arcpy.FeatureVerticesToPoints_management(in_features = self.ranhGioiPhuBeMatFinalLayer,
                                                 out_feature_class = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                                                 point_location = "BOTH_ENDS")
        ranhGioiPhuBeMatFinalPointsBOTHENDSLayer = "RanhGioiPhuBeMatFinalPointsBOTHENDSLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCRanhGioiPhuBeMatFinalPointsBOTHENDS,
                                          out_layer = ranhGioiPhuBeMatFinalPointsBOTHENDSLayer)
        arcpy.SelectLayerByLocation_management(in_layer = ranhGioiPhuBeMatFinalPointsBOTHENDSLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = self.phuBeMatFinalFeatureToLineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        arcpy.SelectLayerByLocation_management(in_layer = self.ranhGioiPhuBeMatFinalLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = ranhGioiPhuBeMatFinalPointsBOTHENDSLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        pass

    def SnapRanhGioiPhuBeMatFinal(self):
        print "\tSnapRanhGioiPhuBeMatFinal"
        distance = "100 Meters"
        snapEnv = [self.phuBeMatFinalLayer, "EDGE", distance]
        with arcpy.da.SearchCursor(self.ranhGioiPhuBeMatFinalLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.ranhGioiPhuBeMatFinalLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = self.phuBeMatFinalLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = self.ranhGioiPhuBeMatFinalLayer,
                                                       search_distance = distance,
                                                       selection_type = "NEW_SELECTION",
                                                       invert_spatial_relationship = "NOT_INVERT")
                arcpy.Snap_edit(self.ranhGioiPhuBeMatFinalLayer, [snapEnv])
        pass

if __name__ == "__main__":
    ranhGioiPhuBeMat = RanhGioiPhuBeMat()
    ranhGioiPhuBeMat.Execute()
    pass