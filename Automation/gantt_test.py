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

def test_LoadGanttChart():
    precondition()

    gantt_button = driver.find_element_by_xpath("//p[contains(text(),'GanttChart')]")
    gantt_button.click()


def ganttchart_test_suite():
    test_LoadGanttChart()

ganttchart_test_suite()