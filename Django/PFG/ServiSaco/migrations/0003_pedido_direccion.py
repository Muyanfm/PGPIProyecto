# Generated by Django 3.0.3 on 2021-03-10 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServiSaco', '0002_vehiculo_pesoactual'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='direccion',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]