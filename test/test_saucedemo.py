import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.driver_factory import get_driver


BASE_URL = "https://www.saucedemo.com/"

# datos para el login
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

    # Espera explícita: login visible
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


def test_login_exitoso_y_validaciones_inventario(driver):
    """
    PRUEBA 1
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
    PRUEBA 2
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


def test_agregar_producto_y_validar_carrito(driver):
    """
    PRUEBA 3
    - Login
    - Agrega primer producto
    - Verifica contador del carrito
    - Navega al carrito
    - Verifica ítem en carrito
    """
    wait = WebDriverWait(driver, 10)
    login(driver)

    # Obtener nombre del primer producto antes de agregar
    first_item_name = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_name"))
    ).text.strip()

    add_first_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item:first-child button.btn_inventory"))
    )
    add_first_btn.click()

    # Verificar badge incrementado
    cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert cart_badge.text.strip() == "1", \
        f"El contador del carrito debería ser 1 y es {cart_badge.text.strip()}"

    # Ir al carrito
    cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
    cart_link.click()

    wait.until(EC.url_contains("/cart.html"))
    assert "/cart.html" in driver.current_url, "No se abrió la página del carrito."

    # Verificar producto añadido
    cart_item_name = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))).text.strip()
    assert cart_item_name == first_item_name, \
        f"Producto en carrito incorrecto. Esperado: {first_item_name} | Obtenido: {cart_item_name}"
