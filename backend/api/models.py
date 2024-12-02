from django.db import models
from django.utils import timezone
import random
from .inference import get_response
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.serializers.json import DjangoJSONEncoder
import json


# Meta information model
class MetaData(models.Model):
    data_version = models.CharField(max_length=10)
    created = models.DateField()
    revision = models.IntegerField()

    def __str__(self):
        return f"MetaData {self.data_version}"

    class Meta:
        verbose_name = "Meta Data"
        verbose_name_plural = "Meta Data"
        ordering = ['-created']

# Teams and players
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    players = models.ManyToManyField('Player', related_name='teams')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ['name']

# Information about the match
class MatchInfo(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    MATCH_TYPE_CHOICES = [
        ('test', 'Test'),
        ('odi', 'ODI'),
        ('t20', 'T20'),
    ]
    balls_per_over = models.IntegerField(default=6,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True,default=None)
    date = models.DateField(null=True,blank=True,default=None)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True,blank=True,default=None)
    match_type = models.CharField(max_length=10, choices=MATCH_TYPE_CHOICES,null=True,blank=True,default=None)
    team_type = models.CharField(max_length=50,null=True,blank=True,default=None)
    players_data = models.JSONField(null=True,blank=True,default=None)
    match_type_number = models.IntegerField(null=True,blank=True,default=None)
    overs = models.IntegerField(null=True,blank=True,default=None)
    season = models.CharField(max_length=20,null=True,blank=True,default=None)
    team_type = models.CharField(max_length=50,null=True,blank=True,default=None)
    venue = models.CharField(max_length=100,null=True,blank=True,default=None)
    player_of_match = models.CharField(max_length=100,null=True,blank=True,default=None)
    team_a = models.TextField(null=True, blank=True,default=None)
    team_a_players = models.TextField(null=True ,blank=True)
    team_b = models.TextField(null=True, blank=True)
    team_b_players = models.TextField(null=True ,blank=True)
    toss_decision = models.CharField(max_length=10,null=True,blank=True,default=None)
    toss_winner = models.CharField(max_length=100,null=True,blank=True,default=None)
    target_runs = models.IntegerField(null=True, blank=True,default=None)
    target_overs = models.IntegerField(null=True, blank=True,default=None)
    meta = models.OneToOneField(MetaData, on_delete=models.CASCADE,null=True,blank=True,default=None)
    # inference_row = models.JSONField(null=True,blank=True,default=None)
    def random_prize_pool():
        return f"${random.randint(1000, 10000)}"
    def random_first_prize():
        return f"${random.randint(500, 5000)}"
    def random_amount_to_be_paid():
        return random.randint(100, 1000)
    def random_spots_left():
        return random.randint(1, 11)

    prize_pool = models.CharField(max_length=225, default=random_prize_pool,null=True,blank=True)
    first_prize = models.CharField(max_length=225, default=random_first_prize,null=True,blank=True)
    amount_to_be_paid = models.IntegerField(default=random_amount_to_be_paid,null=True,blank=True)
    spots_left = models.IntegerField(default=random_spots_left,null=True,blank=True)

    def __str__(self):
        return f"Match {self.match_type} on {self.date}"

    class Meta:
        verbose_name = "Match Info"
        verbose_name_plural = "Match Info"
        ordering = ['-date']

# Officials involved in the match
class Official(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='officials')
    match_referee = models.CharField(max_length=100, null=True, blank=True)
    tv_umpire = models.CharField(max_length=100, null=True, blank=True)
    umpire = models.CharField(max_length=100)

    def __str__(self):
        return f"Official for {self.match_info}"

    class Meta:
        verbose_name = "Official"
        verbose_name_plural = "Officials"

# Outcome of the match
class Outcome(models.Model):
    match_info = models.OneToOneField(MatchInfo, on_delete=models.CASCADE, related_name='outcome')
    runs = models.IntegerField(null=True, blank=True)
    wickets = models.IntegerField(null=True, blank=True)
    winner = models.CharField(max_length=100)

    def __str__(self):
        return f"Outcome of {self.match_info}"

    class Meta:
        verbose_name = "Outcome"
        verbose_name_plural = "Outcomes"

