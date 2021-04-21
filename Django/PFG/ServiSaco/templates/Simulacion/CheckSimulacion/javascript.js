$(document).ready(function(){

    if (caso == 1){
        setTimeout(function(){
            $("#InfoReserva h3").text("Cerrando barrera");
            $("#AnimacionBarrera").attr("src", "/static/Simulacion/CheckSimulacion/media/camioncamino.gif");
        }, 6000);

        setTimeout(function(){
            var nombreAnimacion = $('#TipoOperacion span').text().toLowerCase();
            $('#ContenedorCheckSimulacion').remove();
            var animacion = "<img id ='furgo' src='/static/Simulacion/CheckSimulacion/media/" + nombreAnimacion + ".gif'>";
            $('#ContenedorContenido').append(animacion);
        }, 10000);
    
        setTimeout(function(){
            alert('El vehículo está dentro del recinto');
            window.location.href = "/home/";
        }, 15000);

    }else if (caso == 0){

        setTimeout(function(){
            $("#InfoReserva h3").text("Cerrando barrera");
            $("#AnimacionBarrera").attr("src", "/static/Simulacion/CheckSimulacion/media/camioncamino.gif");
        }, 6000);
    
        setTimeout(function(){
            alert('El vehículo está fuera del recinto');
            window.location.href = "/home/";
        }, 10000);

    }
    
});
