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
class Test_CartDeletePrdAction:
    # Step:02 Read Common Variables from Configuration file
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    #Step:04 Set-up Test Scenario. Pass the driver through
    @pytest.mark.RegularPricing
    def test_DeleteProductAction_Classic(self,setup):
        # Step:03 Set up Logger Object
        self.lgrObj = Logger.logGen('TC_006_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("TC_006_1: Cart - Delete Product Action (Regular Cart - Normal Pricing)")
        self.lgrObj.info("#####################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_006', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_006', 1, 3)
        value = XLUtils.readData(self.file, 'TC_006', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_006', 1, 4)
        value = XLUtils.readData(self.file, 'TC_006', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_006', 1, 5)
        value = XLUtils.readData(self.file, 'TC_006', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_006', 1, 6)
        value = XLUtils.readData(self.file, 'TC_006', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add 5 Products to Cart")
        PrdName1 = XLUtils.readData(self.file, 'TC_006', 2, 8)
        PrdName2 = XLUtils.readData(self.file, 'TC_006', 3, 8)
        PrdName3 = XLUtils.readData(self.file, 'TC_006', 4, 8)
        PrdName4 = XLUtils.readData(self.file, 'TC_006', 5, 8)
        PrdName5 = XLUtils.readData(self.file, 'TC_006', 6, 8)

        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName1)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName2)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName3)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName4)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName5)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Delete Action")
        grandTotBefDel=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotBefDel=grandTotBefDel[4:]
        NoOfRowsBeforeDelete = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- No of roes before Delete action: "+str(NoOfRowsBeforeDelete))
        self.lgrObj.info("---------- Grand Total before delete action: "+str(SlicedGrandTotBefDel))

        # Select One Product. Delete it and then verify the Grand Total
        CartPgObj.ClickCartLineItemCheckBox(PrdName1)
        CartPgObj.ClickMassAction('Delete')

        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(3)

        # Capture Grand Total and No. of line items After One prod is Deleted
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        NoOfRowsAfter1PrdDelete = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total after One Product Delete: "+str(SlicedGrandTotalAfterDelete))

        expctGrandTotal=XLUtils.readData(self.file, 'TC_006', 2, 9)
        print(expctGrandTotal)
        print("Expected Grand Total after one pro is deleted: "+str(expctGrandTotal))
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- RESULTS: Grand Total after One Product Delete is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- RESULTS: Grand Total after One Product Delete is NOT correct ------")
            self.driver.close()

        if NoOfRowsAfter1PrdDelete == (NoOfRowsBeforeDelete-1):
            assert True
            self.lgrObj.info("---------- RESULTS: Row count after one product is deleted is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- RESULTS: Row count after one product is deleted is NOT correct ------")
            self.driver.close()

        self.lgrObj.info("---------- Delete all products and verify the no of rows and Grand Total")
        CartPgObj.ClickSelectAllCheckBox()
        CartPgObj.ClickMassAction('Delete')

        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Count no of rows after all lines are deleted")
        NoOfRowsAfterAllDelete = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Verify that after all cart lines are deleted the Grand Total section disappears")
        path="//div[contains(@ng-repeat,'Grand')]//div[2]//div[contains(@class,'plain-text')]"
        elements=self.driver.find_elements_by_xpath(path)
        if len(elements) == 0:
            assert True
            self.lgrObj.info("----------(PASSED): Grand Total after all prds deleted have disappeared ----------")
        else:
            assert False
            self.lgrObj.info("----------(FAILED): Grand Total after all prds deleted have NOT disappeared ------")

        if NoOfRowsAfterAllDelete == 0:
            assert True
            self.lgrObj.info("---------- (PASSED): All products have been deleted ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): All products have NOT been deleted ------")
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart and delete the Proposal")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.Split
    def test_DeleteProductAction_Split(self,setup):
        # Step:03 Set up Logger Object
        self.lgrObj = Logger.logGen('TC_006_2')
        self.lgrObj.info("#####################################################################")
        self.lgrObj.info(" TC_006_2: Cart - Delete Product Action Split Cart Async Pricing     ")
        self.lgrObj.info("#####################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_006', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_006', 1, 3)
        value = XLUtils.readData(self.file, 'TC_006', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_006', 1, 4)
        value = XLUtils.readData(self.file, 'TC_006', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_006', 1, 5)
        value = XLUtils.readData(self.file, 'TC_006', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_006', 1, 6)
        value = XLUtils.readData(self.file, 'TC_006', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add 5 Products to Cart")
        PrdName1 = XLUtils.readData(self.file, 'TC_006', 2, 8)
        PrdName2 = XLUtils.readData(self.file, 'TC_006', 3, 8)
        PrdName3 = XLUtils.readData(self.file, 'TC_006', 4, 8)
        PrdName4 = XLUtils.readData(self.file, 'TC_006', 5, 8)
        PrdName5 = XLUtils.readData(self.file, 'TC_006', 6, 8)

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
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(7)

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Mass Update Action")
        grandTotBefDel=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotBefDel=grandTotBefDel[4:]
        NoOfRowsBeforeDelete = CartPgObj.FindNoOfCartLines()
        print("No of Rows before Delete: "+str(NoOfRowsBeforeDelete))
        self.lgrObj.info("---------- No of rows before Delete action: "+str(NoOfRowsBeforeDelete))
        self.lgrObj.info("---------- Grand Total before delete action: "+str(SlicedGrandTotBefDel))

        self.lgrObj.info("---------- Select One Product. Delete it and then verify the Grand Total")
        CartPgObj.ClickCartLineItemCheckBox(PrdName1)
        CartPgObj.ClickMassAction('Delete')

        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(7)
        CartPgObj.WaitForPricingProgressBarToFinish()

        time.sleep(7)
        self.lgrObj.info("---------- Capture Grand Total and No. of line items After One prod is Deleted")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        NoOfRowsAfter1PrdDelete = CartPgObj.FindNoOfCartLines()
        print("No of Rows after Delete: " + str(NoOfRowsAfter1PrdDelete))
        self.lgrObj.info("---------- Grand Total after One Product Delete: "+str(SlicedGrandTotalAfterDelete))

        expctGrandTotal=XLUtils.readData(self.file, 'TC_006', 2, 9)
        print(expctGrandTotal)
        self.lgrObj.info("---------- Expected Grand Total after one pro is deleted: "+str(expctGrandTotal))
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after One Product Delete is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Submit for Pricing (Async) btn not present -------- ------")
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after One Product Delete is NOT correct ------")
            self.driver.close()

        if NoOfRowsAfter1PrdDelete == (NoOfRowsBeforeDelete-1):
            assert True
            self.lgrObj.info("---------- (PASSED): Row count after one product is deleted is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): Row count after one product is deleted is NOT correct ------")
            self.driver.close()

        self.lgrObj.info("---------- Delete all products and verify the no of rows and Grand Total")
        CartPgObj.ClickSelectAllCheckBox()
        CartPgObj.ClickMassAction('Delete')

        time.sleep(3)
        self.lgrObj.info("---------- Count no of rows after all lines are deleted")
        NoOfRowsAfterAllDelete = CartPgObj.FindNoOfCartLines()
        print("No of Rows after Delete: " + str(NoOfRowsAfterAllDelete))

        if NoOfRowsAfterAllDelete == 0:
            assert True
            self.lgrObj.info("---------- (PASSED): All products have been deleted ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): All products have NOT been deleted ------")
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart and delete it")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ----------")

    @pytest.mark.TurboPricing
    def test_DeleteProductAction_Turbo(self,setup):
        # Step:03 Set up Logger Object
        self.lgrObj = Logger.logGen('TC_006_3')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("TC_006_3: Cart - Delete Product Action (Regular Cart - Turbo Pricing)")
        self.lgrObj.info("#####################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_006', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_006', 1, 3)
        value = XLUtils.readData(self.file, 'TC_006', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_006', 1, 4)
        value = XLUtils.readData(self.file, 'TC_006', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_006', 1, 5)
        value = XLUtils.readData(self.file, 'TC_006', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_006', 1, 6)
        value = XLUtils.readData(self.file, 'TC_006', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)

        self.lgrObj.info("---------- Search and add 5 Products to Cart")
        PrdName1 = XLUtils.readData(self.file, 'TC_006', 2, 8)
        PrdName2 = XLUtils.readData(self.file, 'TC_006', 3, 8)
        PrdName3 = XLUtils.readData(self.file, 'TC_006', 4, 8)
        PrdName4 = XLUtils.readData(self.file, 'TC_006', 5, 8)
        PrdName5 = XLUtils.readData(self.file, 'TC_006', 6, 8)

        HomePage.SwitchToFrame(self)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName1)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName2)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName3)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName4)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName5)

        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items before Delete Action")
        grandTotBefDel=CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotBefDel=grandTotBefDel[4:]
        NoOfRowsBeforeDelete = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- No of rows before Delete action: "+str(NoOfRowsBeforeDelete))
        self.lgrObj.info("---------- Grand Total before delete action: "+str(SlicedGrandTotBefDel))

        self.lgrObj.info("---------- Select One Product. Delete it and then verify the Grand Total")
        time.sleep(4)
        CartPgObj.ClickCartLineItemCheckBox(PrdName1)
        CartPgObj.ClickMassAction('Delete')

        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Capture Grand Total and No. of line items After One prod is Deleted")
        grandTotalAfterDelete = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotalAfterDelete = grandTotalAfterDelete[4:]
        NoOfRowsAfter1PrdDelete = CartPgObj.FindNoOfCartLines()
        self.lgrObj.info("---------- Grand Total after One Product Delete: "+str(SlicedGrandTotalAfterDelete))

        expctGrandTotal=XLUtils.readData(self.file, 'TC_006', 2, 9)
        print(expctGrandTotal)
        self.lgrObj.info("---------- Expected Grand Total after one pro is deleted: "+str(expctGrandTotal))
        if str(expctGrandTotal) in str(SlicedGrandTotalAfterDelete):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after One Product Delete is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): Grand Total after One Product Delete is NOT correct ------")
            self.driver.close()

        if NoOfRowsAfter1PrdDelete == (NoOfRowsBeforeDelete-1):
            assert True
            self.lgrObj.info("---------- (PASSED): Row count after one product is deleted is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): Row count after one product is deleted is NOT correct ------")
            self.driver.close()

        self.lgrObj.info("---------- Delete all products and verify the no of rows and Grand Total")
        time.sleep(4)
        CartPgObj.ClickSelectAllCheckBox()
        CartPgObj.ClickMassAction('Delete')

        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Count no of rows after all lines are deleted")
        NoOfRowsAfterAllDelete = CartPgObj.FindNoOfCartLines()

        self.lgrObj.info("---------- Verify that after all cart lines are deleted the Grand Total section disappears")
        path="//div[contains(@ng-repeat,'Grand')]//div[2]//div[contains(@class,'plain-text')]"
        elements=self.driver.find_elements_by_xpath(path)
        if len(elements) == 0:
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total after all prds deleted have disappeared ----------")
        else:
            assert False
            self.lgrObj.info("---------- (FAILED): Grand Total after all prds deleted have NOT disappeared ------")

        if NoOfRowsAfterAllDelete == 0:
            assert True
            self.lgrObj.info("---------- (PASSED): All products have been deleted ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_006.png")
            self.lgrObj.info("---------- (FAILED): All products have NOT been deleted ------")
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart and delete the proposal")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")