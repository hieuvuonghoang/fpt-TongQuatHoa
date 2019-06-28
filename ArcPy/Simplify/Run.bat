@echo off
title DuongBoNuoc

:: Runs your command
set pathfile=%~dp0%Simplify.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause