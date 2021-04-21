var horaInicio = 6;
var horaFin = 14;

diasNoLaborables = ['2021-01-01', '2021-01-06', '2021-04-10', '2021-05-01', '2021-08-15', '2021-10-12', '2021-11-02', '2021-12-07', '2021-12-08', '2021-12-25']

$(document).ready(function(){
    mostrarDias();
    seleccionarDia();

    $("#BtnActualizar").on("click", function () {
        var configuracion = getTableContent();
        var dia = getDiaURL();
        $.post('/gestionConfiguracion/' + dia, configuracion);
        alert("Se ha actualizado la configuración")
        window.location.href = "/gestionConfiguracion/_";
    });
});

function getTableContent() {
    var contenido = {};
    var tbody = $("tbody").children();

    for (let i = 0; i < tbody.length; i++) {
        var fila = $(tbody[i]).children();
        var contenidoFila = {};

        for (let j = 0; j < fila.length; j++) {
            if(j < 1)
                var celda = $(fila[j]).text();
            else{
                var celda = $(fila[j]).children()[0];
                celda = $(celda).val();
            }
                
            contenidoFila['celda'+j] = celda;
        }

        contenido['fila'+i] = contenidoFila;
    }

    return {"configuracion" : JSON.stringify(contenido)};
}

function getDiaURL(){
    url = window.location.href;
    url = url.split('/');
    dia = url[url.length-1];
    return dia;
}

function seleccionarDia(){
    dia = getDiaURL();
    if (dia != '_'){
        $('#'+dia).addClass('selectorDiaClicked');
        $('#MensajeSeleccionarDia').remove();

        //Inicializar Contenedor
        inicializarContenedorCalendario();

        //Mostar Tabla correspondiente
        crearTabla(configuracion);

        //Evento cargar fichero
        document.getElementById('CargarConfiguracion').addEventListener('change', readSingleFile, false);
    } 
}

function getSiguienteDiaValido(d){

    do {
        d.setDate(d.getDate()+1);
    } while (!esLaborable(d));

    return d;
}

function esLaborable(d){
    //Comprueba que no es finde
    if(d.getDay() == 0 || d.getDay() == 6)
        return false;
    
    //Comprobación Festivos
    dia = diaACadena(d);
    for (let i = 0; i < diasNoLaborables.length; i++){
        if(dia == diasNoLaborables[i])
            return false;
    }
    
    return true;
}

function diaACadena(d){

    cadena = d.getFullYear()+'-';
    mes = d.getMonth()+1;
    dia = d.getDate();

    if(mes < 10)
        mes = '0' + mes;
    if(dia < 10)
        dia = '0' + dia;

    cadena += mes + '-' + dia;
    return cadena;
}

function mostrarDias(){
    var diaSemana = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];
    var dia;

    cantdiasConConfiguracion = diasConConfiguracion.length;
    cantdiasSinConfiguracion = 5 - cantdiasConConfiguracion;
    
    //Generación Fechas Días con Configuración
    for (let i = 0; i < cantdiasConConfiguracion; i++) {
        dia = new Date(diasConConfiguracion[i]);
        $("#DiasConConf").append("<span id="+ diasConConfiguracion[i] +" class='BotonSelector'>"+diaSemana[dia.getDay()]+" "+(dia.getDate())+"</span>");
    }

    //Generación Fechas Días sin Configuración
    if(cantdiasConConfiguracion){
        for (let i = 0; i < cantdiasSinConfiguracion; i++) {
            dia = getSiguienteDiaValido(dia);
            
            if(i > 0)
                $("#DiasSinConf").append("<span id="+ diaACadena(dia) +" class='BotonSelectorDisabled'>"+diaSemana[dia.getDay()]+" "+(dia.getDate())+"</span>");
            else
                $("#DiasSinConf").append("<span id="+ diaACadena(dia) +" class='BotonSelector'>"+diaSemana[dia.getDay()]+" "+(dia.getDate())+"</span>");
        }
    }
    else{
        dia = getSiguienteDiaValido(new Date());
        for (let i = 0; i < 5; i++) {
            if(i > 0){
                dia = getSiguienteDiaValido(dia);
                $("#DiasSinConf").append("<span id="+ diaACadena(dia) +" class='BotonSelectorDisabled'>"+diaSemana[dia.getDay()]+" "+(dia.getDate())+"</span>");
            }
            else
                $("#DiasSinConf").append("<span id="+ diaACadena(dia) +" class='BotonSelector'>"+diaSemana[dia.getDay()]+" "+(dia.getDate())+"</span>");
        }
    }

}

function createSelectedTipo(tipo){
    var cbTipoVehiculo = "<select id='ComboBoxTipoVehiculo' class='comboBox'>";
    if(tipo.toLowerCase() == "furgoneta")
        cbTipoVehiculo += "<option value='FURGONETA' selected>FURGONETA</option>";
    else
        cbTipoVehiculo += "<option value='FURGONETA'>FURGONETA</option>";
    if(tipo.toLowerCase() == "lona")
        cbTipoVehiculo += "<option value='LONA' selected>LONA</option>";
    else
        cbTipoVehiculo += "<option value='LONA'>LONA</option>";
    if(tipo.toLowerCase() == "trailer")
        cbTipoVehiculo += "<option value='TRAILER' selected>TRAILER</option>";
    else
        cbTipoVehiculo += "<option value='TRAILER'>TRAILER</option>";
    cbTipoVehiculo += "</select>";

    return cbTipoVehiculo;
}

