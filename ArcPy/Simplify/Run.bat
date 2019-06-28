@echo off
title SnapTools

:: Runs your command
set pathfile=%~dp0%Simplify.py
set pathfileconfig=%~dp0%ConfigSimplifyPolygon.json
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig%

:: Presses any key
pause