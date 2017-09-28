from django.shortcuts import render
from .models import Club, Match, MatchStatus, Competition, Link, ContextBlurb
from rest_framework import viewsets
from .serializers import MatchStatusSerializer, ClubSerializer, ClubWithCrestSerializer, CompetitionSerializer, MatchSerializer, ActiveMatchSerializer, LinkSerializer, ContextBlurbSerializer

def index(request):
    return render(request, 'matchday/index.html')

class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows competitions to be viewed or edited.
    """
    queryset = Competition.objects.all().order_by('footballAPIId')
    serializer_class = CompetitionSerializer

class MatchStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows match statuses to be viewed or edited.
    """
    queryset = MatchStatus.objects.all().order_by('description')
    serializer_class = MatchStatusSerializer

class ClubViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clubs to be viewed or edited.
    """
    queryset = Club.objects.all().order_by('name')
    serializer_class = ClubSerializer

class ClubWithCrestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows clubs with crests to be viewed or edited.
    """
    queryset = Club.objects.exclude(crest__isnull=True).exclude(crest__exact='').order_by('name')
    serializer_class = ClubWithCrestSerializer

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows clubs to be viewed or edited.
    """
    queryset = Match.objects.all().order_by('matchTime')
    serializer_class = MatchSerializer

class ActiveMatchViewSet(viewsets.ReadOnlyModelViewSet):
    
    """
    API endpoint that allows clubs to be viewed or edited.
    """
    queryset = Match.objects.filter(display=True).order_by('status__sortOrder', 'matchTime').prefetch_related('events')
    serializer_class = ActiveMatchSerializer

class LinkViewSet(viewsets.ReadOnlyModelViewSet):
    
    """
    API endpoint that allows links to be viewed
    """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

class ContextBlurbViewSet(viewsets.ReadOnlyModelViewSet):
    
    """
    API endpoint that allows the context blurb to be viewed
    """
    queryset = ContextBlurb.objects.all()
    serializer_class = ContextBlurbSerializer

