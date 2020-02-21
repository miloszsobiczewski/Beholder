import os
from selenium import webdriver

from config.settings import BASE_DIR

from .models import Config, Usage


class RouterScraper:
    def __init__(self):
        browser = Config.objects.filter(key="browser").get().value
        if browser == "chrome":
            self.driver = webdriver.Chrome(
                executable_path=os.path.join(BASE_DIR, "static/chromedriver")
            )
        elif browser == "firefox":
            self.driver = webdriver.Firefox(
                executable_path=os.path.join(BASE_DIR, "static/geckodriver")
            )
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
        usage = self.driver.find_element_by_xpath('//*[@id="month_used_value"]').text
        usage = float(usage[: usage.find(" ")])
        Usage.objects.create(amount=usage)

    def restart_router(self):
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[1]/div[1]/div/div/div[2]/ul/li[6]/a/span"
        ).click()
        self.driver.find_element_by_xpath('//*[@id="system"]').click()
        self.driver.find_element_by_xpath('//*[@id="label_reboot"]').click()
        self.driver.find_element_by_xpath('//*[@id="undefined"]').click()

    def close(self):
        self.driver.quit()
