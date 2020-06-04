from django.shortcuts import render
from django.http import HttpResponse, request
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.template import context
from django.http.response import JsonResponse
import yfinance as yf


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
def create_new_portfolio(request):
    if request.method == 'POST':
        print(request.POST.get('stockList'))


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
