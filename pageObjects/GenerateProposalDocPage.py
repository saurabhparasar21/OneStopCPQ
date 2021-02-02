from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time


class GenerateProposalDocPage:

    def __init__(self,driver):
        self.driver=driver

    def SelectTemplate(self,Template):
        time.sleep(12)
        framePath = "//div[@class='iframe-parent slds-template_iframe slds-card']//iFrame[contains(@title,'title')]"
        WebDriverWait(self.driver,60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,framePath)))
        path = "//span[text()='"+Template+"']/../..//input"

        # Scroll to the element
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath(path)).perform()
        self.driver.find_element_by_xpath(path).click()

    def ClickButton(self,Button):
        time.sleep(4)
        path4="//input[@value='"+Button+"']"
        eles=self.driver.find_elements_by_xpath(path4)

        for i in range(len(eles)):
            actions = ActionChains(self.driver)
            actions.move_to_element(eles[i]).perform()
            eles[i].click()
            break

    def IsDocGenerated(self):
        time.sleep(4)
        path = "//span[text()='Document generation successful.']"
        ele = WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, path)))
        ele1=self.driver.find_elements_by_xpath(path)
        return len(ele1)

