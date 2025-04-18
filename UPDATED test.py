import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    def setUp(self):
        # Handle any alert that might be present before loading the page
        try:
            alert = self.driver.switch_to.alert
            alert.accept()  # Close the alert if it's present
        except:
            pass  # If no alert appears, continue with the test

        # Now, load the page
        self.driver.get("http://127.0.0.1:5000")
        
    def test_valid_registration(self):
        self.driver.find_element(By.ID, "name").send_keys("John Doe")
        self.driver.find_element(By.ID, "email").send_keys("john@example.com")
        self.driver.find_element(By.ID, "password").send_keys("123456")
        self.driver.find_element(By.ID, "confirmPassword").send_keys("123456")
        self.driver.find_element(By.TAG_NAME, "button").click()
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()
        self.assertIn("Full Name: John Doe", alert_text)
        self.assertIn("Email: john@example.com", alert_text)
        self.assertNotIn("123456", alert_text)

    def test_short_password(self):
        self.driver.find_element(By.ID, "name").send_keys("Jane Smith")
        self.driver.find_element(By.ID, "email").send_keys("jane@example.com")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.ID, "confirmPassword").send_keys("123")
        self.driver.find_element(By.TAG_NAME, "button").click()
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
        self.assertEqual(alert.text, "Password must be at least 6 characters long.")

    def test_mismatched_passwords(self):
        self.driver.find_element(By.ID, "name").send_keys("Mike Mismatch")
        self.driver.find_element(By.ID, "email").send_keys("mike@example.com")
        self.driver.find_element(By.ID, "password").send_keys("abcdef")
        self.driver.find_element(By.ID, "confirmPassword").send_keys("abcxyz")
        self.driver.find_element(By.TAG_NAME, "button").click()
        alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
        self.assertEqual(alert.text, "Passwords do not match!")

    def test_empty_name(self):
        self.driver.find_element(By.ID, "email").send_keys("noname@example.com")
        self.driver.find_element(By.ID, "password").send_keys("123456")
        self.driver.find_element(By.ID, "confirmPassword").send_keys("123456")
        self.driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        try:
            alert = self.driver.switch_to.alert
            self.fail("Alert appeared unexpectedly: " + alert.text)
        except:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()

