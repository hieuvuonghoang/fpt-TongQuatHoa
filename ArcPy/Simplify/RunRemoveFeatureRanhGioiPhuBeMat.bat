@echo off
title RemoveFeatureRanhGioiPhuBeMat

:: Runs your command
set pathfile=%~dp0%RemoveFeatureRanhGioiPhuBeMat.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause