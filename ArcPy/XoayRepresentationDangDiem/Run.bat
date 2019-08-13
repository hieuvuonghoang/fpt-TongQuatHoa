@echo off
title XoayRepresentation

:: Runs your command
set pathfile=%~dp0%XoayRepresentationDangDiem.py
set pathfileconfig=%~dp0%ConfigTools.json
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig%

:: Presses any key
pause