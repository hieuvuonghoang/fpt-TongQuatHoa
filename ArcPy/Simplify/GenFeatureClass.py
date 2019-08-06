# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import arcpy
import datetime

if __name__ == '__main__':
    pathProcessGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
    str = ""
    for fcDataSetTemp in arcpy.Describe(pathProcessGDB).children:
        for fcTemp in arcpy.Describe(fcDataSetTemp.catalogPath).children:
            if fcTemp.featureType == "Simple" and fcTemp.shapeType == "Polyline":
                print fcTemp.baseName
    #textConfig = json.dumps(obj = self.configTools.GetDict(), indent = 1, sort_keys = True)
    #file = open(pathFile, "w")
    #file.write(textConfig)
    #file.close()
    #pass
    pass