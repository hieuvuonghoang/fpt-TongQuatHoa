using ESRI.ArcGIS.esriSystem;
using System;
using System.IO;
using System.Collections.Generic;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.DataSourcesGDB;
using Newtonsoft.Json;

namespace RepresentationUpdateRuleID
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new RepresentationUpdateRuleID.LicenseInitializer();

        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic },
            new esriLicenseExtensionCode[] { });
            //ESRI License Initializer generated code.

            #region "Run"
            string pathCurrent = Directory.GetCurrentDirectory();
            string pathFileConfig = Path.Combine(pathCurrent, "ConfigTools.json");
            Console.WriteLine("pathGDB: {0}", args[0]);
            Console.WriteLine("pathFileConfig: {0}", pathFileConfig);
            RunUpdateRuleID(args[0], pathFileConfig);
            #endregion

            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }

        static void RunUpdateRuleID(string pathGDB, string pathFileConfig)
        {
            IWorkspaceFactory iWorkspaceFactory = new FileGDBWorkspaceFactoryClass();
            IWorkspace iWorkspace = iWorkspaceFactory.OpenFromFile(pathGDB, 0);
            IRepresentationWorkspaceExtension iRepresentationWorkspaceExtension = GetRepresentationFromFeatureClass(iWorkspace);
            List<ConfigTool> listConfig = ReadFileConfig(pathFileConfig);
            foreach (ConfigTool elemConfig in listConfig)
            {
                foreach (FeatureClass elemFeatureClass in elemConfig.listFeatureClass)
                {
                    IFeatureClass featureClass = OpenFeatureClass(iWorkspace, elemConfig.nameFeatureDataset, elemFeatureClass.nameFeatureClass);
                    if (featureClass != null)
                    {
                        foreach (Representation elemRepresentation in elemFeatureClass.listRepresentation)
                        {
                            foreach (Rule elemRule in elemRepresentation.listRule)
                            {
                                int ruleID;
                                if ((int.TryParse(elemRule.ruleID, out ruleID)) && (elemRule.querySQL != ""))
                                {
                                    UpdateRuleID(featureClass, iRepresentationWorkspaceExtension, elemRepresentation.nameRepresentation, ruleID, elemRule.querySQL);
                                }
                            }
                        }
                    }
                }
            }
        }

        static IRepresentationWorkspaceExtension GetRepresentationFromFeatureClass(IWorkspace iWorkspace)
        {
            IWorkspaceExtensionManager iWorkspaceExtensionManager = (IWorkspaceExtensionManager)iWorkspace;
            UIDClass uIDClass = new UIDClass();
            uIDClass.Value = "{FD05270A-8E0B-4823-9DEE-F149347C32B6}";
            return (IRepresentationWorkspaceExtension)iWorkspaceExtensionManager.FindExtension(uIDClass);
        }

        static List<ConfigTool> ReadFileConfig(string pathFile)
        {
            return JsonConvert.DeserializeObject<List<ConfigTool>>(File.ReadAllText(pathFile));
        }

        static IFeatureClass OpenFeatureClass(IWorkspace iWorkspace, string featureDatasetName, string featureClassName)
        {
            IEnumDataset iEnumDataset = iWorkspace.Datasets[esriDatasetType.esriDTFeatureDataset];
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

        static void UpdateRuleID(IFeatureClass featureClass, IRepresentationWorkspaceExtension iRepresentationWorkspaceExtension, string representationName, int ruleID, string querySQL)
        {
            IRepresentationClass iRepresentationClass = iRepresentationWorkspaceExtension.OpenRepresentationClass(representationName);
            if (iRepresentationClass != null)
            {
                IGeoDataset iGeoDataset = featureClass as IGeoDataset;
                IMapContext iMapContext = new MapContext();
                iMapContext.Init(iGeoDataset.SpatialReference, 50000, iGeoDataset.Extent);
                IQueryFilter iQueryFilter = new QueryFilter();
                iQueryFilter.WhereClause = querySQL;
                IFeatureCursor iFeatureCursor = featureClass.Search(iQueryFilter, true);
                IFeature iFeature = null;
                while ((iFeature = iFeatureCursor.NextFeature()) != null)
                {
                    IRepresentation iRepresentation = iRepresentationClass.GetRepresentation(iFeature, iMapContext);
                    if (iRepresentation != null && iRepresentation.RuleID != ruleID)
                    {
                        iRepresentation.RuleID = ruleID;
                        iRepresentation.UpdateFeature();
                        iFeature.Store();
                    }
                }
            }
        }

    }
}
