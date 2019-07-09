@echo off
title CreateDuongBinhDoPhu

:: Runs your command
set pathfile=%~dp0%Contour.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "5" "2.5" "1"

:: Runs your command
set pathfile=%~dp0%CreateDuongBinhDoPhu.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause