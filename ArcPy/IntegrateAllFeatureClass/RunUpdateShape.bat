@echo off
title UpdateShape

:: Runs your command
set pathfile=%~dp0%UpdateShape.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause