# Generated by Django 4.0 on 2021-12-25 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.news')),
            ],
        ),
    ]