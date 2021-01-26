# Generated by Django 2.0.7 on 2021-01-26 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0002_auto_20210105_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='approval',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='issue_by',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='approval',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='issue_by',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='issue_to',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='stockhistory',
            name='reorder_level',
        ),
        migrations.RemoveField(
            model_name='stockrequesthistory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='stockrequesthistory',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='stockrequesthistory',
            name='receive_by',
        ),
        migrations.RemoveField(
            model_name='stockrequesthistory',
            name='reorder_level',
        ),
        migrations.AddField(
            model_name='stockrequesthistory',
            name='stock_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='stockrequesthistory',
            name='approval',
            field=models.CharField(default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='stockrequesthistory',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
