from django.forms import fields
from .models import Pedido, Vehiculo
from django import forms
from django import forms


class PedidosForm(forms.ModelForm):
    class Meta:
        model=Pedido
        fields=["numero_pedido"
        ,"nombre"
        ,"direccion",
        "vehiculo",
        "operacion",
        "peso"]