from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class SaveAsFavorite:

    # Constructor
    def __init__(self, driver):
        self.driver = driver

    # Set any Text Box like Fav Name, Description
    def SetTextField(self,Field,Value):
        if Field == "Name":
            elepath="//label[contains(text(),'"+Field+"')]/../..//p//input"
            ele = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, elepath)))
            ele.send_keys(Value)
        else:
            print("Inside Else")
            elepath="//label[contains(text(),'"+Field+"')] /../..//p//textarea"
            print("element path is: "+str(elepath))
            ele = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, elepath)))
            ele.send_keys(Value)

    def SetPickListOption(self,Field,Option):
        elepath="//label[contains(text(),'Color')]/../..//div[contains(@class,'PICKLIST')]"
        ele = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, elepath)))
        ele.click()
        optionpath="//div[text()='"+Option+"']"
        OptionEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, optionpath)))
        OptionEle.click()

    def SaveOrCancel(self,Button):
        time.sleep(3)
        elepath="//button[contains(text(),'"+Button+"') and contains(@ng-click,'saveAsFav')]"
        ele = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, elepath)))
        ele.click()

