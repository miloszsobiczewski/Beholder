import json
import logging
import os

import requests
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver

from monitor.models import ExchangeRate

logging.getLogger().setLevel(logging.INFO)


class ExchangeRateScraper:
    _OANDA_URL = "https://www1.oanda.com/currency/live-exchange-rates/"
    _ALIOR_URL = "https://kantor.aliorbank.pl"

    def scrap(self):
        response = requests.get(self._OANDA_URL)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.findAll("script", {"type": "text/javascript"})
        rates = json.loads(data[11].string[152:-6])

        mid_gbp = rates["GBP_PLN"]["ask"]
        mid_usd = rates["USD_PLN"]["ask"]

        return self._save_to_db(gbp_mid=mid_gbp, usd_mid=mid_usd)

    def _save_to_db(
        self,
        gbp_buy=None,
        gbp_mid=None,
        gbp_sell=None,
        usd_buy=None,
        usd_mid=None,
        usd_sell=None,
    ):
        return ExchangeRate.objects.create(
            buy_gbp=gbp_buy,
            mid_gbp=gbp_mid,
            sell_gbp=gbp_sell,
            buy_usd=usd_buy,
            mid_usd=usd_mid,
            sell_usd=usd_sell,
        )

    def scrap_alior(self):
        display = Display(visible=0, size=(1000, 800))
        display.start()

        logging.info("Initialized virtual display..")
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference(
            "browser.download.manager.showWhenStarting", False
        )
        firefox_profile.set_preference("browser.download.dir", os.getcwd())
        firefox_profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "text/csv"
        )

        logging.info("Prepared firefox profile..")

        browser = webdriver.Firefox(firefox_profile=firefox_profile)
        logging.info("Initialized firefox browser..")
        browser.get(self._ALIOR_URL)

        gbp_sell = browser.find_element_by_xpath(
            '//*[@id="alior-kantor-home"]/section[2]/div/div[3]/div/div[1]/span[2]'
        ).text
        gbp_buy = browser.find_element_by_xpath(
            '//*[@id="alior-kantor-home"]/section[2]/div/div[3]/div/div[2]/span[2]'
        ).text
        usd_buy = browser.find_element_by_xpath(
            '//*[@id="alior-kantor-home"]/section[2]/div/div[2]/div/div[1]/span[2]'
        ).text
        usd_sell = browser.find_element_by_xpath(
            '//*[@id="alior-kantor-home"]/section[2]/div/div[2]/div/div[2]/span[2]'
        ).text

        return self._save_to_db(
            gbp_buy=gbp_buy.replace(",", "."),
            gbp_sell=gbp_sell.replace(",", "."),
            usd_buy=usd_buy.replace(",", "."),
            usd_sell=usd_sell.replace(",", "."),
        )


exchange_rate_scraper = ExchangeRateScraper()
