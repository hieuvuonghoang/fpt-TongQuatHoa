@echo off 
title NutDoanTimDuongBo

:: Runs your command
::set pathfileNutDoanTimDuongBo=%~dp0%NutDoanTimDuongBo.py
set pathfileNutDoanTimDuongBo=%~dp0%Count.py
c:
cd %python27%
echo.%pathfileNutDoanTimDuongBo%
python %pathfileNutDoanTimDuongBo%

:: Presses any key
pause