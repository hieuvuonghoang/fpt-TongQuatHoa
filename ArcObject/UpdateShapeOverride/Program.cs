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
                //    iRepresentation.Shape = iFeature.Shape;
                //    iRepresentation.UpdateFeature();
                //    iFeature.Store();
                //}
                //Console.WriteLine(iRepresentation.HasShapeOverride);
                IGeometry shapeCopy = iRepresentation.ShapeCopy;
                IPointCollection shapeCopyPointCollection = shapeCopy as IPointCollection;
                IPoint pointTemp = shapeCopyPointCollection.Point[0];
                //Console.WriteLine("X = {0}, Y = {1}", shapeCopyPointCollection.Point[0].X, shapeCopyPointCollection.Point[0].Y);
                pointTemp.X -= 1000;
                pointTemp.Y -= 1000;
                //Console.WriteLine("X = {0}, Y = {1}", pointTemp.X, pointTemp.Y);
                IPointCollection shape = iRepresentation.Shape as IPointCollection;
                shape.UpdatePoint(0, pointTemp);
                pointTemp = shapeCopyPointCollection.Point[1];
                pointTemp.X -= 1000;
                pointTemp.Y -= 1000;
                shape.UpdatePoint(1, pointTemp);
                iRepresentation.UpdateFeature();
                iFeature.Store();
                break;
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
            IQueryFilter iQueryFilter = new QueryFilter();
            iQueryFilter.WhereClause = whereClause;
            IFeatureCursor iFeatureCursor = featureClassNhaP.Search(iQueryFilter, true);
            IFeature iFeature = null;
            while ((iFeature = iFeatureCursor.NextFeature()) != null)
            {
                IPointCollection pointCollection = iFeature.Shape as IPointCollection;
                Console.Write("OID = {0}, PointCount = {1}; ", iFeature.OID, pointCollection.PointCount);
            }
        }
    }
}