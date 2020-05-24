from django.db import models
from django.utils import timezone
from django.db.models import ManyToManyField, CharField, ForeignKey, OneToOneField, ManyToOneRel
from django.contrib.auth.models import User


class Chart(models.Model):
    chartType = models.CharField


class PortfolioFigure(models.Model):
    figureName = models.CharField(max_length=60)
    figureValue = models.FloatField(max_length=60)


class Stock(models.Model):
    ISIN = models.CharField(max_length=60)

    def __str__(self):
        return self.ISIN


class StockFigure(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    figureName = models.CharField(max_length=60)
    figureValue = models.FloatField(max_length=60)


class Portfolio(models.Model):
    name = models.CharField(max_length=60)
    stock = ManyToManyField(Stock)
    figure = models.ForeignKey(PortfolioFigure, on_delete=models.CASCADE)


# Benutzer noch einrichten
