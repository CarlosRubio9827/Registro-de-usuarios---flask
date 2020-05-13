<?php
session_start();
$titulo = "Consulta Registros";
$actual = "loginConsulta";
require_once("../layout/header.php");
?>
<link rel="stylesheet" href="../../assets/css/guest/auth/style.css" type="text/css">
<link rel="stylesheet" href="../../assets/css/guest/auth/login_style.css" type="text/css">
<style type="text/css">
body {
    background: url("../../assets/img/guest/login/background.jpg")repeat center center fixed;
    background-size: cover;
}
.center-div-link{ 
    background-color: rgba(0, 0, 0, 0.5) !important;
}
 
</style> 
  
<!--Intro Section-->
<section class="view intro-2">
        <div class="mask pattern-0 flex-center"></div>
                <div class="full-bg-img">
                    <div class="container flex-center">
                        <div class="d-flex align-items-center content-height">
                            <div class="row flex-center pt-5 mt-3">
                     
                                <div class="col-md-12 mb-5">
                                    <!--Form-->
                                    <div class="card z-depth-5 hoverable">
                                        <div class="card-body">
                                            <!--Header-->
                                            <div class="text-center">
                                                <h3 class="white-text"><i class="fas fa-user-check mr-2"></i>Consulta Registros</h3>
                                                <hr class="hr-light">
                                            </div>
                                            <form id="login_form" method="POST" action="../../controllers/auth.php">
                                            <input type="hidden" required value="loginConsulta" name="method">
                                            <div class="md-form">
                                                <i class="far fa-envelope prefix white-text"></i>
                                                <input id="email" type="email" class="form-control validate white-text" name="email" required autofocus maxlength="100">
                                                <label for="email" data-error="Error" data-success="Correcto">Email <span class="obligatorio">*</span></label>
                                            </div>
                             

                                            <div class="md-form">
                                                <i class="fas fa-key prefix white-text"></i>
                                                <input id="contraseña" type="password" class="form-control validate white-text" name="contraseña" required>
                                                <label for="contraseña" data-error="Error" data-success="Correcto">Contraseña <span class="obligatorio">*</span></label>
                                            </div>
                     
                                            <div class="text-center mt-4">
                                                <a onclick="validar()" class="btn btn-theme btn-outline-white hoverable waves-light" role="button">
                                                    <i class="fas fa-door-closed mr-2"></i>Ver Registros</a>
                                                    <!--a class="btn waves-light white-text" role="button">
                                                    <i class="fas fa-key mr-2"></i>¿Olvido la contraseña?</a-->
                                            </div>
                                
                                            </form>
                                        </div>
                                    </div>
                                    <!--/.Form-->
                                    
                                </div>
                                           

                            </div>
                        </div>
                    </div>
                </div>
            </section>
<?php
require_once("../layout/js.php");
?>
<script type="text/javascript" src="../../assets/js/addons/validation/jquery.validate.js"></script>
<script type="text/javascript" src="../../assets/js/addons/validation/messages_es.js"></script>
<script type="text/javascript">

function validar(){
  if($("#login_form").validate({
    lang: 'es',
    errorPlacement: function(error, element){
      $(element).parent().after(error);
		}})){
    $("#login_form").submit();
  }
  }

</script>
<?php
require_once("../layout/footer.php");
?>