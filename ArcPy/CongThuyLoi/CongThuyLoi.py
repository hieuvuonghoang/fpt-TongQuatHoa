import sys
import os
import arcpy

class CongThuyLoiP:

    def __init__(__self__, distance):
        __self__.distance = distance
        __self__.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        __self__.fcDataSetThuyHe = "ThuyHe"
        __self__.fcDataSetGiaoThong = "GiaoThong"
        __self__.fcCongThuyLoiP = "CongThuyLoiP"
        __self__.fcKenhMuongL = "KenhMuongL"
        __self__.fcKenhMuongA = "KenhMuongA"
        __self__.fcMatNuocTinh = "MatNuocTinh"
        __self__.fcSongSuoiL = "SongSuoiL"
        __self__.fcSongSuoiA = "SongSuoiA"
        __self__.fcDapL = "DapL"
        __self__.fcDapA = "DapA"
        __self__.fcDoanTimDuongBo = "DoanTimDuongBo"

        __self__.fcCongThuyLoiPInMemory = CopyFeatureClassToMemory(__self__.fcCongThuyLoiP, os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcCongThuyLoiP)))
        __self__.fcCongThuyLoiPInMemory.Excute()

    def Excute(__self__):
        __self__.fcCongThuyLoiPTempLayer = __self__.fcCongThuyLoiPInMemory.fcInMemory + "Layer"
        arcpy.MakeFeatureLayer_management(in_features = __self__.fcCongThuyLoiPInMemory.fcInMemory, out_layer = __self__.fcCongThuyLoiPTempLayer)
        __self__.fcCongThuyLoiPLayer = "in_memory\\" + __self__.fcCongThuyLoiP + "Layer"
        arcpy.MakeFeatureLayer_management(in_features = os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcCongThuyLoiP)), out_layer = __self__.fcCongThuyLoiPLayer)
        print "SongSuoiL, MatNuocTinh"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcSongSuoiL)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcMatNuocTinh)))
        print "KenhMuongL, MatNuocTinh"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcKenhMuongL)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcMatNuocTinh)))
        print "SongSuoiL, SongSuoiA"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcSongSuoiL)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcSongSuoiA)))
        print "KenhMuongL, SongSuoiA"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcKenhMuongL)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcSongSuoiA)))
        print "DoanTimDuongBo, KenhMuongL"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetGiaoThong, __self__.fcDoanTimDuongBo)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcKenhMuongL)))
        print "DoanTimDuongBo, SongSuoiL"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetGiaoThong, __self__.fcDoanTimDuongBo)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcSongSuoiL)))
        print "DapL, SongSuoiL"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcDapL)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcSongSuoiL)))
        print "DapL, KenhMuongL"
        __self__.IntersectPoint(os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcDapL)), os.path.join(__self__.pathProcessGDB, os.path.join(__self__.fcDataSetThuyHe, __self__.fcKenhMuongL)))

    def IntersectPoint(__self__, featureClassOne, featureClassTwo):
        fcIntersectTempP = "in_memory\\fcIntersectTempP"
        arcpy.Intersect_analysis (in_features = [featureClassOne, featureClassTwo],
                                  out_feature_class = fcIntersectTempP,
                                  join_attributes = "ONLY_FID",
                                  cluster_tolerance = "#",
                                  output_type = "POINT")
        #print arcpy.GetCount_management(fcIntersectTempP).getOutput(0)
        if int(arcpy.GetCount_management(fcIntersectTempP).getOutput(0)) == 0:
            return
        fcIntersectTempPLayer = fcIntersectTempP + "Layer"
        arcpy.MakeFeatureLayer_management(in_features = fcIntersectTempP, out_layer = fcIntersectTempPLayer)
        arcpy.SelectLayerByLocation_management(in_layer = __self__.fcCongThuyLoiPTempLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = fcIntersectTempPLayer,
                                               search_distance = __self__.distance,
                                               selection_type = "NEW_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        #print arcpy.GetCount_management(__self__.fcCongThuyLoiPTempLayer).getOutput(0)
        if int(arcpy.GetCount_management(__self__.fcCongThuyLoiPTempLayer).getOutput(0)) == 0:
            return
        arcpy.SelectLayerByLocation_management(in_layer = __self__.fcCongThuyLoiPTempLayer,
                                               overlap_type = "INTERSECT",
                                               select_features = fcIntersectTempPLayer,
                                               search_distance = "0 Meters",
                                               selection_type = "REMOVE_FROM_SELECTION",
                                               invert_spatial_relationship = "NOT_INVERT")
        #print arcpy.GetCount_management(__self__.fcCongThuyLoiPTempLayer).getOutput(0)
        if int(arcpy.GetCount_management(__self__.fcCongThuyLoiPTempLayer).getOutput(0)) == 0:
            return
        snapEnvOne = [fcIntersectTempPLayer, "END", __self__.distance]
        arcpy.Snap_edit(in_features = __self__.fcCongThuyLoiPTempLayer, snap_environment = [snapEnvOne])
        __self__.UpdateShapeForFinalGDB()

    def UpdateShapeForFinalGDB(__self__):
        print "UpdateShapeForFinalGDB"
        with arcpy.da.UpdateCursor(__self__.fcCongThuyLoiPTempLayer, ["SHAPE@", __self__.fcCongThuyLoiPInMemory.fieldName]) as cursor:
            for row in cursor:
                strQuery = "OBJECTID = " + str(row[1])
                arcpy.SelectLayerByAttribute_management(in_layer_or_view = __self__.fcCongThuyLoiPLayer,
                                                        selection_type = "NEW_SELECTION",
                                                        where_clause = strQuery)
                with arcpy.da.UpdateCursor(__self__.fcCongThuyLoiPLayer, ["SHAPE@"]) as cursorSub:
                    for rowSub in cursorSub:
                        rowSub[0] = row[0]
                        cursorSub.updateRow(rowSub)
                cursor.deleteRow()

class CopyFeatureClassToMemory:

    def __init__(__self__, featureClassName, pathFeatureClass):
        __self__.featureClassName = featureClassName
        __self__.pathFeatureClass = pathFeatureClass
        __self__.fcInMemory = "in_memory\\" + __self__.featureClassName + "Temp"
        __self__.fieldName = "OID_Clone"
        __self__.fieldType = "LONG"

    def Excute(__self__):
        __self__.AddFieldOIDClone()
        __self__.UpdateOIDClone()
        __self__.CopyFeatureToMemory()
        __self__.DeleteFieldOIDClone()

    def AddFieldOIDClone(__self__):
        arcpy.AddField_management(in_table = __self__.pathFeatureClass,
                                  field_name = __self__.fieldName,
                                  field_type = __self__.fieldType)

    def UpdateOIDClone(__self__):
        with arcpy.da.UpdateCursor(in_table = __self__.pathFeatureClass, field_names = ["OID@", __self__.fieldName]) as cursor:
            for row in cursor:
                row[1] = row[0]
                cursor.updateRow(row)

    def CopyFeatureToMemory(__self__):
        arcpy.CopyFeatures_management(in_features = __self__.pathFeatureClass, out_feature_class = __self__.fcInMemory)

    def DeleteFieldOIDClone(__self__):
        arcpy.DeleteField_management(__self__.pathFeatureClass, [__self__.fieldName])


if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    distance = "5 Meters"
    congThuyLoiP = CongThuyLoiP(distance)
    congThuyLoiP.Excute();

#- CongThuyLoiP:
#   + IntersectPoint:
#       ++ KenhMuongL vs MatNuocTinh (Line vs Polygon)
#       ++ KenhMuongL vs SongSuoiA (Line vs Polygon)
#       ++ SongSuoiL vs MatNuocTinh (Line vs Polygon)
#       ++ SongSuoiL vs SongSuoiA (Line vs Polygon)
#       ++ SongSuoiL vs KenhMuongL (Line vs Line)
#       ++ DoanTimDuongBo vs SongSuoiL (Line vs Line)
#       ++ DoanTimDuongBo vs KenhMuongL (Line vs Line)
#       ++ DapL vs KenhMuongL
#       ++ DapL vs SongSuoiL
#   + IntersectLine:
#       ++ DoanTimDuongBo vs SuongSuoiA (Line vs Polygon)
#       ++ DoanTimDuongBo vs KenhMuongA (Line vs Polygon)
#       ++ DoanTimDuongBo vs MatNuocTinh (Line vs Polygon)

#- CongThuyLoiL:
#   + IntersectLine:
#       ++ DoanTimDuongBo vs SongSuoiA
#       ++ DoanTimDuongBo vs KenhMuongA
#       ++ DoanTimDuongBo vs MatNuocTinh