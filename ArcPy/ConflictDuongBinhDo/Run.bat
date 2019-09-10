@echo off
title ConflictDuongBinhDo

:: Runs your command
set pathfile=%~dp0%ConflictDuongBinhDo.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

:: Presses any key
pause