from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from matchday import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'matchstatus', views.MatchStatusViewSet)
router.register(r'clubs', views.ClubViewSet)
router.register(r'matches', views.MatchViewSet)
router.register(r'activematches', views.ActiveMatchViewSet, 'match-active')
router.register(r'competitions', views.CompetitionViewSet)
router.register(r'clubswithcrests', views.ClubWithCrestViewSet)
router.register(r'mustreadwatch', views.MustReadWatchViewSet),
router.register(r'contextblurb', views.ContextBlurbViewSet)
router.register(r'tables', views.TableViewSet)
router.register(r'cotw', views.CrestOfTheWeekViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

