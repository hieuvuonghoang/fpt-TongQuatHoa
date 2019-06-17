@echo off
title XoayRepresentation

:: Runs your command
set pathfile=%~dp0%XoayRepresentation.py
set pathfileconfig=%~dp0%ConfigTools.json
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig% "50 Meters"

:: Presses any key
pause