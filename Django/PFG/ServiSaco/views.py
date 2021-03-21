from django.http import HttpResponse, request
from django.template import loader
from .models import *
from .forms import PedidosForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json
import pytz
import datetime

es_simulacion = False
fecha_simulacion = datetime.datetime.now(pytz.timezone('Europe/Madrid'))

# -------  Pantalla de Login/Inicio de aplicacion--------------
#--------------------------------------------------------------
@login_required(login_url='/login/')
def home(request):
    docHtml = loader.get_template('Home/home.html')
    doc = docHtml.render({'user' : request.user})
    return HttpResponse(doc)


# ---------------  Pantalla de Pedidos-------------------------
#--------------------------------------------------------------
@login_required(login_url='/login/')
def TomarPedidos(request):
    data={'form':PedidosForm()}
    if request.method=='POST':
        formulario=PedidosForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="Pedido guardado"
        else:
            data["form"]=formulario    
    return render(request,'Pedidos/pedidos.html',data)
# ----------------Pantallas Realizar Reserva-------------------
#--------------------------------------------------------------

@login_required(login_url='/login/')
def realizarReserva(request, numPedido, dia):
    
    # Verificación Rol #
    if request.user.usuario.rol.nombre != 'Transportista':
        return redirect('/home/')

    """
    Hay que comprobar que el nº de pedido existe, si no, hay que volver a la pantalla
    'checkNumPedido' indicando que no existe (pedidoExiste = False)
    True: el pedido sí existe
    False: el pedido no existe
    """
    vehiculo = Vehiculo.objects.get(usuario = request.user.id)
    pedido = Pedido.objects.filter(numero_pedido = numPedido, vehiculo = vehiculo)
    if(len(pedido) == 0):
        pedidoExiste = False # en vez de False, hay que hacer una comprobación a la BBDD, para saber si poner False o True
    else:
        #Comprobar que no tenga una reserva previa
        reservas = Reserva.objects.filter(pedido = numPedido)
        if reservas:
            pedidoExiste = False 
        else:
            pedido = pedido[0]
            pedidoExiste = True

    if not pedidoExiste:
        vehiculo = Vehiculo.objects.get(usuario_id=request.user.id)
        pedidos = Pedido.objects.filter(vehiculo_id=vehiculo.matricula)
        docHtml = loader.get_template('RealizarReserva/CheckNumPedido/checkNumPedido.html')
        doc = docHtml.render({'user' : request.user, 'pedidoExiste' : pedidoExiste, 'matricula' : vehiculo.matricula, 'pedidos' : pedidos})
        return HttpResponse(doc)
    
    docHtml = loader.get_template('RealizarReserva/realizarReserva.html')


    """
        Datos a enviar
    """
    tipo_vehiculo = TipoVehiculo.objects.get(id = vehiculo.tipo_vehiculo.id)
    datos_pedido = [pedido.numero_pedido, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula] 

    dias = []
    fechas = []
    huecos = DisponibilidadReserva.objects.filter(operacion = pedido.operacion, tipo_vehiculo = vehiculo.tipo_vehiculo, estado = "LIBRE")
    fecha_actual = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
    for hueco in huecos:
        fecha = hueco.fecha_inicio
        dia_fecha = fecha.day
        if dia_fecha not in dias and dia_fecha > fecha_actual.day:
            dias.append(dia_fecha)
            fechas.append(str(fecha.year) + "-" + str(fecha.month) + "-" + str(dia_fecha))
    horas = []
    idHueco = []
    huecos_disponibles = pd.DataFrame({"horas" : [], "idHueco" : []})
    
    if dia != "_": 
        for hueco in huecos:
            fecha = str(hueco.fecha_inicio.year) + "-" + str(hueco.fecha_inicio.month) + "-" + str(hueco.fecha_inicio.day)
            hora = hueco.fecha_inicio.time()
            if fecha == dia and hora not in horas:
                horas.append(hora)
                idHueco.append(hueco.id)
        huecos_disponibles = pd.DataFrame({"horas" : horas, "idHueco" : idHueco}).sort_values(by="horas", ascending=True)
        horas = huecos_disponibles["horas"].values
        for i, hueco in enumerate(horas):
            horas[i] = str(horas[i].hour) + ":" + str(horas[i].minute)
        huecos_disponibles["horas"] = horas
    doc = docHtml.render({'user' : request.user, 'pedido' : datos_pedido, 'dias' : fechas, 'horas' : huecos_disponibles["horas"].values.tolist(), 'idHueco' : huecos_disponibles["idHueco"].values.tolist()})

    return HttpResponse(doc)

