# 🛠️ Solución de Problemas

Aquí encontrarás soluciones a los problemas más comunes al usar **PRC**.

## 1. Error: `ModuleNotFoundError: No module named 'src'`

Este error ocurre cuando intentas ejecutar el script directamente sin instalar el paquete o configurar el `PYTHONPATH`.

**Solución:**
- Instala el paquete en modo editable: `pip install -e .`
- O configura el PYTHONPATH: `$env:PYTHONPATH="."` (Windows) o `export PYTHONPATH=$PYTHONPATH:.` (Linux/Mac)

## 2. Error: `pydantic.error_wrappers.ValidationError`

Tu archivo de configuración no cumple con el esquema esperado.

**Solución:**
- Asegúrate de que todos los campos obligatorios (`name`, `type`, `target`) estén presentes en cada regla.
- Verifica que los tipos de reglas sean válidos (`file_exists`, `dir_exists`, `file_contains`, `command_success`, `env_var_set`).

## 3. El comando `command_success` falla inesperadamente

El comando se ejecuta en el shell actual.

**Solución:**
- Asegúrate de que el comando sea válido en tu sistema operativo.
- Verifica que los ejecutables estén en tu `PATH`.

## 4. El reporte HTML no se genera

El formato HTML requiere obligatoriamente un archivo de salida.

**Solución:**
- Usa el flag `--output` o `-o`: `prc check config.json --format html --output reporte.html`
