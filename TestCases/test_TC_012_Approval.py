import pytest
import time

from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.HomeTab import HomePage
from pageObjects.NetAdjustmentPopUp import NetAdjustmentPopUp
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.loginPage import loginPage
from pageObjects.ApprovalsPage import ApprovalsPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger


class Test_Approvals:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    @pytest.mark.RegularPricing
    def test_Approval_Classic(self, setup):
        self.lgrObj = Logger.logGen('TC_012_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("         TC_012_1: Approvals Reg Cart Normal Pricing             ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_012', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_012', 1, 3)
        value = XLUtils.readData(self.file, 'TC_012', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_012', 1, 4)
        value = XLUtils.readData(self.file, 'TC_012', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_012', 1, 5)
        value = XLUtils.readData(self.file, 'TC_012', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_012', 1, 6)
        value = XLUtils.readData(self.file, 'TC_012', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_012', 2, 7)

        self.lgrObj.info("---------- Search and add Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Set desired Line item fields so that Approval will get triggered")
        CartPgObj.SetQuantityForLineItem(PrdName,10)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj = NetAdjustmentPopUp(self.driver)

        # Adjustment Type = % Discount
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '20')
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Check if Approval icon is shown for the line item
        IsVisible = CartPgObj.IsApprovalIconVisible(PrdName)
        if IsVisible == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Approval icon is visible for the line item")
        else:
            self.lgrObj.info("---------- (FAILED): Approval icon is NOT visible for the line item")
            assert False
            self.driver.close()

        CartApprovalStatus=CartPgObj.GetCartApprovalStatus()
        if CartApprovalStatus == "Approval Required":
            assert True
            self.lgrObj.info("---------- (PASSED): Cart page Approval Status is changed to Approval Required")
        else:
            self.lgrObj.info("---------- (FAILED): Cart page Approval Status is NOT changed to Approval Required")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Click on Submit For Approval button")
        CartPgObj.ClickCartButtons('Submit for Approval')
        ApprvalPgObj = ApprovalsPage(self.driver)
        ApprvalPgObj.SwitchToApprovalFrame('Quote')
        ApprvalPgObj.ClickButton('Submit')
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('title')
        ApprvalPgObj.ClickButton('Return')

        # Check Approval Stage
        #HomePage.SwitchToDefault(self)
        #HomePage.SwitchToFrame(self)
        time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[1])
        #print("Title is: " + str(self.driver.title))
        ActualStatus = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        #print("Status is: "+str(ActualStatus))
        if ActualStatus == "Pending Approval":
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal Detail page Approval Status is updated to Approval Required")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Detail page Approval Status is NOT updated to Approval Required")

        self.lgrObj.info("---------- Click on My Approvals and approve the request")
        # Click on My Approvals button
        PropsPageObj.ClickMenuButton('My Approvals')
        # Click on All Approvals
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('My Approvals')
        time.sleep(5)
        ApprvalPgObj.ClickTab('All Approvals')
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('My Approvals')
        ApprvalPgObj.SelectAllStepsCheckbox()
        # Time is needed
        time.sleep(6)
        ApprvalPgObj.ClickButton('Approve')
        ApprvalPgObj.EnterApproverComment("Approved")
        ApprvalPgObj.ClickButton('Save')
        ApprvalPgObj.ClickButton('Return')

        # Check Approval Stage
        time.sleep(6)
        self.driver.switch_to.window(self.driver.window_handles[2])
        print("Title is: " + str(self.driver.title))
        ActualStatus = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        if ActualStatus == "Approved":
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal Detail page Approval Status is updated to Approved")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Detail page Approval Status is NOT updated to Approved")
            assert False
            self.driver.close()


        self.lgrObj.info("---------- Delete the proposal")
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.driver.quit()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.TurboPricing
    def test_Approval_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_012_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("         TC_012_2: Approvals Reg Cart Turbo Pricing              ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_012', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_012', 1, 3)
        value = XLUtils.readData(self.file, 'TC_012', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_012', 1, 4)
        value = XLUtils.readData(self.file, 'TC_012', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_012', 1, 5)
        value = XLUtils.readData(self.file, 'TC_012', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_012', 1, 6)
        value = XLUtils.readData(self.file, 'TC_012', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_012', 2, 7)

        self.lgrObj.info("---------- Search and add Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Set desired Line item fields so that Approval will get triggered")
        CartPgObj.SetQuantityForLineItem(PrdName,10)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj = NetAdjustmentPopUp(self.driver)

        # Adjustment Type = % Discount
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '20')
        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Check if Approval icon is shown for the line item
        IsVisible = CartPgObj.IsApprovalIconVisible(PrdName)
        if IsVisible == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Approval icon is visible for the line item")
        else:
            self.lgrObj.info("---------- (FAILED): TURBO PRICING ISSUE IN WIN'20 ORG Approval icon is NOT visible for the line item")
            assert False
            self.driver.close()

        CartApprovalStatus=CartPgObj.GetCartApprovalStatus()
        if CartApprovalStatus == "Approval Required":
            assert True
            self.lgrObj.info("---------- (PASSED): Cart page Approval Status is changed to Approval Required")
        else:
            self.lgrObj.info("---------- (FAILED): Cart page Approval Status is NOT changed to Approval Required")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Click on Submit For Approval button")
        CartPgObj.ClickCartButtons('Submit for Approval')
        ApprvalPgObj = ApprovalsPage(self.driver)
        ApprvalPgObj.SwitchToApprovalFrame('Quote')
        ApprvalPgObj.ClickButton('Submit')
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('title')
        ApprvalPgObj.ClickButton('Return')

        # Check Approval Stage
        #HomePage.SwitchToDefault(self)
        #HomePage.SwitchToFrame(self)
        time.sleep(10)
        self.driver.switch_to.window(self.driver.window_handles[1])
        #print("Title is: " + str(self.driver.title))
        ActualStatus = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        #print("Status is: "+str(ActualStatus))
        if ActualStatus == "Approval Required":
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal Detail page Approval Status is updated to Approval Required")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Detail page Approval Status is NOT updated to Approval Required")

        self.lgrObj.info("---------- Click on My Approvals and approve the request")
        # Click on My Approvals button
        PropsPageObj.ClickMenuButton('My Approvals')
        # Click on All Approvals
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('My Approvals')
        time.sleep(5)
        ApprvalPgObj.ClickTab('All Approvals')
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('My Approvals')
        ApprvalPgObj.SelectAllStepsCheckbox()
        # Time is needed
        time.sleep(5)
        ApprvalPgObj.ClickButton('Approve')
        ApprvalPgObj.EnterApproverComment("Approved")
        ApprvalPgObj.ClickButton('Save')
        ApprvalPgObj.ClickButton('Return')

        # Check Approval Stage
        time.sleep(6)
        self.driver.switch_to.window(self.driver.window_handles[2])
        print("Title is: " + str(self.driver.title))
        ActualStatus = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        if ActualStatus == "Approved":
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal Detail page Approval Status is updated to Approved")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Detail page Approval Status is NOT updated to Approved")
            assert False
            self.driver.close()


        self.lgrObj.info("---------- Delete the proposal")
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.driver.quit()
        self.lgrObj.info("---------- END ---------- ")

    @pytest.mark.Split
    def test_Approval_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_012_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("         TC_012_3: Approvals Reg Cart Turbo Pricing              ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_012', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_012', 1, 3)
        value = XLUtils.readData(self.file, 'TC_012', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_012', 1, 4)
        value = XLUtils.readData(self.file, 'TC_012', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_012', 1, 5)
        value = XLUtils.readData(self.file, 'TC_012', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_012', 1, 6)
        value = XLUtils.readData(self.file, 'TC_012', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_012', 2, 7)

        self.lgrObj.info("---------- Search and add Product to Cart")
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
        time.sleep(4)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Set desired Line item fields so that Approval will get triggered")
        time.sleep(4)
        CartPgObj.SetQuantityForLineItem(PrdName,10)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj = NetAdjustmentPopUp(self.driver)

        # Adjustment Type = % Discount
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount', '20')
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(4)
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Check if Approval icon is shown for the line item
        IsVisible = CartPgObj.IsApprovalIconVisible(PrdName)
        if IsVisible == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Approval icon is visible for the line item")
        else:
            self.lgrObj.info("---------- (FAILED): Approval icon is NOT visible for the line item")
            assert False
            self.driver.close()

        CartApprovalStatus=CartPgObj.GetCartApprovalStatus()
        if CartApprovalStatus == "Approval Required":
            assert True
            self.lgrObj.info("---------- (PASSED): Cart page Approval Status is changed to Approval Required")
        else:
            self.lgrObj.info("---------- (FAILED): Cart page Approval Status is NOT changed to Approval Required")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Click on Submit For Approval button")
        self.lgrObj.info("---------- (FAILED): CPQ-40251")
        CartPgObj.ClickCartButtons('Submit for Approval')
        ApprvalPgObj = ApprovalsPage(self.driver)
        ApprvalPgObj.SwitchToApprovalFrame('Quote')
        ApprvalPgObj.ClickButton('Submit')
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('title')
        ApprvalPgObj.ClickButton('Return')

        # Check Approval Stage
        #HomePage.SwitchToDefault(self)
        #HomePage.SwitchToFrame(self)
        time.sleep(6)
        self.driver.switch_to.window(self.driver.window_handles[1])
        #print("Title is: " + str(self.driver.title))
        ActualStatus = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        #print("Status is: "+str(ActualStatus))
        if ActualStatus == "Approval Required":
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal Detail page Approval Status is updated to Approval Required")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Detail page Approval Status is NOT updated to Approval Required")

        self.lgrObj.info("---------- Click on My Approvals and approve the request")
        # Click on My Approvals button
        PropsPageObj.ClickMenuButton('My Approvals')
        # Click on All Approvals
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('My Approvals')
        time.sleep(5)
        ApprvalPgObj.ClickTab('All Approvals')
        ApprvalPgObj.SwitchToDefault()
        ApprvalPgObj.SwitchToApprovalFrame('My Approvals')
        ApprvalPgObj.SelectAllStepsCheckbox()
        # Time is needed
        time.sleep(3)
        ApprvalPgObj.ClickButton('Approve')
        ApprvalPgObj.EnterApproverComment("Approved")
        ApprvalPgObj.ClickButton('Save')
        ApprvalPgObj.ClickButton('Return')

        # Check Approval Stage
        time.sleep(6)
        self.driver.switch_to.window(self.driver.window_handles[2])
        print("Title is: " + str(self.driver.title))
        ActualStatus = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        if ActualStatus == "Approved":
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal Detail page Approval Status is updated to Approved")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Detail page Approval Status is NOT updated to Approved")
            assert False
            self.driver.close()


        self.lgrObj.info("---------- Delete the proposal")
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.driver.quit()
        self.lgrObj.info("----------- END ----------- ")
