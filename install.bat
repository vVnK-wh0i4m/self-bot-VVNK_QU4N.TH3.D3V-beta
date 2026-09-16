@echo off
title VVNK - Cài đặt thư viện
color 0A

echo ============================================
echo       VVNK - Cài đặt thư viện
echo ============================================
echo.

python --version 2>NUL
if %errorlevel% neq 0 (
    echo [!] Python chưa được cài đặt!
    pause
    exit /b 1
)

echo [*] Đang cập nhật pip...
python -m pip install --upgrade pip

echo.
echo [*] Đang cài đặt thư viện...
python install.py

echo.
echo ============================================
echo       Cài đặt xong!
echo ============================================
pause
