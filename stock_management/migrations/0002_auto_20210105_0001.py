# Generated by Django 2.0.7 on 2021-01-04 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='category',
            field=models.CharField(blank=True, max_length=51, null=True),
        ),
    ]