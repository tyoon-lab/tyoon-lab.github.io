@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 complete_remaining_dois.py
) else (
  python complete_remaining_dois.py
)

echo.
pause