function createSelectedAccion(accion){
    var cbTipoAccion = "<select id='ComboBoxTipoAccion' class='comboBox'> \
                            <option value='CARGA'>CARGA</option> \
                            <option value='DESCARGA'>DESCARGA</option> \
                            <option value='NO DISPONIBLE'>NO DISPONIBLE</option> \
                        </select>";

    var cbTipoAccion = "<select id='ComboBoxTipoVehiculo' class='comboBox'>";
    if(accion.toLowerCase() == "carga")
        cbTipoAccion += "<option value='CARGA' selected>CARGA</option>";
    else
        cbTipoAccion += "<option value='CARGA'>CARGA</option>";
    if(accion.toLowerCase() == "descarga")
        cbTipoAccion += "<option value='DESCARGA' selected>DESCARGA</option>";
    else
        cbTipoAccion += "<option value='DESCARGA'>DESCARGA</option>";
    if(accion.toLowerCase() == "no disponible")
        cbTipoAccion += "<option value='NO DISPONIBLE' selected>NO DISPONIBLE</option>";
    else
        cbTipoAccion += "<option value='NO DISPONIBLE'>NO DISPONIBLE</option>";
    cbTipoAccion += "</select>";

    return cbTipoAccion;
}

function readSingleFile(evt) {
    var f = evt.target.files[0]; 

    if (f) {
      var r = new FileReader();
      r.onload = function(e) { 
        var contenido = e.target.result;
        contenido = contenido.split('\n');
        modifyContent(contenido);
      }
      r.readAsText(f);
      $("#Configuracion").css("height","220px");
    } 
    else { 
      alert("No se ha podido leer el fichero");
    }
  }

  function modifyContent(c){

    $("table tbody").empty();

    for(let i = 1; i < c.length-1; i++){

        var contenido = c[i].split(';');

        var cantidadColumnas = contenido.length;
        
        for (let j = 0; j < cantidadColumnas; j++) {
            if(j == 0){
                var tr = "<tr><td>"+ contenido[j] +"</td>";
            }
            else if(j == 1){
                tr += "<td>"+ createSelectedTipo(contenido[j]) +"</td>";
            }
            else{
                tr += "<td>"+ createSelectedAccion(contenido[j]) +"</td>";
            }
        }

        tr += "</tr>";
        $("table tbody").append(tr);
    }
}

$(document).on("click", ".BotonSelector", function(){
    $(".selectorDiaClicked").toggleClass("selectorDiaClicked");
    $(this).toggleClass("selectorDiaClicked");
    
    dia = $(this).attr('id');

    window.location.href = '/gestionConfiguracion/'+dia;
});

$(document).on("click", ".BotonSelectorDisabled", function(){
    alert("Antes de configurar este día tiene que configurar los anteriores.");
});

function crearTabla(contenido){

    var tabla = "<table><thead><tr></tr></thead><tbody></tbody></table>";
    $('#CalendarioConfiguracion').append(tabla);

    for (let i = horaInicio; i < horaFin; i++) {
        
        if( i == horaInicio){
            var elem = "<th>Vehiculo</th>";
            $("table thead tr").append(elem);
            var elem = "<th>Tipo</th>";
            $("table thead tr").append(elem);
        }
        
        var elem = "<th>" + i + ":00-" + (i+1) + ":00</th>";
        $("table thead tr").append(elem);
    }

    var tr;

    if(!contenido.length){
        tr = "<tr><td colspan='10'>No se ha cargado ninguna configuración</td></tr>";
    }
    else{
        for (let i = 0; i < contenido.length; i++){

            for (let j = 0; j < contenido[i].length; j++){

                if(j == 0){
                    tr += "<tr><td>"+ contenido[i][j] +"</td>";
                }
                else if(j == 1){
                    tr += "<td>"+ createSelectedTipo(contenido[i][j]) +"</td>";
                }
                else{
                    tr += "<td>"+ createSelectedAccion(contenido[i][j]) +"</td>";
                }
            }
            tr += '</tr>';
        }
        $("#Configuracion").css("height","220px");
    }

    $("table tbody").append(tr);
}

function inicializarContenedorCalendario(){

    contenedor =    '<div id="Configuracion">\
                        <div id="ContenedorCalendarioConfiguracion">\
                            <div id="CalendarioConfiguracion">\
                            </div>\
                        </div>\
                    </div>';

    botones =       '<label id="CargarConfiguracionLabel" for="CargarConfiguracion">Cargar configuración</label>\
                    <input type="file" id="CargarConfiguracion"/>\
                    <div id="ContenedorBtnActualizar">\
                        <a id="BtnActualizar">Actualizar configuración</a>\
                    </div>';
    
    $('#ContenedorConfiguracion').append(contenedor).append(botones);
}
