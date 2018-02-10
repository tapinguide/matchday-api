import os, sys, os.path
import requests
import config
import commands
import linecache
import django, json
import time
import datetime
from datetime import timedelta 
from django.utils import timezone
from django.conf import settings

#Get this current file path
this_path = os.path.abspath(os.path.dirname(__file__))

#The project path is one level up
proj_path = os.path.abspath(os.path.join(this_path, os.pardir))

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tapinguide.settings")
sys.path.append(proj_path)
django.setup()

from matchday.models import Competition, Match, MatchStatus, Club, Table

def setup_tables():
  
    try:
        key = config.KEY 
        competitions = Competition.objects.all()
        for competition in competitions:
            try:
                tables_response = get_table(key, competition.footballAPIId)
                
                if 'status' in tables_response:
                    print tables_response['message']
                else:
                    for table_response in tables_response:
                        try:      
                            teamId = table_response['team_id']
                            teamName = table_response['team_name']
                            season = table_response['season']
                            recentForm = table_response['recent_form']
                            position = table_response['position']
                            goalDifference = table_response['gd']
                            points = table_response['points']
                            description = table_response['description']

                            club, created = Club.objects.get_or_create(footballAPIId = teamId)
                            if created:
                                club.name = teamName
                                club.save()

                            table, created = Table.objects.get_or_create(competition = competition, club = club)
                            
                            table.season = season
                            table.recentForm = recentForm
                            table.position = position
                            table.goalDifference = goalDifference
                            table.points = points
                            table.description = description
                            table.save()
                        except:
                            PrintException()
            except:
                PrintException()
    except:
        PrintException()

def get_table(key, competition_id):
    uri = "http://api.football-api.com/2.0/standings?Authorization=" + str(key) + "&comp_id=" + str(competition_id)
    print "Getting " + uri
    response = requests.get(uri)
    json_output = json.loads(response.content)
    return json_output

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def main():
    setup_tables()

if __name__ == '__main__':
    main()