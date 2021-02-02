import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ApprovalsPage:

    def __init__(self,driver):
        self.driver=driver

    def SwitchToApprovalFrame(self,title):
        print("---------- Method: SwitchToApprovalFrame")
        time.sleep(6)
        if title == "Quote":
            self.driver.refresh()
            time.sleep(5)
            framePath = "//div[@class='iframe-parent slds-template_iframe slds-card']//iFrame[contains(@title,'"+title+"')]"
            WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, framePath)))
        else:
            framePath = "//div[@class='iframe-parent slds-template_iframe slds-card']//iFrame[contains(@title,'"+title+"')]"
            WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, framePath)))

    def SwitchToDefault(self):
        print("---------- Method: SwitchToDefault")
        self.driver.switch_to.default_content()

    def ClickButton(self,Button):
        print("---------- Method: ClickButton")
        path="//input[@value='"+Button+"']"
        pathEle = WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH, path)))
        pathEle.click()

    def ClickTab(self,Tab):
        print("---------- Method: ClickTab")
        path = "//td[contains(text(),'"+Tab+"')]"
        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        pathEle.click()

    def SelectAllStepsCheckbox(self):
        print("---------- Method: SelectAllStepsCheckbox")
        path = "//input[contains(@name,'MyApprovalsPage') and @type='checkbox' and contains(@title,'Select')]"
        pathEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, path)))
        pathEle.click()

    def EnterApproverComment(self,Comments):
        print("---------- Method: EnterApproverComment")
        path="//textarea[contains(@name,'ApproveComment')]"
        pathEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, path)))
        pathEle.click()
        pathEle.send_keys(Comments)
