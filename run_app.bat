@echo off
setlocal
title Project Readiness Checker - Launcher

:: Configuración de colores (Naranja RS sobre fondo oscuro)
color 06

echo ============================================
echo      RS DIGITAL - PROJECT READINESS CHECKER
echo ============================================

:: 1. Verificar si existe el entorno virtual
if not exist ".venv" (
    echo [INFO] Primera instalacion detectada...
    echo [INFO] Creando entorno virtual Python...
    python -m venv .venv
    
    echo [INFO] Instalando dependencias desde requirements.txt...
    call .venv\Scripts\activate
    pip install -r requirements.txt
    
    echo [SUCCESS] Instalacion completada.
) else (
    echo [INFO] Entorno virtual encontrado.
    call .venv\Scripts\activate
)

:: 2. Iniciar la aplicación
echo [INFO] Iniciando Project Readiness Checker...
start /b pythonw main.py

:: 3. (Opcional) Crear/Actualizar acceso directo en el escritorio
echo [INFO] Verificando acceso directo en el Escritorio...
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1

echo [OK] Aplicacion en ejecucion. Puedes cerrar esta ventana.
pause
exit
