@echo off
setlocal enabledelayedexpansion

:: ============================================================
::  PRODUCTION DEPLOY SCRIPT
::  Changes: half_day_as_cl + saturday_short_day payroll fields
::  Safe: both are BooleanField(default=False) — no data loss
::  Revert: run revert_production.bat
:: ============================================================

echo.
echo ============================================================
echo   PRODUCTION DEPLOY
echo ============================================================
echo.

:: ── CONFIG — fill these in for production ──────────────────
set PROJECT_DIR=C:\path\to\your\project
set PYTHON=C:\path\to\python.exe
set DB_NAME=your_db_name
set DB_USER=your_db_user
set DB_PASS=your_db_password
set DB_HOST=localhost
set BACKUP_DIR=C:\backups
:: ────────────────────────────────────────────────────────────

cd /d "%PROJECT_DIR%"

echo [1/6] Recording current migration state...
%PYTHON% manage.py showmigrations payroll > "%BACKUP_DIR%\migration_state_before_%date:~-4,4%%date:~-10,2%%date:~-7,2%.txt" 2>&1
echo       Saved to %BACKUP_DIR%\migration_state_before_...txt

echo.
echo [2/6] Taking database backup...
set BACKUP_FILE=%BACKUP_DIR%\db_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%.sql
set BACKUP_FILE=%BACKUP_FILE: =0%
mysqldump -h %DB_HOST% -u %DB_USER% -p%DB_PASS% %DB_NAME% > "%BACKUP_FILE%"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Database backup failed. Aborting deploy.
    pause
    exit /b 1
)
echo       Backup saved to %BACKUP_FILE%

echo.
echo [3/6] Pulling latest code from git...
git pull origin main
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git pull failed. Aborting deploy.
    pause
    exit /b 1
)

echo.
echo [4/6] Installing/updating dependencies...
%PYTHON% -m pip install -r requirements.txt --quiet
echo       Done.

echo.
echo [5/6] Running database migrations...
echo       Step 1: staff migrations (0006 adds staff_type column)...
%PYTHON% manage.py migrate staff
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] staff migrate failed.
    pause
    exit /b 1
)
echo       Step 2: payroll migrations (0011 depends on staff 0006, then 0020 and 0021)...
%PYTHON% manage.py migrate payroll
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] payroll migrate failed. Reverting...
    goto :revert_migration
)
echo       Step 3: all remaining app migrations...
%PYTHON% manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Full migrate failed.
    pause
    exit /b 1
)
echo       All migrations applied successfully.

echo.
echo [6/6] Collecting static files...
%PYTHON% manage.py collectstatic --noinput --quiet
echo       Done.

echo.
echo ============================================================
echo   DEPLOY COMPLETE
echo   New fields added (both default OFF, no existing data changed):
echo     - payroll_payrollsettings.half_day_as_cl
echo     - payroll_payrollsettings.saturday_short_day
echo.
echo   To activate: go to Payroll Settings and enable the toggles.
echo   To revert:   run revert_production.bat
echo ============================================================
echo.

:: ── Restart your server here ─────────────────────────────────
:: If using waitress / IIS / supervisor, add your restart command:
:: e.g.  net stop myapp & net start myapp
:: ─────────────────────────────────────────────────────────────

pause
exit /b 0

:revert_migration
echo.
echo [AUTO-REVERT] Reversing payroll migrations to 0019...
%PYTHON% manage.py migrate payroll 0019
echo [AUTO-REVERT] Done. Code was NOT reverted — run revert_production.bat for full rollback.
pause
exit /b 1
