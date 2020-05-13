<?php
session_start();
$titulo = "Registrarme";
$actual = "registro";
require_once("../layout/header.php");
?>
<link rel="stylesheet" href="../../assets/css/guest/auth/style.css" type="text/css">
<link rel="stylesheet" href="../../assets/css/addons/select2.css" type="text/css">
<link rel="stylesheet" href="../../assets/css/addons/bootstrap-material-datetimepicker.css" type="text/css"/>

<style type="text/css">
body {
    background: url("../../assets/img/guest/register/background.jpg")repeat center center fixed;
    background-size: cover;
}

.card{ 
    background-color: rgba(0, 0, 0, 0.5) !important;
}
input,.md-form > small,.select2-selection__rendered{
    color:  white !important;
    }
</style>
<?php
require_once("../layout/css.php");
?>
<main>
<section class="view intro-2">
        <div class="mask pattern-0 flex-center"></div>
<!-- Main Container -->
<div class="container mt-5 pt-3">
   
    <div class="row">
        <!-- Content -->
        <div class="col-md-6 mb-5">

          

           <!-- Products Grid -->
           <section class="section pt-4" >

                <!-- Grid row -->
                <div class="row">
                        <div class="col-12">
                        <div class="card z-depth-5 hoverable">
                            <div class="card-body">
                                <!--Header-->
                                <div class="text-center">
                                    <h3 class="white-text"><i class="fas fa-exclamation-triangle mr-2"></i>Inscripciones Agotadas</h3>
                                    <hr class="hr-light">
                                </div>
                                
                                
                                <h6 class="white-text">
                                    Lo sentimos, las inscripciones a la carrera "Piedra del Canadá: El Órigen" han finalizado.
                                    Puedes ingresar a la página oficial de Piedra del Canadá Tr (<a target="_blank" href="http://piedradelcanadatr.com">www.piedradelcanadatr.com  </a>) para más información acerca de la carrera.
                                </h6>

                                      
                                
                            </div>
                                </div>
            </div>
        </div>
            <!--Grid row-->
       
            </section>
            <!-- /.Products Grid -->
        </div>
        <!-- /.Content -->

        <div class="mt-5  text-center text-md-left  col-md-6 col-xl-5 offset-xl-1">
         
            <div class="card mb-4 z-depth-5 hoverable mt-5">
                <div class="card-body">
                  
                <div class="white-text">
                <h1 class="h1-responsive font-weight-bold">¡Consulta tu Estado! </h1>
                <hr class="hr-light">
                <h6>¿Ya estás registrado?, inicia sesion y verifica el estado de tu inscripción.</h6>
                <br>
                <a href="login.php" class="btn btn-outline-white btn-theme"><i class="fas fa-door-closed mr-2"></i>Consulta tu Estado</a>
            </div>
        </div>
    </div>
        </div>
    </div>
    </div>
<!-- /.Main Container -->
</section>
</main>
<?php
require_once("../layout/js.php");
?>
<script type="text/javascript" src="../../assets/js/addons/select2.min.js"></script>
<script type="text/javascript" src="../../assets/js/addons/i18n/es.js"></script>
<script type="text/javascript" src="../../assets/js/addons/bootstrap-material-datetimepicker.js"></script>
<script type="text/javascript" src="../../assets/js/addons/validation/jquery.validate.js"></script>
<script type="text/javascript" src="../../assets/js/addons/validation/messages_es.js"></script>
<script type="text/javascript">



$('#tipoIdentificacion').select2({
        placeholder: "Tipo de identificación *",
        theme: "material",
        language: "es"
    });
    
    $('#distancia').select2({
        placeholder: "Distancia que desea correr *",
        theme: "material",
        language: "es"
    });

    $('#sexo').select2({
        placeholder: "Sexo *",
        theme: "material",
        language: "es"
    });

    $('#tipoSangre').select2({
        placeholder: "Tipo de sangre *",
        theme: "material",
        language: "es"
    });

    $('#tallaCamisa').select2({
        placeholder: "Talla de camisa *",
        theme: "material",
        language: "es"
    });

    $(".select2-selection__arrow")
        .addClass("fas fa-chevron-down white-text");

$('#fechaNacimiento').bootstrapMaterialDatePicker({

// enable date picker
date : true, 

// enable time picker
time : false, 

// custom date format
format : 'YYYY-MM-DD', 

// min / max date
minDate : null, 
maxDate : null, 

// current date
currentDate : null, 

// Localization
lang : 'es', 

// week starts at
weekStart : 1, 

// short time format
shortTime : false, 

// text for cancel button
'cancelText' : '<i class="fas fa-times fa-2x"></i>', 

// text for ok button
'okText' : '<i class="fas fa-check fa-2x"></i>' 

});
 
function validar(){
  if($("#register_form").validate({
    lang: 'es',
    errorPlacement: function(error, element){
      $(element).parent().after(error);
		}})){        
    var email = $("#email").val();
    var confirmarEmail = $("#confirmarEmail").val();
    if(email == confirmarEmail){
if($("#terminoCondiciones").prop("checked") == true){

   var valor =  $("#numeroIdentificacion").val();
   var codigoGrupo =  $("#codigoGrupo").val();
  
    $.ajax({
  url: "../../controllers/auth.php",
  method: "POST",
  data: { method: "check_nuip", nuip:valor, cod:codigoGrupo},
}).done(function(response) {
    //console.log(response);
    var data = JSON.parse(response);
    if(data.status == 200){
    if(data.existeTodo){
        $("#register_form").submit();
    }else if(data.existeNuip){
        swal({
  //position: 'top-end',
  type: 'warning',
  title: 'El número de identificación ya ha sido registrado.',
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
    }else if(!data.existeCod){
        swal({
  //position: 'top-end',
  type: 'warning',
  title: 'El código que ingresaste no pertenece a ningún grupo registrado.',
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
    }
    }else{
        swal({
  //position: 'top-end',
  type: 'error',
  title: data.existe,
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
    }
    
}).fail(function( jqXHR, textStatus ) {
    swal({
  //position: 'top-end',
  type: 'error',
  title: textStatus,
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
});

//Verificacion de codigo de equipo

 /* var codigoGrupo =  $("#codigoGrupo").val();
    $.ajax({
  url: "../../controllers/auth.php",
  method: "POST",
  data: { method: "check_cod", cod:codigoGrupo},
}).done(function(response) { 
    console.log(response);
    var data = JSON.parse(response);
    if(data.status == 200){
    if(data.existe){
       $("#register_form").submit();    
    }else if(!data.existe){
     swal({
  //position: 'top-end',
  type: 'warning',
  title: 'El código que ingresaste no pertenece a ningún grupo registrado.',
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
    }
    }else{
        swal({
  //position: 'top-end',
  type: 'error',
  title: data.existe,
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
    }
    
}).fail(function( jqXHR, textStatus ) {
    swal({
  //position: 'top-end',
  type: 'error',
  title: textStatus,
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
});  */

//Fin de verificación de código de equipo


}else{
    swal({
  //position: 'top-end',
  type: 'warning',
  title: 'Acepte los terminos',
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
}) 
}
}else{
    swal({
  //position: 'top-end',
  type: 'warning',
  title: 'Los correos no coinciden',
  showConfirmButton: false,
  toast: true,
  animation: false,
  customClass: 'animated shake',
  timer: 3000
})
  }

  }
  }

</script>
<?php
require_once("../layout/footer.php");
?>