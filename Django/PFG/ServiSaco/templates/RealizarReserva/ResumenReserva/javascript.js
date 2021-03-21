$(document).ready(function(){
    var horaMinuto = $("#DatoPeriodoReserva").text().split("-");

    var horaMinuto1 = horaMinuto[0].split(":");
    if(horaMinuto1[1] < 10)
        horaMinuto1[1] = "0" + horaMinuto1[1];

    var horaMinuto2 = horaMinuto[1].split(":");
    if(horaMinuto2[1] < 10)
        horaMinuto2[1] = "0" + horaMinuto2[1];

    $("#DatoPeriodoReserva").text(horaMinuto1[0] + ":" + horaMinuto1[1] + " - " + horaMinuto2[0] + ":" + horaMinuto2[1]);

});

$(document).on("click", "#BotonVolver", function(){
    pedido = $('#NumeroPedidoVal').text();
    dia = $('#DatoDiaReserva').text();
    window.location.href = "/realizarReserva/" + pedido + "/" + dia;
});

$(document).on("click", "#BotonConfirmar", function(){
    $.post("/realizarReserva/resumenReserva/" + numPedido + "/" + idHueco, "");
    alert("Se ha creado la reserva para el pedido: " + numPedido);
    window.location.href = "/reservas/_";
});
