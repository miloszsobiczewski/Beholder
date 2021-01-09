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
    _SUBJECT_MAPPING = {RATE_SCRAPER: "GBP or USD exchange rate are promising ;)"}
    _TEMPLATE_MAPPING = {
        RATE_SCRAPER: {
            "message": "monitor/email/rate_scraper_template_message.txt",
            "html_message": "monitor/email/rate_scraper_template_message.html",
        }
    }

    def render(self, email_list, category, context):
        template = self._TEMPLATE_MAPPING[category]
        message = get_template(template_name=template["message"])
        html_message = get_template(template_name=template["html_message"])

        message = message.render(context)
        html_message = html_message.render(context)

        msg = EmailMultiAlternatives(
            self._SUBJECT_MAPPING[category], message, settings.EMAIL_SENDER, email_list
        )
        msg.attach_alternative(html_message, "text/html")
        return msg


message_renderer = MessageRenderer()


@app.task
def send_email(emails, subject, context):
    msg = message_renderer.render(emails, subject, context)
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

    mid_gbp = rate.mid_gbp
    mid_usd = rate.mid_usd

    logger.info(f"USD: {mid_usd}, GBP: {mid_gbp}")

    if (
        mid_gbp < settings.GBP_LOW_THRESHOLD
        or mid_gbp > settings.GBP_HIGH_THRESHOLD
        or mid_usd < settings.USD_LOW_THRESHOLD
        or mid_usd > settings.USD_HIGH_THRESHOLD
    ):
        context = {
            "GBP_MID": mid_gbp,
            "USD_MID": mid_usd,
        }
        send_email.delay(emails, RATE_SCRAPER, context)


@periodic_task(run_every=crontab(minute="10"))
def scrap_alior_exchange_rates():
    emails = Config.objects.get(key="users_email_list").value.split(",")
    rate = exchange_rate_scraper.scrap_alior()

    buy_gbp = rate.buy_gbp
    sell_gbp = rate.sell_gbp
    buy_usd = rate.buy_usd
    sell_usd = rate.sell_usd

    logger.info(
        f"BUY USD: {buy_usd}, SELL USD: {sell_usd}, BUY GBP: {buy_gbp}, SELL GBP: {sell_gbp}"
    )

    if (
        buy_gbp < settings.GBP_LOW_THRESHOLD
        or sell_gbp > settings.GBP_HIGH_THRESHOLD
        or buy_usd < settings.USD_LOW_THRESHOLD
        or sell_usd > settings.USD_HIGH_THRESHOLD
    ):
        context = {
            "GBP_BUY": buy_gbp,
            "GBP_SELL": sell_gbp,
            "USD_BUY": buy_usd,
            "USD_SELL": sell_usd,
        }
        send_email.delay(emails, RATE_SCRAPER, context)
