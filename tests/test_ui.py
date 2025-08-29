"""
UI Tests for Sauce Demo
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class TestLogin:
    """Simple pytest version of the BDD login tests"""
    
    @pytest.fixture(scope="function")  # Changed from "class" to "function" for test isolation
    def driver(self):
        """Setup Chrome driver with webdriver-manager"""
        # Chrome options for better CI compatibility and test isolation
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode for CI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Test isolation options
        chrome_options.add_argument("--incognito")  # Fresh browser session
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # Enhanced logging suppression:
        chrome_options.add_argument("--log-level=3")  # Only show fatal errors
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-voice-transcription")
        chrome_options.add_argument("--disable-speech-api")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Suppress all output
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        
        # Cleanup: Clear all cookies and local storage before closing
        try:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
        except:
            pass  # Ignore cleanup errors
        driver.quit()
    
    def test_valid_login(self, driver):
        """Test successful login with valid credentials"""
        # Navigate to login page
        driver.get("https://www.saucedemo.com/")
        
        # Enter credentials - Using data-test attributes for stability
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        
        # Click login
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Verify success
        assert "inventory.html" in driver.current_url
        assert driver.find_element(By.CLASS_NAME, "inventory_list").is_displayed()
    
    def test_invalid_login(self, driver):
        """Test login failure with invalid credentials"""
        driver.get("https://www.saucedemo.com/")
        
        # Enter credentials - Using data-test attributes for stability
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("wrong_password")
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Verify specific error message using data-test attribute
        error_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        )
        assert "Epic sadface: Username and password do not match any user in this service" in error_element.text
    
    def test_locked_out_user(self, driver):
        """Test login failure with locked out user"""
        driver.get("https://www.saucedemo.com/")
        
        # Enter credentials - Using data-test attributes for stability
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        
        username_field.send_keys("locked_out_user")
        password_field.send_keys("secret_sauce")
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Verify specific locked out error message using data-test attribute
        error_element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']"))
        )
        assert "Epic sadface: Sorry, this user has been locked out." in error_element.text
    
    def test_logout(self, driver):
        """Test user logout functionality"""
        # First login
        driver.get("https://www.saucedemo.com/")
        
        # Enter credentials - Using data-test attributes for stability
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Wait for successful login - wait for inventory page to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        
        # Verify we're logged in
        assert "inventory.html" in driver.current_url
        
        # Open menu and logout - Using BDD reference selectors
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        menu_button.click()
        
        # Wait for menu to open and find logout link using ID like BDD reference
        logout_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        
        # Add extra wait to ensure menu is fully opened
        time.sleep(1)
        
        # Use JavaScript click as backup in case regular click doesn't work
        try:
            logout_link.click()
        except:
            # Fallback to JavaScript click
            driver.execute_script("arguments[0].click();", logout_link)
        
        # Wait longer for logout to process
        time.sleep(3)
        
        # Debug: Print current URL to see where we are
        print(f"\nCurrent URL after logout: {driver.current_url}")
        print(f"Page title: {driver.title}")
        
        # Check if we're back at login page
        if "inventory.html" in driver.current_url:
            # Still on inventory page - logout didn't work
            assert False, f"Logout failed - still on inventory page: {driver.current_url}"
        
        # Verify logout success - should be back at login page  
        assert driver.current_url == "https://www.saucedemo.com/", f"Expected login page, got: {driver.current_url}"
        
        # Verify that we can see the login form elements
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        assert username_field.is_displayed(), "Username field should be visible after logout"
        assert password_field.is_displayed(), "Password field should be visible after logout"
    
    @pytest.mark.xfail(reason="Expected failure - performance_glitch_user intentionally triggers slow loads to demonstrate performance monitoring")
    def test_page_load_performance(self, driver):
        """Test that product page loads in under 2 seconds.
        
        NOTE: This test is EXPECTED to fail with 'performance_glitch_user' 
        because this demo user intentionally triggers slow page loads to 
        demonstrate performance testing capabilities. The test failure 
        indicates that our performance monitoring is working correctly.
        
        In a real application, this would catch actual performance regressions.
        """
        driver.get("https://www.saucedemo.com/")
        
        # Enter credentials - Using data-test attributes for stability
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        
        username_field.send_keys("performance_glitch_user")
        password_field.send_keys("secret_sauce")
        
        # Start timing
        start_time = time.time()
        
        # Click login
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Wait for inventory page to load - Using ID like BDD reference
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "inventory_container"))
        )
        
        # Calculate load time
        end_time = time.time()
        load_time = end_time - start_time
        
        # Performance assertion (allow some tolerance for CI)
        assert load_time < 2.0, f"Page load took {load_time:.2f} seconds, expected under 2 seconds"
        
        # Log the actual performance for monitoring
        print(f"\nPage load performance: {load_time:.2f} seconds")


class TestInventory:
    """Additional inventory page tests"""
    
    @pytest.fixture(scope="function")  # Changed from "class" to "function" for test isolation
    def logged_in_driver(self):
        """Setup driver and login for inventory tests"""
        # Chrome options for better CI compatibility and test isolation
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Test isolation options
        chrome_options.add_argument("--incognito")  # Fresh browser session
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        # Login - Using data-test attributes for stability
        driver.get("https://www.saucedemo.com/")
        username_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"username\"]")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[data-test=\"password\"]")
        
        username_field.send_keys("standard_user")
        password_field.send_keys("secret_sauce")
        
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        
        # Wait for inventory page to load
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "inventory_container"))
        )
        
        yield driver
        
        # Cleanup: Clear all cookies and local storage before closing
        try:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
        except:
            pass  # Ignore cleanup errors
        driver.quit()
    
    def test_inventory_items_displayed(self, logged_in_driver):
        """Test that inventory items are displayed after login"""
        # Should already be on inventory page from fixture
        assert "https://www.saucedemo.com/inventory.html" in logged_in_driver.current_url
        
        # Check that inventory items are displayed - Using class selectors
        inventory_items = logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(inventory_items) > 0, "No inventory items displayed"
        
        # Verify at least one item has a name and price
        first_item = inventory_items[0]
        item_name = first_item.find_element(By.CLASS_NAME, "inventory_item_name")
        item_price = first_item.find_element(By.CLASS_NAME, "inventory_item_price")
        
        assert item_name.text, "Item name is empty"
        assert item_price.text, "Item price is empty"
