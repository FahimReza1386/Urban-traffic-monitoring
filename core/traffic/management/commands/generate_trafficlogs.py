# Django Imports
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
import random

# Third-Party Imports
from faker import Faker

# Locale Imports
from traffic.models import TrafficLogs, Cameras


class Command(BaseCommand):
    """
    Create Fake Data For TrafficLogs Table.
    """

    help = _("Generated the TrafficLog Fake Data.")

    def handle(self, *args, **options):
        fake = Faker()
        all_cameras = list(Cameras.objects.all())

        batch_size = 50000
        total_records = 1000000
        logs_to_create = []

        base_time = datetime.now()

        self.stdout.write(f"Start generating {total_records} records...")

        if not all_cameras:
            self.stdout.write(
                self.style.ERROR("No cameras found! Please create some cameras first.")
            )
            return

        for i in range(1, total_records + 1):
            log = TrafficLogs(
                plate_number=fake.pystr(max_chars=6),
                camera_id=random.choice(all_cameras),
                timestamp=base_time - timedelta(seconds=random.randint(0, 1000000)),
                type_id=random.randint(1, 4),
            )
            logs_to_create.append(log)

            if i % batch_size == 0:
                TrafficLogs.objects.bulk_create(logs_to_create)
                self.stdout.write(f"{i} records created...")
                logs_to_create = []

        if logs_to_create:
            TrafficLogs.objects.bulk_create(logs_to_create)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated TrafficLogs Fake data")
        )
