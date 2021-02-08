from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import io, json,os
import time
soup = BeautifulSoup("")
import platform

def init_driver_window():
    chrome_options = Options()

    # chrome_options.add_argument("ignore-certificate-errors")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def init_driver():
    chrome_options = Options()
    # chrome_options.add_argument("ignore-certificate-errors")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-data-dir=selenium")
    chrome_options.add_argument("--window-size=1920x1080")
    if 'ubuntu' in platform.platform().lower() or 'linux' in platform.platform().lower():
        print('using ubuntu or linux')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        cur_dir = os.getcwd()
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=cur_dir+ "/window_driver"+"/chromedriver.exe")
    return driver




class Bot():
    def __init__(self, username, password, link_login, link_search,output_folder):
        try:
            self.browser = init_driver()
            self.username = username
            self.password = password
            self.status = 'init'
            self.number_post = 0
            self.time_block = 0
            self.start_block = None
            self.link_login=link_login
            self.link_search = link_search
            self.output_folder= output_folder
        except Exception as e:
            print(e)
            self.status = str(traceback.format_exc())

    def login(self):
        try:
            self.browser.get(self.link_login)
            usernameInput= WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located((By.XPATH, '''//input[@id='__BVID__13']
''')))
            passwordInput = WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located((By.XPATH, '''//input[@id='__BVID__16']
''')))
            usernameInput.send_keys(self.username)
            passwordInput.send_keys(self.password)
            self.status = 'OK'
        except Exception as e:
            print(e)
            self.status = str('LOGIN_FAILED')
    def crawl_data_page(self,soup,search_text,count_page):
        try:
            name_to_style = {
                "No.": 'grid-row: 1 / span 2; grid-column-start: 1;',
                "Property No": "grid-row-start: 1; grid-column: 2 / span 3;",
                "Property item": "grid-row-start: 1; grid-column: 5 / span 5;",
                "Occupied area": "grid-row-start: 1; grid-column: 10 / span 3;",
                "location": "grid-row-start: 1; grid-column: 13 / span 12;",
                "Transaction mode": "grid-row-start: 2; grid-column: 2 / span 3;",
                "price": "grid-row-start: 2; grid-column: 5 / span 3;",
                "Area of use": "grid-row-start: 2; grid-column: 8 / span 2;",
                "mxm Unit price": "grid-row-start: 2; grid-column: 10 / span 3;",
                "Building name": "grid-row-start: 2; grid-column: 13 / span 6;",
                "Location floor": "grid-row-start: 2; grid-column: 19 / span 4;",
                "Floor plan": "grid-row-start: 2; grid-column: 23 / span 2;",
                "Trading conditions": "grid-row-start: 3; grid-column: 2 / span 3;",
                "Management fee": "grid-row-start: 3; grid-column: 5 / span 3;",
                "Unit price per tsubo": "grid-row-start: 3; grid-column: 10 / span 3;",
                "Stations along the line": "grid-row-start: 3; grid-column: 13 / span 6;",
                "traffic": "grid-row-start: 3; grid-column: 19 / span 6;",
                "Trade name": "grid-row-start: 4; grid-column: 13 / span 12;",
                "Date of construction": "grid-row-start: 5; grid-column: 5 / span 4;",
                "phone number": "grid-row-start: 5; grid-column: 13 / span 6;"
            }

            body_row = soup.find_all('div', class_='p-table-body-row')
            list_data_row = []
            for row in body_row:

                data_row = {}
                for style in name_to_style:
                    try:
                        list_item = row.find('div', attrs={'style': name_to_style[style]})
                        if list_item is not None:
                            data_row[style] = list_item.string
                    except Exception as e:
                        print(e)
                list_data_row.append(data_row)

            with io.open(self.output_folder+'/'+ search_text+'/'+ search_text+'_'+'page_'+str(count_page)+ '.txt', 'w',
                         encoding='utf-8') as f:
                f.write(json.dumps(list_data_row, ensure_ascii=False))
        except Exception as e:
            print(e)
            self.status = str('run_to_page_file failed')


    def run_to_page_file(self,search_text):
        try:
            self.browser.get(self.link_search)
            property_type_1_select_box =Select(WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located((By.XPATH, '''//select[@id='__BVID__41']'''))))
            property_type_1_select_box.select_by_value('03')

            prefecturesInput = WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located((By.XPATH, '''//input[@id='__BVID__94']''')))
            prefecturesInput.send_keys(search_text)
        except Exception as e:
            print(e)
            self.status = str('run_to_page_file failed')

        try:
            btnSearch = WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ''' div.col-sm-3.col-4:nth-child(4) > button.btn.p-button.btn-primary.btn-block.px-0''')))
            btnSearch.send_keys(Keys.COMMAND, Keys.ENTER)
        except Exception as e:
            print(e)
            self.status = str('run_to_page_file failed')

        OKclick=False
        try:
            btnOK = WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located(
                (By.XPATH, '''//button[@class='btn btn-primary'][.='OK']''')))
            btnOK.send_keys(Keys.COMMAND, Keys.ENTER)
            OKclick= True
        except Exception as e:
            print(e)
            self.status = str('run_to_page_file failed')

        if OKclick==False:
            try:
                btnOK = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located(
                    (By.XPATH, '''//font[text()='OK']/ancestor::font/ancestor::button[@class='btn btn-primary']''')))
                btnOK.send_keys(Keys.COMMAND, Keys.ENTER)
            except Exception as e:
                print(e)
                self.status = str('run_to_page_file failed')
        crawl_start=True
        count_page=1
        while crawl_start:
            try:

                # print('''//li[@class='page-item active']//button[contains(text(), "{0}") and @class='page-link']'''.format(str(count_page)))
                btn_active=WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located(
                    (By.XPATH, '''//div[@class='p-table-body-row']//div[contains(text(), "{0}") and @class='p-table-body-item large']'''.format(str((count_page-1)*50+1)))))
                # print(btn_active)

                page_source = self.browser.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                self.crawl_data_page(soup,search_text,count_page)
                count_page=count_page+1
                btnNextPage = WebDriverWait(self.browser, 15).until(ec.visibility_of_element_located(
                    (By.XPATH, '''//button[@aria-label='Go to next page'][@class='page-link']''')))
                btnNextPage.send_keys(Keys.COMMAND, Keys.ENTER)
                # time.sleep(1)
            except Exception as e:
                print(e)
                self.status = str('run_to_page_file failed')
                crawl_start=False

        print("END")
    def check_login(self):
        try:
            self.browser.get(self.link_search)
            try:
                btnSearch = WebDriverWait(self.browser, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ''' div.col-sm-3.col-4:nth-child(4) > button.btn.p-button.btn-primary.btn-block.px-0''')))
                return True
            except:
                print("not OK")
                return False
        except Exception as e:
            print(e)
            return  False

    def close(self):
        self.browser.close()

    def to_json(self):
        return {'username': self.username,
                'password': self.password, 'status': self.status, 'number_post': self.number_post,
                'time_block': self.time_block
                }


import os.path

# if __name__ == "__main__":
#     username = "lane287279067"
#     password = "To01111995"
#     t = Bot(username, password)
#     t.login()

