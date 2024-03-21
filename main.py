import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os


# Creating Main class
class SmartPrixWebScraper:

    def __init__(self):
        self.page = 1
        self.laptop = 1
        self.driver = webdriver.Chrome()
        self.url = 'https://www.smartprix.com/laptops'
        # fill_in = {'name' : [],'price' : [],'spec_score' : [],'votes' : [],'user_rating': [], 'os' : [],'utility' : [],'thickness' : [],'weight': [],'warranty' :[],'screen_size' : [],'resolution' : [],'ppi' : [],'battery' : [],'screen_feature1' : [],'screen_feature2' : [],'processor_name' : [],'processor_speed' : [],'no_cores' : [],'caches' : [],'graphics_card' : [],'rom_memory' : [],'internal_memory' : [],'port_connection' : [],'wireless_connection' : [],'usb_ports' : [],'hardware_features' : []}
        self.file_name = 'smartprix_laptop4.csv'
        # self.df = pd.DataFrame()## CONFUSION
        self.initialise_driver()

    # Initialize the driver
    def initialise_driver(self):
        self.driver.get(self.url)
        time.sleep(2)

    # Scrolling all the way down
    def scrolling_allDown(self):

        new_height = 0
        print('New height: ', new_height)
        old_height = self.driver.execute_script('return document.body.scrollHeight')
        print('Old height: ', old_height)  ## self.old_height??

        while True:
            print('Page no. - ', self.page)
            is_ready = self.driver.execute_script('return document.readyState')
            if is_ready == 'complete':
                self.driver.execute_script(f' window.scrollTo({new_height}, {old_height * .625})')
                print('Scrolled down')
                try:
                    load_next = WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "sm-load-more")))
                    load_next.click()
                    print('Load Next CLICKED')
                    self.page += 1
                    time.sleep(2)
                    new_height = old_height
                    print('New height: ', new_height)
                    old_height = self.driver.execute_script('return document.body.scrollHeight')
                    print('Old height: ', old_height)
                    if old_height == new_height:
                        break
                except:
                    break

    def traversing_and_extracting(self):
        duck_up = None

        data = self.driver.page_source
        soup = BeautifulSoup(data, 'lxml')
        containers = soup.find_all('div', class_="sm-product has-tag has-features has-actions")
        print('Total Laptops: ', len(containers))
        # newcode
        current_window = self.driver.current_window_handle

        with open(self.file_name, 'a', encoding='utf-8') as file:

            for box in containers:
                fill_in = {'name': [], 'price': [], 'spec_score': [], 'votes': [], 'user_rating': [], 'os': [],
                           'utility': [], 'thickness': [], 'weight': [], 'warranty': [], 'screen_size': [],
                           'resolution': [], 'ppi': [], 'battery': [], 'screen_feature1': [], 'screen_feature2': [],
                           'processor_name': [], 'processor_speed': [], 'no_cores': [], 'caches': [],
                           'graphics_card': [], 'rom_memory': [], 'internal_memory': [], 'port_connection': [],
                           'wireless_connection': [], 'usb_ports': [], 'hardware_features': []}

                a_tag = box.find('a', class_='name clamp-2')
                link = a_tag['href']

                # javascript
                try:
                    self.driver.execute_script("window.open('" + link + "', 'newtab');")
                    is_ready = self.driver.execute_script('return document.readyState')
                    if is_ready == 'complete':
                        time.sleep(2)
                        duck_up = 1
                    else:
                        self.driver.refresh()

                except Exception as e0:
                    duck_up = 0
                    print('Page could not be loaded: ', e0)
                    continue
                try:
                    # NEW WINDOW
                    new_window = [window for window in self.driver.window_handles if window != current_window][0]
                    self.driver.switch_to.window(new_window)
                    time.sleep(2)
                    WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pg-prd')))
                except:
                    self.driver.refresh()
                    print('Data Parsing ERROR')
                    continue
                try:
                    print('LAPTOP NO. - ', self.laptop)
                    if is_ready == 'complete':
                        try:
                            data2 = self.driver.page_source  ## GIVING ERROR
                        except Exception as e1:
                            self.driver.refresh()
                            # time.sleep(1)
                            print('Page could not be loaded', e1)
                        soup2 = BeautifulSoup(data2, 'lxml')

                    y = soup2.find_all('ul',
                                       class_='group')  ## WHY THE FUCK IS IT NOT WORKING?, EDIT: Working after changing position of #newcode!
                    print('Total items: ', len(y))
                except:
                    continue

                if len(y) == 0 or len(y) == None:
                    if duck_up == 0:
                        fill_in['name'].append(np.nan)
                        fill_in['price'].append(np.nan)
                        fill_in['spec_score'].append(np.nan)
                        fill_in['votes'].append(np.nan)
                        fill_in['user_rating'].append(np.nan)

                    fill_in['os'].append(np.nan)
                    fill_in['utility'].append(np.nan)
                    fill_in['thickness'].append(np.nan)
                    fill_in['weight'].append(np.nan)
                    fill_in['warranty'].append(np.nan)

                    fill_in['screen_size'].append(np.nan)
                    fill_in['resolution'].append(np.nan)
                    fill_in['ppi'].append(np.nan)
                    fill_in['screen_feature1'].append(np.nan)
                    fill_in['screen_feature2'].append(np.nan)

                    fill_in['processor_name'].append(np.nan)
                    fill_in['processor_speed'].append(np.nan)
                    fill_in['no_cores'].append(np.nan)
                    fill_in['caches'].append(np.nan)
                    fill_in['graphics_card'].append(np.nan)
                    fill_in['rom_memory'].append(np.nan)
                    fill_in['internal_memory'].append(np.nan)

                    fill_in['port_connection'].append(np.nan)
                    fill_in['wireless_connection'].append(np.nan)
                    fill_in['usb_ports'].append(np.nan)
                    fill_in['hardware_features'].append(np.nan)

                    fill_in['battery'].append(np.nan)

                else:

                    # Extracting the name

                    info_name = soup2.find('h1')
                    try:
                        fill_in['name'].append(info_name.text)
                        print(info_name.text)
                    except:
                        fill_in['name'].append(np.nan)

                    # Extracting the price

                    info_price = soup2.find('div', class_="price")
                    try:
                        fill_in['price'].append(info_price.text)
                        print(info_price.text)
                    except:
                        fill_in['price'].append(np.nan)

                    # Extracting spec score

                    if soup2.find('div', class_='score rank-1-bg'):
                        info_score = soup2.find('div', class_='score rank-1-bg')
                        try:
                            fill_in['spec_score'].append(info_score.text)
                        except:
                            fill_in['spec_score'].append(np.nan)
                    elif soup2.find('div', class_='score rank-2-bg'):
                        info_score = soup2.find('div', class_='score rank-2-bg')
                        try:
                            fill_in['spec_score'].append(info_score.text)
                        except:
                            fill_in['spec_score'].append(np.nan)
                    elif soup2.find('div', class_='score rank-3-bg'):
                        info_score = soup2.find('div', class_='score rank-3-bg')
                        try:
                            fill_in['spec_score'].append(info_score.text)
                        except:
                            fill_in['spec_score'].append(np.nan)
                    elif soup2.find('div', class_='score rank-4-bg'):
                        info_score = soup2.find('div', class_='score rank-4-bg')
                        try:
                            fill_in['spec_score'].append(info_score.text)
                        except:
                            fill_in['spec_score'].append(np.nan)
                    else:
                        fill_in['spec_score'].append(np.nan)

                    # Extracting no. of votes AND reviews (in same text)

                    info_no_votes = soup2.find('div', class_='pg-prd-rating')
                    try:
                        fill_in['votes'].append(info_no_votes.text)
                    except:
                        fill_in['votes'].append(np.nan)

                    page_height = self.driver.execute_script('return document.body.scrollHeight')
                    time.sleep(1)

                    # Extracting user_rating
                    if soup2.find('span', class_='text rank-1-bg'):
                        rating = soup2.find('span', class_='text rank-1-bg')
                        try:
                            fill_in['user_rating'].append(rating.text)
                        except:
                            fill_in['user_rating'].append(np.nan)
                    elif soup2.find('span', class_='text rank-2-bg'):
                        rating = soup2.find('span', class_='text rank-2-bg')
                        try:
                            fill_in['user_rating'].append(rating.text)
                        except:
                            fill_in['user_rating'].append(np.nan)
                    elif soup2.find('span', class_='text rank-3-bg'):
                        rating = soup2.find('span', class_='text rank-3-bg')
                        try:
                            fill_in['user_rating'].append(rating.text)
                        except:
                            fill_in['user_rating'].append(np.nan)

                    try:

                        x0 = y[0].find_all('li')
                        print('Total felements in box 1: ', len(x0))

                        # Extrtacting OS
                        try:
                            fill_in['os'].append(x0[0].text)
                        except:
                            fill_in['os'].append(np.nan)

                        # Extracting Utility
                        try:
                            fill_in['utility'].append(x0[1].text)
                        except:
                            fill_in['utility'].append(np.nan)

                        # Extracting Thickness
                        try:
                            fill_in['thickness'].append(x0[2].text)
                        except:
                            fill_in['thickness'].append(np.nan)

                        # Extracting Weight
                        try:
                            fill_in['weight'].append(x0[3].text)
                        except:
                            fill_in['weight'].append(np.nan)

                        # Extracting Warranty
                        try:
                            fill_in['warranty'].append(x0[4].text)
                        except:
                            fill_in['warranty'].append(np.nan)
                    except:
                        fill_in['os'].append(np.nan)
                        fill_in['utility'].append(np.nan)
                        fill_in['thickness'].append(np.nan)
                        fill_in['weight'].append(np.nan)
                        fill_in['warranty'].append(np.nan)

                    try:
                        x1 = y[1].find_all('li')
                        print('Total elements in box 2: ', len(x1))

                        # Extracting display size
                        try:
                            fill_in['screen_size'].append(x1[0].text)
                        except:
                            fill_in['screen_size'].append(np.nan)

                        # Extracting display resolution
                        try:
                            fill_in['resolution'].append(x1[1].text)
                        except:
                            fill_in['resolution'].append(np.nan)

                        # Extracting ppi
                        try:
                            fill_in['ppi'].append(x1[2].text)
                        except:
                            fill_in['ppi'].append(np.nan)

                        # Extracting screen features
                        try:
                            fill_in['screen_feature1'].append(x1[3].text)
                        except:
                            fill_in['screen_feature1'].append(np.nan)
                        try:
                            fill_in['screen_feature2'].append(x1[4].text)
                        except:
                            fill_in['screen_feature2'].append(np.nan)
                    except:
                        fill_in['screen_size'].append(np.nan)
                        fill_in['resolution'].append(np.nan)
                        fill_in['ppi'].append(np.nan)
                        fill_in['screen_feature1'].append(np.nan)
                        fill_in['screen_feature2'].append(np.nan)

                    try:

                        x2 = y[2].find_all('li')
                        print('Total elements in box 3: ', len(x2))

                        # Extracting the processor name
                        try:
                            fill_in['processor_name'].append(x2[0].text)
                        except:
                            fill_in['processor_name'].append(np.nan)

                        # Extracting processor_speed
                        try:
                            fill_in['processor_speed'].append(x2[1].text)
                        except:
                            fill_in['processor_speed'].append(np.nan)

                        # Extracting number of cores
                        try:
                            fill_in['no_cores'].append(x2[2].text)
                        except:
                            fill_in['no_cores'].append(np.nan)

                        # Extracting cache size
                        try:
                            fill_in['caches'].append(x2[3].text)
                        except:
                            fill_in['caches'].append(np.nan)

                        # Extracting graphics card
                        try:
                            fill_in['graphics_card'].append(x2[4].text)
                        except:
                            fill_in['graphics_card'].append(np.nan)

                        # Extracting ROM memory
                        try:
                            fill_in['rom_memory'].append(x2[5].text)
                        except:
                            fill_in['rom_memory'].append(np.nan)

                        # Extracting Internal memory
                        try:
                            fill_in['internal_memory'].append(x2[6].text)
                        except:
                            fill_in['internal_memory'].append(np.nan)
                    except:
                        fill_in['processor_name'].append(np.nan)
                        fill_in['processor_speed'].append(np.nan)
                        fill_in['no_cores'].append(np.nan)
                        fill_in['caches'].append(np.nan)
                        fill_in['graphics_card'].append(np.nan)
                        fill_in['rom_memory'].append(np.nan)
                        fill_in['internal_memory'].append(np.nan)

                    try:

                        x3 = y[3].find_all('li')
                        print('Total elements in box 4: ', len(x3))

                        # Extracting port_connection
                        try:
                            fill_in['port_connection'].append(x3[0].text)
                        except:
                            fill_in['port_connection'].append(np.nan)

                        # Extracting wireless_connection
                        try:
                            fill_in['wireless_connection'].append(x3[1].text)
                        except:
                            fill_in['wireless_connection'].append(np.nan)

                        # Extracting usb ports
                        try:
                            fill_in['usb_ports'].append(x3[2].text)
                        except:
                            fill_in['usb_ports'].append(np.nan)

                        # Extracting hardware features
                        try:
                            fill_in['hardware_features'].append(x3[3].text)
                        except:
                            fill_in['hardware_features'].append(np.nan)
                    except:
                        fill_in['port_connection'].append(np.nan)
                        fill_in['wireless_connection'].append(np.nan)
                        fill_in['usb_ports'].append(np.nan)
                        fill_in['hardware_features'].append(np.nan)

                    try:
                        x4 = y[4].find_all('li')
                        print('Total elements in box 5: ', len(x4))
                        fill_in['battery'].append(x4[0].text)
                    except:
                        fill_in['battery'].append(np.nan)
                    self.laptop += 1
                try:
                    df = pd.DataFrame(fill_in)
                except:
                    print(fill_in)

                df.to_csv(file, mode='a', index=False, header=False if self.file_name else True)

        return current_window

    def main_prog(self):
        # scrolling all the way down
        self.scrolling_allDown()

        # opening up and fetching data from each item
        present_window = self.traversing_and_extracting()

        # switching back to main window
        self.driver.switch_to.window(present_window)


if __name__ == '__main__':
    start = time.time()
    class_object = SmartPrixWebScraper()
    class_object.main_prog()
    print("Total TIME taken: ", round((time.time() - start) / 3600, 2), 'hrs')
