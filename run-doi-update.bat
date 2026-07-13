@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 tools\update_publication_dois.py
) else (
  python tools\update_publication_dois.py
)

echo.
pause
