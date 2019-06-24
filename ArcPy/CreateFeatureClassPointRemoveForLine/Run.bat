@echo off
title SnapTools

:: Runs your command
set pathfile=%~dp0%CreateFeatureClassPointRemoveForLine.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause