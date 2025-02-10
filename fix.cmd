@echo off
:: Check if the script is running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb RunAs"
    exit
)

echo Developer [Mohammed Al-Baqer] 
echo.
title Windows Fix Tool
color 0A
echo     Windows Repair Tool
echo.

:: Clean up unnecessary files
echo Cleaning temporary files...
del /s /q %temp%\*.* 
del /s /q C:\Windows\Temp\*.*

:: Repair system image using DISM
echo Repairing Windows image using DISM...
DISM /Online /Cleanup-image /RestoreHealth

:: Reset network services
echo Resetting network settings...
netsh winsock reset
netsh int ip reset

:: Check and fix disk errors
echo Checking and fixing disk errors...
chkdsk C: /f /r /x

:: Flush DNS cache
echo Flushing DNS cache...
ipconfig /flushdns

echo.
echo The process is complete! It's recommended to restart your computer.
pause
exit
