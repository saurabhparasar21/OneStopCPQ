from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class ConstRulePrompt:
    def __init__(self,driver):
        self.driver=driver

    def VerifyCRMessage(self,Message):
        print("---------- Method: VerifyCRMessage")
        Path="//div[@class='modal-content__description']//p"
        PathEle=WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path)))
        if str(Message) in PathEle.text:
            return True
        else:
            return False

    def ClickButton(self,ButtonName):
        print("---------- Method: ClickButton")
        #Path="//button[contains(text(),'"+ButtonName+"')]"
        # Changed above path for Exclusion
        try:
            Path="//div[@class='modal-dialog']//div[@class='modal-content__modal-row-container']//button[contains(text(),'Remove')]"
            PathEle=WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path)))
            PathEle.click()
        except:
            Path = "//button[contains(text(),'"+ButtonName+"')]"
            PathEle = WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, Path)))
            PathEle.click()
