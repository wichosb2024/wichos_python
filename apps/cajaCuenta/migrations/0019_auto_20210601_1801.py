# Generated by Django 2.2.4 on 2021-06-02 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cajaCuenta', '0018_pedido_cobrado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuenta',
            name='fkCategoriaIncidencia',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='fkCategoriaIncidencia',
        ),
        migrations.DeleteModel(
            name='CategoriaIncidencia',
        ),
    ]
