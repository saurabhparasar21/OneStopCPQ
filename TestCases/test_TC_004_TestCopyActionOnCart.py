from utilities.readProperties import ReadConfig
from utilities.Logger import Logger
from utilities import XLUtils
from pageObjects.loginPage import loginPage
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.CartPage import CartPage
import time
import pytest

    # Step:01 Create a Test class
class Test_CartCopyAction:
    # Step:02 Read Common Variables from Configuration file
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    #Step:04 Set-up Test Scenario. Pass the driver through
    @pytest.mark.RegularPricing
    def test_CartCopyAction_Classic(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_004_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_004_1: Cart - Copy Action (Regular Cart - Normal Pricing)   ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_004', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_004', 1, 3)
        value = XLUtils.readData(self.file, 'TC_004', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_004', 1, 4)
        value = XLUtils.readData(self.file, 'TC_004', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_004', 1, 5)
        value = XLUtils.readData(self.file, 'TC_004', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_004', 1, 6)
        value = XLUtils.readData(self.file, 'TC_004', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        # Search and add Product to Cart
        PrdName = XLUtils.readData(self.file,'TC_004', 2, 8)
        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Copy Action")
        grandTotalBeforeCopy=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalBeforeCopy=grandTotalBeforeCopy[4:]
        NoOfRowsBeforeCopy = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total before Copy: "+str(SlicedGrandTotalBeforeCopy))
        self.lgrObj.info("---------- No. of rows before Copy: "+str(NoOfRowsBeforeCopy))

        self.lgrObj.info("---------- Select the Product Checkbox and click on Copy button")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Copy')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items After Copy Action")
        grandTotalAfterCopy = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterCopy = grandTotalAfterCopy[4:]
        NoOfRowsAfterCopy = CartPgObj.FindNoOfCartLines()

        # Check if the Lines are copied properly and the Total is Grand Total is correct
        self.lgrObj.info("---------- Grand Total after Copy: " + str(SlicedGrandTotalAfterCopy))
        self.lgrObj.info("---------- No. of rows after Copy: " + str(NoOfRowsAfterCopy))

        if str(NoOfRowsAfterCopy) == str(2*NoOfRowsBeforeCopy):
            assert True
            self.lgrObj.info("---------- (PASSED): Cart Line Item is copied successfully ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Cart Line Item is NOT copied successfully ------")
            self.driver.close()

        if str(float(SlicedGrandTotalAfterCopy)) == str(2*float(SlicedGrandTotalBeforeCopy)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after copy action is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after copy action is NOT correct ------")
            self.driver.close()
        time.sleep(3)
        #Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(10)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_CartCopyAction_Split(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_004_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_004_2: Cart - Copy Action Split Cart - Async Pricing      ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_004', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_004', 1, 3)
        value = XLUtils.readData(self.file, 'TC_004', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_004', 1, 4)
        value = XLUtils.readData(self.file, 'TC_004', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_004', 1, 5)
        value = XLUtils.readData(self.file, 'TC_004', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_004', 1, 6)
        value = XLUtils.readData(self.file, 'TC_004', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(7)
        CtlgPgObj = CatalogPage(self.driver)
        # Search and add Product to Cart
        PrdName = XLUtils.readData(self.file,'TC_004', 2, 8)
        HomePage.SwitchToFrame(self)
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
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Copy Action")
        grandTotalBeforeCopy=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalBeforeCopy=grandTotalBeforeCopy[4:]
        NoOfRowsBeforeCopy = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total Before Copy: "+str(SlicedGrandTotalBeforeCopy))
        self.lgrObj.info("---------- No of rows before Copy: "+str(NoOfRowsBeforeCopy))

        self.lgrObj.info("---------- Select the Product Checkbox and click on Copy button")
        time.sleep(3)
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Copy')
        time.sleep(7)
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items After Copy Action")

        grandTotalAfterCopy = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterCopy = grandTotalAfterCopy[4:]
        NoOfRowsAfterCopy = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total After Copy: " + str(SlicedGrandTotalAfterCopy))
        self.lgrObj.info("---------- No of rows After Copy: " + str(NoOfRowsAfterCopy))

        # Check if the Lines are copied properly and the Total is Grand Total is correct
        print("No of rows before copy is: " + str(2*NoOfRowsBeforeCopy))
        print("No of rows after copy is: "+str(NoOfRowsAfterCopy))
        if str(NoOfRowsAfterCopy) == str(2*NoOfRowsBeforeCopy):
            print("No of Rows after Copy matched")
            assert True
            self.lgrObj.info("---------- (PASSED): Cart Line Item is copied successfully ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Cart Line Item is NOT copied successfully ------")
            self.driver.close()

        if str(float(SlicedGrandTotalAfterCopy)) == str(2*float(SlicedGrandTotalBeforeCopy)):
            print("Grand Total after Copy is matched")
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after copy action is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after copy action is NOT correct ------")
            self.driver.close()

        #Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_CartCopyAction_Turbo(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_004_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("    TC_004_3: Cart - Copy Action (Normal Cart - Turbo Pricing)     ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_004', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_004', 1, 3)
        value = XLUtils.readData(self.file, 'TC_004', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_004', 1, 4)
        value = XLUtils.readData(self.file, 'TC_004', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_004', 1, 5)
        value = XLUtils.readData(self.file, 'TC_004', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_004', 1, 6)
        value = XLUtils.readData(self.file, 'TC_004', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        time.sleep(4)

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(7)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to Cart")
        PrdName = XLUtils.readData(self.file,'TC_004', 2, 8)
        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        #CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Copy Action")
        grandTotalBeforeCopy=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalBeforeCopy=grandTotalBeforeCopy[4:]
        NoOfRowsBeforeCopy = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total Before Copy: "+str(SlicedGrandTotalBeforeCopy))
        self.lgrObj.info("---------- No. of Rows Before Copy: "+str(NoOfRowsBeforeCopy))

        self.lgrObj.info("---------- Select the Product Checkbox and click on Copy button")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Copy')
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(15)

        self.lgrObj.info("---------- Capture Grand Total and No. of line items After Copy Action")
        grandTotalAfterCopy = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterCopy = grandTotalAfterCopy[4:]
        NoOfRowsAfterCopy = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total after copy is: " + str(SlicedGrandTotalAfterCopy))
        self.lgrObj.info("---------- No of rows after copy is: " + str(NoOfRowsAfterCopy))

        # Check if the Lines are copied properly and the Total is Grand Total is correct
        if str(NoOfRowsAfterCopy) == str(2*NoOfRowsBeforeCopy):
            assert True
            self.lgrObj.info("---------- (PASSED): Cart Line Item is copied successfully ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Cart Line Item is NOT copied successfully ------")
            self.driver.close()

        if str(float(SlicedGrandTotalAfterCopy)) == str(2*float(SlicedGrandTotalBeforeCopy)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after copy action is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after copy action is NOT correct ------")
            self.driver.close()

        #Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- End ----------")
        self.driver.close()