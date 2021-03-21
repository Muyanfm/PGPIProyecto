$(document).ready(function(){

    setTimeout(function(){
        var matricula = $('#span1').text();
        var io = $('#io').text();

        var url = window.location.href;
        var url = url.split('/');

        var dia = url[url.length-2];
        var hora = url[url.length-1];

        window.location.href = "/simulacion/checkSimulacion/" + io + "/" + matricula + "/" + dia + "/" + hora;
    }, 5000);

});

