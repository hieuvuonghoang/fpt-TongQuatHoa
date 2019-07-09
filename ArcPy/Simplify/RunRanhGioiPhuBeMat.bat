@echo off
title RanhGioiPhuBeMat

:: Runs your command
set pathfile=%~dp0%RanhGioiPhuBeMat.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "100 Meters"

:: Presses any key
pause