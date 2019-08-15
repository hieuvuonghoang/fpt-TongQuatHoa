@echo off
title Run Tools

::Set pathDirCurrent
set pathDirCurrent=%~dp0%
::Set pathTool: SnapTools
set pathSnapTools=%pathDirCurrent%SnapTools
::Set pathTool: NutDoanTimDuongBo
set pathNutDoanTimDuongBo=%pathDirCurrent%NutDoanTimDuongBo
::Set pathTool: RepresentationUpdateRuleID
set pathRepresentationUpdateRuleID=%pathDirCurrent%RepresentationUpdateRuleID
::Set pathTool: DichNhaPRep
set pathDichNhaPRep=%pathDirCurrent%DichNhaPRep
::Set pathTool: XoayRepresentationDangDiem
set pathXoayRepresentationDangDiem=%pathDirCurrent%XoayRepresentationDangDiem
::Run SnapTools
cd %pathSnapTools%
@echo call | Run.bat
::Run NutDoanTimDuongBo
cd %pathNutDoanTimDuongBo%
@echo call | Run.bat
::Run RepresentationUpdateRuleID
cd %pathRepresentationUpdateRuleID%
@echo call | Run.bat
::Run DichNhaPRep
cd %pathDichNhaPRep%
@echo call | Run.bat
::Run XoayRepresentationDangDiem
cd %pathXoayRepresentationDangDiem%
@echo call | Run.bat
:: Presses any key
pause