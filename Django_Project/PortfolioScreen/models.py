from django.db import models
from django.utils import timezone
from django.db.models import ManyToManyField, CharField, ForeignKey, OneToOneField, ManyToOneRel
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Chart(models.Model):
    chartName = models.CharField(
        max_length=60, blank=True, default='chart')
    chartType = models.CharField(max_length=60, blank=True)


def countnumber(sender, instance, **kwargs):
    if instance.chartName == 'chart':
        instance.chartName = str(instance.chartName)+str(Chart.objects.count())
        instance.save()
        print(str(instance.chartName))


post_save.connect(countnumber, sender=Chart)


class PortfolioFigure(models.Model):
    portfolioname = models.CharField(max_length=60)
    figureValue = models.FloatField(max_length=60)

    def __str__(self):
        return self.portfolioname


class Stock(models.Model):
    ISIN = models.CharField(max_length=60)

    def __str__(self):
        return self.ISIN


class StockFigure(models.Model):
    stockname = models.CharField(max_length=60)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stockfigureValue = models.FloatField(max_length=60)

    def __str__(self):
        return self.stockname


class Portfolio(models.Model):
    portfolioname = models.CharField(max_length=60)
    fundmanager = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = ManyToManyField(Stock)
    figure = models.ForeignKey(PortfolioFigure, on_delete=models.CASCADE)

    def __str__(self):
        return self.portfolioname


# Benutzer noch einrichten
