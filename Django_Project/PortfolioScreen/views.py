import csv
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure, OverallFigure
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import context
from django.http.response import JsonResponse
from .temp_vars import portfolioStatic, stockStatic
import xlsxwriter


import yfinance as yf
import time
from django.urls import reverse
from PortfolioScreen.models import PortfolioFigureHeader
from io import StringIO


@login_required
def PortfolioScreen(request):
    context = {
        'Users': request.user,
        'Portfolios': Portfolio.objects.filter(fundmanager__exact=request.user),
        'OverallFigures': OverallFigure.objects.all(),
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
        'portfolio_header': load_header(portfolio),
        'Stocks': Portfolio.objects.get(portfolioname__exact=portfolio).stock.all(),
        'title': "Portfolio Table",
        'PortfolioFigures': Portfolio.objects.get(portfolioname__exact=portfolio).portfolio_figure.all(),
        # nur für diesen Benutzer genutzte Portfolios auswählen! (oben in POrtfolioScreen)
        # aus den Portfolios die einzelnen Aktien auswählen!
        # die zugehörigen Portfolio-Kennzahlen
    }
    portfolioStatic.portfolioname = portfolio
    print(Portfolio.objects.get(portfolioname__exact=portfolio).stock.all())
    return render(request, 'PortfolioScreen/datadisplay.html', context)


def load_header(_portfolio):
    header = None
    try:
        header = PortfolioFigureHeader.objects.filter(
            portfolio__portfolioname=_portfolio).get()
    except Exception:
        print("Couldn't load PortfolioFigureHeader "+_portfolio)
    return header


@login_required
def exportCSV(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C',
                     '"Testing"', "Here's a quote"])

    return response


@login_required
def add_overall_figure(request):
    data = {'': ''}
    _figurename = request.POST.get('figurename')
    _pythoncode = request.POST.get('pythoncode')
    print(_figurename, '  ', _pythoncode)
    try:
        ovf = OverallFigure(name=_figurename, pythoncode=_pythoncode)
        ovf.save()
        data['status'] = 0
        data['msg'] = _figurename + ' was added'
    except Exception:
        data['status'] = 1
        data['msg'] = _figurename + ' could not be added'

    return JsonResponse(data)


@login_required
def exportExcel(request):
    output = StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Some Data')
    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename="some_file_name.xlsx"'

    response.write(output.getvalue())

    return response


@login_required
def exportPDF(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


@login_required
def hide_figure_column(request, figureid, portfolio):
    data = {'': ''}
    try:
        portfolioContainingFigure = PortfolioFigureHeader.objects.filter(
            portfolio__portfolioname=portfolio).get()
        figureToBeDeleted = OverallFigure.objects.filter(name=figureid).get()
        portfolioContainingFigure.figures.remove(figureToBeDeleted)
        data['status'] = '1'
        data['message'] = "removed"
        data['redirecturl'] = str("table/"+portfolio),
        print(portfolioContainingFigure.figures.all())
    except Exception:
        data['status'] = '0'
        data['message'] = 'This figure is non-existent: ' + figureid
        print(data['message'])
    return JsonResponse(data)


@login_required
def remove_portfolio_figure(request):
    data = {'': ''}
    try:
        tobedeleted_list = Portfolio.objects.get(portfolioname__exact=request.POST.get(
            'portfolioid')).portfolio_figure.filter(overallfigure__name__startswith=request.POST.get('figureid')).all()
        [v.delete() for v in tobedeleted_list]
        data['status'] = 0
        data['msg'] = 'Wurde gelöscht'
    except Exception:
        data['status'] = 1
        data['msg'] = "Konnte nicht gefunden werden"
    return JsonResponse(data)


@login_required
def delete_portfolio(request):
    data = {'': ''}
    portfolioparam = request.POST.get('portfolio')
    print(portfolioparam)
    try:
        data['status'] = 0
        data['msg'] = 'Everything went well'
        data['redirecturl'] = ''
        Portfolio.objects.filter(portfolioname=portfolioparam).delete()
    except Exception:
        data['status'] = 1
        data['msg'] = 'Failed to remove ' + portfolioparam
    return JsonResponse(data)


@login_required
def add_figure_to_column(request):
    data = {'': ''}
    container = request.POST.get('whereid')
    figurename = request.POST.get('figurename')
    print('container ', container)
    print('figurename', figurename)
    thefigure = OverallFigure.objects.filter(name=figurename).get()
    if (container == 'tableregion'):
        try:
            HinzuzufuegenderHeader = PortfolioFigureHeader.objects.filter(
                portfolio__portfolioname=portfolioStatic.portfolioname).get()
            figureToBeDeleted = OverallFigure.objects.filter(
                name=figurename).get()
            HinzuzufuegenderHeader.figures.add(figureToBeDeleted)

            data['status'] = 0
            data['code'] = thefigure.pythoncode
        except Exception:
            data['status'] = 1
            data['code'] = ''
    elif container == 'portfolio-region':
        try:
            _figure = OverallFigure.objects.filter(name=figurename).get()
            pffigure = PortfolioFigure(
                overallfigure=_figure, figureValue='1.0')
            pffigure.save()
            print(portfolioStatic.portfolioname)
            Portfolio.objects.get(
                portfolioname__exact=portfolioStatic.portfolioname).portfolio_figure.add(pffigure)

            data['status'] = 0
            data['code'] = thefigure.pythoncode
        except Exception:
            data['status'] = 1
            data['code'] = 'failed'
    return JsonResponse(data)


@login_required
def create_new_portfolio(request):
    if request.method == "POST":

        stockliste = request.POST.dict()
        _portfolioname = request.POST.get('portfolionamepost')
        print(stockliste)
        # komplizierte Konvert2ierungen um an die Werte im dict zu kommen - Verbesserungen willkommen!
        l = []
        [l.extend([v]) for v in stockliste.items()]

        print(len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)))

        # portfolio erstellen:
        if len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)) == 0:
            _portfolio = Portfolio(
                portfolioname=_portfolioname, fundmanager=request.user)
            _portfolio.save()
            alphaof = OverallFigure.objects.filter(name='Alpha').get()
            betaof = OverallFigure.objects.filter(name='Beta').get()
            dailyreturnof = OverallFigure.objects.filter(
                name='Daily Returns').get()

            print('portfolioname: ', _portfolio)
            header = PortfolioFigureHeader(portfolio=_portfolio)
            header.save()
            header.figures.add(alphaof)
            header.figures.add(betaof)
            header.figures.add(dailyreturnof)
            header.save()

            print(header)
            # stocks erstellen
            for x in range(2, len(l)):  # ersten 2 sind token und portfolioname
                # erstelle Stock
                # price und name ziehen!
                stockStatic.info_static = yf.Ticker(str(l[x][1])).info
                stockStatic.hist_data = yf.Ticker(str(l[x][1])).history()
                _stock_info = stockStatic.info_static

                selected_stock = _portfolio.stock.create(
                    tickersymbol=str(l[x][1]), fullname=_stock_info['longName'], price=_stock_info['regularMarketPrice'])

                # den Stock ziehen
                for the_figure in OverallFigure.objects.all():
                    stock_figure = StockFigure(
                        overallfigure=the_figure, stock=selected_stock, portfolio=_portfolio, stockfigureValue=run_figure_pythoncode(stockStatic.hist_data, stockStatic.info_static, the_figure.pythoncode))
                    stock_figure.save()

            _portfolio.save()
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
                'redirecturl': str("table/"+_portfolioname),
            }
            return JsonResponse(data)
        else:
            messages.error(request, f'Portfolio of that name already exists')

            print("Stock schon vorhanden")
            data = {
                'status': 1,  # ist Misserfolg
                'message': 'This Portfolio exists already. Choose another name.',
            }
            return JsonResponse(data)


