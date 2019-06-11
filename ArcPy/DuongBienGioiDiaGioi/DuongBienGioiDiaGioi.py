# -*- coding: utf-8 -*-

import arcpy
import os
import json

# doiTuong: 1. C?p t?nh, 2. C?p huy?n, 3. C?p x?

class DuongBienGioiDiaGioi:
    
    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDBienGioiDiaGioi = "BienGioiDiaGioi"
        self.fCDuongBienGioi = "DuongBienGioi"
        self.fCDuongDiaGioi = "DuongDiaGioi"
        self.fCDiaPhan = "DiaPhan"
        # Path Process
        self.pathDuongBienGioiProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDuongBienGioi)
        self.pathDuongDiaGioiProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDuongDiaGioi)
        self.pathDiaPhanProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), self.fCDiaPhan)
        # Path Final
        self.pathDuongBienGioiFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDuongBienGioi)
        self.pathDuongDiaGioiFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDuongDiaGioi)
        self.pathDiaPhanFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDBienGioiDiaGioi), self.fCDiaPhan)
        pass

    def Execute(self):
        arcpy.env.overwriteOutput = True
        # Copy Feature Class
        arcpy.CopyFeatures_management(in_features = self.pathDuongDiaGioiProcess,
                                      out_feature_class = self.pathDuongDiaGioiFinal)
        # doiTuong = 3 (C?p x?)
        print "Duong Dia Gioi (Cap xa):"
        self.CreateFCPointRemove("3")
        self.UpdateShapeDuongDiaGioiFinal("3")
        self.SnapDuongDiaGioi("3")
        # doiTuong = 2 (C?p huy?n)
        print "Duong Dia Gioi (Cap huyen):"
        self.CreateFCPointRemove("2")
        self.UpdateShapeDuongDiaGioiFinal("2")
        self.SnapDuongDiaGioi("2")
        # doiTuong = 1 (C?p t?nh)
        print "Duong Dia Gioi (Cap tinh):"
        self.CreateFCPointRemove("1")
        self.UpdateShapeDuongDiaGioiFinal("1")
        self.SnapDuongDiaGioi("1")
        pass

    def CreateFCPointRemove(self, doiTuong):
        print "\tCreateFCPointRemove"
        # Add Point For DuongDiaGioi Final
        ## Make Feature Layer
        self.diaPhanProcessLayer = "DiaPhanProcessLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDiaPhanProcess,
                                          out_layer = self.diaPhanProcessLayer)
        self.duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongDiaGioiFinal,
                                          out_layer = self.duongDiaGioiFinalLayer)
        ## Select Layer
        sqlQuery = "doiTuong = " + doiTuong
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.diaPhanProcessLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        ## Feature Vertices To Points: fCDiaPhan
        fCDiaPhanToProcessPoints = "in_memory\\DiaPhanToProcessPoints"
        arcpy.FeatureVerticesToPoints_management(in_features = self.diaPhanProcessLayer,
                                                 out_feature_class = fCDiaPhanToProcessPoints,
                                                 point_location = "ALL")
        ## Add Point For fCDuongDiaGioi using Integrate Tool
        arcpy.Integrate_management(in_features = [[self.duongDiaGioiFinalLayer, 1], [fCDiaPhanToProcessPoints, 2]],
                                   cluster_tolerance = "0 Meters")
        
        # Create Feature Class Point Remove
        ## Make Feature Layer
        self.diaPhanFinalLayer = "DiaPhanFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDiaPhanFinal,
                                          out_layer = self.diaPhanFinalLayer)
        ## Select Layer
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        ## Feature To Line
        fCDiaPhanFinalFeatureToLine = "in_memory\\DiaPhanFinalFeatureToLine"
        arcpy.FeatureToLine_management(in_features = self.diaPhanFinalLayer,
                                       out_feature_class = fCDiaPhanFinalFeatureToLine,
                                       cluster_tolerance = "0 Meters")
        diaPhanFinalFeatureToLineLayer = "DiaPhanFinalFeatureToLineLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCDiaPhanFinalFeatureToLine,
                                          out_layer = diaPhanFinalFeatureToLineLayer)
        ## Feature Vertices To Points: DuongDiaGioi Final
        fCDuongDiaGioiFinalPointsALL = "in_memory\\DuongDiaGioiFinalPointsALL"
        arcpy.FeatureVerticesToPoints_management(in_features = self.duongDiaGioiFinalLayer,
                                                 out_feature_class = fCDuongDiaGioiFinalPointsALL,
                                                 point_location = "ALL")
        fCDuongDiaGioiFinalPointsBOTHENDS = "in_memory\\DuongDiaGioiFinalPointsBOTHENDS"
        arcpy.FeatureVerticesToPoints_management(in_features = self.duongDiaGioiFinalLayer,
                                                 out_feature_class = fCDuongDiaGioiFinalPointsBOTHENDS,
                                                 point_location = "BOTH_ENDS")
        fCDuongDiaGioiFinalPoints = "in_memory\\DuongDiaGioiFinalPoints"
        arcpy.Erase_analysis(in_features = fCDuongDiaGioiFinalPointsALL,
                             erase_features = fCDuongDiaGioiFinalPointsBOTHENDS,
                             out_feature_class = fCDuongDiaGioiFinalPoints)
        duongDiaGioiFinalPointsLayer = "DuongDiaGioiFinalPointsLayer"
        arcpy.MakeFeatureLayer_management(in_features = fCDuongDiaGioiFinalPoints,
                                          out_layer = duongDiaGioiFinalPointsLayer)
        ## Select fCDuongDiaGioiFinalPoints
        arcpy.SelectLayerByLocation_management(in_layer = duongDiaGioiFinalPointsLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = diaPhanFinalFeatureToLineLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "INVERT")
        self.fCPointRemove = "in_memory\\PointRemove"
        arcpy.CopyFeatures_management(in_features = duongDiaGioiFinalPointsLayer,
                                      out_feature_class = self.fCPointRemove)
        pass

    def UpdateShapeDuongDiaGioiFinal(self, doiTuong):
        print "\tUpdateShapeDuongDiaGioiFinal"
        self.duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongDiaGioiFinal,
                                          out_layer = self.duongDiaGioiFinalLayer)
        sqlQuery = "doiTuong = " + doiTuong
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        self.pointRemoveLayer = "PointRemoveLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.fCPointRemove,
                                          out_layer = self.pointRemoveLayer)
        with arcpy.da.UpdateCursor(self.duongDiaGioiFinalLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.SelectLayerByLocation_management(in_layer = self.pointRemoveLayer,
                                                       overlap_type = "INTERSECT",
                                                       select_features = self.duongDiaGioiFinalLayer,
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
        pass

    def SelectLineSnap(self, doiTuong):
        print "\tSelectLineSnap"
        self.duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongDiaGioiFinal,
                                          out_layer = self.duongDiaGioiFinalLayer)
        sqlQuery = "doiTuong = " + doiTuong
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        fCDiaPhanFinalFeatureToLine = "in_memory\\DiaPhanFinalFeatureToLine"
        arcpy.FeatureToLine_management(in_features = self.diaPhanFinalLayer,
                                       out_feature_class = fCDiaPhanFinalFeatureToLine,
                                       cluster_tolerance = "0 Meters")
        pass

    def SnapDuongDiaGioi(self, doiTuong):
        print "\tSnapDuongDiaGioi"
        self.duongDiaGioiFinalLayer = "DuongDiaGioiFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongDiaGioiFinal,
                                          out_layer = self.duongDiaGioiFinalLayer)
        sqlQuery = "doiTuong = " + doiTuong
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        self.diaPhanFinalLayer = "DiaPhanFinalLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.diaPhanFinalLayer,
                                          out_layer = self.diaPhanFinalLayer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.diaPhanFinalLayer,
                                                selection_type = "NEW_SELECTION",
                                                where_clause = sqlQuery)
        snapEnv = [self.diaPhanFinalLayer, "EDGE", "100 Meters"]
        with arcpy.da.SearchCursor(self.duongDiaGioiFinalLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = self.duongDiaGioiFinalLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = "OBJECTID = " + str(rowA[0]))
                arcpy.Snap_edit(self.duongDiaGioiFinalLayer, [snapEnv])
        pass

if __name__ == "__main__":
    
    duongBienGioiDiaGioi = DuongBienGioiDiaGioi()
    duongBienGioiDiaGioi.Execute()
