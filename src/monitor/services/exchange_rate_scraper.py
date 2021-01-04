import json

import requests
from bs4 import BeautifulSoup

from monitor.models import ExchangeRate


class ExchangeRateScraper:
    _OANDA_URL = "https://www1.oanda.com/currency/live-exchange-rates/"

    def scrap(self):
        response = requests.get(self._OANDA_URL)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.findAll("script", {"type": "text/javascript"})
        rates = json.loads(data[11].string[152:-6])

        gbp = rates["GBP_PLN"]["ask"]
        usd = rates["USD_PLN"]["ask"]
        self._save_to_db(gbp, usd)

    def _save_to_db(self, gbp, usd):
        ExchangeRate.objects.get_or_create(
            mid_gbp_exchange_rate=gbp, mid_usd_exchange_rate=usd
        )


exchange_rate_scraper = ExchangeRateScraper()
