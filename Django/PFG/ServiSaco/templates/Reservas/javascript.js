var popUp = "<div id='PopUpContainer'> \
                <div id='PopUp'> \
                    <h3>¿Seguro que desea eliminar la reserva con id '<span></span>' ?</h3> \
                    <div id='PopUpBtns'> \
                        <a id='PopUpSi'>Sí</a> \
                        <a id='PopUpNo'>No</a> \
                    </div \
                </div> \
            </div>";

var id = '';

$(document).ready(function(){

    $("body").append(popUp);
    $("#PopUpContainer").hide();

    //Marcar Checkbox
    var url = window.location.href;
    var urlParam = url.split('/');
    var filter = urlParam[urlParam.length-1];
    checkBox = $('#PedidosDia input')[0];

    if(filter == "_")
        checkBox.checked = false;
    else
        checkBox.checked = true;


    $("#PopUpNo").on("click", function(){
        $("#PopUpContainer").fadeOut("fast");
    });

    $("#PopUpSi").on("click", function(){
        $("#PopUpContainer").fadeOut("fast");
        window.location.href = "/reservas/eliminarReserva/" + id;
    });

    $(".verReservaLink").on("click", function(){
        id = $(this).parent().parent().children()[0];
        id = $(id).text().trim();
        window.location.href = "/reservas/verReserva/" + id;
    });

    $(".editarReservaLink").on("click", function(){
        id = $(this).parent().parent().children()[0];
        id = $(id).text().trim();
        window.location.href = "/reservas/editarReserva/" + id + "/_";
    });

    $(".eliminarReservaLink").on("click", function(){
        id = $(this).parent().parent().children()[0];
        id = $(id).text().trim();
        $("#PopUp h3 span").text(id);
        $("#PopUpContainer").fadeIn("fast");
    });

    $("#PedidosDia input").on("click", function(){
        checkBox = $(this)[0];
        estado = checkBox.checked;
        
        if(estado)
            window.location.href = "/reservas/" + "filterPedidosDia";
        else
            window.location.href = "/reservas/" + "_";
    });
});