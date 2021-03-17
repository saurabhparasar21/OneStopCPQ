import time
from datetime import datetime, date
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class CPQAdmin:
    def __init__(self, driver):
        self.driver = driver

    def SwitchToFrame(self):
        print("---------- Method: SwitchToFrame")
        framePath = "//iFrame[contains(@title,'Apttus Admin')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, framePath)))

    def ClickOnDetailPageTab(self, TabName):
        print("---------- Method: ClickOnDetailPageTab")
        if TabName == "Pricing":
            path = "//span[text()='" + TabName + "']"
            self.driver.find_element_by_xpath(path).click()

    def ClickPipeLineTab(self, TabName):
        print("---------- Method: ClickPipeLineTab")
        if TabName == "Manage Price Pipeline":
            path = "//a[@aria-label='" + TabName + "']"
            self.driver.find_element_by_xpath(path).click()

    def CreateNewPipeline(self, btnName):
        print("---------- Method: CreateNewPipeline")
        pipelineBtn = "//button[text()='" + btnName + "']"
        self.driver.find_element_by_xpath(pipelineBtn).click()
        time.sleep(15)
        now = date.today()
        print(now)
        nametext = "//input[@name='name']"
        self.driver.find_element_by_xpath(nametext).send_keys('NeW PP')
        seqtext="//input[@name='sequence']"
        self.driver.find_element_by_xpath(seqtext).send_keys(1)
        desctext="//textarea[@name='Description']"
        self.driver.find_element_by_xpath(desctext).send_keys("Newly cretaed Pipeline")
        effectiveDate="//input[@placeholder='Effective Date']"
        self.driver.find_element_by_xpath(effectiveDate).send_keys("03/15/2021")
        expirationDate="//input[@placeholder='Expiration Date']"
        self.driver.find_element_by_xpath(expirationDate).send_keys("03/15/2023")