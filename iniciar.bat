@echo off
cd /d "%~dp0"
title CineMax

where python >nul 2>nul
if errorlevel 1 goto sin_python

powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"
if errorlevel 1 goto ya_encendido

echo.
echo Iniciando CineMax...
echo.

if not exist "venv\Scripts\python.exe" (
    echo Creando el entorno virtual por primera vez...
    python -m venv venv
)

"venv\Scripts\python.exe" -m pip install -q -r requirements.txt

echo Servidor en marcha. El navegador se abre solo.
echo Para apagarlo, cerra esta ventana o apreta Ctrl + C.
echo.

"venv\Scripts\python.exe" backend\app.py

echo.
echo El servidor se cerro.
pause
exit

:ya_encendido
echo.
echo El servidor ya estaba encendido. Abriendo el navegador...
start "" http://127.0.0.1:5000/login.html
exit

:sin_python
echo.
echo No se encontro Python en la computadora.
echo Instalalo desde python.org y marca la opcion "Add Python to PATH".
echo.
pause
exit
