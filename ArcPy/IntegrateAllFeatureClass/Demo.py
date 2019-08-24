import os
import math

class Demo:

    def __init__(self):
        pass

    def Execute(self):
        self.FeatureVerticesToPoint()
        pass

    def FeatureVerticesToPoint(self):
        # 292752.0038, 2341724.3137
        # 292784.2496, 2341727.6797
        # 292710.3079, 2341711.8303
        x, y = self.CreatePoint(292784.2496, 2341727.6797, 292710.3079, 2341711.8303, 292752.0038, 2341724.3137)
        print "{}, {}".format(str(x), str(y))
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
        #print "cA: {}".format(cA)
        #print "{}x + {}y + {} = 0".format(str(xN), str(yN), str(cA))
        # Duong thang di qua C(xC, yC) song song voi AB:
        ## PT duong thang di qua C(xC, yC) song song voi AB: xU(x - xC) + yU(y - yC) = 0 => cC = xU*(-xC) + yU*(-yC)
        cC = round((xU*(-xC) + yU*(-yC)), 10)
        #print "cC: {}".format(cC)
        #print "{}x + {}y + {} = 0".format(str(xU), str(yU), str(cC))
        # Tim D(xD, yD) la giao diem cua hai duong thang:
        ## x = (-cA - yN*y) / xN
        ## xU*((-cA - yN*y) / xN) + yU*y + cC = 0 => xU*(-cA - yN*y) + yU*xN*y + cC*xN = 0 => -xU*cA - xU*yN*y + yU*xN*y + cC*xN = 0 => y*(yU*xN - xU*yN) + xU*(-cA) + cC*xN = 0 => y = (xU*cA - cC*xN) / (yU*xN - xU*yN)
        yD = round((xU*cA - cC*xN) / (yU*xN - xU*yN), 10)
        xD = round((-cA - yN*yD) / xN, 10)
        # Tinh Vecto DA(xA - xD, yA - yD), DB(xB - xD, yB - yD)
        xDA = round(xA - xD, 10)
        yDA = round(yA - yD, 10)
        xDB = round(xB - xD, 10)
        yDB = round(yB - yD, 10)
        print "{}, {}".format(xD, yD)
        print "DA({}, {}), DB({}, {})".format(str(xDA), str(yDA), str(xDB), str(yDB))
        lengthDA = math.sqrt(math.pow(xDA, 2) + math.pow(yDA, 2))
        lengthDB = math.sqrt(math.pow(xDB, 2) + math.pow(yDB, 2))
        lengthAB = math.sqrt(math.pow(xU, 2) + math.pow(yU, 2))
        print "lengthDA: {}".format(lengthDA)
        print "lengthDB: {}".format(lengthDB)
        print "lengthAB: {}".format(lengthAB)
        if lengthDA + lengthDB == lengthAB:
            return xD, yD
        elif lengthDA < lengthDB:
            return xA, yA
        elif lengthDA > lengthDB:
            return xB, yB
        pass

if __name__ == "__main__":
    demo = Demo()
    demo.Execute()
    pass