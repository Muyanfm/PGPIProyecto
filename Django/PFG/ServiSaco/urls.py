from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import checkSimulacion, editarReserva, eliminarReserva, estadoVehiculos, gestionConfiguracion, gestionPedidos, historicoPedidos, home, index,checkNumPedido, lecturaMatricula, realizarReserva, reservas, resumenReserva, simulacion, verReserva,TomarPedidos

urlpatterns = [

    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', home),
    path('home/', home, name='home'),
    path('realizarReserva/checkNumPedido/', checkNumPedido, name='checkNumPedido'),
    path('realizarReserva/<str:numPedido>/<str:dia>', realizarReserva, name='realizarReserva'),
    path('realizarReserva/resumenReserva/<str:numPedido>/<str:idHueco>', resumenReserva, name='resumenReserva'),
    path('reservas/<str:filtroPedidosDia>', reservas, name='reservas'),
    path('reservas/editarReserva/<str:id>/<str:dia>', editarReserva, name='editarReservas'),
    path('reservas/verReserva/<str:id>', verReserva, name='verReservas'),
    path('reservas/eliminarReserva/<str:id>', eliminarReserva, name='eliminarReserva'),
    path('pedidos/', TomarPedidos, name='pedidos'),
    path('gestionPedidos/', gestionPedidos, name='gestionPedidos'),
    path('gestionConfiguracion/<str:dia>', gestionConfiguracion, name='gestionConfiguracion'),
    path('simulacion/', simulacion, name='simulacion'),
    path('simulacion/lecturaMatricula/<str:io>/<str:mtr>/<str:dia>/<str:hora>', lecturaMatricula, name='lecturaMatricula'),
    path('simulacion/checkSimulacion/<str:io>/<str:mtr>/<str:dia>/<str:hora>', checkSimulacion, name='checkSimulacion'),
    path('estadoVehiculos/', estadoVehiculos, name='estadoVehiculos'),
    path('historicoPedidos/', historicoPedidos, name='historicoPedidos'),
    path('index/', index, name='index')
]