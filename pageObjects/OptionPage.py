from pyautogui import press
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class OptionPage:


# Initialize Constructors
    def __init__(self,driver):
        self.driver=driver

    def SwitchToFrame(self):
        print("---------- Method: SwitchToFrame")
        framePath="//iFrame[contains(@title,'MN')]"
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,framePath)))

    def SwitchToDefault(self):
        print("---------- Method: SwitchToDefault")
        self.driver.switch_to.default_content()

    def SearchOption(self,OptnPrdName):
        Path="//input[contains(@placeholder,'Find Products')]"
        PathEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH,Path)))
        #actions = ActionChains(self.driver)
        #actions.move_to_element(PathEle).perform()
        self.driver.execute_script("return arguments[0].scrollIntoView(true);",PathEle)
        PathEle.click()
        PathEle.clear()
        PathEle.send_keys(OptnPrdName)
        press('enter')


    def SelectOptionProd(self,OptnPrdName):
        print("---------- Method: SelectOptionProd")
        self.SearchOption(OptnPrdName)
        OptnChkBxPath="//span[contains(text(),'"+OptnPrdName+"')]/ancestor::div[@class='form-element-container product-option__name']//div"
        OptnChkBx=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, OptnChkBxPath)))
        actions = ActionChains(self.driver)
        actions.move_to_element(OptnChkBx).perform()
        OptnChkBx.click()

    def IsOptionEnableOrDisable(self,OptnPrdName):
        print("---------- Method: IsOptionEnableOrDisable")
        Path="//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'form')]//div[@class='checkbox-override']//input"
        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
        return pathEle.get_attribute("disabled")

    def SetOptionPrdQty(self,OptnPrdName,Qty):
        print("---------- Method: SetOptionPrdQty")
        Path="//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'main-configure-product__product-option-container')]//dynamic-field//input"
        pathEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, Path)))
        pathEle.click()
        pathEle.clear()
        pathEle.send_keys(Qty)
        pathEle.send_keys(Keys.TAB)

    def IsOptionPrdCheckedOrUnChecked(self,OptnPrdName):
        print("---------- Method: IsOptionPrdCheckedOrUnChecked")
        Path = "//span[text()='"+OptnPrdName+"']/ancestor::div[contains(@class,'form')]//div[@class='checkbox-override']//input"
        pathEle = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, Path)))
        Value=pathEle.get_attribute('checked')
        #Value=hasattr(pathEle,'checked')
        return Value






