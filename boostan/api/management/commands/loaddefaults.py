from django.core.management import call_command
from django.core.management.base import BaseCommand

from api.models import Message, Setting


class Command(BaseCommand):
    help = "Migrate and load fixtures to db"

    def handle(self, *args, **kwargs):
        fixtures_path = "boostan/api/fixtures/"
        settings_count = Setting.objects.all().count()
        if not settings_count:
            self.stdout.write("Load settings model data...")
            call_command("loaddata", fixtures_path + "settings.json")
        else:
            self.stdout.write("Skip loading data for setting model.")

        messagess_count = Message.objects.all().count()
        if not messagess_count:
            self.stdout.write("Load messages model data...")
            call_command("loaddata", fixtures_path + "messages.json")
        else:
            self.stdout.write("Skip loading data for message model.")
