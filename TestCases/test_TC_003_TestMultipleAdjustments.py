import pytest
import allure

from utilities.readProperties import ReadConfig
from utilities.Logger import Logger
from utilities import XLUtils
from pageObjects.loginPage import loginPage
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.MultipleAdjustmentsDialog import MultipleAdjustmentsDialog
from pageObjects.CartPage import CartPage
import time


class Test_MultipleAdjustments:
    baseUrl=ReadConfig.getbaseURL()
    UserName=ReadConfig.getuserName()
    Password=ReadConfig.getpassword()
    file=ReadConfig.getFilePath()

    # Make Sure Method name contains test keyword
    @pytest.mark.RegularPricing
    def test_MultipleAdjustment_Classic(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_003_1')
        self.driver=setup
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_003_1: MultipleAdjustment (Regular Cart - Normal Pricing)   ")
        self.lgrObj.info("#################################################################")

        self.driver.get(self.baseUrl)
        self.lgrObj.info("---------- Login to the Application")
        self.lgnObj=loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_003', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_003', 1, 3)
        value = XLUtils.readData(self.file, 'TC_003', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_003', 1, 4)
        value = XLUtils.readData(self.file, 'TC_003', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_003', 1, 5)
        value = XLUtils.readData(self.file, 'TC_003', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_003', 1, 6)
        value = XLUtils.readData(self.file, 'TC_003', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)
        CtlgPgObj=CatalogPage(self.driver)
        # Search and add Product to Cart
        PrdName=XLUtils.readData(self.file,'TC_003',2,8)
        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart',PrdName)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Click on 3 dots buttons
        CartPgObj.ClickOn3VerticalDots(PrdName)

        self.lgrObj.info("---------- Click on Multiple Adjustment Button")
        CartPgObj.ClickOn3DotsButton("Multiple Adjustments")

        self.lgrObj.info("---------- Add 2 Adjs in Mul Adj Pop-up and click on Save")
        # Set up Object for Multiple Adjustment Pop-up
        self.MulAdj = MultipleAdjustmentsDialog(self.driver)
        # Set Type
        self.MulAdj.SetType(1, 'Default')
        # Set Adjustment Applies to
        self.MulAdj.SetAdjustmentAppliesTo(1,'Starting Price')
        # Set Adjustment Type
        self.MulAdj.SetAdjustmentType(1,'% Discount')
        # Set Adjustment Amount
        self.MulAdj.SetAdjustmentAmount(1,10)
        # Click on Save button to add data for 2nd row
        self.MulAdj.ClickAddAnotherAdjustment()
        # Set data for the second row
        self.MulAdj.SetType(2,'Default')
        self.MulAdj.SetAdjustmentAppliesTo(2,'Previous Price')
        self.MulAdj.SetAdjustmentType(2,'% Discount')
        self.MulAdj.SetAdjustmentAmount(2,20)

        # Click on Save Button
        self.MulAdj.ClickButton('Save')
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)
        # Capture th Grand Total and verify with the expected data
        expGrandTotal = XLUtils.readData(self.file, 'TC_003', 2, 9)
        self.lgrObj.info("---------- Expected Grand Total: "+str(expGrandTotal))
        print("Expected Grand Total is: "+str(expGrandTotal))
        # Set obj to access methods for Cart page
        self.cartPage=CartPage(self.driver)
        actGrandTotal=self.cartPage.GetValueOfTotal('Grand Total')
        self.lgrObj.info("---------- Actual Grand Total: " +str(actGrandTotal))
        if str(expGrandTotal) in (str(actGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after multiple adjustments is correct")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
        else:
            self.driver.save_screenshot("../Screenshots/" + "TC_003.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after multiple adjustments is not correct")
            self.lgrObj.info("---------- END ----------")
            assert False
            self.driver.close()

    @pytest.mark.TurboPricing
    def test_MultipleAdjustment_Turbo(self, setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_003_2')
        self.driver = setup
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_003_2: MultipleAdjustment (Regular Cart - Turbo Pricing)    ")
        self.lgrObj.info("#################################################################")

        self.driver.get(self.baseUrl)
        ## Login to the Application
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_003', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_003', 1, 3)
        value = XLUtils.readData(self.file, 'TC_003', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_003', 1, 4)
        value = XLUtils.readData(self.file, 'TC_003', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_003', 1, 5)
        value = XLUtils.readData(self.file, 'TC_003', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_003', 1, 6)
        value = XLUtils.readData(self.file, 'TC_003', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to Cart")
        PrdName = XLUtils.readData(self.file, 'TC_003', 2, 8)
        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        #CartPgObj.WaitForPricingProgressBarToFinish()

        # Click on 3 dots buttons
        CartPgObj.ClickOn3VerticalDots(PrdName)
        time.sleep(3)
        self.lgrObj.info("---------- Click on Multiple Adjustment Button")
        CartPgObj.ClickOn3DotsButton("Multiple Adjustments")

        # Set up Object for Multiple Adjustment Pop-up
        self.MulAdj = MultipleAdjustmentsDialog(self.driver)
        self.MulAdj.ClickButton('Cancel')
        time.sleep(2)
        (self)
        CartPgObj.ClickOn3VerticalDots(PrdName)
        CartPgObj.ClickOn3DotsButton("Multiple Adjustments")

        self.lgrObj.info("---------- Add 2 Adjs in Multiple Adj pop-up and click on Save")
        # Set Type
        self.MulAdj.SetType(1,'Default')
        # Set Adjustment Applies to
        self.MulAdj.SetAdjustmentAppliesTo(1, 'Starting Price')
        # Set Adjustment Type
        self.MulAdj.SetAdjustmentType(1, '% Discount')
        # Set Adjustment Amount
        self.MulAdj.SetAdjustmentAmount(1, 10)
        # Click on Save button to add data for 2nd row
        self.MulAdj.ClickAddAnotherAdjustment()
        # Set data for the second row
        self.MulAdj.SetType(2, 'Default')
        self.MulAdj.SetAdjustmentAppliesTo(2, 'Previous Price')
        self.MulAdj.SetAdjustmentType(2, '% Discount')
        self.MulAdj.SetAdjustmentAmount(2, 20)

        # Click on Save Button
        self.MulAdj.ClickButton('Save')

        self.lgrObj.info("---------- Capture th Grand Total and verify with the expected data")
        expGrandTotal = XLUtils.readData(self.file, 'TC_003', 2, 9)
        self.lgrObj.info("---------- Expected Grand Total: "+str(expGrandTotal))
        actGrandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        self.lgrObj.info("---------- Actual Grand Total: "+str(actGrandTotal))
        print("Actual total is: " +str(actGrandTotal))
        if str(expGrandTotal) in (str(actGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after multiple adjustments is correct **********")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
        else:
            self.driver.save_screenshot("../Screenshots/" + "TC_003.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after multiple adjustments is not correct **********")
            self.lgrObj.info("---------- (FAILED): (NOT SUPPORTED) Turbo Pricing")
            self.lgrObj.info("---------- END ----------")
            self.driver.close()
            assert False


        # Make Sure Method name contains test keyword

    @pytest.mark.Split
    def test_MultipleAdjustment_Split(self, setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_003_3')
        self.driver = setup
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_003_3: MultipleAdjustment Split Cart - Async Pricing      ")
        self.lgrObj.info("#################################################################")

        self.driver.get(self.baseUrl)
        ## Login to the Application
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_003', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile','Split')

        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_003', 1, 3)
        value = XLUtils.readData(self.file, 'TC_003', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_003', 1, 4)
        value = XLUtils.readData(self.file, 'TC_003', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_003', 1, 5)
        value = XLUtils.readData(self.file, 'TC_003', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_003', 1, 6)
        value = XLUtils.readData(self.file, 'TC_003', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to Cart")
        PrdName = XLUtils.readData(self.file, 'TC_003', 2, 8)
        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName)

        # Click on Mini-Cart & then View Cart button
        CtlgPgObj.ClickCatalogPageButton('mini-cart')
        CtlgPgObj.ClickCatalogPageButton('view-cart')
        #time.sleep(10)

        # Set up Object for Cart Page
        CartPgObj=CartPage(self.driver)
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)

        self.lgrObj.info("---------- Click on 3 dots buttons")
        CartPgObj.ClickOn3VerticalDots(PrdName)

        self.lgrObj.info("---------- Click on Multiple Adjustment Button")
        CartPgObj.ClickOn3DotsButton("Multiple Adjustments")

        # MULTIPLE ADJUSTMENT POP-UP
        # Set up Object for Multiple Adjustment Pop-up
        self.MulAdj = MultipleAdjustmentsDialog(self.driver)
        # Set Type
        self.MulAdj.SetType(1, 'Default')
        # Set Adjustment Applies to
        self.MulAdj.SetAdjustmentAppliesTo(1, 'Starting Price')
        # Set Adjustment Type
        self.MulAdj.SetAdjustmentType(1, '% Discount')
        # Set Adjustment Amount
        self.MulAdj.SetAdjustmentAmount(1, 10)
        # Click on Save button to add data for 2nd row
        self.MulAdj.ClickAddAnotherAdjustment()
        # Set data for the second row
        self.MulAdj.SetType(2, 'Default')
        self.MulAdj.SetAdjustmentAppliesTo(2, 'Previous Price')
        self.MulAdj.SetAdjustmentType(2, '% Discount')
        self.MulAdj.SetAdjustmentAmount(2, 20)

        # Click on Save Button
        self.MulAdj.ClickButton('Save')
        self.lgrObj.info("---------- Click Save button after adding 2 adjustment lines")
        ## Click on Submit for Pricing (Async) button
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) to calculate Total based on mul adjs")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Capture th Grand Total and verify with the expected data
        expGrandTotal = XLUtils.readData(self.file, 'TC_003', 2, 9)
        # Set obj to access methods for Cart page
        self.cartPage = CartPage(self.driver)
        actGrandTotal = self.cartPage.GetValueOfTotal('Grand Total')
        self.lgrObj.info("---------- Expected total is: "+str(expGrandTotal))
        self.lgrObj.info("---------- Actual total is: " +str(actGrandTotal))

        if str(expGrandTotal) in (str(actGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after multiple adjustments is correct **********")
            self.driver.close()
        else:
            self.driver.save_screenshot("../Screenshots/" + "TC_003.png")
            self.lgrObj.info("---------- (FAILED): (CPQ-46474) Grand Total after multiple adjustments is not correct")
            assert False
            self.driver.close()