@login_required(login_url='/login/')
def checkNumPedido(request):

    # Verificación Rol #
    if request.user.usuario.rol.nombre != 'Transportista':
        return redirect('/home/')

    vehiculo = Vehiculo.objects.get(usuario_id=request.user.id)
    pedidos = Pedido.objects.filter(vehiculo_id=vehiculo.matricula)

    docHtml = loader.get_template('RealizarReserva/CheckNumPedido/checkNumPedido.html')
    doc = docHtml.render({'user' : request.user, 'matricula' : vehiculo.matricula, 'pedidos' : pedidos})
    return HttpResponse(doc)


@login_required(login_url='/login/')
@csrf_exempt
def resumenReserva(request, numPedido, idHueco):

    docHtml = loader.get_template('RealizarReserva/ResumenReserva/resumenReserva.html')
    if request.method == "POST":
        
        pedido = Pedido.objects.get(numero_pedido = numPedido)  
        vehiculo = Vehiculo.objects.get(matricula = pedido.vehiculo.matricula)
        reserva = Reserva.objects.filter(pedido = numPedido)
        if(len(reserva) != 0):
            reserva = reserva[0]
            hueco = DisponibilidadReserva.objects.get(id = reserva.disponibilidad_reserva.id)
            hueco.estado = "LIBRE"
            hueco.save()
            reserva.delete()
        
        hueco = DisponibilidadReserva.objects.get(id = idHueco)
        hueco.estado = "RESERVADO"
        hueco.save()
        
        reserva = Reserva.objects.create(pedido = pedido, disponibilidad_reserva = hueco)
        

        
    else:
        pedido = Pedido.objects.get(numero_pedido = numPedido)
        vehiculo = Vehiculo.objects.get(matricula = pedido.vehiculo.matricula)
        tipo_vehiculo = TipoVehiculo.objects.get(id = vehiculo.tipo_vehiculo.id)
        datos_pedido = [pedido.numero_pedido, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula] 

        #Se hace una consulta donde se obtenga el pedido a partir del numPedido  pedido = [pedido.numero_pedido, pedido.operacion, 'Camión', '5243TRG'] 
        hueco = DisponibilidadReserva.objects.get(id = idHueco)
        horaInicio = str(hueco.fecha_inicio.hour) + ":" + str(hueco.fecha_inicio.minute) 
        horaFin = str(hueco.fecha_fin.hour) + ":" + str(hueco.fecha_fin.minute) 

        dia = str(hueco.fecha_inicio.year) + "-"  + str(hueco.fecha_inicio.month) + "-" + str(hueco.fecha_inicio.day)
        vehiculo = hueco.vehiculo.matricula

        doc = docHtml.render({ 'user' : request.user, 'numPedido' : numPedido, 'idHueco' : idHueco ,'pedido' : datos_pedido, 'dia' : dia, 'vehiculo' : vehiculo, 'horaInicio' : horaInicio, 'horaFin' : horaFin})
    return HttpResponse(doc)
#---------------------------------------------------

# ----------  Pantallas Reservas -----------------
#---------------------------------------------------

