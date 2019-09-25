@echo off 
title DichNhaP Representation

:: Runs your command
set pathCurrent=%~dp0%
set pathRemoveShape=%pathCurrent%ReleaseRemoveShapeOverride\RemoveShapeOverride.exe
set pathClearShape=%pathCurrent%Release\SetEmptyShapeRepresentation.exe
set pathfileResolveBuildingConflict=%~dp0%ResolveBuildingConflict.py
set pathfileResolveConflictNhaP=%~dp0%ResolveConflictNhaP.py
set pathfileConfig=%~dp0%ConfigTools.json

echo %pathRemoveShape%
echo %pathClearShape%

%pathRemoveShape% "C:\Generalize_25_50\50K_Final.gdb" "NhaP" "Nhap_Rep1" ""

c:
cd %python27%
echo.%pathfileResolveBuildingConflict%
python %pathfileResolveBuildingConflict% "150 Meters" "15 Meters" "1 Meters" "35 Meters"
echo.%pathfileResolveConflictNhaP%
python %pathfileResolveConflictNhaP% %pathfileConfig% "0 Meters" "0 Meters"

%pathClearShape% "C:\Generalize_25_50\50K_Final.gdb" "NhaP" "Nhap_Rep1" "invisibility_field = 1"

:: Presses any key
pause