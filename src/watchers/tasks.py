from urllib.parse import urljoin

import requests
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.template.loader import get_template

from reminder.tasks import send_email

logger = get_task_logger(__name__)


def check_usd_rate():
    response = requests.get(urljoin(settings.NBP_API_URL, "usd/"))
    return response.json()["rates"][0]["mid"]


def check_gbp_rate():
    response = requests.get(urljoin(settings.NBP_API_URL, "gbp/"))
    return response.json()["rates"][0]["mid"]


@periodic_task(run_every=crontab(minute="0", hour="3"))
def check_rates():
    usd_rate = check_usd_rate()
    gbp_rate = check_gbp_rate()
    if usd_rate < float(settings.USD_THRESHOLD) or gbp_rate < float(
        settings.GBP_THRESHOLD
    ):
        text = f"""
        USD: {usd_rate}
        GBP: {gbp_rate}
        """
        context = {"name": "USD | GBP rates", "text": text, "deadline": ""}

        message = get_template(template_name="watchers/email/rates_message.txt")
        html_message = get_template(template_name="watchers/email/rates_message.html")

        send_email(
            ("sobiczewski.milosz@gmail.com",),
            "[Beholder] - USD | GBP rates notification",
            context,
            message,
            html_message,
        )
