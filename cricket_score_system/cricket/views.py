from django.shortcuts import render, get_object_or_404
from .models import Team, Player, Match, Ball
from django.db.models import Sum, Count
import json
from sklearn.linear_model import LinearRegression
import numpy as np

def home(request):
    matches = Match.objects.all()
    return render(request, 'cricket/home.html', {'matches': matches})

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'cricket/team_list.html', {'teams': teams})

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = team.players.all()
    return render(request, 'cricket/team_detail.html', {'team': team, 'players': players})

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    balls = match.balls.all()
    team1_score = balls.filter(batsman__team=match.team1).aggregate(total_runs=Sum('runs'))['total_runs'] or 0
    team2_score = balls.filter(batsman__team=match.team2).aggregate(total_runs=Sum('runs'))['total_runs'] or 0
    total_runs = team1_score + team2_score
    team1_win_prob = (team1_score / total_runs * 100) if total_runs > 0 else 50
    team2_win_prob = 100 - team1_win_prob
    overs = balls.values('over').annotate(runs=Sum('runs')).order_by('over')
    graph_data = json.dumps(list(overs))
    # Simple score prediction
    if overs:
        X = np.array([item['over'] for item in overs]).reshape(-1, 1)
        y = np.array([item['runs'] for item in overs])
        model = LinearRegression()
        model.fit(X, y)
        predicted_score = model.predict([[20]])[0]  # Predict for 20 overs
    else:
        predicted_score = 0
    return render(request, 'cricket/match_detail.html', {
        'match': match,
        'balls': balls,
        'team1_score': team1_score,
        'team2_score': team2_score,
        'team1_win_prob': team1_win_prob,
        'team2_win_prob': team2_win_prob,
        'graph_data': graph_data,
        'predicted_score': predicted_score
    })

def player_stats(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    balls_faced = Ball.objects.filter(batsman=player)
    total_runs = balls_faced.aggregate(total_runs=Sum('runs'))['total_runs'] or 0
    wickets_taken = Ball.objects.filter(bowler=player, is_wicket=True).count()
    return render(request, 'cricket/player_stats.html', {
        'player': player,
        'total_runs': total_runs,
        'wickets_taken': wickets_taken
    })