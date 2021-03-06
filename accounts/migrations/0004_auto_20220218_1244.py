# Generated by Django 3.2.11 on 2022-02-18 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20220217_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loading',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Finished', 'Finished')], max_length=200, null=True),
        ),
    ]
