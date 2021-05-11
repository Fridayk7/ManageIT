from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get("http://127.0.0.1:8000/")

def precondition():
    username = driver.find_element_by_xpath("//input[@id=\'id_username\']")
    username.find_element_by_xpath("//*[@id=\'id_username\']").clear()
    username.send_keys("Test_Username")

    password = driver.find_element_by_xpath("//*[@id=\'id_password\']")
    password.find_element_by_xpath("//*[@id=\'id_password\']").clear()
    password.send_keys("test")

    login_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/form/button")
    login_button.click()


def test_VerifyUsername():
    precondition()
    actual_username = driver.find_element_by_xpath("//input[@id=\'id_username\']")
    s = len(actual_username.text)

    if (s > 0):
        print("FAILED")
    else:
        print("PASSED")


def user_profile_test_suite():

    test_VerifyUsername()


user_profile_test_suite()