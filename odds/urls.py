from django.urls import path

from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('league/<int:league_id>/',views.LeagueContentListView.as_view(),name='league_list'),
    path('sport/<int:sport_id>/',views.LeagueListView.as_view(),name='Sports'),
    path('event/<int:Event_id>/',views.EventContentView.as_view(),name='Events'),
    path('event/<int:Event_id>/ajax/current_info', views.AjaxInfo.as_view(), name='current_info')
    #path('index',views.aa,name='aa')
         ]