@login_required(login_url='/login/')
def reservas(request, filtroPedidosDia):
    docHtml = loader.get_template('Reservas/reservas.html')

    reservas = []

    usuarios = [Usuario.objects.get(user = request.user.id)]

    # Verificación Rol #
    if request.user.usuario.rol.nombre != 'Transportista':
        usuarios = Usuario.objects.filter(rol__nombre = "Transportista")

    for usuario in usuarios: 
        vehiculo = Vehiculo.objects.get(usuario = usuario)
        pedidos = Pedido.objects.filter(vehiculo = vehiculo)
        for pedido in pedidos:
            
            reserva = Reserva.objects.filter(pedido = pedido.numero_pedido)
            if(len(reserva) > 0):
                reserva = reserva[0]
                vehiculo = reserva.disponibilidad_reserva.vehiculo
                fecha_inicio = reserva.disponibilidad_reserva.fecha_inicio
                fecha_fin = reserva.disponibilidad_reserva.fecha_fin
                if filtroPedidosDia == "_" or datetime.datetime.now(pytz.timezone('Europe/Madrid')).date() == fecha_inicio.date():
                    reservas.append([pedido.numero_pedido, vehiculo.matricula, pedido.operacion, vehiculo.tipo_vehiculo.nombre, vehiculo.matricula, fecha_inicio.date, fecha_inicio.time, fecha_fin.time])
            
    data = {'user' : request.user, 'reservas' : reservas}
    doc = docHtml.render(data)
    return HttpResponse(doc)

@login_required(login_url='/login/')
def editarReserva(request, id, dia):
    docHtml = loader.get_template('Reservas/EditarReserva/editarReserva.html')

    pedido = Pedido.objects.get(numero_pedido = id)
    vehiculo = Vehiculo.objects.get(matricula = pedido.vehiculo)
    tipo_vehiculo = TipoVehiculo.objects.get(id = vehiculo.tipo_vehiculo.id)
    datos_pedido = [pedido.numero_pedido, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula] 

    dias = []
    fechas = []
    huecos = DisponibilidadReserva.objects.filter(operacion = pedido.operacion, tipo_vehiculo = vehiculo.tipo_vehiculo, estado = "LIBRE")
    #primero se devuelven los dias

    for hueco in huecos:
        fecha = hueco.fecha_inicio
        dia_fecha = fecha.day
        if dia_fecha not in dias:
            dias.append(dia_fecha)
            fechas.append(str(fecha.year) + "-" + str(fecha.month) + "-" + str(dia_fecha))
    horas = []
    idHueco = []
    if dia != "_": 
        for hueco in huecos:
            fecha = str(hueco.fecha_inicio.year) + "-" + str(hueco.fecha_inicio.month) + "-" + str(hueco.fecha_inicio.day)
            hora = str(hueco.fecha_inicio.hour) + ":" + str(hueco.fecha_inicio.minute)
            if fecha == dia and hora not in horas:
                horas.append(hora)
                idHueco.append(hueco.id)

    doc = docHtml.render({'user' : request.user, 'pedido' : datos_pedido, 'dias' : fechas, 'horas' : horas, 'idHueco' : idHueco})
    # la vista 'realizarReserva'
    return HttpResponse(doc)


@login_required(login_url='/login/')
def guardarReserva(request, numPedido, idHueco):
    #Aqui se guarda la reserva
    docHtml = loader.get_template('Home/home.html')
    #No se si se puede hacer asi. Mostrar la vista reservas
    pedido = Pedido.objects.get(numero_pedido = numPedido)
    hueco = DisponibilidadReserva.objects.get(id = idHueco)
    hueco.estado = "RESERVADO"
    hueco.save()
    reserva = Reserva.objects.create(pedido = pedido, disponibilidad_reserva = hueco)
    doc = docHtml.render({'user' : request.user})
    return HttpResponse(doc)

@login_required(login_url='/login/')
def verReserva(request, id):
    reserva = Reserva.objects.get(pedido=id)
    docHtml = loader.get_template('Reservas/VerReserva/verReserva.html')
    doc = docHtml.render({'user' : request.user, 'reserva' : reserva})
    return HttpResponse(doc)

