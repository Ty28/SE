import time
import os
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


def save_state_activity_info(state_index):
    adb_exe_path = "C:\\Users\\TY\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb"
    p = os.popen(adb_exe_path + ' shell dumpsys window | findstr mCurrentFocus')
    info = str(p.read().strip())
    start = info.find("u0")
    if start == -1:
        state_activity_dic[state_index] = 'null'
    else:
        state_activity_dic[state_index] = info[start + 3:-1]


def save_info_as_file():
    with open('state_activity.txt', 'w') as f:
        for state_index in state_activity_dic:
            f.write(str(state_index) + ' ' + state_activity_dic[state_index] + '\n')


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
# testcase1 : test HOME--Settings 0-1-2-3
save_state_activity_info(0)
el = driver.find_elements_by_id("android:id/button1")[0]
el_op(el, 1)
save_state_activity_info(1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/settings_button")[0]  # Settings button
el_op(el, 1)
save_state_activity_info(2)
el = driver.find_elements_by_class_name("android.widget.CheckBox")[0]  # Settings first checkbox
el_op(el, 1)
save_state_activity_info(3)
# testcase1 finished

driver.back()

# testcase2 : test HOME--More options(Settings & About)
# Settings : 1-4-3
# About ：1-4-5-1
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(4)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Settings
el_op(el, 1)
driver.back()
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # About
el_op(el, 1)
save_state_activity_info(5)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
# testcase2 finished

# testcase3 : test SUDOKU LISTS LEVEL--SELECT(Easy/Medium/Hard)
el = driver.find_elements_by_id("org.moire.opensudoku:id/sudoku_lists_button")[0]  # sudoku lists
el_op(el, 1)
save_state_activity_info(6)
# Easy : 1-6-7
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Easy
el_op(el, 1)
save_state_activity_info(7)

driver.back()

# Medium : 1-6-8
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[1]  # Medium
el_op(el, 1)
save_state_activity_info(8)
driver.back()
# Hard : 1-6-9
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Hard
el_op(el, 1)
save_state_activity_info(9)
driver.back()
# testcase3 finished

# testcase4 : test SUDOKU LISTS LEVEL--More options(Add folder/Import/Export all folders/Settings/About)
# Add folder : 6-10-11-6(Cancel)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(10)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Add folder
el_op(el, 1)
save_state_activity_info(11)
el = driver.find_elements_by_id("android:id/button2")[0]  # Cancel button
el_op(el, 1)
# Add folder : 6-10-11-12-122(Add new folder called "test")
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Add folder
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/name")[0]  # Input text
el.send_keys("test")
save_state_activity_info(12)
time.sleep(2)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
save_state_activity_info(122)
# Import  122-125-13
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(125)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Import
el_op(el, 1)
save_state_activity_info(13)

el = driver.find_elements_by_id("com.android.permissioncontroller:id/permission_allow_button")[0]
el_op(el, 1)
driver.back()
# Export all folders 122-125-14
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Export all folders
el_op(el, 1)
save_state_activity_info(14)
driver.back()
# Settings 122-125-3
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[6]  # Settings
el_op(el, 1)
driver.back()
# About 122-125-15-122
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[8]  # About
el_op(el, 1)
save_state_activity_info(15)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
# testcase4 finished

# testcase5 : test SUDOKU LISTS LEVEL--long press a folder()
# Export folder 122-16-17
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]  # long press a folder
TouchAction(driver).long_press(el, duration=5000).release().perform()
save_state_activity_info(16)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Export folder
el.click()
save_state_activity_info(17)
driver.back()
# Rename folder(Cancel) 122-16-18-122
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]  # long press a folder
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Rename folder
el_op(el, 1)
save_state_activity_info(18)
el = driver.find_elements_by_id("android:id/button2")[0]  # Cancel button
el_op(el, 1)
# Rename folder(OK) 122-16-18-19-123
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]  # long press a folder
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Rename folder
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/name")[0]  # Input text
el.send_keys("renamed")
save_state_activity_info(19)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
save_state_activity_info(123)

# Delete folder(Cancel) 123-16-20-123
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]  # long press a folder
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Delete folder
el_op(el, 1)
save_state_activity_info(20)
el = driver.find_elements_by_id("android:id/button2")[0]  # Cancel button
el_op(el, 1)
# Delete folder(OK)123-16-20-6
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]  # long press a folder
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Delete folder
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
# testcase5 finished


# testcase6 : test SUDOKU LISTS--More options(Folders/Filter/Sort/Add sudoku/Settings)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Easy 6-7
el_op(el, 1)
save_state_activity_info(7)

# Folders 7-21-6
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(21)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Folders
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Easy
el_op(el, 1)
# Filter 7-21-22-23-22
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Filter
el_op(el, 1)
save_state_activity_info(22)
el = driver.find_elements_by_class_name("android.widget.CheckedTextView")[0]  # Click first checkbox
el_op(el, 1)
save_state_activity_info(23)
# Filter 22-7(Cancel)
el = driver.find_elements_by_class_name("android.widget.CheckedTextView")[0]  # Click first checkbox
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button2")[0]  # Cancel button
el_op(el, 1)
# Filter 7-21-22-7(Ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Filter
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
# Sort 7-21-24-124
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Sort
el_op(el, 1)
save_state_activity_info(24)
el = driver.find_elements_by_class_name("android.widget.CheckedTextView")[1]  # Click second checkbox
el_op(el, 1)
save_state_activity_info(124)
# Sort 124-7(Cancel)
el = driver.find_elements_by_id("android:id/button2")[0]  # Cancel button
el_op(el, 1)
# Sort 7-21-124-24-7(Ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Sort
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.CheckedTextView")[0]  # Click first checkbox
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
# Add sudoku
# Switch to notes 7-21-25-26-25-26
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[6]  # Add sudoku
el_op(el, 1)
save_state_activity_info(25)
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_num_note")[0]  # switch_num_note button
el_op(el, 1)
save_state_activity_info(26)
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_num_note")[0]  # switch_num_note button
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_num_note")[0]  # switch_num_note button
el_op(el, 1)

# More options(Check solvability)26-27-28-26
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(27)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Check Solvability
el_op(el, 1)
save_state_activity_info(28)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
# More options(Cancel)26-27-7
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Cancel
el_op(el, 1)
# More options(Ok) 7-21-25-29-30-31
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[6]  # Add sudoku
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(29)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(30)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Save
el_op(el, 1)
save_state_activity_info(31)
# Settings 31-32-3
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(32)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[8]  # Settings
el_op(el, 1)
driver.back()
# testcase6 finished


# testcase7 : long press(play this puzzle/edit note/reset puzzle/edit puzzle/delete puzzle)
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
save_state_activity_info(33)
# play this puzzle 31-33-34-35-36
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # play this puzzle
el_op(el, 1)
save_state_activity_info(34)
el = driver.find_elements_by_id("android:id/button1")[0]  # close button
el_op(el, 1)
save_state_activity_info(35)
el = driver.find_elements_by_id("android:id/button1")[0]  # close button
el_op(el, 1)
save_state_activity_info(36)
driver.back()
# edit note 31-33-37-31-33-37-38-39
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # edit note
el_op(el, 1)
save_state_activity_info(37)
el = driver.find_elements_by_id("android:id/button2")[0]  # Cancel button
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # edit note
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/note")[0]  # note text
el.send_keys("test")
save_state_activity_info(38)
time.sleep(2)
el = driver.find_elements_by_id("android:id/button1")[0]  # save button
el_op(el, 1)
save_state_activity_info(39)
# reset puzzle 39-40-41-39-40-41-42
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
save_state_activity_info(40)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # reset puzzle
el_op(el, 1)
save_state_activity_info(41)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # reset puzzle
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
save_state_activity_info(42)
# edit puzzle 42-43-44
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
save_state_activity_info(43)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[6]  # edit puzzle
el_op(el, 1)
save_state_activity_info(44)
driver.back()
# delete puzzle 42-43-45-42-43-45-7
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[8]  # delete puzzle
el_op(el, 1)
save_state_activity_info(45)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
TouchAction(driver).long_press(el, duration=5000).release().perform()
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[8]  # delete puzzle
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
# testcase7 finished

