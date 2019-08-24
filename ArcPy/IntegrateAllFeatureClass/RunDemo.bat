@echo off
title Demo

:: Runs your command
set pathfile=%~dp0%Demo.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause