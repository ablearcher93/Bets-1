from django.shortcuts import render,get_object_or_404 
from django.views.generic.list import ListView
from .models import MainMarket, Sport, League, Event
from django.core import serializers
from django.views.generic.base import TemplateResponseMixin, View
import re
import json
from django.http import JsonResponse
def Sport_list(request):
    context = {"sports": Sport.objects.all(),}
    return render(request,"odds/sport_list.html",context)
class ManageSportListView(ListView):
    model = Sport
    template_name = 'courses/manage/course/list.html'
    
class EventContentView(TemplateResponseMixin, View):
    template_name = 'odds/Events.html'
    def get(self, request, Event_id):
        events = get_object_or_404(Event,id=Event_id)
        g=MainMarket.objects.datetimes('date_update', 'second', order='DESC')[0]
        events_main_market = MainMarket.objects.filter(event_id=Event_id)
        events_main_market_current = MainMarket.objects.filter(event_id=Event_id, date_update=g)
#        with open('D:\WiseBet\parsers\Книга1.csv','wb') as csv_file:
#            write_csv(events_main_market_for_graphs, csv_file, field_order=["type","date","bwin","onexstavka","fonbet","tennesi"])
        sports=League.objects.raw("select* from odds_sport a inner join(SELECT count (title), sport_id	FROM public.odds_league	group by sport_Id) b on a.id=b.sport_id")
        graphs=MainMarket.objects.raw("select* from odds_mainmarket WHERE event_id = %s" % Event_id)

        h=serializers.serialize('json', events_main_market, fields=('bmk', 'cf1', 'cf2','cfX','date_update'))
#        h=json.load(h)
        json_graphs=h.replace('"model": "odds.mainmarket", "pk": ','')
        json_graphs=re.sub('{(\d){,5}, "fields": ','',json_graphs)
        #json_graphs=json_graphs.replace('{, "fields": ','')
        json_graphs=json_graphs.replace('}}','}')
        print(json_graphs)
        x=json.loads(json_graphs)
 
        return self.render_to_response({'events_main_market_last': events_main_market,'current_events':events_main_market_current, 'event_main': Event_id,'events': events, 'sports': sports, 'current_date':g, 'for_graphs': x})

class AjaxInfo(TemplateResponseMixin, View):
    def get(self, request, Event_id):
        g=MainMarket.objects.datetimes('date_update', 'second', order='DESC')[0]
        events_main_market = MainMarket.objects.filter(event_id=Event_id,date_update=g )
        a=[]
        for i in events_main_market:
        	a.append({
			"cf1": i.cf1,
			"cfX": i.cfX,
			"cf2": i.cf2,
			"bmk": i.bmk,
			"date_update": i.date_update})

        return JsonResponse({"current_info":a}, status=200)
    



class LeagueContentListView(TemplateResponseMixin, View):
    template_name = 'odds/league_list.html'

            
    def get(self, request, league_id):
        league = get_object_or_404(League,id=league_id)
        events = Event.objects.filter(League_id=league_id)
        sports=League.objects.raw("select* from odds_sport a inner join(SELECT count (title), sport_id	FROM public.odds_league	group by sport_Id) b on a.id=b.sport_id")
        return self.render_to_response({'league': league,'events': events, 'sports': sports})
    
class LeagueListView(TemplateResponseMixin, View):
    template_name = 'odds/Sports.html'
    def get(self, request, sport_id):
        sport = get_object_or_404(Sport,id=sport_id)
        sports=League.objects.raw("select* from odds_sport a inner join(SELECT count (title), sport_id	FROM public.odds_league	group by sport_Id) b on a.id=b.sport_id")
        leagues = League.objects.filter(sport_id=sport_id)
        return self.render_to_response({'sport': sport,'leagues': leagues, 'sports': sports})

def index(request):
#    sports = Sport.objects.all
    sports=League.objects.raw("select* from odds_sport a inner join(SELECT count (title), sport_id	FROM public.odds_league	group by sport_Id) b on a.id=b.sport_id")
    context = {'sports': sports}
    return render(request, 'odds/bsae.html', context)

#def index(request):
#    events = MainMarket.objects.all()
#    context = {'events': events}
#    return render(request, 'odds/bet_page.html', context)
## Create your views here.
##class ArticleListView(ListView):
##
##    model = League
##
##    def get_context_data(self, **kwargs):
##        context = super().get_context_data(**kwargs)
##        return context
##
#class PublisherBookList(ListView):
#
#    template_name = 'odds/league_list.html'
#
#    def get_queryset(self):
#        return League.objects.filter(sport=self.sport)