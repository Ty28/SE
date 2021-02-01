import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


def el_op(element, mode, key=None, row=None, col=None):
    if mode == 1:
        element.click()
        time.sleep(2)
    elif mode == 2:
        element.send_keys(key)
        time.sleep(1)
    elif mode == 3:
        newx, newy = find_elements_by_xy(element, row, col)
        TouchAction(driver).tap(x=newx, y=newy).perform()
        time.sleep(2)


# (x, y)=find_elements_by_xy(driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board"),1,1)
def find_elements_by_xy(ele, row, col):
    w = ele.size['width']
    x = ele.location['x']
    y = ele.location['y']
    unit = w / 9
    return [int(x + col * unit - unit / 2), int(y + row * unit - unit / 2)]

state_activity_dic = {}
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '11'
desired_caps['deviceName'] = 'Pixel API 30'
desired_caps['appPackage'] = 'org.moire.opensudoku'
desired_caps['appActivity'] = 'org.moire.opensudoku.gui.TitleScreenActivity'

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver.implicitly_wait(20)
time.sleep(4)
# bug1: 0-1-6-10-13
el = driver.find_elements_by_id("android:id/button1")[0]
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/sudoku_lists_button")[0]  # sudoku lists
el_op(el, 1)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Import
el_op(el, 1)
el = driver.find_elements_by_id("com.android.permissioncontroller:id/permission_allow_button")[0]
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[10]  # Download
el_op(el, 1)
driver.quit()