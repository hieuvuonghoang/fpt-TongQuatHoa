@echo off
title FixPointRemove

:: Runs your command
set pathfile=%~dp0%FixPointRemove.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause