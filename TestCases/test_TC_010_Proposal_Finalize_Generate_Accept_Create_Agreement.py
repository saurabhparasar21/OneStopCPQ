import pytest
import time

from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.PresentProposalPage import PresentProposalPage
from pageObjects.loginPage import loginPage
from pageObjects.AgreementPage import AgreementPage
from pageObjects.GenerateProposalDocPage import GenerateProposalDocPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger

class Test_Proposal_To_Agreement_Flow:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    @pytest.mark.RegularPricing
    def test_Prop2Agrmnt_Classic(self, setup):
        self.lgrObj = Logger.logGen('TC_010_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("  TC_010_1: Proposal_To_Agreement flow (Reg Cart Normal Pricing   ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_010', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_010', 1, 4)
        value = XLUtils.readData(self.file, 'TC_010', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_010', 1, 5)
        value = XLUtils.readData(self.file, 'TC_010', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_010', 1, 6)
        value = XLUtils.readData(self.file, 'TC_010', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add the Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart',PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Finalize the Cart")
        CartPgObj.ClickCartButtons('Finalize')
        self.lgrObj.info("---------- Click on Related Tab, Check Configuration Status")

        time.sleep(5)
        PropsPageObj.ClickOnDetailPageTab('Related')
        ConfigSts=PropsPageObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal is Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal is NOT Finalized Successfully")
            assert False
            self.driver.close()
        PropsPageObj.ClickOnDetailPageTab('Details')
        self.lgrObj.info("---------- Generate Proposal Document")
        PropsPageObj.ClickProposalPageButton('Generate')


        GenPgObj=GenerateProposalDocPage(self.driver)
        Template=XLUtils.readData(self.file, 'TC_010', 2, 8)
        print("Template: "+str(Template))
        GenPgObj.SelectTemplate(Template)
        GenPgObj.ClickButton('Generate')

        # Check if Document gets generated or not
        TrOrFal=GenPgObj.IsDocGenerated()
        print(TrOrFal)

        if str(TrOrFal) >= str("1"):
            self.lgrObj.info("---------- (PASSED): Proposal Document generated successfully")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Document is NOT generated")
            assert False
            self.driver.close()
        # Return to Proposal
        GenPgObj.ClickButton('Return')

        # Verify if Approval Stage is updated to Generated
        Value=PropsPageObj.getFieldValue('Picklist','Approval Stage')
        if str(Value) == "Generated":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Generated")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Generated")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Present the Proposal")
        PropsPageObj.ClickProposalPageButton('Present')
        PrsntPropObj=PresentProposalPage(self.driver)
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PrsntPropObj.SelectAttachment(value)
        PrsntPropObj.ClickButton('Next')
        time.sleep(6)
        PrsntPropObj.SetTextBox('Additional','mnayak@conga.com')
        PrsntPropObj.ClickButton('Send')
        PrsntPropObj.DialogYesOrNo('Yes')
        # Verify if Approval Stage is updated to Presented
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Presented":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Presented")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Presented")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Accept the Proposal")
        PropsPageObj.ClickProposalPageButton('Accept')
        # Verify if Approval Stage is updated to Presented

        time.sleep(8)
        Value2 = PropsPageObj.getFieldValue('Picklist','Approval Stage')
        print(Value2)
        if str(Value2) == str("Accepted"):
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Accepted")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Accepted")
            assert False
            self.driver.close()

        # Create Agreement With Line Items
        self.lgrObj.info("---------- Click on Create Agreement With Line Items")
        PropsPageObj.ClickProposalPageButton('Create Agreement With Line Items')

        # Set up object for Agreement Object
        AgrmntPgObj=AgreementPage(self.driver)
        AgrmntPgObj.AgrmntRecTypPageButton('Continue')
        # Check Agreement Name
        AgrmntName=AgrmntPgObj.getFieldValue('Text','Agreement Name')
        if AgrmntName == value:
            self.lgrObj.info("---------- (PASSED): Agreement creation from Proposal is successful **********")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Agreement creation from Proposal is failed **********")
            assert False
            self.driver.close()

        # Go to Related Tab and Verify the status of Configuration
        AgrmntPgObj.ClickOnDetailPageTab('Related')
        ConfigSts = AgrmntPgObj.CheckConfigurationStatus('Saved')
        if str(ConfigSts) == str('Saved'):
            assert True
            self.lgrObj.info("---------- (PASSED): Agreement is Saved Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Agreement is NOT Saved Successfully")
            assert False
            self.driver.close()

        # Check if correct no. of Agreement lines are created
        NoOfAgmntLns=AgrmntPgObj.CountNoOfAgrmntLines()
        print(NoOfAgmntLns)
        print("No of Agreement lines: "+str(NoOfAgmntLns))
        if str(NoOfAgmntLns) == str("(1)"):
            assert True
            self.lgrObj.info("---------- (PASSED): Correct No. of Agreement line(s) created")
        else:
            self.lgrObj.info("---------- (FAILED): In-Correct No. of Agreement line(s) created")
            assert False
            self.driver.close()

        # Delete the Agreement
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Agreement")
        AgrmntPgObj.ClickAgreementPageButton('Delete')
        time.sleep(4)
        AgrmntPgObj.DialogAcceptOrCancel('Delete')
        time.sleep(4)

        # Delete the Proposal
        self.lgrObj.info("---------- Delete the Proposal")
        time.sleep(4)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        time.sleep(4)
        self.driver.close()
        self.lgrObj.info("---------- END ----------")

    @pytest.mark.TurboPricing
    def test_Prop2Agrmnt_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_010_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("  TC_010_2: Proposal_To_Agreement flow (Reg Cart Turbo Pricing   ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_010', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_010', 1, 4)
        value = XLUtils.readData(self.file, 'TC_010', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_010', 1, 5)
        value = XLUtils.readData(self.file, 'TC_010', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_010', 1, 6)
        value = XLUtils.readData(self.file, 'TC_010', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add the Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        time.sleep(2)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(2)
        self.lgrObj.info("---------- Finalize the Cart")
        CartPgObj.ClickCartButtons('Finalize')
        self.lgrObj.info("---------- Click on Related Tab, Check Configuration Status")

        time.sleep(5)
        PropsPageObj.ClickOnDetailPageTab('Related')
        ConfigSts = PropsPageObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal is Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal is NOT Finalized Successfully")
            assert False
            self.driver.close()
        PropsPageObj.ClickOnDetailPageTab('Details')
        self.lgrObj.info("---------- Generate Proposal Document")
        PropsPageObj.ClickProposalPageButton('Generate')

        GenPgObj = GenerateProposalDocPage(self.driver)
        Template = XLUtils.readData(self.file, 'TC_010', 2, 8)
        print("Template: " + str(Template))
        GenPgObj.SelectTemplate(Template)
        GenPgObj.ClickButton('Generate')

        # Check if Document gets generated or not
        TrOrFal = GenPgObj.IsDocGenerated()
        print(TrOrFal)

        if str(TrOrFal) >= str("1"):
            self.lgrObj.info("---------- (PASSED): Proposal Document generated successfully")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Document is NOT generated")
            assert False
            self.driver.close()
        # Return to Proposal
        GenPgObj.ClickButton('Return')

        # Verify if Approval Stage is updated to Generated
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Generated":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Generated")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Generated")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Present the Proposal")
        PropsPageObj.ClickProposalPageButton('Present')
        PrsntPropObj = PresentProposalPage(self.driver)
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PrsntPropObj.SelectAttachment(value)
        PrsntPropObj.ClickButton('Next')
        time.sleep(6)
        PrsntPropObj.SetTextBox('Additional', 'mnayak@conga.com')
        PrsntPropObj.ClickButton('Send')
        PrsntPropObj.DialogYesOrNo('Yes')
        # Verify if Approval Stage is updated to Presented
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Presented":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Presented")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Presented")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Accept the Proposal")
        PropsPageObj.ClickProposalPageButton('Accept')
        # Verify if Approval Stage is updated to Presented

        time.sleep(8)
        Value1 = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        print(Value1)
        if str(Value1) == str("Accepted"):
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Accepted")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Accepted")
            assert False
            self.driver.close()

        # Create Agreement With Line Items
        self.lgrObj.info("---------- Click on Create Agreement With Line Items")
        PropsPageObj.ClickProposalPageButton('Create Agreement With Line Items')

        # Set up object for Agreement Object
        AgrmntPgObj = AgreementPage(self.driver)
        AgrmntPgObj.AgrmntRecTypPageButton('Continue')
        # Check Agreement Name
        AgrmntName = AgrmntPgObj.getFieldValue('Text', 'Agreement Name')
        if AgrmntName == value:
            self.lgrObj.info("---------- (PASSED): Agreement creation from Proposal is successful **********")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Agreement creation from Proposal is failed **********")
            assert False
            self.driver.close()

        # Go to Related Tab and Verify the status of Configuration
        AgrmntPgObj.ClickOnDetailPageTab('Related')
        ConfigSts = AgrmntPgObj.CheckConfigurationStatus('Saved')
        if str(ConfigSts) == str('Saved'):
            assert True
            self.lgrObj.info("---------- (PASSED): Agreement is Saved Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Agreement is NOT Saved Successfully")
            assert False
            self.driver.close()

        # Check if correct no. of Agreement lines are created
        NoOfAgmntLns = AgrmntPgObj.CountNoOfAgrmntLines()
        print(NoOfAgmntLns)
        print("No of Agreement lines: " + str(NoOfAgmntLns))
        if str(NoOfAgmntLns) == str("(1)"):
            assert True
            self.lgrObj.info("---------- (PASSED): Correct No. of Agreement line(s) created")
        else:
            self.lgrObj.info("---------- (FAILED): In-Correct No. of Agreement line(s) created")
            assert False
            self.driver.close()

        # Delete the Agreement
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Agreement")
        AgrmntPgObj.ClickAgreementPageButton('Delete')
        time.sleep(4)
        AgrmntPgObj.DialogAcceptOrCancel('Delete')
        time.sleep(4)

        # Delete the Proposal
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Proposal")
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ----------")

    @pytest.mark.Split
    def test_Prop2Agrmnt_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_010_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("  TC_010_3: Proposal_To_Agreement flow Split Cart Async Pricing  ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_010', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_010', 1, 4)
        value = XLUtils.readData(self.file, 'TC_010', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_010', 1, 5)
        value = XLUtils.readData(self.file, 'TC_010', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_010', 1, 6)
        value = XLUtils.readData(self.file, 'TC_010', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add the Product to Cart")
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
        time.sleep(3)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Finalize the Cart")
        CartPgObj.ClickCartButtons('Finalize')
        # Click OK in the Dialog
        CartPgObj.FinalizeDialog('OK')

        self.lgrObj.info("---------- Click on Related Tab, Check Configuration Status")
        time.sleep(6)
        PropsPageObj.ClickOnDetailPageTab('Related')
        ConfigSts = PropsPageObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal is Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal is NOT Finalized Successfully")
            assert False
            self.driver.close()
        PropsPageObj.ClickOnDetailPageTab('Details')
        self.lgrObj.info("---------- Generate Proposal Document")
        PropsPageObj.ClickProposalPageButton('Generate')

        GenPgObj = GenerateProposalDocPage(self.driver)
        Template = XLUtils.readData(self.file, 'TC_010', 2, 8)
        print("Template: " + str(Template))
        GenPgObj.SelectTemplate(Template)
        GenPgObj.ClickButton('Generate')

        # Check if Document gets generated or not
        TrOrFal = GenPgObj.IsDocGenerated()
        print(TrOrFal)

        if str(TrOrFal) >= str("1"):
            self.lgrObj.info("---------- (PASSED): Proposal Document generated successfully")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Document is NOT generated")
            assert False
            self.driver.close()
        # Return to Proposal
        GenPgObj.ClickButton('Return')

        # Verify if Approval Stage is updated to Generated
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Generated":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Generated")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Generated")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Present the Proposal")
        PropsPageObj.ClickProposalPageButton('Present')
        PrsntPropObj = PresentProposalPage(self.driver)
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PrsntPropObj.SelectAttachment(value)
        PrsntPropObj.ClickButton('Next')
        time.sleep(6)
        PrsntPropObj.SetTextBox('Additional', 'mnayak@conga.com')
        PrsntPropObj.ClickButton('Send')
        PrsntPropObj.DialogYesOrNo('Yes')
        # Verify if Approval Stage is updated to Presented
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Presented":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Presented")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Presented")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Accept the Proposal")
        PropsPageObj.ClickProposalPageButton('Accept')
        # Verify if Approval Stage is updated to Presented
        time.sleep(8)
        Value1 = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        print(Value1)
        if str(Value1) == str("Accepted"):
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Accepted")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Accepted")
            assert False
            self.driver.close()

        # Create Agreement With Line Items
        self.lgrObj.info("---------- Click on Create Agreement With Line Items")
        PropsPageObj.ClickProposalPageButton('Create Agreement With Line Items')

        # Set up object for Agreement Object
        AgrmntPgObj = AgreementPage(self.driver)
        AgrmntPgObj.AgrmntRecTypPageButton('Continue')
        # Check Agreement Name
        AgrmntName = AgrmntPgObj.getFieldValue('Text', 'Agreement Name')
        if AgrmntName == value:
            self.lgrObj.info("---------- (PASSED): Agreement creation from Proposal is successful **********")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Agreement creation from Proposal is failed **********")
            assert False
            self.driver.close()

        # Go to Related Tab and Verify the status of Configuration
        time.sleep(7)
        AgrmntPgObj.ClickOnDetailPageTab('Related')
        ConfigSts = AgrmntPgObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Agreement is Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Agreement is NOT Finalized Successfully")
            assert False
            self.driver.close()


        # Check if correct no. of Agreement lines are created
        NoOfAgmntLns = AgrmntPgObj.CountNoOfAgrmntLines()
        print(NoOfAgmntLns)
        print("No of Agreement lines: " + str(NoOfAgmntLns))
        if str(NoOfAgmntLns) == str("(1)"):
            assert True
            self.lgrObj.info("---------- (PASSED): Correct No. of Agreement line(s) created")
        else:
            self.lgrObj.info("---------- (FAILED): In-Correct No. of Agreement line(s) created")
            assert False
            self.driver.close()

        # Delete the Agreement
        self.lgrObj.info("---------- Delete the Agreement")
        time.sleep(4)
        AgrmntPgObj.ClickAgreementPageButton('Delete')
        time.sleep(4)
        AgrmntPgObj.DialogAcceptOrCancel('Delete')
        time.sleep(4)

        # Delete the Proposal
        self.lgrObj.info("---------- Delete the Proposal")
        time.sleep(4)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ----------")

    @pytest.mark.EnterpriseRegularPricing
    def test_Prop2Agrmnt_EnterpriseClassic(self, setup):
        self.lgrObj = Logger.logGen('TC_010_4')
        self.lgrObj.info("######################################################################")
        self.lgrObj.info("  TC_010_4: Proposal_To_Agreement flow (Enterprise Cart Reg Pricing   ")
        self.lgrObj.info("######################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_010', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile','Enterprise')

        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_010', 1, 4)
        value = XLUtils.readData(self.file, 'TC_010', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_010', 1, 5)
        value = XLUtils.readData(self.file, 'TC_010', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_010', 1, 6)
        value = XLUtils.readData(self.file, 'TC_010', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add the Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Finalize the Cart")
        CartPgObj.ClickCartButtons('Finalize')
        self.lgrObj.info("---------- Click on Related Tab, Check Configuration Status")

        time.sleep(5)
        PropsPageObj.ClickOnDetailPageTab('Related')
        ConfigSts = PropsPageObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal is Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal is NOT Finalized Successfully")
            assert False
            self.driver.close()
        PropsPageObj.ClickOnDetailPageTab('Details')
        self.lgrObj.info("---------- Generate Proposal Document")
        PropsPageObj.ClickProposalPageButton('Generate')

        GenPgObj = GenerateProposalDocPage(self.driver)
        Template = XLUtils.readData(self.file, 'TC_010', 2, 8)
        print("Template: " + str(Template))
        GenPgObj.SelectTemplate(Template)
        GenPgObj.ClickButton('Generate')

        # Check if Document gets generated or not
        TrOrFal = GenPgObj.IsDocGenerated()
        print(TrOrFal)

        if str(TrOrFal) >= str("1"):
            self.lgrObj.info("---------- (PASSED): Proposal Document generated successfully")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Document is NOT generated")
            assert False
            self.driver.close()
        # Return to Proposal
        GenPgObj.ClickButton('Return')

        # Verify if Approval Stage is updated to Generated
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Generated":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Generated")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Generated")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Present the Proposal")
        PropsPageObj.ClickProposalPageButton('Present')
        PrsntPropObj = PresentProposalPage(self.driver)
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PrsntPropObj.SelectAttachment(value)
        PrsntPropObj.ClickButton('Next')
        time.sleep(6)
        PrsntPropObj.SetTextBox('Additional', 'mnayak@conga.com')
        PrsntPropObj.ClickButton('Send')
        PrsntPropObj.DialogYesOrNo('Yes')
        # Verify if Approval Stage is updated to Presented
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Presented":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Presented")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Presented")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Accept the Proposal")
        PropsPageObj.ClickProposalPageButton('Accept')
        # Verify if Approval Stage is updated to Presented
        time.sleep(8)
        Value1 = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        print(Value1)
        if str(Value1) == str("Accepted"):
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Accepted")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Accepted")
            assert False
            self.driver.close()

        # Create Agreement With Line Items
        self.lgrObj.info("---------- Click on Create Agreement With Line Items")
        PropsPageObj.ClickProposalPageButton('Create Agreement With Line Items')

        # Set up object for Agreement Object
        AgrmntPgObj = AgreementPage(self.driver)
        AgrmntPgObj.AgrmntRecTypPageButton('Continue')
        # Check Agreement Name
        AgrmntName = AgrmntPgObj.getFieldValue('Text', 'Agreement Name')
        if AgrmntName == value:
            self.lgrObj.info("---------- (PASSED): Agreement creation from Proposal is successful **********")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Agreement creation from Proposal is failed **********")
            assert False
            self.driver.close()

        # Go to Related Tab and Verify the status of Configuration
        AgrmntPgObj.ClickOnDetailPageTab('Related')
        ConfigSts = AgrmntPgObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Agreement is auto Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Agreement is NOT auto Finalized Successfully")
            assert False
            self.driver.close()

        # Check if correct no. of Agreement lines are created
        NoOfAgmntLns = AgrmntPgObj.CountNoOfAgrmntLines()
        print(NoOfAgmntLns)
        print("No of Agreement lines: " + str(NoOfAgmntLns))
        if str(NoOfAgmntLns) == str("(1)"):
            assert True
            self.lgrObj.info("---------- (PASSED): Correct No. of Agreement line(s) created")
        else:
            self.lgrObj.info("---------- (FAILED): In-Correct No. of Agreement line(s) created")
            assert False
            self.driver.close()

        # Delete the Agreement
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Agreement")
        AgrmntPgObj.ClickAgreementPageButton('Delete')
        time.sleep(4)
        AgrmntPgObj.DialogAcceptOrCancel('Delete')
        time.sleep(4)

        # Delete the Proposal
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Proposal")
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ----------")

    @pytest.mark.TurboPricing
    def test_Prop2Agrmnt_EnterpriseTurbo(self, setup):
        self.lgrObj = Logger.logGen('TC_010_5')
        self.lgrObj.info("########################################################################")
        self.lgrObj.info("  TC_010_5: Proposal_To_Agreement flow (Enterprise Cart Turbo Pricing   ")
        self.lgrObj.info("########################################################################")

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
        appToSearchFor = XLUtils.readData(self.file, 'TC_010', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Set QTC Profile
        PropsPageObj.SetProposalField('QTC Profile', 'Enterprise')

        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_010', 1, 4)
        value = XLUtils.readData(self.file, 'TC_010', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_010', 1, 5)
        value = XLUtils.readData(self.file, 'TC_010', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_010', 1, 6)
        value = XLUtils.readData(self.file, 'TC_010', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_010', 2, 7)
        self.lgrObj.info("---------- Search and add the Product to Cart")
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Finalize the Cart")
        time.sleep(2)
        CartPgObj.ClickCartButtons('Finalize')
        self.lgrObj.info("---------- Click on Related Tab, Check Configuration Status")

        time.sleep(5)
        PropsPageObj.ClickOnDetailPageTab('Related')
        ConfigSts = PropsPageObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Proposal is Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Proposal is NOT Finalized Successfully")
            assert False
            self.driver.close()
        PropsPageObj.ClickOnDetailPageTab('Details')
        self.lgrObj.info("---------- Generate Proposal Document")
        PropsPageObj.ClickProposalPageButton('Generate')

        GenPgObj = GenerateProposalDocPage(self.driver)
        Template = XLUtils.readData(self.file, 'TC_010', 2, 8)
        print("Template: " + str(Template))
        GenPgObj.SelectTemplate(Template)
        GenPgObj.ClickButton('Generate')

        # Check if Document gets generated or not
        TrOrFal = GenPgObj.IsDocGenerated()
        print(TrOrFal)

        if str(TrOrFal) >= str("1"):
            self.lgrObj.info("---------- (PASSED): Proposal Document generated successfully")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Proposal Document is NOT generated")
            assert False
            self.driver.close()
        # Return to Proposal
        GenPgObj.ClickButton('Return')

        # Verify if Approval Stage is updated to Generated
        time.sleep(4)
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Generated":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Generated")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Generated")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Present the Proposal")
        PropsPageObj.ClickProposalPageButton('Present')
        PrsntPropObj = PresentProposalPage(self.driver)
        label = XLUtils.readData(self.file, 'TC_010', 1, 3)
        value = XLUtils.readData(self.file, 'TC_010', 2, 3)
        PrsntPropObj.SelectAttachment(value)
        PrsntPropObj.ClickButton('Next')
        time.sleep(6)
        PrsntPropObj.SetTextBox('Additional', 'mnayak@conga.com')
        PrsntPropObj.ClickButton('Send')
        PrsntPropObj.DialogYesOrNo('Yes')
        # Verify if Approval Stage is updated to Presented
        Value = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        if str(Value) == "Presented":
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Presented")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Presented")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Accept the Proposal")
        PropsPageObj.ClickProposalPageButton('Accept')
        # Verify if Approval Stage is updated to Presented

        time.sleep(12)
        Value1 = PropsPageObj.getFieldValue('Picklist', 'Approval Stage')
        print(Value1)
        if str(Value1) == str("Accepted"):
            self.lgrObj.info("---------- (PASSED): Approval Stage is correctly updated to Accepted")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Approval Stage is NOT updated to Accepted")
            assert False
            self.driver.close()

        # Create Agreement With Line Items
        self.lgrObj.info("---------- Click on Create Agreement With Line Items")
        PropsPageObj.ClickProposalPageButton('Create Agreement With Line Items')

        # Set up object for Agreement Object
        AgrmntPgObj = AgreementPage(self.driver)
        AgrmntPgObj.AgrmntRecTypPageButton('Continue')
        # Check Agreement Name
        AgrmntName = AgrmntPgObj.getFieldValue('Text', 'Agreement Name')
        if AgrmntName == value:
            self.lgrObj.info("---------- (PASSED): Agreement creation from Proposal is successful **********")
            assert True
        else:
            self.lgrObj.info("---------- (FAILED): Agreement creation from Proposal is failed **********")
            assert False
            self.driver.close()

        # Go to Related Tab and Verify the status of Configuration
        AgrmntPgObj.ClickOnDetailPageTab('Related')
        ConfigSts = AgrmntPgObj.CheckConfigurationStatus('Finalized')
        if str(ConfigSts) == str('Finalized'):
            assert True
            self.lgrObj.info("---------- (PASSED): Agreement is auto Finalized Successfully")
        else:
            self.lgrObj.info("---------- (FAILED): Agreement is NOT auto Finalized Successfully")
            assert False
            self.driver.close()

        # Check if correct no. of Agreement lines are created
        NoOfAgmntLns = AgrmntPgObj.CountNoOfAgrmntLines()
        print(NoOfAgmntLns)
        print("No of Agreement lines: " + str(NoOfAgmntLns))
        if str(NoOfAgmntLns) == str("(1)"):
            assert True
            self.lgrObj.info("---------- (PASSED): Correct No. of Agreement line(s) created")
        else:
            self.lgrObj.info("---------- (FAILED): In-Correct No. of Agreement line(s) created")
            assert False
            self.driver.close()

        # Delete the Agreement
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Agreement")
        AgrmntPgObj.ClickAgreementPageButton('Delete')
        time.sleep(4)
        AgrmntPgObj.DialogAcceptOrCancel('Delete')
        time.sleep(4)

        # Delete the Proposal
        time.sleep(4)
        self.lgrObj.info("---------- Delete the Proposal")
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.driver.close()
        self.lgrObj.info("---------- END ----------")













