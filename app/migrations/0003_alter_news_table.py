# Generated by Django 5.0.2 on 2024-03-02 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_news_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='news',
            table='app_news',
        ),
    ]