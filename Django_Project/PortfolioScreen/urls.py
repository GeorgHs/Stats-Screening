from django.urls import path
#from .FrontEndCode import exportingPortfolio
from . import views

urlpatterns = [
    path('main/', views.PortfolioScreen, name='PortfolioScreen'),
    path('about/', views.about, name="about"),
    #path('ExportCsv/', exportingPortfolio.exportCSV, name='exportCSV'),
    #path('ExportPDF/', exportingPortfolio.exportPDF, name='exportPDF'),
    path('new/<ISIN>', views.operation, name='operation-isin'),
    path('', views.PortfolioScreen, name="portfolio-table"),
    path('table/', views.table, name="portfolio-table"),
    path('chart/', views.chart, name="portfolio-chart"),
    path('settings/', views.settings, name="portfolio-settings"),
    path('table/<portfolio>/', views.datadisplay,
         name="datadisplay-pass"),
    path('chart/<portfolio>/', views.chart_portfolio,
         name="portfolio-chart-pass"),
    path('settings/<portfolio>/', views.settings_portfolio,
         name="portfolio-settings-pass"),
]