@login_required(login_url='/login/')
def eliminarReserva(request, id):
    # Proceso de eliminar en base al 'id'
    pedido = Pedido.objects.get(numero_pedido = id)
    reserva = Reserva.objects.get(pedido = pedido)
    hueco = DisponibilidadReserva.objects.get(id = reserva.disponibilidad_reserva.id)
    hueco.estado = "LIBRE"
    hueco.save()
    reserva.delete()
    return redirect('/reservas/_')

#---------------------------------------------------

# ----------  Pantallas Gestión Pedidos/Configuracion ----------
#---------------------------------------------------------------

@login_required(login_url='/login/')
@csrf_exempt
def gestionPedidos(request):

    # Verificación Rol #
    if request.user.usuario.rol.nombre != 'Administrador':
        return redirect('/home/')

    # Si se actualizan los Pedidos
    if request.method == 'POST':
        pedidos = json.loads(request.POST['contenido'])

        listaPedidos = []

        for pedido in pedidos:
            filaPedido = []
            for item in pedidos[pedido]:
                valor = pedidos[pedido][item]
                filaPedido.append(valor)  
            listaPedidos.append(filaPedido)
        Pedido.objects.all().delete()
        for pedido in listaPedidos:
            vehiculo = Vehiculo.objects.filter(matricula = pedido[3])
            if(len(vehiculo) == 0):
                tipo_vehiculo = TipoVehiculo.objects.filter(nombre = pedido[2].upper())[0]

                vehiculo = Vehiculo.objects.update(tipo_vehiculo = tipo_vehiculo, matricula = pedido[3])
                
            else:
                vehiculo = vehiculo[0]
            pedido_historico = PedidoCompletado.objects.filter(numero_pedido = pedido[0])
            if(len(Pedido.objects.filter(numero_pedido = pedido[0])) == 0 and len(pedido_historico) == 0):
                pedido_creado = Pedido.objects.create(operacion = pedido[1].upper(), numero_pedido = pedido[0], vehiculo = vehiculo)
        
      


    docHtml = loader.get_template('GestionPedidos/gestionPedidos.html')

    usuarios = Usuario.objects.get(user = request.user.id)
    if(usuarios.rol.nombre == "Transportista"):
        redirect("/home/")
    
    consulta_pedidos = Pedido.objects.all() 
    pedidos = []
    for pedido in consulta_pedidos:
        vehiculo = Vehiculo.objects.get(matricula = pedido.vehiculo.matricula)
        pedidos.append([pedido.numero_pedido, pedido.operacion, vehiculo.tipo_vehiculo.nombre, vehiculo.matricula])
   
    data = {'user' : request.user, 'pedidos' : pedidos}

    doc = docHtml.render(data)
    return HttpResponse(doc)



