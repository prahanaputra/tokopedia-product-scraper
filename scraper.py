from os import mkdir, path, system, name
import json
import logging
from json import dump
from requests import get, post
from bs4 import BeautifulSoup as bs
from re import findall
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import pandas as pd
import time



class scraper():
    def __init__(self, shop_name):
        self.shop_url = f'https://tokopedia.com/{shop_name}'
        self.shop_name = shop_name
        self.header	= {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
        self.all_product = []
        self.get_id()
    
    def get_id(self):
        # try:
        req = post(self.shop_url, headers=self.header, timeout=3.000)
        if req.status_code == 200:
            proses = bs(req.text, 'html.parser')
            script_element = proses.find_all('script', type='text/javascript')
            script_content = script_element[3].string
            pattern = r'\{\\\"shop_ids\\\":\[(\d+)\]\}'
            matches = findall(pattern, script_content)
            if matches:
                self.shop_id = matches[0]
                print(f'Shop ID : {self.shop_id}>')
                self.get_data()
        #         else:
        #             print(f'  +-[!] ERROR: Tidak dapat mendapatkan ID Toko')
        #     else:
        #         print(f'  +-[!] Toko tidak ditemukan <Response Code [{req.status_code}]>')
        # except:
        #     print(f'  +-[!] Toko tidak valid <Response Code [{req.status_code}]>')

    def get_data(self, start=0):
        self.start = start

        json_url = f'https://ace.tokopedia.com/search/product/v3?shop_id={self.shop_id}&rows=200&start={self.start}&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product'
        request 	= get(json_url, headers=self.header)
        self.result	= request.json()

        if not path.isdir(self.shop_name):
            mkdir(self.shop_name)

        with open(f'{self.shop_name}/{self.shop_name}_[detail]_{self.start}.json', 'w') as file:
            json.dump(self.result, file)

        for i in self.result['data']['products']:
            self.all_product.append([
                i['name'],
                i['price_int'],
                i['url'],
                i['image_url_500'],
                i['category_breadcrumb'],
                i['department_id']
            ])
        print(f'Scraped Data = {len(self.all_product)}')
        self.total_product = self.result['header']['total_data_text']
        print(f'Total Product = {self.total_product}')
        self.product_check()
    

    def product_check(self):
        if len(self.all_product) < int(self.total_product):
            print('Repeat Get Data')
            next_start = self.start + 200
            self.get_data(next_start)
        else:
            print('OK')
            self.get_details()
    
    def get_details(self):
        self.product_details = []
        firefox_options = Options()
        firefox_options.headless = True
        firefox_options = webdriver.FirefoxOptions()
        # firefox_options.set_preference('geo.prompt.testing', True)
        # firefox_options.set_preference('geo.prompt.testing.allow', True)
        # firefox_options.set_preference('geo.provider.network.url','data:application/json,{"location": {"lat": -6.595038, "lng": 106.816635}, "accuracy": 100.0}')
        driver = webdriver.Firefox(options=firefox_options)
        
        for item in self.all_product:
            url = item[2]
            driver.get(url)
            try:
                wait = WebDriverWait(driver, 15)
                kurir_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Lihat Pilihan Kurir"]')))
                kurir_button.click()
            except NoSuchElementException:
                print ('no clickable button found')    
            try:
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.weight-value')))
                weight_element = driver.find_element(By.CSS_SELECTOR, 'div.weight-value')
                product_weight = weight_element.text
            except NoSuchElementException:
                print ('no weight information found')
            try:
                wait = WebDriverWait(driver, 10)
                description = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="lblPDPDescriptionProduk"]')))
                description_text = description.text
            except NoSuchElementException:
                print ('no description found')

            self.product_details.append([product_weight, description_text])
        driver.quit()
        self.save_data()
    
    def save_data(self):
        df = pd.DataFrame(data=zip(self.all_product, self.product_details),columns=['name', 'lprice', 'lurl', 'image_url', 'category', 'category_id', 'weight', 'description'])
        df.to_excel(f'{self.shop_name}/{self.shop_name}_[produk].xlsx', index=False)

