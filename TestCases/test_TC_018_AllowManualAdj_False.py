import pytest
import time

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


class Test_ConstRule_Exclusion:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Step:04 Set-up Test Scenario. Pass the driver through...
    @pytest.mark.RegularPricing
    def test_AllowManualAdj_False_Classic(self,setup):
        self.lgrObj = Logger.logGen('TC_018_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_018_1: B to O and B to Sub>O Allow manual Adj False        ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_018', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_018', 1, 3)
        value = XLUtils.readData(self.file, 'TC_018', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_018', 1, 4)
        value = XLUtils.readData(self.file, 'TC_018', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_018', 1, 5)
        value = XLUtils.readData(self.file, 'TC_018', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_018', 1, 6)
        value = XLUtils.readData(self.file, 'TC_018', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_018', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.ConfigureProduct("Configure",PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1= XLUtils.readData(self.file, 'TC_018', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_018', 3, 8)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_018', 4, 8)

        # Select the Option Product
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)

        # Wait for Pricing to Complete
        OptnPgObj.OptnPageWaitForPricingToComplete()
        OptnPgObj.ClickOnButton("GoToPricing")
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        CartPgObj.ExpandAllIcon()

        # Check if the Net Adjustment is disabled for the Option product
        EnabledDisabled=CartPgObj.IsEnalbedOrDisabled(OptionPrd1,'Net Adjustment %')

        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product"+OptionPrd1)
        else:
            self.lgrObj.info("---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd1)
            assert False
            self.driver.close()

        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd3, 'Net Adjustment %')
        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product"+OptionPrd3)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product"+OptionPrd3)
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.RegularPricing
    def test_AllowManualAdj_False_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_018_2')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_018_2: B to O and B to Sub>O Allow manual Adj False        ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_018', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_018', 1, 3)
        value = XLUtils.readData(self.file, 'TC_018', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_018', 1, 4)
        value = XLUtils.readData(self.file, 'TC_018', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_018', 1, 5)
        value = XLUtils.readData(self.file, 'TC_018', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_018', 1, 6)
        value = XLUtils.readData(self.file, 'TC_018', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_018', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_018', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_018', 3, 8)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_018', 4, 8)

        # Select the Option Product
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)

        # Wait for Pricing to Complete
        OptnPgObj.OptnPageWaitForPricingToComplete()
        OptnPgObj.ClickOnButton("GoToPricing")
        CartPgObj = CartPage(self.driver)
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(3)
        CartPgObj.ExpandAllIcon()

        # Check if the Net Adjustment is disabled for the Option product
        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd1, 'Net Adjustment %')

        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product" + OptionPrd1)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd1)
            assert False
            self.driver.close()

        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd3, 'Net Adjustment %')
        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product" + OptionPrd3)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd3)
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_AllowManualAdj_False_TP(self, setup):
        self.lgrObj = Logger.logGen('TC_018_3')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_018_3: B to O and B to Sub>O Allow manual Adj False        ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_018', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_018', 1, 3)
        value = XLUtils.readData(self.file, 'TC_018', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_018', 1, 4)
        value = XLUtils.readData(self.file, 'TC_018', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_018', 1, 5)
        value = XLUtils.readData(self.file, 'TC_018', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_018', 1, 6)
        value = XLUtils.readData(self.file, 'TC_018', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (TP)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_018', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_018', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_018', 3, 8)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_018', 4, 8)

        # Select the Option Product
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)

        # Wait for Pricing to Complete
        OptnPgObj.OptnPageWaitForPricingToComplete()
        OptnPgObj.ClickOnButton("GoToPricing")
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        CartPgObj.ExpandAllIcon()

        # Check if the Net Adjustment is disabled for the Option product
        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd1, 'Net Adjustment %')

        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product" + OptionPrd1)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd1)
            assert False
            self.driver.close()

        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd3, 'Net Adjustment %')
        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product" + OptionPrd3)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd3)
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboConfig
    def test_AllowManualAdj_False_TC(self, setup):
        self.lgrObj = Logger.logGen('TC_018_4')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_018_4: B to O and B to Sub>O Allow manual Adj False        ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_018', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_018', 1, 3)
        value = XLUtils.readData(self.file, 'TC_018', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_018', 1, 4)
        value = XLUtils.readData(self.file, 'TC_018', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_018', 1, 5)
        value = XLUtils.readData(self.file, 'TC_018', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_018', 1, 6)
        value = XLUtils.readData(self.file, 'TC_018', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020(TC)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_018', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_018', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_018', 3, 8)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_018', 4, 8)

        # Select the Option Product
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)

        time.sleep(3)
        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)

        # Wait for Pricing to Complete
        OptnPgObj.OptnPageWaitForPricingToComplete()
        OptnPgObj.ClickOnButton("GoToPricing")
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        CartPgObj.ExpandAllIcon()

        # Check if the Net Adjustment is disabled for the Option product
        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd1, 'Net Adjustment %')

        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product" + OptionPrd1)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd1)
            assert False
            self.driver.close()

        EnabledDisabled = CartPgObj.IsEnalbedOrDisabled(OptionPrd3, 'Net Adjustment %')
        if "disabled" in str(EnabledDisabled):
            assert True
            self.lgrObj.info("---------- (PASSED): Net Adjustment % is disabled for the option product" + OptionPrd3)
        else:
            self.lgrObj.info(
                "---------- (FAILED): Net Adjustment % is NOT disabled for the option product" + OptionPrd3)
            assert False
            self.driver.close()

        # Abandon the Cart and delete it
        CartPgObj.ClickCartButtons('Abandon')
        CartPgObj.AbandonDialog('OK')
        time.sleep(7)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()





