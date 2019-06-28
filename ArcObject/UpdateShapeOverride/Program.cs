using ESRI.ArcGIS.esriSystem;
using System;
using System.Collections.Generic;
using System.Text;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geometry;

namespace UpdateShapeOverride
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new UpdateShapeOverride.LicenseInitializer();

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });
            //Console.WriteLine("pathGDB = \"{0}\", featureClassName = \"{1}\", representationName = \"{2}\", whereClause = \"{3}\"", args[0], args[1], args[2], args[3]);
            //Run(args[0], args[1], args[2], args[3]);
            Example(@"C:\Generalize_25_50\50K_Final.gdb", "DuongBoNuoc", "");
            Console.WriteLine("Success!!!");
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }

        private static void Run(string pathGDB, string featureClassName, string representationName, string whereClause)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathGDB, 0);
            IRepresentationWorkspaceExtension iRepresentationWorkspaceExtension = GetRepresentationFromFeatureClass(iWorkspace);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassNhaP = iFeatureWorkspace.OpenFeatureClass(featureClassName);
            IRepresentationClass iRepresentationClass = iRepresentationWorkspaceExtension.OpenRepresentationClass(representationName);
            IGeoDataset iGeoDataset = featureClassNhaP as IGeoDataset;
            IMapContext iMapContext = new MapContext();
            iMapContext.Init(iGeoDataset.SpatialReference, 50000, iGeoDataset.Extent);
            IQueryFilter iQueryFilter = new QueryFilter();
            iQueryFilter.WhereClause = whereClause;
            IFeatureCursor iFeatureCursor = featureClassNhaP.Search(iQueryFilter, true);
            IFeature iFeature = null;
            while ((iFeature = iFeatureCursor.NextFeature()) != null)
            {
                IRepresentation iRepresentation = iRepresentationClass.GetRepresentation(iFeature, iMapContext);
                //if (iRepresentation.HasShapeOverride == false)
                //{
                //    Console.WriteLine("False");
                //}
                //iRepresentation.Shape = iFeature.Shape;
                //iRepresentation.UpdateFeature();
                //iFeature.Store();
            }
        }

        private static IRepresentationWorkspaceExtension GetRepresentationFromFeatureClass(IWorkspace iWorkspace)
        {
            IWorkspaceExtensionManager iWorkspaceExtensionManager = (IWorkspaceExtensionManager)iWorkspace;
            UIDClass uIDClass = new UIDClass();
            uIDClass.Value = "{FD05270A-8E0B-4823-9DEE-F149347C32B6}";
            return (IRepresentationWorkspaceExtension)iWorkspaceExtensionManager.FindExtension(uIDClass);
        }

        private static void Example(string pathGDB, string featureClassName, string whereClause)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathGDB, 0);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassNhaP = iFeatureWorkspace.OpenFeatureClass(featureClassName);
            IFeatureClass featureClassPointRemove = GetFeatureClassPointRemove(@"C:\Generalize_25_50\50K_Process.gdb", "PointRemove");
            IQueryFilter iQueryFilter = new QueryFilter();
            iQueryFilter.WhereClause = whereClause;
            IFeatureCursor iFeatureCursor = featureClassNhaP.Search(iQueryFilter, true);
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

        private static IFeatureClass GetFeatureClassPointRemove(string pathGDB, string featureClassName)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathGDB, 0);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassPointRemove = iFeatureWorkspace.OpenFeatureClass(featureClassName);
            return featureClassPointRemove;
        }
    }
}
