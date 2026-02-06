# 🏗️ Arquitectura y Decisiones de Diseño

Este documento describe las decisiones técnicas y la estructura del **Project Readiness Checker**.

## 🎯 Objetivos del Diseño

1.  **Extensibilidad:** Permitir agregar nuevos tipos de validaciones sin modificar el núcleo del motor.
2.  **Desacoplamiento:** Separar la lógica de validación de la lógica de presentación (formateadores).
3.  **Portabilidad:** Funcionar en diferentes sistemas operativos (Windows, Linux, macOS) gracias a Python.
4.  **Facilidad de Uso:** Configuración simple basada en YAML/JSON que no requiere conocimientos de programación.

## 🧱 Componentes Principales

### 1. Modelos de Datos (`src/models.py`)
Utilizamos **Pydantic** para definir los esquemas de configuración y reportes. Esto garantiza que cualquier error en el archivo de configuración sea detectado inmediatamente al cargar el programa.

### 2. Motor de Reglas (`src/checkers/engine.py`)
El `CheckerEngine` es el corazón del sistema. Itera sobre las reglas definidas y utiliza la lógica adecuada según el `RuleType`. Se ha diseñado para ser fácilmente extendible mediante el patrón de estrategia o simplemente agregando nuevos evaluadores en el método `_evaluate_rule`.

### 3. Sistema de Formateo (`src/formatters/`)
Implementamos una clase base abstracta `Formatter` para asegurar que todos los formatos de salida sigan el mismo contrato.
- **CLIFormatter:** Utiliza la librería `rich` para crear tablas y paneles estéticos en la terminal.
- **JSONFormatter:** Facilita la integración con pipelines de CI/CD.
- **HTMLFormatter:** Utiliza `Jinja2` para generar reportes visuales que pueden ser compartidos fácilmente.

### 4. CLI (`src/cli.py`)
Construido con `Typer` para una experiencia de usuario moderna, con ayuda integrada y manejo de argumentos intuitivo.

## 🛠️ Stack Tecnológico

- **Python 3.8+**: Lenguaje base.
- **Typer**: Interfaz de línea de comandos.
- **Pydantic**: Validación de datos.
- **Rich**: Formateo de texto en consola.
- **Jinja2**: Motor de plantillas para reportes HTML.
- **Pytest**: Framework de pruebas unitarias.

## 📑 ADRs (Architecture Decision Records)

### ADR 001: Uso de Pydantic para Validación de Configuración
- **Estado:** Aceptado
- **Contexto:** Necesitábamos una forma robusta de validar archivos YAML/JSON de entrada.
- **Decisión:** Usar Pydantic v2 por su rendimiento y facilidad para definir esquemas complejos.
- **Consecuencias:** Validación inmediata en tiempo de carga, mensajes de error claros para el usuario.

### ADR 002: Desacoplamiento de Formateadores
- **Estado:** Aceptado
- **Contexto:** El usuario puede querer el reporte en diferentes formatos (Terminal, Web, CI/CD).
- **Decisión:** Implementar el patrón Strategy con una clase base abstracta `Formatter`.
- **Consecuencias:** Fácil de añadir nuevos formatos (ej. Markdown, PDF) sin tocar el motor de reglas.

### ADR 003: Typer para la Interfaz de Usuario
- **Estado:** Aceptado
- **Contexto:** Queremos una CLI intuitiva y con autocompletado.
- **Decisión:** Usar Typer debido a su integración con Type Hints de Python.
- **Consecuencias:** Código de la CLI más limpio y generación automática de ayuda (`--help`).

## 📈 Evolución Futura

- Soporte para reglas personalizadas mediante scripts de Python externos.
- Integración nativa con GitHub Actions.
- Más validadores (ej. tamaño de archivo, permisos, hashes de archivos).
