@echo off
title SimplifyProduction

:: Runs your command
set pathfile=%~dp0%SimplifyProduction.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause