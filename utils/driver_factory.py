from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

def get_driver(headless=False):
    
    #Crea una instancia de ChromeDriver    
    # WebDriver: Instancia del driver de Chrome
    
    options = webdriver.ChromeOptions()
    
    if headless:
        options.add_argument("--headless")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    
    driver_path = os.path.join(
        os.path.dirname(__file__),
        "../drivers/chromedriver.exe"
    )
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver
