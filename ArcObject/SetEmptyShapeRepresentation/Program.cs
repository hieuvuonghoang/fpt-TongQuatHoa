using ESRI.ArcGIS.esriSystem;
using System;
using System.Collections.Generic;
using System.Text;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Controls;

namespace SetEmptyShapeRepresentation
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new SetEmptyShapeRepresentation.LicenseInitializer();

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });
            //Console.WriteLine("pathGDB = \"{0}\", featureClassName = \"{1}\", representationName = \"{2}\", whereClause = \"{3}\"", args[0], args[1], args[2], args[3]);
            //SetEmptyShapeRepresentation(args[0], args[1], args[2], args[3]);
            SetEmptyShapeRepresentation(@"C:\Generalize_25_50\50K_Final.gdb", "NhaP", "NhaP_Rep1", "OBJECTID = 3202");
            Console.ReadKey();
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }

        private static void SetEmptyShapeRepresentation(string pathGDB, string featureClassName, string representationName, string whereClause)
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
                IRepresentationRules iRepresentationRules = iRepresentationClass.RepresentationRules;
                IRepresentationRule iRepresentationRule = iRepresentationRules.Rule[iRepresentation.RuleID];
                IGraphicAttributes iGraphicAttributes = iRepresentationRule.Layer[0] as IGraphicAttributes;
                //var angle = iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["Angle"]];
                iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["Angle"]] = 45.0d;
                iRepresentation.UpdateFeature();
                iFeature.Store();
            }
        }

        private static IRepresentationWorkspaceExtension GetRepresentationFromFeatureClass(IWorkspace iWorkspace)
        {
            IWorkspaceExtensionManager iWorkspaceExtensionManager = (IWorkspaceExtensionManager)iWorkspace;
            UIDClass uIDClass = new UIDClass();
            uIDClass.Value = "{FD05270A-8E0B-4823-9DEE-F149347C32B6}";
            return (IRepresentationWorkspaceExtension)iWorkspaceExtensionManager.FindExtension(uIDClass);
        }
    }
}
