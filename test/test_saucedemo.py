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


