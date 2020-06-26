import json
import requests
from datetime import datetime, timedelta
import hashlib

from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile

from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

from moneyball.models import MoneyBall, Upcoming

logger = get_task_logger(__name__)


def odds_request(region):
    odds_response = requests.get(
        settings.ODDS_API_URL,
        params={
            "api_key": settings.ODDS_API_KEY,
            "sport": "upcoming",
            "region": region,  # uk | us | eu | au
            "mkt": "h2h",  # h2h | spreads | totals
        },
    )
    logger.info('Remaining requests', odds_response.headers['x-requests-remaining'])
    logger.info('Used requests', odds_response.headers['x-requests-used'])
    return odds_response


def get_requests_status(odds_response):
    return (
        odds_response.headers["x-requests-remaining"],
        odds_response.headers["x-requests-used"],
    )


def get_upcoming_data(region="eu"):
    upcoming_data = odds_request(region).json()
    return [
        x
        for x in upcoming_data["data"]
        if datetime.fromtimestamp(x["commence_time"])
        > datetime.now() + timedelta(hours=1)
    ]


def get_and_concatenate_upcoming_data():
    all_upcomings = {k: get_upcoming_data(k) for k in ["eu", "uk", "us", "au"]}

    for region_name, region_request_value in all_upcomings.items():
        for row in region_request_value:
            row["sites_%s" % region_name] = row.pop("sites")
            row["sites_count_%s" % region_name] = row.pop("sites_count")

    list_of_rows = []
    for i, _ in enumerate(region_request_value):
        rows_i = [v[i] for k, v in all_upcomings.items()]
        concatenated_row = {}
        _ = [concatenated_row.update(d) for d in rows_i]
        list_of_rows.append(concatenated_row)
    return list_of_rows


@periodic_task(run_every=crontab(minute="0", hour="3"))
def refresh_upcoming_model(refresh_all=False):
    if refresh_all:
        data = get_and_concatenate_upcoming_data()
    else:
        data = get_upcoming_data()
    for row in data:
        teams = " vs ".join(row["teams"])
        hex_hash = (row["teams"][0], row["teams"][1], str(row["commence_time"]))
        hex_hash = hashlib.md5("".join(hex_hash).encode("utf-8")).hexdigest()
        timestamp = datetime.fromtimestamp(row["commence_time"])
        sport_key = row["sport_key"]

        json_file = ContentFile(json.JSONEncoder().encode(row))
        upcoming, _ = Upcoming.objects.update_or_create(
            hex_hash=hex_hash, timestamp=timestamp, teams=teams, sport_key=sport_key
        )
        upcoming.json_file.save(f"{hex_hash}.json", json_file, save=True)


@periodic_task(run_every=crontab(minute="*/15"))
def collect_moneyball():
    for upcoming in Upcoming.objects.all():
        if upcoming.timestamp < timezone.now() + timedelta(hours=1):
            # if upcoming.last_run < timezone.now() - timedelta(minutes=20):
            refresh_upcoming_model(refresh_all=True)
            _upcoming = Upcoming.objects.get(hex_hash=upcoming.hex_hash)
            # else:
            #     _upcoming = upcoming
            MoneyBall.objects.update_or_create(
                hex_hash=_upcoming.hex_hash,
                timestamp=_upcoming.timestamp,
                json_file=_upcoming.json_file,
                teams=_upcoming.teams,
                sport_key=_upcoming.sport_key,
            )
            _upcoming.delete()
