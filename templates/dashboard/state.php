<?php
session_start();
$titulo = "Estado de la Inscripción";
$actual = "state";
require_once("../layout/header.php");
require_once("../../controllers/require/pdo.php");
?>
<link rel="stylesheet" href="../../assets/css/guest/auth/style.css" type="text/css">
<link rel="stylesheet" href="../../assets/css/guest/auth/login_style.css" type="text/css">
<style type="text/css">
body {
    background: url("../../assets/img/dashboard/state/background.jpg")repeat center center fixed;
    background-size: cover;
}
 

</style>  
<?php
require_once("../layout/css.php");
$db = new PDO_Connect;
$db->connect();
$usuario = $db->getRow("SELECT * FROM usuarios WHERE idusuarios = ?",array($user->idusuarios));
if($usuario){
    $_SESSION['usuario'] = json_encode($usuario);   
    $user = $usuario;
}else{
    header('Location: ../auth/login.php');
}
$tz  = new DateTimeZone('America/Bogota');
$date_time = new DateTime($user->fechaNacimiento, $tz);
$edad = $date_time->diff(new DateTime('now', $tz))->y; 
?>
<!--Intro Section-->
<section class="section pt-4">
        <div class="mask pattern-0 flex-center"></div>
                <div class="full-bg-img">
                    <div class="container flex-center">
                        <div class="d-flex align-items-center content-height">
                            <div class="row flex-center pt-5 mt-3">
                     
                                <div class="col-12 mb-5 content-div">
                                    <!--Form-->
                                    <div class="card z-depth-5 hoverable">
                                        <div class="card-body">
                                            <!--Header-->
                                            <div class="text-center">
                                                <h4 class="white-text"><i class="fas fa-running mr-2"></i>
                                                <?php 
                                                
                                                if($user->sexo == 'Femenino'){
                                                echo "Bienvenida ". $user->nombreUsuario." ".$user->apellidosUsuario ;  
                                                }else{
                                                    echo "Bienvenido ". $user->nombreUsuario." ".$user->apellidosUsuario ;
                                               
                                                }

                                                ?>
                                            </h4>
                                                <hr class="hr-light">

                                                <?php

                                                if($user->estadoIncripcion == 'registrado'){
                                                  
                                                    ?>
                                                 <h5 class="white-text">¿Qué paso debo seguir para confirmar mi cupo en <strong> Piedra del Canadá: El órigen?</strong></h5>

                                                <h6 class="white-text">Terminar su inscripción a Piedra Del Canadá: El órigen es muy fácil, y cuentas con las siguientes opciones:</h6>
                                                </div>
                                                <div class="text-left">
                                                <ul>
                                                    <li class="white-text">
                                                        <h6 align="left"><strong>Tranferencia Bancaria</strong></h6>
                                                        <ul>
                                                            <li type="circle">
                                                                <p style="font-size:14px;" align="left">Consigne o transfiera la suma de <span class="resaltar"><?php echo '$'.number_format($user->valorPagar);?></span>
                                                            (valor de <span class="resaltar"><?php echo $user->distancia; ?></span>)</strong> a la Cuenta de ahorros <span class="resaltar">Bancolombia</span> #<span class="resaltar">864-196988-59</span>, a nombre de <span class="resaltar">Nelson Eduardo Martinez</span>. CC <span class="resaltar">6407506</span>.</p>
                                                            </li>

                                                            <li type="circle">
                                                                <p  style="font-size:14px;"align="left">Por último envia un correo a <span class="resaltar">info@rupinsi.com</span> con el comprobante de pago para 
                                                            confirmar tu transacción y activar tu inscripción.</p>
                                                            </li>
                                                        </ul>
                                                    </li>
                                                    <li class="white-text">
                                                        <h6 align="left" > <strong>Pago Presencial</strong></h6>
                                                        <ul>
                                                            <li><p style="font-size:14px;"  align="left">Comunicate al número de celular <span class="resaltar">+57 310 6899013</span> y acuerda un encuentro para terminar tu proceso de inscripción.</p>
                                                            </li>
                                                        </ul>
                                                    </li>
                                                </ul>
                                                <?php
                                                }else if($user->estadoIncripcion == 'pago'){
                                                    ?>
                                                    <h4 class="white-text"><i class="fas fa-flag-checkered mr-2"></i>
                                                    ¡Felicidades, estás inscrito en la Piedra Del Canadá: El órigen!
                                                </h4>
                                             
                                                    <h6 class="white-text"><span class="resaltar">Pronto te daremos más información acerca de la carrera</span></strong></h6>
                                                    <?php 
                                                        }
                                                    ?>
                                                </div>
                                       
                                        </div>
                                    </div>
                                    <!--/.Form-->
                                    
                                </div>

        

                                                   <!--Datos personales--> 
                                
                                <div class="col-12 mb-5 content-div">
                                    <!--Form-->
                                    <div class="card z-depth-5 hoverable">
                                        <div class="card-body">
                                            <!--Header-->
                                            <div class="text-center">
                                                <h4 class="white-text"><i class="fas fa-user-circle mr-2"></i>
                                                Tus Datos Personales
                                            </h4>
                                                <!--hr class="hr-light"-->
                                                 
                                                <div style=" text-align: center; background-color: rgba(255,255,255,0)!important;">
                                                    <table  class="table table-sm table-hover" >
                                                            <thead>
                                                                
                                                            </thead>
                                                            <tbody style=" text-align: left;background-color: rgba(0,0,0,0.05)!important;">
                                                            <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Estado Inscripción </strong></th>
                                                                <td>
                                                                <?php

if($user->estadoIncripcion == 'registrado'){
  
    ?>
                                                                
                                                                  <h4><span class="badge badge-warning hoverable">
                                                                  <i class="fas fa-hand-holding-usd mr-1"></i> Pendiente de Pago
                                                                </span></h4>
                                                                <?php
                                                }else if($user->estadoIncripcion == 'pago'){
                                                    ?>
                                                      <h4><span class="badge badge-success hoverable">
                                                      <i class="fas fa-flag-checkered mr-1"></i> Inscrito
                                                                </span></h4>
                                                            
                                                            <?php 
                                                        }
                                                    ?></td>
                                                                </tr>    
                                                            <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Distancia</strong></th>
                                                                <td><?php echo $user->distancia; ?></td>
                                                                
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Nombre Completo</strong></th>
                                                                <td><?php echo mb_strtoupper($user->nombreUsuario." ".$user->apellidosUsuario, 'UTF-8'); ?></td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Equipo</strong></th>
                                                                <td><?php echo mb_strtoupper($user->grupo, 'UTF-8'); ?></td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Correo Electrónico</strong></th>
                                                                <td><?php echo $user->correoElectronico; ?></td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Doc. Identidad</strong></th>
                                                                <td><?php echo $user->tipoIdentificacion." -:- ".$user->numeroIdentificacion; ?></td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Número Teléfono</strong></th>
                                                                <td><?php echo $user->telefono; ?></td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Fecha de Nacimiento</strong></th>
                                                                <td><?php echo $date_time->format('d/m/Y'); ?></td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Edad</strong></th>
                                                                <td><?php echo $edad; ?> Años</td>
                                                                </tr>
                                                                <tr class="hoverable tr-theme">
                                                                <th scope="row"><strong>Talla Camisa</strong></th>
                                                                <td><h5><span class="badge badge-primary hoverable"><?php echo mb_strtoupper($user->tallaCamisa, 'UTF-8'); ?></span></h5></td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <!--
                                                        <a href="../../controllers/exit.php" class="btn btn-theme btn-outline-white hoverable waves-light waves-effect"><i class="fas fa-door-closed mr-2"></i>Regresar a la Página Principal</a>
                                                        -->
                                                        
                                                </div>
                                                
                                                </div>
   
                                        </div>
                                    </div>
                                    <!--/.Form-->
                                  
                                </div>

                                <!--Fin datos Persoanles-->
<!--0=======================================================================================================-->
                                <!--Inicio de Hospedaje-->

                                <div class="col-12 mb-5 content-div">
                                    <!--Form-->
                                    <div class="card z-depth-5 hoverable">
                                        <div class="card-body">
                                            <!--Header-->
                                            <div class="text-center">
                                                <h4 class="white-text"><i class="fas fa-bed mr-2"></i>
                                                        ¿A DÓNDE VAMOS? 
                                                </h4>
                                                <hr class="hr-light">

                                                
                                                 <h5 class="white-text">¡Si esta pregunta te preocupa, <strong> Piedra del Canadá: El órigen</strong> te tiene la solución!</h5>

                                                </div>
                                                <div class="text-center">
                                                    <h4 class="white-text">
                                                    Pasadias, Hospedajes en fincas de alquiler, Alimentación, Guía y lógistica en turismo de la región.
                                                    </h4>  
                                             
                                                    <h3 class="white-text"><span class="resaltar">Para más información </span><span class="badge badge-success hoverable"> <a class="white-text" href="hospedaje.rupinsi.com"> <i class="fas fa-check mr-2"></i> Click Aquí</a>  </span></strong></h3>
                                                   
                                                </div>
                                       
                                        </div>
                                    </div>
                                    <!--/.Form-->
                                    
                                </div>

                                <!--Fin Hospedaje-->
                              
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