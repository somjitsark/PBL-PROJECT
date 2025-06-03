from django.contrib import admin
from .models import Team, Player, Match, Ball

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')  #this list name and created date 
    search_fields = ('name',)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role', 'runs', 'wickets')
    list_filter = ('team', 'role')
    search_fields = ('name',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'date', 'status', 'winner')
    list_filter = ('status', 'date')
    search_fields = ('team1__name', 'team2__name')

@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = ('match', 'over', 'batsman', 'bowler', 'runs', 'is_wicket')
    list_filter = ('match', 'is_wicket', 'is_wide', 'is_no_ball')
    search_fields = ('batsman__name', 'bowler__name')