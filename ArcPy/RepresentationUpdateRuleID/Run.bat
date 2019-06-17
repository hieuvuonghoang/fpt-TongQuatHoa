@echo off
title RepresentationUpdateRuleID

:: Runs your command
set pathfile=%~dp0RepresentationUpdateRuleID.py
echo.%pathfile%
c:
cd %python27%
python %pathfile%

::
pause