@echo off
title DemoCreateFeatureClass.py

:: Runs your command
set pathfile=%~dp0%DemoCreateFeatureClass.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause