import os
import math
#import arcpy

class Demo:

    def __init__(self):
        self.pathProcessGDB = "C:\\Generalize_25_50\\50K_Process.gdb"
        self.pathFinalGDB = "C:\\Generalize_25_50\\50K_Final.gdb"
        self.fDThuyHe = "ThuyHe"
        self.fCMatNuocTinh = "MatNuocTinh"
        self.fCDuongBoNuoc = "DuongBoNuoc"
        self.fDQuanSuA = "QuanSu"
        self.fCQuanSuA = "QuanSuA"
        self.fDGiaoThong = "GiaoThong"
        self.fCDoanTimDuongBo = "DoanTimDuongBo"
        self.fDBienGioiDiaGioi = "BienGioiDiaGioi"
        self.fCDuongDiaGioi = "DuongDiaGioi"
        self.fCDiaPhan = "DiaPhan"
        pass

    def Execute(self):
        self.FeatureVerticesToPoint()
        #################### DiaPhan ########################
        #294100.6522, 2367846.945
        #294109.9946, 2367870.8198
        #pntUpdate = arcpy.Point(294109.9946, 2367870.8198)
        #diaPhan = FeatureClass(self.fCDiaPhan)
        #duongDiaGioi = FeatureClass(self.fCDuongDiaGioi)
        #diaPhan.SetFeatureClassPointRemove()
        #pathDiaPhanPointRemove = os.path.join(os.path.join(self.pathProcessGDB, self.fDBienGioiDiaGioi), diaPhan.featureClassPointRemove)
        #diaPhanPointRemoveLayer = "diaPhanPointRemoveLayer"
        #arcpy.MakeFeatureLayer_management(pathDiaPhanPointRemove, diaPhanPointRemoveLayer)
        #arcpy.SelectLayerByAttribute_management(diaPhanPointRemoveLayer, "NEW_SELECTION", "FID_DiaPhan = 1")
        #arrPointRemove = arcpy.Array()
        #with arcpy.da.SearchCursor(diaPhanPointRemoveLayer, ["OID@", "Shape@XY"]) as cursor:
        #    for row in cursor:
        #        x, y = row[1]
        #        arrPointRemove.add(arcpy.Point(x, y))
        #        #x, y = row[1]
        #        print "{}, {}".format(str(round(x, 10)), str(round(y, 10)))
        #print "arrAllPoint Count: {}".format(str(arrPointRemove.count))

        ##
        #pathQuanSuA = os.path.join(os.path.join(self.pathProcessGDB, self.fDQuanSuA), quanSuA.featureClass)
        #quanSuALayer = "quanSuALayer"
        #arcpy.MakeFeatureLayer_management(pathQuanSuA, quanSuALayer)
        #arcpy.SelectLayerByAttribute_management(quanSuALayer, "NEW_SELECTION", "OBJECTID = 23")
        #arrPolygon = arcpy.Array()
        #with arcpy.da.SearchCursor(quanSuALayer, ["OID@", "Shape@"]) as cursor:
        #    for row in cursor:
        #        arrPart = arcpy.Array()
        #        for part in row[1]:
        #            for pnt in part:
        #                arrPart.add(pnt)
        #        arrPolygon.add(arrPart)
        #print "arrPolygon Count: {}".format(str(arrPolygon.count))
        #print "arrPolygon[0] Count: {}".format(str(arrPolygon[0].count))



        #matNuocTinh = FeatureClass(self.fCMatNuocTinh)
        #duongBoNuoc = FeatureClass(self.fCDuongBoNuoc)
        #matNuocTinh.SetFeatureClassPointRemove()
        #pathMatNuocTinhPointRemove = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), matNuocTinh.featureClassPointRemove)
        #matNuocTinhPointRemoveLayer = "matNuocTinhPointRemoveLayer"
        #arcpy.MakeFeatureLayer_management(pathMatNuocTinhPointRemove, matNuocTinhPointRemoveLayer)
        #arcpy.SelectLayerByAttribute_management(matNuocTinhPointRemoveLayer, "NEW_SELECTION", "FID_MatNuocTinh = 1037")
        #arrPointRemove = arcpy.Array()
        #with arcpy.da.SearchCursor(matNuocTinhPointRemoveLayer, ["OID@", "Shape@XY"]) as cursor:
        #    for row in cursor:
        #        x, y = row[1]
        #        arrPointRemove.add(arcpy.Point(x, y))
        #        #x, y = row[1]
        #        #print "{}, {}".format(str(round(x, 10)), str(round(y, 10)))
        #print "arrAllPoint Count: {}".format(str(arrPointRemove.count))

        ##
        #pathMatNuocTinh = os.path.join(os.path.join(self.pathProcessGDB, self.fDThuyHe), matNuocTinh.featureClass)
        #matNuocTinhLayer = "matNuocTinhLayer"
        #arcpy.MakeFeatureLayer_management(pathMatNuocTinh, matNuocTinhLayer)
        #arcpy.SelectLayerByAttribute_management(matNuocTinhLayer, "NEW_SELECTION", "OBJECTID = 1037")
        #arrPolygon = arcpy.Array()
        #with arcpy.da.SearchCursor(matNuocTinhLayer, ["OID@", "Shape@"]) as cursor:
        #    for row in cursor:
        #        arrPart = arcpy.Array()
        #        for part in row[1]:
        #            for pnt in part:
        #                arrPart.add(pnt)
        #        arrPolygon.add(arrPart)
        #print "arrPolygon Count: {}".format(str(arrPolygon.count))
        #print "arrPolygon[0] Count: {}".format(str(arrPolygon[0].count))


        #################### Quan Su A ########################
        ##294100.6522, 2367846.945
        ##294109.9946, 2367870.8198
        #pntUpdate = arcpy.Point(294109.9946, 2367870.8198)
        #quanSuA = FeatureClass(self.fCQuanSuA)
        #doanTimDuongBo = FeatureClass(self.fCDoanTimDuongBo)
        #quanSuA.SetFeatureClassPointRemove()
        #pathQuanSuAPointRemove = os.path.join(os.path.join(self.pathProcessGDB, self.fDQuanSuA), quanSuA.featureClassPointRemove)
        #quanSuAPointRemoveLayer = "quanSuAPointRemoveLayer"
        #arcpy.MakeFeatureLayer_management(pathQuanSuAPointRemove, quanSuAPointRemoveLayer)
        #arcpy.SelectLayerByAttribute_management(quanSuAPointRemoveLayer, "NEW_SELECTION", "FID_QuanSuA = 23")
        #arrPointRemove = arcpy.Array()
        #with arcpy.da.SearchCursor(quanSuAPointRemoveLayer, ["OID@", "Shape@XY"]) as cursor:
        #    for row in cursor:
        #        x, y = row[1]
        #        arrPointRemove.add(arcpy.Point(x, y))
        #        #x, y = row[1]
        #        print "{}, {}".format(str(round(x, 10)), str(round(y, 10)))
        #print "arrAllPoint Count: {}".format(str(arrPointRemove.count))

        ##
        #pathQuanSuA = os.path.join(os.path.join(self.pathProcessGDB, self.fDQuanSuA), quanSuA.featureClass)
        #quanSuALayer = "quanSuALayer"
        #arcpy.MakeFeatureLayer_management(pathQuanSuA, quanSuALayer)
        #arcpy.SelectLayerByAttribute_management(quanSuALayer, "NEW_SELECTION", "OBJECTID = 23")
        #arrPolygon = arcpy.Array()
        #with arcpy.da.SearchCursor(quanSuALayer, ["OID@", "Shape@"]) as cursor:
        #    for row in cursor:
        #        arrPart = arcpy.Array()
        #        for part in row[1]:
        #            for pnt in part:
        #                arrPart.add(pnt)
        #        arrPolygon.add(arrPart)
        #print "arrPolygon Count: {}".format(str(arrPolygon.count))
        #print "arrPolygon[0] Count: {}".format(str(arrPolygon[0].count))

        #x, y = self.ReturnPointUpdate(pntUpdate, arrPointRemove, arrPolygon)
        #print "{}, {}".format(str(x), str(y))

        #
        #293891.261, 2368153.675
        #294100.6522, 2367846.945
        #pntUpdate = arcpy.Point(293891.261, 2368153.675)
        #x, y = self.ReturnPointUpdate(pntUpdate, arrPointRemove, arrPolygon)
        #print "{}, {}".format(str(x), str(y))
        pass

    def ReturnPointUpdate(self, pntUpdate, arrPointRemove, arrPolygon):
        # Remove pntUpdate in arrPointRemove
        arrIndexPointRemove = []
        indexPointRemove = 0
        for pntRemove in arrPointRemove:
            if round(pntRemove.X, 5) == round(pntUpdate.X, 5) and round(pntRemove.Y, 5) == round(pntUpdate.Y, 5):
                arrIndexPointRemove.append(indexPointRemove)
            indexPointRemove += 1
        indexLoop = 0
        for indexPointRemvoe in arrIndexPointRemove:
            arrPointRemove.remove(indexPointRemvoe - indexLoop)
            indexLoop += 1
        # Mark Index Remove Point in arrPolygon
        arrIndexPart = []
        for part in arrPolygon:
            arrIndexPointOfPart = []
            indexPointOfPart = 0
            for pnt in part:
                if pnt:
                    if arrPointRemove.count == 0:
                        continue
                    foundPoint = False
                    indexPointRemove = 0
                    for pntRemove in arrPointRemove:
                        if round(pntRemove.X, 5) == round(pnt.X, 5) and round(pntRemove.Y, 5) == round(pnt.Y, 5):
                            foundPoint = True
                            break
                        indexPointRemove += 1
                    if foundPoint:
                        arrPointRemove.remove(indexPointRemove)
                        arrIndexPointOfPart.append(indexPointOfPart)
                indexPointOfPart += 1
            arrIndexPart.append(arrIndexPointOfPart)
        #print arrIndexPart
        #print "arrIndexPart[0] count: {}".format(len(arrIndexPart[0]))
        # Remove Point in arrPolygon
        indexPartNum = 0
        for indexPart in arrIndexPart:
            indexPointInPartNum = 0
            for indexPointInPart in indexPart:
                arrPolygon[indexPartNum].remove(indexPointInPart - indexPointInPartNum)
                indexPointInPartNum += 1
            indexPartNum += 1
        #print "arrPolygon[0] Count: {}".format(str(arrPolygon[0].count))
        # Find Point
        indexPartNum = 0
        indexPointInPartNum = 0
        for part in arrPolygon:
            indexPointInPartNum = 0
            found = False
            for pnt in part:
                if pnt:
                    if round(pnt.X, 5) == round(pntUpdate.X, 5) and round(pnt.Y, 5) == round(pntUpdate.Y, 5):
                        found = True
                        break
                indexPointInPartNum += 1
            if found:
                break
            indexPartNum += 1
        # Print
        #for part in arrPolygon:
        #    for pnt in part:
        #        if pnt:
        #            print "{}, {}".format(pnt.X, pnt.Y)
        # Process IndexPoint
        arrPolygonCount = arrPolygon[indexPartNum].count
        if indexPointInPartNum == 0:
            pntBefore = arrPolygon[indexPartNum].getObject(indexPointInPartNum + 1)
            pntAfter = arrPolygon[indexPartNum].getObject(arrPolygonCount - 2)
        elif indexPointInPartNum == arrPolygonCount - 1:
            pntBefore = arrPolygon[indexPartNum].getObject(0)
            pntAfter = arrPolygon[indexPartNum].getObject(arrPolygonCount - 2)
        else:
            pntBefore = arrPolygon[indexPartNum].getObject(indexPointInPartNum + 1)
            pntAfter = arrPolygon[indexPartNum].getObject(indexPointInPartNum - 1)
        x, y = self.CreatePoint(pntBefore.X, pntBefore.Y, pntAfter.X, pntAfter.Y, pntUpdate.X, pntUpdate.Y)
        return x, y
        pass

    def FeatureVerticesToPoint(self):
        # 292752.0038, 2341724.3137
        # 292784.2496, 2341727.6797
        # 292710.3079, 2341711.8303
        #x, y = self.CreatePoint(293881.019, 2368152.378, 293906.508, 2368134.78, 293891.261, 2368153.675)
        x, y = self.CreatePoint(292784.2496, 2341727.6797, 292710.3079, 2341711.8303, 292752.0038, 2341724.3137)
        print "{}, {}".format(str(x), str(y))
        pass

    def CreatePoint(self, xA, yA, xB, yB, xC, yC):
        try:
            # Duong thang di qua 2 diem A(xA, yA) va B(xB, yB)
            ## Vecto AB(xB - xA, yB- yA) => VTCP u(xU, yU)
            xU = round((xB - xA), 4)
            yU = round((yB - yA), 4)
            ## VTPT n = (-yU, xU)
            xN = -yU
            yN = xU
            ## PT duong thang di qua A nhan n lam VTPT la: xN(x - xA) + yN(y - yA) = 0 => cA = xN*-xA + yN*-yA
            cA = round((xN*(-xA) + yN*(-yA)), 4)
            #print "cA: {}".format(cA)
            #print "{}x + {}y + {} = 0".format(str(xN), str(yN), str(cA))
            # Duong thang di qua C(xC, yC) song song voi AB:
            ## PT duong thang di qua C(xC, yC) song song voi AB: xU(x - xC) + yU(y - yC) = 0 => cC = xU*(-xC) + yU*(-yC)
            cC = round((xU*(-xC) + yU*(-yC)), 4)
            #print "cC: {}".format(cC)
            #print "{}x + {}y + {} = 0".format(str(xU), str(yU), str(cC))
            # Tim D(xD, yD) la giao diem cua hai duong thang:
            ## x = (-cA - yN*y) / xN
            ## xU*((-cA - yN*y) / xN) + yU*y + cC = 0 => xU*(-cA - yN*y) + yU*xN*y + cC*xN = 0 => -xU*cA - xU*yN*y + yU*xN*y + cC*xN = 0 => y*(yU*xN - xU*yN) + xU*(-cA) + cC*xN = 0 => y = (xU*cA - cC*xN) / (yU*xN - xU*yN)
            yD = round((xU*cA - cC*xN) / (yU*xN - xU*yN), 4)
            xD = round((-cA - yN*yD) / xN, 4)
            # Tinh Vecto DA(xA - xD, yA - yD), DB(xB - xD, yB - yD)
            xDA = round(xA - xD, 4)
            yDA = round(yA - yD, 4)
            xDB = round(xB - xD, 4)
            yDB = round(yB - yD, 4)
            #print "{}, {}".format(xD, yD)
            #print "DA({}, {}), DB({}, {})".format(str(xDA), str(yDA), str(xDB), str(yDB))
            lengthDA = round((math.sqrt(math.pow(xDA, 2) + math.pow(yDA, 2))), 4)
            lengthDB = round((math.sqrt(math.pow(xDB, 2) + math.pow(yDB, 2))), 4)
            lengthAB = round((math.sqrt(math.pow(xU, 2) + math.pow(yU, 2))), 4)
            #print "lengthDA: {}".format(lengthDA)
            #print "lengthDB: {}".format(lengthDB)
            #print "lengthAB: {}".format(lengthAB)
            if round(lengthDA + lengthDB, 4) == round(lengthAB, 4):
                return xD, yD
            elif round(lengthDA, 4) < round(lengthDB, 4):
                return xA, yA
            elif round(lengthDA, 4) > round(lengthDB, 4):
                return xB, yB
        except:
            return None, None
        pass

class FeatureClass:

    def __init__(self, featureClass):
        self.featureClass = featureClass
        pass
    
    def SetFeatureClassInMemory(self):
        self.featureClassInMemory = "in_memory\\" + self.featureClass
        pass

    def SetFeatureLayer(self):
        self.featureLayer = self.featureClass + "Layer"
        pass

    def SetFeatureClassAllPoint(self):
        self.featureClassAllPoint = self.featureClass + "_AllPoint"
        pass

    def SetFeatureClassSimplify(self):
        self.featureClassSimplify = self.featureClass + "_Simplify"
        pass

    def SetFeatureClassSimplifyAllPoint(self):
        self.featureClassSimplifyAllPoint = self.featureClass + "_Simplify_AllPoint"
        pass

    def SetFeatureClassPointRemove(self):
        self.featureClassPointRemove = self.featureClass + "_PointRemove"
        pass

    def SetFeatureClassPointRemoveDissolve(self):
        self.featureClassPointRemoveDissolve = self.featureClass + "_PointRemove_Dissolve"
        pass

if __name__ == "__main__":
    demo = Demo()
    demo.Execute()
    pass