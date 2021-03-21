var popUp = "<div id='PopUpContainer'> \
                <div id='PopUp'> \
                    <h3>¿Seguro que desea eliminar el pedido con id '<span></span>' ?</h3> \
                    <div id='PopUpBtns'> \
                        <a id='PopUpSi'>Sí</a> \
                        <a id='PopUpNo'>No</a> \
                    </div \
                </div> \
            </div>";

var id = '';
var pedido;

$(document).ready(function () {

    $("body").append(popUp);
    $("#PopUpContainer").hide();

    $("#PopUpNo").on("click", function () {
        $("#PopUpContainer").fadeOut("fast");
    });

    $("#PopUpSi").on("click", function () {
        $("#PopUpContainer").fadeOut("fast");
        $(pedido).remove();
    });

    $(document).on('click', ".eliminarPedidoLink", function () {
        pedido = $(this).parent().parent();
        id = $(this).parent().parent().children()[0];
        id = $(id).text().trim();
        $("#PopUp h3 span").text(id);
        $("#PopUpContainer").fadeIn("fast");
    });

    /*$("#CargarPedidos").change(function(){
        var fileInput = $(this);
        var reader = new FileReader();
        reader.readAsText(fileInput);
        alert(reader.result);
    });*/


    function readSingleFile(evt) {
        var f = evt.target.files[0];

        if (f) {
            var r = new FileReader();
            r.onload = function (e) {
                var contenido = e.target.result;
                contenido = contenido.split('\n');
                addContent(contenido);
            }
            r.readAsText(f);
        }
        else {
            alert("No se ha podido leer el fichero");
        }
    }

    function addContent(c) {
        for (let i = 0; i < c.length; i++) {
            var content = c[i].split(';');
            var trash = "<a class='eliminarPedidoLink'><i class='fas fa-trash-alt'></i></a>";
            var tr = "<tr class='nuevosPedidos'>\
                            <td>" + content[0] + "</td>\
                            <td>" + content[1] + "</td>\
                            <td>" + content[2] + "</td>\
                            <td>" + content[3] + "</td>\
                            <td>" + trash + "</td>\
                        </tr>";
            $("#Reservas table tbody").append(tr);
        }
    }

    document.getElementById('CargarPedidos').addEventListener('change', readSingleFile, false);


    $("#BtnActualizar").on("click", function () {
        var contenido = getTableContent();
        //alert(JSON.stringify(contenido));
        $.post('/gestionPedidos/', contenido);
        alert("Se han actualizado los pedidos");
        location.reload();
    });

    function getTableContent() {
        var contenido = {};
        var tbody = $("tbody").children();

        for (let i = 0; i < tbody.length; i++) {
            var fila = $(tbody[i]).children();
            var contenidoFila = {};

            for (let j = 0; j < fila.length - 1; j++) {
                var celda = $(fila[j]).text().trim();
                contenidoFila['celda'+j] = celda;
            }

            contenido['fila'+i] = contenidoFila;
        }

        return {"contenido" : JSON.stringify(contenido)};
    }

});