# Generated by Django 3.0.3 on 2021-02-10 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisponibilidadReserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacion', models.CharField(max_length=15)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('estado', models.CharField(default='LIBRE', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('numero_pedido', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('operacion', models.CharField(max_length=15)),
                ('peso', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('tiempo_carga', models.IntegerField()),
                ('tiempo_descarga', models.IntegerField()),
                ('peso', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Rol')),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('matricula', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=30)),
                ('tipo_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.TipoVehiculo')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibilidad_reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.DisponibilidadReserva')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoCompletado',
            fields=[
                ('numero_pedido', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('operacion', models.CharField(max_length=15)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('resultado', models.CharField(max_length=30)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Usuario')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Vehiculo')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Vehiculo'),
        ),
        migrations.AddField(
            model_name='disponibilidadreserva',
            name='tipo_vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.TipoVehiculo'),
        ),
        migrations.AddField(
            model_name='disponibilidadreserva',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Vehiculo'),
        ),
        migrations.CreateModel(
            name='ConfiguracionVehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacion', models.CharField(max_length=30)),
                ('fecha', models.DateTimeField()),
                ('tipo_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.TipoVehiculo')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ServiSaco.Vehiculo')),
            ],
        ),
    ]