@login_required(login_url='/login/')
@csrf_exempt
def gestionConfiguracion(request, dia):

    # Verificación Rol #
    if request.user.usuario.rol.nombre != 'Administrador':
        return redirect('/home/')

    
    # Si se actualizan la Gestión de Configuración
    if request.method == 'POST':
        conf = json.loads(request.POST['configuracion'])

        listaConfiguracion = []

        for c in conf:
            filaPedido = []
            for item in conf[c]:
                valor = conf[c][item]
                filaPedido.append(valor)
            
            listaConfiguracion.append(filaPedido)
        
        info_dia = dia.split("-")

        fecha_configuracion = datetime.datetime(year=int(info_dia[0]), month=int(info_dia[1]), day=int(info_dia[2]))
        configuraciones = ConfiguracionVehiculo.objects.all()       
        for configuracion in configuraciones:
            if(configuracion.fecha.date() < datetime.datetime.now(pytz.timezone('Europe/Madrid')).date() or configuracion.fecha.date() == fecha_configuracion.date()):
                configuracion.delete()
        
        huecos = DisponibilidadReserva.objects.all()       
        for hueco in huecos:
            if(hueco.fecha_inicio.date() < datetime.datetime.now(pytz.timezone('Europe/Madrid')).date() or hueco.fecha_inicio.date() == fecha_configuracion.date()):
                
                if(hueco.estado == "RESERVADO"):
                    reserva = Reserva.objects.get(disponibilidad_reserva = hueco.id)
                    pedido = Pedido.objects.get(numero_pedido = reserva.numero_pedido)
                    vehiculo = Vehiculo.objects.get(matricula = pedido.matricula)
                    usuario = Usuario.objects.get(user = vehiculo.usuario)
                    pedido_completado = PedidoCompletado.objects.create(
                        numero_pedido = pedido.numero_pedido,
                        operacion = pedido.operacion,
                        fecha_inicio = datetime.datetime.now(pytz.timezone('Europe/Madrid')),
                        fecha_fin = datetime.datetime.now(pytz.timezone('Europe/Madrid')),
                        usuario = usuario,
                        vehiculo = vehiculo,
                        resultado = "AUSENTE"
                        )
                    pedido.delete()
                hueco.delete()

        for configuracion in listaConfiguracion:
            hora_inicio = fecha_configuracion
            
            vehiculo = Vehiculo.objects.filter(matricula = configuracion[0])
            if(len(vehiculo) == 0):
                vehiculo = Vehiculo.objects.update_or_create(matricula = configuracion[0], estado = "LIBRE")              
            else:
                vehiculo = vehiculo[0]
            
            tipo_vehiculo = TipoVehiculo.objects.get(matricula = configuracion[1])
            tiempo_carga = datetime.timedelta(minutes = tipo_vehiculo.tiempo_carga)
            tiempo_descarga = datetime.timedelta(minutes = tipo_vehiculo.tiempo_descarga)
            i = 2
            fecha_inicio = fecha_configuracion.replace(hour=6)
        
            while(i < 10):
                operacion = configuracion[i].upper()
                configuracion_nueva = ConfiguracionVehiculo.objects.create(operacion = operacion, fecha = fecha_inicio, vehiculo = vehiculo, tipo_vehiculo = tipo_vehiculo)
                
                fecha_inicio = fecha_inicio + datetime.timedelta(hours = 1)
                i+=1
            i = 2
            fecha_inicio = fecha_configuracion.replace(hour=6)
            while(i < 10):
                operacion = configuracion[i].upper()
                fecha_siguiente_configuracion = fecha_inicio + datetime.timedelta(hours = 1)
                if operacion == "CARGA" or operacion == "DESCARGA":

                    if operacion == "CARGA":
                        tiempo_operacion = tiempo_carga
                    else:
                        tiempo_operacion = tiempo_descarga
                    
                    while(fecha_inicio + tiempo_operacion <= fecha_siguiente_configuracion):
                        fecha_fin = fecha_inicio + tiempo_operacion
                        disponibilidad_nueva = DisponibilidadReserva.objects.create(operacion = operacion, fecha_inicio = fecha_inicio, fecha_fin = fecha_fin, estado = "LIBRE", vehiculo = vehiculo, tipo_vehiculo = tipo_vehiculo)
                        fecha_inicio = fecha_fin

                        if(fecha_inicio + tiempo_operacion > fecha_siguiente_configuracion and i+1 < 10):
                            if(configuracion[i+1] == configuracion[i]):
                                fecha_siguiente_configuracion = fecha_siguiente_configuracion + datetime.timedelta(hours = 1)
                                i+=1
                    i+=1
                    fecha_inicio = fecha_siguiente_configuracion
                else:
                    i+=1
                    fecha_inicio = fecha_siguiente_configuracion
        """
        SI LA CONFIGURACION ES DEL TIPO '[[]]', es porque no se ha cargado ninguna configuración,
        por lo que simplemente no guardar nada.
        """



    configuraciones = ConfiguracionVehiculo.objects.all()
    diasConConfiguracion = []
    dias = []
    fecha_actual = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
    for configuracion in configuraciones:
        fecha = configuracion.fecha
        dia_fecha = fecha.day
        if dia_fecha not in dias:
            dias.append(dia_fecha)
            diasConConfiguracion.append(str(fecha.year) + "-" + str(fecha.month) + "-" + str(dia_fecha))
    
    horas = []
    datos_configuracion = []
    if dia != '_':
        fecha_consulta = "_"
        configuraciones = ConfiguracionVehiculo.objects.all()
        for configuracion in configuraciones:
            fecha = str(configuracion.fecha.year) + "-" + str(configuracion.fecha.month) + "-" + str(configuracion.fecha.day)
            if(fecha == dia):
                fecha_consulta = configuracion.fecha.date()
        # Consulta de la configuración del día recibido por parámetro:
        if(fecha_consulta != "_"):
            vehiculos = Vehiculo.objects.all()
        
            for vehiculo in vehiculos:
                existe = ConfiguracionVehiculo.objects.filter(vehiculo= vehiculo, fecha__date = fecha_consulta)
                if len(existe) > 0:
                    configuraciones_vehiculo = []
                    configuraciones_vehiculo.append(vehiculo.matricula)
                    consulta_configuraciones = ConfiguracionVehiculo.objects.filter(vehiculo= vehiculo.matricula)
                    configuraciones = []
                    
                    for consulta in consulta_configuraciones:
                        if consulta.fecha.date() == fecha_consulta:
                            configuraciones.append(consulta)
                            tipo = consulta.tipo_vehiculo.nombre
                    configuraciones_vehiculo.append(tipo)
                    for configuracion in configuraciones:
                        
                        configuraciones_vehiculo.append(configuracion.operacion)
                    datos_configuracion.append(configuraciones_vehiculo)
    else:
        configuracion = ['_']

    docHtml = loader.get_template('GestionConfiguracion/gestionConfiguracion.html')
    doc = docHtml.render({'user' : request.user, 'configuracion' : datos_configuracion,'diasConConfiguracion' : diasConConfiguracion})
    return HttpResponse(doc)

