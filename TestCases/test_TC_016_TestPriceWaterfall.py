import pytest
import time

from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.HomeTab import HomePage
from pageObjects.PriceWaterFall import PriceWaterfallPage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.loginPage import loginPage
from utilities import XLUtils
from utilities.readProperties import ReadConfig
from utilities.Logger import Logger

class Test_PriceWaterfall:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    # Step:04 Set-up Test Scenario. Pass the driver through
    @pytest.mark.RegularPricing
    def test_PriceWaterfall_Classic(self,setup):
        self.lgrObj = Logger.logGen('TC_016_1')
        self.lgrObj.info("####################################################################")
        self.lgrObj.info("             TC_016_1: Price Waterfall (Regular Pricing)            ")
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
        appToSearchFor = XLUtils.readData(self.file, 'TC_016', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields ----------")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_016', 1, 3)
        value = XLUtils.readData(self.file, 'TC_016', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_016', 1, 4)
        value = XLUtils.readData(self.file, 'TC_016', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_016', 1, 5)
        value = XLUtils.readData(self.file, 'TC_016', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_016', 1, 6)
        value = XLUtils.readData(self.file, 'TC_016', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        time.sleep(4)

        CtlgPgObj = CatalogPage(self.driver)
        HomePage.SwitchToFrame(self)
        self.lgrObj.info("---------- Search and Add Product to Cart")
        PrdName= XLUtils.readData(self.file, 'TC_016', 2, 7)
        CtlgPgObj.SearchAndAddProduct('Add to Cart',PrdName)
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Analyze Price Waterfall")
        CartPgObj.ClickCartMenuButton("Analyze Price Waterfall")
        time.sleep(7)

        #hmpageObj.SwitchToFrame()

        # # Set up Price Waterfall Object
        PrcWtrFlObj = PriceWaterfallPage(self.driver)
        Verified=PrcWtrFlObj.VerifyPricePointValueColor('List Price','rgb(25,146,229)','USD 100.00000')
        print("Returned value is: "+str(Verified))

        Verified=PrcWtrFlObj.VerifyPricePointValueColor('PM-0000000456','rgb(255,94,25)','(USD 5.00000)')
        print("Returned value is: "+str(Verified))

        Verified = PrcWtrFlObj.VerifyPricePointValueColor('Base Price', 'rgb(25,146,229)', 'USD 95.00000')
        print("Returned value is: " + str(Verified))

        # ActPPValue = PrcWtrFlObj.GetActualPri'ceOfAnyPricePoint('MN - 2020 PR 1')
        # print("MN - 2020 PR 1 Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('Net Price')
        # print("Base Price Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('SP PP01 (Net Price)')
        # print("Base Price Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('SP PP02')
        # print("SP PP02 Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('shsarkar_price_point_1')
        # print("shsarkar_price_point_1 Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('shsarkar_price_point_2')
        # print("shsarkar_price_point_2 Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('MN - 2020 PP1')
        # print("Contribution Margin Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('MN - 2020 PP2')
        # print("Net Margin Price Point Value is: " + str(ActPPValue))
        #
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('MN - 2020 PP3')
        # print("Contribution Margin Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('Contribution Margin')
        # print("Net Margin Price Point Value is: " + str(ActPPValue))
        #
        # ActPPValue = PrcWtrFlObj.GetActualPriceOfAnyPricePoint('Net Margin')
        # print("Net Margin Price Point Value is: " + str(ActPPValue))







        # # Abandon the Cart and delete it
        # CartPgObj.ClickCartButtons('Abandon')
        # CartPgObj.AbandonDialog('OK')
        # time.sleep(6)
        # PropsPageObj.DeleteProposal()
        # time.sleep(3)
        # PropsPageObj.DialogAcceptOrCancel('Delete')
        # self.lgrObj.info("---------- END ---------- ")
        # self.driver.close()