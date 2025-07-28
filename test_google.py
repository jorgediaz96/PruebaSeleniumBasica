from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar el driver automáticamente
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abrir Google
driver.get("https://www.google.com")
time.sleep(2)

# Aceptar cookies si aparecen
try:
    driver.find_element(By.ID, "L2AGLb").click()
except:
    pass

# Buscar "OpenAI"
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("OpenAI")
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# Validar que el título contenga "OpenAI"
assert "OpenAI" in driver.title
print("✅ Prueba exitosa: 'OpenAI' está en el título.")

# Cerrar navegador
driver.quit()
