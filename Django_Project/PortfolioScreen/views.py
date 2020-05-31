from django.shortcuts import render
from django.http import HttpResponse, request
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.template import context


@login_required
def PortfolioScreen(request):
    context = {
        'Users': request.user,
        'Portfolios': Portfolio.objects.filter(fundmanager__exact=request.user),
    }
    return render(request, 'PortfolioScreen/main.html', context)


@login_required
def datadisplay(request, portfolio):
    context = {
        'UserSpec': request.user,
        'Portfolioparam': portfolio,
        'Portfolios': Portfolio.objects.filter(fundmanager__exact=request.user),
        # request.user.objects(),
        'PortfolioObject': Portfolio.objects.get(portfolioname__exact=portfolio),
        'Stocks': Portfolio.objects.get(portfolioname__exact=portfolio).stock.all(),
        'title': "Portfolio Table",
        'PortfolioFigures': Portfolio.objects.filter(),
        # nur für diesen Benutzer genutzte Portfolios auswählen! (oben in POrtfolioScreen)
        # aus den Portfolios die einzelnen Aktien auswählen!
        # die zugehörigen Portfolio-Kennzahlen
    }
    return render(request, 'PortfolioScreen/datadisplay.html', context)


@login_required
def operation(request, ISIN):
    iscorrect = False
    print("executed", ISIN)
    if ISIN == "hallo":
        iscorrect = True
    return iscorrect


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
def table_portfolio(request):

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
