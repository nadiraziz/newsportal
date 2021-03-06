# Generated by Django 4.0 on 2021-12-28 14:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_interestedlike_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='interestedlike',
            name='interest',
        ),
        migrations.RemoveField(
            model_name='interestedlike',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Interested',
        ),
        migrations.DeleteModel(
            name='InterestedLike',
        ),
    ]
