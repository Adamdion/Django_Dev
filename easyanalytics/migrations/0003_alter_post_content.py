# Generated by Django 4.2 on 2023-04-27 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyanalytics', '0002_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.JSONField(null=True),
        ),

    ]
