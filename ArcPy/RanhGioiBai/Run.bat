@echo off
title RanhGioiBai

:: Runs your command
set pathfile=%~dp0%RanhGioiBai.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause