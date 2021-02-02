import allure
import pytest
# Import Page Objects
from allure_commons.types import AttachmentType

from pageObjects.loginPage import loginPage
from pageObjects.OpportunitiesPage import OpportunityPage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.HomeTab import HomePage
from utilities.Logger import Logger
from utilities.readProperties import ReadConfig
from utilities import XLUtils
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#Make sure Class name contains Test keyword
class Test_CreateProposal:
    # Get Common Values from Configuration file
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Add Marker
    @pytest.mark.RegularPricing
    # Define method to verify Proposal Creation from Opportunity
    def test_CreateProposalFromOppty(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_002_1')
        self.driver=setup
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("           TC_002_1: Test Proposal Creation from Opportunity     ")
        self.lgrObj.info("#################################################################")
        self.driver.get(self.baseUrl)

        # Set up object for Login page object class
        self.lgnObj=loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()

        # Set up object for Home page object class
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        #self.lgrObj.info("Home Page: Search and then select an Opportunity MN-2020 Opportunity")
        hmpageObj.ClickSearchAppsIcon()
        appToSearchFor=XLUtils.readData(self.file,'TC_002',2,3)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        recordToSearch=XLUtils.readData(self.file,'TC_002',2,4)
        hmpageObj.SearchRecord(appToSearchFor,recordToSearch)

        # Setup Object for Opportunity Page class
        OpptyPageObj=OpportunityPage(self.driver)
        OpptyPageObj.ClickShowMoreActions()
        OpptyPageObj.ClickCreateProposalMenuItem()

        # Switch to iFrame
        WebDriverWait(self.driver,60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe')))
        OpptyPageObj.ProposalRecordTypeClickButton('Continue')

        # Setup Object for Proposal Page class
        OpptyPageObj=ProposalDetailPage(self.driver)

        #Verify if the Proposal from the Opportunity gets created successfully
        fieldType=XLUtils.readData(self.file,'TC_002',2,5)
        getFieldLabelOf=XLUtils.readData(self.file,'TC_002',2,6)
        expProposalName=XLUtils.readData(self.file,'TC_002',2,4)
        PropName=OpptyPageObj.getFieldValue(fieldType,getFieldLabelOf)
        if PropName == expProposalName:
            self.lgrObj.info("---------- (PASSED): Proposal creation from Opportunity is successful **********")
            assert True
        else:
            allure.attach(self.driver.get_screenshot_as_png(), name="test_CreateProposalFromOppty",
                          attachment_type=AttachmentType.PNG)
            self.lgrObj.info("---------- (FAILED): Proposal creation from Opportunity is not successful **********")
            self.driver.close()
            assert False

        # Setup Object for Proposal Detail Page class
        propDetPgObj=ProposalDetailPage(self.driver)
        propDetPgObj.ClickProposalPageButton("Delete")
        propDetPgObj.DialogAcceptOrCancel("Delete")
        self.lgrObj.info("---------- END ----------")
        # Close the Driver
        self.driver.close()

    @pytest.mark.RegularPricing
    def test_CreateDirectProposal(self,setup):
        # Create a Logger Object
        self.lgrObj = Logger.logGen('TC_002_2')
        self.driver=setup
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("           TC_002_2: Test Direct Proposal Creation                 ")
        self.lgrObj.info("#################################################################")

        self.driver.get(self.baseUrl)
        # Set up object for Login page object class
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()

        # Set up object for Home Page object class
        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        # Search Proposal App
        hmpageObj.ClickSearchAppsIcon()
        appToSearchFor=XLUtils.readData(self.file,'TC_002',3,3)
        hmpageObj.SearchAndClickApp(appToSearchFor)

        # Set up Object for Proposal Tab Page object class
        PropsPageObj=ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        # Set Proposal fields
        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label=XLUtils.readData(self.file,'TC_002',1,7)
        value=XLUtils.readData(self.file,'TC_002',3,7)
        PropsPageObj.SetProposalField(label,value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_002',1,8)
        value = XLUtils.readData(self.file, 'TC_002',3,8)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_002',1,9)
        value = XLUtils.readData(self.file, 'TC_002',3,9)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_002',1,10)
        value = XLUtils.readData(self.file, 'TC_002',3,10)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')
        # Verify created Proposal Name
        fieldType=XLUtils.readData(self.file,'TC_002',3,5)
        getFieldLabelOf=XLUtils.readData(self.file,'TC_002',3,6)
        expProposalName=XLUtils.readData(self.file,'TC_002',3,7)
        PropName=PropsPageObj.getFieldValue(fieldType, getFieldLabelOf)
        if PropName == expProposalName:
            self.lgrObj.info("---------- (PASSED): Direct Proposal creation is successful **********")
            assert True
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "test_CreateDirectProposal.png")
            self.lgrObj.info("---------- (FAILED): Direct Proposal creation is Failed **********")
            self.driver.close()
        time.sleep(3)
        PropsPageObj.DeleteProposal()
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ----------")
        self.driver.close()
