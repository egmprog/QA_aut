# Automatización Saucedemo con Selenium + Pytest

## Propósito del proyecto
Automatizar flujos básicos de navegación web en https://www.saucedemo.com con Selenium WebDriver y Python, validando login, inventario y carrito de compras.

## Tecnologías utilizadas
- Python 3.8+
- Selenium WebDriver
- Pytest
- Pytest-HTML
- WebDriver Manager (ChromeDriver automático)

## Estructura
```text
pre-entrega-final/
├── drivers/
│   └── chromedriver.exe
├── reports/
├── test/
│   └── test_saucedemo.py
├── utils/
│   └── driver_factory.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Instalación
1. Crear y activar entorno virtual (opcional):
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de pruebas
Desde la carpeta raíz `QA_aut`:

```bash
pytest test/test_saucedemo.py -v
```

## Reporte HTML
Generar reporte en HTML:

```bash
pytest test/test_saucedemo.py -v --html=reports/reporte.html
```

> Si querés exactamente el comando solicitado:
```bash
pytest QA_aut/test_saucedemo.py -v --html=reporte.html
```