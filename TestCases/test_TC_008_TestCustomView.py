from selenium.webdriver import ActionChains

from utilities.Logger import Logger
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from pageObjects.loginPage import loginPage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.CustomCartView import CustomCartView
from pageObjects.HomeTab import HomePage
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

class TestCustomCartView:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    @pytest.mark.RegularPricing
    def test_CustomCartView_Classic(self, setup):
        self.lgrObj = Logger.logGen('TC_008_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_008_1: Custom Cart View (Regular Cart Normal Pricing      ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
        self.driver = setup
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        self.lgrObj.info("---------- Switch to Lightning if not set")
        self.HomePageObj = HomePage(self.driver)
        self.HomePageObj.switchToLightning()

        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_008', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_008', 1, 3)
        value = XLUtils.readData(self.file, 'TC_008', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_008', 1, 4)
        value = XLUtils.readData(self.file, 'TC_008', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_008', 1, 5)
        value = XLUtils.readData(self.file, 'TC_008', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_008', 1, 6)
        value = XLUtils.readData(self.file, 'TC_008', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to the Cart")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_008', 2, 8)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(3)

        self.lgrObj.info("---------- Create a new Custom View")
        CustViwObj=CustomCartView(self.driver)
        CustViwObj.CreateCustomCartView('Is Optional','MN-2020 Is Optional View 1')

        self.lgrObj.info("---------- Check the Group Name")
        path="//div[@class='block-productname']//a//span"
        GrpEle=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ActualGrpName=GrpEle.get_attribute("title")
        print("Actual Group name is: "+str(ActualGrpName))
        if ActualGrpName == str("false (1)"):
            assert True
            self.lgrObj.info("---------- (PASSED) Custom Cart View Group is Correct")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED) Custom Cart View Group is NOT Correct")
            self.driver.close()

        self.lgrObj.info("---------- Expand the Group and set Is Optional Checkbox")
        ExpandIcon="//div[@class='block-productname']//a"
        ExpandIconEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ExpandIcon)))
        ExpandIconEle.click()
        time.sleep(3)
        # print("Click on Is Optional Checkbox")
        CartPgObj.ClickIsOptionalForLineItem('MN - 2020 Standalone 1')
        CartPgObj.WaitForPricingProgressBarToFinish()

        CustViwObj.SelectCustomCartView('MN-2020 Is Optional View 1')
        time.sleep(3)
        self.lgrObj.info("---------- Check the Group Name")
        path = "//div[@class='block-productname']//a//span"
        GrpEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ActualGrpName = GrpEle.get_attribute("title")
        print("Actual Group name is: " + str(ActualGrpName))
        if ActualGrpName == str("true (1)"):
            assert True
            self.lgrObj.info("---------- (PASSED) Custom Cart View Group Name is updated correctly")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED) Custom Cart View Group Name is NOT updated correctly")
            self.driver.close()
        self.lgrObj.info("---------- Delete the View")
        CustViwObj.EditDeleteCustomCartView('MN-2020 Is Optional View 1','Delete View')

        self.lgrObj.info("---------- Abandon the Cart and delete the proposal")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.TurboPricing
    def test_CustomCartView_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_008_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_008_2: Custom Cart View (Regular Cart Turbo Pricing)      ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
        self.driver = setup
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        self.lgrObj.info("---------- Switch to Lightning if not set")
        self.HomePageObj = HomePage(self.driver)
        self.HomePageObj.switchToLightning()

        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_008', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_008', 1, 3)
        value = XLUtils.readData(self.file, 'TC_008', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_008', 1, 4)
        value = XLUtils.readData(self.file, 'TC_008', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_008', 1, 5)
        value = XLUtils.readData(self.file, 'TC_008', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_008', 1, 6)
        value = XLUtils.readData(self.file, 'TC_008', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to the Cart")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_008', 2, 8)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(3)

        self.lgrObj.info("---------- Create a new Custom View")
        CustViwObj = CustomCartView(self.driver)
        CustViwObj.CreateCustomCartView('Is Optional', 'MN-2020 Is Optional View 2')

        self.lgrObj.info("---------- Check the Group Name")
        path = "//div[@class='block-productname']//a//span"
        GrpEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ActualGrpName = GrpEle.get_attribute("title")
        print("Actual Group name is: " + str(ActualGrpName))
        if ActualGrpName == str("false (1)"):
            assert True
            self.lgrObj.info("---------- (PASSED) Custom Cart View Group is Correct")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED) Custom Cart View Group is NOT Correct")
            self.driver.close()

        self.lgrObj.info("---------- Expand the Group and set Is Optional Checkbox")
        ExpandIcon = "//div[@class='block-productname']//a"
        ExpandIconEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ExpandIcon)))
        ExpandIconEle.click()
        time.sleep(3)
        # print("Click on Is Optional Checkbox")
        CartPgObj.ClickIsOptionalForLineItem('MN - 2020 Standalone 1')
        CartPgObj.WaitForPricingProgressBarToFinish()

        CustViwObj.SelectCustomCartView('MN-2020 Is Optional View 2')
        time.sleep(3)
        self.lgrObj.info("---------- Check the Group Name")
        path = "//div[@class='block-productname']//a//span"
        GrpEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ActualGrpName = GrpEle.get_attribute("title")
        print("Actual Group name is: " + str(ActualGrpName))
        if ActualGrpName == str("true (1)"):
            assert True
            self.lgrObj.info("---------- (PASSED) Custom Cart View Group Name is updated correctly")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED) Custom Cart View Group Name is NOT updated correctly")
            self.driver.close()
        self.lgrObj.info("---------- Delete the View")
        CustViwObj.EditDeleteCustomCartView('MN-2020 Is Optional View 2', 'Delete View')

        self.lgrObj.info("---------- Abandon the Cart and delete the proposal")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.Split
    def test_CustomCartView_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_008_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_008_3: Custom Cart View Split Cart Async Pricing          ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
        self.driver = setup
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        self.lgrObj.info("---------- Switch to Lightning if not set")
        self.HomePageObj = HomePage(self.driver)
        self.HomePageObj.switchToLightning()

        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_008', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile', 'Split')
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_008', 1, 3)
        value = XLUtils.readData(self.file, 'TC_008', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_008', 1, 4)
        value = XLUtils.readData(self.file, 'TC_008', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_008', 1, 5)
        value = XLUtils.readData(self.file, 'TC_008', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_008', 1, 6)
        value = XLUtils.readData(self.file, 'TC_008', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to the Cart")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_008', 2, 8)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName)

        # Click on Mini-Cart & then View Cart button
        CtlgPgObj.ClickCatalogPageButton('mini-cart')
        CtlgPgObj.ClickCatalogPageButton('view-cart')
        self.lgrObj.info("---------- Go to Shopping Cart")

        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Create a new Custom View")
        CustViwObj = CustomCartView(self.driver)
        CustViwObj.CreateCustomCartView('Is Optional', 'MN-2020 Is Optional View 3')

        self.lgrObj.info("---------- Check the Group Name")
        path = "//div[@class='block-productname']//a//span"
        GrpEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ActualGrpName = GrpEle.get_attribute("title")
        print("Actual Group name is: " + str(ActualGrpName))
        if ActualGrpName == str("false (1)"):
            assert True
            self.lgrObj.info("---------- (PASSED) Custom Cart View Group is Correct")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED) Custom Cart View Group is NOT Correct")
            self.driver.close()

        self.lgrObj.info("---------- Expand the Group and set Is Optional Checkbox")
        ExpandIcon = "//div[@class='block-productname']//a"
        ExpandIconEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ExpandIcon)))
        ExpandIconEle.click()
        time.sleep(3)
        # print("Click on Is Optional Checkbox")
        CartPgObj.ClickIsOptionalForLineItem('MN - 2020 Standalone 1')
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        CustViwObj.SelectCustomCartView('MN-2020 Is Optional View 3')
        time.sleep(3)
        self.lgrObj.info("---------- Check the Group Name")
        path = "//div[@class='block-productname']//a//span"
        GrpEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ActualGrpName = GrpEle.get_attribute("title")
        print("Actual Group name is: " + str(ActualGrpName))
        if ActualGrpName == str("true (1)"):
            assert True
            self.lgrObj.info("---------- (PASSED) Custom Cart View Group Name is updated correctly")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED) Custom Cart View Group Name is NOT updated correctly")
            self.driver.close()
        self.lgrObj.info("---------- Delete the View")
        CustViwObj.EditDeleteCustomCartView('MN-2020 Is Optional View 3', 'Delete View')

        self.lgrObj.info("---------- Abandon the Cart and delete the proposal")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")