# Generated by Django 2.2.4 on 2021-06-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajaCuenta', '0022_auto_20210602_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='abreviatura',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
