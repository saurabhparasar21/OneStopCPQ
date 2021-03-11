import allure
import pytest
# Import Page Objects
from allure_commons.types import AttachmentType

from pageObjects.loginPage import loginPage
from pageObjects.HomeTab import HomePage
from utilities.Logger import Logger
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from pageObjects.CPQAdmin import CPQAdmin
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Make sure Class name contains Test keyword
class Test_CreateProposal:
    # Get Common Values from Configuration file
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Add Marker
    @pytest.mark.RegularPricing
    # Define method to verify Pipeline Creation
    def test_CreatePipeLine(self, setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_019')
        self.driver = setup
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("           TC_019: Test Pipeline Creation     ")
        self.lgrObj.info("#################################################################")
        self.driver.get(self.baseUrl)

        # Set up object for Login page object class
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()

        # Set up object for Home page object class
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        # self.lgrObj.info("Home Page: Search and then select an Opportunity MN-2020 Opportunity")
        hmpageObj.ClickSearchAppsIcon()
        appToSearchFor = XLUtils.readData(self.file, 'TC_019', 3, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        time.sleep(30)
        # click on Pricing tab
        pricingPageObj = CPQAdmin(self.driver)
        pricingPageObj.ClickOnDetailPageTab('Pricing')
        print("Clicked on Pricing tab")


