from django.db import models

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
    balls_per_over = models.IntegerField(default=6)
    city = models.CharField(max_length=100)
    date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    match_type = models.CharField(max_length=10, choices=MATCH_TYPE_CHOICES)
    match_type_number = models.IntegerField()
    overs = models.IntegerField()
    season = models.CharField(max_length=20)
    team_type = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)
    player_of_match = models.CharField(max_length=100)
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_b')
    toss_decision = models.CharField(max_length=10)
    toss_winner = models.CharField(max_length=100)
    meta = models.OneToOneField(MetaData, on_delete=models.CASCADE)

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
    identifier = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        ordering = ['name']

# Inning and overs
class Inning(models.Model):
    match_info = models.ForeignKey(MatchInfo, on_delete=models.CASCADE, related_name='innings')
    team = models.CharField(max_length=100)

    def __str__(self):
        return f"Inning of {self.team} in {self.match_info}"

    class Meta:
        verbose_name = "Inning"
        verbose_name_plural = "Innings"

# Delivery details
class Delivery(models.Model):
    batter = models.CharField(max_length=100)
    bowler = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)
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
    deliveries = models.ManyToManyField(Delivery, related_name='over')

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
