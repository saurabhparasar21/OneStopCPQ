# Cart Page Object Class
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
import time

class CartPage:
   # Constructor
    def __init__(self,driver):
        self.driver=driver

    # Get the Total Values
    def GetValueOfTotal(self,value):
        print("---------- Method:GetValueOfTotal")
        time.sleep(2)
        if value=="Grand Total":
            value1="Grand"
            Total = "//div[contains(@ng-repeat,'" + value1 + "')]//div[2]//div[contains(@class,'plain-text')]"
            eleTotal = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Total)))
            return eleTotal.text
        else:
            value2="Line"
            Total = "//div[contains(@ng-repeat,'"+value2+"')]//div[2]//div[contains(@class,'plain-text')]"
            print("Total xpath is: "+Total)
            # eleTotal = self.driver.find_element_by_xpath(Total)
            eleTotal = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Total)))
            return eleTotal.text

    def ClickCartButtons(self,button):
        print("---------- Method:ClickCartButtons")
        # Click on Different button on Cart
        # //button[contains(text(),'Finalize')]
        # //button[contains(text(),'Reprice')]
        # //button[contains(text(),'Add Miscellaneous Item')]
        # //button[contains(text(),'Submit for Pricing (Async)')]
        # //button[contains(text(),'Abandon')]
        # Abandon Icon
        # //button[contains(@ng-class,'exit')]
        if button != "Abandon":
            eleXpath="//button[contains(text(),'"+button+"')]"
            try:
                ele=WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,eleXpath)))
                ele.click()
            except (TimeoutException,InvalidSessionIdException):
                print("Element "+button+" not present")
                print("---------- END ----------")
                self.driver.close()
        if button == "Abandon":
            eleXpath = "//button[contains(@ng-class,'exit')]"
            ele = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, eleXpath)))
            ele.click()

    def WaitForPricingProgressBarToFinish(self):
        print("---------- Method:WaitForPricingProgressBarToFinish")
        time.sleep(7)
        #print("Inside Progress bar")
        eleXpath="//p[@id='progress-bar-right']"
        element=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,eleXpath)))
        # Loop to compare the text
        for i in range(8000):
            if element.text == "All line items are priced, calculating totals" or element.text == "":
                break
            i += 1
        time.sleep(3)
        #print("Outside Progress bar")

    # Get all the Columns and their Ids
    def getColNoAndId(self,ColName):
        print("---------- Method:getColNoAndId")
        ele = "//span[contains(@class,'ui-grid-header')]"
        eles = self.driver.find_elements_by_xpath(ele)
        for i in range(len(eles)):
            if eles[i].text == ColName:
                id=eles[i].get_attribute("id")
                return i, id
                break

    def getColNoAndId2(self):
        print("---------- Method:getColNoAndId2")
        ele = "//span[contains(@class,'ui-grid-header')]"
        eles = self.driver.find_elements_by_xpath(ele)
        for i in range(len(eles)):
            print(str(i)+"    "+ eles[i].text)

    def ClickCartLineItemCheckBox(self,PrdName):
        print("---------- Method:ClickCartLineItemCheckBox")
        ChkboxPath="//span[text()='"+PrdName+"']/ancestor::div[@class='"+"ui-"+"grid-canvas'"+"]//div[@class='ui-grid-cell-contents checkbox-override']"
        print("Inside Checkbox")
        print(ChkboxPath)
        ChkBox=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ChkboxPath)))
        ChkBox.click()

    def ClickSelectAllCheckBox(self):
        print("---------- Method:ClickSelectAllCheckBox")
        ele="//div[@id='cart-checkbox--header']"
        AllChkBox = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ele)))
        AllChkBox.click()

    def ClickMassAction(self,IconName):
        print("---------- Method:ClickMassAction")
        ChkboxPath = "//div[@id='gridCartUpdateButtonGroup']//button[contains(@aria-label,'"+IconName+"')]"
        ChkBox = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ChkboxPath)))
        ChkBox.click()
        # Copy Icon
        # //div[@id='gridCartUpdateButtonGroup']//button[contains(@aria-label,'Copy')]
        # Delete Icon
        # //div[@id='gridCartUpdateButtonGroup']//button[contains(@aria-label,'Delete')]
        # Mass Update
        # //div[@id='gridCartUpdateButtonGroup']//button[contains(@aria-label,'Mass Update')]
        # Save as Favorite
        # //div[@id='gridCartUpdateButtonGroup']//button[contains(@aria-label,'Quick Buy')]

    # Click on three vertical dots for specific Product
    def ClickOn3VerticalDots(self,ProductName):
        time.sleep(3)
        print("---------- Method:ClickOn3VerticalDots")
        # Click on three line level Vertical Icon
        element = "//span[text()='"+ProductName+"']/ancestor::div[contains(@class,'ui-grid-row ui-grid-tree-header-row')]//span[@class='line-item-icon']"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()
        time.sleep(3)

    # Click on ThreeDotsButton
    def ClickOn3DotsButton(self,Button):
        print("---------- Method:ClickOn3DotsButton")
        element = "//*[@class='lineAction-dropdown']//*//button[contains(text(),'"+Button+"')]"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()
        time.sleep(3)

    def WaitForPricingPendingIndicatorToGoAway(self):
        print("---------- Method:WaitForPricingPendingIndicatorToGoAway")
        print("Inside Price Pending check loop")
        elePath="//span[@title='Pricing Pending']"
        element1 = self.driver.find_elements_by_xpath(elePath)
        for i in range(500):
            print(len(element1))
            if len(element1) == 0:
                break
        print("Outside Price Pending check loop")
        time.sleep(2)

    # Get all the Columns and their Ids
    def getRowNoOfProduct(self, ProductName):
        print("Insisde Get Row No Prd")
        time.sleep(4)
        print("Prd name received: "+str(ProductName))
        print("---------- Method:getRowNoOfProduct")
        ele = "//span[@class='product-name-space']//span"
        eles = self.driver.find_elements_by_xpath(ele)
        print("matching elements else")
        print(len(eles))

        for i in range(len(eles)):
            print("Prd name is: ")
            print(eles[i].text)
            if eles[i].text == ProductName:
                return i
                break

    def FindNoOfCartLines(self):
        print("---------- Method:FindNoOfCartLines")
        path="//div[@class='left ui-grid-render-container-left ui-grid-render-container']//div[@class='ui-grid-canvas']//div[@role='row']"
        Rows=self.driver.find_elements_by_xpath(path)
        return len(Rows)

    def AbandonDialog(self,Button):
        print("---------- Method:AbandonDialog")
        if Button == "OK":
            path="//md-dialog[contains(@aria-label,'Small')]//button[contains(text(),'"+Button+"')]"
            ele=self.driver.find_element_by_xpath(path)
            ele.click()
        if Button == "Cancel":
            path="//md-dialog[contains(@aria-label,'Small')]//button[contains(text(),'"+Button+"')]"
            ele=self.driver.find_element_by_xpath(path)
            ele.click()

    def FinalizeDialog(self,Button):
        print("---------- Method:FinalizeDialog")
        if Button == "OK":
            time.sleep(9)
            path="//md-dialog[contains(@aria-label,'The request')]//button[contains(text(),'"+Button+"')]"
            element = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,path)))
            print("Path is: "+path)
            element.click()

    def ClickNetAdjForAnyProduct(self,PrdName):
        time.sleep(5)
        print("---------- Method:ClickNetAdjForAnyProduct")
        rowNo=self.getRowNoOfProduct(PrdName)
        elesPath = "//div[@class='right ui-grid-render-container-right ui-grid-render-container']//div[@title='Adjustments']"
        elesCnt=self.driver.find_elements_by_xpath(elesPath)
        for i in range(500):
            if i==rowNo:
                elesCnt[i].click()

    def ClickIsOptionalForLineItem(self,PrdName):
        print("---------- Method:ClickNetAdjForAnyProduct")
        rowNo=self.getRowNoOfProduct(PrdName)
        print("Row no is: "+str(rowNo))
        time.sleep(3)
        elesPath = "//div[contains(@ng-if,'Optional')]//dynamic-field//div[@role]"
        elesCnt=self.driver.find_elements_by_xpath(elesPath)
        print("No of matching line items: "+str(len(elesCnt)))

        for i in range(100):
            if i==rowNo:
                i-=1
                print(i)
                elesCnt[i].click()
                break

    def IsEnalbedOrDisabled(self,PrdName,ColName):
        print("---------- Method:IsEnalbedOrDisabled")
        rowNo = self.getRowNoOfProduct(PrdName)
        if ColName == "Net Adjustment %":
            elesPath = "//div[@class='right ui-grid-render-container-right ui-grid-render-container']//div[@title='Adjustments']//dynamic-field"
            elesCnt = self.driver.find_elements_by_xpath(elesPath)
            for i in range(100):
                if i == rowNo:
                    Result=elesCnt[i].get_attribute("class")
                    break
        return Result

    def SetQuantityForLineItem(self,PrdName,Quantity):
        print("---------- Method:SetQuantityForLineItem")
        rowNo=self.getRowNoOfProduct(PrdName)
        time.sleep(6)
        QtyPath = "//div[contains(@class,'QUANTITY')]//input"
        elesCnt=self.driver.find_elements_by_xpath(QtyPath)

        for i in range(100):
            if i==rowNo:
                i-=1
                elesCnt[i].click()
                elesCnt[i].clear()
                elesCnt[i].send_keys(Quantity)
                break

    def IsApprovalIconVisible(self,PrdName):
        print("---------- Method:SetQuantityForLineItem")
        rowNo = self.getRowNoOfProduct(PrdName)
        print("Row no is: " + str(rowNo))
        time.sleep(3)
        AprvlIconPath = "//span[contains(@ng-if,'isApprovalRequired')]//md-icon"
        elesCnt = self.driver.find_elements_by_xpath(AprvlIconPath)

        for i in range(100):
            if i == rowNo:
                i -= 1
                print(i)
                if len(elesCnt) >= 1:
                    return True
                else:
                    return False

    def GetCartApprovalStatus(self):
        print("---------- Method:GetCartApprovalStatus")
        path="//span[@class='proposal-summary__approval-statuslabel']/following-sibling::span//div"
        element1 = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        return element1.text

    def VerifyDealGuidanceShapeAndColor(self,PrdName,ExpectedShape,ExpectedColor):
        print("---------- Method:VerifyDealGuidanceShapeAndColor")
        rowNo = self.getRowNoOfProduct(PrdName)
        print("Row No is: "+str(rowNo))
        elesPath = "//pricing-guidance//span"
        elesCnt = self.driver.find_elements_by_xpath(elesPath)
        for i in range(100):
            if i == rowNo:
                actShape=elesCnt[i].get_attribute("class")
                print("Actual Shape is: "+str(actShape))
                if str(ExpectedShape) in str(actShape):
                    actColor = elesCnt[i].get_attribute("style")
                    print("Actual Color is: " + str(actColor))
                    if str(ExpectedColor) in str(actColor):
                        print("Inside True")
                        return True
                else:
                    print("Inside False")
                    return False

    def SetValueInShoppingCartTable(self,PrdName,ColName,ColType,Value):
        print("---------- Method:SetValueInShoppingCartTable")
        if ColType == str("Picklist"):
            rowNo = self.getRowNoOfProduct(PrdName)
            # Generate Path based on Column Name
            Path="//span[text()='"+ColName+"']"
            PathEle=self.driver.find_element_by_xpath(Path)
            IdOfEle=PathEle.get_attribute("id")
            OldString = IdOfEle
            NewString1 = str.replace(OldString, '-uiGrid', '-0-uiGrid')
            NewString2 = str.replace(NewString1, '-header-text', '-cell')
            elesPath = "//div[@id='"+NewString2+"']"
            elesCnt = self.driver.find_elements_by_xpath(elesPath)

            print("Click on the Cart Col and set value")
            for i in range(100):
                if i==rowNo:
                    i-=1
                    time.sleep(2)
                    elesCnt[i].click()
                    path = "//div[contains(text(),'"+Value+"')]/.."
                    ele=self.driver.find_element_by_xpath(path)
                    time.sleep(2)
                    ele.click()
                    time.sleep(2)
                    break

    def ClickCartMenuButton(self,Button):
        path="//span[@class='menu-toggle']"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,path)))
        element1.click()
        time.sleep(1)
        path2="//button[contains(text(),'"+Button+"')]"
        element2=self.driver.find_element_by_xpath(path2)
        #WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, path)))
        # Scroll to the element
        actions = ActionChains(self.driver)
        actions.move_to_element(element2).perform()
        time.sleep(1)
        element2.click()






       #//div[@class='aptPercentage read-only-plain-text']
   # //span[text()='MN - 2020 Standalone 1']/../../../../../../../../../../../../../..//div[@class='right ui-grid-render-container-right ui-grid-render-container']//div[1][@title='Adjustments']



