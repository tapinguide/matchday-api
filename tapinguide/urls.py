from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from matchday import views

router = routers.DefaultRouter()
router.register(r'matchstatus', views.MatchStatusViewSet)
router.register(r'clubs', views.ClubViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'activematches', views.ActiveMatchViewSet, 'match-active')
router.register(r'competitions', views.CompetitionViewSet)
router.register(r'clubswithcrests', views.ClubWithCrestViewSet)
router.register(r'links', views.LinkViewSet),
router.register(r'contextblurb', views.ContextBlurbViewSet)


# First route goes to home page
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

