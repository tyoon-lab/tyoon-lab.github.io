@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 update-home-identity.py
) else (
  python update-home-identity.py
)

echo.
pause
