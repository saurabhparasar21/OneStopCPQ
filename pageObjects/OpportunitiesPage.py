from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#-------------------- Remove It -----------------------
#import selenium
#from selenium.webdriver.common.keys import Keys
#from selenium import webdriver
#driver=webdriver.Chrome()
#driver.switch_to.default_content()
#driver.find_element_by_xpath().is_selected()
#driver.find_element_by_xpath().is_displayed()
# -------------------------------------------------------------

class OpportunityPage:
    Icon_ShowMoreActions_XPath="//button[@class='slds-button slds-button_icon-border-filled']"
    MenuItem_CreateQuoteProposal_XPath="//span[text()='Create Quote/Proposal']"

    # Constructor
    def __init__(self, driver):
        self.driver = driver

    # Click on Create Quote/Proposal Menu Item from Opportunity Detail page
    def ClickShowMoreActions(self):
        print("---------- Method: ClickShowMoreActions")
        element=WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,self.Icon_ShowMoreActions_XPath)))
        element.click()

    def ClickCreateProposalMenuItem(self):
        print("---------- Method: ClickCreateProposalMenuItem")
        element1=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, self.MenuItem_CreateQuoteProposal_XPath)))
        element1.click()

    def ProposalRecordTypeClickButton(self,Button):
        print("---------- Method: ProposalRecordTypeClickButton")
        btn="//input[@value='"+Button+"']"
        RecTypPageBtn=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, btn)))
        RecTypPageBtn.click()