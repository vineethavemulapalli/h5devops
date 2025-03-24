import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Path to your ChromeDriver (make sure it matches your Chrome version)
        cls.driver = webdriver.Chrome()
        # Replace with your actual URL if different
        cls.driver.get("http://127.0.0.1:5000")
        cls.driver.maximize_window()

    def setUp(self):
        # Before each test, reload the page so we start fresh
        self.driver.get("http://127.0.0.1:5000")

    # 1) Test valid registration: password >= 6 chars, matching
    def test_valid_registration(self):
        driver = self.driver

        driver.find_element(By.ID, "name").send_keys("John Doe")
        driver.find_element(By.ID, "email").send_keys("john@example.com")
        driver.find_element(By.ID, "password").send_keys("123456")
        driver.find_element(By.ID, "confirmPassword").send_keys("123456")
        driver.find_element(By.TAG_NAME, "button").click()

        # Wait for alert
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        # Check that the alert does NOT show the password, only name & email
        self.assertIn("Full Name: John Doe", alert_text)
        self.assertIn("Email: john@example.com", alert_text)
        self.assertNotIn("123456", alert_text)  # Password shouldn't appear

    # 2) Test short password: < 6 chars
    def test_short_password(self):
        driver = self.driver

        driver.find_element(By.ID, "name").send_keys("Jane Smith")
        driver.find_element(By.ID, "email").send_keys("jane@example.com")
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.ID, "confirmPassword").send_keys("123")
        driver.find_element(By.TAG_NAME, "button").click()

        # Expect "Password must be at least 6 characters long."
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        self.assertEqual(alert_text, "Password must be at least 6 characters long.")

    # 3) Test mismatched passwords: same length but different values
    def test_mismatched_passwords(self):
        driver = self.driver

        driver.find_element(By.ID, "name").send_keys("Mike Mismatch")
        driver.find_element(By.ID, "email").send_keys("mike@example.com")
        driver.find_element(By.ID, "password").send_keys("abcdef")
        driver.find_element(By.ID, "confirmPassword").send_keys("abcxyz")
        driver.find_element(By.TAG_NAME, "button").click()

        # Expect "Passwords do not match!"
        alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        self.assertEqual(alert_text, "Passwords do not match!")

    # 4) Test required fields (e.g., empty name)
    def test_empty_name(self):
        driver = self.driver

        # Leave name empty
        driver.find_element(By.ID, "email").send_keys("noname@example.com")
        driver.find_element(By.ID, "password").send_keys("123456")
        driver.find_element(By.ID, "confirmPassword").send_keys("123456")

        # Attempt to submit
        driver.find_element(By.TAG_NAME, "button").click()

        # Because of HTML5 "required" attribute, the browser blocks submission
        # There's no JS alert, so we check that NO alert is present.
        time.sleep(2)  # Wait to see if an alert appears
        try:
            alert = driver.switch_to.alert
            # If alert is present, test fails
            self.fail("Alert appeared unexpectedly: " + alert.text)
        except:
            # No alert means the test passes (browser blocked submission).
            pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
