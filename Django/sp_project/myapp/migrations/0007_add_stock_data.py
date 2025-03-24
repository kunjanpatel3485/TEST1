from django.db import migrations

def add_initial_stocks(apps, schema_editor):
    Stock = apps.get_model('myapp', 'Stock')
    Stock.objects.create(
        companyName="Tesla",
        symbol="TSLA",
        currentPrice=200,
        peRatio=20.5,  # Provide a valid value
        pbRatio=4.3,
        dividendYield=1.2
    )

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_company_watchlist'),  
    ]

    operations = [
        migrations.RunPython(add_initial_stocks),
    ]
