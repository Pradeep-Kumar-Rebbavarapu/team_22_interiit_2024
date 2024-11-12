from django.contrib import admin
from .models import MatchInfo, Team, MetaData, Official, Outcome, Inning, Delivery, Over, Extra, Wicket, Powerplay,Player

class OfficialInline(admin.TabularInline):
    model = Official
    extra = 0

class OutcomeInline(admin.StackedInline):
    model = Outcome
    extra = 0

class InningInline(admin.TabularInline):
    model = Inning
    extra = 0

class PowerplayInline(admin.TabularInline):
    model = Powerplay
    extra = 0

class MatchInfoAdmin(admin.ModelAdmin):
    inlines = [OfficialInline, OutcomeInline, InningInline, PowerplayInline]
    list_display = ('match_type', 'date', 'team_a', 'team_b', 'venue')
    search_fields = ('team_a__name', 'team_b__name', 'venue')

admin.site.register(MatchInfo, MatchInfoAdmin)
admin.site.register(Team)
admin.site.register(MetaData)
admin.site.register(Delivery)
admin.site.register(Over)
admin.site.register(Extra)
admin.site.register(Wicket)
admin.site.register(Powerplay)
admin.site.register(Player)
