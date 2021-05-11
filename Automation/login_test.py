from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get("http://127.0.0.1:8000/")

def test_VerifySuccessfulLogin():
    username = driver.find_element_by_xpath("//*[@id=\"id_username\"]")
    username.find_element_by_xpath("//*[@id=\"id_username\"]").clear()
    username.send_keys("Test_Username")

    password = driver.find_element_by_xpath("//*[@id=\"id_password\"]")
    password.find_element_by_xpath("//*[@id=\"id_password\"]").clear()
    password.send_keys("test")

    login_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/form/button")
    login_button.click()

    error_message = driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/h6/span")

    s = len(error_message)
    if (s > 0):
        print("FAILED")
    else:
        print("PASSED")

def test_VerifyInvalidCredentialsLogin():
    username = driver.find_element_by_xpath("//*[@id=\"id_username\"]")
    username.find_element_by_xpath("//*[@id=\"id_username\"]").clear()
    username.send_keys("Test_Username_invalid")

    password = driver.find_element_by_xpath("//*[@id=\"id_password\"]")
    password.find_element_by_xpath("//*[@id=\"id_password\"]").clear()
    password.send_keys("test")

    login_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/form/button")
    login_button.click()

    error_message = driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/h6/span")

    s = len(error_message)
    if (s > 0):
        print("PASSED")
    else:
        print("FAILED")

def login_test_suite():

    test_VerifySuccessfulLogin()
    test_VerifyInvalidCredentialsLogin()

login_test_suite()