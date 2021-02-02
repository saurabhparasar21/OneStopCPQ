# Import Selenium, Pytest, Webdriver
import pytest
import allure
from allure_commons.types import AttachmentType

from utilities.readProperties import ReadConfig
from utilities.Logger import Logger
from pageObjects.loginPage import loginPage
from pageObjects.HomeTab import HomePage
import time


class Test_001_TestLogin:
    # What data we need to run this test case
    # URL, User Name, Password
    # If these data are common across all TCs then put them in Config.ini file and get them read by properties file
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()

# In each below methods, call conftest method to return driver
# What Scenarios we want to verify:
# We need to capture actions in log file. Create a Logger file under utilities

# Add Markers
#1 Verify Login page opens up, verify login page Title. #Input=URL
    @pytest.mark.RegularPricing
    def test_LoginPageTitle(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_001_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("           TC_001_1:Test Login Page Title")
        self.lgrObj.info("#################################################################")
        self.driver = setup
        self.driver.get(self.baseUrl)
        act_loginPageTitle=self.driver.title
        print("Actual Login Page Title is: "+act_loginPageTitle)
        if act_loginPageTitle == "Login | Salesforce":
            assert True
            self.lgrObj.info("---------- (PASSED): Login page title is passed")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
        else:
            # Capture the screenshots of Failures
            allure.attach(self.driver.get_screenshot_as_png(),name="test_LoginPageTitle",
                          attachment_type=AttachmentType.PNG)
            self.lgrObj.error("---------- (FAILED): Login page title is failed")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
            assert False

    @pytest.mark.RegularPricing
    def test_Login(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_001_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("           TC_001_2: Test Lightning Page Title")
        self.lgrObj.info("#################################################################")
        self.driver = setup
        self.driver.get(self.baseUrl)
        self.lp = loginPage(self.driver)
        self.lp.setUsername(self.UserName)
        self.lp.setPassword(self.Password)
        self.lp.clickLoginButton()
        self.driver.maximize_window()

        # Set up object for Home page object class
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()
        # Verify Home Page Title after logging in
        time.sleep(10)
        act_title=self.driver.title
        self.lgrObj.info("Actual Title is: "+str(act_title))
        if str("Salesforce") in act_title:
            assert True
            self.lgrObj.info("---------- (PASSED): Home Page Title is matched")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
        else:
            allure.attach(self.driver.get_screenshot_as_png(), name="test_Login",
                          attachment_type=AttachmentType.PNG)
            self.lgrObj.error("---------- (FAILED): Home Page Title doesn't match")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
            assert False