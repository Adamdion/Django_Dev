# Generated by Django 4.2 on 2023-04-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyanalytics', '0007_alter_post_plot_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='plot_data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
