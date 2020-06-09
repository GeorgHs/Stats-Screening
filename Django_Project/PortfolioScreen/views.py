from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure, OverallFigure
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import context
from django.http.response import JsonResponse


import yfinance as yf
import time
from django.urls import reverse


@login_required
def PortfolioScreen(request):
    context = {
        'Users': request.user,
        'Portfolios': Portfolio.objects.filter(fundmanager__exact=request.user),
    }
    return render(request, 'PortfolioScreen/main.html', context)


@login_required
def datadisplay(request, portfolio):
    # draw stuff from yfinance and then compute everything that hasn't been computed yet
    # Immer zuerst in Datenbank schauen: 1. ist es leer, 2. Wenn leer, dann aus Yahoo Finance ziehen, 3. per Rechtsklick kann entweder neu berechnet werden oder umbenannt (bei Namen)
    context = {
        'UserSpec': request.user,
        'Portfolioparam': portfolio,
        'Portfolios': Portfolio.objects.filter(fundmanager__exact=request.user),
        # request.user.objects(),
        'ordinary_figures': OverallFigure.objects.all(),
        'PortfolioObject': Portfolio.objects.get(portfolioname__exact=portfolio),
        'Stocks': Portfolio.objects.get(portfolioname__exact=portfolio).stock.all(),
        'title': "Portfolio Table",
        'PortfolioFigures': Portfolio.objects.filter(),
        # nur für diesen Benutzer genutzte Portfolios auswählen! (oben in POrtfolioScreen)
        # aus den Portfolios die einzelnen Aktien auswählen!
        # die zugehörigen Portfolio-Kennzahlen
    }
    print(Portfolio.objects.get(portfolioname__exact=portfolio).stock.all())
    return render(request, 'PortfolioScreen/datadisplay.html', context)


@login_required
def create_new_portfolio(request):
    if request.method == "POST":
        stockliste = request.POST.dict()
        _portfolioname = request.POST.get('portfolionamepost')
        print(stockliste)
        # komplizierte Konvertierungen um an die Werte im dict zu kommen - Verbesserungen willkommen!
        l = []
        [l.extend([v]) for v in stockliste.items()]

        print(len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)))

        # portfolio erstellen:
        if len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)) == 0:
            portfolio = Portfolio(
                portfolioname=_portfolioname, fundmanager=request.user)
            portfolio.save()
            # stocks erstellen
            for x in range(2, len(l)):  # ersten 2 sind token und portfolioname
                # erstelle Stock
                portfolio.stock.create(Tickersymbol=str(l[x][1]))
            portfolio.save()
            # in Warteschleife, bis in Datenbank erstellt!
            while len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)) == 0:
                time.sleep(1)
                print("warte bis erstellt")
            # sobald erstellt, weiterleiten bitte

            context = {
                'Users': request.user,
                'Portfolios': Portfolio.objects.filter(fundmanager__exact=request.user),
            }
            print("alles ok")
            data = {
                'status': 0,  # ist Erfolg
                'message': 'everything went alright',
                'redirecturl': 'table/'+_portfolioname,
            }
            return JsonResponse(data)
        else:
            messages.error(request, f'Portfolio of that name already exists')

            print("Portfolio schon vorhanden")
            data = {
                'status': 1,  # ist Misserfolg
                'message': 'This Portfolio exists already. Choose another name.',
            }
            return JsonResponse(data)


@login_required
def create_figures_from_scratch(request, portfolio):
    OverallFigure.objects.bulk_create([
        OverallFigure(overallfigurename="Beta", pythoncode="import pandas as pd \n"
                      "import numpy as np \n"
                      "import matplotlib.pyplot as plt \n"
                      "import pandas_datareader as web \n"
                      "from scipy import stats \n"
                      "import seaborn as sns \n"
                      "# Create a list of tickers and weights \n"
                      "tickers = ['BND', 'VB', 'VEA', 'VOO', 'VWO'] \n"
                      "wts = [0.1,0.2,0.25,0.25,0.2] \n"
                      "price_data = web.get_data_yahoo(tickers, \n"
                      "start = '2013-01-01', \n"
                      "end = '2018-03-01') \n"
                      "price_data = price_data['Adj Close'] \n"
                      "ret_data = price_data.pct_change()[1:] \n"
                      "port_ret = (ret_data * wts).sum(axis = 1) \n"
                      "benchmark_price = web.get_data_yahoo('SPY', \n"
                      "start = '2013-01-01', \n"
                      "end = '2018-03-01') \n"
                      "benchmark_ret = benchmark_price['Adj Close'].pct_change()[1:] \n"
                      "(beta, alpha) = stats.linregress(benchmark_ret.values, "
                      "port_ret.values)[0:2]"
                      "print('The portfolio beta is', round(beta, 4)) \n"
                      ),

        OverallFigure(overallfigurename="Alpha", pythoncode=""),
        OverallFigure(overallfigurename="Daily Returns", pythoncode=""),
    ])

    return redirect('datadisplay-pass', portfolio)


@login_required
def add_stock_to_portfolio(request):
    if request.method == "POST":
        stockliste = request.POST.dict()
        _portfolioname = request.POST.get('portfolionamepost')
        # komplizierte Konvertierungen um an die Werte im dict zu kommen - Verbesserungen willkommen!
        l = []
        [l.extend([v]) for v in stockliste.items()]

        print(len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)))

        # portfolio erstellen - das bedeutet, dass das Portfolio vorhanden ist!
        if len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)) == 1:
            try:
                dasPortfolio = Portfolio.objects.filter(
                    portfolioname__exact=_portfolioname).get()
                print(l)
                for x in range(2, len(l)):  # ersten 2 sind token und portfolioname
                    # erstelle Stock
                    dasPortfolio.stock.create(Tickersymbol=str(l[x][1]))
                    print(str(l[x][1]) + " hinzugefügt")
                    dasPortfolio.save()
                EingabeDerDaten = {
                    'status': 0,  # ist Erfolg
                    'message': 'everything went alright',
                    'redirecturl': 'table/'+_portfolioname,
                }
            except:
                EingabeDerDaten = {
                    'status': 1,  # ist Erfolg
                    'message': 'could not be added',
                    'redirecturl': 'table/'+_portfolioname,
                }
            return JsonResponse(EingabeDerDaten, safe=False)


@login_required
def validate_ticker_symbol(request):
    if request.method == "POST":
        tickersymbol = request.POST.get('tickersymbPost')
        exists = False
        priceonStock = ''
        nameonStock = ''
        currencyonStock = ''
        try:
            tksym = yf.Ticker(str(tickersymbol))
            datastock = tksym.info
            print(datastock)
            exists = True
            nameonStock = datastock['shortName']
            # das hier ist float
            priceonStock = datastock['regularMarketPrice']
            currencyonStock = datastock['currency']
        except:
            exists = False
        Stockdata = {
            'exists': exists,
            'tickersymb': tickersymbol,
            'name': nameonStock if len(nameonStock) != 0 else '',
            'currency': currencyonStock if len(currencyonStock) != 0 else '',
            # das hier ist float
            'price': priceonStock if priceonStock != 0 else 0,
        }
        # hier den Gültigkeitswert des Tickers abspeichern!
        request.session['exists'] = Stockdata
        return JsonResponse(request.session.get('exists'), safe=False)
    else:
        return JsonResponse(request.session.get('exists'), safe=False)


def ajax_method():
    return HttpResponse("Response")


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
