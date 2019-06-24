using ESRI.ArcGIS.esriSystem;
using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using ESRI.ArcGIS.SpatialAnalystTools;
using ESRI.ArcGIS.DataManagementTools;
using ESRI.ArcGIS.DataSourcesGDB;
using ESRI.ArcGIS.Geoprocessor;
using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.CartographyTools;
using ESRI.ArcGIS.Display;

namespace TaoDuongBinhDoPhu
{
    class Program
    {
        private static LicenseInitializer m_AOLicenseInitializer = new TaoDuongBinhDoPhu.LicenseInitializer();
        private static string pathFileRaster = @"C:\Generalize_25_50\Input.tif";
        private static string pathProcessGDB = @"C:\Generalize_25_50\50K_Process.gdb";
        private static string fCDuongBinhDo = "DuongBinhDo";
        private static string fCDuongBinhDoPhuTemp = "DuongBinhDoTemp";
        private static string fCDuongBinhDoPhu = "DuongBinhDo_Phu";
        private static string fDDiaHinh = "DiaHinh";
        private static string pathFDDiaHinh = System.IO.Path.Combine(new string[] { pathProcessGDB, fDDiaHinh });
        private static string pathDuongBinhDo = System.IO.Path.Combine(new string[] { pathProcessGDB, fDDiaHinh, fCDuongBinhDo });
        private static string pathDuongBinhDoPhuTemp = System.IO.Path.Combine(new string[] { pathProcessGDB, fCDuongBinhDoPhuTemp });
        [STAThread()]
        static void Main(string[] args)
        {
            //ESRI License Initializer generated code.
            m_AOLicenseInitializer.InitializeApplication(new esriLicenseProductCode[] { esriLicenseProductCode.esriLicenseProductCodeBasic, esriLicenseProductCode.esriLicenseProductCodeStandard, esriLicenseProductCode.esriLicenseProductCodeAdvanced },
            new esriLicenseExtensionCode[] { });
            Console.WriteLine("Running...");
            Run();
            Console.WriteLine("Success!!!");
            Console.ReadKey();
            //ESRI License Initializer generated code.
            //Do not make any call to ArcObjects after ShutDownApplication()
            m_AOLicenseInitializer.ShutdownApplication();
        }

        private static void Run()
        {
            #region SetEnvironmentValue
            Geoprocessor GP = new Geoprocessor();
            GP.SetEnvironmentValue("workspace", pathProcessGDB);
            GP.OverwriteOutput = true;
            #endregion

            //#region Using Contour Tool
            //Contour contourTool = new Contour();
            //contourTool.in_raster = pathFileRaster;
            //contourTool.out_polyline_features = pathDuongBinhDoPhuTemp;
            //contourTool.contour_interval = 5;
            //contourTool.base_contour = 2.5;
            //contourTool.z_factor = 1;
            //GP.Execute(contourTool, null);
            //#endregion

            #region Using Make Layer
            //string duongBinhDoLayer = "duongBinhDoLayer";
            //MakeFeatureLayer makeFeatureLayer = new MakeFeatureLayer();
            //makeFeatureLayer.in_features = pathDuongBinhDo;
            //makeFeatureLayer.out_layer = duongBinhDoLayer;
            #endregion

            #region Using CreateFeatureclass Tool
            IGPValueTable valueTableCreateFeatureclassTool = new GPValueTableClass();
            IGPDataType dataTypeInputFieldLayer = new GPStringTypeClass();
            valueTableCreateFeatureclassTool.AddDataType(dataTypeInputFieldLayer);
            valueTableCreateFeatureclassTool.AddRecord(new ESRI.ArcGIS.esriSystem.Array() as IArray);
            valueTableCreateFeatureclassTool.SetValue(0, 0, dataTypeInputFieldLayer.CreateValue(pathDuongBinhDo));

            CreateFeatureclass createFeatureclassTool = new CreateFeatureclass();
            createFeatureclassTool.out_path = pathFDDiaHinh;
            createFeatureclassTool.out_path = fCDuongBinhDoPhu;
            createFeatureclassTool.template = valueTableCreateFeatureclassTool;
            GP.Execute(createFeatureclassTool, null);
            #endregion
        }

    }
}
