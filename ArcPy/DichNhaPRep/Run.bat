@echo off
title DichNhaP Representation

:: Runs your command
set pathfileResolveBuildingConflict=%~dp0%ResolveBuildingConflict.py
set pathfileResolveConflictNhaP=%~dp0%ResolveConflictNhaP.py
set pathfileConfig=%~dp0%ConfigTools.json
c:
cd %python27%
::python %pathfile% "50 Meters" "0 Meters" "15 Meters" "20 Meters"
echo.%pathfileResolveBuildingConflict%
python %pathfileResolveBuildingConflict% "60 Meters" "0.3 Meters" "10 Meters" "15 Meters"
echo.%pathfileResolveConflictNhaP%
python %pathfileResolveConflictNhaP% %pathfileConfig% "0 Meters" "0 Meters"

:: Presses any key
pause