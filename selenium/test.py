from selenium import webdriver
import pyautogui


driver = webdriver.Edge()

driver.get("https://google.com")

a = driver.title
b = "Google"
assert a == b
search_box = driver.find_element("xpath","/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
search_box.send_keys("Facebook-signup")
pyautogui.press("enter")
driver.find_element_by_link_text("Sign Up For Facebook®").click()
driver.maximize_window()
c = driver.title
d = "Meta | Social Metaverse Company"
assert c == d

input("Press Enter to close the browser")
