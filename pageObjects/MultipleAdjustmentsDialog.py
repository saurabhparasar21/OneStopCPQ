from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class MultipleAdjustmentsDialog:

    # Constructor
    def __init__(self, driver):
        self.driver = driver

    def SetType(self,RowNo,Value):
        print("---------- Method Name: SetType")
        RowSetType = "//table[@class='multiple-adjustment-block']//tbody//tr["+str(RowNo)+"]//td[2]//a"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,RowSetType)))
        element1.click()
        element = "//div[text()='"+Value+"']"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()

    def SetAdjustmentAppliesTo(self,RowNo,Value):
        print("---------- Method Name: SetAdjustmentAppliesTo")
        RowAdjustmentAppliesTo = "//table[@class='multiple-adjustment-block']//tbody//tr["+str(RowNo)+"]//td[3]//a"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,RowAdjustmentAppliesTo)))
        element1.click()
        element = "//div[text()='"+Value+"']"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()

    def SetAdjustmentType(self,RowNo,Value):
        print("---------- Method Name: SetAdjustmentType")
        # Set Adjustment Type
        RowAdjustmentType = "//table[@class='multiple-adjustment-block']//tbody//tr["+str(RowNo)+"]//td[4]//a"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, RowAdjustmentType)))
        element1.click()
        element = "// div[text() = '"+Value+"']"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()

    def SetAdjustmentAmount(self, RowNo, Value):
        print("---------- Method: SetAdjustmentAmount")
        # Set Adjustment Amount
        RowAdjustmentAmount = "//table[@class ='multiple-adjustment-block']//tbody//tr["+str(RowNo)+"]//td[5]//input"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,RowAdjustmentAmount)))
        element1.clear()
        element1.send_keys(Value)

    def ClickAddAnotherAdjustment(self):
        print("---------- Method: ClickAddAnotherAdjustment")
        # Click on Add Another Adjustment
        element = "//span[@class='add-adjustment-line']"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()

    def ClickButton(self,Button):
        print("---------- Method: ClickButton")
        element = "//md-dialog[@ng-show='multipleAdjustments.visible()']//button[contains(text(),'"+Button+"')]"
        element1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, element)))
        element1.click()
        time.sleep(20)