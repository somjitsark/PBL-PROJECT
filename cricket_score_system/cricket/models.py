from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    role = models.CharField(max_length=50, choices=[('Batsman', 'Batsman'), ('Bowler', 'Bowler'), ('All-Rounder', 'All-Rounder'), ('Wicket-Keeper', 'Wicket-Keeper')])
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.team.name})"

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('Upcoming', 'Upcoming'), ('Live', 'Live'), ('Completed', 'Completed')])
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - {self.date}"

class Ball(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='balls')
    over = models.FloatField()
    batsman = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batsman_balls')
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowler_balls')
    runs = models.IntegerField(default=0)
    is_wicket = models.BooleanField(default=False)
    is_wide = models.BooleanField(default=False)
    is_no_ball = models.BooleanField(default=False)
    commentary = models.TextField(blank=True)

    def __str__(self):
        return f"Ball {self.over} in {self.match}"