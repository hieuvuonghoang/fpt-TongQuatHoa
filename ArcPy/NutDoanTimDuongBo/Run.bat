@echo off 
title NutDoanTimDuongBo

:: Runs your command
set pathfile=%~dp0%CreateNodeLine.py.py
c:
cd %python27%
echo.%pathfile%
python %pathfile%

:: Presses any key
pause