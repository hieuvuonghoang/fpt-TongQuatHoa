@echo off
title DeleteFeature

:: Runs your command
set pathfile=%~dp0%DeleteFeature.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause