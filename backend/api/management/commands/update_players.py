import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Player

class Command(BaseCommand):
    help = "Command to upload player data from CSV to the server"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'people.csv')
        
        # Check if the file exists
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"File {csv_file_path} not found."))
            return

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                player, created = Player.objects.update_or_create(
                    identifier=row.get("identifier"),
                    defaults={
                        "name": row.get("name"),
                        "unique_name": row.get("unique_name"),
                    }
                )
                
                player.key_bcci = row.get("key_bcci")
                player.key_bcci_2 = row.get("key_bcci_2")
                player.key_bigbash = row.get("key_bigbash")
                player.key_cricbuzz = row.get("key_cricbuzz")
                player.key_cricheroes = row.get("key_cricheroes")
                player.key_crichq = row.get("key_crichq")
                player.key_cricinfo = row.get("key_cricinfo")
                player.key_cricinfo_2 = row.get("key_cricinfo_2")
                player.key_cricingif = row.get("key_cricingif")
                player.key_cricketarchive = row.get("key_cricketarchive")
                player.key_cricketarchive_2 = row.get("key_cricketarchive_2")
                player.key_cricketworld = row.get("key_cricketworld")
                player.key_nvplay = row.get("key_nvplay")
                player.key_nvplay_2 = row.get("key_nvplay_2")
                player.key_opta = row.get("key_opta")
                player.key_opta_2 = row.get("key_opta_2")
                player.key_pulse = row.get("key_pulse")
                player.key_pulse_2 = row.get("key_pulse_2")

                player.save()

                # Log the creation or update
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created player {player.name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated player {player.name}"))

        self.stdout.write(self.style.SUCCESS("Player data upload complete."))
