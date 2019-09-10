@echo off
title FPT_Simplify.py

:: Runs your command
set pathfile=%~dp0%FPT_Simplify.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause