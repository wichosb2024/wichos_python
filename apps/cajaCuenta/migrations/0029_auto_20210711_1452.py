# Generated by Django 2.2.4 on 2021-07-11 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajaCuenta', '0028_auto_20210709_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]
