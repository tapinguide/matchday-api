import os, sys, os.path
import config, requests
import commands
import linecache
import django, json
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.db import connection
import sched, time

#Get this current file path
this_path = os.path.abspath(os.path.dirname(__file__))

#The project path is one level up
proj_path = os.path.abspath(os.path.join(this_path, os.pardir))

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tapinguide.settings")
sys.path.append(proj_path)
django.setup()

from matchday.models import Competition, Match, MatchStatus, Club, Event

def updateMatches():
    try:
        print 'Updating matches...'
        key = config.KEY 
       
        activeMatches = Match.objects.filter(display=True)
        for activeMatch in activeMatches:
            match = activeMatch
            try:
                match_response = get_match(key, match.footballAPIId)
                if match_response['status'] == 'error':
                    print match_response['message']
                else:
                    if match_response['status'] != match_response['time']:
                        print match_response['localteam_score']
                        if match_response['localteam_score'] is not None:
                            match.homeClubScore = match_response['localteam_score']
                        if match_response['visitorteam_score'] is not None:
                            match.visitorClubScore = match_response['visitorteam_score']
                        match.timer = match_response['timer']

                        if match_response['penalty_local'] is not None:
                            match.homeClubPenalties = match_response['penalty_local']
                        else:
                            match.homeTeamPenalties = 0
                        if match_response['penalty_visitor'] is not None:
                            match.visitorClubPenalties = match_response['penalty_visitor']
                        else:
                            match.visitorClubPenalties = 0
                        try:
                            status = MatchStatus.objects.get(description=match_response['status'])
                            match.status = status
                        except:
                            if match_response['status'] == match_response['time']:
                                #Scheduled
                                match.status_id = 1
                            elif match_response['status'] == match_response['timer']:
                                #Match is in progress
                                match.status = MatchStatus.objects.get(description='In Progress')
                        #fuck yeah
                        match.save()
                        print "Match Updated"

                        for event in match_response['events']:
                            eventClubId = 0
                            eventApiId = event['id']
                            eventType = event['type']
                            eventMinute = event['minute']
                            eventExtraMinute = event['extra_min']
                            eventPlayer = event['player']
                            eventTeam = event['team']
                            eventTeamName = ''
                            eventAssist = event['assist']
                            if(event['assist_id'] == ''):
                                eventAssistId = 0
                            else:
                                eventAssistId = event['assist_id']
                            eventResult = event['result']

                            if(eventTeam == "localteam"):
                                eventClubId = match.homeClub.id
                                eventTeamName = match.homeClub.name
                            else:
                                eventClubId = match.visitorClub.id
                                eventTeamName = match.visitorClub.name
                                
                            club = Club.objects.get(id = eventClubId)

                            if club is not None:
                                if eventPlayer and len(eventPlayer) > 0:
                                    event, created = Event.objects.get_or_create(match=match, footballAPIId = eventApiId)
                                    event.event_api_id = eventApiId
                                    event.match = match
                                    event.club = club
                                    event.eventType = eventType
                                    event.assist = eventAssist
                                    event.assistFootballAPIId = eventAssistId
                                    event.result = eventResult
                                    event.eventTeamName = eventTeamName
                                    if eventMinute == '':
                                        event.minute = 0
                                    else:
                                        event.minute = eventMinute
                                    if eventExtraMinute == '':
                                        event.extraMinute = 0
                                    else:
                                        event.extraMinute = eventExtraMinute
                                    event.player = eventPlayer
                                    event.save()
                                    print 'Event updated/added'
                                else:
                                    print 'Empty player field'
                            else:
                                print 'Match has not yet started'
                               
            except:
                PrintException()
    except:
        PrintException()
    finally:
        print 'Entering finally clause'
        connection.close()

def get_match(key, match_id):
    uri = "http://api.football-api.com/2.0/matches/" + str(match_id) +"?Authorization=" + str(key)
    response = requests.get(uri)
    json_output = json.loads(response.content)
    print uri
    return json_output

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

def updateMatchesLongRunning():
    starttime=time.time()
    while True:
        updateMatches()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

def main():
    updateMatches()

if __name__ == '__main__':
    main()