# Generated by Django 2.2.4 on 2021-05-01 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajaCuenta', '0003_auto_20210501_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='nombre',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
