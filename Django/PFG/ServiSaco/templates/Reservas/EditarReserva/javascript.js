$(document).ready(function(){

    mostrarDias();
    mostrarHoras();
    seleccionarDia();

    
    $("#btnAct1").addClass("btnActActive");


    $("#BotonCancelar").on("click", function(){
        window.location.href = "/reservas/_";
    });

    $(document).on("click", "#BotonReservar", function(){
        pedido = $('#numPedido').text();
        fecha = $('.selectorDiaClicked').attr('id');
        idHueco = $('.selectorHoraClicked').attr('id');
    
        if(idHueco == undefined)
            alert('Debe seleccionar una hora para realizar la reserva');
        else
            window.location.href = "/realizarReserva/resumenReserva/" + pedido +  "/" + idHueco;
    });

});

function mostrarDias(){
    var diaSemana = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];

    for (let i = 0; i < dias.length; i++) {
        dia = new Date(dias[i]);
        $("#SelectorDia").append("<span id="+ dias[i] +" class='BotonSelector'>"+diaSemana[dia.getDay()]+" "+(dia.getDate())+"</span>");
    }
}

function mostrarHoras(){

    var izq = "<i id='izq' class='fas fa-chevron-left flecha'></i>";
    var der = "<i id='der' class='fas fa-chevron-right flecha'></i>";
    $("#HoraReserva").append(izq).append(der);

    for (let i = 0; i < horas.length; i++) {
        var horaMinuto = horas[i].split(":");
        hora = horaMinuto[0];
        minuto = horaMinuto[1];
        if(minuto < 10)
            minuto = "0" + minuto;
        $("#SelectorHora").append("<span class='BotonSelector' id="+ idHueco[i] +">"+ hora + ":" + minuto +"</span>");
    }
}

function seleccionarDia(){
    //Seleccionar Día según la URL
    var url = window.location.href;
    var urlParam = url.split('/');
    var dia = urlParam[urlParam.length-1];
    $("#" + dia).addClass('selectorDiaClicked');
}

$(document).on("click", "#SelectorDia span", function(){
    var numPedido = $('#numPedido').text();
    var dia = $(this).attr('id');
    window.location.href = "/reservas/editarReserva/" + numPedido + "/" + dia;
});

$(document).on("click", "#SelectorHora span", function(){
    $(".selectorHoraClicked").toggleClass("selectorHoraClicked");
    $(this).toggleClass("selectorHoraClicked");
});

$(document).on("click", "#der", function(){
    $("#SelectorHora").animate({
        scrollLeft: $("#SelectorHora").scrollLeft()+100
    });
});

$(document).on("click", "#izq", function(){
    $("#SelectorHora").animate({
        scrollLeft: $("#SelectorHora").scrollLeft()-100
    });
});

