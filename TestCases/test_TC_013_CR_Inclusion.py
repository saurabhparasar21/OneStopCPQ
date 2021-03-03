import pytest
import time

from pageObjects.AttributePage import AttributePage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.ConstRulePrompt import ConstRulePrompt
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.loginPage import loginPage
from pageObjects.AttributeOptionPage import AttributeOptionPage
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
    def test_CR_Inclusion_Classic(self,setup):
        self.lgrObj = Logger.logGen('TC_013_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_013_1: Bundle With Criteria (LI, ATTR) INCLUSION           ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_013', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_013', 1, 3)
        value = XLUtils.readData(self.file, 'TC_013', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_013', 1, 4)
        value = XLUtils.readData(self.file, 'TC_013', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_013', 1, 5)
        value = XLUtils.readData(self.file, 'TC_013', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_013', 1, 6)
        value = XLUtils.readData(self.file, 'TC_013', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_013', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName,2)
        CtlgPgObj.ConfigureProduct("Configure",PrdName)

        self.lgrObj.info("---------- Set Attribute to trigger Constraint rule")
        AttrPgObj = AttributePage(self.driver)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        Attr = XLUtils.readData(self.file, 'TC_013',2,8)
        AttrValue=XLUtils.readData(self.file, 'TC_013',3,8)
        print(AttrValue)
        AttrPgObj.SetAttribute("Picklist",Attr,AttrValue)

        self.lgrObj.info("---------- Verify Constraint rule message from Prompt")
        CRPromptObj = ConstRulePrompt(self.driver)
        ExpectMsg=XLUtils.readData(self.file, 'TC_013',2,9)
        MsgMatched=CRPromptObj.VerifyCRMessage(ExpectMsg)
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Prompt")
            CRPromptObj.ClickButton('Add to Bundle')
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Prompt")
            assert False
            self.driver.close()
        time.sleep(2)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        # Go to Product Options Tab
        AtrOptnPgObj=AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        self.lgrObj.info("---------- Verify Constraint rule message from Inclusion")
        # Verify CR Bundle to Option Inclusion Messages
        ExpectMsg2 = XLUtils.readData(self.file, 'TC_013', 2, 10)
        print("Expected Msg2 is: " + str(ExpectMsg2))

        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg2)
        print("Actual Msg2 is: "+str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Verify Constraint rule message from Inclusion Show Message")
        ExpectMsg3 = XLUtils.readData(self.file, 'TC_013', 2, 11)
        print("Expected Msg3 is: " + str(ExpectMsg3))
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg3)
        print("Actual Msg3 is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion Show Message")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion Show Message")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Select the Option Product and Verify Show Message disappears")
        OptnPrdName=XLUtils.readData(self.file, 'TC_013', 2, 12)
        AtrOptnPgObj.SelectOptionPrd(OptnPrdName)
        time.sleep(3)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg3)
        print("Actual Msg3 is: " + str(MsgMatched))
        if str(MsgMatched) == "False":
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion Show Message has disappeared")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion Show Message has NOT disappeared")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Verify Check on Finalization message")
        AtrOptnPgObj.ClickMiniCartButton('Finalize')
        # Wait for Pricing to complete in mini-cart
        AtrOptnPgObj.WaitForMiniCartPricingCalcToComplete()
        ChkOnFinzMsg = XLUtils.readData(self.file,'TC_013',2,13)
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ChkOnFinzMsg)

        print("Actual Msg3 is: " +str(MsgMatched))
        if str(MsgMatched) == "True":
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Check On Finalization Message displayed")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Check On Finalization Message NOT displayed")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_CR_Inclusion_Split(self,setup):
        self.lgrObj = Logger.logGen('TC_013_2')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_013_2: Bundle With Criteria (LI, ATTR) INCLUSION           ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_013', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_013', 1, 3)
        value = XLUtils.readData(self.file, 'TC_013', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_013', 1, 4)
        value = XLUtils.readData(self.file, 'TC_013', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_013', 1, 5)
        value = XLUtils.readData(self.file, 'TC_013', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_013', 1, 6)
        value = XLUtils.readData(self.file, 'TC_013', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_013', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName,2)
        CtlgPgObj.ConfigureProduct("Configure",PrdName)

        self.lgrObj.info("---------- Set Attribute to trigger Constraint rule")
        AttrPgObj = AttributePage(self.driver)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        Attr = XLUtils.readData(self.file, 'TC_013',2,8)
        AttrValue=XLUtils.readData(self.file, 'TC_013',3,8)
        print(AttrValue)
        AttrPgObj.SetAttribute("Picklist",Attr,AttrValue)

        self.lgrObj.info("---------- Verify Constraint rule message from Prompt")
        CRPromptObj = ConstRulePrompt(self.driver)
        ExpectMsg=XLUtils.readData(self.file, 'TC_013',2,9)
        MsgMatched=CRPromptObj.VerifyCRMessage(ExpectMsg)
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Prompt")
            CRPromptObj.ClickButton('Add to Bundle')
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Prompt")
            assert False
            self.driver.close()
        time.sleep(2)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        # Go to Product Options Tab
        AtrOptnPgObj=AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        self.lgrObj.info("---------- Verify Constraint rule message from Inclusion")
        # Verify CR Bundle to Option Inclusion Messages
        ExpectMsg2 = XLUtils.readData(self.file, 'TC_013', 2, 10)
        print("Expected Msg2 is: " + str(ExpectMsg2))

        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg2)
        print("Actual Msg2 is: "+str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Verify Constraint rule message from Inclusion Show Message")
        ExpectMsg3 = XLUtils.readData(self.file, 'TC_013', 2, 11)
        print("Expected Msg3 is: " + str(ExpectMsg3))
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg3)
        print("Actual Msg3 is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion Show Message")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion Show Message")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Select the Option Product and Verify Show Message disappears")
        OptnPrdName=XLUtils.readData(self.file, 'TC_013', 2, 12)
        AtrOptnPgObj.SelectOptionPrd(OptnPrdName)
        time.sleep(3)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg3)
        print("Actual Msg3 is: " + str(MsgMatched))
        if str(MsgMatched) == "False":
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion Show Message has disappeared")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion Show Message has NOT disappeared")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Verify Check on Finalization message")
        AtrOptnPgObj.ClickMiniCartButton('Finalize')
        # Wait for Pricing to complete in mini-cart
        AtrOptnPgObj.WaitForMiniCartPricingCalcToComplete()
        ChkOnFinzMsg = XLUtils.readData(self.file,'TC_013',2,13)
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ChkOnFinzMsg)

        print("Actual Msg3 is: " +str(MsgMatched))
        if str(MsgMatched) == "True":
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Check On Finalization Message displayed")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Check On Finalization Message NOT displayed")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_CR_Inclusion_Turbo(self,setup):
        self.lgrObj = Logger.logGen('TC_013_3')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("      TC_013_3: Bundle With Criteria (LI, ATTR) INCLUSION           ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_013', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_013', 1, 3)
        value = XLUtils.readData(self.file, 'TC_013', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_013', 1, 4)
        value = XLUtils.readData(self.file, 'TC_013', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_013', 1, 5)
        value = XLUtils.readData(self.file, 'TC_013', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_013', 1, 6)
        value = XLUtils.readData(self.file, 'TC_013', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Configure the Bundle")
        PrdName= XLUtils.readData(self.file, 'TC_013', 2, 7)
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName,2)
        CtlgPgObj.ConfigureProduct("Configure",PrdName)

        self.lgrObj.info("---------- Set Attribute to trigger Constraint rule")
        AttrPgObj = AttributePage(self.driver)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        Attr = XLUtils.readData(self.file, 'TC_013',2,8)
        AttrValue=XLUtils.readData(self.file, 'TC_013',3,8)
        print(AttrValue)
        AttrPgObj.SetAttribute("Picklist",Attr,AttrValue)

        self.lgrObj.info("---------- Verify Constraint rule message from Prompt")
        CRPromptObj = ConstRulePrompt(self.driver)
        ExpectMsg=XLUtils.readData(self.file, 'TC_013',2,9)
        MsgMatched=CRPromptObj.VerifyCRMessage(ExpectMsg)
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Prompt")
            CRPromptObj.ClickButton('Add to Bundle')
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Prompt")
            assert False
            self.driver.close()
        time.sleep(2)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        # Go to Product Options Tab
        AtrOptnPgObj=AttributeOptionPage(self.driver)
        AtrOptnPgObj.ClickOnTab('Product Options')
        time.sleep(2)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        self.lgrObj.info("---------- Verify Constraint rule message from Inclusion")
        # Verify CR Bundle to Option Inclusion Messages
        ExpectMsg2 = XLUtils.readData(self.file, 'TC_013', 2, 10)
        print("Expected Msg2 is: " + str(ExpectMsg2))

        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg2)
        print("Actual Msg2 is: "+str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Verify Constraint rule message from Inclusion Show Message")
        ExpectMsg3 = XLUtils.readData(self.file, 'TC_013', 2, 11)
        print("Expected Msg3 is: " + str(ExpectMsg3))
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg3)
        print("Actual Msg3 is: " + str(MsgMatched))
        if str(MsgMatched) == "True":
            assert True
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion Show Message")
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion Show Message")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Select the Option Product and Verify Show Message disappears")
        OptnPrdName=XLUtils.readData(self.file, 'TC_013', 2, 12)
        AtrOptnPgObj.SelectOptionPrd(OptnPrdName)
        time.sleep(3)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ExpectMsg3)
        print("Actual Msg3 is: " + str(MsgMatched))
        if str(MsgMatched) == "False":
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Inclusion Show Message has disappeared")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Inclusion Show Message has NOT disappeared")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Verify Check on Finalization message")
        AtrOptnPgObj.ClickMiniCartButton('Finalize')
        # Wait for Pricing to complete in mini-cart
        AtrOptnPgObj.WaitForMiniCartPricingCalcToComplete()
        ChkOnFinzMsg = XLUtils.readData(self.file,'TC_013',2,13)
        MsgMatched = AtrOptnPgObj.VerifyCRMessage(ChkOnFinzMsg)

        print("Actual Msg3 is: " +str(MsgMatched))
        if str(MsgMatched) == "True":
            self.lgrObj.info("---------- (PASSED): Bundle to Option CR Check On Finalization Message displayed")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Bundle to Option CR Check On Finalization Message NOT displayed")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Abandon the Cart")
        AtrOptnPgObj.AbandonCart()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()
