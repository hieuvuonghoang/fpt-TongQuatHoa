import arcpy
import os
import sys

class DuongBoNuoc:
    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        self.fCDuongBoNuocPointRemove = "DuongBoNuocPointRemove"
        self.pathDuongBoNuoc = os.path.join(os.path.join(self.pathFinalGDB, self.fDThuyHe), self.fCDuongBoNuoc)
        self.pathDuongBoNuocPointRemove = os.path.join(self.pathDefaultGDB, self.fCDuongBoNuocPointRemove)
    def Excute(self):
        self.pathDuongBoNuocPointRemoveInMemory = "in_memory\\PathDuongBoNuocPointRemoveInMemory"
        arcpy.CopyFeatures_management(in_features = self.pathDuongBoNuocPointRemove,
                                      out_feature_class = self.pathDuongBoNuocPointRemoveInMemory)
        self.duongBoNuocPointRemoveInMemoryLayer = "DuongBoNuocPointRemoveInMemoryLayer"
        self.duongBoNuocLayer = "DuongBoNuocLayer"
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongBoNuoc,
                                          out_layer = self.duongBoNuocLayer)
        arcpy.MakeFeatureLayer_management(in_features = self.pathDuongBoNuocPointRemoveInMemory,
                                          out_layer = self.duongBoNuocPointRemoveInMemoryLayer)
        with arcpy.da.UpdateCursor(self.duongBoNuocLayer, ["OID@", "SHAPE@"]) as cursorA:
            for rowA in cursorA:
                print rowA[0]
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
                listPoint = []
                for rowASub in rowA[1]:
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
                rowA[1] = arcpy.Polyline(arcpy.Array(listPoint))
                cursorA.updateRow(rowA)

if __name__ == '__main__':
    print "DuongBoNuoc Tools"
    arcpy.env.overwriteOutput = True
    duongBoNuoc = DuongBoNuoc()
    duongBoNuoc.Excute()
    print "Success!!!"