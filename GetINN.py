from selenium import webdriver
from selenium.webdriver.support.ui import Select
from timeit import time

driver = webdriver.Chrome()
driver.get('https://service.nalog.ru/inn.do')

fields = {
    "fam": "иванов",
    "nam": "иван",
    "otch": "иванович",
    "bdate": "01011900",
    "bplace": "ленинград",
    "docno": "4000123456",
    "docdt": "01011920",
    "doctype": "21 - паспорт гражданина российской федерации"
}

for param in fields.keys():
    time.sleep(0.01)
    name = fields[param]
    if param == 'doctype':
        field = driver.find_element_by_id('uni_select_2')
        field.clear()
        field.send_keys(name)
    else:
        field = driver.find_element_by_name(param)
        for letter in name:
            field.send_keys(letter)
field = driver.find_element_by_id("captcha")
field.send_keys("")
