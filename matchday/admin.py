from django.contrib import admin

from .models import Club, Match, MatchStatus, Competition, MustReadWatch, ContextBlurb
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django import forms

class CompetitionAdmin(admin.ModelAdmin):  
    ordering = ('name',) 
admin.site.register(Competition, CompetitionAdmin)

class ClubAdmin(admin.ModelAdmin):  
    ordering = ('name',) 
    search_fields = ['name']
admin.site.register(Club, ClubAdmin)

class MatchModelForm(forms.ModelForm):
    preMatchDetails = forms.CharField(widget=forms.Textarea, label = 'Pre Match Details: 500 characters', required=True)
    inMatchDetails = forms.CharField(widget=forms.Textarea, label = 'In Match Details: 500 characters', required=False)
    postMatchDetails = forms.CharField(widget=forms.Textarea, label = 'Post Match Details: 500 characters', required=False)
    class Meta:
        model = Match
        fields = '__all__' 

class MatchAdmin(admin.ModelAdmin):  
    ordering = ('matchTime',) 
    list_filter = (
        'display',
        ('matchTime', DateRangeFilter),
        'competition__name',
        )
    search_fields = ['homeClub__name', 'visitorClub__name', 'competition__region', 'competition__name']
    form = MatchModelForm
admin.site.register(Match, MatchAdmin)

class MatchStatusAdmin(admin.ModelAdmin):  
    ordering = ('description',) 
admin.site.register(MatchStatus, MatchStatusAdmin)

admin.site.register(MustReadWatch)

class ContextBlurbModelForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label = 'Context Blurb: 500 characters', required=True)
    class Meta:
        model = Match
        fields = '__all__' 

class ContextBlurbAdmin(admin.ModelAdmin):  
    form = ContextBlurbModelForm
admin.site.register(ContextBlurb, ContextBlurbAdmin)

