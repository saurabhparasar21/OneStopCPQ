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


class Test_ManualAdjustments:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    @pytest.mark.RegularPricing
    def test_ManualAdjustment_Classic(self, setup):
        self.lgrObj = Logger.logGen('TC_011_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info(" TC_011_1: Different Type of Adjustments Reg Cart Normal Pricing ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_011', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_011', 1, 3)
        value = XLUtils.readData(self.file, 'TC_011', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_011', 1, 4)
        value = XLUtils.readData(self.file, 'TC_011', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_011', 1, 5)
        value = XLUtils.readData(self.file, 'TC_011', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_011', 1, 6)
        value = XLUtils.readData(self.file, 'TC_011', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)

        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)

        # Adjustment Type = % Discount
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount','10')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("90") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Manual Adjustment (% Discount), Grand Total is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Manual Adjustment (% Discount), Grand Total is NOT correct ----------")
            assert False
            self.driver.close()

        # Adjustment Type = Discount Amount
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Discount Amount', '20')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("80") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Manual Adjustment (Discount Amount), Grand Total is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Manual Adjustment (Discount Amount), Grand Total is NOT correct ----------")
            assert False
            self.driver.close()

        # Adjustment Type = % Markup
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('% Markup', '10')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("110") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (%Mark up), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (%Mark up), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Markup Amount
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Markup Amount', '20')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("120") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Markup Amount), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Markup Amount), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Base Price Override, When applied on Bundle, the Base Pice though on UI does not get
        # changed but takes the override value. It does not affect the Option base price nor apply any discount
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Base Price Override', '30')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("30") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Base Price Override), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Base Price Override), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Price Override. When applied on Bundle, the Net Price, Net Adj% gets updated.
        # The Base Price, Option Price of the Bundle does not get changed. Only the Net Price.
        # The the same proportion of discount gets applied on the Net Price of the Option too
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Price Override', '30')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("30") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Price Override), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Price Override), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Price Factor. When applied there will be no changed to Base Price, Option price
        # for bundle or option line. However the Net Price of bundle will get multiplied by the factor
        # That results in + Net % hike in Bunlde and that same % gets applied on option which increases it's net Price
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Price Factor', '2')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("200") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Price Factor), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Price Factor), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Delete the Product & Add Product to test "Allow Manual Adjustment False at PLI"
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(3)

        self.lgrObj.info("---------- Go back to Catalog Page and the Prd to test Allow Manual Adj False at PLI")
        CartPgObj.ClickCartButtons('Add More Products')

        # Search and add product which is set to Allow Man Adj False
        PrdName2 = XLUtils.readData(self.file, 'TC_011', 3, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName2)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Check Net Adjustment link is disabled for this product
        Result1=CartPgObj.IsEnalbedOrDisabled(PrdName2,'Net Adjustment %')
        print(Result1)

        if str("disabled") in str(Result1):
            self.lgrObj.info("---------- (PASSED): Net Adj. is disabled for Product with Allow Manual Adj False in PLI")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Net Adj. is NOT disabled for Product with Allow Manual Adj False in PLI")
            assert False
            self.driver.close()

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
    def test_ManualAdjustment_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_011_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info(" TC_011_2: Different Type of Adjustments Reg Cart Turbo Pricing ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_011', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_011', 1, 3)
        value = XLUtils.readData(self.file, 'TC_011', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_011', 1, 4)
        value = XLUtils.readData(self.file, 'TC_011', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_011', 1, 5)
        value = XLUtils.readData(self.file, 'TC_011', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_011', 1, 6)
        value = XLUtils.readData(self.file, 'TC_011', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)

        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)

        # Adjustment Type = % Discount
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount','10')
        time.sleep(4)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("90") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Manual Adjustment (% Discount), Grand Total is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Manual Adjustment (% Discount), Grand Total is NOT correct ----------")
            assert False
            self.driver.close()

        # Adjustment Type = Discount Amount
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Discount Amount', '20')
        time.sleep(4)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("80") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Manual Adjustment (Discount Amount), Grand Total is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Manual Adjustment (Discount Amount), Grand Total is NOT correct ----------")
            assert False
            self.driver.close()

        # Adjustment Type = % Markup
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('% Markup', '10')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("110") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (%Mark up), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (%Mark up), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Markup Amount
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Markup Amount', '20')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("120") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Markup Amount), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Markup Amount), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # # Adjustment Type = Base Price Override, When applied on Bundle, the Base Pice though on UI does not get
        # # changed but takes the override value. It does not affect the Option base price nor apply any discount
        # time.sleep(2)
        # CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        # NetAdjObj.SetAdjustmentTypeAndValue('Base Price Override', '30')
        # time.sleep(2)
        # #self.lgrObj.info("---------- Click on Reprice button")
        #
        # CartPgObj.ClickCartButtons('Reprice')
        # CartPgObj.WaitForPricingProgressBarToFinish()
        # grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        # SlicedGrandTotal = grandTotal[4:]
        #
        # if str("30") in str(float(SlicedGrandTotal)):
        #         assert True
        #         self.lgrObj.info("---------- (PASSED): Manual Adjustment (Base Price Override), Grand Total is correct ----------")
        # else:
        #         self.lgrObj.info("---------- (FAILED): Manual Adjustment (Base Price Override), Grand Total is NOT correct ----------")
        #         assert False
        #         self.driver.close()

        # Adjustment Type = Price Override. When applied on Bundle, the Net Price, Net Adj% gets updated.
        # The Base Price, Option Price of the Bundle does not get changed. Only the Net Price.
        # The the same proportion of discount gets applied on the Net Price of the Option too
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Price Override', '30')
        time.sleep(4)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("30") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Price Override), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Price Override), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Price Factor. When applied there will be no changed to Base Price, Option price
        # for bundle or option line. However the Net Price of bundle will get multiplied by the factor
        # That results in + Net % hike in Bunlde and that same % gets applied on option which increases it's net Price
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Price Factor', '2')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()
        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("200") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Price Factor), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Price Factor), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Delete the Product & Add Product to test "Allow Manual Adjustment False at PLI"
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(3)

        self.lgrObj.info("---------- Go back to Catalog Page and the Prd to test Allow Manual Adj False at PLI")
        CartPgObj.ClickCartButtons('Add More Products')

        # Search and add product which is set to Allow Man Adj False
        PrdName2 = XLUtils.readData(self.file, 'TC_011', 3, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName2)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Check Net Adjustment link is disabled for this product
        Result1=CartPgObj.IsEnalbedOrDisabled(PrdName2,'Net Adjustment %')
        print(Result1)

        if str("disabled") in str(Result1):
            self.lgrObj.info("---------- (PASSED): Net Adj. is disabled for Product with Allow Manual Adj False in PLI")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Net Adj. is NOT disabled for Product with Allow Manual Adj False in PLI")
            assert False
            self.driver.close()

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
    def test_ManualAdjustment_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_011_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info(" TC_011_3: Different Type of Adjustments Split Cart Async Pricing")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_011', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile','Split')
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_011', 1, 3)
        value = XLUtils.readData(self.file, 'TC_011', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_011', 1, 4)
        value = XLUtils.readData(self.file, 'TC_011', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_011', 1, 5)
        value = XLUtils.readData(self.file, 'TC_011', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_011', 1, 6)
        value = XLUtils.readData(self.file, 'TC_011', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add Product to Cart")
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName)

        self.lgrObj.info("---------- Click on Mini-Cart & then View Cart button")
        CtlgPgObj.ClickCatalogPageButton('mini-cart')
        CtlgPgObj.ClickCatalogPageButton('view-cart')
        time.sleep(3)

        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)

        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj = NetAdjustmentPopUp(self.driver)

        # Adjustment Type = % Discount
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount','10')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("90") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Manual Adjustment (% Discount), Grand Total is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Manual Adjustment (% Discount), Grand Total is NOT correct ----------")
            assert False
            self.driver.close()

        # Adjustment Type = Discount Amount
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Discount Amount', '20')
        time.sleep(5)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("80") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Manual Adjustment (Discount Amount), Grand Total is correct ----------")
        else:
            self.lgrObj.info("---------- (FAILED): Manual Adjustment (Discount Amount), Grand Total is NOT correct ----------")
            assert False
            self.driver.close()

        # Adjustment Type = % Markup
        time.sleep(5)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('% Markup', '10')
        time.sleep(5)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("110") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (%Mark up), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (%Mark up), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Markup Amount
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Markup Amount', '20')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("120") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Markup Amount), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Markup Amount), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Base Price Override, When applied on Bundle, the Base Pice though on UI does not get
        # changed but takes the override value. It does not affect the Option base price nor apply any discount
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Base Price Override', '30')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("30") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Base Price Override), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Base Price Override), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Price Override. When applied on Bundle, the Net Price, Net Adj% gets updated.
        # The Base Price, Option Price of the Bundle does not get changed. Only the Net Price.
        # The the same proportion of discount gets applied on the Net Price of the Option too
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Price Override', '30')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("30") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Price Override), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Price Override), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Adjustment Type = Price Factor. When applied there will be no changed to Base Price, Option price
        # for bundle or option line. However the Net Price of bundle will get multiplied by the factor
        # That results in + Net % hike in Bunlde and that same % gets applied on option which increases it's net Price
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)
        NetAdjObj.SetAdjustmentTypeAndValue('Price Factor', '2')
        time.sleep(2)
        #self.lgrObj.info("---------- Click on Reprice button")

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]

        if str("200") in str(float(SlicedGrandTotal)):
                assert True
                self.lgrObj.info("---------- (PASSED): Manual Adjustment (Price Factor), Grand Total is correct ----------")
        else:
                self.lgrObj.info("---------- (FAILED): Manual Adjustment (Price Factor), Grand Total is NOT correct ----------")
                assert False
                self.driver.close()

        # Delete the Product & Add Product to test "Allow Manual Adjustment False at PLI"
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)

        self.lgrObj.info("---------- Go back to Catalog Page and the Prd to test Allow Manual Adj False at PLI")
        CartPgObj.ClickCartButtons('Add More Products')

        # Search and add product which is set to Allow Man Adj False
        PrdName2 = XLUtils.readData(self.file, 'TC_011', 3, 7)
        CtlgPgObj.SearchAndAddProduct('View Cart', PrdName2)

        self.lgrObj.info("---------- Click on Mini-Cart & then View Cart button")
        CtlgPgObj.ClickCatalogPageButton('mini-cart')
        CtlgPgObj.ClickCatalogPageButton('view-cart')
        time.sleep(3)

        self.lgrObj.info("---------- Click on Submit for Pricing (Async) button")
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        # Check Net Adjustment link is disabled for this product
        Result1=CartPgObj.IsEnalbedOrDisabled(PrdName2,'Net Adjustment %')
        print(Result1)

        if str("disabled") in str(Result1):
            self.lgrObj.info("---------- (PASSED): Net Adj. is disabled for Product with Allow Manual Adj False in PLI")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Net Adj. is NOT disabled for Product with Allow Manual Adj False in PLI")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart and delete the proposal")
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ---------- ")