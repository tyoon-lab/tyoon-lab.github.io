@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 update-final-hierarchy-tweak.py
) else (
  python update-final-hierarchy-tweak.py
)

echo.
pause
