using ESRI.ArcGIS.esriSystem;
using System;

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

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });

            string pathProcessGDB = @"C:\Generalize_25_50\50K_Process.gdb";
            Run(pathProcessGDB);

            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }
        private static void Run(string pathProcessGDB)
        {
            //SetEnvironmentValue
            Geoprocessor GP = new Geoprocessor();
            GP.SetEnvironmentValue("workspace", pathProcessGDB);
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
            detectGraphicConflictTool.out_feature_class = pathProcessGDB + @"\DetectGraphicConflictTool";
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
