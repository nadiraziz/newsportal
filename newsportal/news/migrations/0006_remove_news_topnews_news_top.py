# Generated by Django 4.0 on 2021-12-26 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_news_topnews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='topNews',
        ),
        migrations.AddField(
            model_name='news',
            name='Top',
            field=models.BooleanField(default=False),
        ),
    ]
