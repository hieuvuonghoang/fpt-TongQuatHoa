import os
import math
import arcpy

class Demo:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDGiaoThong = "GiaoThong"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.pathDoanTimDuongBoProcess = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), self.fCDoanTimDuongBo)
        pass

    def Execute(self):
        self.FeatureVerticesToPoint()
        pass

    def FeatureVerticesToPoint(self):
        fCDoanTimDuongBoPoint = "DoanTimDuongBo_Point"
        outPut = os.path.join(os.path.join(self.pathProcessGDB, self.fDGiaoThong), fCDoanTimDuongBoPoint)
        arcpy.FeatureVerticesToPoints_management(in_features = self.pathDoanTimDuongBoProcess,
                                                 out_feature_class = outPut,
                                                 point_location = "BOTH_ENDS")
        pass

    def CreatePoint(self, xA, yA, xB, yB, xC, yC):
        # Duong thang di qua 2 diem A(xA, yA) va B(xB, yB)
        ## Vecto AB(xB - xA, yB- yA) => VTCP u(xU, yU)
        xU = round((xB - xA), 10)
        yU = round((yB - yA), 10)
        ## VTPT n = (-yU, xU)
        xN = -yU
        yN = xU
        ## PT duong thang di qua A nhan n lam VTPT la: xN(x - xA) + yN(y - yA) = 0 => cA = xN*-xA + yN*-yA
        cA = round((xN*(-xA) + yN*(-yA)), 10)
        #print "{}x + {}y + {} = 0".format(str(xN), str(yN), str(cA))
        # Duong thang di qua C(xC, yC) song song voi AB:
        ## PT duong thang di qua C(xC, yC) song song voi AB: xU(x - xC) + yU(y - yC) = 0 => cC = xU*(-xC) + yU*(-yC)
        cC = round((xU*(-xC) + yU*(-yC)), 10)
        #print "{}x + {}y + {} = 0".format(str(xU), str(yU), str(cC))
        # Tim D(xD, yD) la giao diem cua hai duong thang:
        ## x = (-cA - yN*y) / xN
        ## xU*((-cA - yN*y) / xN) + yU*y + cC = 0 => xU*(-cA - yN*y) + yU*xN*y + cC*xN = 0 => -xU*cA - xU*yN*y + yU*xN*y + cC*xN = 0 => y*(yU*xN - xU*yN) + xU*(-cA) + cC*xN = 0 => y = (xU*cA - cC*xN) / (yU*xN - xU*yN)
        yD = round((xU*cA - cC*xN) / (yU*xN - xU*yN), 10)
        xD = round((-cA - yN*yD) / xN, 10)
        # Tinh khoang cach:
        # D -> A, D -> B, A -> B
        dDA = round(math.sqrt(math.pow(xD - xA, 2) + math.pow(yD - yA, 2)), 10)
        dDB = round(math.sqrt(math.pow(xD - xB, 2) + math.pow(yD - yB, 2)), 10)
        dAB = round(math.sqrt(math.pow(xA - xB, 2) + math.pow(yA - yB, 2)), 10)
        #print "{}, {}, {}".format(dDA, dDB, dAB)
        if dDA + dDB == dAB:
            return xD, yD
        elif dDA < dDB:
            return xA, yA
        elif dDA > dDB:
            return xB, yB
        pass

if __name__ == "__main__":
    demo = Demo()
    demo.Execute()
    pass