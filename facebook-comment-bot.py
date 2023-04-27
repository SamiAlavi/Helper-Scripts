from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time

comments=['']

# Using Chrome to access web
driver = webdriver.Chrome('chromedriver.exe')

# Open the website
driver.get("http://mobile.facebook.com/")

# Select the id box
id_box = driver.find_element_by_name('email')
# Send id information
id_box.send_keys('#email')
# Find password box
pass_box = driver.find_element_by_name('pass')
# Send password
pass_box.send_keys('#password')

# Find login button
login_button = driver.find_element_by_name('login')
# Click login
pass_box.send_keys(Keys.RETURN)

time.sleep(5)
driver.get("#m.fbpost")
time.sleep(3)

cmntbox = driver.find_element_by_id('composerInput')
sbmtbox = driver.find_element_by_name('submit')

for i in range(5000):
    j = i%len(comments)    
    cmntbox.send_keys(comments[j])
    time.sleep(1)
    sbmtbox.click()
    time.sleep(3)
