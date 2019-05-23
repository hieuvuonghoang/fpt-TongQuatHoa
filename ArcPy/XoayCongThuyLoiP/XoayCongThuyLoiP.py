# Xoay Representation CongThuyLoiP theo DoanTimDuongBo

import arcpy

if __name__ == '__main__':
    arcpy.env.workspace = "C:\\Generalize_25_50\\50K_Process.gdb"
    arcpy.env.overwriteOutput = True
    arcpy.env.referenceScale = "50000"
    fcCongThuyLoiP = "CongThuyLoiP"
    fcDoanTimDuongBo = "DoanTimDuongBo"
    congThuyLoiPLayer = "CongThuyLoiPLayer"
    doanTimDuongBoLayer = "DoanTimDuongBoLayer"
    arcpy.MakeFeatureLayer_management(in_features = fcCongThuyLoiP,
                                        out_layer = congThuyLoiPLayer)
    arcpy.MakeFeatureLayer_management(in_features = fcDoanTimDuongBo,
                                        out_layer = doanTimDuongBoLayer)
    arcpy.SetLayerRepresentation_cartography(in_layer = congThuyLoiPLayer,
                                             representation = "CongThuyLoiP_Rep")
    arcpy.SetLayerRepresentation_cartography(in_layer = doanTimDuongBoLayer,
                                             representation = "DoanTimDuongBo_Rep")
    #PERPENDICULAR: aligns representation markers perpendicularly to the stroke or fill edge. This is the default.
    #PARALLEL: aligns representation markers parallel to the stroke or fill edge.
    arcpy.AlignMarkerToStrokeOrFill_cartography(in_point_features = congThuyLoiPLayer,
                                                in_line_or_polygon_features = doanTimDuongBoLayer,
                                                search_distance = "0 Meters",
                                                marker_orientation = "PERPENDICULAR")
