@echo off
title DichNhaP Representation

:: Runs your command
set pathfile=%~dp0%DichNhaPRep.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "50 Meters" "0 Meters" "15 Meters" "20 Meters"

:: Presses any key
pause