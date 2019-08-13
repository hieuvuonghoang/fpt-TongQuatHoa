@echo off
title GeneralizeSharedFeatures.py

:: Runs your command
set pathfile=%~dp0%GeneralizeSharedFeatures.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause