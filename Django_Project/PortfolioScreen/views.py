from django.shortcuts import render
from django.http import HttpResponse, request
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure
from django.contrib.auth.decorators import login_required
from django.template import context


@login_required
def PortfolioScreen(request):
    context = {
        'Portfolio': Portfolio.objects.all()
    }
    return render(request, 'PortfolioScreen/main.html', context)


@login_required
def about(request):
    return render(request, 'PortfolioScreen/about.html', {'title:': 'About'})


@login_required
def table(request):
    context = {
        'Portfolioparam': 'eingabe',
    }
    return render(request, 'pages/table.html', context)


@login_required
def table_portfolio(request, portfolio):
    context = {
        'Portfolioparam': portfolio,
        'Portfolios': Portfolio.objects.all(),
        'Stocks': Stock.objects.all(),
        'title': "Portfolio Table",
        'PortfolioFigures': Portfolio.objects.filter(),
        # nur für diesen Benutzer genutzte Portfolios auswählen! (oben in POrtfolioScreen)
        # aus den Portfolios die einzelnen Aktien auswählen!
        # die zugehörigen Portfolio-Kennzahlen
    }
    return render(request, 'pages/table.html', context)


@login_required
def chart(request):
    return render(request, 'pages/chart.html', {'title': 'Charts'})


@login_required
def chart_portfolio(request, portfolioparam):
    context = {
        'portfolioparam': portfolioparam,
    }
    return render(request, 'pages/chart.html', context)


@login_required
def settings(request):
    return render(request, 'pages/settings.html', {'title': 'Settings'})


@login_required
def settings_portfolio(request, portfolioparam):
    context = {
        'portfolioparam': portfolioparam,
    }
    return render(request, 'pages/chart.html', context)
