@echo off
title IntegrateAllFeatureClass

:: Runs your command
set pathfile=%~dp0%IntegrateAllFeatureClass.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause