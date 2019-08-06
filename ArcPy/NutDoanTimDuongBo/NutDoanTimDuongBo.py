import os
import arcpy
import ArcHydroTools

class NutDoanTimDuongBo:

   def __init__(self):
       self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
       self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
       self.fDGiaoThong = "GiaoThong"
       self.fCDoanTimDuongBo = "DoanTimDuongBo"
       self.pathDoanTimDuongBoFinal = os.path.join(os.path.join(self.pathFinalGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
       pass

   def Execute(self):
       arcpy.env.overwriteOutput = True
       ArcHydroTools.GenerateFNodeTNode(self.pathDoanTimDuongBoFinal)
       pass

if __name__ == "__main__":
    nutDoanTimDuongBo = NutDoanTimDuongBo()
    nutDoanTimDuongBo.Execute()
    pass