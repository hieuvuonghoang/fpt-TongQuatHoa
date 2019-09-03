@echo off
title RanhGioiDuongBo

:: Runs your command
set pathfile=%~dp0%RanhGioiDuongBo.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause