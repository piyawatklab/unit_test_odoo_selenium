from colorama import Fore, init

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from seleniumbase import Driver

import time

from libs.settings import USERNAME_LOGIN , PASSWORD_LOGIN

init()

url = 'https://mp-dev.almacom.co.th/web#action=389&model=mrp.bom&view_type=list&cids=2&menu_id=218'

json_data = {
    "product_tmpl_id" : 'A00001',
    "product_qty": 2,
    "product":[{
        "product_id": 'TTT001',
        "product_qty": 3,
    },{
        "product_id": 'TTT002',
        "product_qty": 4,
    },
    ]
}

def run():

    try:
        name = 'open_odoo'
        
        driver = Driver(uc=True)
        # driver = Driver(uc=True,headless=True)
        driver.get(url)
        time.sleep(3)
        print_ok(name)

    # except Exception as e:
    #     print_error(name) 
    #     print_error(e)

        name = 'login_odoo'

    # try:
        driver.find_element(By.XPATH, "//input[@name='login']").send_keys(USERNAME_LOGIN)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(PASSWORD_LOGIN)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        check_text = driver.find_element(By.XPATH, "//span[@class='text-truncate']").text
        if check_text == 'Bills of Materials':
            print_ok(name)
        else:
            e = driver.find_element(By.XPATH, "//div[@class='o_notification_manager']").text
            print_error(name,e)

    # except Exception as e:
    #     print_error(name) 
    #     print_error(e)
    
        name = 'create_bom'

    # try:
        driver.find_element(By.XPATH, ".//button[@class='btn btn-primary o_list_button_add']").click()
        time.sleep(3)
        
        input_partner = driver.find_element(By.XPATH, "//input[@id='product_tmpl_id']")
        input_partner.send_keys(json_data["product_tmpl_id"])
        input_partner.send_keys(Keys.ENTER)
        time.sleep(1)

        input_product_qty = driver.find_element(By.XPATH, "//input[@id='product_qty']")
        input_product_qty.clear()
        input_product_qty.send_keys(json_data["product_qty"])
        input_product_qty.send_keys(Keys.ENTER)
        time.sleep(1)

        add_line = driver.find_element(By.XPATH, "//a[contains(text(), 'Add a line')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_line)
        time.sleep(1)
        add_line.click()
        time.sleep(1)

        product_list = json_data["product"]

        for i in range(len(product_list)):

            tbody_add = driver.find_element(By.XPATH, ".//tbody[contains(@class, 'ui-sortable')]")
            tr_add = tbody_add.find_elements(By.TAG_NAME, "tr")

            td_add = tr_add[i].find_element(By.XPATH, ".//td[@name='product_id']")
            td_add.find_element(By.XPATH, ".//input[@type='text']").send_keys(product_list[i]["product_id"])
            time.sleep(3)
            td_add.send_keys(Keys.ENTER)
            time.sleep(3)

            td_add = tr_add[i].find_element(By.XPATH, ".//td[@name='product_qty']")
            td_add.click()
            time.sleep(3)
            td_add.find_element(By.XPATH, ".//input[@type='text']").send_keys(product_list[i]["product_qty"])
            time.sleep(3)
            td_add.send_keys(Keys.ENTER)
            time.sleep(3)

        print_ok(name)
    
    # except Exception as e:
    #     print_error(name)
    #     print_error(e)
    
        name = 'save_bom'

    # try:

        driver.find_element(By.XPATH, "//button[@data-tooltip='Save manually']").click()
        time.sleep(3)

        check_text = driver.find_element(By.XPATH, "//span[@class='text-truncate']").text
        if check_text != 'New':
            print_ok(name)
            print('- BoM : ' + check_text)
        else:
            e = driver.find_element(By.XPATH, "//div[@class='o_notification_manager']").text
            print_error(name,e)
        time.sleep(3)
    
    # except Exception as e:
    #     print_error(name)
    #     print_error(e)
    
        name = 'create_mo'

    # try:
        driver.get('https://mp-dev.almacom.co.th/web#action=395&model=mrp.production&view_type=list&cids=2&menu_id=229')
        time.sleep(3)
        
        driver.find_element(By.XPATH, ".//button[@class='btn btn-primary o_list_button_add']").click()
        time.sleep(3)

        bom_id = check_text.split(":")

        input_bom = driver.find_element(By.XPATH, "//input[@id='bom_id']")
        input_bom.send_keys(bom_id[0])
        input_bom.send_keys(Keys.ENTER)
        time.sleep(3)
        
        print_ok(name)
    
    # except Exception as e:
    #     print_error(name)
    #     print_error(e)
    
        name = 'save_mo'

    # try:

        driver.find_element(By.XPATH, "//button[@data-tooltip='Save manually']").click()
        time.sleep(3)

        check_text = driver.find_element(By.XPATH, "//span[@class='text-truncate']").text
        if check_text != 'New':
            print_ok(name)
            print('- MO : ' + check_text)
        else:
            e = driver.find_element(By.XPATH, "//div[@class='o_notification_manager']").text
            print_error(name,e)
        time.sleep(3)
    
    # except Exception as e:
    #     print_error(name)
    #     print_error(e)
    
        name = 'confirm_mo'

    # try:

        driver.find_element(By.XPATH, "//button[@name='action_confirm']").click()
        time.sleep(3)

        check_text = driver.find_element(By.XPATH, "//button[@aria-label='Current state']").text
        if check_text == 'CONFIRMED':
            print_ok(name)
        else:
            e = driver.find_element(By.XPATH, "//button[@aria-label='Current state']").text
            print_error(name,e)
        time.sleep(3)
    
    except Exception as e:
        print_error(name)
        print(e)

def print_ok(name):
    print(Fore.GREEN + name + " Pass")

def print_error(name):
    print(Fore.RED + name + " Fail")

if __name__ == "__main__":

    run()