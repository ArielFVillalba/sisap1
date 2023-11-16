
$(window).resize(function(){
actcompelem();
});
function actcompelem(){
if(document.getElementById('formArticulo') ){
    if (document.querySelector('#columnalst')) {
       $('.columnalst').css({'height':'30px'});
     if ($(columna).width()<1000){
        $('.columnalst').css({'height':'100px'});
        $('.columnalstt').css({'height':'80px'});
      }
    }
    if (document.querySelector('#columna0')) {
       $('.columna0').css({'height':'910px'});
        if ($(columna0).width()<800){
             $('.columna0').css({'height':'600px'});
        }
    }
}
}
function procesarfun(){
setTimeout(colorlistdo,2);
setTimeout(formatearcampos,2);
setTimeout(actcompelem(),1000);


}

function buscararticulo(){

var inputElement = document.getElementById('idbuscar');
var variable = inputElement.value;
let longitud = variable.length;
if ( variable=='') {variable=0};

if ( variable.length>1  || variable==0 || variable=="*" ) {
var url = "/articulos/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}else{
variable=0;
var url = "/articulos/" + variable + "/listar/";  // Construir la URL de la vista
window.location.href = url;
}
}

function buscdatosart(){
document.getElementById("descripcion").value="";
variable= document.getElementById('codigo').value
let longitud = variable.length;
if ( variable.length>3) {
var codigo = document.getElementById('codigo').value;
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/articulodatos/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'codigo': codigo},
     success: function(data) {
     var list = data.datos;
     var artículos = list[0];
if (document.querySelector('#descripcion')) { document.getElementById("descripcion").value=artículos.descripcion;}
if (document.querySelector('#precio')) { document.getElementById("precio").value=artículos.precio;}
if (document.querySelector('#iva')) { document.getElementById("iva").value=artículos.iva;}
if (document.querySelector('#cantidad')) { document.getElementById("cantidad").focus();}

 }
});
}
//else{ if (document.getElementById("descripcion")) {document.getElementById("descripcion").focus();}}
}

function buscdatosartdescri(){
var desc = document.getElementById('descripcion').value;

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/articulodatosdesc/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     data: { 'desc': desc},
     success: function(data) {
     var list = data.datos;
     var artículos = list[0];
if (document.querySelector('#codigo')) { document.getElementById("codigo").value=artículos.codigo;}
if (document.querySelector('#precio')) { document.getElementById("precio").value=artículos.precio;}
if (document.querySelector('#iva')) { document.getElementById("iva").value=artículos.iva;}
if (document.querySelector('#cantidad')) { document.getElementById("cantidad").focus();}
    }
});
}

function colorlistdo(){
const elementos = document.querySelectorAll('.columnalst');
e=1;  col='#D5F5E3';
elementos.forEach(elemento => {
  elemento.style.backgroundColor = col;
  e=e+1;
  if (e > 1 ){  if (e % 2 === 0) { col='#EAF2F8';   } else {  col='#D5F5E3';   }  }
});
}

function formatearcampos(){

formatearcampnumv("id_costo");
formatearcampnumv("id_precio");

const titleElement = document.getElementById('titleElement');
const titleText = titleElement.textContent.trim();
if   (titleText=="EDITAR  ARTICULO")  { extraercoma();};
}

function extraercoma(){
document.getElementById("id_costo").value=document.getElementById("id_costo").value.replace(/,/g, '');
document.getElementById("id_precio").value=document.getElementById("id_precio").value.replace(/,/g, '');

}


function cargarcmbart(){

var csrftoken = $("[name=csrfmiddlewaretoken]").val();
$.ajax({
     url: "/cmbarticulo/",  type: 'POST', datatype: 'json',  headers:{ "X-CSRFToken": csrftoken    },
     success: function(data) {
     const obj = data.datos;
    crearcmbart(obj);
    }
});
}

function crearcmbart(list){
    var dataList = document.createElement('datalist');
    dataList.id = "descrip_list";

for (var i = 0; i < list.length; i++) {
  var artículo = list[i];
     var option = document.createElement('option');
        option.setAttribute('id', artículo.codigo);
        option.value = artículo.descripcion;
        dataList.appendChild(option);
    }
    document.body.appendChild(dataList
    );
}
