from random import randrange

from datetime import timedelta
from django.utils import timezone

from amper.utils import random_datetime, time_round

from django.core.management.base import BaseCommand

from amper.models import Report, Item, CapacityHour, Day


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            items_size = Item.objects.all().count()

            one_day = timedelta(days=1)
            today = timezone.now()

            for i in range(100):
                item = Item.objects.all()[randrange(1, items_size)]

                date = random_datetime(today - one_day, today + one_day)

                Report.objects.create(
                    item=item,
                    duration=randrange(0, 100),
                    consumption=250 - randrange(0, 500),
                    start_time=date,
                )

            for i in range(500):
                date = random_datetime(today - one_day, today + one_day)
                date = time_round(date)

                try:

                    CapacityHour.objects.create(
                        hour=date,
                        capacity=1000 + randrange(0, 1000)
                    )

                except Exception as e:
                    print(e)

            reports = []

            for j in range(10):
                date = random_datetime(today - one_day, today + one_day)

                day = Day.objects.create(
                    date=date,
                    capacity=randrange(1, 300)
                )

                day.reports = reports
                day.save()
        except Exception as e:
            print(e)
