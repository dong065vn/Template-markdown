@echo off
REM ============================================
REM ADM Build Script
REM ============================================
REM Build standalone executable with PyInstaller
REM ============================================

echo.
echo =============================================
echo    ADM Build Script
echo =============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

REM Check PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Building ADM...
echo.

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM Build with spec file
pyinstaller adm.spec --clean

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo =============================================
echo    Build Complete!
echo =============================================
echo.
echo Output: dist\ADM.exe
echo.

pause
