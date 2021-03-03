import pyautogui
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.HomeTab import HomePage
import time

###########  button_Delete Problemetic ############## DIV[3] or DIV[4]

class ProposalDetailPage:

    # Set up Constructor
    def __init__(self,driver):
        self.driver=driver

    def getFieldValue(self,FieldType,FieldLabel):
        time.sleep(15)
        print("---------- Method: getFieldValue")
        if FieldType == "Text" or "Picklist":
            element="//span[@class='test-id__field-label' and text()='"+FieldLabel+"']/ancestor::div[2]//div[2]//slot//slot//lightning-formatted-text"
            eleY=WebDriverWait(self.driver,180).until(EC.presence_of_element_located((By.XPATH,element)))
            # Scroll to the element
            actions = ActionChains(self.driver)
            actions.move_to_element(eleY).perform()
            eleLabel=eleY.get_attribute("value")
        return eleLabel

    def ClickProposalPageButton(self,Button):
        print("---------- Method: ClickProposalPageButton")
        if Button == "Delete":
            time.sleep(5)
            button_Delete = "//button[@name='Delete']"
            elements=self.driver.find_elements_by_xpath(button_Delete)

            if elements[0].is_displayed() and elements[0].is_enabled():
                elements[0].click()
            elif elements[1].is_displayed() and elements[1].is_enabled():
                elements[1].click()
        elif Button == "Configure Products":
            ConfigurePrds="//span[text()='MN - 2020 (Configure Prds)']/ancestor::*[@class='slds-form__item slds-no-space']//a"
            Btn = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ConfigurePrds)))
            Btn.click()
        elif Button == "Generate" or Button == "Present" or Button == "Accept" or Button == "Create Agreement With Line Items":
            Path = "//span[text()='"+Button+"']/ancestor::*[@class='slds-form__item slds-no-space']//a"
            Btn = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, Path)))
            Btn.click()
        else:
            time.sleep(2)
            ProposalBtn="//*[@title='"+Button+"']"
            #and(@role='button' or @type='button')
            "runtime_platform_actions-action-renderer"
            Btn=WebDriverWait(self.driver,120).until(EC.presence_of_element_located((By.XPATH,ProposalBtn)))
            Btn.click()

    def DeleteProposal(self):
        print("---------- Method: DeleteProposal")
        time.sleep(6)
        path = "//button[@name='Delete']"
        ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, path)))
        ele.click()
        time.sleep(3)

    def ClickConfigureProductButton(self,Button):
        print("---------- Method: ClickConfigureProductButton")
        ConfigurePrds = "//span[text()='"+Button+"']/ancestor::*[@class='slds-form__item slds-no-space']//a"
        Btn = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ConfigurePrds)))
        Btn.click()

    def DialogAcceptOrCancel(self,Button):
        print("---------- Method: DialogClickNextOrCancel")
        if Button == 'Next' or Button == 'Delete':
            btn="//span[text()='"+Button+"']"
            PopUpBtn=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,btn)))
            PopUpBtn.click()
            time.sleep(3)

    def SetProposalField(self,FieldLabel,FieldValue):
        print("---------- Method: SetProposalField: "+FieldLabel)
        field="//label[contains(text(),'"+FieldLabel+"')]//./..//input"
        fieldElement=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,field)))
        fieldElement.send_keys(FieldValue)
        time.sleep(2)
        if FieldLabel=="Price List" or FieldLabel=="Opportunity":
            ele="//lightning-base-combobox-formatted-text[@title='"+FieldValue+"']"
            fieldElement = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, ele)))
            fieldElement.click()
        elif FieldLabel=="Account":
            #time.sleep(2)
            eleAccnt="//span[@class='slds-listbox__option-text slds-listbox__option-text_entity']/lightning-base-combobox-formatted-text[@title='"+FieldValue+"']"
            fieldElement=WebDriverWait(self.driver,60).until(EC.presence_of_element_located((By.XPATH,eleAccnt)))
            fieldElement.click()
        elif FieldLabel=="QTC Profile" and FieldValue=="Split":
            field = "//label[contains(text(),'"+FieldLabel+"')]//./..//input"
            fieldElement = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, field)))
            fieldElement.click()
            time.sleep(3)
            fieldElement.click()
            print("Inside QTC Profile")
            #time.sleep(5)
            SplitPath="//lightning-base-combobox-item[contains(@data-value,'Split')]"
            SplitOptnEl = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,SplitPath)))
            SplitOptnEl.click()
        elif FieldLabel=="QTC Profile" and FieldValue=="Regular":
            field = "//label[contains(text(),'"+FieldLabel+"')]//./..//input"
            fieldElement = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, field)))
            #fieldElement.click()
            #print("Inside QTC Profile")
            time.sleep(5)
            ReglrPath = "//lightning-base-combobox-item[contains(@data-value,'Regular')]"
            ReglrEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ReglrPath)))
            ReglrEle.click()
        elif FieldLabel=="QTC Profile" and FieldValue=="Enterprise":
            field = "//label[contains(text(),'"+FieldLabel+"')]//./..//input"
            fieldElement = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, field)))
            #fieldElement.click()
            #print("Inside QTC Profile")
            time.sleep(5)
            EntrprsPath = "//lightning-base-combobox-item[contains(@data-value,'Enterprise')]"
            EntrprsEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, EntrprsPath)))
            EntrprsEle.click()

    def CheckConfigurationStatus(self,QTCProfile,ExpectedStatus):
        for i in range(100):
            if QTCProfile == "Split":
                print("Inside Split")
                Path="//span[@title='Configurations']/ancestor::div[@class='listWrapper']//td//span//lightning-formatted-text[text()='Main']/ancestor::td/following-sibling::td[1]//lightning-primitive-custom-cell"
            else:
                Path = "//span[@title='Configurations']/ancestor::lst-common-list//div[@class='slds-scrollable_y']//td[@data-label='Status']//lightning-formatted-text"
            Ele = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
            print(Ele.text)
            if Ele.text != ExpectedStatus:
                time.sleep(2)
                print("Inside If")
                # self.driver.find_element_by_xpath(Keys.F5)
                pyautogui.press('f5')
                time.sleep(6)
                self.ClickOnDetailPageTab('Related')
                time.sleep(3)
        return Ele.text

    def ClickOnDetailPageTab(self,TabName):
        path = "//a[text()='"+TabName+"']"
        Ele = WebDriverWait(self.driver, 180).until(EC.element_to_be_clickable((By.XPATH, path)))
        Ele.click()

    def ClickMenuButton(self,MenuButtonName):
        path = "//lightning-button-menu[contains(@class,'menu')]//button"
        Ele = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, path)))
        Ele.click()
        path1="//a//span[text()='"+MenuButtonName+"']"
        Ele1 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, path1)))
        Ele1.click()



