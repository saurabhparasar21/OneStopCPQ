import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class PresentProposalPage:

    def __init__(self,driver):
        self.driver=driver

    def SelectAttachment(self,FileName):
        framePath = "//div[@class='iframe-parent slds-template_iframe slds-card']//iFrame[contains(@title,'title')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, framePath)))
        path="//td[contains(text(),'"+FileName+"')]/..//input"
        Ele=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,path)))
        Ele.click()
        time.sleep(4)

    def ClickButton(self,BtnName):
        time.sleep(2)
        path="//input[contains(@value,'"+BtnName+"')]"
        eles=self.driver.find_elements_by_xpath(path)
        eles[0].click()
        time.sleep(2)

    def SetTextBox(self,FieldName,Value):
        path="//textarea[contains(@title,'"+FieldName+"')]"
        Ele=WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, path)))
        Ele.send_keys(Value)

    def DialogYesOrNo(self,YesOrNo):
        time.sleep(2)
        path="//input[contains(@Value,'"+YesOrNo+"')]"
        Ele = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, path)))
        Ele.click()
        time.sleep(5)