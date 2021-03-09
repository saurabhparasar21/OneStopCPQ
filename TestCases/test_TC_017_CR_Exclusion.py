import pytest
import time

from pageObjects.AttributePage import AttributePage
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
    def test_CR_Exclusion_Disable_Selection_Classic(self,setup):
        self.lgrObj = Logger.logGen('TC_017_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_1: B to O and O to O CR Exclusion Disable Selection    ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName,3)
        CtlgPgObj.ConfigureProduct("Configure",PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1= XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Check if the Option Prd in Bundle to Option scenario s disabled
        Actual=OptnPgObj.IsOptionEnableOrDisable(OptionPrd1)
        print("Actual result is: "+str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option Disable Selection is successful")
            assert False
            self.driver.close()

        # Select the Option Product and check Option to Option disable selection
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        # Set desired Option Qty that will trigger the constraint rule
        OptnPgObj.SetOptionPrdQty(OptionPrd2,3)
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd3)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option Disable Selection is successful")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_CR_Exclusion_Disable_Selection_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_017_2')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_2: B to O and O to O CR Exclusion Disable Selection    ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 3)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Check if the Option Prd in Bundle to Option scenario s disabled
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd1)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option Disable Selection is successful")
            assert False
            self.driver.close()

        # Select the Option Product and check Option to Option disable selection
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        # Set desired Option Qty that will trigger the constraint rule
        OptnPgObj.SetOptionPrdQty(OptionPrd2, 3)
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd3)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option Disable Selection is successful")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_CR_Exclusion_Disable_Selection_TP(self, setup):
        self.lgrObj = Logger.logGen('TC_017_3')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_3: B to O and O to O CR Exclusion Disable Selection    ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (TP)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 3)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Check if the Option Prd in Bundle to Option scenario s disabled
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd1)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option Disable Selection is successful")
            assert False
            self.driver.close()

        # Select the Option Product and check Option to Option disable selection
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        # Set desired Option Qty that will trigger the constraint rule
        OptnPgObj.SetOptionPrdQty(OptionPrd2, 3)
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd3)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option Disable Selection is successful")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_CR_Exclusion_Disable_Selection_TC(self, setup):
        self.lgrObj = Logger.logGen('TC_017_3.2')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_3.2: B to O and O to O CR Exclusion Disable Selection    ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020(TC)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 3)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Check if the Option Prd in Bundle to Option scenario s disabled
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd1)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option Disable Selection is successful")
            assert False
            self.driver.close()

        # Select the Option Product and check Option to Option disable selection
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        # Set desired Option Qty that will trigger the constraint rule
        OptnPgObj.SetOptionPrdQty(OptionPrd2, 3)
        Actual = OptnPgObj.IsOptionEnableOrDisable(OptionPrd3)
        print("Actual result is: " + str(Actual))

        if Actual == str('true'):
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option Disable Selection is successful")
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option Disable Selection is successful")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.RegularPricing
    def test_CR_Exclusion_Prompt_Selection_Classic(self, setup):
        self.lgrObj = Logger.logGen('TC_017_4')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_4: B to O and O to O CR Exclusion Prompt               ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 4)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Select the Option Product and check Bundle to Option prompt
        time.sleep(5)
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd1)
        # Set up CR Prompt object
        CRPromptObj = ConstRulePrompt(self.driver)
        B2OExclExpctMsg=XLUtils.readData(self.file, 'TC_017', 3, 8)
        print("Expected Message is: "+str(B2OExclExpctMsg))
        time.sleep(5)
        MsgMatched=CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: "+str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked=OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd1)
        print("Checked is: "+str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        # Check Option to Option Exclusion Prompt Scenario
        OptnPgObj.SelectOptionProd(OptionPrd2)
        OptnPgObj.SetOptionPrdQty(OptionPrd2,4)
        OptnPgObj.SelectOptionProd(OptionPrd3)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 9)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(5)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd3)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_CR_Exclusion_Prompt_Selection_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_017_5')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_5: B to O and O to O CR Exclusion Prompt               ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 4)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Select the Option Product and check Bundle to Option prompt
        time.sleep(5)
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)
        # Set up CR Prompt object
        CRPromptObj = ConstRulePrompt(self.driver)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 8)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(5)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd1)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        # Check Option to Option Exclusion Prompt Scenario
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        OptnPgObj.SetOptionPrdQty(OptionPrd2, 4)
        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 9)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(5)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd3)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_CR_Exclusion_Prompt_Selection_TP(self, setup):
        self.lgrObj = Logger.logGen('TC_017_6')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_6: B to O and O to O CR Exclusion Prompt               ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (TP)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 4)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Select the Option Product and check Bundle to Option prompt
        time.sleep(5)
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)
        # Set up CR Prompt object
        CRPromptObj = ConstRulePrompt(self.driver)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 8)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(5)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd1)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        # Check Option to Option Exclusion Prompt Scenario
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        OptnPgObj.SetOptionPrdQty(OptionPrd2, 4)
        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 9)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(5)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd3)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboConfig
    def test_CR_Exclusion_Prompt_Selection_TC(self, setup):
        self.lgrObj = Logger.logGen('TC_017_7')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_017_7: B to O and O to O CR Exclusion Prompt               ")
        self.lgrObj.info("####################################################################")

        self.driver = setup
        print("Test")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_017', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_017', 1, 3)
        value = XLUtils.readData(self.file, 'TC_017', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_017', 1, 4)
        value = XLUtils.readData(self.file, 'TC_017', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_017', 1, 5)
        value = XLUtils.readData(self.file, 'TC_017', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_017', 1, 6)
        value = XLUtils.readData(self.file, 'TC_017', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020(TC)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName = XLUtils.readData(self.file, 'TC_017', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 4)
        CtlgPgObj.ConfigureProduct("Configure", PrdName)

        # Go to Product Options Tab
        AtrOptnPgObj = AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)

        OptnPgObj = OptionPage(self.driver)
        OptionPrd1 = XLUtils.readData(self.file, 'TC_017', 2, 8)
        OptionPrd2 = XLUtils.readData(self.file, 'TC_017', 2, 9)
        OptionPrd3 = XLUtils.readData(self.file, 'TC_017', 2, 10)

        # Select the Option Product and check Bundle to Option prompt
        time.sleep(6)
        OptnPgObj.SearchOption(OptionPrd1)
        OptnPgObj.SelectOptionProd(OptionPrd1)
        time.sleep(6)
        # Set up CR Prompt object
        CRPromptObj = ConstRulePrompt(self.driver)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 8)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(2)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
            time.sleep(4)
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd1)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        # Check Option to Option Exclusion Prompt Scenario
        OptnPgObj.SearchOption(OptionPrd2)
        OptnPgObj.SetOptionPrdQty(OptionPrd2, 4)
        OptnPgObj.SelectOptionProd(OptionPrd2)
        time.sleep(4)

        OptnPgObj.SearchOption(OptionPrd3)
        OptnPgObj.SelectOptionProd(OptionPrd3)
        B2OExclExpctMsg = XLUtils.readData(self.file, 'TC_017', 3, 9)
        print("Expected Message is: " + str(B2OExclExpctMsg))
        time.sleep(3)
        MsgMatched = CRPromptObj.VerifyCRMessage(B2OExclExpctMsg)
        print("Returned message is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Option to Option CR Exclusion Prompt Message Matched")
            CRPromptObj.ClickButton('Remove')
            time.sleep(6)
        else:
            self.lgrObj.info("---------- (FAILED): Option to Option CR Exclusion Prompt Message doesn't Match")
            assert False
            self.driver.close()

        # Check the Option Prd is un-checked
        Checked = OptnPgObj.IsOptionPrdCheckedOrUnChecked(OptionPrd3)
        print("Checked is: " + str(Checked))
        if str(Checked) == "None":
            assert True
            self.lgrObj.info("---------- (PASSED): Option Prd has been unchecked by CR prompt remove action")
        else:
            self.lgrObj.info("---------- (FAILED): Option Prd has not been unchecked by CR prompt remove action")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        time.sleep(5)
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()