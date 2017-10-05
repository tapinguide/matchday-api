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

from matchday.models import Competition, Match, MatchStatus, Club

def setup_matches(from_date, to_date):
  
    try:
        key = config.KEY 
        competitions = Competition.objects.all()
        
        for competition in competitions:
            try:
                matches_response = get_matches(key, competition.footballAPIId, from_date, to_date)
                
                if 'status' in matches_response:
                    print matches_response['message']
                else:
                    for match_response in matches_response:
                        try:      
                            matchApiId = match_response['id']
                        
                            match, created = Match.objects.get_or_create(competition=competition, footballAPIId = matchApiId)
                                
                            homeClub, created = Club.objects.get_or_create(footballAPIId = match_response['localteam_id'])
                            homeClub.name = match_response['localteam_name'] 
                            homeClub.save()
                            
                            visitorClub, created = Club.objects.get_or_create(footballAPIId = match_response['visitorteam_id'])
                            visitorClub.name = match_response['visitorteam_name']
                            visitorClub.save()

                            match.homeClub = homeClub
                            match.visitorClub = visitorClub
                            matchDate = match_response['formatted_date']
                            if match_response['time'] != "TBA":
                                matchTime = match_response['time']
                                matchDateTime = matchDate + ' ' + matchTime
                                match.matchTime = datetime.datetime.strptime(matchDateTime, '%d.%m.%Y %H:%M').strftime('%Y-%m-%d %H:%M')
                            match.homeClubScore = 0
                            match.visitorClubScore = 0
                            match.homeClubPenalties = 0
                            match.visitorClubPenalties = 0
                            match.status = MatchStatus.objects.get(id=1)
                            match.timer = ''
                            match.active = False
                            if(match.venue != ''):
                                match.venue = match_response['venue']
                            if(match.venueCity != ''):
                                match.venueCity = match_response['venue_city']
                            match.save()
                            if created:
                                print 'Match inserted - ' + match.homeClub.name.encode(sys.stdout.encoding, errors='replace') + ' v ' + match.visitorClub.name.encode(sys.stdout.encoding, errors='replace')
                            else:
                                print 'Match updated - ' + match.homeClub.name.encode(sys.stdout.encoding, errors='replace') + ' v ' + match.visitorClub.name.encode(sys.stdout.encoding, errors='replace')
                        except:
                            PrintException()
            except:
                PrintException()
    except:
        PrintException()

def get_matches(key, competition_id, from_date, to_date):
    uri = "http://api.football-api.com/2.0/matches?Authorization=" + str(key) + "&comp_id=" + str(competition_id) + "&from_date=" + from_date + "&to_date=" + to_date
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
    if len(sys.argv) > 1:
        from_date = sys.argv[1]
        to_date = sys.argv[2]
    else:
        today = datetime.datetime.now()
        future = today + timedelta(days=30)
        from_date = today.strftime('%m/%d/%Y')
        to_date = future.strftime('%m/%d/%Y')

    setup_matches(from_date, to_date)

if __name__ == '__main__':
    main()