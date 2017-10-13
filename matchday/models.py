from __future__ import unicode_literals
from django.db import models

class MatchStatus(models.Model):
    description = models.CharField('Match Status', max_length=500, null=True)
    sortOrder = models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4,4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])
    class Meta:
        verbose_name = 'Match Status'
        verbose_name_plural = 'Match Statuses'
    def __str__(self):
        return self.description

class Competition(models.Model):
    footballAPIId = models.IntegerField('Football API Competition Id',default=0, null=True, unique=True, blank=True)
    name = models.CharField('Name', max_length=200, null=True, blank=True)
    region = models.CharField('Region', max_length=200, null=True, blank=True)
    def __unicode__(self):
        return self.name + ' (' + self.region + ')'

class Club(models.Model):
    name = models.CharField('Club Name', max_length=200, null=True)
    shortName = models.CharField('Short Name', max_length=200, null=True, blank=True)
    nickName = models.CharField('Nickname', max_length=200, null=True, blank=True)
    footballAPIId = models.IntegerField('Football API Team Id', default=0, null=True, unique=True, blank=True)
    crest = models.FileField(upload_to='crests', null=True, blank=True)
    color = models.CharField('Color', max_length=200, null=True, blank=True)
    def __unicode__(self):
        return self.name

class Match(models.Model):
    competition = models.ForeignKey(Competition, verbose_name='Competition/League', null=False, blank=False)
    footballAPIId = models.IntegerField('Football API Match Id', default=0, null=False, blank=False)
    homeClub = models.ForeignKey(Club, verbose_name='Home Club (API Local Club)', related_name='match_homeClubs', null=True)
    visitorClub = models.ForeignKey(Club, verbose_name='Visitor Club (API Visitor Club)', related_name='match_visitorClubs', null=True)
    matchTime = models.DateTimeField('Match Time GMT',null=True, blank=True) 
    homeClubScore = models.IntegerField('Home Club Score', null=True, blank=True)
    visitorClubScore = models.IntegerField('Visitor Club Score', null=True, blank=True)
    homeClubPenalties = models.IntegerField('Home Club Penalties', null=True, blank=True)
    visitorClubPenalties = models.IntegerField('Visitor Club Penalties', null=True, blank=True)
    status = models.ForeignKey(MatchStatus, verbose_name='Match Status', null=True, blank=True)
    timer = models.CharField(max_length=10, blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)
    venueCity = models.CharField('Venue City', max_length=100, blank=True, null=True)
    tvDetails = models.CharField('TV Details', max_length=100, blank=True, null=True)
    display = models.BooleanField('Display Match', default=False, null=False)
    preMatchDetails = models.CharField('Pre Match Details',max_length=500, null=True, blank=True)
    inMatchDetails = models.CharField('In Match Details', max_length=500, null=True, blank=True)
    postMatchDetails = models.CharField('Post Match Details', max_length=500, null=True, blank=True)
    highlightsUrl = models.CharField('Highlights URL', max_length=300,null=True, blank=True)
    class Meta:
        verbose_name_plural = "Matches"
    def _get_match_date(self):
        "Returns the date from matchTime"
        if self.matchTime is None:
            return ''
        else:
            return self.matchTime.date().strftime("%A %d %B")
    def _get_home_club_name(self):
        "Returns the name of the home club"
        if self.homeClub is None:
            return 'NA'
        else:
            return self.homeClub.name
    def _get_visitor_club_name(self):
        "Returns the name of the home club"
        if self.visitorClub is None:
            return 'NA'
        else:
            return self.visitorClub.name
    def _get_match_date_time(self):
        "Returns the date and time from matchTime"
        if self.matchTime is None:
            return 'Match time not set'
        else:
            return str(self.matchTime)
    matchDate = property(_get_match_date)
    matchDateTime = property(_get_match_date_time)
    homeClubName = property(_get_home_club_name)
    visitorClubName = property(_get_visitor_club_name)
    def __unicode__(self):
        return self.homeClubName \
        + ' v ' + self.visitorClubName \
        + ' -- ' + self.matchDateTime

class Event(models.Model):
    footballAPIId = models.IntegerField(unique=True, null=True)
    match = models.ForeignKey(Match, null=True, related_name='events')
    club = models.ForeignKey(Club, null=True)
    eventType = models.CharField(max_length=200, null=True)
    minute = models.IntegerField(default=0, null=True)
    extraMinute = models.IntegerField(default=0, null=True)
    player = models.CharField(max_length=200, null=True)
    playerFootballAPIId = models.IntegerField(default=0, null=True)
    assist = models.CharField(max_length=200, null=True)
    assistFootballAPIId = models.IntegerField(default=0, null=True)
    result = models.CharField(max_length=50, null=True)
    eventTeamName = models.CharField(max_length=200, null=True)
    def totalMinutes(self):
        result = self.minute + self.extraMinute
        return result
    def __unicode__(self):
        return self.player + ' - ' + self.eventType

class MustReadWatch(models.Model):
    header = models.CharField(max_length=15, null=False, blank=False)
    text = models.CharField(max_length=50, null=False, blank=False)
    url = models.CharField(max_length=500, null=False, blank=False)
    mustType = models.CharField('Type', max_length=256, choices=[('read', 'Read'), ('watch', 'Watch')], null=False, blank=False)
    def __unicode__(self):
        return self.mustType + ' - ' + self.text

class ContextBlurb(models.Model):
    text = models.CharField(max_length=500, null=True)
    def __unicode__(self):
        return 'This week''s context blurb'