@echo off
title ChongDePolygon

:: Runs your command
set pathfile=%~dp0%ChongDePolygon.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "C:\Generalize_25_50\Feature.json" "C:\Generalize_25_50\FeatureClass.json"

:: Presses any key
pause