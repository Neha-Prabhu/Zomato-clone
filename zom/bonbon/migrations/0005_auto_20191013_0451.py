# Generated by Django 2.2.4 on 2019-10-12 23:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bonbon', '0004_res_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='time',
            new_name='date',
        ),
        migrations.AddField(
            model_name='bill',
            name='day',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]