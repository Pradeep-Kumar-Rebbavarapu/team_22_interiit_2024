import logging
from django.core.management.base import BaseCommand
import os
import json
from django.conf import settings
from django.db import transaction
from api.models import (MetaData, MatchInfo, Team, Official, Outcome, 
                        Player, Inning, Over, Delivery, Extra, Wicket, Powerplay)

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

class Command(BaseCommand):
    help = "Command to upload match data to the server"

    def handle(self, *args, **options):
        folder_name = input("Enter the folder name inside the data folder containing the JSON files: ")
        data_folder = os.path.join(settings.BASE_DIR, 'data', folder_name)
        for filename in os.listdir(data_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(data_folder, filename)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        self.stdout.write(self.style.SUCCESS(f'Processing file: {filename}'))
                        self.create_match_data(data)
                except Exception as e:
                    logging.error(f'Failed to process file {filename}: {e}')
                    self.stdout.write(self.style.ERROR(f'Failed to process file: {filename}'))

    @transaction.atomic
    def create_match_data(self, data):
        try:
            # MetaData
            meta_data = data.get("meta", {})
            meta_obj = MetaData.objects.create(
                data_version=meta_data.get("data_version"),
                created=meta_data.get("created"),
                revision=meta_data.get("revision")
            )
            self.stdout.write(self.style.SUCCESS('MetaData created or retrieved'))

            # MatchInfo
            target_runs = None
            target_overs = None
            info = data.get("info", {})
            for inning in data.get("innings", []):
                if "target" in inning:
                    target_runs = inning["target"].get("runs")
                    target_overs = inning["target"].get("overs")
                    break
                
            match_info = MatchInfo.objects.create(
                balls_per_over=info.get("balls_per_over", 6),
                city=info.get("city", ""),
                date=info.get("dates", [""])[0],
                gender=info.get("gender", ""),
                match_type=info.get("match_type", "").lower(),
                match_type_number=info.get("match_type_number", 0),
                overs=info.get("overs", 0),
                season=info.get("season", ""),
                team_type=info.get("team_type", ""),
                venue=info.get("venue", ""),
                player_of_match=info.get("player_of_match", [""])[0],
                toss_decision=info.get("toss", {}).get("decision", ""),
                toss_winner=info.get("toss", {}).get("winner", ""),
                target_overs=target_overs,
                target_runs=target_runs,
                meta=meta_obj
            )
            self.stdout.write(self.style.SUCCESS('MatchInfo created'))

            # Teams and Players
            team_objs = {}
            player_objs = {player.identifier: player for player in Player.objects.all()}
            for team_name, players in info.get("players", {}).items():
                team_obj, _ = Team.objects.get_or_create(name=team_name)
                team_objs[team_name] = team_obj
                peoples = info.get("registry", {})['people']
                player_list = []
                for player_name in players:
                    identifier = peoples[player_name]
                    player_obj = player_objs.get(identifier)
                    if not player_obj:
                        logging.error(f'Player with identifier {identifier} not found')
                        raise Exception(f'Player with identifier {identifier} not found')
                    player_list.append(player_obj)
                team_obj.players.set(player_list)
                self.stdout.write(self.style.SUCCESS(f'Team and players for {team_name} created or retrieved'))

            # Set teams for MatchInfo
            teams = list(info.get("teams", []))
            if len(teams) == 2:
                match_info.team_a = team_objs[teams[0]]
                match_info.team_b = team_objs[teams[1]]
                match_info.save()
                self.stdout.write(self.style.SUCCESS('Teams set for MatchInfo'))

            # Officials
            officials = info.get("officials", {})
            Official.objects.create(
                match_info=match_info,
                umpire=officials.get("umpires", [None])[0],
                match_referee=officials.get("match_referees", [None])[0],
                tv_umpire=officials.get("tv_umpires", [None])[0]
            )
            self.stdout.write(self.style.SUCCESS('Officials created'))

            # Outcome
            outcome = info.get("outcome", {})
            Outcome.objects.create(
                match_info=match_info,
                runs=outcome.get("by", {}).get("runs"),
                wickets=outcome.get("by", {}).get("wickets"),
                winner=outcome.get("winner", "")
            )
            self.stdout.write(self.style.SUCCESS('Outcome created'))

            # Innings and Overs
            innings = []
            overs = []
            deliveries = []
            extras = []
            wickets = []
            for inning_data in data.get("innings", []):
                inning = Inning(
                    match_info=match_info,
                    team=inning_data.get("team", "")
                )
                innings.append(inning)
                for over_data in inning_data.get("overs", []):
                    over = Over(
                        inning=inning,
                        over_number=over_data.get("over", 0)
                    )
                    overs.append(over)
                    for delivery_data in over_data.get("deliveries", []):
                        delivery = Delivery(
                            over=over,
                            batter=delivery_data.get("batter", ""),
                            bowler=delivery_data.get("bowler", ""),
                            non_striker=delivery_data.get("non_striker", ""),
                            batter_runs=delivery_data.get("runs", {}).get("batter", 0),
                            extras_runs=delivery_data.get("runs", {}).get("extras", 0),
                            total_runs=delivery_data.get("runs", {}).get("total", 0)
                        )
                        deliveries.append(delivery)

                        # Extras
                        extras_data = delivery_data.get("extras", {})
                        if extras_data:
                            extra = Extra(
                                delivery=delivery,
                                wides=extras_data.get("wides"),
                                legbyes=extras_data.get("legbyes")
                            )
                            extras.append(extra)

                        # Wicket
                        if 'wicket' in delivery_data:
                            wicket_data = delivery_data["wicket"]
                            fielder_name = wicket_data.get("fielders", [None])[0]
                            fielder_obj = Player.objects.filter(name=fielder_name).first() if fielder_name else None
                            wicket = Wicket(
                                delivery=delivery,
                                kind=wicket_data.get("kind", ""),
                                player_out=wicket_data.get("player_out", ""),
                                fielder=fielder_obj
                            )
                            wickets.append(wicket)
                self.stdout.write(self.style.SUCCESS(f'Inning and overs for team {inning_data.get("team", "")} created'))

            Inning.objects.bulk_create(innings)
            Over.objects.bulk_create(overs)
            Delivery.objects.bulk_create(deliveries)
            Extra.objects.bulk_create(extras)
            Wicket.objects.bulk_create(wickets)

            # Powerplays
            powerplays = []
            for inning_data in data.get("innings", []):
                for pp_data in inning_data.get("powerplays", []):
                    powerplay = Powerplay(
                        match_info=match_info,
                        from_over=pp_data.get("from", 0),
                        to=pp_data.get("to", 0),
                        powerplay_type=pp_data.get("type", "")
                    )
                    powerplays.append(powerplay)
            Powerplay.objects.bulk_create(powerplays)

            self.stdout.write(self.style.SUCCESS('Powerplays created'))

        except Exception as e:
            logging.error(f'Failed to create match data: {e}')
            self.stdout.write(self.style.ERROR('Failed to create match data'))