@login_required(login_url='/login/')
def ActualizarConfiguracion(request):
    return 0

# ----------  Pantallas Simulación -----------------
#---------------------------------------------------

@login_required(login_url='/login/')
def simulacion(request):

    # Verificación Rol #
    if request.user.usuario.rol.nombre == 'Transportista':
        return redirect('/home/')

    docHtml = loader.get_template('Simulacion/simulacion.html')
    doc = docHtml.render({'user' : request.user})
    return HttpResponse(doc)

@login_required(login_url='/login/')
def lecturaMatricula(request, io, mtr, dia, hora):

    # Verificación Rol #
    if request.user.usuario.rol.nombre == 'Transportista':
        return redirect('/home/')

    docHtml = loader.get_template('Simulacion/LecturaMatricula/lecturaMatricula.html')
    doc = docHtml.render({'user' : request.user, 'mtr' : mtr, 'io' : io})
    return HttpResponse(doc)

@login_required(login_url='/login/')
def checkSimulacion(request, io, mtr, dia, hora):
    global es_simulacion
    global fecha_simulacion
    # Verificación Rol #
    if request.user.usuario.rol.nombre == 'Transportista':
        return redirect('/home/')

    '''
        Caso Entrada:
            Caso 1: Llegando a tiempo con Reserva (considerar que hay un margen de 10min)
            Caso 2: Llegada tarde (perdió la reserva)
            Caso 3: Tiene Reserva, pero más adelante
            Caso 4: No existen reservas para la matrícula
 
        Caso Salida:
            Caso 0: Gestionar la salida del recinto y poner la reserva como completada
    '''
    docHtml = loader.get_template('Simulacion/simulacion.html')
    
    fecha_consulta = dia.split("-")
    hora_consulta = hora.split(":")
    fecha = datetime.datetime(year = int(fecha_consulta[0]), month = int(fecha_consulta[1]), day = int(fecha_consulta[2]), hour = int(hora_consulta[0]), minute = int(hora_consulta[1]))
    vehiculo = Vehiculo.objects.filter(matricula = mtr)
    caso = 4
    reserva_sim = ["-", "-", "-", "-", mtr, fecha.date, "-", "-"]

    if(len(vehiculo) != 0):
        vehiculo = vehiculo[0]

        usuario = Usuario.objects.get(user = vehiculo.usuario)
        pedidos = Pedido.objects.filter(vehiculo= vehiculo)
        
        reservas = []
        for pedido in pedidos:
            reserva = Reserva.objects.filter(pedido = pedido.numero_pedido)
            if(reserva):
                reservas.append(reserva[0])
        '''
            HOLA EQUIPO
            Aquí se hace la consulta y se pasa el resultado por contexto
            Las variables de entrada son: (mtr - matrícula) (io - hace referencia a si es una entrada o una salida de vehículo) 
            Sustituir las dos variables de abajo por las reales y ya estaría todo
        '''
        if(len(reservas) == 0):
                caso = 4
        elif io == 'salida':
            
            for reserva in reservas:
                hueco_reserva = DisponibilidadReserva.objects.get(id = reserva.disponibilidad_reserva.id)
                tipo_vehiculo = TipoVehiculo.objects.get(id = vehiculo.tipo_vehiculo.id)
                if hueco_reserva.estado == "EJECUCION":
                    pedido = Pedido.objects.get(numero_pedido = reserva.pedido.numero_pedido)
                    vehiculo = Vehiculo.objects.get(id = hueco_reserva.vehiculo.matricula)
                    usuario = Usuario.objects.get(user = vehiculo.usuario)
                    vehiculo.estado = "LIBRE"
                    vehiculo.save()
                    pedido_completado = PedidoCompletado.objects.create(
                        numero_pedido = pedido.numero_pedido,
                        operacion = pedido.operacion,
                        fecha_inicio = hueco_reserva.fecha_inicio,
                        fecha_fin = fecha,
                        usuario = usuario,
                        vehiculo = vehiculo,
                        resultado = "COMPLETADO"
                    )
                    reserva_sim = [pedido.numero_pedido, vehiculo.matricula, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula, fecha.date, hueco_reserva.fecha_inicio.time, fecha.time]
                    pedido.delete()
                    reserva.delete()
                    hueco_reserva.delete()
                    fecha_simulacion = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
                    es_simulacion = False
            caso = 0  # Hacer la consulta teniendo en cuenta que es una salida
        else:
            realizado = False
            for reserva in reservas:
                hueco_reserva = DisponibilidadReserva.objects.get(id = reserva.disponibilidad_reserva.id)
                pedido = Pedido.objects.get(numero_pedido = reserva.pedido.numero_pedido)
                vehiculo = Vehiculo.objects.get(id = hueco_reserva.vehiculo.matricula)
                usuario = Usuario.objects.get(user = vehiculo.usuario)
                tipo_vehiculo = TipoVehiculo.objects.get(id = vehiculo.tipo_vehiculo.id)
                fecha_inicio = hueco_reserva.fecha_inicio
                fecha_inicio = datetime.timedelta(days = fecha_inicio.day, hours = fecha_inicio.hour, minutes= fecha_inicio.minute).total_seconds() / 60
                fecha_dif = datetime.timedelta(days = fecha.day, hours = fecha.hour, minutes = fecha.minute).total_seconds() / 60
                diferencia = fecha_inicio - fecha_dif
                
                if (diferencia > 10 and realizado == False):
                    caso = 3
                    reserva_sim = [pedido.numero_pedido, vehiculo.matricula, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula, hueco_reserva.fecha_inicio.date, hueco_reserva.fecha_inicio.time, hueco_reserva.fecha_fin.time]
                    
                elif (abs(diferencia) <= 10 and realizado == False):
                    caso = 1
                    vehiculo.estado = pedido.operacion
                    hueco_reserva.estado = "EJECUCION"
                    hueco_reserva.save()
                    vehiculo.save()
                    reserva_sim = [pedido.numero_pedido, vehiculo.matricula, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula, hueco_reserva.fecha_inicio.date, hueco_reserva.fecha_inicio.time, hueco_reserva.fecha_fin.time]
                    fecha_simulacion = fecha
                    es_simulacion = True
                    realizado = True
                elif (diferencia < -10 and realizado == False):
                    #Se elimina la reserva
                    reserva_sim = [pedido.numero_pedido, vehiculo.matricula, pedido.operacion, tipo_vehiculo.nombre, vehiculo.matricula, hueco_reserva.fecha_inicio.date, hueco_reserva.fecha_inicio.time, hueco_reserva.fecha_fin.time]
                    pedido_completado = PedidoCompletado.objects.create(
                    numero_pedido = pedido.numero_pedido,
                    operacion = pedido.operacion,
                    fecha_inicio = hueco_reserva.fecha_inicio,
                    fecha_fin = fecha,
                    usuario = usuario,
                    vehiculo = vehiculo,
                    resultado = "AUSENTE"
                    )
                    pedido.delete()
                    reserva.delete()
                    hueco_reserva.delete()
                    
             
                    caso = 2

    docHtml = loader.get_template('Simulacion/CheckSimulacion/checkSimulacion.html')
    doc = docHtml.render({'user' : request.user, 'caso' : caso, 'reserva' : reserva_sim, 'horaActual' : hora})
    return HttpResponse(doc)