class Player(models.Model):
    name = models.CharField(max_length=100)
    unique_name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    identifier = models.CharField(max_length=10, null=True, blank=True, unique=True)
    key_bcci = models.CharField(max_length=100, null=True, blank=True)
    key_bcci_2 = models.CharField(max_length=100, null=True, blank=True)
    key_bigbash = models.CharField(max_length=100, null=True, blank=True)
    key_cricbuzz = models.CharField(max_length=100, null=True, blank=True)
    key_cricheroes = models.CharField(max_length=100, null=True, blank=True)
    key_crichq = models.CharField(max_length=100, null=True, blank=True)
    key_cricinfo = models.CharField(max_length=100, null=True, blank=True)
    key_cricinfo_2 = models.CharField(max_length=100, null=True, blank=True)
    key_cricingif = models.CharField(max_length=100, null=True, blank=True)
    key_cricketarchive = models.CharField(max_length=100, null=True, blank=True)
    key_cricketarchive_2 = models.CharField(max_length=100, null=True, blank=True)
    key_cricketworld = models.CharField(max_length=100, null=True, blank=True)
    key_nvplay = models.CharField(max_length=100, null=True, blank=True)
    key_nvplay_2 = models.CharField(max_length=100, null=True, blank=True)
    key_opta = models.CharField(max_length=100, null=True, blank=True)
    key_opta_2 = models.CharField(max_length=100, null=True, blank=True)
    key_pulse = models.CharField(max_length=100, null=True, blank=True)
    key_pulse_2 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        ordering = ['name']

# Inning and overs
class Inning(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='innings')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='innings')

    def __str__(self):
        return f"Inning of {self.team} in {self.match_info}"

    class Meta:
        verbose_name = "Inning"
        verbose_name_plural = "Innings"

# Delivery details
class Delivery(models.Model):
    over = models.ForeignKey('Over', on_delete=models.CASCADE, related_name='deliveries')
    batter = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='deliveries_faced')
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='deliveries_bowled')
    non_striker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='deliveries_non_striker')
    batter_runs = models.IntegerField()
    extras_runs = models.IntegerField(default=0)
    total_runs = models.IntegerField()

    def __str__(self):
        return f"Delivery by {self.bowler} to {self.batter}"

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

class Over(models.Model):
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE, related_name='overs')
    over_number = models.IntegerField()

    def __str__(self):
        return f"Over {self.over_number} in {self.inning}"

    class Meta:
        verbose_name = "Over"
        verbose_name_plural = "Overs"

# Extras in a delivery
class Extra(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='extras')
    wides = models.IntegerField(null=True, blank=True)
    legbyes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Extras in {self.delivery}"

    class Meta:
        verbose_name = "Extra"
        verbose_name_plural = "Extras"

# Wickets in a delivery
class Wicket(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='wickets')
    kind = models.CharField(max_length=100)
    player_out = models.CharField(max_length=100)
    fielder = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fielders', null=True, blank=True)

    def __str__(self):
        return f"Wicket: {self.player_out} by {self.kind}"

    class Meta:
        verbose_name = "Wicket"
        verbose_name_plural = "Wickets"

class Powerplay(models.Model):
    from_over = models.DecimalField(max_digits=3, decimal_places=1)
    to = models.DecimalField(max_digits=3, decimal_places=1)
    powerplay_type = models.CharField(max_length=10)
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='powerplays')

    def __str__(self):
        return f"Powerplay from {self.from_over} to {self.to}"

    class Meta:
        verbose_name = "Powerplay"
        verbose_name_plural = "Powerplays"


class Chat(models.Model):
    match = models.ForeignKey('MatchInfo', on_delete=models.CASCADE, related_name="chats")
    message = models.TextField()
    is_ai = models.BooleanField(default=False)  
    is_user = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        message_origin = "User" if self.is_user else "AI"
        return f"{message_origin} message for match {self.match_id} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']

class Message(models.Model):
    chat = models.ForeignKey("Chat",  on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id}"


