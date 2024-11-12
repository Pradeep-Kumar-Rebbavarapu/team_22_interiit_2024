from django.contrib import admin
from .models import (
    MetaData, Team, MatchInfo, Official, Outcome, Player, Inning, Delivery, Over,
    Extra, Wicket, Powerplay
)

# Register the models with the admin site
admin.site.register(MetaData)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_count')
    search_fields = ('name',)

    def player_count(self, obj):
        return obj.players.count()
    player_count.short_description = 'Players'

@admin.register(MatchInfo)
class MatchInfoAdmin(admin.ModelAdmin):
    list_display = ('date', 'gender', 'match_type', 'team_a', 'team_b')
    search_fields = ('city', 'date', 'gender', 'match_type', 'season', 'venue', 'team_a__name', 'team_b__name')

@admin.register(Official)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ('match_info', 'umpire', 'match_referee', 'tv_umpire')
    search_fields = ('match_info__date', 'match_info__team_a__name', 'match_info__team_b__name', 'umpire')

@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('match_info', 'runs', 'wickets', 'winner')
    search_fields = ('match_info__date', 'match_info__team_a__name', 'match_info__team_b__name', 'winner')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_name', 'identifier', 'teams_display')
    search_fields = ('name', 'unique_name', 'identifier', 'teams__name')

    def teams_display(self, obj):
        return ', '.join(team.name for team in obj.teams.all())
    teams_display.short_description = 'Teams'

@admin.register(Inning)
class InningAdmin(admin.ModelAdmin):
    list_display = ('match_info', 'team')
    search_fields = ('match_info__date', 'match_info__team_a__name', 'match_info__team_b__name', 'team__name')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('over', 'batter', 'bowler', 'non_striker', 'batter_runs', 'extras_runs', 'total_runs')
    search_fields = ('over__inning__match_info__date', 'over__inning__match_info__team_a__name', 'over__inning__match_info__team_b__name', 'batter', 'bowler')

@admin.register(Over)
class OverAdmin(admin.ModelAdmin):
    list_display = ('inning', 'over_number')
    search_fields = ('inning__match_info__date', 'inning__match_info__team_a__name', 'inning__match_info__team_b__name', 'inning__team__name', 'over_number')

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'wides', 'legbyes')
    search_fields = ('delivery__over__inning__match_info__date', 'delivery__over__inning__match_info__team_a__name', 'delivery__over__inning__match_info__team_b__name')

@admin.register(Wicket)
class WicketAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'kind', 'player_out', 'fielder')
    search_fields = ('delivery__over__inning__match_info__date', 'delivery__over__inning__match_info__team_a__name', 'delivery__over__inning__match_info__team_b__name', 'player_out', 'fielder__name')

@admin.register(Powerplay)
class PowerplayAdmin(admin.ModelAdmin):
    list_display = ('match_info', 'from_over', 'to', 'powerplay_type')
    search_fields = ('match_info__date', 'match_info__team_a__name', 'match_info__team_b__name', 'from_over', 'to', 'powerplay_type')