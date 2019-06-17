@echo off
title RepresentationUpdateRuleID

:: Runs your command
set pathfile=%~dp0%RepresentationUpdateRuleID.py
set pathfileconfig=%~dp0%ConfigTools.json
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig%

:: Presses any key
pause