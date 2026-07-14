@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 update-research-page-refinement.py
) else (
  python update-research-page-refinement.py
)

echo.
pause
