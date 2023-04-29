
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyanalytics', '0008_alter_post_plot_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='plot_data',
            field=models.JSONField(default=dict, blank=True, null=True),
        ),
    ]
