from utilities.Logger import Logger
from utilities.readProperties import ReadConfig
from utilities import XLUtils
from pageObjects.loginPage import loginPage
from pageObjects.HomeTab import HomePage
from pageObjects.ProposalDetailPage import ProposalDetailPage
from pageObjects.CartPage import CartPage
from pageObjects.CatalogPage import CatalogPage
from pageObjects.NetAdjustmentPopUp import NetAdjustmentPopUp
from pageObjects.SaveAsFavoriteDialog import SaveAsFavorite
import time
import pytest

class TestSaveAsFav:
    baseUrl = ReadConfig.getbaseURL()
    UserName = ReadConfig.getuserName()
    Password = ReadConfig.getpassword()
    file = ReadConfig.getFilePath()

    @pytest.mark.RegularPricing
    def test_SaveAsFav_Classic(self,setup):
        self.lgrObj=Logger.logGen('TC_007_1')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("        TC_007_1: Save As Fav (Regular Cart Normal Pricing         ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
        self.driver=setup
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        self.lgrObj.info("---------- Switch to Lightning if not set")
        self.HomePageObj=HomePage(self.driver)
        self.HomePageObj.switchToLightning()

        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_007', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_007', 1, 3)
        value = XLUtils.readData(self.file, 'TC_007', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_007', 1, 4)
        value = XLUtils.readData(self.file, 'TC_007', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_007', 1, 5)
        value = XLUtils.readData(self.file, 'TC_007', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_007', 1, 6)
        value = XLUtils.readData(self.file, 'TC_007', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to the Cart")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_007', 2, 8)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)

        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj=NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount','10')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Select the Prd and click on Save as Fav icon")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Save as Favorite')
        self.lgrObj.info("---------- Set fields in Favorite Pop-up and Save it")
        FavPgObj=SaveAsFavorite(self.driver)
        FavName=XLUtils.readData(self.file, 'TC_007', 2, 9)
        print("Fav name is: "+FavName)
        FavDesc=XLUtils.readData(self.file, 'TC_007', 2, 10)

        FavPgObj.SetTextField('Name',FavName)
        FavPgObj.SetTextField('Description',FavDesc)
        FavPgObj.SaveOrCancel('Save')
        print("Save button is clicked")
        print("Below Wait is needed - Checked")
        time.sleep(3)

        self.lgrObj.info("---------- Delete the Product from Cart")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Go back to Catalog Page")
        CartPgObj.ClickCartButtons('Add More Products')

        self.lgrObj.info("---------- Click on Fav Icon")
        CtlgPgObj.ClickOnLink('Favorites')
        self.lgrObj.info("---------- Search for the desired Favorite")
        CtlgPgObj.SearchAndAddProduct('Add to Cart',FavName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]
        self.lgrObj.info("---------- Grand Total of Added Favorite record is : " + str(SlicedGrandTotal))

        if  str("90") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total of added Favorite (With Adjustment) is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total of added Favorite (With Adjustment) is NOT correct ------")
            self.driver.close()
        self.lgrObj.info("---------- Delete the Product from Cart")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Go back to Catalog Page")
        CartPgObj.ClickCartButtons('Add More Products')

        self.lgrObj.info("---------- Click on Fav Icon")
        CtlgPgObj.ClickOnLink('Favorites')
        self.lgrObj.info("---------- Search and add Favorite with out Adjustment")
        CtlgPgObj.SearchAndAddProduct('Exclude Adjustments', FavName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]
        self.lgrObj.info("---------- Grand Total of Added Favorite (With out Adjustment) is : " + str(SlicedGrandTotal))

        if str("100") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total of added Favorite (with out adjustment) is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total of added Favorite (with out adjustment) is NOT correct ------")
            self.driver.close()

        self.lgrObj.info("---------- Go back to Catalog page and delete the Fav")
        CartPgObj.ClickCartButtons('Add More Products')
        self.lgrObj.info("---------- Click on Fav Icon")
        CtlgPgObj.ClickOnLink('Favorites')
        self.lgrObj.info("---------- Search and Delete the Favorite")
        CtlgPgObj.SearchAndAddProduct('Delete Fav', FavName)
        CtlgPgObj.AbandonCatalog()
        time.sleep(2)
        PropsPageObj.DeleteProposal()
        time.sleep(2)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.TurboPricing
    def test_SaveAsFav_Turbo(self,setup):
        self.lgrObj=Logger.logGen('TC_007_2')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("        TC_007_2: Save As Fav (Regular Cart Turbo Pricing        ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
        self.driver=setup
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        self.lgrObj.info("---------- Switch to Lightning if not set")
        self.HomePageObj=HomePage(self.driver)
        self.HomePageObj.switchToLightning()

        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_007', 2, 2)
        hmpageObj.SearchAndClickApp(appToSearchFor)
        # Set up Object for Proposal Tab Page object class
        PropsPageObj = ProposalDetailPage(self.driver)

        # Click on New button to go to Create Proposal Edit page
        PropsPageObj.ClickProposalPageButton('New')
        # CLick Next in the Record Type Dialog Box
        PropsPageObj.DialogAcceptOrCancel('Next')

        self.lgrObj.info("---------- Set Proposal Fields")
        # Proposal Name
        label = XLUtils.readData(self.file, 'TC_007', 1, 3)
        value = XLUtils.readData(self.file, 'TC_007', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_007', 1, 4)
        value = XLUtils.readData(self.file, 'TC_007', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_007', 1, 5)
        value = XLUtils.readData(self.file, 'TC_007', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_007', 1, 6)
        value = XLUtils.readData(self.file, 'TC_007', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Turbo)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to the Cart")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_007', 2, 8)
        CtlgPgObj.SearchAndAddProduct('Add to Cart', PrdName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        # Set up Object for Cart Page
        CartPgObj = CartPage(self.driver)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)

        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj=NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount','10')
        time.sleep(2)
        self.lgrObj.info("---------- Click on Reprice button")

        CartPgObj.ClickCartButtons('Reprice')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Select the Prd and click on Save as Fav icon")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Save as Favorite')
        self.lgrObj.info("---------- Set fields in Favorite Pop-up and Save it")
        FavPgObj=SaveAsFavorite(self.driver)
        FavName=XLUtils.readData(self.file, 'TC_007', 2, 9)
        print("Fav name is: "+FavName)
        FavDesc=XLUtils.readData(self.file, 'TC_007', 2, 10)

        FavPgObj.SetTextField('Name',FavName)
        FavPgObj.SetTextField('Description',FavDesc)
        FavPgObj.SaveOrCancel('Save')
        print("Save button is clicked")
        print("Below Wait is needed - Checked")
        time.sleep(3)

        self.lgrObj.info("---------- Delete the Product from Cart")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Go back to Catalog Page")
        CartPgObj.ClickCartButtons('Add More Products')

        self.lgrObj.info("---------- Click on Fav Icon")
        CtlgPgObj.ClickOnLink('Favorites')
        self.lgrObj.info("---------- Search for the desired Favorite")
        CtlgPgObj.SearchAndAddProduct('Add to Cart',FavName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]
        self.lgrObj.info("---------- Grand Total of Added Favorite record is : " + str(SlicedGrandTotal))

        if  str("90") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total of added Favorite (With Adjustment) is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total of added Favorite (With Adjustment) is NOT correct ------")
            self.driver.close()
        self.lgrObj.info("---------- Delete the Product from Cart")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()
        self.lgrObj.info("---------- Go back to Catalog Page")
        CartPgObj.ClickCartButtons('Add More Products')

        self.lgrObj.info("---------- Click on Fav Icon")
        CtlgPgObj.ClickOnLink('Favorites')
        self.lgrObj.info("---------- Search and add Favorite with out Adjustment")
        CtlgPgObj.SearchAndAddProduct('Exclude Adjustments', FavName)
        self.lgrObj.info("---------- Go to Shopping Cart")
        CtlgPgObj.ClickCatalogPageButton('Go to Pricing')
        CartPgObj.WaitForPricingProgressBarToFinish()

        grandTotal = CartPgObj.GetValueOfTotal('Grand Total')
        SlicedGrandTotal = grandTotal[4:]
        self.lgrObj.info("---------- Grand Total of Added Favorite (With out Adjustment) is : " + str(SlicedGrandTotal))

        if str("100") in str(float(SlicedGrandTotal)):
            assert True
            self.lgrObj.info("---------- (PASSED): Grand Total of added Favorite (with out adjustment) is correct ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Grand Total of added Favorite (with out adjustment) is NOT correct ------")
            self.driver.close()

        self.lgrObj.info("---------- Go back to Catalog page and delete the Fav")
        CartPgObj.ClickCartButtons('Add More Products')
        self.lgrObj.info("---------- Click on Fav Icon")
        CtlgPgObj.ClickOnLink('Favorites')
        self.lgrObj.info("---------- Search and Delete the Favorite")
        CtlgPgObj.SearchAndAddProduct('Delete Fav', FavName)
        CtlgPgObj.AbandonCatalog()
        time.sleep(2)
        PropsPageObj.DeleteProposal()
        time.sleep(2)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()

    @pytest.mark.Split
    def test_SaveAsFav_Split(self,setup):
        self.lgrObj=Logger.logGen('TC_007_3')
        self.lgrObj.info("#################################################################")
        self.lgrObj.info("        TC_007_3: Save As Fav Split Cart Async Pricing           ")
        self.lgrObj.info("#################################################################")

        self.lgrObj.info("---------- Login to the Application")
        print("---------- Login to the Application")
        self.driver=setup
        self.driver.get(self.baseUrl)
        self.lgnObj = loginPage(self.driver)
        self.lgnObj.setUsername(self.UserName)
        self.lgnObj.setPassword(self.Password)
        self.lgnObj.clickLoginButton()
        self.driver.maximize_window()
        self.lgrObj.info("---------- Switch to Lightning if not set")
        self.HomePageObj=HomePage(self.driver)
        self.HomePageObj.switchToLightning()

        hmpageObj = HomePage(self.driver)
        hmpageObj.switchToLightning()

        self.lgrObj.info("---------- Create a new Proposal")
        hmpageObj.ClickSearchAppsIcon()
        # td_AppToSearchSelect=
        appToSearchFor = XLUtils.readData(self.file, 'TC_007', 2, 2)
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
        label = XLUtils.readData(self.file, 'TC_007', 1, 3)
        value = XLUtils.readData(self.file, 'TC_007', 2, 3)
        PropsPageObj.SetProposalField(label, value)

        # Price List
        label = XLUtils.readData(self.file, 'TC_007', 1, 4)
        value = XLUtils.readData(self.file, 'TC_007', 2, 4)
        PropsPageObj.SetProposalField(label, value)

        # Opportunity
        label = XLUtils.readData(self.file, 'TC_007', 1, 5)
        value = XLUtils.readData(self.file, 'TC_007', 2, 5)
        PropsPageObj.SetProposalField(label, value)

        # Account
        label = XLUtils.readData(self.file, 'TC_007', 1, 6)
        value = XLUtils.readData(self.file, 'TC_007', 2, 6)
        PropsPageObj.SetProposalField(label, value)

        # Click on Save button
        PropsPageObj.ClickProposalPageButton('Save')

        self.lgrObj.info("---------- Configure the Proposal")
        PropsPageObj.ClickConfigureProductButton('MN - 2020 (Quick Launch)')
        CtlgPgObj = CatalogPage(self.driver)
        self.lgrObj.info("---------- Search and add Product to the Cart")
        HomePage.SwitchToFrame(self)
        PrdName = XLUtils.readData(self.file, 'TC_007', 2, 8)
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
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Click on Net Adj link for the Product")
        time.sleep(2)
        CartPgObj.ClickNetAdjForAnyProduct(PrdName)

        self.lgrObj.info("---------- Set Adjustments in Net Adj Popup and Click on Save")
        NetAdjObj=NetAdjustmentPopUp(self.driver)
        NetAdjObj.SetAdjustmentTypeAndValue('% Discount','10')
        CartPgObj.ClickCartButtons('Submit for Pricing (Async)')
        CartPgObj.ClickCartButtons('Submit & Stay On Cart')
        print("Wait is needed--Checked")
        time.sleep(5)
        CartPgObj.WaitForPricingProgressBarToFinish()

        self.lgrObj.info("---------- Select the Prd and click on Save as Fav icon")
        time.sleep(2)
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Save as Favorite')
        self.lgrObj.info("---------- Set fields in Favorite Pop-up and Save it")
        FavPgObj=SaveAsFavorite(self.driver)
        FavName=XLUtils.readData(self.file, 'TC_007', 2, 9)
        print("Fav name is: "+FavName)
        FavDesc=XLUtils.readData(self.file, 'TC_007', 2, 10)

        FavPgObj.SetTextField('Name',FavName)
        FavPgObj.SetTextField('Description',FavDesc)
        FavPgObj.SaveOrCancel('Save')
        print("Save button is clicked")
        print("Below Wait is needed - Checked")
        time.sleep(6)

        self.lgrObj.info("---------- Delete the Product from Cart")
        CartPgObj.ClickCartLineItemCheckBox(PrdName)
        CartPgObj.ClickMassAction('Delete')
        CartPgObj.WaitForPricingProgressBarToFinish()
        time.sleep(5)

        self.lgrObj.info("---------- Go back to Catalog Page")
        CartPgObj.ClickCartButtons('Add More Products')
        time.sleep(3)

        self.lgrObj.info("---------- Check Favorite Category is not present for Split Cart")
        linkpath = "//a[text()='Favorites']"
        ChkFavLink=self.driver.find_elements_by_xpath(linkpath)

        if str(len(ChkFavLink)) == str("0"):
            assert True
            self.lgrObj.info("---------- (PASSED): Favorite is not available for Split Cart ----------")
        else:
            assert False
            self.driver.save_screenshot("../Screenshots/" + "TC_004.png")
            self.lgrObj.info("---------- (FAILED): Favorite is available for Split Cart ------")
            self.driver.close()

        CtlgPgObj.AbandonCatalog()
        time.sleep(2)
        PropsPageObj.DeleteProposal()
        time.sleep(2)
        PropsPageObj.DialogAcceptOrCancel('Delete')
        self.lgrObj.info("---------- END ---------- ")
        self.driver.close()