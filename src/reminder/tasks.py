from datetime import date

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from config.celery import app

from .models import Memory

logger = get_task_logger(__name__)


@app.task
def send_email(email_list, subject, context):

    message = get_template(template_name="reminder/email/email_template_message.txt")
    html_message = get_template(
        template_name="reminder/email/email_template_message.html"
    )

    message = message.render(context)
    html_message = html_message.render(context)

    msg = EmailMultiAlternatives(subject, message, settings.EMAIL_SENDER, email_list)
    msg.attach_alternative(html_message, "text/html")
    msg.send()


@periodic_task(run_every=crontab(minute="0", hour="3"))
def run_reminder():
    """
    Iterate through all memories and send reminder messages
    """

    memories = Memory.objects.filter(active=True)

    for memory in memories:
        context = {
            "name": memory.name,
            "text": memory.text,
            "deadline": memory.deadline
        }
        if memory.date == date.today():
            send_email.delay(settings.DEFAULT_USER_LIST.split(","), f"[Beholder] - {memory.name} - reminder", context)
        elif memory.day == date.today().day and memory.active is True:
            send_email.delay(settings.DEFAULT_USER_LIST.split(","), f"[Beholder] - {memory.name} - reminder", context)
            memory.active = False
            memory.save()
        else:
            pass
