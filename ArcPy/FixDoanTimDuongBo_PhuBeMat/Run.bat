@echo off
title FixDoanTimDuongBo_PhuBeMat

:: Runs your command
set pathfile=%~dp0%FixDoanTimDuongBo_PhuBeMat.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig%

:: Presses any key
pause