# Three Vertical dots for any Line Item:
    #//span[text()='MN - 2020 BUNDLE']/ancestor::div[contains(@class,'ui-grid-row ui-grid-tree-header-row')]//span[@class='line-item-icon']

# Left Side View of Cart Table
# Left Side View of Cart Table
    # //div[@class='left ui-grid-render-container-left ui-grid-render-container']

# Right Side View of Cart Table
    #//div[@class='right ui-grid-render-container-right ui-grid-render-container']

# Count of No. of Rows. Note these no get changed when we expand or collapse
    #//div[@class='left ui-grid-render-container-left ui-grid-render-container']//div[@class='ui-grid-canvas']//div[@role='row']

# Find the Proposal Name on Cart page
    #//span[@class='proposal-summary__display']

# Find Approval Status
    #//span[@class='proposal-summary__approval-statuslabel']/..//div[@class=' read-only-plain-text']

# Add More Products button
    #//button[contains(text(),'Add More Products')]

# Get text of Primary button
    #// button[contains( @ ng - click, 'displayAction.primaryAction')]

# Icon Next to Grand Total
# //span[@class='grid-cart-grand-total-icon']//i[@class='fa fa-angle-double-down']

# Icon to open buttons menu
#//span[@class='menu-toggle']//i[@class='fa fa-angle-double-down']