#---------------------------------------------------

@login_required(login_url='/login/')
def estadoVehiculos(request):

    global es_simulacion
    global fecha_simulacion
    # Verificación Rol #
    if request.user.usuario.rol.nombre == 'Transportista':
        return redirect('/home/')
    fecha_actual = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
    if es_simulacion:
        fecha_actual = fecha_simulacion
    docHtml = loader.get_template('EstadoVehiculos/estadoVehiculos.html')
    vehiculos = Vehiculo.objects.all()
    datos_vehiculos = []
    for vehiculo in vehiculos:
        if vehiculo.estado != "LIBRE":
            hueco = DisponibilidadReserva.objects.get(vehiculo = vehiculo.matricula, estado = "EJECUCION")
            reserva = Reserva.objects.get(disponibilidad_reserva = hueco.id)
            vehiculo = Vehiculo.objects.get(matricula = reserva.pedido.vehiculo)
            datos_vehiculos.append([vehiculo.matricula, vehiculo.tipo_vehiculo.nombre, vehiculo.matricula, vehiculo.estado])
        else:
            hueco = DisponibilidadReserva.objects.filter(fecha_inicio__hour = fecha_actual.hour, vehiculo = vehiculo)
            if hueco:
                datos_vehiculos.append([vehiculo.matricula, vehiculo.tipo_vehiculo.nombre, vehiculo.estado])
            else:
                datos_vehiculos.append([vehiculo.matricula, vehiculo.tipo_vehiculo.nombre, "NO DISPONIBLE"])

    data = {'user' : request.user, 'vehiculos' : datos_vehiculos, "hora" : fecha_actual.time()}
    doc = docHtml.render(data)
    return HttpResponse(doc)

@login_required(login_url='/login/')
def historicoPedidos(request):

    # Verificación Rol #
    if request.user.usuario.rol.nombre == 'Transportista':
        return redirect('/home/')

    docHtml = loader.get_template('HistoricoPedidos/historicoPedidos.html')
    
    historico_pedidos = PedidoCompletado.objects.all()
    historico = []
    for pedido in historico_pedidos:
        vehiculo = Vehiculo.objects.get(matricula = pedido.vehiculo)
        tipo_vehiculo = TipoVehiculo.objects.get(id = vehiculo.tipo_vehiculo.id)
        historico.append([pedido.numero_pedido, tipo_vehiculo.nombre, vehiculo.matricula, pedido.operacion, pedido.fecha_inicio.time, pedido.fecha_fin.time, pedido.resultado])
    
   
    data = {'user' : request.user, 'historico' : historico}
    doc = docHtml.render(data)
    return HttpResponse(doc)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")