class PlayerStatistics(models.Model):
    player_name = models.CharField(max_length=100)
    batting = models.CharField(max_length=50, null=True, blank=True)
    bowling = models.CharField(max_length=50, null=True, blank=True)
    games = models.IntegerField(null=True, blank=True)
    won = models.IntegerField(null=True, blank=True)
    drawn = models.IntegerField(null=True, blank=True)
    win_percentage = models.FloatField(null=True, blank=True)
    innings_batted = models.IntegerField(null=True, blank=True)
    runs = models.IntegerField(null=True, blank=True)
    singles = models.IntegerField(null=True, blank=True)
    fours = models.IntegerField(null=True, blank=True)
    sixes = models.IntegerField(null=True, blank=True)
    dot_balls = models.IntegerField(null=True, blank=True)
    balls_faced = models.IntegerField(null=True, blank=True)
    outs = models.IntegerField(null=True, blank=True)
    bowled_outs = models.IntegerField(null=True, blank=True)
    lbw_outs = models.IntegerField(null=True, blank=True)
    hitwicket_outs = models.IntegerField(null=True, blank=True)
    caught_outs = models.IntegerField(null=True, blank=True)
    stumped_outs = models.IntegerField(null=True, blank=True)
    run_outs = models.IntegerField(null=True, blank=True)
    caught_and_bowled_outs = models.IntegerField(null=True, blank=True)
    dot_ball_percentage = models.FloatField(null=True, blank=True)
    strike_turnover_percentage = models.FloatField(null=True, blank=True)
    batting_sr = models.FloatField(null=True, blank=True)
    batting_sr_meanad = models.FloatField(null=True, blank=True)
    batting_avg = models.FloatField(null=True, blank=True)
    mean_score = models.FloatField(null=True, blank=True)
    score_meanad = models.FloatField(null=True, blank=True)
    scoring_consistency = models.FloatField(null=True, blank=True)
    boundary_percentage = models.FloatField(null=True, blank=True)
    runs_per_ball = models.FloatField(null=True, blank=True)
    mean_balls_faced = models.FloatField(null=True, blank=True)
    balls_faced_meanad = models.FloatField(null=True, blank=True)
    survival_consistency = models.FloatField(null=True, blank=True)
    avg_first_boundary_ball = models.FloatField(null=True, blank=True)
    dismissal_rate = models.FloatField(null=True, blank=True)
    boundary_rate = models.FloatField(null=True, blank=True)
    innings_bowled = models.IntegerField(null=True, blank=True)
    runs_given = models.IntegerField(null=True, blank=True)
    singles_given = models.IntegerField(null=True, blank=True)
    fours_given = models.IntegerField(null=True, blank=True)
    sixes_given = models.IntegerField(null=True, blank=True)
    wickets = models.IntegerField(null=True, blank=True)
    balls_bowled = models.IntegerField(null=True, blank=True)
    extras = models.IntegerField(null=True, blank=True)
    no_balls = models.IntegerField(null=True, blank=True)
    wides = models.IntegerField(null=True, blank=True)
    dot_balls_bowled = models.IntegerField(null=True, blank=True)
    bowleds = models.IntegerField(null=True, blank=True)
    lbws = models.IntegerField(null=True, blank=True)
    hitwickets = models.IntegerField(null=True, blank=True)
    caughts = models.IntegerField(null=True, blank=True)
    stumpeds = models.IntegerField(null=True, blank=True)
    caught_and_bowleds = models.IntegerField(null=True, blank=True)
    catches = models.IntegerField(null=True, blank=True)
    runouts = models.IntegerField(null=True, blank=True)
    stumpings = models.IntegerField(null=True, blank=True)
    economy_rate = models.FloatField(null=True, blank=True)
    economy_rate_meanad = models.FloatField(null=True, blank=True)
    dot_ball_bowled_percentage = models.FloatField(null=True, blank=True)
    boundary_given_percentage = models.FloatField(null=True, blank=True)
    bowling_avg = models.FloatField(null=True, blank=True)
    bowling_avg_meanad = models.FloatField(null=True, blank=True)
    bowling_sr = models.FloatField(null=True, blank=True)
    bowling_sr_meanad = models.FloatField(null=True, blank=True)
    runs_given_per_ball = models.FloatField(null=True, blank=True)
    boundary_given_rate = models.FloatField(null=True, blank=True)
    strike_turnover_given_percentage = models.FloatField(null=True, blank=True)
    avg_consecutive_dot_balls = models.FloatField(null=True, blank=True)
    runs_rate = models.FloatField(null=True, blank=True)
    runs_given_per_wicket = models.FloatField(null=True, blank=True)
    runs_aa = models.FloatField(null=True, blank=True)
    runs_per_ball_aa = models.FloatField(null=True, blank=True)
    runs_given_aa = models.FloatField(null=True, blank=True)
    runs_given_per_ball_aa = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.player_name



@receiver(post_save, sender=MatchInfo)
def update_inference_row(sender, instance, **kwargs):
    try:
        # team_a_players_ids = list(instance.team_a_players.values_list('identifier', flat=True))
        team_a_players = list(instance.team_a_players.values_list('unique_name', flat=True))
        # team_b_players_ids = list(instance.team_b_players.values_list('identifier', flat=True))
        team_b_players = list(instance.team_b_players.values_list('unique_name', flat=True))
        
        # inference_list = get_response(team_a_players,team_b_players,team_a_players_ids,team_b_players_ids, instance.match_type, instance.date)

        inference_list = get_response(team_a_players,team_b_players,instance.match_type, instance.date)
        
        instance.inference_row = inference_list
        
        MatchInfo.objects.filter(pk=instance.pk).update(
            inference_row=json.dumps(inference_list, cls=DjangoJSONEncoder)
        )
    except Exception as e:
        print(f"Error updating inference row: {e}")

