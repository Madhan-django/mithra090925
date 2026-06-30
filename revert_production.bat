@echo off
setlocal enabledelayedexpansion

:: ============================================================
::  PRODUCTION REVERT SCRIPT
::  Reverses: half_day_as_cl + saturday_short_day migrations
::  Reverts code to the commit before these changes
:: ============================================================

echo.
echo ============================================================
echo   PRODUCTION REVERT
echo ============================================================
echo.
echo   This will:
echo     1. Reverse migrations 0020 and 0021 (drops 2 columns)
echo     2. Revert code to git commit before these changes
echo.
echo   Data impact: NONE — both columns were BooleanField(default=False)
echo   Existing PayrollSettings rows are unaffected.
echo.

:: ── CONFIG — fill these in for production ──────────────────
set PROJECT_DIR=C:\path\to\your\project
set PYTHON=C:\path\to\python.exe
:: Commit hash BEFORE our changes (run: git log --oneline to find it)
set REVERT_TO_COMMIT=c0eb2dc
:: ────────────────────────────────────────────────────────────

set /p CONFIRM=Type YES to confirm revert:
if /i not "%CONFIRM%"=="YES" (
    echo Revert cancelled.
    pause
    exit /b 0
)

cd /d "%PROJECT_DIR%"

echo.
echo [1/3] Reversing database migrations to 0019...
%PYTHON% manage.py migrate payroll 0019
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Migration revert failed. Check database manually.
    pause
    exit /b 1
)
echo       Migrations reversed. Columns half_day_as_cl and saturday_short_day removed.

echo.
echo [2/3] Reverting code to previous commit (%REVERT_TO_COMMIT%)...
git checkout %REVERT_TO_COMMIT% -- payroll/models.py payroll/forms.py payroll/views.py templates/payroll/monthlyattendance.html templates/payroll/create_psettings.html templates/payroll/edit_psettings.html templates/payroll/psettings.html
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git checkout failed.
    pause
    exit /b 1
)
echo       Code reverted.

echo.
echo [3/3] Collecting static files...
%PYTHON% manage.py collectstatic --noinput --quiet
echo       Done.

echo.
echo ============================================================
echo   REVERT COMPLETE
echo   Database: migrations 0020 and 0021 reversed
echo   Code: 7 files reverted to commit %REVERT_TO_COMMIT%
echo ============================================================
echo.

:: ── Restart your server here ─────────────────────────────────
:: e.g.  net stop myapp & net start myapp
:: ─────────────────────────────────────────────────────────────

pause
exit /b 0
