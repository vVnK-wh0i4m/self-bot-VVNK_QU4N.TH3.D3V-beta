@echo off
title VVNK - QU4N.TH3.D3V
color 0A

echo ============================================
echo        VVNK - QU4N.TH3.D3V
echo ============================================
echo.

python --version 2>NUL
if %errorlevel% neq 0 (
    echo [!] Python chua duoc cai dat!
    pause
    exit /b 1
)

if not exist "config" mkdir config
if not exist "config\config.json" (
    echo {"token": "", "prefix": ".", "sniper_webhook": ""} > config\config.json
)

python -c "import json; d=json.load(open('config/config.json')); exit(0 if d.get('token','').strip() else 1)" 2>NUL
if %errorlevel% neq 0 (
    echo [!] Chua co token trong config!
    echo [!] Mo notepad de nhap token...
    notepad config\config.json
    echo.
    echo [!] Nhap token xong nhan Enter de tiep tuc...
    pause >NUL
)

if not exist "music" mkdir music
if not exist "ffmpeg" mkdir ffmpeg
if not exist "trash" mkdir trash
if not exist "cogs" mkdir cogs

echo.
echo [*] Dang cap nhat pip...
python -m pip install --upgrade pip 2>NUL

echo.
echo [*] Dang cai dat thu vien...
python install.py

echo.
echo ============================================
echo          Dang khoi dong bot...
echo ============================================
echo.

python bot.py
pause
