@echo off
title DichNhaP Representation

:: Runs your command
set pathfile=%~dp0%DichNhaPRep.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause