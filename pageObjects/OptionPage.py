import time
from pyautogui import press
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class OptionPage:


# Initialize Constructors
    def __init__(self,driver):
        self.driver=driver

    def SwitchToFrame(self):
        print("---------- Method: SwitchToFrame")
        framePath="//iFrame[contains(@title,'MN')] or contains(@title,'title')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,framePath)))

    def SwitchToDefault(self):
        print("---------- Method: SwitchToDefault")
        self.driver.switch_to.default_content()

    def SearchOption(self,OptnPrdName):
        self.driver.execute_script("scrollBy(0,-500);")
        Path="//input[contains(@placeholder,'Find Products')]"
        PathEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,Path)))
        #self.driver.execute_script("return arguments[0].scrollIntoView(true);",PathEle)
        PathEle.click()
        PathEle.clear()
        PathEle.send_keys(OptnPrdName)
        press('enter')
        #actions = ActionChains(self.driver)
        #actions.move_to_element(PathEle).perform()
        #self.driver.execute_script("window.scrollBy(0, 75);")

    def SelectOptionProd(self,OptnPrdName):
        print("---------- Method: SelectOptionProd")
        try:
            OptnChkBxPath = "//span[contains(text(),'"+OptnPrdName+"')]/ancestor::div[@class='form-element-container product-option__name']//div//label"
            OptnChkBx = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,OptnChkBxPath)))
            actions = ActionChains(self.driver)
            actions.move_to_element(OptnChkBx).perform()
            OptnChkBx.click()
        except:
            print("Inside except")
            OptnChkBxPath1 = "//span[contains(text(),'"+OptnPrdName+"')]/ancestor::div[@class='form-element-container product-option__name']//div//label"
            OptnChkBx1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, OptnChkBxPath1)))
            actions = ActionChains(self.driver)
            actions.move_to_element(OptnChkBx1).perform()
            self.driver.execute_script("window.scrollBy(0,50);")
            time.sleep(5)
            OptnChkBx1.click()

    def IsOptionEnableOrDisable(self,OptnPrdName):
        print("---------- Method: IsOptionEnableOrDisable")
        Path="//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'form')]//div[@class='checkbox-override']//input"
        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
        time.sleep(4)
        return pathEle.get_attribute("disabled")

    def SetOptionPrdQty(self,OptnPrdName,Qty):
        print("---------- Method: SetOptionPrdQty")
        Path="//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'main-configure-product__product-option-container')]//dynamic-field//input"
        pathEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, Path)))
        pathEle.click()
        pathEle.clear()
        pathEle.send_keys(Qty)
        pathEle.send_keys(Keys.TAB)

    def IsOptionPrdCheckedOrUnChecked(self,OptnPrdName):
        print("---------- Method: IsOptionPrdCheckedOrUnChecked")
        Path = "//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'form')]//div[@class='checkbox-override']//input"
        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
        Value=pathEle.get_attribute('checked')
        #Value=hasattr(pathEle,'checked')
        return Value

    def OptnPageWaitForPricingToComplete(self):
        print("---------- Method: OptnPageWaitForPricingToComplete")
        time.sleep(7)

        for n in range(1,20):
            print(n)
            for r in range(300):
                path="//button[contains(@class,'GoToPricing')]"
                pathele=self.driver.find_element_by_xpath(path)
                #print(pathele.is_enabled())
                if pathele.is_enabled() == True:
                    print('Break')
                    break

    def ClickOnButton(self,ButtonName):
        Path="//button[contains(@class,'"+ButtonName+"')]"
        PathEle=WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,Path)))
        PathEle.click()


    def VerifyPriceinSummarySection(self,ChargeType,ExpectedPrice):

        if ChargeType != "Net Price":
            print("Inside")
            Path="//div[contains(text(),'"+ChargeType+"')]/ancestor::span[@class='configure-product__price-name']/following-sibling::span"
            print("Path is: "+str(Path))
            PathEle=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,Path)))
            print(PathEle.text)
            if ExpectedPrice in str(PathEle.text):
                return True
            else:
                return False
        if ChargeType == "Net Price":
            Path = "//span[contains(text(),'Net Price')]/following-sibling::span"
            PathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
            if ExpectedPrice in str(PathEle.text):
                return True
            else:
                return False




        for i in range(len(PathEle)):
            PathEle.text








