# Beholder
App used for:

## 1. Monitoring 
Checks the daily usage of data transfer and send emails notifications.
Usage is retrieved using selenium from the `Huawei B-315` router UI.

### Config variables
Set of variables to be set for appriopriate functioning of a program

1. `router_url`
2. `router_username`
3. `router_password`
4. `users_email_list` - comma separated.
5. `watch_date` - schedule date
6. `period_start_day` - day of the month
7. `data_retention` - in GB
8. `transfer_limit` - notification is sent when the remaining transfer drops below this value
9. `browser` - supports `chrome` (Chrome v79) and `firefox` browsers.

## Running the app
App will be run on Raspberry Pi 4. 

Docker is not used because of Pi low performance.

To start the app you need four services:


```bash
# 1. django - main app
cd src/
python manage.py runserver

# 2. redis - message broker
redis-server

# 3. celery - task que
celery -A config worker -l info

# 4. celery beat - scheduler
celery -A config beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

