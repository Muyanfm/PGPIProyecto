from django.db import models
from django.contrib.auth.models import User
from django.forms import fields
# Create your models here.


class Rol(models.Model):
    nombre = models.CharField(max_length=30)  

    def __str__(self):
        return self.nombre


class Usuario(models.Model): 
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=30)
    tiempo_carga = models.IntegerField()
    tiempo_descarga = models.IntegerField()
    peso = models.IntegerField()

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    matricula = models.CharField(primary_key=True, max_length=7)
    estado = models.CharField(max_length=30)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    pesoactual = models.IntegerField()

    def __str__(self):
        return self.matricula

class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=6, primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion=models.CharField(max_length=50)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    operacion = models.CharField(max_length=15)
    peso = models.IntegerField()  

    def __str__(self):
        return self.numero_pedido


class ConfiguracionVehiculo(models.Model):
    operacion = models.CharField(max_length=30)
    fecha = models.DateTimeField()
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)

class DisponibilidadReserva(models.Model):
    operacion = models.CharField(max_length=15)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=30, default="LIBRE")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return "Hora: " + str(self.fecha_inicio.time()) + " | Vehiculo: " + str(self.vehiculo.matricula) + " | Tipo de vehiculo: " + str(self.tipo_vehiculo.nombre)

class Reserva(models.Model):
    disponibilidad_reserva = models.ForeignKey(DisponibilidadReserva, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

class PedidoCompletado(models.Model):
    numero_pedido = models.CharField(max_length=6, primary_key=True)
    operacion = models.CharField(max_length=15)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=30)
