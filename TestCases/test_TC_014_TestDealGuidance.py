import pytest
import time


from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.HomeTab import HomePage
from pageObjects.NetAdjustmentPopUp import NetAdjustmentPopUp
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.loginPage import loginPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger

class Test_ConstRule_Inclusion:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Step:04 Set-up Test Scenario. Pass the driver through
    @pytest.mark.RegularPricing
    def test_DealGuidance_Classic(self,setup):
        self.lgrObj = Logger.logGen('TC_014_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_014_1: Deal Guidance (Regular Pricing)              ")
        self.lgrObj.info("####################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_014', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_014', 1, 3)
        value = XLUtils.readData(self.file, 'TC_014', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_014', 1, 4)
        value = XLUtils.readData(self.file, 'TC_014', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_014', 1, 5)
        value = XLUtils.readData(self.file, 'TC_014', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_014', 1, 6)
        value = XLUtils.readData(self.file, 'TC_014', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_014', 2, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart',PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '5')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched=CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName,'circle','rgb(56, 124, 53)')
        print("Matched is: "+str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '8')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'triangle', 'rgb(144, 238, 144)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '10')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'diamond', 'rgb(255, 229, 18)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '12')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'square', 'rgb(227, 111, 30)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '15')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'pentagon', 'rgb(178, 16, 44)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '20')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'star', 'rgb(0, 0, 160)')
        print("Matched is: " + str(Matched))

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(10)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_DealGuidance_Split(self,setup):
        self.lgrObj = Logger.logGen('TC_014_2')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_014_2: Deal Guidance (Split Cart)                   ")
        self.lgrObj.info("####################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_014', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_014', 1, 3)
        value = XLUtils.readData(self.file, 'TC_014', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_014', 1, 4)
        value = XLUtils.readData(self.file, 'TC_014', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_014', 1, 5)
        value = XLUtils.readData(self.file, 'TC_014', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_014', 1, 6)
        value = XLUtils.readData(self.file, 'TC_014', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_014', 2, 7)
        CtlgPgObj.SearchAndAddProduct('View Cart',PrdName)

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

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '5')
        time.sleep(2)

        self.lgrObj.info("---------- Click on Async Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched=CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName,'circle','rgb(56, 124, 53)')
        print("Matched is: "+str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '8')
        time.sleep(2)

        self.lgrObj.info("---------- Click on Async Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'triangle', 'rgb(144, 238, 144)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '10')
        time.sleep(2)

        self.lgrObj.info("---------- Click on Async Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'diamond', 'rgb(255, 229, 18)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '12')
        time.sleep(2)

        self.lgrObj.info("---------- Click on Async Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'square', 'rgb(227, 111, 30)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '15')
        time.sleep(2)

        self.lgrObj.info("---------- Click on Async Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'pentagon', 'rgb(178, 16, 44)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '20')
        time.sleep(2)

        self.lgrObj.info("---------- Click on Async Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'star', 'rgb(0, 0, 160)')
        print("Matched is: " + str(Matched))

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(10)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_DealGuidance_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_014_3')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_014_3: Deal Guidance (Turbo Pricing)              ")
        self.lgrObj.info("####################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_014', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_014', 1, 3)
        value = XLUtils.readData(self.file, 'TC_014', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_014', 1, 4)
        value = XLUtils.readData(self.file, 'TC_014', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_014', 1, 5)
        value = XLUtils.readData(self.file, 'TC_014', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_014', 1, 6)
        value = XLUtils.readData(self.file, 'TC_014', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_014', 2, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '5')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'circle', 'rgb(56, 124, 53)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '8')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'triangle', 'rgb(144, 238, 144)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '10')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'diamond', 'rgb(255, 229, 18)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '12')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'square', 'rgb(227, 111, 30)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '15')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'pentagon', 'rgb(178, 16, 44)')
        print("Matched is: " + str(Matched))

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '20')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Verify the Guidance Color")
        Matched = CartPgObj.VerifyDealGuidanceShapeAndColor(PrdName, 'star', 'rgb(0, 0, 160)')
        print("Matched is: " + str(Matched))

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(10)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()