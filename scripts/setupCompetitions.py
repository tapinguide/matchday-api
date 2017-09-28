import os, sys, os.path
import requests
import config
import commands
import linecache
import django, json
import time
import datetime
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

from matchday.models import Competition
def setup_competitions():
  
    try:
        key = config.KEY 
        competitions_response = get_competitions(key)

        for competition_response in competitions_response:
            competitionApiId = competition_response['id']
            competition, created = Competition.objects.get_or_create(footballAPIId = competitionApiId)
            competition.name = competition_response['name']
            competition.region = competition_response['region']
            competition.save()
    except:
        PrintException()

def get_competitions(key):
    uri = "http://api.football-api.com/2.0/competitions?Authorization=" + str(key)
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
    setup_competitions()

if __name__ == '__main__':
    main()