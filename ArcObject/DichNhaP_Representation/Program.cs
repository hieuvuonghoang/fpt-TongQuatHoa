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
        private static string confilctDistance = "0 meters";
        private static string distanceAlignMarkerToStrokeOrFill = "50 meters";
        private static string distanceDichNhaP = "0 meters";
        private static string buildingGap = "15 meters";
        private static string minimumSize = "20 meters";

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });

            //Run(pathFinalGDB);
            Execute();
            //Example();

            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }

        static void Example()
        {

            Geoprocessor GP = new Geoprocessor();
            GP.SetEnvironmentValue("workspace", "in_memory");
            GP.SetEnvironmentValue("referenceScale", "50000");
            GP.OverwriteOutput = true;

            IGPValueTable valueTable = new GPValueTable() as IGPValueTable;
            IGPDataType dataTypeFeatureClass = new DEFeatureClassType() as IGPDataType;
            valueTable.AddDataType(dataTypeFeatureClass);
            IGPDataType dataTypeLongType = new GPLongType() as IGPDataType;
            valueTable.AddDataType(dataTypeLongType);

            IGPValue valueOneA = dataTypeFeatureClass.CreateValue(pathDoanTimDuongBoFinal);
            IGPValue valueTwoA = dataTypeLongType.CreateValue("0");
            IGPValue valueOneB = dataTypeFeatureClass.CreateValue(pathNhaPFinal);
            IGPValue valueTwoB = dataTypeLongType.CreateValue("1");

            IArray arrayOne = new ESRI.ArcGIS.esriSystem.Array();
            arrayOne.Add(valueOneA);
            arrayOne.Add(valueTwoA);
            IArray arrayTwo = new ESRI.ArcGIS.esriSystem.Array();
            arrayTwo.Add(valueOneB);
            arrayTwo.Add(valueTwoB);
            valueTable.AddRecord(arrayOne);
            valueTable.AddRecord(arrayTwo);

            Console.WriteLine(valueTable.GetValue(0, 0).GetAsText());


            //IGPValue value = dataType.CreateValue(pathDoanTimDuongBoFinal);
            //value.SetAsText(pathDoanTimDuongBoFinal);
            //Console.WriteLine(value.GetAsText());
            //valueTable.SetValue(0, 0, value);


            Intersect intersectTool = new Intersect();
            intersectTool.in_features = valueTable;
            intersectTool.out_feature_class = System.IO.Path.Combine(new string[] { pathProcessGDB, "TempIntersect" });
            intersectTool.output_type = "POINT";
            GP.Execute(intersectTool, null);

        }
        static void Execute()
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
            addFieldTool.field_name = "invisibility_field";
            addFieldTool.field_type = "Short";
            GP.Execute(addFieldTool, null);
            addFieldTool.in_table = nhaPFinalLayer;
            addFieldTool.field_name = "ShapeIsEmpty";
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

            #region Using Detect Graphic Conflict Tool
            string nhaPConflict = "in_memory\\nhaPConflict";
            DetectGraphicConflict detectGraphicConflictTool = new DetectGraphicConflict();
            detectGraphicConflictTool.in_features = nhaPFinalLayer;
            detectGraphicConflictTool.out_feature_class = nhaPConflict;
            detectGraphicConflictTool.conflict_features = doanTimDuongBoFinalLayer;
            detectGraphicConflictTool.conflict_distance = confilctDistance;
            GP.Execute(detectGraphicConflictTool, null);
            #endregion

            #region Using Table Select Tool
            string tableNhaPConflict = "in_memory\\tableNhaPConflict";
            TableSelect tableSelectTool = new TableSelect();
            tableSelectTool.in_table = nhaPConflict;
            tableSelectTool.out_table = tableNhaPConflict;
            GP.Execute(tableSelectTool, null);
            #endregion

            #region Using Statistics Tool
            string tableNhaPConflictStatistics = "in_memory\\tableNhaPConflictStatistics";

            IGPValueTable valueTableStatisticsTool = new GPValueTableClass();
            IGPDataType dataTypeField = new FieldTypeClass();
            IGPDataType dataTypeStatistics = new GPStringTypeClass();
            valueTableStatisticsTool.AddDataType(dataTypeField);
            valueTableStatisticsTool.AddDataType(dataTypeStatistics);
            valueTableStatisticsTool.AddRecord(new ESRI.ArcGIS.esriSystem.Array() as IArray);
            valueTableStatisticsTool.SetValue(0, 0, dataTypeField.CreateValue("FID_DoanTimDuongBo"));
            valueTableStatisticsTool.SetValue(0, 1, dataTypeStatistics.CreateValue("FIRST"));

            Statistics statisticsTool = new Statistics();
            statisticsTool.in_table = tableNhaPConflict;
            statisticsTool.out_table = tableNhaPConflictStatistics;
            statisticsTool.statistics_fields = valueTableStatisticsTool;
            statisticsTool.case_field = "FID_NhaP";
            GP.Execute(statisticsTool, null);
            #endregion

            #region Using AddJoin
            AddJoin addJoinTool = new AddJoin();
            addJoinTool.in_layer_or_view = nhaPFinalLayer;
            addJoinTool.in_field = "OBJECTID";
            addJoinTool.join_table = tableNhaPConflictStatistics;
            addJoinTool.join_field = "FID_NhaP";
            GP.Execute(addJoinTool, null);
            #endregion

            #region Using SelectLayerByAttribute
            SelectLayerByAttribute selectLayerByAttributeTool = new SelectLayerByAttribute();
            selectLayerByAttributeTool.in_layer_or_view = nhaPFinalLayer;
            selectLayerByAttributeTool.selection_type = "NEW_SELECTION";
            selectLayerByAttributeTool.where_clause = "tableNhaPConflictStatistics.FID_NhaP IS NOT NULL";
            GP.Execute(selectLayerByAttributeTool, null);
            #endregion

            #region Using CalculateField
            CalculateField calculateFieldTool = new CalculateField();
            calculateFieldTool.in_table = nhaPFinalLayer;
            calculateFieldTool.field = "invisibility_field";
            calculateFieldTool.expression = "0";
            GP.Execute(calculateFieldTool, null);
            #endregion

            #region Using RemoveJoin
            RemoveJoin removeJoinTool = new RemoveJoin();
            removeJoinTool.in_layer_or_view = nhaPFinalLayer;
            removeJoinTool.join_name = "tableNhaPConflictStatistics";
            GP.Execute(removeJoinTool, null);
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
            resolveBuildingConflictsTool.invisibility_field = "invisibility_field";
            resolveBuildingConflictsTool.building_gap = buildingGap;
            resolveBuildingConflictsTool.minimum_size = minimumSize;
            GP.Execute(resolveBuildingConflictsTool, null);
            #endregion


            //Part B
            #region Using Detect Graphic Conflict Tool
            string nhaPConflictSauDich = "in_memory\\nhaPConflictSauDich";
            detectGraphicConflictTool.in_features = nhaPFinalLayer;
            detectGraphicConflictTool.out_feature_class = nhaPConflictSauDich;
            detectGraphicConflictTool.conflict_features = doanTimDuongBoFinalLayer;
            detectGraphicConflictTool.conflict_distance = confilctDistance;
            GP.Execute(detectGraphicConflictTool, null);
            #endregion

            #region Using Table Select Tool
            string tableNhaPConflictSauDich = "in_memory\\tableNhaPConflictSauDich";
            tableSelectTool.in_table = nhaPConflictSauDich;
            tableSelectTool.out_table = tableNhaPConflictSauDich;
            GP.Execute(tableSelectTool, null);
            #endregion

            #region Using Statistics Tool
            string tableNhaPConflictStatisticsSauDich = "in_memory\\tableNhaPConflictStatisticsSauDich";

            valueTableStatisticsTool.RemoveRecord(0);
            valueTableStatisticsTool.AddRecord(new ESRI.ArcGIS.esriSystem.Array() as IArray);
            valueTableStatisticsTool.SetValue(0, 0, dataTypeField.CreateValue("FID_DoanTimDuongBo"));
            valueTableStatisticsTool.SetValue(0, 1, dataTypeStatistics.CreateValue("FIRST"));

            statisticsTool.in_table = tableNhaPConflictSauDich;
            statisticsTool.out_table = tableNhaPConflictStatisticsSauDich;
            statisticsTool.statistics_fields = valueTableStatisticsTool;
            statisticsTool.case_field = "FID_NhaP";
            GP.Execute(statisticsTool, null);
            #endregion

            #region Using AddJoin
            addJoinTool.in_layer_or_view = nhaPFinalLayer;
            addJoinTool.in_field = "OBJECTID";
            addJoinTool.join_table = tableNhaPConflictStatisticsSauDich;
            addJoinTool.join_field = "FID_NhaP";
            GP.Execute(addJoinTool, null);
            #endregion

            #region Using SelectLayerByAttribute
            selectLayerByAttributeTool.in_layer_or_view = nhaPFinalLayer;
            selectLayerByAttributeTool.selection_type = "NEW_SELECTION";
            selectLayerByAttributeTool.where_clause = "tableNhaPConflictStatisticsSauDich.FID_NhaP IS NOT NULL";
            GP.Execute(selectLayerByAttributeTool, null);
            #endregion

            #region Using CalculateField
            calculateFieldTool.in_table = nhaPFinalLayer;
            calculateFieldTool.field = "ShapeISEmpty";
            calculateFieldTool.expression = "1";
            GP.Execute(calculateFieldTool, null);
            #endregion
        }

        private static void Run(string pathGDB)
        {
            //SetEnvironmentValue
            Geoprocessor GP = new Geoprocessor();
            GP.SetEnvironmentValue("workspace", pathGDB);
            GP.SetEnvironmentValue("referenceScale", "50000");
            GP.OverwriteOutput = true;
            //Init parameters
            string fCDoanTimDuongBo = "DoanTimDuongBo";
            string fCDoanTimDuongBoLayer = "DoanTimDuongBoLayer";
            string repDoanTimDuongBo = "DoanTimDuongBo_Rep";
            string fCNhaP = "NhaP";
            string fCNhaPLayer = "NhaPLayer";
            string repNhaP = "NhaP_Rep1";
            string confilctDistance = "0 Meters";
            string lineConnectionAllowance = "0 Meters";
            //Using MakeFeatureLayer Tool
            MakeFeatureLayer makeFeatureLayerTool = new MakeFeatureLayer();
            //MakeFeatureLayer DoanTimDuongBo
            makeFeatureLayerTool.in_features = fCDoanTimDuongBo;
            makeFeatureLayerTool.out_layer = fCDoanTimDuongBoLayer;
            GP.Execute(makeFeatureLayerTool, null);
            //MakeFeatureLayer NhaP
            makeFeatureLayerTool.in_features = fCNhaP;
            makeFeatureLayerTool.out_layer = fCNhaPLayer;
            GP.Execute(makeFeatureLayerTool, null);
            //Using SetLayerRepresentation Tool
            SetLayerRepresentation setLayerRepresentationTool = new SetLayerRepresentation();
            //SetLayerRepresentation repDoanTimDuongBo
            setLayerRepresentationTool.in_layer = fCDoanTimDuongBoLayer;
            setLayerRepresentationTool.representation = repDoanTimDuongBo;
            GP.Execute(setLayerRepresentationTool, null);
            //SetLayerRepresentation repDoanTimDuongBo
            setLayerRepresentationTool.in_layer = fCNhaPLayer;
            setLayerRepresentationTool.representation = repNhaP;
            GP.Execute(setLayerRepresentationTool, null);
            //Using DetectGraphicConflict Tool
            DetectGraphicConflict detectGraphicConflictTool = new DetectGraphicConflict();
            detectGraphicConflictTool.in_features = fCDoanTimDuongBoLayer;
            detectGraphicConflictTool.out_feature_class = pathGDB + @"\DetectGraphicConflictTool";
            detectGraphicConflictTool.conflict_features = fCNhaPLayer;
            detectGraphicConflictTool.conflict_distance = confilctDistance;
            detectGraphicConflictTool.line_connection_allowance = lineConnectionAllowance;
            GP.Execute(detectGraphicConflictTool, null);
        }
        private static IRepresentationWorkspaceExtension GetRepresentationFromFeatureClass(IWorkspace iWorkspace)
        {
            IWorkspaceExtensionManager iWorkspaceExtensionManager = (IWorkspaceExtensionManager)iWorkspace;
            UIDClass uIDClass = new UIDClass();
            uIDClass.Value = "{FD05270A-8E0B-4823-9DEE-F149347C32B6}";
            return (IRepresentationWorkspaceExtension)iWorkspaceExtensionManager.FindExtension(uIDClass);
        }
        private static IFeatureClass OpenFeatureClass(IWorkspace iWorkspace, string featureDatasetName, string featureClassName)
        {
            IEnumDataset iEnumDataset = iWorkspace.Datasets[esriDatasetType.esriDTFeatureDataset];
            //iEnumDataset.Reset();

            IDataset iDataset = null;
            while ((iDataset = iEnumDataset.Next()) != null)
            {
                if (iDataset.Name == featureDatasetName)
                {
                    break;
                }
            }
            if (iDataset != null)
            {
                IEnumDataset iEnumDatasetSub = iDataset.Subsets;
                //iEnumDatasetSub.Reset();

                IDataset iDatasetSub = null;
                while ((iDatasetSub = iEnumDatasetSub.Next()) != null)
                {
                    if (iDatasetSub.Name == featureClassName)
                    {
                        break;
                    }
                }
                if (iDatasetSub != null)
                {
                    IFeatureClass iFeatureClass = iDatasetSub as IFeatureClass;
                    return iFeatureClass;
                }
            }
            return null;
        }
    }
}
