@echo off
title Simpliify Process Topology

:: Runs your command
set pathfile=%~dp0%InitData.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Runs your command
set pathfile=%~dp0%UpdatePointRemovePolyline.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Runs your command
set pathfile=%~dp0%UpdateShape.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause