import datetime
from decimal import Decimal

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.template.loader import get_template

from config.celery import app

from monitor.models import Config, Usage
from monitor.monitor import RouterScraper
from monitor.services.exchange_rate_scraper import exchange_rate_scraper

logger = get_task_logger(__name__)

RATE_SCRAPER = "rate_scraper"


class MessageRenderer:
    _SUBJECT_MAPPING = {
        RATE_SCRAPER: "GBP or USD exchange rate are promising ;)"
    }
    _TEMPLATE_MAPPING = {
        RATE_SCRAPER: {
            "message": "monitor/email/rate_scraper_template_message.txt",
            "html_message": "monitor/email/rate_scraper_template_message.html"
        }
    }

    def render(self, email_list, category, context):
        template = self._TEMPLATE_MAPPING[category]
        message = get_template(template_name=template["message"])
        html_message = get_template(
            template_name=template["html_message"]
        )

        message = message.render(context)
        html_message = html_message.render(context)

        msg = EmailMultiAlternatives(self._SUBJECT_MAPPING[category], message, settings.EMAIL_SENDER, email_list)
        msg.attach_alternative(html_message, "text/html")
        return msg


message_renderer = MessageRenderer()


@app.task
def send_email(msg):
    msg.send()


# @periodic_task(run_every=crontab(minute="0", hour="3"))
def check_usage():
    """
    Function is checking the actual value of data usage on router and saves it to django model
    in the end function is triggering router restart to refresh the internet connection
    """

    logger.info(f"check_usage : init scraper")
    scraper = RouterScraper()
    logger.info(f"check_usage : log into router")
    scraper.login()
    logger.info(f"check_usage : get stats")
    scraper.get_usage_stats()
    scraper.restart_router()
    logger.info(f"check_usage : log out")
    scraper.close()


# @periodic_task(run_every=crontab(minute="15", hour="3"))
def monitor_usage():
    """
    Function is checking if the specified period data usage is close to set retention
    if yes it is going to trigger an e-mail notification to set of users
    """

    logger.info("monitor_usage : run")

    period_start_day = int(Config.objects.get(key="period_start_day").value)
    today = datetime.date.today()
    if today.day > period_start_day:
        start_date = datetime.date(today.year, today.month, period_start_day)
        end_date = datetime.date(today.year, today.month + 1, period_start_day)
    else:
        if today.month == 1:
            start_date = datetime.date(today.year - 1, 12, period_start_day)
        else:
            start_date = datetime.date(today.year, today.month - 1, period_start_day)
        end_date = datetime.date(today.year, today.month, period_start_day)

    data_retention = Config.objects.get(key="data_retention").value
    transfer_limit = Decimal(Config.objects.get(key="transfer_limit").value)
    users_email_list = Config.objects.get(key="users_email_list").value
    usage = (
        Usage.objects.filter(date__range=(start_date, end_date))
        .aggregate(Sum("amount"))
        .get("amount__sum")
    )
    if not usage:
        usage = 0

    users_email_list = users_email_list.split(",")
    remain = transfer_limit - usage

    logger.info("monitor_usage run: ", f"{usage}/{transfer_limit}")

    if usage > float(data_retention):
        context = {
            "usage": float(usage),
            "remain": float(remain),
            "transfer_limit": transfer_limit,
            "retention": data_retention,
        }

        # send_email.delay(
        #     users_email_list, "Data usage warning on Mobile Viking", context
        # )


@periodic_task(run_every=crontab(minute="5"))
def scrap_exchange_rates():
    emails = Config.objects.get(key="users_email_list").value.split(",")
    rate = exchange_rate_scraper.scrap()

    gbp_rate = rate.mid_gbp_exchange_rate
    usd_rate = rate.mid_usd_exchange_rate

    logger.info(f"USD: {usd_rate}, GBP: {gbp_rate}")

    if gbp_rate < settings.GBP_LOW_THRESHOLD or gbp_rate > settings.GBP_HIGH_THRESHOLD or usd_rate < settings.USD_LOW_THRESHOLD or usd_rate > settings.USD_HIGH_THRESHOLD:
        context = {
            "GBP_MID": gbp_rate,
            "USD_MID": usd_rate,
        }
        msg = message_renderer.render(emails, RATE_SCRAPER, context)
        send_email.delay(msg)
