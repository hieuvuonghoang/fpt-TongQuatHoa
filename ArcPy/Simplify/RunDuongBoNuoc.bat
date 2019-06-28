@echo off
title DuongBoNuoc

:: Runs your command
set pathfile=%~dp0%DuongBoNuoc.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause