import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display

from config.settings import BASE_DIR

from .models import Config, Usage


class RouterScraper:
    def __init__(self):
        driver = Config.objects.filter(key="driver").get().value
        driver_path = os.path.join(BASE_DIR, "static/", driver)

        if "gecko" in driver:
            display = Display(visible=0, size=(800, 600))
            display.start()
            # options = Options()
            # options.headless = True
            self.driver = webdriver.Firefox(
                # options=options,
                executable_path=driver_path
            )
        elif "chrome" in driver:
            self.driver = webdriver.Chrome(executable_path=driver_path)
        else:
            raise NotImplementedError

        self.url = Config.objects.filter(key="router_url").get().value
        self.username = Config.objects.filter(key="router_username").get().value
        self.password = Config.objects.filter(key="router_password").get().value
        self.driver.get(self.url)

    def login(self):
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div[1]/div/div/div[3]/div[2]"
        ).click()
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(
            self.username
        )
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
            self.password
        )
        self.driver.find_element_by_xpath('//*[@id="pop_login"]').click()

    def get_usage_stats(self):
        self.driver.find_element_by_xpath('//*[@id="statistic"]/span').click()
        usage_txt = self.driver.find_element_by_xpath(
            '//*[@id="month_used_value"]'
        ).text
        usage_list = usage_txt.split(" ")
        if usage_list[1] == "GB":
            usage = float(usage_list[0])
        elif usage_list[1] == "MB":
            usage = float(usage_list[0]) / 1024
        else:
            raise NotImplementedError
        Usage.objects.create(amount=usage)

    def restart_router(self):
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[1]/div[1]/div/div/div[2]/ul/li[6]/a/span"
        ).click()
        self.driver.find_element_by_xpath('//*[@id="system"]').click()
        self.driver.find_element_by_xpath('//*[@id="label_reboot"]').click()
        self.driver.find_element_by_xpath('//*[@id="undefined"]').click()
        self.driver.find_element_by_xpath('//*[@id="pop_confirm"]').click()

    def close(self):
        self.driver.quit()
