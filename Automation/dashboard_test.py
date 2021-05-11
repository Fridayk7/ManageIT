from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time

driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get("http://127.0.0.1:8000/")

def precondition():
    username = driver.find_element_by_xpath("//*[@id=\"id_username\"]")
    username.find_element_by_xpath("//*[@id=\"id_username\"]").clear()
    username.send_keys("Test_Username")

    password = driver.find_element_by_xpath("//*[@id=\"id_password\"]")
    password.find_element_by_xpath("//*[@id=\"id_password\"]").clear()
    password.send_keys("test")

    login_button = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/div/div/div[2]/form/button")
    login_button.click()

    time.sleep(2)

    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    time.sleep(2)

    load_project_button = driver.find_element_by_css_selector("[href=\"/projects/3\"]")
    load_project_button.click()


def test_VerifyTaskBurnDown():
    precondition()

    dashboard_button = driver.find_element_by_xpath("//p[contains(text(),'Dashboard')]")
    dashboard_button.click()

    task_burndown_table = driver.find_element_by_xpath("//div[@id='burndown']//div//div//div//*[local-name()='svg']")

    if (task_burndown_table.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")

def test_VerifyWorkLoadContainer():
    precondition()

    dashboard_button = driver.find_element_by_xpath("//p[contains(text(),'Dashboard')]")
    dashboard_button.click()

    time.sleep(2)

    workload_table = driver.find_element_by_css_selector("[id=\"workload\"]")

    if (workload_table.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def test_VerifyWorkload():
    precondition()

    dashboard_button = driver.find_element_by_xpath("//p[contains(text(),'Dashboard')]")
    dashboard_button.click()

    time.sleep(2)

    critical_tasks = driver.find_element_by_xpath("//div[@id=\'workload\']")

    if (critical_tasks.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def test_VerifyTasks():
    precondition()

    dashboard_button = driver.find_element_by_xpath("//p[contains(text(),'Dashboard')]")
    dashboard_button.click()

    time.sleep(2)

    tasks = driver.find_element_by_css_selector("#piechart")

    if (tasks.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def dashboard_test_suite():

    test_VerifyTasks()
    test_VerifyTaskBurnDown()
    test_VerifyWorkload()

dashboard_test_suite()