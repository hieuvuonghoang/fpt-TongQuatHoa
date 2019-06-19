using ESRI.ArcGIS.esriSystem;
using System;
using System.IO;

using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geoprocessor;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.AnalysisTools;
using ESRI.ArcGIS.CartographyTools;
using ESRI.ArcGIS.DataManagementTools;

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
        private static string confilctDistance = "0 Meters";

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });

            //Run(pathFinalGDB);
            Execute();

            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
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

            #region Using SetLayerRepresentation Tool
            SetLayerRepresentation setLayerRepresentationTool = new SetLayerRepresentation();
            //SetLayerRepresentation repDoanTimDuongBo
            setLayerRepresentationTool.in_layer = doanTimDuongBoFinalLayer;
            setLayerRepresentationTool.representation = repDoanTimDuongBoName;
            GP.Execute(setLayerRepresentationTool, null);
            //SetLayerRepresentation repDoanTimDuongBo
            setLayerRepresentationTool.in_layer = nhaPFinalLayer;
            setLayerRepresentationTool.representation = repNhaPName;
            GP.Execute(setLayerRepresentationTool, null);
            #endregion
            
            #region Using DetectGraphicConflict Tool
            DetectGraphicConflict detectGraphicConflictTool = new DetectGraphicConflict();
            detectGraphicConflictTool.in_features = nhaPFinalLayer;
            detectGraphicConflictTool.out_feature_class = System.IO.Path.Combine(new string [] { pathProcessGDB, "NhaPConflictDoanTimDuongBo"});
            detectGraphicConflictTool.conflict_features = doanTimDuongBoFinalLayer;
            detectGraphicConflictTool.conflict_distance = confilctDistance;
            detectGraphicConflictTool.line_connection_allowance = "0 Meters";
            GP.Execute(detectGraphicConflictTool, null);
            #endregion

            #region Using Table Select Tool
            TableSelect tableSelectTool = new TableSelect();
            tableSelectTool.in_table = System.IO.Path.Combine(new string[] { pathProcessGDB, "NhaPConflictDoanTimDuongBo" });
            tableSelectTool.out_table = System.IO.Path.Combine(new string[] { pathProcessGDB, "NhaPConflictTable" });
            tableSelectTool.where_clause = "OBJECTID IS NOT NULL";
            GP.Execute(tableSelectTool, null);
            #endregion

            #region Add Field
            //Add Field
            AddField addFieldTool = new AddField();
            addFieldTool.in_table = nhaPFinalLayer;
            addFieldTool.field_name = "invisibility_field";
            addFieldTool.field_type = "Short";
            GP.Execute(addFieldTool, null);
            #endregion

            #region Add Join
            AddJoin addJoinTool = new AddJoin();
            addJoinTool.in_layer_or_view = nhaPFinalLayer;
            addJoinTool.in_field = "OBJECTID";
            addJoinTool.join_table = System.IO.Path.Combine(new string[] { pathProcessGDB, "NhaPConflictTable" });
            addJoinTool.join_field = "NhaPConflictTable.FID_NhaP";
            GP.Execute(addJoinTool, null);
            #endregion

            #region Select Layer By Attribute
            SelectLayerByAttribute selectLayerByAttributeTool = new SelectLayerByAttribute();
            selectLayerByAttributeTool.in_layer_or_view = nhaPFinalLayer;
            selectLayerByAttributeTool.selection_type = "NEW_SELECTION";
            selectLayerByAttributeTool.where_clause = "NhaPConflictTable.FID_NhaP IS NOT NULL";
            GP.Execute(selectLayerByAttributeTool, null);
            #endregion

            #region Calculate Field
            CalculateField calculateTool = new CalculateField();
            calculateTool.in_table = nhaPFinalLayer;
            calculateTool.field = "invisibility_field";
            calculateTool.expression = "0";
            GP.Execute(calculateTool, null);
            #endregion

            #region Remove Join
            RemoveJoin removeJoinTool = new RemoveJoin();
            removeJoinTool.in_layer_or_view = nhaPFinalLayer;
            removeJoinTool.join_name = "NhaPConflictTable";
            GP.Execute(removeJoinTool, null);
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
