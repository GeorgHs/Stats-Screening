# Generated by Django 3.0.6 on 2020-06-04 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chartName', models.CharField(blank=True, default='chart', max_length=60)),
                ('chartType', models.CharField(blank=True, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='OverallFigure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overallfigurename', models.CharField(default='asdf', max_length=60)),
                ('pythoncode', models.TextField(default='asdf', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolioname', models.CharField(max_length=60)),
                ('fundmanager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tickersymbol', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='StockFigure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockname', models.CharField(max_length=60)),
                ('stockfigureValue', models.FloatField(max_length=60)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PortfolioScreen.Stock')),
                ('stockmainfigure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PortfolioScreen.OverallFigure')),
            ],
        ),
        migrations.CreateModel(
            name='PortfolioFigure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('figurename', models.CharField(default='beta', max_length=60)),
                ('figureValue', models.FloatField(max_length=60)),
                ('portfoliomainfigure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PortfolioScreen.OverallFigure')),
                ('portfolioname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PortfolioScreen.Portfolio')),
            ],
        ),
        migrations.AddField(
            model_name='portfolio',
            name='stock',
            field=models.ManyToManyField(to='PortfolioScreen.Stock'),
        ),
    ]
