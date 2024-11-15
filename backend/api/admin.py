from django.contrib import admin
from .models import (
    MetaData, Team, MatchInfo, Official, Outcome, Player, Inning, Delivery, Over, PlayerStatistics,
    Extra, Wicket, Powerplay, Chat, Message
)
from import_export.admin import ImportExportModelAdmin
from .resources import PlayerStatisticsResource

@admin.register(PlayerStatistics)
class PlayerStatisticsAdmin(ImportExportModelAdmin):
    resource_class = PlayerStatisticsResource

    list_display = (
        'player_name', 'batting', 'bowling', 'games', 'won', 'drawn', 'win_percentage', 
        'innings_batted', 'runs', 'fours', 'sixes', 'balls_faced', 'outs', 'bowled_outs', 'lbw_outs', 
        'caught_outs', 'stumped_outs', 'run_outs', 'batting_sr', 'batting_avg', 'mean_score', 
        'scoring_consistency', 'boundary_percentage', 'runs_per_ball', 'innings_bowled', 'runs_given', 
        'wickets', 'balls_bowled', 'economy_rate', 'bowling_avg', 'bowling_sr', 'runs_given_per_ball'
    )
    list_filter = (
        'player_name', 'batting', 'bowling', 'games', 'won', 'drawn', 'win_percentage', 
        'innings_batted', 'runs', 'fours', 'sixes', 'balls_faced', 'outs', 'bowled_outs', 'lbw_outs', 
        'caught_outs', 'stumped_outs', 'run_outs', 'batting_sr', 'batting_avg', 'mean_score', 
        'scoring_consistency', 'boundary_percentage', 'runs_per_ball', 'innings_bowled', 'runs_given', 
        'wickets', 'balls_bowled', 'economy_rate', 'bowling_avg', 'bowling_sr', 'runs_given_per_ball'
    )

class OfficialInline(admin.TabularInline):
    model = Official
    extra = 0

class OutcomeInline(admin.StackedInline):
    model = Outcome
    extra = 0

class DeliveryInline(admin.TabularInline):
    model = Delivery
    extra = 0

class OverInline(admin.TabularInline):
    model = Over
    extra = 0
    inlines = [DeliveryInline]

class InningInline(admin.TabularInline):
    model = Inning
    extra = 0

class PowerplayInline(admin.TabularInline):
    model = Powerplay
    extra = 0

@admin.register(MatchInfo)
class MatchInfoAdmin(admin.ModelAdmin):
    inlines = [OfficialInline, OutcomeInline, InningInline, PowerplayInline]
    list_display = ('match_type', 'date', 'team_a', 'team_b', 'venue')
    list_filter = ('team_type', 'match_type')
    search_fields = ('team_a__name', 'team_b__name', 'venue')

@admin.register(Inning)
class InningAdmin(admin.ModelAdmin):
    inlines = [OverInline]
    list_display = ('team', 'match_info')
    search_fields = ('team__name', 'match_info__team_a__name', 'match_info__team_b__name')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'player_count')
    search_fields = ('name',)

    def player_count(self, obj):
        return obj.players.count()
    player_count.short_description = 'Players'

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

admin.site.register(MetaData)
admin.site.register(Chat)
admin.site.register(Message)