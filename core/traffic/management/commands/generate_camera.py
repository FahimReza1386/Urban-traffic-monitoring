# Django Imports
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import random

# Third-Party Imports
from faker import Faker

# Locale Imports
from traffic.models import Cameras

class Command(BaseCommand):
    help = _("Generated the TrafficLog Fake Data.")
    
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(95):
            
            Cameras.objects.create(
                name = fake.word(),
            )
        self.stdout.write(self.style.SUCCESS('Successfully generated Cameras Fake data'))
