

function selecflia(cat,scat) {
   
if ($(document).width()<1300){  $('#categoria').hide();  $('#mostrador').show();}
cargapagina('mostrador.php?cat='+cat+'&scat='+scat,'mostrador');
selec();   
}
function seleccab() { 
    selec();   

}
function selec() {    
 
vale=0;
    $('.menu-cat li:has(ul)').click(function(e){   
        if(vale==0){
           vale=1;
        e.preventDefault();        
        if($(this).hasClass('activado')){
            $(this).removeClass('activado');
            $(this).children('ul').slideUp();
        }else{        
            $('.menu-cat li ul').slideUp();
            $('.menu-cat li').removeClass('activado');
            $(this).addClass('activado');
            $(this).children('ul').slideDown();
        }
        }      
    });  
        
}

function cargacodigo(){
if (validarusu()==true){
   document.location.href='/cargainventario';
}
}

function inventprocesarcod(){
if (validarusu()==true){
   document.location.href='/invprocesos/';
}
}
function informes(){
if (validarusu()==true){
   document.location.href='/informes';
}
}
