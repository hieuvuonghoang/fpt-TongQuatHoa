@echo off
title DuongBoNuoc

:: Runs your command
set pathfile=%~dp0%DuongDiaGioi.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% "100 Meters"

:: Presses any key
pause