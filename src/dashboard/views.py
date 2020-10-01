import requests
from datetime import date
from urllib.parse import urljoin
from django.conf import settings

from django.shortcuts import render

from dashboard.bokeh import test_line_plot, test_hex_plot


def home(request):
    line_script, line_div = test_line_plot()
    hex_script, hex_div = test_hex_plot()

    return render(
        request,
        "dashboard/bokeh.html",
        {
            "line_script": line_script,
            "line_div": line_div,
            "hex_script": hex_script,
            "hex_div": hex_div,
        },
    )


def rates(request):
    usd = requests.get(urljoin(settings.NBP_API_URL, "usd/")).json()
    gbp = requests.get(urljoin(settings.NBP_API_URL, "gbp/")).json()
    today = date.today().strftime("%Y%m%d")
    gold = requests.get(
        urljoin(settings.GOLDAPI_URL, f"XAU/USD/{today}/"),
        headers={"x-access-token": settings.GOLDAPI_TOKEN},
    ).json()
    silver = requests.get(
        urljoin(settings.GOLDAPI_URL, f"XAG/USD/{today}/"),
        headers={"x-access-token": settings.GOLDAPI_TOKEN},
    ).json()
    metals = requests.get(
        urljoin(settings.METAL_API_URL, f"?access_key={settings.METAL_API_KEY}"),
        headers={"x-access-token": settings.GOLDAPI_TOKEN},
    ).json()
    # import pdb;pdb.set_trace()

    context = {
        "usd": usd["rates"][0]["mid"],
        "gbp": gbp["rates"][0]["mid"],
        "silver": metals["rates"]["XAG"],
        "gold": metals["rates"]["XAU"]
        # "silver_price": silver["price"],
        # "silver_change": silver["chp"],
        # "gold_price": gold["price"],
        # "gold_change": gold["chp"],
    }
    return render(request, "dashboard/rates.html", context)
