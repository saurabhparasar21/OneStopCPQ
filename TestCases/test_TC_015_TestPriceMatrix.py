import pytest
import time

from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.loginPage import loginPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger

class Test_PriceMatrix:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Step:04 Set-up Test Scenario. Pass the driver through
    @pytest.mark.RegularPricing
    def test_PriceMatrix_Classic(self,setup):
        self.lgrObj = Logger.logGen('TC_015_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_015_1: Price Matrix (Regular Pricing)              ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_015', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_015', 1, 3)
        value = XLUtils.readData(self.file, 'TC_015', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_015', 1, 4)
        value = XLUtils.readData(self.file, 'TC_015', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_015', 1, 5)
        value = XLUtils.readData(self.file, 'TC_015', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_015', 1, 6)
        value = XLUtils.readData(self.file, 'TC_015', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Search and Add Product to Cart")
        PrdName= XLUtils.readData(self.file, 'TC_015', 2, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart',PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Set Quantity, MN - 2020 LI PICK and check if appropriate bucket adjustment is applied")
        CartPgObj.SetQuantityForLineItem(PrdName,10)
        CartPgObj.SetValueInShoppingCartTable(PrdName,"MN - 2020 LI PICK","Picklist",'Pick 1')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: "+str(SlicedGrandTotalAfterDelete))
        expctGrandTotal=str("950")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 1st bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 1st bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 20)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 2')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("1,800.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 2nd bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 2nd bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 30)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 3')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("2,550.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 3rd bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 3rd bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 31)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("3,100.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix OutSide bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix OutSide bucket pricing is correct")
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(6)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_PriceMatrix_Split(self,setup):
        self.lgrObj = Logger.logGen('TC_015_2')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_015_2: Price Matrix (Async Pricing)                 ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_015', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_015', 1, 3)
        value = XLUtils.readData(self.file, 'TC_015', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_015', 1, 4)
        value = XLUtils.readData(self.file, 'TC_015', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_015', 1, 5)
        value = XLUtils.readData(self.file, 'TC_015', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_015', 1, 6)
        value = XLUtils.readData(self.file, 'TC_015', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Search and Add Product to Cart")
        PrdName= XLUtils.readData(self.file, 'TC_015', 2, 7)
        CtlgPgObj.SearchAndAddProduct('View Cart',PrdName)
        self.lgrObj.info("---------- Click on Mini-Cart & then View Cart button")
        CtlgPgObj.ClickCatalogPageButton('mini-cart')
        CtlgPgObj.ClickCatalogPageButton('view-cart')
        time.sleep(3)

        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(7)

        self.lgrObj.info("---------- Set Quantity, MN - 2020 LI PICK and check if appropriate bucket adjustment is applied")
        CartPgObj.SetQuantityForLineItem(PrdName,10)
        CartPgObj.SetValueInShoppingCartTable(PrdName,"MN - 2020 LI PICK","Picklist",'Pick 1')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: "+str(SlicedGrandTotalAfterDelete))
        expctGrandTotal=str("950")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 1st bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 1st bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 20)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 2')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("1,800.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 2nd bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 2nd bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 30)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 3')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("2,550.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 3rd bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 3rd bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 31)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("3,100.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix OutSide bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix OutSide bucket pricing is correct")
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(6)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_PriceMatrix_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_015_3')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_015_3: Price Matrix (Turbo Pricing)                 ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_015', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_015', 1, 3)
        value = XLUtils.readData(self.file, 'TC_015', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_015', 1, 4)
        value = XLUtils.readData(self.file, 'TC_015', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_015', 1, 5)
        value = XLUtils.readData(self.file, 'TC_015', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_015', 1, 6)
        value = XLUtils.readData(self.file, 'TC_015', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Search and Add Product to Cart")
        PrdName = XLUtils.readData(self.file, 'TC_015', 2, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info(
            "---------- Set Quantity, MN - 2020 LI PICK and check if appropriate bucket adjustment is applied")
        CartPgObj.SetQuantityForLineItem(PrdName, 10)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 1')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("950")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 1st bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 1st bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 20)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 2')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("1,800.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 2nd bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 2nd bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 30)
        CartPgObj.SetValueInShoppingCartTable(PrdName, "MN - 2020 LI PICK", "Picklist", 'Pick 3')
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("2,550.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix 3rd bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix 3rd bucket pricing is correct")
            assert False
            self.driver.close()

        CartPgObj.SetQuantityForLineItem(PrdName, 31)
        self.lgrObj.info("---------- Click on Reprice button")
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Verify Grand Total")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        print("Actual Grand Total is: " + str(SlicedGrandTotalAfterDelete))
        expctGrandTotal = str("3,100.00")
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Price Matrix OutSide bucket pricing is correct")
        else:
            self.lgrObj.info("---------- (FAILED): Price Matrix OutSide bucket pricing is correct")
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(6)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()