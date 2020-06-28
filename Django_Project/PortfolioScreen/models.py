from django.db import models
from django.utils import timezone
from django.db.models import ManyToManyField, CharField, ForeignKey, OneToOneField, ManyToOneRel
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

from .temp_vars import portfolioStatic


class Tickersym:
    ticker = models.CharField()


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


class OverallFigure(models.Model):
    name = models.CharField(max_length=60)
    pythoncode = models.TextField(max_length=60)

    def __str__(self):
        return self.name


class PortfolioFigure(models.Model):
    overallfigure = models.ForeignKey(
        OverallFigure, on_delete=models.CASCADE, null=True)
    figureValue = models.FloatField(max_length=60, default=1.0)

    def __str__(self):
        return self.overallfigure.name


class Stock(models.Model):
    tickersymbol = models.CharField(max_length=60)
    price = models.CharField(max_length=60, null=True, default='')

    def __str__(self):
        return self.tickersymbol

    def get_all_stock_figures_right_order(self):
        # hier werden nur die Queries ausgegeben
        ordinary_figures = OverallFigure.objects.all()
        # hier erstmal alle Figures zu Stock in entsprechendem Portfolio auswählen
        all_stock_figures = StockFigure.objects.filter(
            stock__tickersymbol=self.tickersymbol).filter(portfolio__portfolioname=portfolioStatic.portfolioname)
        # hier jetzt die richtigen String-Values
        all_stock_figure_names = [
            figure.overallfigure.name for figure in all_stock_figures]
        print('allstockfigurenames', all_stock_figure_names)
        figure_right_order_list = {'': ''}
        for item in ordinary_figures:
            item = str(item)
            if item in all_stock_figure_names:
                print(self.tickersymbol)
                print(portfolioStatic.portfolioname)
                print(item)
                # paste value
                figure_right_order_list[item] = StockFigure.objects.filter(stock__tickersymbol=self.tickersymbol).filter(
                    portfolio__portfolioname=portfolioStatic.portfolioname).filter(overallfigure__name=item).get().stockfigureValue
            else:
                # empty item
                figure_right_order_list[item] = 'null'
        return figure_right_order_list


class Portfolio(models.Model):
    portfolioname = models.CharField(max_length=60)
    fundmanager = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = ManyToManyField(Stock)
    portfolio_figure = ManyToManyField(PortfolioFigure)

    def __str__(self):
        return self.portfolioname

    def get_absolute_url(self):
        return reverse("datadisplay-pass", kwargs={"portfolio": self.portfolioname})


class PortfolioFigureHeader(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, blank=True,
        null=True)
    # figures to be shown!
    figures = ManyToManyField(OverallFigure)

    def __str__(self):
        return self.portfolio.portfolioname

    def figure_list(self):
        all_stock_figure_names = [
            figure.name for figure in self.figures.all()]
        return all_stock_figure_names


class StockFigure(models.Model):
    overallfigure = models.ForeignKey(
        OverallFigure, on_delete=models.CASCADE, null=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=True)
    stockfigureValue = models.FloatField(max_length=60)

    def __str__(self):
        return self.overallfigure.name
    # Benutzer noch einrichten

    def value_access(self):
        return str(self.stockfigureValue)
