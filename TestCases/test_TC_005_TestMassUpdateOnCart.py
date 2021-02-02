import pytest
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger
from utilities import XLUtils
from pageObjects.loginPage import loginPage
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.CartPage import CartPage
from pageObjects.MassUpdate import MassUpdate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


    # Step:01 Create a Test class
class Test_CartMassUpdate:
    # Step:02 Read Common Variables from Configuration file
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    #Step:04 Set-up Test Scenario. Pass the driver through
    @pytest.mark.RegularPricing
    def test_MassUpdateAction_Classic(self,setup):
        # Step:03 Set up Logger Object
        self.lgrObj = Logger.logGen('TC_005_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("TC_005_1: Cart - Mass Update Action (Regular Cart - Normal Pricing)")
        self.lgrObj.info("#################################################################")
        self.driver=setup

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_005', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_005', 1, 3)
        value = XLUtils.readData(self.file, 'TC_005', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_005', 1, 4)
        value = XLUtils.readData(self.file, 'TC_005', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_005', 1, 5)
        value = XLUtils.readData(self.file, 'TC_005', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_005', 1, 6)
        value = XLUtils.readData(self.file, 'TC_005', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add five Products to Cart")
        PrdName1 = XLUtils.readData(self.file, 'TC_005', 2, 8)
        PrdName2 = XLUtils.readData(self.file, 'TC_005', 3, 8)
        PrdName3 = XLUtils.readData(self.file, 'TC_005', 4, 8)
        PrdName4 = XLUtils.readData(self.file, 'TC_005', 5, 8)
        PrdName5 = XLUtils.readData(self.file, 'TC_005', 6, 8)

        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName1)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName2)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName3)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName4)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName5)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        time.sleep(5)
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Mass Update Action")
        grandTotBefMassUpdate=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotBefMassUpdate=grandTotBefMassUpdate[4:]
        NoOfRowsBeforeMassUpdate = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- No of rows before mass update: "+str(NoOfRowsBeforeMassUpdate))
        self.lgrObj.info("---------- Grand Total before mass update: "+str(SlicedGrandTotBefMassUpdate))

        self.lgrObj.info("---------- Select all check boxes and then Click on Mass Update action")
        CartPgObj.ClickSelectAllCheckBox()
        CartPgObj.ClickMassAction('Mass Update')

        self.lgrObj.info("---------- Set Quantity, Adjustments in Mass Update Pop-up")
        massUpdObj=MassUpdate(self.driver)
        massUpdObj.SetMassUpdateField('Set','Quantity','5')
        massUpdObj.SetMassUpdateField('Set','Adjustment Type','% Discount')
        massUpdObj.SetMassUpdateField('Set', 'Adjustment Amount', '10')
        massUpdObj.ClickButton('Apply')

        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Capture Grand Total and No. of line items After Mass Update Action")
        grandTotalAfterMassUpdate = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterMassUpdate = grandTotalAfterMassUpdate[4:]
        self.lgrObj.info("---------- Grand Total after Mass Update: "+str(SlicedGrandTotalAfterMassUpdate))

        expctGrandTotal=XLUtils.readData(self.file, 'TC_005', 2, 9)
        print(expctGrandTotal)
        print("Expected Grand Total is: "+str(expctGrandTotal))
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterMassUpdate):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after Mass Update action is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_005.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after Mass Update action is NOT correct ------")
            self.driver.close()

        #Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.Split
    def test_MassUpdateAction_Split(self,setup):
        # Step:03 Set up Logger Object
        self.lgrObj = Logger.logGen('TC_005_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info(" TC_005_2: Cart - Mass Update Action Split Cart Async Pricing    ")
        self.lgrObj.info("#################################################################")

        self.driver=setup
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_005', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile', 'Split')
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_005', 1, 3)
        value = XLUtils.readData(self.file, 'TC_005', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_005', 1, 4)
        value = XLUtils.readData(self.file, 'TC_005', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_005', 1, 5)
        value = XLUtils.readData(self.file, 'TC_005', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_005', 1, 6)
        value = XLUtils.readData(self.file, 'TC_005', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add 5 Products to Cart")
        PrdName1 = XLUtils.readData(self.file, 'TC_005', 2, 8)
        PrdName2 = XLUtils.readData(self.file, 'TC_005', 3, 8)
        PrdName3 = XLUtils.readData(self.file, 'TC_005', 4, 8)
        PrdName4 = XLUtils.readData(self.file, 'TC_005', 5, 8)
        PrdName5 = XLUtils.readData(self.file, 'TC_005', 6, 8)

        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName1)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName2)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName3)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName4)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName5)

        self.lgrObj.info("---------- Click on Mini-Cart & then View Cart button")
        CtlgPgObj.ClickCatalogPageButton('mini-cart')
        CtlgPgObj.ClickCatalogPageButton('view-cart')
        time.sleep(3)

        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Mass Update Action")
        grandTotBefMassUpdate=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotBefMassUpdate=grandTotBefMassUpdate[4:]
        NoOfRowsBeforeMassUpdate = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- No of rows before mass update: "+str(NoOfRowsBeforeMassUpdate))
        self.lgrObj.info("---------- Grand Total before mass update: "+str(SlicedGrandTotBefMassUpdate))

        self.lgrObj.info("---------- Select all check boxes and then Click on Mass Update action")
        time.sleep(3)
        CartPgObj.ClickSelectAllCheckBox()
        CartPgObj.ClickMassAction('Mass Update')

        self.lgrObj.info("---------- Set Quantity, Adjustments in Mass Update Pop-up")
        massUpdObj=MassUpdate(self.driver)
        massUpdObj.SetMassUpdateField('Set','Quantity','5')
        massUpdObj.SetMassUpdateField('Set','Adjustment Type','% Discount')
        massUpdObj.SetMassUpdateField('Set', 'Adjustment Amount', '10')
        massUpdObj.ClickButton('Apply')


        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(6)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)

        self.lgrObj.info("---------- Capture Grand Total and No. of line items After Mass Update Action")
        grandTotalAfterMassUpdate = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterMassUpdate = grandTotalAfterMassUpdate[4:]
        self.lgrObj.info("---------- Grand Total after Mass Update: "+str(SlicedGrandTotalAfterMassUpdate))

        expctGrandTotal=XLUtils.readData(self.file, 'TC_005', 2, 9)
        print(expctGrandTotal)
        print("Expected Grand Total is: "+str(expctGrandTotal))
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterMassUpdate):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after Mass Update action is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_005.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after Mass Update action is NOT correct ------")
            self.driver.close()

        #Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.TurboPricing
    def test_MassUpdateAction_Turbo(self, setup):
        # Step:03 Set up Logger Object
        self.lgrObj = Logger.logGen('TC_005_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("TC_005_3: Cart - Mass Update Action (Normal Cart - Turbo Pricing)  ")
        self.lgrObj.info("#################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_005', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile', 'Regular')
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_005', 1, 3)
        value = XLUtils.readData(self.file, 'TC_005', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_005', 1, 4)
        value = XLUtils.readData(self.file, 'TC_005', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_005', 1, 5)
        value = XLUtils.readData(self.file, 'TC_005', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_005', 1, 6)
        value = XLUtils.readData(self.file, 'TC_005', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add 5 Products to Cart")
        PrdName1 = XLUtils.readData(self.file, 'TC_005', 2, 8)
        PrdName2 = XLUtils.readData(self.file, 'TC_005', 3, 8)
        PrdName3 = XLUtils.readData(self.file, 'TC_005', 4, 8)
        PrdName4 = XLUtils.readData(self.file, 'TC_005', 5, 8)
        PrdName5 = XLUtils.readData(self.file, 'TC_005', 6, 8)

        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName1)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName2)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName3)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName4)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName5)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Copy Action")
        grandTotalBeforeMassUpdate = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalBeforeMassUpdate = grandTotalBeforeMassUpdate[4:]
        self.lgrObj.info("---------- Grand Total Before Mass Update: " + str(SlicedGrandTotalBeforeMassUpdate))

        self.lgrObj.info("---------- Select all check boxes and then Click on Mass Update action")
        time.sleep(3)
        CartPgObj.ClickSelectAllCheckBox()
        CartPgObj.ClickMassAction('Mass Update')

        self.lgrObj.info("---------- Set Quantity, Adjustments in Mass Update Pop-up")
        massUpdObj = MassUpdate(self.driver)
        time.sleep(3)
        massUpdObj.SetMassUpdateField('Set', 'Quantity', '5')
        massUpdObj.SetMassUpdateField('Set', 'Adjustment Type', '% Discount')
        massUpdObj.SetMassUpdateField('Set', 'Adjustment Amount', '10')
        massUpdObj.ClickButton('Apply')

        time.sleep(5)
        CartPgObj.WaitForPricingPendingIndicatorToGoAway()
        time.sleep(5)

        self.lgrObj.info("---------- Capture Grand Total and No. of line items After Mass Update Action")
        grandTotalAfterMassUpdate = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterMassUpdate = grandTotalAfterMassUpdate[4:]
        self.lgrObj.info("---------- Grand Total after Mass Update: " + str(SlicedGrandTotalAfterMassUpdate))

        expctGrandTotal = XLUtils.readData(self.file, 'TC_005', 2, 9)
        print(expctGrandTotal)
        print("Expected Grand Total is: " + str(expctGrandTotal))
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterMassUpdate):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after Mass Update action is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/"+"TC_005.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after Mass Update action is NOT correct ------")
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")