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
            Execute(@"C:\Generalize_25_50\50K_Process.gdb", "DuongBoNuoc_PointRemove_Dissolve");
            //Run(@"C:\Generalize_25_50\50K_Final.gdb", "RanhGioiPhuBeMat", "", @"C:\Generalize_25_50\50K_Process.gdb", "RanhGioiPhuBeMatPointRemove");
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }
        private static void Execute(string pathGDB, string fCClassName)
        {
            //
            IFeatureClass featureClass = GetFeatureClass(pathGDB, fCClassName);
            IQueryFilter iQueryFilter = new QueryFilter();
            iQueryFilter.WhereClause = "";
            IFeatureCursor iFeatureCursor = featureClass.Search(iQueryFilter, true);
            int fIDField = iFeatureCursor.FindField("FID_DuongBoNuoc");
            IFeature iFeature = null;
            //
            IFeatureClass fCDuongBoNuoc = GetFeatureClass(pathGDB, "DuongBoNuoc");
            IFeatureCursor iFeatureCursorDBN = fCDuongBoNuoc.Search(iQueryFilter, true);
            IFeature iFeatureDBN = null;
            while ((iFeature = iFeatureCursor.NextFeature()) != null)
            {
                IPointCollection pointCollectionRemove = iFeature.Shape as IPointCollection;
                //Console.WriteLine("{0}", pointCollection.PointCount);
                while ((iFeatureDBN = iFeatureCursorDBN.NextFeature()) != null)
                {
                    int test = int.Parse(string.Format("{0}", iFeature.Value[fIDField]));
                    if (test == iFeatureDBN.OID)
                    {
                        IPointCollection pointCollection = iFeatureDBN.Shape as IPointCollection;

                        break;
                    }
                } 
                //Console.WriteLine("{0}", iFeature.Value[fIDField]);
                
            }
        }
        private static IFeatureClass GetFeatureClass(string pathGDB, string featureClassName)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathGDB, 0);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassPointRemove = iFeatureWorkspace.OpenFeatureClass(featureClassName);
            return featureClassPointRemove;
        }
    }
}
