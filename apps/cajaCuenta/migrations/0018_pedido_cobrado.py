# Generated by Django 2.2.4 on 2021-05-25 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajaCuenta', '0017_auto_20210524_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='cobrado',
            field=models.BooleanField(default=False),
        ),
    ]