import arcpy
import os

class TryDemo:
    
    def __init__(self):
        self.pathDefaultGDB = "C:\\Users\\vuong\\Documents\\ArcGIS\\Default.gdb"
        self.fCPointRandomInPolygon = "PointRandomInPolygon"

    def Excute(self):

        pass

if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    tryDemo = TryDemo()
    tryDemo.Excute()