def create_figures():
    OverallFigure.objects.bulk_create([
        OverallFigure(name="Beta", pythoncode="import pandas as pd \n"
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

        OverallFigure(name="Alpha", pythoncode=""),
        OverallFigure(name="Daily Returns", pythoncode=""),
    ])


@login_required
def create_figures_from_scratch(request, _portfolio):
    create_figures()
    # nur redirecten, wenn auch Argument vorhanden ist
    return redirect('datadisplay-pass', _portfolio)


def create_figures_from_scratch_no_portfolio(request):
    create_figures()
    return redirect('portfolio-table')


@login_required
def add_stock_to_portfolio(request):
    if request.method == "POST":
        stockliste = request.POST.dict()
        _portfolioname = request.POST.get('portfolionamepost')
        # komplizierte Konvertierungen um an die Werte im dict zu kommen - Verbesserungen willkommen!
        l = []
        [l.extend([v]) for v in stockliste.items()]

        # portfolio erstellen - das bedeutet, dass das Portfolio vorhanden ist!
        if len(Portfolio.objects.filter(portfolioname__exact=_portfolioname)) == 1:
            # try:
            dasPortfolio = Portfolio.objects.filter(
                portfolioname__exact=_portfolioname).get()

            for x in range(2, len(l)):  # ersten 2 sind token und portfolioname
                # erstelle Stock
                stockStatic.info_static = yf.Ticker(str(l[x][1])).info
                stockStatic.hist_data = yf.Ticker(str(l[x][1])).history()
                _stock_info = stockStatic.info_static

                selected_stock = dasPortfolio.stock.create(
                    tickersymbol=str(l[x][1]), fullname=_stock_info['longName'], price=_stock_info['regularMarketPrice'])

                # den Stock ziehen
                for the_figure in OverallFigure.objects.all():
                    stock_figure = StockFigure(
                        overallfigure=the_figure, stock=selected_stock, portfolio=dasPortfolio, stockfigureValue=run_figure_pythoncode(stockStatic.hist_data, stockStatic.info_static, the_figure.pythoncode))
                    stock_figure.save()

                dasPortfolio.save()
            EingabeDerDaten = {
                'status': 0,  # ist Erfolg
                'message': 'everything went alright',
                'redirecturl': 'table/'+_portfolioname,
            }
            return JsonResponse(EingabeDerDaten)
            # except Exception:
            EingabeDerDaten = {
                'status': 1,  # ist Erfolg
                'message': 'could not be added',
                'redirecturl': 'table/'+_portfolioname,
            }
            return JsonResponse(EingabeDerDaten)


def run_figure_pythoncode(histdata, stock_info, pythoncode):
    import sys
    dailyreturns = []
    ausgabe = ""
    codeOut = StringIO()
    sys.stdout = codeOut
    pythoncode = """dailyreturns = []
for x in range(1, len(histdata['Close'])):
    dailyreturn = ((histdata['Close'][x]-histdata['Close'][x-1])/histdata['Close'][x])
    dailyreturns.append(dailyreturn)
ausgabe = str(round(dailyreturns[-1]*100, 2))+'%'
print(ausgabe)"""

    exec(pythoncode)
    sys.stdout = codeOut
    s = codeOut.getvalue()
    print(s)
    ausgabe = s
    # Ausgabe immer als String bitte! Somit kann z.B. % angehängt werden!
    return ausgabe


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
