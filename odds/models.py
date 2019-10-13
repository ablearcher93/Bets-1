from django.db import models

# Create your models here.


class Sport(models.Model):
    title = models.CharField(max_length=200)


class League(models.Model):
    title = models.CharField(max_length=255)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)


class Event(models.Model):
    date = models.CharField(max_length=200)
    pl1 = models.CharField(max_length=200)
    pl2 = models.CharField(max_length=200)
    League = models.ForeignKey(League, on_delete=models.CASCADE)


class MainMarket(models.Model):
    cf1 = models.FloatField()
    #    DecimalField(max_digits=4, decimal_places=2)
    cfX = models.CharField(max_length=200)
    cf2 = models.FloatField()
    ref = models.URLField()
    bmk = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_update = models.DateTimeField(auto_now=True)


class MainMarket_for_graphs(models.Model):
    type = models.CharField(max_length=200)
    #    DecimalField(max_digits=4, decimal_places=2)
    date = models.DateTimeField()
    bwin = models.FloatField()
    onexstavka = models.FloatField()
    fonbet = models.FloatField()
    tennesi = models.FloatField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)