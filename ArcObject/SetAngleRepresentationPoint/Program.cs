using ESRI.ArcGIS.esriSystem;
using System;
using System.Collections.Generic;
using System.Text;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Controls;

namespace SetAngleRepresentationPoint
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new SetAngleRepresentationPoint.LicenseInitializer();

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });
            Console.WriteLine("Check License OK!!!");
            //Console.ReadKey();
            Console.WriteLine("pathGDB = \"{0}\", featureClassName = \"{1}\", representationName = \"{2}\", whereClause = \"{3}\"", args[0], args[1], args[2], args[3]);
            //SetAngleRepresentationPoint(args[0], args[1], args[2], args[3]);
            SetEmptyShapeOverride(args[0], args[1], args[2], args[3]);
            //SetEmptyShapeOverride(@"C:\Generalize_25_50\50K_Final.gdb", "NhaP", "NhaP_Rep1", "");
            //SetAngleRepresentationPoint(@"C:\Generalize_25_50_B\50K_Final.gdb", "NhaP", "NhaP_Rep1", "");
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            //Console.ReadKey();
            m_AOLicenseInitializer.ShutdownApplication();
        }

        private static void SetAngleRepresentationPoint(string pathGDB, string featureClassName, string representationName, string whereClause)
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
                if (iRepresentation.HasShapeOverride)
                {
                    //IRepresentationRules iRepresentationRules = iRepresentationClass.RepresentationRules;
                    //IRepresentationRule iRepresentationRule = iRepresentationRules.Rule[iRepresentation.RuleID];
                    //IBasicMarkerSymbol iBasicMarkerSymbol = iRepresentationRule.Layer[0] as IBasicMarkerSymbol;
                    //IGraphicAttributes iGraphicAttributes = iBasicMarkerSymbol.MarkerPlacement as IGraphicAttributes;
                    ////Console.WriteLine("{0}", iGraphicAttributes.GraphicAttributeCount);
                    ////IGraphicAttributes iGraphicAttributes = iRepresentationRule.Layer[0] as IGraphicAttributes;
                    //for (int index = 0; index < iGraphicAttributes.GraphicAttributeCount; index++)
                    //{
                    //    Console.WriteLine("    ## {0}: {1}", iGraphicAttributes.ID[index], iGraphicAttributes.Name[iGraphicAttributes.ID[index]]);
                    //}
                    //Console.WriteLine("    ## XOffset: {0}, YOffset: {1}", iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["XOffset"]], iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["YOffset"]]);
                    //Console.WriteLine("Marker: {0}, Size: {1}, Angle: {2}, RotateClockwise: {3}", iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["Marker"]], iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["Size"]], iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["Angle"]], iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["RotateClockwise"]]);

                    //iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["XOffset"]] = iPoint.X + 25;
                    //iRepresentation.Value[iGraphicAttributes, iGraphicAttributes.IDByName["XOffset"]] = iPoint.X + 25;
                    //IPoint iPoint = iFeature.Shape as IPoint;
                    //iPoint.X += 25;
                    //iPoint.Y += 25;
                    iRepresentation.Shape = iFeature.Shape;
                    //Console.WriteLine(" # {0} : {1}", iFeature.OID, iRepresentation.HasShapeOverride);
                    //iRepresentation.Shape.SetEmpty();
                    iRepresentation.UpdateFeature();
                    iFeature.Store();
                }
            }
        }

        private static void SetEmptyShapeOverride(string pathGDB, string featureClassName, string representationName, string whereClause)
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
                if (iRepresentation.RuleID != 0)
                {
                    IPoint iPoint = iFeature.Shape as IPoint;
                    iRepresentation.Shape = (IGeometry)iPoint;
                    iRepresentation.UpdateFeature();
                    iFeature.Store();
                }
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
