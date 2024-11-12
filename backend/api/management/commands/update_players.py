import os
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Player
from tqdm import tqdm

class Command(BaseCommand):
    help = "Command to upload player data from CSV to the server"

    def handle(self, *args, **options):
        csv_file_path = os.path.join(settings.BASE_DIR, 'data', 'people.csv')
        
        # Check if the file exists
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"File {csv_file_path} not found."))
            return

        players_to_create = []
        players_to_update = []

        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = list(csv.DictReader(file))
            total_rows = len(reader)
            
            for row in tqdm(reader, desc="Processing players", unit="player"):
                player_data = {
                    "identifier": row.get("identifier"),
                    "name": row.get("name"),
                    "unique_name": row.get("unique_name"),
                    "key_bcci": row.get("key_bcci"),
                    "key_bcci_2": row.get("key_bcci_2"),
                    "key_bigbash": row.get("key_bigbash"),
                    "key_cricbuzz": row.get("key_cricbuzz"),
                    "key_cricheroes": row.get("key_cricheroes"),
                    "key_crichq": row.get("key_crichq"),
                    "key_cricinfo": row.get("key_cricinfo"),
                    "key_cricinfo_2": row.get("key_cricinfo_2"),
                    "key_cricingif": row.get("key_cricingif"),
                    "key_cricketarchive": row.get("key_cricketarchive"),
                    "key_cricketarchive_2": row.get("key_cricketarchive_2"),
                    "key_cricketworld": row.get("key_cricketworld"),
                    "key_nvplay": row.get("key_nvplay"),
                    "key_nvplay_2": row.get("key_nvplay_2"),
                    "key_opta": row.get("key_opta"),
                    "key_opta_2": row.get("key_opta_2"),
                    "key_pulse": row.get("key_pulse"),
                    "key_pulse_2": row.get("key_pulse_2"),
                }

                try:
                    player = Player.objects.get(identifier=row.get("identifier"))
                    for key, value in player_data.items():
                        setattr(player, key, value)
                    players_to_update.append(player)
                    self.stdout.write(self.style.SUCCESS(f"Updated player: {player.name}"))
                except Player.DoesNotExist:
                    players_to_create.append(Player(**player_data))
                    self.stdout.write(self.style.SUCCESS(f"Created player: {player_data['name']}"))

        if players_to_create:
            Player.objects.bulk_create(players_to_create)
            self.stdout.write(self.style.SUCCESS(f"Created {len(players_to_create)} players"))

        if players_to_update:
            Player.objects.bulk_update(players_to_update, [
                "name", "unique_name", "key_bcci", "key_bcci_2", "key_bigbash", "key_cricbuzz",
                "key_cricheroes", "key_crichq", "key_cricinfo", "key_cricinfo_2", "key_cricingif",
                "key_cricketarchive", "key_cricketarchive_2", "key_cricketworld", "key_nvplay",
                "key_nvplay_2", "key_opta", "key_opta_2", "key_pulse", "key_pulse_2"
            ])
            self.stdout.write(self.style.SUCCESS(f"Updated {len(players_to_update)} players"))

        self.stdout.write(self.style.SUCCESS("Player data upload complete."))
