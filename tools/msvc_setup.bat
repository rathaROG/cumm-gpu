@echo off
REM Find Visual Studio installation path using vswhere.exe
FOR /F "delims=" %%i IN ('"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -property installationpath') DO SET InstallPath=%%i

REM Activate Visual Studio Developer Command Prompt environment
CALL "%InstallPath%\Common7\Tools\VsDevCmd.bat" -arch=x64 -no_logo
