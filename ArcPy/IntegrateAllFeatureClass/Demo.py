import os
import math
import arcpy

class Demo:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50_B\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50_B\\50K_Final.gdb"
        #arcpy.PolygonToLine_management(in_features, out_feature_class, neighbor_option)
        #arcpy.AddField_management(in_table, field_name, field_type)
        #arcpy.CalculateField_management(in_table, field, expression, expression_type)
        #arcpy.SelectLayerByAttribute_management(in_layer_or_view, selection_type, where_clause)
        #arcpy.FeatureToPolygon_management(in_features, out_feature_class)
        pass

    def Run(self):
        arcpy.env.overwriteOutput = True
        pathPhuBeMatLine = os.path.join(os.path.join(self.pathProcessGDB, "PhuBeMat"), "PhuBeMatLine")
        pathPhuBeMatIntersectDoanTimDuongBo = os.path.join(os.path.join(self.pathProcessGDB, "PhuBeMat"), "PhuBeMatLineIntersectDoanTimDuongBo")
        pathPhuBeMatIntersectDoanTimDuongBoClone = os.path.join(os.path.join(self.pathProcessGDB, "PhuBeMat"), "PhuBeMatLineIntersectDoanTimDuongBoClone")
        arcpy.CopyFeatures_management(in_features = pathPhuBeMatIntersectDoanTimDuongBo,
                                      out_feature_class = pathPhuBeMatIntersectDoanTimDuongBoClone)
        phuBeMatLineLayer = "phuBeMatLineLayer"
        phuBeMatIntersectDoanTimDuongBoCloneLayer = "phuBeMatIntersectDoanTimDuongBoCloneLayer"
        arcpy.MakeFeatureLayer_management(in_features = pathPhuBeMatLine,
                                          out_layer = phuBeMatLineLayer)
        arcpy.MakeFeatureLayer_management(in_features = pathPhuBeMatIntersectDoanTimDuongBoClone,
                                          out_layer = phuBeMatIntersectDoanTimDuongBoCloneLayer)
        with arcpy.da.SearchCursor(pathPhuBeMatIntersectDoanTimDuongBo, ["OID@"]) as cursorA:
            for rowA in cursorA:
                strQueryA = "OBJECTID = " + str(rowA[0])
                #print "# strQueryA: {}".format(strQueryA)
                outSelectA = arcpy.SelectLayerByAttribute_management(in_layer_or_view = phuBeMatIntersectDoanTimDuongBoCloneLayer,
                                                                     selection_type = "NEW_SELECTION",
                                                                     where_clause = strQueryA)
                #countOutSelectA = int(arcpy.GetCount_management(outSelectA).getOutput(0))
                #if countOutSelectA == 0:
                #    continue
                #print "   ## Count outSelectA: {}".format(str(countOutSelectA))
                with arcpy.da.SearchCursor(outSelectA, ["OID@", "LEFT_FID", "RIGHT_FID"]) as cursorB:
                    for rowB in cursorB:
                        strQueryB = "LEFT_FID = " + str(rowB[1]) + " AND " + "RIGHT_FID = " + str(rowB[2])
                        #print "      ### strQueryB: {}".format(strQueryB)
                outSelectB = arcpy.SelectLayerByAttribute_management(in_layer_or_view = phuBeMatLineLayer,
                                                                     selection_type = "NEW_SELECTION",
                                                                     where_clause = strQueryB)
                #countOutSelectB = int(arcpy.GetCount_management(outSelectB).getOutput(0))
                #if countOutSelectB == 0:
                #    continue
                #print "      ### Count outSelectB: {}".format(str(countOutSelectB))
                snapEnv = [outSelectB, "END", "0.5 Meters"]
                arcpy.Snap_edit(in_features = outSelectA,
                                snap_environment = [snapEnv])
                arcpy.AlignFeatures_edit(in_features = outSelectA,
                                         target_features = outSelectB,
                                         search_distance = "0.5 Meters",
                                         match_fields = [["LEFT_FID", "LEFT_FID"], ["RIGHT_FID", "RIGHT_FID"]])
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

if __name__ == "__main__":
    runTime = RunTime()
    demo = Demo()
    print "Running..."
    demo.Run()
    print "Success!!!"
    runTime.GetTotalRunTime()
    pass