# 🤝 Contribuyendo a PRC

¡Gracias por tu interés en mejorar el Project Readiness Checker!

## 🛠️ Entorno de Desarrollo

1.  Asegúrate de tener Python 3.8 o superior.
2.  Crea un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  Instala las dependencias de desarrollo:
    ```bash
    pip install -e ".[dev]"
    # Nota: Si no hay sección [dev], instala pytest manualmente:
    pip install pytest
    ```

## 🧪 Pruebas

Antes de enviar cualquier cambio, asegúrate de que todas las pruebas pasen:

```bash
pytest
```

## 📝 Guía de Estilo

- Seguimos **PEP 8** para el código Python.
- Las nuevas reglas deben ser documentadas en el README.
- Cada nueva funcionalidad debe venir acompañada de sus respectivos tests.

## 🚀 Proceso de Pull Request

1.  Crea una rama para tu funcionalidad (`git checkout -b feat/nueva-regla`).
2.  Haz tus cambios y asegúrate de que los tests pasen.
3.  Haz commit de tus cambios con mensajes descriptivos.
4.  Envía el PR para revisión.

---

Diseñado con ❤️ para la comunidad de ingeniería.
