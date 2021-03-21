var cantidadVehiculo = 10;
var horaInicio = 6;
var horaFin = 14;

$(document).ready(function(){
    crearTabla();
});

function crearTabla(){

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

    var cbTipoVehiculo = "<select id='ComboBoxTipoVehiculo' class='comboBox'> \
                            <option value='0'>Furgoneta</option> \
                            <option value='1'>Lona</option> \
                            <option value='2'>Trailer</option> \
                        </select>";

    var cbTipoAccion = "<select id='ComboBoxTipoAccion' class='comboBox'> \
                            <option value='0'>CARGA</option> \
                            <option value='1'>DESCARGA</option> \
                            <option value='2'>NO DISPONIBLE</option> \
                        </select>";
    for (let i = 0; i < cantidadVehiculo; i++) {
        var tr = "<tr><td>"+(i+1)+"</td>";
        tr += "<td>"+cbTipoVehiculo+"</td>";
        for (let j = 0; j < horaFin-horaInicio; j++) {
            tr += "<td>"+cbTipoAccion+"</td>";
        }
        tr += "</tr>";
        $("table tbody").append(tr);
    }   
}