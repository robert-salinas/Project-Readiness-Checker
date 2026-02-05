# 🚀 Project Readiness Checker (PRC) v0.1.0

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**PRC** es una herramienta de línea de comandos diseñada para ingenieros que necesitan validar el estado de sus proyectos (Software, Hardware o Sistemas Embebidos) antes de un lanzamiento, entrega o revisión de diseño.

## ✨ Características

- 🛠️ **Motor de Reglas Flexible:** Valida existencia de archivos, directorios, contenido de archivos, ejecución de comandos y variables de entorno.
- 📁 **Multi-dominio:** Configuraciones listas para usar en proyectos de Hardware, Software y Sistemas Embebidos.
- 📊 **Reportes Multi-formato:** Salida visual en CLI, exportación a JSON para CI/CD, y reportes HTML interactivos.
- ⚙️ **Severidad Configurable:** Define qué fallos son críticos (`error`), advertencias (`warning`) o simple información (`info`).

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/robertesteban/Project-Readiness-Checker.git
cd Project-Readiness-Checker

# Instalar dependencias
pip install -e .
```

## 🛠️ Uso Básico

Para verificar un proyecto usando uno de los ejemplos incluidos:

```bash
# Verificación básica en consola
prc check examples/software_project.json

# Generar un reporte HTML
prc check examples/software_project.json --format html --output reporte.html

# Salida en formato JSON para integración
prc check examples/software_project.json --format json
```

## 📝 Configuración de Reglas

Crea un archivo `ready.yaml` o `ready.json`:

```yaml
project_name: "Mi Super Proyecto"
project_type: "software"
rules:
  - name: "README Presente"
    type: "file_exists"
    target: "README.md"
    severity: "error"
    remediation: "Crea un archivo README.md explicando el proyecto."
```

### Tipos de Reglas Soportadas:
- `file_exists`: Verifica que un archivo exista.
- `dir_exists`: Verifica que un directorio exista.
- `file_contains`: Busca un patrón regex en un archivo.
- `command_success`: Ejecuta un comando y verifica que el código de salida sea 0.
- `env_var_set`: Verifica que una variable de entorno esté definida.

## 📖 Documentación Adicional

- [Arquitectura y Decisiones de Diseño](docs/ARCHITECTURE.md)
- [Guía de Contribución](docs/CONTRIBUTING.md)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
