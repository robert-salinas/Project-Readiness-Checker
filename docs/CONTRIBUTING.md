# 🤝 Contribuyendo a PRC

¡Gracias por tu interés en mejorar el Project Readiness Checker!

## 🛠️ Entorno de Desarrollo

1.  Asegúrate de tener Python 3.11 o superior.
2.  Crea un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  Instala las dependencias de desarrollo:
    ```bash
    pip install -e ".[dev]"
    ```

## 🧪 Pruebas

Antes de enviar cualquier cambio, asegúrate de que todas las pruebas pasen:

```bash
pytest
```

## 📜 Código de Conducta

Al participar en este proyecto, te comprometes a seguir nuestro [Código de Conducta](../CODE_OF_CONDUCT.md).

## 📝 Guía de Estilo

- Seguimos **PEP 8** para el código Python.
- Usamos Type Hints en todas las funciones nuevas.
- Cada nueva funcionalidad debe venir acompañada de sus respectivos tests.

## 🚀 Proceso de Pull Request

1.  Crea una rama para tu funcionalidad (`git checkout -b feat/nueva-regla`).
2.  Haz tus cambios y asegúrate de que los tests pasen.
3.  Haz commit de tus cambios con mensajes descriptivos.
4.  Envía el PR al [repositorio principal](https://github.com/robert-salinas/Project-Readiness-Checker).

---

Diseñado con ❤️ por la comunidad de ingeniería.
