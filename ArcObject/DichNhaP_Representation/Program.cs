using ESRI.ArcGIS.esriSystem;
using System;
using System.IO;

using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geoprocessor;
using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.AnalysisTools;
using ESRI.ArcGIS.CartographyTools;
using ESRI.ArcGIS.DataManagementTools;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.DataSourcesFile;
using ESRI.ArcGIS.Display;

namespace DichNhaP_Representation
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new DichNhaP_Representation.LicenseInitializer();

        private static string pathProcessGDB = @"C:\Generalize_25_50\50K_Process.gdb";
        private static string pathFinalGDB = @"C:\Generalize_25_50\50K_Final.gdb";
        private static string fDDanCuCoSoHaTang = "DanCuCoSoHaTang";
        private static string fDGiaoThong = "GiaoThong";
        private static string fCNhaP = "NhaP";
        private static string fCDoanTimDuongBo = "DoanTimDuongBo";
        private static string pathNhaPFinal = System.IO.Path.Combine(new string[] { pathFinalGDB, fDDanCuCoSoHaTang, fCNhaP });
        private static string pathDoanTimDuongBoFinal = System.IO.Path.Combine(new string[] { pathFinalGDB, fDGiaoThong, fCDoanTimDuongBo });
        private static string repDoanTimDuongBoName = "DoanTimDuongBo_Rep";
        private static string repNhaPName = "NhaP_Rep1";
        private static string doanTimDuongBoFinalLayer = "doanTimDuongBoFinalLayer";
        private static string nhaPFinalLayer = "nhaPFinalLayer";
        private static string distanceAlignMarkerToStrokeOrFill = "50 meters";
        private static string distanceDichNhaP = "0 meters";
        private static string buildingGap = "15 meters";
        private static string minimumSize = "20 meters";
        private static string invisibilityFieldName = "invisibility_field";

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });

            //ResolveBuildingConflicts();
            //SetEmptyShapeRepresentation();
            DeleteField();

            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }

        private static void ResolveBuildingConflicts()
        {
            #region SetEnvironmentValue
            Geoprocessor GP = new Geoprocessor();
            GP.SetEnvironmentValue("workspace", pathFinalGDB);
            GP.SetEnvironmentValue("referenceScale", "50000");
            GP.OverwriteOutput = true;
            #endregion

            #region Using MakeFeatureLayer Tool
            MakeFeatureLayer makeFeatureLayerTool = new MakeFeatureLayer();
            //MakeFeatureLayer DoanTimDuongBo
            makeFeatureLayerTool.in_features = pathDoanTimDuongBoFinal;
            makeFeatureLayerTool.out_layer = doanTimDuongBoFinalLayer;
            GP.Execute(makeFeatureLayerTool, null);
            //MakeFeatureLayer NhaP
            makeFeatureLayerTool.in_features = pathNhaPFinal;
            makeFeatureLayerTool.out_layer = nhaPFinalLayer;
            GP.Execute(makeFeatureLayerTool, null);
            #endregion

            #region Using AddField
            AddField addFieldTool = new AddField();
            addFieldTool.in_table = nhaPFinalLayer;
            addFieldTool.field_name = invisibilityFieldName;
            addFieldTool.field_type = "Short";
            GP.Execute(addFieldTool, null);
            #endregion

            #region Using SetLayerRepresentation Tool
            SetLayerRepresentation setLayerRepresentationTool = new SetLayerRepresentation();
            //SetLayerRepresentation repDoanTimDuongBo
            setLayerRepresentationTool.in_layer = doanTimDuongBoFinalLayer;
            setLayerRepresentationTool.representation = repDoanTimDuongBoName;
            setLayerRepresentationTool.out_layer = System.IO.Path.Combine(new string[] { pathFinalGDB, "DoanTimDuongBoLayer" });
            GP.Execute(setLayerRepresentationTool, null);
            //SetLayerRepresentation repDoanTimDuongBo
            setLayerRepresentationTool.in_layer = nhaPFinalLayer;
            setLayerRepresentationTool.representation = repNhaPName;

            setLayerRepresentationTool.out_layer = System.IO.Path.Combine(new string[] { pathFinalGDB, "NhaPLayer" });
            GP.Execute(setLayerRepresentationTool, null);
            #endregion

            #region Using AlignMarkerToStrokeOrFill Tool
            AlignMarkerToStrokeOrFill alignMarkerToStrokeOrFillTool = new AlignMarkerToStrokeOrFill();
            alignMarkerToStrokeOrFillTool.in_point_features = nhaPFinalLayer;
            alignMarkerToStrokeOrFillTool.in_line_or_polygon_features = doanTimDuongBoFinalLayer;
            alignMarkerToStrokeOrFillTool.search_distance = distanceAlignMarkerToStrokeOrFill;
            alignMarkerToStrokeOrFillTool.marker_orientation = "PERPENDICULAR";
            GP.Execute(alignMarkerToStrokeOrFillTool, null);
            #endregion

            #region Using ResolveBuildingConflicts Tool
            IGPValueTable valueTableResolveBuildingConflictsTool = new GPValueTableClass();
            IGPDataType dataTypeInputFieldLayer = new GPFeatureLayerTypeClass();
            IGPDataType dataTypeBoolean = new GPStringTypeClass();
            IGPDataType dataTypeGap = new GPLinearUnitTypeClass();
            valueTableResolveBuildingConflictsTool.AddDataType(dataTypeInputFieldLayer);
            valueTableResolveBuildingConflictsTool.AddDataType(dataTypeBoolean);
            valueTableResolveBuildingConflictsTool.AddDataType(dataTypeGap);
            valueTableResolveBuildingConflictsTool.AddRecord(new ESRI.ArcGIS.esriSystem.Array() as IArray);
            valueTableResolveBuildingConflictsTool.SetValue(0, 0, dataTypeInputFieldLayer.CreateValue(doanTimDuongBoFinalLayer));
            valueTableResolveBuildingConflictsTool.SetValue(0, 1, dataTypeBoolean.CreateValue("False"));
            valueTableResolveBuildingConflictsTool.SetValue(0, 2, dataTypeGap.CreateValue(distanceDichNhaP));

            ResolveBuildingConflicts resolveBuildingConflictsTool = new ResolveBuildingConflicts();
            resolveBuildingConflictsTool.in_buildings = nhaPFinalLayer;
            resolveBuildingConflictsTool.in_barriers = valueTableResolveBuildingConflictsTool;
            resolveBuildingConflictsTool.invisibility_field = invisibilityFieldName;
            resolveBuildingConflictsTool.building_gap = buildingGap;
            resolveBuildingConflictsTool.minimum_size = minimumSize;
            GP.Execute(resolveBuildingConflictsTool, null);
            #endregion
        }

        private static void SetEmptyShapeRepresentation()
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathFinalGDB, 0);
            IRepresentationWorkspaceExtension iRepresentationWorkspaceExtension = GetRepresentationFromFeatureClass(iWorkspace);
            IFeatureWorkspace iFeatureWorkspace = iWorkspace as IFeatureWorkspace;
            IFeatureClass featureClassNhaP = iFeatureWorkspace.OpenFeatureClass(fCNhaP);
            IRepresentationClass iRepresentationClass = iRepresentationWorkspaceExtension.OpenRepresentationClass(repNhaPName);
            IGeoDataset iGeoDataset = featureClassNhaP as IGeoDataset;
            IMapContext iMapContext = new MapContext();
            iMapContext.Init(iGeoDataset.SpatialReference, 50000, iGeoDataset.Extent);
            IQueryFilter iQueryFilter = new QueryFilter();
            iQueryFilter.WhereClause = invisibilityFieldName + " = 1";
            IFeatureCursor iFeatureCursor = featureClassNhaP.Search(iQueryFilter, true);
            IFeature iFeature = null;
            while ((iFeature = iFeatureCursor.NextFeature()) != null)
            {
                IRepresentation iRepresentation = iRepresentationClass.GetRepresentation(iFeature, iMapContext);
                iRepresentation.Shape.SetEmpty();
                iRepresentation.UpdateFeature();
                iFeature.Store();
            }
        }

        private static void DeleteField()
        {
            #region SetEnvironmentValue
            Geoprocessor GP = new Geoprocessor();
            #endregion

            #region Using MakeFeatureLayer Tool
            MakeFeatureLayer makeFeatureLayerTool = new MakeFeatureLayer();
            //MakeFeatureLayer NhaP
            makeFeatureLayerTool.in_features = pathNhaPFinal;
            makeFeatureLayerTool.out_layer = nhaPFinalLayer;
            GP.Execute(makeFeatureLayerTool, null);
            #endregion

            #region Using DelteField Tool
            IGPValueTable valueTableDropField = new GPValueTableClass();
            IGPDataType dataTypeField = new FieldTypeClass();
            valueTableDropField.AddDataType(dataTypeField);
            valueTableDropField.AddRecord(new ESRI.ArcGIS.esriSystem.Array() as IArray);
            valueTableDropField.SetValue(0, 0, dataTypeField.CreateValue(invisibilityFieldName));

            DeleteField deleteFieldTool = new ESRI.ArcGIS.DataManagementTools.DeleteField();
            deleteFieldTool.in_table = nhaPFinalLayer;
            deleteFieldTool.drop_field = valueTableDropField;
            GP.Execute(deleteFieldTool, null);
            #endregion
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
