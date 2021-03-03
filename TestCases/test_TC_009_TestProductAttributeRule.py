from selenium.webdriver import ActionChains

from utilities.Logger import Logger
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from pageObjects.loginPage import loginPage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.AttributePage import AttributePage
from pageObjects.CustomCartView import CustomCartView
from pageObjects.HomeTab import HomePage
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

class TestProductAttributeRule:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    @pytest.mark.RegularPricing
    def test_PAR_Classic(self, setup):
        self.lgrObj = Logger.logGen('TC_009_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("   TC_009_1: PAR (All Actions) (Regular Cart Normal Pricing      ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_009', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_009', 1, 3)
        value = XLUtils.readData(self.file, 'TC_009', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_009', 1, 4)
        value = XLUtils.readData(self.file, 'TC_009', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_009', 1, 5)
        value = XLUtils.readData(self.file, 'TC_009', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_009', 1, 6)
        value = XLUtils.readData(self.file, 'TC_009', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_009', 2, 8)
        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 5)
        CtlgPgObj.ConfigureProduct('Configure',PrdName)

        AttrPgObj = AttributePage(self.driver)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        self.lgrObj.info("---------- Check if the attributes are hidden according to the PAR")
        Attr1=XLUtils.readData(self.file, 'TC_009', 2, 9)
        Attr2 = XLUtils.readData(self.file, 'TC_009', 2, 10)
        Attr3 = XLUtils.readData(self.file, 'TC_009', 2, 11)
        Attr4 = XLUtils.readData(self.file, 'TC_009', 2, 12)
        Attr5 = XLUtils.readData(self.file, 'TC_009', 2, 13)
        Attr6 = XLUtils.readData(self.file, 'TC_009', 2, 14)
        Attr7 = XLUtils.readData(self.file, 'TC_009', 2, 15)
        Attr8 = XLUtils.readData(self.file, 'TC_009', 2, 16)


        ######################
        # PAR (HIDDEN)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1=AttrPgObj.CheckIfAttrIsHidden(Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): "+Attr1+" is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT hidden")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.CheckIfAttrIsHidden(Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT hidden")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.CheckIfAttrIsHidden(Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT hidden")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.CheckIfAttrIsHidden(Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT hidden")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.CheckIfAttrIsHidden(Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT hidden")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.CheckIfAttrIsHidden(Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT hidden")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.CheckIfAttrIsHidden(Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT hidden")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.CheckIfAttrIsHidden(Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT hidden")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 7)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (DISABLED)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.IsAttrDisabled('Checkbox',Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT disabled")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.IsAttrDisabled('Text',Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT disabled")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrDisabled('Text',Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT disabled")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrDisabled('MultiPickList',Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT disabled")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrDisabled('Text',Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT disabled")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrDisabled('Text',Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT disabled")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrDisabled('Picklist',Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT disabled")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.IsAttrDisabled('Lookup',Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT disabled")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        time.sleep(4)
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 9)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (REQUIRED)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.IsAttrRequired('Checkbox', Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT required")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.IsAttrRequired('Text', Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT required")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrRequired('Text', Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT required")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrRequired('MultiPickList', Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT required")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrRequired('Text', Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT required")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrRequired('Text', Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT required")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrRequired('Picklist', Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT required")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.IsAttrRequired('Lookup', Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT required")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 13)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (DEFAULT)
        #####################
        self.lgrObj.info("----------------------------------------------------------")
        Result2 = AttrPgObj.ReadAttr('Text', Attr2)
        print("Result2 is : "+str(Result2))
        if str('10') in Result2:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.ReadAttr('Text', Attr3)
        print("Result3 is : " + str(Result3))
        if str('Default') in Result3:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Returned_list=AttrPgObj.ReadAttr('MultiPickList', Attr4)
        #print("Result4 is : " + str(Result4))
        if 'Value4' in Returned_list:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT required")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.ReadAttr('Text', Attr5)
        print("Result5 is : " + str(Result5))
        if str('11') in Result5:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.ReadAttr('Text', Attr6)
        print("Result6 is : " + str(Result6))
        if str('12') in Result6:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.ReadAttr('Picklist', Attr7)
        print("Result7 is : " + str(Result7))
        if str('2025') in Result7:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT defaulted correctly")
            assert False
            self.driver.close()


        ######################
        # PAR (RESET)
        #####################
        AttrPgObj.ClickButton('Remove')
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 15)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        self.lgrObj.info("---------------------------------------------------------")
        Result2 = AttrPgObj.IsAttrReset('Text', Attr2,'10')
        print("Result2 is : " + str(Result2))
        if Result2 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrReset('Text', Attr3,'Default')
        print("Result3 is : " + str(Result3))
        if Result3 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrReset('MultiPickList', Attr4,"['Value2', 'Value3']")
        print("Result4 is : " + str(Result4))
        if Result4 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrReset('Text', Attr5, '11')
        print("Result5 is : " + str(Result5))
        if Result5 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrReset('Text', Attr6, '12')
        print("Result6 is : " + str(Result6))
        if Result6 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrReset('Picklist', Attr7, '2022')
        print("Result7 is : " + str(Result7))
        if Result7 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT Reset correctly")
            assert False
            self.driver.close()


        ######################
        # PAR (ALLOW)
        #####################
        AttrPgObj.ClickButton('Remove')
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 11)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        Result7 = AttrPgObj.CheckIfCorrectAttrAllowed('Picklist', Attr7, "['2021', '2022']")
        print("Result7 is : " + str(Result7))
        if Result7 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Correct attributes are allowed for "+str(Attr7))
        else:
            self.lgrObj.info("---------- (FAILED): Correct attributes are NOT allowed for "+str(Attr7))
            assert False
            self.driver.close()

        Result4 = AttrPgObj.CheckIfCorrectAttrAllowed('MultiPickList', Attr4, "['Value2', 'Value3']")
        print("Result4 is : " + str(Result4))
        if Result4 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Correct attributes are allowed for " + str(Attr4))
        else:
            self.lgrObj.info("---------- (FAILED): Correct attributes are NOT allowed for " + str(Attr4))
            assert False
            self.driver.close()

        self.lgrObj.info("----------------------------------------------------------")
        self.lgrObj.info("Abandon the Cart")
        AttrPgObj.AttrPageAbandonCartIcon()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(5)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_PAR_Split(self, setup):
        self.lgrObj = Logger.logGen('TC_009_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("   TC_009_2: PAR (All Actions) Split Cart Async Pricing          ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_009', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_009', 1, 3)
        value = XLUtils.readData(self.file, 'TC_009', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_009', 1, 4)
        value = XLUtils.readData(self.file, 'TC_009', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_009', 1, 5)
        value = XLUtils.readData(self.file, 'TC_009', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_009', 1, 6)
        value = XLUtils.readData(self.file, 'TC_009', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_009', 2, 8)
        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 5)
        CtlgPgObj.ConfigureProduct('Configure',PrdName)

        AttrPgObj = AttributePage(self.driver)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        self.lgrObj.info("---------- Check if the attributes are hidden according to the PAR")
        Attr1=XLUtils.readData(self.file, 'TC_009', 2, 9)
        Attr2 = XLUtils.readData(self.file, 'TC_009', 2, 10)
        Attr3 = XLUtils.readData(self.file, 'TC_009', 2, 11)
        Attr4 = XLUtils.readData(self.file, 'TC_009', 2, 12)
        Attr5 = XLUtils.readData(self.file, 'TC_009', 2, 13)
        Attr6 = XLUtils.readData(self.file, 'TC_009', 2, 14)
        Attr7 = XLUtils.readData(self.file, 'TC_009', 2, 15)
        Attr8 = XLUtils.readData(self.file, 'TC_009', 2, 16)


        ######################
        # PAR (HIDDEN)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1=AttrPgObj.CheckIfAttrIsHidden(Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): "+Attr1+" is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT hidden")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.CheckIfAttrIsHidden(Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT hidden")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.CheckIfAttrIsHidden(Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT hidden")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.CheckIfAttrIsHidden(Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT hidden")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.CheckIfAttrIsHidden(Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT hidden")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.CheckIfAttrIsHidden(Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT hidden")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.CheckIfAttrIsHidden(Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT hidden")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.CheckIfAttrIsHidden(Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT hidden")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 7)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (DISABLED)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.IsAttrDisabled('Checkbox',Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT disabled")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.IsAttrDisabled('Text',Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT disabled")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrDisabled('Text',Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT disabled")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrDisabled('MultiPickList',Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT disabled")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrDisabled('Text',Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT disabled")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrDisabled('Text',Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT disabled")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrDisabled('Picklist',Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT disabled")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.IsAttrDisabled('Lookup',Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT disabled")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 9)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (REQUIRED)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.IsAttrRequired('Checkbox', Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT required")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.IsAttrRequired('Text', Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT required")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrRequired('Text', Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT required")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrRequired('MultiPickList', Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT required")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrRequired('Text', Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT required")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrRequired('Text', Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT required")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrRequired('Picklist', Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT required")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.IsAttrRequired('Lookup', Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT required")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 13)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (DEFAULT)
        #####################
        self.lgrObj.info("----------------------------------------------------------")
        Result2 = AttrPgObj.ReadAttr('Text', Attr2)
        print("Result2 is : "+str(Result2))
        if str('10') in Result2:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.ReadAttr('Text', Attr3)
        print("Result3 is : " + str(Result3))
        if str('Default') in Result3:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Returned_list=AttrPgObj.ReadAttr('MultiPickList', Attr4)
        #print("Result4 is : " + str(Result4))
        if 'Value4' in Returned_list:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT required")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.ReadAttr('Text', Attr5)
        print("Result5 is : " + str(Result5))
        if str('11') in Result5:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.ReadAttr('Text', Attr6)
        print("Result6 is : " + str(Result6))
        if str('12') in Result6:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.ReadAttr('Picklist', Attr7)
        print("Result7 is : " + str(Result7))
        if str('2025') in Result7:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT defaulted correctly")
            assert False
            self.driver.close()


        ######################
        # PAR (RESET)
        #####################
        AttrPgObj.ClickButton('Remove')
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 15)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        self.lgrObj.info("---------------------------------------------------------")
        Result2 = AttrPgObj.IsAttrReset('Text', Attr2,'10')
        print("Result2 is : " + str(Result2))
        if Result2 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrReset('Text', Attr3,'Default')
        print("Result3 is : " + str(Result3))
        if Result3 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrReset('MultiPickList', Attr4,"['Value2', 'Value3']")
        print("Result4 is : " + str(Result4))
        if Result4 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrReset('Text', Attr5, '11')
        print("Result5 is : " + str(Result5))
        if Result5 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrReset('Text', Attr6, '12')
        print("Result6 is : " + str(Result6))
        if Result6 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrReset('Picklist', Attr7, '2022')
        print("Result7 is : " + str(Result7))
        if Result7 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT Reset correctly")
            assert False
            self.driver.close()


        ######################
        # PAR (ALLOW)
        #####################
        AttrPgObj.ClickButton('Remove')
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 11)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        Result7 = AttrPgObj.CheckIfCorrectAttrAllowed('Picklist', Attr7, "['2021', '2022']")
        print("Result7 is : " + str(Result7))
        if Result7 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Correct attributes are allowed for "+str(Attr7))
        else:
            self.lgrObj.info("---------- (FAILED): Correct attributes are NOT allowed for "+str(Attr7))
            assert False
            self.driver.close()

        Result4 = AttrPgObj.CheckIfCorrectAttrAllowed('MultiPickList', Attr4, "['Value2', 'Value3']")
        print("Result4 is : " + str(Result4))
        if Result4 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Correct attributes are allowed for " + str(Attr4))
        else:
            self.lgrObj.info("---------- (FAILED): Correct attributes are NOT allowed for " + str(Attr4))
            assert False
            self.driver.close()

        self.lgrObj.info("----------------------------------------------------------")
        self.lgrObj.info("Abandon the Cart")
        AttrPgObj.AttrPageAbandonCartIcon()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_PAR_Turbo(self, setup):
        self.lgrObj = Logger.logGen('TC_009_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("   TC_009_3: PAR (All Actions) (Regular Cart Turbo Pricing       ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_009', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")

        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_009', 1, 3)
        value = XLUtils.readData(self.file, 'TC_009', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_009', 1, 4)
        value = XLUtils.readData(self.file, 'TC_009', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_009', 1, 5)
        value = XLUtils.readData(self.file, 'TC_009', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_009', 1, 6)
        value = XLUtils.readData(self.file, 'TC_009', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and Configure the Product")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_009', 2, 8)
        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 5)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)

        AttrPgObj = AttributePage(self.driver)
        AttrPgObj.AttrPageWaitForPricingToComplete()
        self.lgrObj.info("---------- Check if the attributes are hidden according to the PAR")
        Attr1 = XLUtils.readData(self.file, 'TC_009', 2, 9)
        Attr2 = XLUtils.readData(self.file, 'TC_009', 2, 10)
        Attr3 = XLUtils.readData(self.file, 'TC_009', 2, 11)
        Attr4 = XLUtils.readData(self.file, 'TC_009', 2, 12)
        Attr5 = XLUtils.readData(self.file, 'TC_009', 2, 13)
        Attr6 = XLUtils.readData(self.file, 'TC_009', 2, 14)
        Attr7 = XLUtils.readData(self.file, 'TC_009', 2, 15)
        Attr8 = XLUtils.readData(self.file, 'TC_009', 2, 16)

        ######################
        # PAR (HIDDEN)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.CheckIfAttrIsHidden(Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT hidden")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.CheckIfAttrIsHidden(Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT hidden")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.CheckIfAttrIsHidden(Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT hidden")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.CheckIfAttrIsHidden(Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT hidden")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.CheckIfAttrIsHidden(Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT hidden")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.CheckIfAttrIsHidden(Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT hidden")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.CheckIfAttrIsHidden(Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT hidden")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.CheckIfAttrIsHidden(Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is hidden")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT hidden")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 7)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (DISABLED)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.IsAttrDisabled('Checkbox', Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT disabled")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.IsAttrDisabled('Text', Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT disabled")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrDisabled('Text', Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT disabled")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrDisabled('MultiPickList', Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT disabled")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrDisabled('Text', Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT disabled")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrDisabled('Text', Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT disabled")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrDisabled('Picklist', Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT disabled")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.IsAttrDisabled('Lookup', Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is disabled")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT disabled")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 9)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (REQUIRED)
        #####################
        self.lgrObj.info("---------------------------------------------------")
        Result1 = AttrPgObj.IsAttrRequired('Checkbox', Attr1)
        if bool(Result1) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr1 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr1 + " is NOT required")
            assert False
            self.driver.close()

        Result2 = AttrPgObj.IsAttrRequired('Text', Attr2)
        if bool(Result2) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT required")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrRequired('Text', Attr3)
        if bool(Result3) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT required")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrRequired('MultiPickList', Attr4)
        if bool(Result4) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT required")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrRequired('Text', Attr5)
        if bool(Result5) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT required")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrRequired('Text', Attr6)
        if bool(Result6) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT required")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrRequired('Picklist', Attr7)
        if bool(Result7) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT required")
            assert False
            self.driver.close()

        Result8 = AttrPgObj.IsAttrRequired('Lookup', Attr8)
        if bool(Result8) == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr8 + " is required")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr8 + " is NOT required")
            assert False
            self.driver.close()

        self.lgrObj.info("---------- Remove the Product and go to Catalog page")
        AttrPgObj.ClickButton('Remove')

        self.lgrObj.info("---------- Search Product, Set Qty and the Configure the Bundle")
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 13)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        ######################
        # PAR (DEFAULT)
        #####################
        self.lgrObj.info("----------------------------------------------------------")
        Result2 = AttrPgObj.ReadAttr('Text', Attr2)
        print("Result2 is : " + str(Result2))
        if str('10') in Result2:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.ReadAttr('Text', Attr3)
        print("Result3 is : " + str(Result3))
        if str('Default') in Result3:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Returned_list = AttrPgObj.ReadAttr('MultiPickList', Attr4)
        # print("Result4 is : " + str(Result4))
        if 'Value4' in Returned_list:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT required")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.ReadAttr('Text', Attr5)
        print("Result5 is : " + str(Result5))
        if str('11') in Result5:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.ReadAttr('Text', Attr6)
        print("Result6 is : " + str(Result6))
        if str('12') in Result6:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.ReadAttr('Picklist', Attr7)
        print("Result7 is : " + str(Result7))
        if str('2025') in Result7:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is defaulted correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT defaulted correctly")
            assert False
            self.driver.close()

        ######################
        # PAR (RESET)
        #####################
        AttrPgObj.ClickButton('Remove')
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 15)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        self.lgrObj.info("---------------------------------------------------------")
        Result2 = AttrPgObj.IsAttrReset('Text', Attr2, '10')
        print("Result2 is : " + str(Result2))
        if Result2 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr2 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr2 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result3 = AttrPgObj.IsAttrReset('Text', Attr3, 'Default')
        print("Result3 is : " + str(Result3))
        if Result3 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr3 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr3 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result4 = AttrPgObj.IsAttrReset('MultiPickList', Attr4, "['Value2', 'Value3']")
        print("Result4 is : " + str(Result4))
        if Result4 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr4 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr4 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result5 = AttrPgObj.IsAttrReset('Text', Attr5, '11')
        print("Result5 is : " + str(Result5))
        if Result5 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr5 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr5 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result6 = AttrPgObj.IsAttrReset('Text', Attr6, '12')
        print("Result6 is : " + str(Result6))
        if Result6 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr6 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr6 + " is NOT Reset correctly")
            assert False
            self.driver.close()

        Result7 = AttrPgObj.IsAttrReset('Picklist', Attr7, '2022')
        print("Result7 is : " + str(Result7))
        if Result7 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): " + Attr7 + " is Reset correctly")
        else:
            self.lgrObj.info("---------- (FAILED): " + Attr7 + " is NOT Reset correctly")
            assert False
            self.driver.close()
        self.lgrObj.info("---------------------------------------------------------")

        ######################
        # PAR (ALLOW)
        #####################

        AttrPgObj.ClickButton('Remove')
        CtlgPgObj.SearchProduct(PrdName)
        CtlgPgObj.CatalogPageQty(PrdName, 11)
        CtlgPgObj.ConfigureProduct('Configure', PrdName)
        AttrPgObj.AttrPageWaitForPricingToComplete()

        Result7 = AttrPgObj.CheckIfCorrectAttrAllowed('Picklist', Attr7, "['2021', '2022']")
        print("Result7 is : " + str(Result7))
        if Result7 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Correct attributes are allowed for " + str(Attr7))
        else:
            self.lgrObj.info("---------- (FAILED): Correct attributes are NOT allowed for " + str(Attr7))
            assert False
            self.driver.close()

        Result4 = AttrPgObj.CheckIfCorrectAttrAllowed('MultiPickList', Attr4, "['Value2', 'Value3']")
        print("Result4 is : " + str(Result4))
        if Result4 == True:
            assert True
            self.lgrObj.info("---------- (PASSED): Correct attributes are allowed for " + str(Attr4))
        else:
            self.lgrObj.info("---------- (FAILED): Correct attributes are NOT allowed for " + str(Attr4))
            assert False
            self.driver.close()

        self.lgrObj.info("----------------------------------------------------------")
        time.sleep(4)
        self.lgrObj.info("Abandon the Cart")
        AttrPgObj.AttrPageAbandonCartIcon()
        time.sleep(8)
        PropsPageObj.DeleteProposal()
        time.sleep(3)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()