using ESRI.ArcGIS.esriSystem;
using System;
using System.Collections.Generic;
using System.Text;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geometry;

namespace RemovePointOnLine
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new RemovePointOnLine.LicenseInitializer();

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });
            Execute();
            //Run(@"C:\Generalize_25_50\50K_Final.gdb", "RanhGioiPhuBeMat", "", @"C:\Generalize_25_50\50K_Process.gdb", "RanhGioiPhuBeMatPointRemove");
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }
        private static void Execute()
        {
            string pathGDB = @"C:\Generalize_25_50\50K_Process.gdb";
            IFeatureClass fCPointRemove = GetFeatureClass(pathGDB, "DuongBoNuoc_PointRemove_Dissolve");
            IFeatureClass fCPolyline = GetFeatureClass(pathGDB, "DuongBoNuoc");
            RemovePointOnLine(fCPointRemove, fCPolyline);
        }
        private static void RemovePointOnLine(IFeatureClass fCPointRemove, IFeatureClass fCPolyline)
        {
            IFeatureCursor iFeatureCursorPointRemove = fCPointRemove.Search(new QueryFilter() { WhereClause = "" }, true);
            IFeature iFeaturePointRemove = null;
            IFeatureCursor iFeatureCursorPolyline = fCPolyline.Search(new QueryFilter() { WhereClause = "" }, true);
            IFeature iFeaturePolyline = null;
            string strFID = "FID_DuongBoNuoc";
            int indexFID = iFeatureCursorPointRemove.FindField(strFID);
            while (((iFeaturePointRemove = iFeatureCursorPointRemove.NextFeature()) != null))
            {
                IPointCollection iPointCollPointRemove = iFeaturePointRemove.Shape as IPointCollection;
                int fID = (int)iFeaturePointRemove.Value[indexFID];
                while (((iFeaturePolyline = iFeatureCursorPolyline.NextFeature()) != null))
                {
                    if (fID == iFeaturePolyline.OID)
                    {
                        IPointCollection iPointCollPolyline = iFeaturePolyline.Shape as IPointCollection;
                        List<int> indexRemove = new List<int>();
                        int iPointCollPolylineCount = iPointCollPolyline.PointCount;
                        for (int indexPolyline = 0; indexPolyline < iPointCollPolylineCount; indexPolyline++)
                        {
                            if (iPointCollPointRemove.PointCount == 0)
                            {
                                break;
                            }
                            IPoint iPointPolyline = iPointCollPolyline.Point[indexPolyline];
                            for (int indexPointRemove = 0; indexPointRemove < iPointCollPointRemove.PointCount; indexPointRemove++)
                            {
                                IPoint iPointPointRemove = iPointCollPointRemove.Point[indexPointRemove];
                                if ((iPointPolyline.X == iPointPointRemove.X) && (iPointPolyline.Y == iPointPointRemove.Y))
                                {
                                    if ((indexPolyline != 0) || (indexPolyline != iPointCollPolylineCount))
                                    {
                                        iPointCollPointRemove.RemovePoints(indexPointRemove, 1);
                                    }
                                    indexRemove.Add(indexPolyline);
                                    break;
                                }
                            }
                        }
                        int countRemove = 0;
                        foreach (int index in indexRemove)
                        {
                            iPointCollPolyline.RemovePoints(index - countRemove, 1);
                            countRemove++;
                        }
                        if (countRemove > 0)
                        {
                            iFeaturePolyline.Store();
                        }
                        break;
                    }
                }
                iFeaturePointRemove.Store();
            }

            //IFeatureCursor iFeatureCursorPointRemove = fCPointRemove.Search(new QueryFilter() { WhereClause = "" }, true);
            //IFeatureCursor iFeatureCursorPolyline = fCPolyline.Search(new QueryFilter() { WhereClause = "" }, true);
            //IFeature iFeaturePolyline = null;
            //while (((iFeaturePolyline = iFeatureCursorPolyline.NextFeature()) != null))
            //{
            //    IPointCollection iPointCollPolyline = iFeaturePolyline.Shape as IPointCollection;
            //    List<int> indexRemove = new List<int>();
            //    string strFID = "FID_DuongBoNuoc";
            //    IFeatureCursor iFeatureCursorPointRemove = fCPointRemove.Search(new QueryFilter() { WhereClause = strFID + " = " + iFeaturePolyline.OID.ToString() }, true);
            //    IFeature iFeaturePointRemove = null;
            //    while (((iFeaturePointRemove = iFeatureCursorPointRemove.NextFeature()) != null))
            //    {
            //        IPointCollection iPointCollPointRemove = iFeaturePointRemove.Shape as IPointCollection;
            //        for (int indexPolyline = 0; indexPolyline < iPointCollPolyline.PointCount; indexPolyline++)
            //        {
            //            if (iPointCollPointRemove.PointCount == 0)
            //            {
            //                break;
            //            }
            //            bool foundPoint = false;
            //            IPoint iPointPolyline = iPointCollPolyline.Point[indexPolyline];
            //            for (int indexPointRemove = 0; indexPointRemove < iPointCollPointRemove.PointCount; indexPointRemove++)
            //            {
            //                IPoint iPointPointRemove = iPointCollPointRemove.Point[indexPointRemove];
            //                if ((iPointPolyline.X == iPointPointRemove.X) && (iPointPolyline.Y == iPointPointRemove.Y))
            //                {
            //                    foundPoint = true;
            //                    iPointCollPointRemove.RemovePoints(indexPointRemove, 1);
            //                    break;
            //                }
            //            }
            //            if (foundPoint)
            //            {
            //                indexRemove.Add(indexPolyline);
            //            }
            //        }
            //    }
            //    int countRemove = 0;
            //    foreach (int index in indexRemove)
            //    {
            //        iPointCollPolyline.RemovePoints(index - countRemove, 1);
            //        countRemove++;
            //    }
            //    if (countRemove > 0)
            //    {
            //        iFeaturePolyline.Store();
            //    }
            //}
        }
        private static IFeatureClass GetFeatureClass(string pathGDB, string featureClassName)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathGDB, 0);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass iFeatureClass = iFeatureWorkspace.OpenFeatureClass(featureClassName);
            return iFeatureClass;
        }
    }
}
