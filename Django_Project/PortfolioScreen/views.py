from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock


def PortfolioScreen(request):
    context = {
        'Stocks': Stock.objects.all()
    }
    return render(request, 'PortfolioScreen/main.html', context)

def about(request):
    return render(request, 'PortfolioScreen/about.html', {'title:':'About'})

def table(request):
    context = {
        'Stocks': Stock.objects.all(),
        'title': "Portfolio Table"
    }
    return render(request, 'pages/table.html', context)

def chart(request):
    return render(request, 'pages/chart.html', {'title':'Charts'})

def settings(request):
    return render(request, 'pages/settings.html', {'title': 'Settings'})
