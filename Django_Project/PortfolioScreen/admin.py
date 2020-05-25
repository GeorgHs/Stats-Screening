from django.contrib import admin
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure

admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(PortfolioFigure)
admin.site.register(Chart)
admin.site.register(StockFigure)
