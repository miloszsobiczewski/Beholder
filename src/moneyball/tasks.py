import os
import json
import requests
from datetime import datetime, timedelta
import hashlib

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

from moneyball.models import MoneyBall, Upcoming


def my_request(sport_key, verbose=False):
    odds_response = requests.get(
        "https://api.the-odds-api.com/v3/odds",
        params={
            "api_key": "c12e9667a637e7d84aa5a21018b2fd88",
            "sport": sport_key,
            "region": "uk",  # uk | us | eu | au
            "mkt": "h2h",  # h2h | spreads | totals
        },
    )
    # if verbose:
    #     print('Remaining requests', odds_response.headers['x-requests-remaining'])
    #     print('Used requests', odds_response.headers['x-requests-used'])
    odds_json = json.loads(odds_response.text)
    return odds_json


def get_upcoming_data():
    upcoming_data = my_request("upcoming")
    return [
        x
        for x in upcoming_data["data"]
        if (
            (
                datetime.fromtimestamp(x["commence_time"])
                > datetime.now() + timedelta(hours=1)
            )
            and (x["sport_key"].startswith("soccer"))
        )
    ]


def refresh_upcoming_model():
    for row in get_upcoming_data():
        hex_hash = row["teams"]
        hex_hash.append(str(row["commence_time"]))
        hex_hash = hashlib.md5("".join(hex_hash).encode("utf-8")).hexdigest()
        timestamp = datetime.fromtimestamp(row["commence_time"])

        file_name = os.path.join(settings.MEDIA_ROOT, f"{hex_hash}.json")
        with open(file_name, "w+") as f:
            # json.dump(json.JSONEncoder().encode(row), f)
            json_file = ContentFile(json.JSONEncoder().encode(row))
            # json_file = File(file=f, name=file_name)
            mb, _ = Upcoming.objects.update_or_create(
                hex_hash=hex_hash, timestamp=timestamp
            )
            mb.json_file.save(f"{hex_hash}.json", json_file, save=True)


def collect_moneyball():
    for upcoming in Upcoming.objects.all():
        if upcoming.timestamp > datetime.now() + timedelta(
            hours=1
        ) and upcoming.last_run < datetime.now() + timedelta(minutes=15):
            refresh_upcoming_model()
            _upcoming = Upcoming.objects.get(hex_hash=upcoming.hex_hash)
            MoneyBall.objects.update_or_create(
                hex_hash=_upcoming.hex_hash,
                timestamp=_upcoming.timestamp,
                json_file=_upcoming.json_file,
            )