# testcase8 : POP MODE
# ENTER A PUZZLE 7-46
el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
el_op(el, 1)
save_state_activity_info(46)
# check same number 46-47
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=2)
save_state_activity_info(47)
# input wrong number 47-48-49
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(48)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(49)
# input correct number 49-50-51
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(50)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_7")[0]  # button7
el_op(el, 1)
save_state_activity_info(51)
# close POP 51-52-51
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(52)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_close")[0]  # close button
el_op(el, 1)
# clear number 51-52-46
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_clear")[0]  # clear button
el_op(el, 1)
# switch to notes 46-48-53
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[1]  # EDIT NOTE
el_op(el, 1)
save_state_activity_info(53)
# input notes 53-54-55-54-56-57
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(54)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_2")[0]  # button2
el_op(el, 1)
save_state_activity_info(55)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_2")[0]  # button2
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_7")[0]  # button7
el_op(el, 1)
save_state_activity_info(56)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_close")[0]  # close button
el_op(el, 1)
save_state_activity_info(57)
# clear note 57-56-58-46
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_clear")[0]  # clear button
el_op(el, 1)
save_state_activity_info(58)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_close")[0]  # close button
el_op(el, 1)
# undo by button 46-59-60-61-62-63-64-65-66-67-65-63
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=4, col=2)
save_state_activity_info(59)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # SELECT NUMBER
el_op(el, 1)
save_state_activity_info(60)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_2")[0]  # button2
el_op(el, 1)
save_state_activity_info(61)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=9)
save_state_activity_info(62)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
save_state_activity_info(63)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=6, col=1)
save_state_activity_info(64)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
save_state_activity_info(65)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=5, col=1)
save_state_activity_info(66)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
save_state_activity_info(67)
el = driver.find_elements_by_accessibility_id("Undo")[0]  # undo
el_op(el, 1)
el = driver.find_elements_by_accessibility_id("Undo")[0]  # undo
el_op(el, 1)
# Settings 63-3
el = driver.find_elements_by_accessibility_id("Settings")[0]  # Settings
el_op(el, 1)
driver.back()
# More options--Undo 63-64-65-66-67-68-65-69-63
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=6, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=5, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(68)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Undo
el_op(el, 1)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(69)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # Undo
el_op(el, 1)
# More options--Clear all notes 63-70-71-72-73-74-75-76-77-78-76(cancel)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=5, col=1)
save_state_activity_info(70)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[1]  # EDIT NOTE
el_op(el, 1)
save_state_activity_info(71)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_6")[0]  # button6
el_op(el, 1)
save_state_activity_info(72)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_close")[0]  # close button
el_op(el, 1)
save_state_activity_info(73)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=4, col=4)
save_state_activity_info(74)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_5")[0]  # button5
el_op(el, 1)
save_state_activity_info(75)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_close")[0]  # close button
el_op(el, 1)
save_state_activity_info(76)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(77)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Clear all notes
el_op(el, 1)
save_state_activity_info(78)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
# More options--Clear all notes 76-77-78-63(OK)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[2]  # Clear all notes
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
# More options--Set Checkpoint 63-79-63
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(79)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[4]  # Set checkpoint
el_op(el, 1)
# More options--Undo to checkpoint 63-80-64-65-66-67-81-82-67(cancel)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=6, col=1)
save_state_activity_info(80)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[0]  # SELECT NUMBER
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=5, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(81)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[6]  # Undo to checkpoint
el_op(el, 1)
save_state_activity_info(82)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
# More options--Undo to checkpoint 67-81-82-63(ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[6]  # Undo to checkpoint
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
# More options--Undo to before mistake 63-64-65-66-67-68-83-67(cancel)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=6, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=5, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_9")[0]  # button9
el_op(el, 1)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[8]  # Undo to before mistake
el_op(el, 1)
save_state_activity_info(83)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
# More options--Undo to before mistake 67-68-83-84(ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[8]  # Undo to before mistake
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
save_state_activity_info(84)
# More options--Hint 84-85-86-87-88-86(cancel)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(85)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_close")[0]  # close button
el_op(el, 1)
save_state_activity_info(86)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(87)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[10]  # Hint
el_op(el, 1)
save_state_activity_info(88)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
# More options--Hint 86-87-88-89(ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[10]  # Hint
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
save_state_activity_info(89)
# More options--Solve puzzle 89-90-91-89(cancel)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(90)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[12]  # Solve puzzle
el_op(el, 1)
save_state_activity_info(91)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
# More options--Solve puzzle 89-90-91-92-93(ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[12]  # Solve puzzle
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # ok button
el_op(el, 1)
save_state_activity_info(92)
el = driver.find_elements_by_id("android:id/button1")[0]  # OK button
el_op(el, 1)
save_state_activity_info(93)
# More options--Settings 93-94-3
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
save_state_activity_info(94)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[16]  # Settings
el_op(el, 1)
driver.back()
# More options--Help 93-94-95-93
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[18]  # Help
el_op(el, 1)
save_state_activity_info(95)
el = driver.find_elements_by_id("android:id/button1")[0]  # close button
el_op(el, 1)
# More options--Restart 93-94-96-93(Cancel)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[14]  # Restart
el_op(el, 1)
save_state_activity_info(96)
el = driver.find_elements_by_id("android:id/button2")[0]  # cancel button
el_op(el, 1)
# More options--Restart 93-94-96-46(Ok)
el = driver.find_elements_by_accessibility_id("More options")[0]  # More options...
el_op(el, 1)
el = driver.find_elements_by_class_name("android.widget.LinearLayout")[14]  # Settings
el_op(el, 1)
el = driver.find_elements_by_id("android:id/button1")[0]  # Ok button
el_op(el, 1)
# testcase8 finished

