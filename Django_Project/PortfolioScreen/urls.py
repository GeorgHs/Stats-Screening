from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.PortfolioScreen, name='PortfolioScreen'),
    path('about/', views.about, name="about"),
    path('ExportExcel/', views.exportExcel, name='exportExcel'),
    path('ExportCsv/', views.exportCSV, name='exportCSV'),
    path('ExportPDF/', views.exportPDF, name='exportPDF'),
    path('validate_ticker_symbol/', views.validate_ticker_symbol,
         name='validate_ticker_symbol'),
    path('create_new_portfolio/', views.create_new_portfolio,
         name='create_new_portfolio'),
    path('add_figure_to_column/', views.add_figure_to_column,
         name='add_figure_to_column'),
    path('add_overall_figure', views.add_overall_figure,
         name='add_overall_figure'),
    path('save_composition', views.ajax_method, name='ajax_method'),
    path('', views.PortfolioScreen, name="portfolio-table"),
    path('chart/', views.chart, name="portfolio-chart"),
    path('settings/', views.settings, name="portfolio-settings"),
    path('add_stock_to_portfolio/', views.add_stock_to_portfolio,
         name="add_stock_to_portfolio"),
    path('remove_portfolio_figure/', views.remove_portfolio_figure,
         name='remove_portfolio_figure'),
    path('create_figures_from_scratch/<portfolio>', views.create_figures_from_scratch,
         name="create_figures_from_scratch"),
    path('create_figures_from_scratch_no_portfolio/', views.create_figures_from_scratch_no_portfolio,
         name="create_figures_from_scratch_no_portfolio"),
    path('hide_figure_column/<figureid>/<portfolio>',
         views.hide_figure_column, name='hide_figure_column'),
    path('delete_portfolio',
         views.delete_portfolio, name='delete_portfolio'),
    path('table/<portfolio>/', views.datadisplay,
         name="datadisplay-pass"),
    path('chart/<portfolio>/', views.chart_portfolio,
         name="portfolio-chart-pass"),
    path('settings/<portfolio>/', views.settings_portfolio,
         name="portfolio-settings-pass"),
]
