$(document).ready(function(){
    activo = {
        "Realizar Reserva":"reservar", // 0
        "Reservas":"reservas", // 1
        "Gestión de Configuración":"gestionConf", // 2
        "Gestión de Pedidos":"gestionPedidos", // 3
        "Estado de los Vehiculo":"estadoVehiculos", // 4
        "Histórico de Pedidos":"historicoPedidos", // 5
        "Simulación":"simular", // 6
    };
    tituloPag = $("title").text();
    
    $("#"+activo[tituloPag]).addClass("btnActActive");

    $("#reservas").on("click", function(){
        window.location.href = "/reservas/" + "_";
    });

    $("#gestionConf").on("click", function(){
        window.location.href = "/gestionConfiguracion/" + "_";
    });

    
});