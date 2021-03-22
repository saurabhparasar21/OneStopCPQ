from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class AttributeOptionPage:
    def __init__(self,driver):
        self.driver=driver

    def ClickOnTab(self,TabName):
        print("---------- Method: ClickOnTab")
        Path="//md-tab-item[contains(text(),'"+TabName+"')]"
        PathEle = WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path)))
        PathEle.click()

    def VerifyCRMessage(self,Message):
        print("---------- Method: VerifyCRMessage")
        try:
            Path="//*//p[contains(text(),'"+Message+"')]"
            PathEle = WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH, Path)))
            # Scroll to the element
            actions = ActionChains(self.driver)
            actions.move_to_element(PathEle).perform()
            print(PathEle.text)
            if str(Message) in PathEle.text:
                return True
            else:
                return False
        except:
            return False

    def SelectOptionPrd(self,OptionName):
        print("---------- Method: SelectOptionPrd")
        Path="//span[text()='"+OptionName+"']/ancestor::div[@class='form-element-container product-option__name']//div"
        print("path is: "+str(Path))
        PathEle = WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path)))
        # Scroll to the element
        actions = ActionChains(self.driver)
        actions.move_to_element(PathEle).perform()
        self.driver.execute_script("window.scrollBy(0, 75);")
        PathEle.click()

    def ClickMiniCartButton(self,ButtonName):
        print("---------- Method: ClickMiniCartButton")
        Path="//md-icon[@aria-label='shopping_cart']"
        PathEle = WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path)))
        PathEle.click()
        # Click on the Button
        Path1="//button[contains(text(),'"+ButtonName+"')]"
        PathEle1 = WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path1)))
        PathEle1.click()

    def WaitForMiniCartPricingCalcToComplete(self):
        print("---------- Method: WaitForMiniCartPricingCalcToComplete")
        time.sleep(1)
        Path="//span[text()='Recalculating...']"
        Cnt=self.driver.find_elements_by_xpath(Path)
        for i in range(100):
            if len(Cnt) == int(0):
                return True
                break

    def AbandonCart(self):
        print("---------- Method: AbandonCart")
        try:
            print("Inside Try")
            eleXpath="//button[contains(@ng-class,'exit')]"
            ele1 = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH,eleXpath)))
            ele1.click()
        except:
            print("Inside except")
            eleXpath = "//button[contains(@class,'Abandon') and @type='button'][1]"
            ele1 = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, eleXpath)))
            ele1.click()
        time.sleep(3)
        path = "//md-dialog[contains(@aria-label,'Small')]//button[contains(text(),'OK')]"
        ele = self.driver.find_element_by_xpath(path)
        ele.click()

    def SwitchToFrame(self):
        print("---------- Method: SwitchToFrame")
        framePath="//iFrame[contains(@title,'MN')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,framePath)))

    def SwitchToDefault(self):
        print("---------- Method: SwitchToDefault")
        self.driver.switch_to.default_content()





