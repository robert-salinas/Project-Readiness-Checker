# 📖 Ejemplos Detallados de Uso

En este documento encontrarás ejemplos avanzados de cómo configurar y utilizar el **Project Readiness Checker**.

## 🖥️ Proyecto de Software (Python)

Configuración ideal para un repositorio de Python:

```json
{
    "project_name": "My Python API",
    "project_type": "software",
    "rules": [
        {
            "name": "Check venv",
            "type": "dir_exists",
            "target": ".venv",
            "severity": "warning",
            "remediation": "Crea un entorno virtual con 'python -m venv .venv'"
        },
        {
            "name": "Check Tests",
            "type": "command_success",
            "target": "pytest tests/",
            "severity": "error"
        }
    ]
}
```

## 🔌 Proyecto de Sistemas Embebidos

Validación de herramientas de compilación:

```json
{
    "project_name": "Firmware V1",
    "project_type": "embedded",
    "rules": [
        {
            "name": "GCC ARM installed",
            "type": "command_success",
            "target": "arm-none-eabi-gcc --version",
            "severity": "error"
        },
        {
            "name": "Linker script exists",
            "type": "file_exists",
            "target": "linker.ld",
            "severity": "error"
        }
    ]
}
```

## 🏗️ Proyecto de Hardware

Control de archivos de fabricación:

```json
{
    "project_name": "PCB Motor Control",
    "project_type": "hardware",
    "rules": [
        {
            "name": "Gerber Files",
            "type": "dir_exists",
            "target": "fabrication/gerbers",
            "severity": "error"
        },
        {
            "name": "BOM complete",
            "type": "file_contains",
            "target": "fabrication/BOM.csv",
            "pattern": "Component,Quantity,Value",
            "severity": "error"
        }
    ]
}
```
