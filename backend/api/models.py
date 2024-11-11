from django.db import models

# Meta information model
class MetaData(models.Model):
    data_version = models.CharField(max_length=10)
    created = models.DateField()
    revision = models.IntegerField()

# Teams and players
class Team(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField('Player', related_name='teams')

# Information about the match
class MatchInfo(models.Model):
    balls_per_over = models.IntegerField(default=6)
    city = models.CharField(max_length=100)
    date = models.DateField()
    gender = models.CharField(max_length=10)
    match_type = models.CharField(max_length=10)
    match_type_number = models.IntegerField()
    overs = models.IntegerField()
    season = models.CharField(max_length=20)
    team_type = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)
    player_of_match = models.CharField(max_length=100)
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches')
    toss_decision = models.CharField(max_length=10)
    toss_winner = models.CharField(max_length=100)
    meta = models.OneToOneField(MetaData, on_delete=models.CASCADE)

# Officials involved in the match
class Official(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='officials')
    match_referee = models.CharField(max_length=100, null=True, blank=True)
    tv_umpire = models.CharField(max_length=100, null=True, blank=True)
    umpire = models.CharField(max_length=100)

# Outcome of the match
class Outcome(models.Model):
    match_info = models.OneToOneField(MatchInfo, on_delete=models.CASCADE, related_name='outcome')
    runs = models.IntegerField(null=True, blank=True)
    wickets = models.IntegerField(null=True, blank=True)
    winner = models.CharField(max_length=100)

class Player(models.Model):
    name = models.CharField(max_length=100)
    unique_name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=10, null=True, blank=True)

# Inning and overs
class Inning(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='innings')
    team = models.CharField(max_length=100)

# Delivery details
class Delivery(models.Model):
    batter = models.CharField(max_length=100)
    bowler = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)
    batter_runs = models.IntegerField()
    extras_runs = models.IntegerField(default=0)
    total_runs = models.IntegerField()

class Over(models.Model):
    inning = models.ForeignKey(Inning, on_delete=models.CASCADE, related_name='overs')
    over_number = models.IntegerField()
    deliveries = models.ManyToManyField(Delivery, related_name='over')

# Extras in a delivery
class Extra(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='extras')
    wides = models.IntegerField(null=True, blank=True)
    legbyes = models.IntegerField(null=True, blank=True)

# Wickets in a delivery
class Wicket(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='wickets')
    kind = models.CharField(max_length=100)
    player_out = models.CharField(max_length=100)
    fielder = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fielders', null=True, blank=True)

