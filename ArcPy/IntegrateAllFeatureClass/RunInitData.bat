@echo off
title InitData

:: Runs your command
set pathfile=%~dp0%InitData.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause