from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class MassUpdate:

    # Constructor
    def __init__(self, driver):
        self.driver = driver

    def SetMassUpdateField(self,SetOrReset,fieldName,fieldValue):
        print("---------- Method: SetMassUpdateField")
        if SetOrReset == "Set":
            if fieldName != "Adjustment Type":
                elepath="//label[text()='"+fieldName+"']/ancestor::tr[@class='massupdate-row']//input[@type='text']"
                ele= WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH,elepath)))
                ele.send_keys(fieldValue)
            if fieldName == "Adjustment Type":
                elepath1="//label[text()='Adjustment Type']/ancestor::tr[@class='massupdate-row']//a"
                ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, elepath1)))
                ele.click()
            # Select desired Option
                elepath2 = "//li[@class='ui-select-choices-group']//li[@role='option']//div[text()='"+fieldValue+"']"
                ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, elepath2)))
                ele.click()
        if SetOrReset == "Reset":
            ele1="//label[text()='Adjustment Amount']/ancestor::tr[@class='massupdate-row']//input[@type='checkbox']"
        

    def ClickButton(self,Button):
        print("---------- Method: ClickButton")
        element = "//md-dialog-actions[@class='ands-dialog-footer layout-row']//button[contains(text(),'"+Button+"')]"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()
        time.sleep(3)