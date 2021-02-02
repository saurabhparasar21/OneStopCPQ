from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class NetAdjustmentPopUp:

    # Constructor
    def __init__(self,driver):
        self.driver = driver

    # Set Adjustment Type, Value
    def SetAdjustmentTypeAndValue(self,AdjType,Value):
        print("---------- Set Adjustment Type drop down")
        ele = "//div[@class='adjustment-menu-content fieldtype-wrapper--PICKLIST']//span[@class='md-select-icon']/../.."
        AdjTypeIcon = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ele)))
        AdjTypeIcon.click()

        time.sleep(2)
        adjTypeOptionpath = "//md-select-menu[@class='_md md-overflow']//md-option[@value='"+AdjType+"']"
        AdjTypeOptn = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, adjTypeOptionpath)))
        AdjTypeOptn.click()
        time.sleep(2)

        print("---------- Set Adjustment Amount")
        AdjValue = "//div[@class='adjustment-menu-content']//input"
        AdjValue1 = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, AdjValue)))
        AdjValue1.clear()
        AdjValue1.send_keys(Value)
        time.sleep(2)

        print("---------- Click on Apply button")
        ApplyBtnPath = "//md-menu-content[contains(@id,'adjustment-popup')]//button"
        ApplyBtn = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ApplyBtnPath)))
        ApplyBtn.click()
