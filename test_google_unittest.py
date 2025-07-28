import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class GoogleSearchTest(unittest.TestCase):

    def setUp(self):
        # Configura el navegador (se ejecuta antes de cada prueba)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def test_search_openai(self):
        driver = self.driver
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

        # Validar que el título contiene "OpenAI"
        self.assertIn("OpenAI", driver.title)



    def test_search_selenium(self):
        driver = self.driver
        driver.get("https://www.google.com")
        time.sleep(2)

        try:
            driver.find_element(By.ID, "L2AGLb").click()
        except:
            pass

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        self.assertIn("Selenium", driver.title)
        print("✅ Prueba Selenium exitosa.")

    def tearDown(self):
        # Cierra el navegador (se ejecuta después de cada prueba)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
