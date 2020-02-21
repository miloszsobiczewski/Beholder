# Beholder
Monitoring app

## Config variables
Set of variables to be set for appriopriate functioning of a program

1. `router_url`
2. `router_username`
3. `router_password`
4. `users_email_list`
5. `watch_date`
6. `period_start_day`
7. `data_retention`
8. `transfer_limit`

## Run
First
```bash
cd src/
```
django:
```bash
python manage.py runserver
```
redis:
```bash
redis-server
```

celery:
```bash
celery -A config worker -l info
```
celery-beat:
```bash
celery -A config beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
## todo:
[ ] add redis