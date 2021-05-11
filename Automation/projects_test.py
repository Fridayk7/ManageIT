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


def test_VerifyCreateProjectButton():
    precondition()
    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    create_button = driver.find_element_by_xpath("//button[@class='btn btn-primary']")
    if (create_button.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def test_CreateNewProject():
    precondition()
    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    time.sleep(2)

    create_button = driver.find_element_by_xpath("//button[@class='btn btn-primary']")
    create_button.click()

    time.sleep(2)

    project_name = driver.find_element_by_xpath("//input[@name='project_name']")
    project_name.send_keys("Test Project")

    inside_create_button = driver.find_element_by_xpath("//input[@class='btn btn-block btn-secondary']")
    inside_create_button.click()

    time.sleep(2)

    if (driver.find_element_by_css_selector("[href=\"/projects/3\"]").is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def test_LoadProject():
    precondition()
    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    time.sleep(2)

    load_project_button = driver.find_element_by_css_selector("[href=\"/projects/3\"]")

    try:
        load_project_button.click()
        print("PASSED")
    except Exception:
        print("FAILED")

def test_VerifyCreateTaskButton():
    precondition()

    time.sleep(2)

    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    time.sleep(2)

    load_project_button = driver.find_element_by_css_selector("[href=\"/projects/3\"]")
    load_project_button.click()

    create_task_button = driver.find_element_by_xpath("//button[contains(text(),'Create a Task')]")
    if (create_task_button.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def test_VerifyCreateWorkBreakDownButton():
    precondition()

    time.sleep(2)

    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    time.sleep(2)

    load_project_button = driver.find_element_by_css_selector("[href=\"/projects/3\"]")
    load_project_button.click()

    work_breakdown_button = driver.find_element_by_xpath("//button[contains(text(),'Create Work Breakdown Structure')]")
    if (work_breakdown_button.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")


def test_VerifyInviteTeamButton():
    precondition()

    time.sleep(2)

    projects_button = driver.find_element_by_xpath("//p[contains(text(),'Projects')]")
    projects_button.click()

    time.sleep(2)

    load_project_button = driver.find_element_by_css_selector("[href=\"/projects/3\"]")
    load_project_button.click()

    invite_button = driver.find_element_by_xpath("//button[contains(text(),'Invite Your Team!')]")
    if (invite_button.is_displayed()):
        print("PASSED")
    else:
        print("FAILED")

def projects_test_suite():

    test_VerifyCreateProjectButton()
    test_CreateNewProject()
    test_LoadProject()
    test_VerifyCreateWorkBreakDownButton()
    test_VerifyInviteTeamButton()

projects_test_suite()