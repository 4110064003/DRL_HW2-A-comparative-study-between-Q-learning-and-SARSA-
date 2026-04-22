@echo off
setlocal EnableExtensions

set "MSG=%~1"
if /I "%~1"=="-CommitMessage" set "MSG=%~2"
if /I "%~1"=="CommitMessage" set "MSG=%~2"

if not defined MSG (
	powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0ending.ps1"
) else (
	powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0ending.ps1" -CommitMessage "%MSG%"
)

endlocal
