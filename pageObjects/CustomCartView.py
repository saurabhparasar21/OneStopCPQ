from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pageObjects.HomeTab import HomePage
import time


class CustomCartView:
    def __init__(self,driver):
        self.driver=driver

    def CreateCustomCartView(self,GrpBy,ViewName):
        DrpDownPath="//div[@class='view-menu']//button"
        DrpDownEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, DrpDownPath)))
        DrpDownEle.click()
        CrtNewViPath="//button[text()='Create New View']"
        CrtNewViwEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, CrtNewViPath)))
        CrtNewViwEle.click()
        GrpByDrpDownPath="//*[@id='groupByColumn']"
        GrpByEle= WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, GrpByDrpDownPath)))
        GrpByEle.click()
        SelGrpBy="//div[text()='"+GrpBy+"']"
        SelGrpByEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, SelGrpBy)))
        SelGrpByEle.click()
        ChooseCartColsTabPath="//span[@class='tabTitle Cust-Col-Selections']"
        ChooseCartColsTabEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ChooseCartColsTabPath)))
        ChooseCartColsTabEle.click()
        LeftBoxSelAllPath="//div[@class='leftColumn']//span[@class='selectAll']"
        LeftBoxSelAllEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, LeftBoxSelAllPath)))
        LeftBoxSelAllEle.click()
        # Move all items from left side box to right side
        Sourcepath = "//span[@class='leftColumnData' and text()='Option Price']"
        source = self.driver.find_element_by_xpath(Sourcepath)
        TargetPath = "//div[@class='rightColumnDataRoot']"
        Target = self.driver.find_element_by_xpath(TargetPath)
        actions = ActionChains(self.driver)
        actions.click_and_hold(source).drag_and_drop(source,Target).perform()
        actions = ActionChains(self.driver)
        actions.click_and_hold(source).drag_and_drop(source,Target).perform()
        Target.click()
        ViewNamepath = "//label[text()='View Name']/..//input"
        ViewNameEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ViewNamepath)))
        ViewNameEle.click()
        ViewNameEle.send_keys(ViewName)
        SaveBtnPth="//button[text()='Save']"
        SaveBtnEle=WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, SaveBtnPth)))
        SaveBtnEle.click()
        time.sleep(8)

    def SelectCustomCartView(self,ViewName):
        time.sleep(3)
        DrpDownPath = "//div[@class='view-menu']//button"
        DrpDownEle=self.driver.find_element_by_xpath(DrpDownPath)
        self.driver.execute_script('arguments[0].scrollIntoView({block: "center"})', DrpDownEle)
        DrpDownEle.click()
        print("Select the View from the drop down")
        ViewPath="//span[@title='"+ViewName+"']"
        SelectViewEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ViewPath)))
        SelectViewEle.click()

    def EditDeleteCustomCartView(self,ViewName,EditOrDeleteView):
        DrpDownPath = "//div[@class='view-menu']//button"
        DrpDownEle = self.driver.find_element_by_xpath(DrpDownPath)
        self.driver.execute_script('arguments[0].scrollIntoView({block: "center"})', DrpDownEle)
        DrpDownEle.click()
        ViewPath = "//span[@title='" + ViewName + "']"
        SelectViewEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, ViewPath)))
        actions = ActionChains(self.driver)
        actions.move_to_element(SelectViewEle).perform()
        Path="//button[contains(text(),'"+EditOrDeleteView+"')]"
        PathEle = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.XPATH, Path)))
        PathEle.click()

