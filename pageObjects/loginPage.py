# Define Page Object Class
# Define all the Locators
class loginPage:
    textbox_Username_id="username"
    textbox_Password_id="password"
    button_LogInToSandbox_id="Login"

#
    def __init__(self, driver):
        self.driver = driver

# Define all the methods using all these locators
    def setUsername(self,username):
        self.driver.maximize_window()
        self.driver.find_element_by_id(self.textbox_Username_id).clear()
        self.driver.find_element_by_id(self.textbox_Username_id).send_keys(username)

    def setPassword(self,password):
        self.driver.find_element_by_id(self.textbox_Password_id).send_keys(password)

    def clickLoginButton(self):
        self.driver.find_element_by_id(self.button_LogInToSandbox_id).click()
