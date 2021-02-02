from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class CatalogPage:

    def __init__(self,driver):
        self.driver=driver

    def ClickCatalogPageButton(self,ButtonName):
        print("---------- Method: ClickCatalogPageButton")
        #WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iFrame[contains(@title,"MN")]')))
        if ButtonName == "Installed Products":
            #WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iFrame[contains(@title,"MN")]')))
            InstldPrdBtn="Installed"
            eleXpath = "//button[contains(@class,'"+InstldPrdBtn+"')]"
            ele=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH,eleXpath)))
            ele.click()
        if ButtonName == "Go to Pricing":
            print("Inside Go to Pricing")
            #WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iFrame[contains(@title,"MN")]')))
            GotoPrcngBtn="GoToPricing"
            time.sleep(13)
            eleXpath = "//button[contains(@class,'"+GotoPrcngBtn+"')]"
            ele=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, eleXpath)))
            ele.click()
            print("Go to Pricing button is clicked")
        else:
            print("Inside Go to Pricing else")
            #WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iFrame[contains(@title,"MN")]')))
            eleXpath="//*[contains(@class,'"+ButtonName+"')]"
            ele=WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,eleXpath)))
            ele.click()

    def SearchAndAddProduct(self,Action,ProdName):
        print("---------- Method: SearchAndAddProduct")
        print("Fav name is: "+str(ProdName))
        if Action == "Add to Cart" or Action == "View Cart":
            # Enter Product Name in Find Products box and Search
            FindPrdXPath="//div[@class='search-area-search-term']//input[@type='search']"
            #//input[@placeholder='Find Products']
            FindPrdEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,FindPrdXPath)))
            FindPrdEle.clear()
            FindPrdEle.click()
            FindPrdEle.send_keys(ProdName)
            FindPrdEle.send_keys(Keys.RETURN)
            # Click on Add to Cart button
            fullstring = ProdName
            substring = "FAV"
            if fullstring.find(substring) != -1:
                time.sleep(3)
                Add2CartXPath ="//a[contains(text(),'"+ProdName+"')]/ancestor::div[contains(@class,'main__listings_item listing-item')]//button"
                Add2CartEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, Add2CartXPath)))
                Add2CartEle.click()
            else:
                Add2CartXPath = "//a[text()='"+ProdName+"']/ancestor::div[contains(@class,'main__listings_item listing-item')]//button[contains(@ng-show,'Add')]"
                Add2CartEle = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, Add2CartXPath)))
                print("After Add2CartEle")
                # Scroll to the element
                actions = ActionChains(self.driver)
                actions.move_to_element(Add2CartEle).perform()
                # self.driver.execute_script("return arguments[0].scrollIntoView(true);",Add2CartEle)
                print("Scroll little more before")
                self.driver.execute_script("window.scrollBy(0, 75);")
                print("Scroll little more after")
                # Click on Add to Cart
                Add2CartEle.click()
                time.sleep(8)
            if Action == "Add to Cart":
                for i in range(1000):
                    GotoPrcngBtn = "GoToPricing"
                    eleXpath = "//button[contains(@class,'"+GotoPrcngBtn+"')]"
                    ele=self.driver.find_element_by_xpath(eleXpath)
                    boolv=ele.is_enabled()
                    print(bool(boolv))
                    if boolv == True:
                        print("Go to Pricing button is now enabled, search and add another product now")
                        break
                        i+=1
                # Scroll to the top of the page so that we see search product box
                self.driver.execute_script("window.scrollBy(0, -200);")
                # Switch to default content from frame
            if Action == "View Cart":
                self.driver.execute_script("window.scrollBy(0, -200);")

        if Action == "Exclude Adjustments":
            drpdownPath="//i[@class='fa fa-angle-double-down']"
            drpdownEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, drpdownPath)))
            drpdownEle.click()
            time.sleep(2)
            ExclAdjPath="//ul[@class='context-menu-container']//li[contains(text(),'Exclude Adjustments')]"
            ExclAdjEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,ExclAdjPath)))
            ExclAdjEle.click()
            time.sleep(3)
            print("Wait for Go to Pricing button to get processed before existing this loop")
            for i in range(1000):
                GotoPrcngBtn = "GoToPricing"
                eleXpath = "//button[contains(@class,'"+GotoPrcngBtn+"')]"
                ele = self.driver.find_element_by_xpath(eleXpath)
                boolv = ele.is_enabled()
                print(bool(boolv))
                if boolv == True:
                    print("Go to Pricing button is now enabled, search and add another product now")
                    break
                    i += 1

        if Action == "Delete Fav":
            drpdownPath="//i[@class='fa fa-angle-double-down']"
            drpdownEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, drpdownPath)))
            drpdownEle.click()
            time.sleep(2)
            ExclAdjPath="//ul[@class='context-menu-container']//li[contains(text(),'Delete')]"
            ExclAdjEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,ExclAdjPath)))
            ExclAdjEle.click()
            time.sleep(3)
            self.driver.find_element_by_xpath("//span[text()='Delete']").click()
            time.sleep(3)

    def SearchProduct(self,ProdName):
        print("---------- Method: SearchProduct")
        # Enter Product Name in Find Products box and Search
        FindPrdXPath = "//div[@class='search-area-search-term']//input[@type='search']"
        # //input[@placeholder='Find Products']
        FindPrdEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, FindPrdXPath)))
        FindPrdEle.clear()
        FindPrdEle.click()
        FindPrdEle.send_keys(ProdName)
        FindPrdEle.send_keys(Keys.RETURN)

    def ConfigureProduct(self,Action,ProdName):
        print("---------- Method: ConfigureProduct")
        if Action == "Configure":
            # Click on Configure button for the Product
            ConfBtnPath="//a[text()='"+ProdName+"']/ancestor::div[contains(@class,'main__listings_item listing-item')]//button[contains(@ng-show,'Configur')]"
            print("Path is: "+str(ConfBtnPath))
            ConfgBtnEle=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,ConfBtnPath)))
            # Scroll to the element
            actions = ActionChains(self.driver)
            actions.move_to_element(ConfgBtnEle).perform()
            # self.driver.execute_script("return arguments[0].scrollIntoView(true);",Add2CartEle)
            print("Scroll little more before")
            self.driver.execute_script("window.scrollBy(0, 75);")
            print("Scroll little more after")
            # Click on Add to Cart
            ConfgBtnEle.click()

    def ClickOnLink(self,LinkName):
        print("---------- Method: ClickOnLink")
        linkpath="//a[text()='Favorites']"
        link=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,linkpath)))
        link.click()

    def AbandonCatalog(self):
        AbnIconPath="//*[contains(@ng-class,'Abandon')]"
        AbnIconEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,AbnIconPath)))
        AbnIconEle.click()
        path = "//md-dialog[contains(@aria-label,'Small')]//button[contains(text(),'OK')]"
        print("Path is: " + path)
        ele = self.driver.find_element_by_xpath(path)
        ele.click()

    def CatalogPageQty(self,PrdName,Qty):
        print("---------- Method: CatalogPageQty")
        QtyPath="//a[text()='"+PrdName+"']/ancestor::div[contains(@class,'main__listings_item listing-item')]//div[@class='listing-quantity']//input"
        QtyEle=WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, QtyPath)))
        QtyEle.clear()
        QtyEle.send_keys(Qty)






#//*[contains(@ng-class,'Abandon')]
#//*[@class='mini-cart__display']

#//label[@dfor='checkbox-all']
#//*[text()='MN - 2020 Category']
#//a[text()='MN - 2020 BUNDLE 5']/ancestor::div[contains(@class,'main__listings_item listing-item')]//button[contains(@ng-show,'Configure')]