@echo off
title SimplifyPolygon

:: Runs your command
set pathfile=%~dp0%Simplify.py
set pathfileconfig=%~dp0%ConfigSimplifyPolygon.json
echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig% "BEND_SIMPLIFY" "200 Meters" "#" "RESOLVE_ERRORS" "NO_KEEP"

:: Presses any key
pause