# Default View Drop Down
    # //div[@class='view-menu']

# Search Box on Cart
    # //form//input[@placeholder='Search']

# Filter Icon
    # //div[@class='cart-filter']

# Pricing Progress Bar
    #//pricing-progress[@id='pricing-progress']

#Three Vertical Dots that will show Product Collab button
    #//i[@class='fa fa-lg fa-ellipsis-v']

# Product Collaboration button
    #//*[@id="massActionMenu"]/md-menu-item[1]


#Cart Left Section, Middle, Right Section

# Left Side complete section:
    #//div[@class='left ui-grid-render-container-left ui-grid-render-container']
#//div[@class='right ui-grid-render-container-right ui-grid-render-container']
#//div[@class='ui-grid-render-container ui-grid-render-container-body']

# Find all Columns and their position
        #cols=self.driver.find_elements_by_xpath("//span[contains(@class,'ui-grid-header-cell-label')]")
        #print(cols[0].text())
        #for r in range(len(cols)):
            #print("Col # is: "+str(r)+"value is: "+cols[r].text)

# PArent of Is read only
#//div[@class='md-icon']/../../../../../../../../..


# Count # of Rows.
# elements=self.driver.find_elements_by_xpath("//div[@class='left ui-grid-render-container-left ui-grid-render-container']//div[@class='ui-grid-canvas']//div[@role='row']")
# print("Total # of Rows: "+str(len(elements)))

# Find all Columns and their position

# cols=self.driver.find_elements_by_xpath("//span[contains(@class,'ui-grid-header-cell-label')]")
# print(cols[0].text())
# for r in range(len(cols)):
# print("Col # is: "+str(r)+"value is: "+cols[r].text)


# CtlgPgObj.ClickCatalogPageButton('Installed Products')

# PropsPageObj.ClickProposalPageButton("Delete")
# PropsPageObj.DialogAcceptOrCancel("Delete")
# self.driver.close()

        #def Test():
            # Get Col No & Id of desired column
            #ColNo,ColId = CartPgObj.getColNoAndId('Product')
            #print("Col No. is: "+str(ColNo))
            #print("Col Id. is: " + str(ColId))

            # Get Row Id Of passed Product Name
            #RowId=CartPgObj.getRowNoOfProduct('MN - 2020 Standalone 2')
            #print('Row Id of Product MN - 2020 Standalone 2 is: '+str(RowId))

            # Print all Column Names and their position
            #CartPgObj.getColNoAndId2()