from telnetlib import EC

import pytest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.AttributePage import AttributePage
from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.ConstRulePrompt import ConstRulePrompt
from pageObjects.HomeTab import HomePage
from pageObjects.OptionPage import OptionPage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.loginPage import loginPage
from pageObjects.AttributeOptionPage import AttributeOptionPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger


class Test_DirectConfiguration_CurrencyCheck:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Step:04 Set-up Test Scenario. Pass the driver through...
    @pytest.mark.RegularPricing
    def test_Currency_In_DirectConfiguration(self,setup):
        self.lgrObj = Logger.logGen('TC_021_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_021_1: Currency Code check in Direct Configuration          ")
        self.lgrObj.info("#####################################################################")

        self.driver = setup
        self.lgrObj.info("---------- Login to the application")
        # Set up Object for Login Page Object # Set User Name, Password
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()

        # Switch to Lightning
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file,'TC_021', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_021', 1, 3)
        value = XLUtils.readData(self.file, 'TC_021', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_021', 1, 4)
        value = XLUtils.readData(self.file, 'TC_021', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_021', 1, 5)
        value = XLUtils.readData(self.file, 'TC_021', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_021', 1, 6)
        value = XLUtils.readData(self.file, 'TC_021', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_021', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.ConfigureProduct("Configure",PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1= XLUtils.readData(self.file, 'TC_021', 2, 8)


        # Select the Option Product
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)

        # Wait for Pricing to Complete
        OptnPgObj.OptnPageWaitForPricingToComplete()
        OptnPgObj.ClickOnButton("GoToPricing")
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        # Save or Finalize the Cart
        time.sleep(5)
        CartPgObj.ClickCartMenuButton('Save')

        # Configure with the Direct button
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (DirectConfig)')
        time.sleep(8)

        # Verify whether price is shown with the correct currency
        OptnPgObj.SwitchToFrame()
        AtrOptnPgObj.ClickOnTab('Product Options')

        Matched=OptnPgObj.VerifyPriceinSummarySection('Standard Price','GBP 110')
        if Matched == "True":
            self.lgrObj.info("---------- (PASSED): Price for Standard Price is shown in GBP")
        else:
            self.lgrObj.info("---------- (FAILED): Price for Standard Price is shown in GBP")

        OptnPgObj.VerifyPriceinSummarySection('License Fee', 'GBP 220')
        if Matched == "True":
            self.lgrObj.info("---------- (PASSED): Price for License Fee is shown in GBP")
        else:
            self.lgrObj.info("---------- (FAILED): Price for License Fee is shown in GBP")

        OptnPgObj.VerifyPriceinSummarySection('Net Price', 'GBP 330')
        if Matched == "True":
            self.lgrObj.info("---------- (PASSED): Price for Net Price is shown in GBP")
        else:
            self.lgrObj.info("---------- (FAILED): Price for Net Price is shown in GBP")

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()





