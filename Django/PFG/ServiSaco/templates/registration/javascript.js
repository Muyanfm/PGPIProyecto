$(document).ready(function(){

    if($("#Usuario").val().length){
        $("#labelUsuario").addClass("labelActive");
        $("#Usuario").addClass("inputActive");
    }

    if($("#Password").val().length){
        $("#labelPassword").addClass("labelActive");
        $("#Password").addClass("inputActive");
    }

    $("#ContenedorUser").on("focusin", function(){
        $("#labelUsuario").addClass("labelActive");
        $("#Usuario").addClass("inputActive");
    });

    $("#ContenedorUser").on("focusout", function(){
        if(!$("#Usuario").val().length){
            $("#labelUsuario").removeClass("labelActive");
            $("#Usuario").removeClass("inputActive");
        }
    });


    $("#ContenedorPassword").on("focusin", function(){
        $("#labelPassword").addClass("labelActive");
        $("#Password").addClass("inputActive");
    });

    $("#ContenedorPassword").on("focusout", function(){
        if(!$("#Password").val().length){
            $("#labelPassword").removeClass("labelActive");
            $("#Password").removeClass("inputActive");
        }
    });
});