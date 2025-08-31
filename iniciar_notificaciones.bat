@echo off
title Gestor de Suscripciones - Servicio de Notificaciones
color 0E

echo ========================================
echo  GESTOR DE SUSCRIPCIONES - DANI666
echo  Servicio de Notificaciones
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar archivos necesarios
if not exist "servicio_notificaciones.py" (
    echo ERROR: No se encuentra servicio_notificaciones.py
    pause
    exit /b 1
)

REM Ejecutar el iniciador
python iniciar_servicio.py

echo.
echo Presiona cualquier tecla para salir...
pause >nul