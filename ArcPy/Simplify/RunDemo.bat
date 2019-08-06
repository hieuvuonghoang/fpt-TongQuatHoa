@echo off
title GenFeatureClass

:: Runs your command
set pathfile=%~dp0%GenFeatureClass.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause