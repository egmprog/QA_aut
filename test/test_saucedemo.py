import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_factory import get_driver

# información para el test
BASE_URL = "https://www.saucedemo.com/"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


@pytest.fixture
def driver():
    driver = get_driver(headless=False)
    yield driver
    driver.quit()


def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    # Espera explícita: que se vea el login
    username_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

    username_input.clear()
    username_input.send_keys(VALID_USER)
    password_input.clear()
    password_input.send_keys(VALID_PASS)
    login_button.click()

    # Validación de redirección y elementos clave
    wait.until(EC.url_contains("/inventory.html"))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))

    assert "/inventory.html" in driver.current_url, \
        f"No redirigió a inventario. URL actual: {driver.current_url}"

    app_logo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "app_logo")))
    products_title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))

    assert "Swag Labs" in app_logo.text, "No aparece el texto 'Swag Labs'."
    assert products_title.text.strip() == "Products", \
        f"Se esperaba 'Products' y se obtuvo '{products_title.text.strip()}'"

# despues de login, validar elementos clave de la página de inventario
def test_login_exitoso_y_validaciones_inventario(driver):
    """
    - Navegar a login
    - Ingresar credenciales válidas
    - Validar login exitoso: URL /inventory.html + Products/Swag Labs
    - Verificar elementos clave: título, menú, filtro y productos visibles
    """
    wait = WebDriverWait(driver, 10)
    login(driver)

    # Validar título de página de inventario
    inventory_title = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))
    assert inventory_title.text.strip() == "Products", \
        f"Título incorrecto. Esperado: Products | Obtenido: {inventory_title.text.strip()}"

    # Validar elementos importantes de UI
    menu_button = wait.until(EC.visibility_of_element_located((By.ID, "react-burger-menu-btn")))
    sort_filter = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product_sort_container")))
    assert menu_button.is_displayed(), "El menú no está visible."
    assert sort_filter.is_displayed(), "El filtro no está visible."

    # Validar presencia de productos (al menos uno)
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
    assert len(products) > 0, "No se encontraron productos en el inventario."

def test_listar_primer_producto_nombre_precio(driver):
    """
    - Login
    - Valida presencia de productos
    - Lista nombre/precio del primero
    """
    wait = WebDriverWait(driver, 10)
    login(driver)

    first_item_name = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_name"))
    )
    first_item_price = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_price"))
    )

    assert first_item_name.text.strip() != "", "El nombre del primer producto está vacío."
    assert first_item_price.text.strip().startswith("$"), \
        f"Precio inválido del primer producto: {first_item_price.text.strip()}"

    print(f"\nPrimer producto: {first_item_name.text.strip()} | Precio: {first_item_price.text.strip()}")

