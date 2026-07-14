@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 update-hero-about-hierarchy.py
) else (
  python update-hero-about-hierarchy.py
)

echo.
pause
