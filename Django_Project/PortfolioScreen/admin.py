from django.contrib import admin
from .models import Stock, Portfolio, PortfolioFigure, Chart, StockFigure, OverallFigure, PortfolioFigureHeader


admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(PortfolioFigure)
admin.site.register(Chart)
admin.site.register(StockFigure)
admin.site.register(OverallFigure)
admin.site.register(PortfolioFigureHeader)
