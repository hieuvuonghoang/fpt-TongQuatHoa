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
            Console.WriteLine("{0}, {1}, {2}, {3}, {4}", args[0], args[1], args[2], args[3], args[4]);
            Run(args[0], args[1], args[2], args[3], args[4]);
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }
        private static void Run(string pathFinalGDB, string fCLineName, string whereClause, string pathProcessGDB, string fCPointRemoveName)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathFinalGDB, 0);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassLine = iFeatureWorkspace.OpenFeatureClass(fCLineName);
            IFeatureClass featureClassPointRemove = GetFeatureClassPointRemove(pathProcessGDB, fCPointRemoveName);
            IQueryFilter iQueryFilter = new QueryFilter();
            iQueryFilter.WhereClause = whereClause;
            IFeatureCursor iFeatureCursor = featureClassLine.Search(iQueryFilter, true);
            IFeature iFeature = null;
            while ((iFeature = iFeatureCursor.NextFeature()) != null)
            {
                IPointCollection pointCollection = iFeature.Shape as IPointCollection;
                string querySQL = "ORIG_FID = " + iFeature.OID.ToString();
                iQueryFilter.WhereClause = querySQL;
                IFeatureCursor iFeatureCursorPointRemove = featureClassPointRemove.Search(iQueryFilter, true);
                IFeature iFeaturePointRemve = null;
                while ((iFeaturePointRemve = iFeatureCursorPointRemove.NextFeature()) != null)
                {
                    IPoint pointTemp = iFeaturePointRemve.Shape as IPoint;
                    for (int index = 0; index < pointCollection.PointCount; index++)
                    {
                        if (pointCollection.Point[index].X == pointTemp.X && pointCollection.Point[index].Y == pointTemp.Y)
                        {
                            pointCollection.RemovePoints(index, 1);
                            break;
                        }
                    }
                }
                iFeature.Store();
            }
        }
        private static IFeatureClass GetFeatureClassPointRemove(string pathProcessGDB, string featureClassName)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathProcessGDB, 0);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassPointRemove = iFeatureWorkspace.OpenFeatureClass(featureClassName);
            return featureClassPointRemove;
        }
    }
}