# SWITCH TO SN MODE 46-97-98
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_input_mode")[0]  # POP button
el_op(el, 1)
save_state_activity_info(97)
el = driver.find_elements_by_id("android:id/button1")[0]  # CLOSE button
el_op(el, 1)
save_state_activity_info(98)
# testcase9 : test SN MODE
# check same number 98-99
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(99)
# input wrong number 99-100
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(100)
# input correct number 100-101-102
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_7")[0]  # button7
el_op(el, 1)
save_state_activity_info(101)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(102)
# clear number 102-103-104
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_clear")[0]  # clear button
el_op(el, 1)
save_state_activity_info(103)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(104)
# switch to notes 104-105
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_num_note")[0]  # switch button
el_op(el, 1)
save_state_activity_info(105)
# input notes 105-106-107-108-109
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(106)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(107)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_2")[0]  # button2
el_op(el, 1)
save_state_activity_info(108)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(109)
# clear note 109-110-111
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_clear")[0]  # clear button
el_op(el, 1)
save_state_activity_info(110)
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
save_state_activity_info(111)

# SWITCH TO NUMPAD MODE 111-112-113
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_input_mode")[0]  # SN button
el_op(el, 1)
save_state_activity_info(112)
el = driver.find_elements_by_id("android:id/button1")[0]  # CLOSE button
el_op(el, 1)
save_state_activity_info(113)

# testcase10 : test NUMPAD MODE
# check same number 113-114
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=2)
save_state_activity_info(114)
# input wrong number 114-113-115
el = driver.find_element_by_id("org.moire.opensudoku:id/sudoku_board")
el_op(el, 3, row=1, col=1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(115)
# input correct number 115-116
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_7")[0]  # button7
el_op(el, 1)
save_state_activity_info(116)
# clear number 116-113
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_clear")[0]  # clear button
el_op(el, 1)
# switch to notes 113-117
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_num_note")[0]  # switch button
el_op(el, 1)
save_state_activity_info(117)
# input notes 117-118-119-118-120
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_1")[0]  # button1
el_op(el, 1)
save_state_activity_info(118)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_2")[0]  # button2
el_op(el, 1)
save_state_activity_info(119)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_2")[0]  # button2
el_op(el, 1)
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_7")[0]  # button7
el_op(el, 1)
save_state_activity_info(120)
# clear note 120-117
el = driver.find_elements_by_id("org.moire.opensudoku:id/button_clear")[0]  # clear button
el_op(el, 1)

# SWITCH TO POP MODE 117-121-46
el = driver.find_elements_by_id("org.moire.opensudoku:id/switch_input_mode")[0]  # NUMPAD button
el_op(el, 1)
save_state_activity_info(121)
el = driver.find_elements_by_id("android:id/button1")[0]  # CLOSE button
el_op(el, 1)
driver.quit()

save_info_as_file()
