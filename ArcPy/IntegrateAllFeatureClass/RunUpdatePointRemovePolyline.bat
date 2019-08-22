@echo off
title UpdatePointRemovePolyline

:: Runs your command
set pathfile=%~dp0%UpdatePointRemovePolyline.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause