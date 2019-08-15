@echo off
title SimplifyProduction

:: Runs your command
set pathfile=%~dp0%SimplifyProduction.py
set pathfileconfig=%~dp0%Configs.json
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig%

:: Presses any key
pause