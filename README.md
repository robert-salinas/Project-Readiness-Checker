# 🚀 Project Readiness Checker (PRC) v0.1.0

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/robert-salinas/Project-Readiness-Checker/actions/workflows/tests.yml/badge.svg)](https://github.com/robert-salinas/Project-Readiness-Checker/actions/workflows/tests.yml)
[![Linting](https://github.com/robert-salinas/Project-Readiness-Checker/actions/workflows/lint.yml/badge.svg)](https://github.com/robert-salinas/Project-Readiness-Checker/actions/workflows/lint.yml)

**PRC** es una herramienta versátil que combina la potencia de una **Línea de Comandos (CLI)** y la comodidad de una **Interfaz Gráfica (GUI)** moderna. Está diseñada para ingenieros que necesitan validar el estado de sus proyectos (Software, Hardware o Sistemas Embebidos) antes de un lanzamiento, entrega o revisión de diseño.

## 💡 El Problema

En proyectos complejos y multidisciplinarios, es común olvidar archivos críticos, configuraciones de entorno o validaciones básicas antes de una entrega. Las listas de verificación manuales son propensas a errores humanos. **PRC** automatiza este proceso, asegurando que cada proyecto cumpla con los estándares de calidad definidos por el equipo.

## ✨ Características Únicas

- 💻 **Interfaz Dual (CLI & GUI):** Acceso rápido vía consola de comandos para tuberías de CI/CD, o interfaz gráfica interactiva con indicadores en tiempo real.
- 🛠️ **Motor de Reglas Flexible:** Valida existencia de archivos, directorios, contenido de archivos, ejecución de comandos y variables de entorno.
- 📁 **Multi-dominio:** Configuraciones listas para usar en proyectos de Hardware, Software y Sistemas Embebidos.
- 📊 **Reportes Multi-formato:** Salida visual en CLI, exportación JSON para integración, y reportes HTML interactivos (Soportados en GUI y CLI).
- ⚙️ **Severidad Configurable:** Define qué fallos son críticos (`error`), advertencias (`warning`) o simple información (`info`).

## 🛠️ Stack Tecnológico

- **Python 3.11+**
- **Typer** (CLI Interface)
- **Pydantic** (Data Validation)
- **Rich** (Terminal Formatting)
- **Jinja2** (HTML Reports)
- **Pytest** (Testing Framework)

## 🚀 Instalación Rápida (< 5 minutos)

```bash
# Clonar el repositorio
git clone https://github.com/robert-salinas/Project-Readiness-Checker.git
cd Project-Readiness-Checker

# Instalar dependencias
pip install -e .
```

## 🛠️ Uso Básico

Para verificar un proyecto utilizando la interfaz visual (Auditorías Asíncronas, KPIs, Botón de Ayuda):

```bash
# Lanzar la aplicación
python main.py
```

### 💻 Línea de Comandos (CLI)

Para verificar un proyecto usando la terminal y reglas estructuradas:

```bash
# Verificación básica en consola
prc check examples/software_project.json

# Generar un reporte HTML
prc check examples/software_project.json --format html --output reporte.html
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
- [Ejemplos Detallados](docs/EXAMPLES.md)
- [Solución de Problemas](docs/TROUBLESHOOTING.md)

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, revisa la [Guía de Contribución](docs/CONTRIBUTING.md) para más detalles sobre cómo empezar.

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Ver el archivo [LICENSE](LICENSE) para más detalles.

---
Desarrollado con ❤️ por [Robert Salinas](https://github.com/robert-salinas)
