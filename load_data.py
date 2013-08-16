# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Loading Data from openLigaDB

# <codecell>

import json
import urllib
import urllib2
import pandas as pd
import datetime as dt

def getJsonResponse(function, parameters):
    """Gets JSON response of function and parameters according to http://openligadb-json.heroku.com/"""
    encoded_args = urllib.urlencode(parameters)
    response = urllib2.urlopen('http://openligadb-json.heroku.com/api/' + function + '?' + encoded_args)
    return json.loads(response.read())

# <codecell>

def scrape_all_data():
    """Downloads all 1. Bundesliga information from openLigaDB.de and stores it in a csv-file"""
    # Get teams from 2013/2014
    teams = getJsonResponse('teams_by_league_saison', {'league_saison':'2013', 'league_shortcut':'bl1'})
    teams = pd.DataFrame.from_dict(teams['team'])
    teams.to_csv('data/teams.csv', encoding='utf-8', index=False)
    
    # Get all games from 2009-2013. This can take quite some time due to server caching
    years = ['2009', '2010', '2011', '2012', '2013']
    matches = dict.fromkeys(years)
    for year in years:
        saison = getJsonResponse('matchdata_by_league_saison', {'league_saison':year, 'league_shortcut':'bl1'})
        matches[year] = pd.DataFrame.from_dict(saison['matchdata'])
    
    # Concatenate all data into one dataset
    all_matches = pd.concat(matches, ignore_index=True)
    
    # Save dataset in csv file
    all_matches.to_csv('data/leagueDB.csv', encoding='utf-8', index=False)

# <codecell>

def load_db_from_file():
    return pd.read_csv('data/leagueDB.csv')

# <codecell>

def update_db(db, this_saison):
    """ Checks if database changed today and updates the db accordingly"""
    last_change_date = getJsonResponse('last_change_date_by_league_saison', {'league_saison':str(this_saison), 'league_shortcut':'bl1'})
    last_change_date = dt.datetime.strptime(last_change_date[:10], '%Y-%m-%d')
    if dt.date.today() <= last_change_date.date():
        # Remove current saison
        db = db[db['league_saison']!=this_saison]
        # Download saison data
        saison = getJsonResponse('matchdata_by_league_saison', {'league_saison':str(this_saison), 'league_shortcut':'bl1'})
        # Store in DataFrame
        saison_frame = pd.DataFrame.from_dict(saison['matchdata'])
        # Append to database
        db = pd.concat([db, saison_frame], ignore_index=True)
        # Save in csv-file
        db.to_csv('data/leagueDB.csv', encoding='utf-8', index=False)
        print 'leagueDB has been updated'
        return db
    else:
        # No changes
        print 'leagueDB up to date'
        return db

