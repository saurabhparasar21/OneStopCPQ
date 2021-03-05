from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class OptionPage:


# Initialize Constructors
    def __init__(self,driver):
        self.driver=driver

    def SelectOptionProd(self,OptnPrdName):
        OptnChkBxPath="//span[contains(text(),'"+OptnPrdName+"')]/ancestor::div[@class='form-element-container product-option__name']//input"
        OptnChkBx=WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, OptnChkBxPath)))
        OptnChkBx.click()

    def IsOptionEnableOrDisable(self,OptnPrdName):
        Path="//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'form')]//div[@class='checkbox-override']//input"
        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
        return pathEle.get_attribute('disabled')




