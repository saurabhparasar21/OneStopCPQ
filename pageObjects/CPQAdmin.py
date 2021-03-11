import time
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class CPQAdmin:
    def __init__(self, driver):
        self.driver = driver

    def SwitchToFrame(self):
        print("---------- Method: SwitchToFrame")
        framePath="//iFrame[contains(@title,'Apttus Admin')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,framePath)))

    def ClickOnDetailPageTab(self, TabName):
        print("---------- Method: ClickOnDetailPageTab")
        if TabName == "Pricing":
            path = "//span[text()='"+TabName+"']"
            self.driver.find_element_by_xpath(path).click()

