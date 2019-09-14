@echo off 
title DichNhaP Representation

:: Runs your command
set pathfileResolveBuildingConflict=%~dp0%ResolveBuildingConflict.py
set pathfileResolveConflictNhaP=%~dp0%ResolveConflictNhaP.py
set pathfileConfig=%~dp0%ConfigTools.json
c:
cd %python27%
echo.%pathfileResolveBuildingConflict%
python %pathfileResolveBuildingConflict% "150 Meters" "15 Meters" "1 Meters" "35 Meters"
echo.%pathfileResolveConflictNhaP%
python %pathfileResolveConflictNhaP% %pathfileConfig% "0 Meters" "0 Meters"

:: Presses any key
pause