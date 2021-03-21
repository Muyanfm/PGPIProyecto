from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("user", "rol")
    list_filter = ("rol",)

admin.site.register(Usuario, UsuarioAdmin)

class RolAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    list_filter = ("nombre",)

admin.site.register(Rol, RolAdmin)

class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tiempo_carga", "tiempo_descarga","peso")
    list_filter = ("nombre",)

admin.site.register(TipoVehiculo, TipoVehiculoAdmin)

class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("usuario","estado", "tipo_vehiculo", "matricula","pesoactual")
    list_filter = ("usuario", "estado","tipo_vehiculo")

admin.site.register(Vehiculo, VehiculoAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ("numero_pedido", "nombre", "direccion","vehiculo", "operacion","peso")
    list_filter = ("vehiculo","peso","operacion")
   
admin.site.register(Pedido, PedidoAdmin)


class ConfiguracionesVehiculoAdmin(admin.ModelAdmin):
    list_display = ("operacion", "fecha", "vehiculo", "tipo_vehiculo")
    list_filter = ("operacion", "fecha", "vehiculo", "tipo_vehiculo")
   
admin.site.register(ConfiguracionVehiculo, ConfiguracionesVehiculoAdmin)


class DisponibilidadReservaAdmin(admin.ModelAdmin):
    list_display = ("operacion", "fecha_inicio", "fecha_fin","estado", "vehiculo", "tipo_vehiculo")
    list_filter = ("operacion", "fecha_inicio", "fecha_fin", "estado", "vehiculo", "tipo_vehiculo")
   
admin.site.register(DisponibilidadReserva, DisponibilidadReservaAdmin)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ("disponibilidad_reserva", "pedido")
    list_filter = ("disponibilidad_reserva", "pedido")
   
admin.site.register(Reserva, ReservaAdmin)
