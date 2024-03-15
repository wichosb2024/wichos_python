# Generated by Django 2.2.4 on 2021-05-01 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cajaCuenta', '0004_receta_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receta',
            name='insumos',
        ),
        migrations.AddField(
            model_name='lineadereceta',
            name='fkReceta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cajaCuenta.Receta'),
        ),
    ]
