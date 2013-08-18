# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import HTML, display

def team_matches(db, team_name):
    return db[(db['name_team1']==team_name) | (db['name_team2']==team_name)]

def saison_matches(db, saison):
    return db[db['league_saison']==saison]

def team_wins(db, team_name):
    team1_wins = (db['name_team1']==team_name) & (db['points_team1']>db['points_team2'])
    team2_wins = (db['name_team2']==team_name) & (db['points_team1']<db['points_team2'])
    return db[team1_wins | team2_wins]

def team_loses(db, team_name):
    team1_wins = (db['name_team1']==team_name) & (db['points_team1']<db['points_team2'])
    team2_wins = (db['name_team2']==team_name) & (db['points_team1']>db['points_team2'])
    return db[team1_wins | team2_wins]

def team_draws(db, team_name):
    matches = team_matches(db, team_name)
    return matches[matches['points_team1']==matches['points_team2']]

def next_matches(db):
    return db[db['match_is_finished']==False]

def last_matches(db):
    return db[db['match_is_finished']==True].sort('match_date_time', ascending=False)

def show_next_matches(db, num_matches):
    display(next_matches(db)[['match_date_time', 'name_team1', 'name_team2']].head(num_matches))
    
def show_last_matches(db, num_matches):
    display(last_matches(db)[['match_date_time', 'name_team1', 'name_team2', 'points_team1', 'points_team2']].head(num_matches))

