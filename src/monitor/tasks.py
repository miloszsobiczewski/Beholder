import datetime
from decimal import Decimal

from django.conf import settings
from django.db.models import Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from config.celery import app

from .monitor import RouterScraper
from .models import Usage, Config

logger = get_task_logger(__name__)


@app.task
def send_email(email_list, subject, context):

    message = get_template(template_name="monitor/email/email_template_message.txt")
    html_message = get_template(
        template_name="monitor/email/email_template_message.html"
    )

    message = message.render(context)
    html_message = html_message.render(context)

    msg = EmailMultiAlternatives(subject, message, settings.EMAIL_SENDER, email_list)
    msg.attach_alternative(html_message, "text/html")
    msg.send()


@periodic_task(run_every=crontab(minute="*/1"))
def heartbeat():
    """
    What it says
    """
    logger.info(f" MILOSZ - heartbeat: {datetime.datetime.now()}")


# # @periodic_task(run_every=crontab(minute="*/1"))
# def heartbeat():
#     """
#     What it says
#     """
#     users_email_list = Config.objects.get(key="users_email_list").value
#     users_email_list = users_email_list.split(",")
#
#     subject = get_template(
#     template_name='monitor/email/email_template_subject.txt'
#     )
#     message = get_template(
#     template_name='monitor/email/email_template_message.txt'
#     )
#     html_message = get_template(
#     template_name='monitor/email/email_template_message.html'
#     )
#
#     d = {'username': "milosz"}
#     message = message.render(d)
#     html_message = html_message.render(d)
#
#     msg = EmailMultiAlternatives(subject, message, settings.EMAIL_SENDER, users_email_list)
#     msg.attach_alternative(html_message, "text/html")
#     msg.send()


@periodic_task(run_every=crontab(minute="*/5"))
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
    # scraper.restart_router()
    logger.info(f"check_usage : log out")
    scraper.close()


@periodic_task(run_every=crontab(minute="*/5"))
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
            "usage": usage,
            "remain": remain,
            "transfer_limit": transfer_limit,
            "retention": data_retention,
        }

        send_email.delay(
            users_email_list, "Data usage warning on Mobile Viking", context
        )
