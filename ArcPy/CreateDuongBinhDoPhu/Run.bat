@echo off
title CreateDuongBinhDoPhu

:: Runs your command
set pathfile=%~dp0CreateDuongBinhDoPhu.py
echo.%pathfile%
c:
cd %python27%
python %pathfile% 5 2.5 1

::
pause