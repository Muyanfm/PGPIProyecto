$(document).ready(function(){

    // Conf Calendario
    fecha = new Date();
    dia = fecha.getDate();
    mes = fecha.getMonth() + 1;
    anio = fecha.getFullYear();

    if(dia < 10)
        dia = "0" + dia;

    if(mes < 10)
        mes = "0" + mes;

    hoy = anio + "-" + mes + "-" + dia;
    calendario = "<input type='date' id='dia' value='" + hoy + "' min='" + hoy + "'>";

    $('#SimularDia').append(calendario);
    
});

$(document).on("click", "#Matricula input", function(){
    $("#Matricula input").css("border","1px solid #ffcc00");

    $("#Matricula label").css(
        {"top":"0",
        "z-index":"2",
        "color":"#ffcc00",
        "font-size":".8em"}
    );
});

$(document).on("focusout", "#Matricula input", function(){
    if(!$("#Matricula input").val()){

        $("#Matricula input").css("border","1px solid #ffe88c");

        $("#Matricula label").css(
            {"top":"50%",
            "z-index":"0",
            "color":"#989898",
            "font-size":"1em"}
        );
    }
});

$(document).on("click", ".ContenedorBoton a", function(){
    matriculaLeida = $('#Matricula input').val().toUpperCase();
    matricula = matriculaLeida.replace(" ", "");
    
    if(matricula.length < 7){
        alert('La matrícula ' + matriculaLeida + ' no tiene el formato válido')
    }
    else{
        var io = $(this).attr('id')
        var dia = $("#dia").val();
        var hora = $("#hora").val();
        var minuto = $("#minuto").val();

        if(minuto < 10)
            minuto = "0" + minuto;

        hora += ":" + minuto;

        window.location.href = "/simulacion/lecturaMatricula/" + io + "/" + matricula + "/" + dia + "/" + hora;
    }   
});
