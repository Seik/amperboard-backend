from random import randrange

from datetime import timedelta
from django.utils import timezone

from amper.utils import random_datetime

from django.core.management.base import BaseCommand

from amper.models import Report, Item, CapacityHour, Day


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            items_size = Item.objects.all().count()

            one_day = timedelta(days=1)
            today = timezone.now()

            for i in range(500):
                item = Item.objects.all()[randrange(1, items_size)]

                date = random_datetime(today - one_day, today + one_day)

                Report.objects.create(
                    item=item,
                    duration=randrange(0, 100),
                    consumption=randrange(100, 500),
                    start_time=date,
                )

            for i in range(500):
                date = random_datetime(today - one_day, today + one_day)

                CapacityHour.objects.create(
                    hour=date,
                    capacity=randrange(0, 4000)
                )

            reports = []
            all_reports = Report.objects.all()

            for j in range(10):
                reports.append(all_reports[randrange(1, all_reports.count())])

                date = random_datetime(today - one_day, today + one_day)

                day = Day.objects.create(
                    date=date,
                    capacity=randrange(1, 300)
                )

                day.reports = reports
                day.save()

                print date
        except Exception as e:
            print e
