from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure
from django.contrib.auth.decorators import login_required


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
        'Stocks': Stock.objects.all(),
        'title': "Portfolio Table"
    }
    return render(request, 'pages/table.html', context)


@login_required
def chart(request):
    return render(request, 'pages/chart.html', {'title': 'Charts'})


@login_required
def settings(request):
    return render(request, 'pages/settings.html', {'title': 'Settings'})
