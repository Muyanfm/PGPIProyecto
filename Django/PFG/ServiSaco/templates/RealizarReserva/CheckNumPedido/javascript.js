$(document).ready(function(){

    if($("#InputNumPedido").val().length){
        $("#InfoPedido input").css("border","1px solid #ffcc00");

        $("#InfoPedido label").css(
            {"top":"0",
            "z-index":"2",
            "color":"#ffcc00",
            "font-size":".8em"}
        );
    }
});

$(document).on("click", "#InfoPedido input", function(){
    $("#InfoPedido input").css("border","1px solid #ffcc00");

    $("#InfoPedido label").css(
        {"top":"0",
        "z-index":"2",
        "color":"#ffcc00",
        "font-size":".8em"}
    );
});

$(document).on("focusout", "#InfoPedido input", function(){
    if(!$("#InfoPedido input").val()){

        $("#InfoPedido input").css("border","1px solid #ffe88c");

        $("#InfoPedido label").css(
            {"top":"20px",
            "z-index":"0",
            "color":"#989898",
            "font-size":"1em"}
        );
    }
});

$(document).on("click", ".ContenedorBoton a", function(){
    pedidoLeido = $('#InputNumPedido').val();
    pedido = pedidoLeido.replace(" ", "");
    
    if(pedido.length < 6){
        alert('El número de pedido ' + pedidoLeido + ' no tiene el formato válido')
    }
    else{
        window.location.href = "/realizarReserva/" + pedido + "/_";
    }   
});
