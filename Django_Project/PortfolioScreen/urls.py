from django.urls import path
#from .FrontEndCode import exportingPortfolio
from . import views


urlpatterns = [
    path('main/', views.PortfolioScreen, name='PortfolioScreen'),
    path('about/', views.about, name="about"),
    #path('ExportCsv/', exportingPortfolio.exportCSV, name='exportCSV'),
    #path('ExportPDF/', exportingPortfolio.exportPDF, name='exportPDF'),
    path('validate_ticker_symbol/', views.validate_ticker_symbol,
         name='validate_ticker_symbol'),
    path('create_new_portfolio/', views.create_new_portfolio,
         name='create_new_portfolio'),
    path('save_composition', views.ajax_method, name='ajax_method'),
    path('', views.PortfolioScreen, name="portfolio-table"),
    path('table/', views.table, name="portfolio-table"),
    path('chart/', views.chart, name="portfolio-chart"),
    path('settings/', views.settings, name="portfolio-settings"),
    path('add_stock_to_portfolio/', views.add_stock_to_portfolio,
         name="add_stock_to_portfolio"),
    path('create_figures_from_scratch/<portfolio>', views.create_figures_from_scratch,
         name="create_figures_from_scratch"),
    path('table/<portfolio>/', views.datadisplay,
         name="datadisplay-pass"),
    path('chart/<portfolio>/', views.chart_portfolio,
         name="portfolio-chart-pass"),
    path('settings/<portfolio>/', views.settings_portfolio,
         name="portfolio-settings-pass"),
]
