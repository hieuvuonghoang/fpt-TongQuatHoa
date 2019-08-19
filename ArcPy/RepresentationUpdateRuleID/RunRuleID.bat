@echo off
title ReadIDPhuBeMat

:: Runs your command
set pathfile=%~dp0%ReadIDPhuBeMat.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

pause
:: Presses any key
::pause