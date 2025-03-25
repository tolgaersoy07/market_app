@echo off
:loop
cls
echo [91m[INFO] PROGRAM BASLATILIYOR...[0m
python app.py
echo.
echo [91m[ERROR] PROGRAM YUKARIDAKI SEKILDE HATA VERDI.[0m
echo [91m[INFO] 2 SANIYE SONRA YENIDEN BASLATILACAK.[0m
timeout /t 2 /nobreak >nul
goto loop
