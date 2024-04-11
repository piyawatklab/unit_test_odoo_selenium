from colorama import Fore, init

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from seleniumbase import Driver

import time

from libs.settings import USERNAME_LOGIN , PASSWORD_LOGIN

init()

url = 'https://mp-dev.almacom.co.th/web#action=447&model=sale.order&view_type=list&cids=2&menu_id=261'

json_data = {
    "partner_id" : 'MP055758',
    "sales_series" : 'Head Office',
    "sales_channel" : 'MP B2B Project',
    "sales_method": 'MPS Project',
    "product":[{
        "product_id": 'TTT001',
        "product_uom_qty": 3,
    },{
        "product_id": 'TTT002',
        "product_uom_qty": 4,
    },
    ]
}

def run():
    name = 'open_odoo'
    try:
        driver = Driver(uc=True)
        # driver = Driver(uc=True,headless=True)
        driver.get(url)
        time.sleep(3)
        print_ok(name)

    except Exception as e:
        print_error(name) 
        print_error(e)

    name = 'login_odoo'
    try:
        driver.find_element(By.XPATH, "//input[@name='login']").send_keys(USERNAME_LOGIN)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(PASSWORD_LOGIN)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        check_text = driver.find_element(By.XPATH, "//span[@class='text-truncate']").text
        if check_text == 'Sales Orders':
            print_ok(name)
        else:
            e = driver.find_element(By.XPATH, "//div[@class='o_notification_manager']").text
            print_error(name,e)

    except Exception as e:
        print_error(name) 
        print_error(e)
    
    name = 'create_sales_order'
    try:
        driver.find_element(By.XPATH, "//button[@class='btn btn-primary o_list_button_add']").click()
        time.sleep(3)
        input_partner = driver.find_element(By.XPATH, "//input[@id='partner_id']")
        input_partner.send_keys(json_data["partner_id"])
        input_partner.send_keys(Keys.ENTER)
        time.sleep(1)
        input_sale_series = driver.find_element(By.XPATH, "//input[@id='sale_series_id']")
        input_sale_series.send_keys(json_data["sales_series"])
        input_sale_series.send_keys(Keys.ENTER)
        time.sleep(1)
        input_sale_channel = driver.find_element(By.XPATH, "//input[@id='sale_channel_id']")
        input_sale_channel.send_keys(json_data["sales_channel"])
        input_sale_channel.send_keys(Keys.ENTER)
        time.sleep(1)
        input_sale_method = driver.find_element(By.XPATH, "//input[@id='sale_method_id']")
        input_sale_method.send_keys(json_data["sales_method"])
        input_sale_method.send_keys(Keys.ENTER)
        time.sleep(1)

        add_line = driver.find_element(By.XPATH, "//a[contains(text(), 'Add a product')]")
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

            td_add = tr_add[i].find_element(By.XPATH, ".//td[@name='product_uom_qty']")
            td_add.click()
            time.sleep(3)
            td_add.find_element(By.XPATH, ".//input[@type='text']").send_keys(product_list[i]["product_uom_qty"])
            time.sleep(1)
            td_add.send_keys(Keys.ENTER)
            time.sleep(3)

            # td_add = tr_add.find_element(By.XPATH, ".//td[@name='price_unit']")
            # td_add.click()
            # time.sleep(3)
            # td_add.find_element(By.XPATH, ".//input[@type='text']").send_keys(json_data["product"][0]["price_unit"])
            # time.sleep(1)
            # td_add.send_keys(Keys.ENTER)
            # time.sleep(3)

        print_ok(name)
    
    except Exception as e:
        print_error(name)
        print_error(e)
    
    name = 'save_sales_order'
    try:

        driver.find_element(By.XPATH, "//button[@data-tooltip='Save manually']").click()
        time.sleep(3)

        check_text = driver.find_element(By.XPATH, "//span[@class='text-truncate']").text
        if check_text != 'New':
            print_ok(name)
            print('SO : ' + check_text)
        else:
            e = driver.find_element(By.XPATH, "//div[@class='o_notification_manager']").text
            print_error(name,e)
    
    except Exception as e:
        print_error(name)
        print_error(e)

def print_ok(name):
    print(Fore.GREEN + name + " Pass")

def print_error(name):
    print(Fore.RED + name + " Fail")

if __name__ == "__main__":

    run()