@echo off
title XoayRepresentationDangDiem

:: Runs your command
set pathfile=%~dp0%XoayRepresentationDangDiem.py
set pathfileconfig=%~dp0%ConfigTools.json
set pathSetAngle=%~dp0%Release\SetAngleRepresentationPoint.exe

echo.%pathfile%
c:
cd %python27%
python %pathfile% %pathfileconfig%

%pathSetAngle% "C:\Generalize_25_50\50K_Final.gdb" "CauGiaoThongP" "CauGiaoThongP_Rep" ""
%pathSetAngle% "C:\Generalize_25_50\50K_Final.gdb" "CongGiaoThongP" "CongGiaoThongP_RepPhai" ""
%pathSetAngle% "C:\Generalize_25_50\50K_Final.gdb" "CongGiaoThongP" "CongGiaoThongP_RepTrai" ""
%pathSetAngle% "C:\Generalize_25_50\50K_Final.gdb" "CongThuyLoiP" "CongThuyLoiP_Rep" ""

:: Presses any key
pause