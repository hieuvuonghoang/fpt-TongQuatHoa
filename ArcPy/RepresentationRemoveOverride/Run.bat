@echo off
title RepresentationRemoveOverride

:: Runs your command
set pathfile=%~dp0%RepresentationRemoveOverride.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "C:\Generalize_25_50\50K_Final.gdb" "DoanTimDuongBo" "DoanTimDuongBo_Rep" "BOTH"
python %pathfile% "C:\Generalize_25_50\50K_Final.gdb" "DoanTimDuongBo" "DoanTimDuongBo_Nen" "BOTH"

:: Presses any key
pause