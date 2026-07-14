@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 fix-home-typography-after-cache.py
) else (
  python fix-home-typography-after-cache.py
)

echo.
pause
