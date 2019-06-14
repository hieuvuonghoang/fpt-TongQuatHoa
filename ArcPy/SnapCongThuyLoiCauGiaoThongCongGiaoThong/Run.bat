@echo off
title SnapTools

:: Runs your command
set pathfile=%~dp0SnapTools.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "50 Meters"

:: Presses any key
pause