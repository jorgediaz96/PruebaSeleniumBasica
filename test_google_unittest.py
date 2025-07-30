import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SauceDemoTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com")
        self.wait = WebDriverWait(self.driver, 10)

    def cerrar_modal_si_aparece(self):
        driver = self.driver
        try:
            modal_close = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "modal_close_button"))  # <-- Reemplaza con clase real si es distinta
            )
            modal_close.click()
            print("Modal cerrado.")
        except:
            print("No apareció ningún modal.")

    def test_checkout_flow(self):
        driver = self.driver
        wait = self.wait

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        self.cerrar_modal_si_aparece()  # <-- Aquí se maneja el modal

        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Jorge")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("110111")
        driver.find_element(By.ID, "continue").click()
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        print("Se hizo clic en 'finish'")

        confirmation = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))).text
        self.assertIn("THANK YOU FOR YOUR ORDER", confirmation.upper())

    def test_checkout_with_item_removal(self):
        driver = self.driver
        wait = self.wait

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        self.cerrar_modal_si_aparece()  # <-- También aquí

        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-test.allthethings()-t-shirt-(red)"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-fleece-jacket"))).click()
        
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        wait.until(EC.element_to_be_clickable((By.ID, "remove-test.allthethings()-t-shirt-(red)"))).click()

        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Jorge")
        driver.find_element(By.ID, "last-name").send_keys("Tester")
        driver.find_element(By.ID, "postal-code").send_keys("110111")
        driver.find_element(By.ID, "continue").click()
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

        confirmation = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))).text
        self.assertIn("THANK YOU FOR YOUR ORDER", confirmation.upper())

    def test_checkout_missing_fields(self):
        driver = self.driver
        wait = self.wait

        # Login
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Agregar un producto al carrito
        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

        # Ir al carrito y hacer checkout
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

        # No llenar los campos -> directamente hacer clic en “Continue”
        driver.find_element(By.ID, "continue").click()

        # Verificar que aparece mensaje de error
        error_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))).text
        self.assertIn("Error: First Name is required", error_message)

    def test_checkout_missing_lastName(self):
        driver = self.driver
        wait = self.wait

        # Login
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Agregar un producto al carrito
        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

        # Ir al carrito y hacer checkout
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

        # No llenar los campos apellido-> directamente hacer clic en “Continue”
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Jorge")
        driver.find_element(By.ID, "continue").click()

        # Verificar que aparece mensaje de error
        error_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container"))).text
        self.assertIn("Error: Last Name is required", error_message)



    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
