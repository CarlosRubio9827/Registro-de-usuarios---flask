# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response, make_response, request, redirect,url_for, flash, session, json, jsonify, logging, send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pdfkit
import io
import xlwt
from datetime import date
from datetime import datetime

app = Flask(__name__)



#Configuración de sesion . permanete
@app.before_request
def session_management():
  session.permanent = True
  
#Mysql connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PORT"] = 3307
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "piedradelcanada2"

mysql = MySQL(app)

#Session
app.secret_key = "piedradelcanada"


#definir rutas

#Ruta adminLogin

@app.route("/loginAdmin")
def loginAdmin():
 
  messages= []
  if session["loggedAdmin"] == True:
    email = session["email"]
    contraseña = session["contraseña"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarioadministrador WHERE correoElectronico = (%s) and contraseña = (%s)", (email, contraseña))
    usuario = cur.fetchone()
    if usuario:
      cur.execute("SELECT * FROM usuarios")
      usuarios = cur.fetchall()
      usuarios = list(usuarios)
     
      usuarios2 = []
      for x in range(0, len(usuarios)):
        user = list(usuarios[x])
        
        
        #Tipo Identificación
        tipoIdentificacion = user[6]
        cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
        tipoIdentificacion = cur.fetchone()
        tipoIdentificacion = tipoIdentificacion[1]
        user[6] = tipoIdentificacion
            
        #Sexo
        sexo = user[9]
        cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
        sexo = cur.fetchone()
        sexo = sexo[1]
        user[9] = sexo
           
        #Distancia
        distancia = user[3]
        cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
        distancia = cur.fetchone()
        user[3] = distancia[1]
          
        #Tipo Sangre
        tipoSangre = user[14]  
        cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
        tipoSangre = cur.fetchone()     
        tipoSangre = tipoSangre[1]
        user[14] = tipoSangre  

        #Talla Camisa
        tallaCamisa = user[16]
        cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
        tallaCamisa = cur.fetchone()
        tallaCamisa = tallaCamisa[1]
        user[16] = tallaCamisa

        #Categoria
        categoria = user[4]
        cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
        categoria = cur.fetchone()
        categoria = categoria[1]
        user[4] = categoria

        #Estado Inscripción
        estadoInscripcion = user[19]
        cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
        estadoInscripcion = cur.fetchone()
        estadoInscripcion = estadoInscripcion[1]
        user[19] = estadoInscripcion
        
        #Estado Kit
        estadoKit = user[20]
        cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
        estadoKit = cur.fetchone()
        estadoKit = estadoKit[1]
        user[20] = estadoKit
      
        #Código Equipo
        codigoEquipo = user[21]     
        cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
        codigoEquipo = cur.fetchone()
        codigoEquipo = codigoEquipo[1]
        user[21] = codigoEquipo

        #Fecha de Reistro
        fechaRegistro = str(user[22])
        fechaRegistro = fechaRegistro[0:10]
        user[22] = fechaRegistro
        usuarios2.append(user)
      usuarios = usuarios2
      

      if "messages" in session:
        messagesNew = session['messages']
        messages.append("success")
        messages.append(messagesNew[1])  
      else:
        messages.append("0")
        messages.append("1")
      return render_template("dashboard/estado.html", usuario=usuario, usuarios=usuarios,messages = messages)
    
  else:
    messages.append("0")
    messages.append("1")
    return render_template("auth/loginConsulta.html", messages = messages)

@app.route("/loginAdmin", methods=["POST"])
def adminLoginPost():
  messages = []
  email = request.form["email"]
  contraseña = request.form["contraseña"]
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM usuarioadministrador WHERE correoElectronico = (%s) and contraseña = (%s)", (email, contraseña))
  usuario = cur.fetchone()
  if usuario:
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    usuarios = list(usuarios)
    usuarios2 = []
    for x in range(0, len(usuarios)):
      user = list(usuarios[x])
      
      #Tipo Identificación
      tipoIdentificacion = user[6]
      cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
      tipoIdentificacion = cur.fetchone()
      tipoIdentificacion = tipoIdentificacion[1]
      user[6] = tipoIdentificacion
          
      #Sexo
      sexo = user[9]
      cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
      sexo = cur.fetchone()
      sexo = sexo[1]
      user[9] = sexo
          
      #Distancia
      distancia = user[3]
      cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
      distancia = cur.fetchone()
      user[3] = distancia[1]
        
      #Tipo Sangre
      tipoSangre = user[14]  
      cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
      tipoSangre = cur.fetchone()     
      tipoSangre = tipoSangre[1]
      user[14] = tipoSangre  

      #Talla Camisa
      tallaCamisa = user[16]
      cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
      tallaCamisa = cur.fetchone()
      tallaCamisa = tallaCamisa[1]
      user[16] = tallaCamisa

      #Categoria
      categoria = user[4]
      cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
      categoria = cur.fetchone()
      categoria = categoria[1]
      user[4] = categoria

      #Estado Inscripción
      estadoInscripcion = user[19]
      cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
      estadoInscripcion = cur.fetchone()
      estadoInscripcion = estadoInscripcion[1]
      user[19] = estadoInscripcion
      
      #Estado Kit
      estadoKit = user[20]
      cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
      estadoKit = cur.fetchone()
      estadoKit = estadoKit[1]
      user[20] = estadoKit
    
      #Código Equipo
      codigoEquipo = user[21]     
      cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
      codigoEquipo = cur.fetchone()
      codigoEquipo = codigoEquipo[1]
      user[21] = codigoEquipo

      #Fecha de Reistro
      fechaRegistro = str(user[22])
      fechaRegistro = fechaRegistro[0:10]
      user[22] = fechaRegistro
      usuarios2.append(user)
    usuarios = usuarios2  
    
    session["loggedAdmin"] = True
    session["email"] = email
    session["contraseña"] = contraseña
    messages.append("info")
    messages.append("Bienvenido a la consulta de datos - Piedra del Canadá")
    return render_template("dashboard/estado.html", usuario=usuario, usuarios=usuarios, messages = messages)
  else:
    messages.append("error")
    messages.append("Credenciales Incorrectos")
    return render_template("auth/loginConsulta.html", messages=messages)

@app.route("/configuracion")
def configuracion():
  return render_template("dashboard/configuracion.html")

@app.route("/confirmarPago/<string:id>", methods=["POST"])
def confirmarPago(id):
    cur = mysql.connection.cursor()
    
    cur.execute("UPDATE usuarios SET estadoInscripcion_idestadoInscripcion=(%s) WHERE idusuarios = (%s)", ("2", id))
    mysql.connection.commit()
    messages = []
    messages.append("confirmarPago")
    messages.append("¡Se ha guardado el pago correctamente!")
    session["messages"] = messages
    
    return redirect(url_for("loginAdmin"))

@app.route("/entregarKit/<string:id>", methods=["POST"])
def entregarKit(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET estadoKit_idestadoKit=(%s) WHERE idusuarios = (%s)", ("2", id))
    mysql.connection.commit()
    messages = []
    messages.append("confirmarPago")
    messages.append("¡Se ha cambiado el estado de entrega del kit correctamente!")
    session["messages"] = messages
    
    return redirect(url_for("loginAdmin"))  

# Ruta para exportar a PDF
@app.route("/exportarPdf")
def exportarPdf():
  
  cur = mysql.connection.cursor()
  
  cur.execute("SELECT * FROM usuarios")
  usuarios = cur.fetchall()
  usuarios = list(usuarios)
  usuarios2 = []
  for x in range(0, len(usuarios)):
    user = list(usuarios[x])
    
    #Tipo Identificación
    tipoIdentificacion = user[6]
    cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
    tipoIdentificacion = cur.fetchone()
    tipoIdentificacion = tipoIdentificacion[1]
    user[6] = tipoIdentificacion
        
    #Sexo
    sexo = user[9]
    cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
    sexo = cur.fetchone()
    sexo = sexo[1]
    user[9] = sexo
        
    #Distancia
    distancia = user[3]
    cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
    distancia = cur.fetchone()
    user[3] = distancia[1]
      
    #Tipo Sangre
    tipoSangre = user[14]  
    cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
    tipoSangre = cur.fetchone()     
    tipoSangre = tipoSangre[1]
    user[14] = tipoSangre  

    #Talla Camisa
    tallaCamisa = user[16]
    cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
    tallaCamisa = cur.fetchone()
    tallaCamisa = tallaCamisa[1]
    user[16] = tallaCamisa

    #Categoria
    categoria = user[4]
    cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
    categoria = cur.fetchone()
    categoria = categoria[1]
    user[4] = categoria

    #Estado Inscripción
    estadoInscripcion = user[19]
    cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
    estadoInscripcion = cur.fetchone()
    estadoInscripcion = estadoInscripcion[1]
    user[19] = estadoInscripcion
    
    #Estado Kit
    estadoKit = user[20]
    cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
    estadoKit = cur.fetchone()
    estadoKit = estadoKit[1]
    user[20] = estadoKit
  
    #Código Equipo
    codigoEquipo = user[21]     
    cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
    codigoEquipo = cur.fetchone()
    codigoEquipo = codigoEquipo[1]
    user[21] = codigoEquipo

    #Fecha de Reistro
    fechaRegistro = str(user[22])
    fechaRegistro = fechaRegistro[0:10]
    user[22] = fechaRegistro
    usuarios2.append(user)
  usuarios = usuarios2  
  now = datetime.now()
  fecha = []
  fecha.append(now.year)
  fecha.append(now.month)
  fecha.append(now.day)
  fecha.append(now.hour)
  fecha.append(now.minute)
  fecha.append(now.second)
  
  rendered = render_template("export/usuariosPdf.html", usuarios=usuarios, fecha=fecha)

  config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

  pdf = pdfkit.from_string(rendered, False, configuration=config)
  response = make_response(pdf)
  response.headers["Content-Type"] = "application/pdf"
  response.headers["Content-Disposition"] = "inline; filename=output.pdf"
  return response
  
   
# Ruta para exportar a Excel
@app.route("/exportarExcel")
def exportarExcel():
  cur = mysql.connection.cursor()
  
  cur.execute("SELECT * FROM usuarios")
  usuarios = cur.fetchall()
  usuarios = list(usuarios)
  usuarios2 = []
  for x in range(0, len(usuarios)):
    user = list(usuarios[x])
    
    #Tipo Identificación
    tipoIdentificacion = user[6]
    cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
    tipoIdentificacion = cur.fetchone()
    tipoIdentificacion = tipoIdentificacion[1]
    user[6] = tipoIdentificacion
        
    #Sexo
    sexo = user[9]
    cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
    sexo = cur.fetchone()
    sexo = sexo[1]
    user[9] = sexo
        
    #Distancia
    distancia = user[3]
    cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
    distancia = cur.fetchone()
    user[3] = distancia[1]
      
    #Tipo Sangre
    tipoSangre = user[14]  
    cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
    tipoSangre = cur.fetchone()     
    tipoSangre = tipoSangre[1]
    user[14] = tipoSangre  

    #Talla Camisa
    tallaCamisa = user[16]
    cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
    tallaCamisa = cur.fetchone()
    tallaCamisa = tallaCamisa[1]
    user[16] = tallaCamisa

    #Categoria
    categoria = user[4]
    cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
    categoria = cur.fetchone()
    categoria = categoria[1]
    user[4] = categoria

    #Estado Inscripción
    estadoInscripcion = user[19]
    cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
    estadoInscripcion = cur.fetchone()
    estadoInscripcion = estadoInscripcion[1]
    user[19] = estadoInscripcion
    
    #Estado Kit
    estadoKit = user[20]
    cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
    estadoKit = cur.fetchone()
    estadoKit = estadoKit[1]
    user[20] = estadoKit
  
    #Código Equipo
    codigoEquipo = user[21]     
    cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
    codigoEquipo = cur.fetchone()
    codigoEquipo = codigoEquipo[1]
    user[21] = codigoEquipo

    #Fecha de Reistro
    fechaRegistro = str(user[22])
    fechaRegistro = fechaRegistro[0:10]
    user[22] = fechaRegistro
    usuarios2.append(user)
  usuarios = usuarios2

  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Reporte de Usuarios')
   
  #add headers
  sh.write(0, 0, 'Doc. Id.')
  sh.write(0, 1, 'Nombre')
  sh.write(0, 2, 'Apellido')
  sh.write(0, 3, 'Fecha Nacimiento')
  sh.write(0, 4, 'Email')
  sh.write(0, 5, 'Equipo')
  sh.write(0, 6, 'Distancia')
  sh.write(0, 7, 'Sexo')
  sh.write(0, 8, 'Telefono')
  sh.write(0, 9, 'País')
  sh.write(0, 10, 'Departamento')
  sh.write(0, 11, 'Ciudad')
  sh.write(0, 12, 'Tipo Sangre')
  sh.write(0, 13, "Entidad Salud")
  sh.write(0, 14, "Talla Camisa")
  sh.write(0, 15, 'Estado incripción')
  sh.write(0, 16, "Estado Kit")
  sh.write(0, 17, "Categoría")
  

  idx = 0
  for user in usuarios:
   sh.write(idx+1, 0, user[7])
   sh.write(idx+1, 1, user[1])
   sh.write(idx+1, 2, user[2])
   sh.write(idx+1, 3, user[8])
   sh.write(idx+1, 4, user[5])
   sh.write(idx+1, 5, user[21])
   sh.write(idx+1, 6, user[3])
   sh.write(idx+1, 7, user[9])
   sh.write(idx+1, 8, user[10])
   sh.write(idx+1, 9, user[11])
   sh.write(idx+1, 10, user[12])
   sh.write(idx+1, 11, user[13])
   sh.write(idx+1, 12, user[14])
   sh.write(idx+1, 13, user[15])
   sh.write(idx+1, 14, user[16])
   sh.write(idx+1, 15, user[19])
   sh.write(idx+1, 16, user[20])
   sh.write(idx+1, 17, user[4])
   idx += 1
    
  workbook.save(output)
  output.seek(0)
  now = datetime.now()
  

  nameFile = "Reporte usuarios - " + str(now)
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename="+nameFile+".xls"})
 

@app.route("/mostrarUsuario/<string:id>")
def mostrarUsuario(id):
    if session["loggedAdmin"] == True:
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM usuarios WHERE idusuarios=(%s)", [id])
      usuario = cur.fetchone()
      if usuario:
        usuario = list(usuario)

        #Tipo Identificación
        tipoIdentificacion = usuario[6]
        cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
        tipoIdentificacion = cur.fetchone()
        tipoIdentificacion = tipoIdentificacion[1]
        usuario[6] = tipoIdentificacion
        
        #Sexos   
        sexo = usuario[9]
        cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
        sexo = cur.fetchone()
        sexo = sexo[1]
        usuario[9] = sexo

        #Distancia
        distancia = usuario[3]
        cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
        distancia = cur.fetchone()
        usuario[3] = distancia
        
        #Tipo Sangre
        tipoSangre = usuario[14]
        cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
        tipoSangre = cur.fetchone()
        tipoSangre = tipoSangre[1]
        usuario[14] = tipoSangre  

        #Talla Camisa
        tallaCamisa = usuario[16]
        cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
        tallaCamisa = cur.fetchone()
        tallaCamisa = tallaCamisa[1]
        usuario[16] = tallaCamisa

        #Categoria
        categoria = usuario[4]
        cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
        categoria = cur.fetchone()
        categoria = categoria[1]
        usuario[4] = categoria

        #Estado Inscripción
        estadoInscripcion = usuario[19]
        cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
        estadoInscripcion = cur.fetchone()
        estadoInscripcion = estadoInscripcion[1]
        usuario[19] = estadoInscripcion
    
        #Estado Kit
        estadoKit = usuario[20]
        cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
        estadoKit = cur.fetchone()
        estadoKit = estadoKit[1]
        usuario[20] = estadoKit

        #Código Equipo
        codigoEquipo = usuario[21]
        cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
        codigoEquipo = cur.fetchone()
        codigoEquipo = codigoEquipo[1]
        usuario[21] = codigoEquipo

        #Fecha de Reistro
        fechaRegistro = str(usuario[22])
        fechaRegistro = fechaRegistro[0:10]
        usuario[22] = fechaRegistro 
        messages = []
        messages.append("info")
        messages.append("Información de "+usuario[1]+" "+usuario[2]) 
        return render_template("dashboard/mostrarUsuario.html", messages=messages, usuario=usuario)
      else:
        return redirect(url_for("loginAdmin"))
    else:
      return redirect(url_for("loginAdmin"))

@app.route("/logoutAdmin", methods=["POST"])
def logoutAdmin():
  if request.method == "POST":
    session['loggedAdmin'] = False
    
    return redirect(url_for("loginAdmin"))

#Ruta login

@app.route("/")
def raiz():
  session["loggedin"] = False
  session["loggedAdmin"] = False

  """ messages = []
  ["loggedAdmin"]
  if session["loggedin"] == True:
    nuip = session["nuip"]
    email = session["email"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE correoElectronico = (%s) and numeroIdentificacion = (%s)", (email, nuip))
    usuario = cur.fetchone()
    if usuario:  
      session['loggedin'] = True
      session['nuip'] = nuip
      session['email'] = email
      messages = []
      messages.append("info")
      messages.append("Bienvenido a la piedra del Canadá") 
      return render_template("dashboard/state.html", messages=messages, usuario=usuario) """
  #session['loggedin'] = False
  return redirect(url_for("login"))


@app.route('/login')
def login():
  cur = mysql.connection.cursor()
  messages = []
  session['login'] = "active"
  session['registro'] = ""
  if session["loggedin"] == True:
    nuip = session["nuip"]
    email = session["email"]
    
    cur.execute("SELECT * FROM usuarios WHERE correoElectronico = (%s) and numeroIdentificacion = (%s)", (email, nuip))
    usuario = cur.fetchone()
    if usuario:
      usuario = list(usuario)

      #Tipo Identificación
      tipoIdentificacion = usuario[6]
      cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
      tipoIdentificacion = cur.fetchone()
      tipoIdentificacion = tipoIdentificacion[1]
      usuario[6] = tipoIdentificacion
      
      #Sexos   
      sexo = usuario[9]
      cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
      sexo = cur.fetchone()
      sexo = sexo[1]
      usuario[9] = sexo

      #Distancia
      distancia = usuario[3]
      cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
      distancia = cur.fetchone()
      usuario[3] = distancia
       
      #Tipo Sangre
      tipoSangre = usuario[14]
      cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
      tipoSangre = cur.fetchone()
      tipoSangre = tipoSangre[1]
      usuario[14] = tipoSangre  

      #Talla Camisa
      tallaCamisa = usuario[16]
      cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
      tallaCamisa = cur.fetchone()
      tallaCamisa = tallaCamisa[1]
      usuario[16] = tallaCamisa

      #Categoria
      categoria = usuario[4]
      cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
      categoria = cur.fetchone()
      categoria = categoria[1]
      usuario[4] = categoria

      #Estado Inscripción
      estadoInscripcion = usuario[19]
      cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
      estadoInscripcion = cur.fetchone()
      estadoInscripcion = estadoInscripcion[1]
      usuario[19] = estadoInscripcion
  
      #Estado Kit
      estadoKit = usuario[20]
      cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
      estadoKit = cur.fetchone()
      estadoKit = estadoKit[1]
      usuario[20] = estadoKit

      #Código Equipo
      codigoEquipo = usuario[21]
      cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
      codigoEquipo = cur.fetchone()
      codigoEquipo = codigoEquipo[1]
      usuario[21] = codigoEquipo

      #Fecha de Reistro
      fechaRegistro = str(usuario[22])
      fechaRegistro = fechaRegistro[0:10]
      usuario[22] = fechaRegistro   

      #Inicialización de Cookies para la sesión
      session['loggedin'] = True
      session['nuip'] = nuip
      session['email'] = email
      messages = []
      messages.append("info")
      messages.append("Bienvenido a la piedra del Canadá")
      return render_template("dashboard/state.html", messages=messages, usuario=usuario)
  messages.append("0")
  messages.append("1")





  return render_template("auth/login.html", messages=messages)

#Méetodo de login
@app.route("/login", methods=["POST"])
def loginUsuario():
  
  if request.method == "POST":
    email = request.form["email"] 
    nuip = request.form["numeroIdentificacion"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE correoElectronico = (%s) and numeroIdentificacion = (%s)", (email, nuip))
    usuario = cur.fetchone()
    if usuario:
      usuario = list(usuario)

      #Tipo Identificación
      tipoIdentificacion = usuario[6]
      cur.execute("SELECT * FROM tipoIdentificacion WHERE idtipoIdentificacion = (%s)", [tipoIdentificacion])
      tipoIdentificacion = cur.fetchone()
      tipoIdentificacion = tipoIdentificacion[1]
      usuario[6] = tipoIdentificacion
      
      #Sexos   
      sexo = usuario[9]
      cur.execute("SELECT * FROM sexo WHERE idsexo = (%s)", [sexo])
      sexo = cur.fetchone()
      sexo = sexo[1]
      usuario[9] = sexo

      #Distancia
      distancia = usuario[3]
      cur.execute("SELECT * FROM distancias WHERE iddistancias = (%s)", [distancia])
      distancia = cur.fetchone()
      usuario[3] = distancia
       
      #Tipo Sangre
      tipoSangre = usuario[14]
      cur.execute("SELECT * FROM tiposangre WHERE idtipoSangre = (%s)", [tipoSangre])
      tipoSangre = cur.fetchone()
      tipoSangre = tipoSangre[1]
      usuario[14] = tipoSangre  

      #Talla Camisa
      tallaCamisa = usuario[16]
      cur.execute("SELECT * FROM tallacamisa WHERE idtallaCamisa = (%s)", [tallaCamisa])
      tallaCamisa = cur.fetchone()
      tallaCamisa = tallaCamisa[1]
      usuario[16] = tallaCamisa

      #Categoria
      categoria = usuario[4]
      cur.execute("SELECT * FROM categorias WHERE idcategorias = (%s)", [categoria])
      categoria = cur.fetchone()
      categoria = categoria[1]
      usuario[4] = categoria

      #Estado Inscripción
      estadoInscripcion = usuario[19]
      cur.execute("SELECT * FROM estadoinscripcion WHERE idestadoInscripcion = (%s)", [estadoInscripcion])
      estadoInscripcion = cur.fetchone()
      estadoInscripcion = estadoInscripcion[1]
      usuario[19] = estadoInscripcion
      
      #Estado Kit
      estadoKit = usuario[20]
      cur.execute("SELECT * FROM estadokit WHERE idestadoKit = (%s)", [estadoKit])
      estadoKit = cur.fetchone()
      estadoKit = estadoKit[1]
      usuario[20] = estadoKit

      #Código Equipo
      codigoEquipo = usuario[21]
      cur.execute("SELECT * FROM equipos WHERE idequipos = (%s)", [codigoEquipo])
      codigoEquipo = cur.fetchone()
      codigoEquipo = codigoEquipo[1]
      usuario[21] = codigoEquipo

      #Fecha de Reistro
      fechaRegistro = str(usuario[22])
      fechaRegistro = fechaRegistro[0:10]
      usuario[22] = fechaRegistro   

      #Inicialización de Cookies para la sesión
      session['loggedin'] = True
      session['nuip'] = nuip
      session['email'] = email
      messages = []
      messages.append("info")
      messages.append("Bienvenido a la piedra del Canadá")
      return render_template("dashboard/state.html", messages=messages, usuario=usuario)
    else:
      messages = []
      messages.append("error")
      messages.append("Credenciales Incorrectas") 
      return render_template("auth/login.html", messages=messages)

@app.route("/logout", methods=["POST"])
def estado():
  if request.method == "POST":
    session['loggedin'] = False
    
    return  redirect(url_for("login"))
    

#Ruta registro
@app.route("/registro")
def registro():
  #Conexión a la base de datos
  cur = mysql.connection.cursor()

  session['registro'] = "active"
  session['login'] = ""
  messages = []
  if session["loggedin"] == True:
    return  redirect(url_for("login"))
    
  messages.append("0")
  messages.append("1")

  #Consutal Distancias
  cur.execute("SELECT * FROM distancias")
  distancias = cur.fetchall()
  
  #Consutal Sexo
  cur.execute("SELECT * FROM sexo")
  sexos = cur.fetchall()
  
  #Consutal Tallas camisa
  cur.execute("SELECT * FROM tallacamisa")
  tallaCamisas = cur.fetchall()
  
  #Consutal Tipo identificación
  cur.execute("SELECT * FROM tipoidentificacion")
  tiposIdentificacion = cur.fetchall()
  
  #Consutal Tipo Sangre
  cur.execute("SELECT * FROM tiposangre")
  tiposSangre = cur.fetchall()
  
  return render_template("auth/registro.html", messages=messages,distancias=distancias,sexos=sexos,tallaCamisas=tallaCamisas,tiposIdentificacion=tiposIdentificacion,tiposSangre=tiposSangre)

#Método de Registro
@app.route("/registro", methods=["POST"])
def registroUsuario():
  if request.method == "POST":
    cur = mysql.connection.cursor()
    nombre = request.form['nombre']
    apellidos = request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']
    pais = request.form['pais']
    departamento = request.form['departamento']
    ciudad = request.form['ciudad']
    entidadSalud = request.form['seguroMedico']
    nombreContactoEmergencia = request.form['nombreContactoEmergencia']
    telefonoContactoEmergencia = request.form['numeroContactoEmergencia']
    fechaNacimiento = request.form['fechaNacimiento']
    numeroIdentificacion = request.form['numeroIdentificacion']
    
    #Tipo Identificación
    tipoIdentificacion = request.form['tipoIdentificacion']
    cur.execute("SELECT * FROM tipoIdentificacion WHERE inicialesTipoIdentificacion = (%s)", [tipoIdentificacion])
    tipoIdentificacion = cur.fetchone()
    tipoIdentificacion = tipoIdentificacion[0]

    #Sexos
    sexo = request.form['sexo']
    cur.execute("SELECT * FROM sexo WHERE nombreSexo = (%s)", [sexo])
    sexo = cur.fetchone()
    sexo2 = sexo[1]
    sexo = sexo[0]

    #Distancia
    distancia = request.form['distancia']
    cur.execute("SELECT * FROM distancias WHERE nombreDistancia = (%s)", [distancia])
    distancia = cur.fetchone()
    distancia2 = distancia[1]
    distancia = distancia[0]
    
    #Tipo Sangre
    tipoSangre = request.form['tipoSangre']
    cur.execute("SELECT * FROM tiposangre WHERE nombreTipoSangre = (%s)", [tipoSangre])
    tipoSangre = cur.fetchone()
    tipoSangre = tipoSangre[0]  

    #Talla Camisa
    tallaCamisa = request.form['tallaCamisa']
    cur.execute("SELECT * FROM tallacamisa WHERE tamañoTalla = (%s)", [tallaCamisa])
    tallaCamisa = cur.fetchone()
    tallaCamisa = tallaCamisa[0]

    #Categoria
    now = datetime.now()    
    fechaNacimiento = int(fechaNacimiento[0:4])
    edad = (int(format(now.year)) - int(fechaNacimiento))
    fechaNacimiento = request.form['fechaNacimiento']
    cur.execute("SELECT * FROM categorias WHERE rangoMin <= (%s) and rangoMax > (%s) and sexo = (%s) and distancia = (%s)", (edad,edad, sexo2, distancia2))
    categoria = cur.fetchone()
    categoria = categoria[0]
    
    #Código Equipo
    codigoEquipo = request.form["codigoGrupo"]
    cur.execute("SELECT * FROM equipos WHERE codigoEquipo = (%s)", [codigoEquipo])
    codigoEquipo = cur.fetchone()
    codigoEquipo = codigoEquipo[0]

    # cur.execute("SET NAMES utf8;")
    # cur.execute("SET CHARACTER SET utf8;")
    # cur.execute("SET character_set_connection=utf8;")
    sql = """INSERT INTO usuarios (nombreUsuario,apellidosUsuario,distancias_iddistancias,categorias_idcategorias,correoElectronico,
    tipoIdentificacion_idtipoIdentificacion,numeroIdentificacion,fechaNacimiento,sexo_idsexo,telefono,pais,departamento,ciudad, 
    tipoSangre_idtipoSangre,entidadSalud,tallaCamisa_idtallaCamisa,contactoEmergenciaNombre,contactoEmergenciaApellido,
    estadoInscripcion_idestadoInscripcion,estadoKit_idestadoKit,equipos_idequipos,fechaRegistro)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    values = (nombre,apellidos,str(distancia),str(categoria),email,str(tipoIdentificacion),numeroIdentificacion,
    fechaNacimiento,str(sexo),telefono,pais,departamento,ciudad,str(tipoSangre),entidadSalud,
    str(tallaCamisa),nombreContactoEmergencia,telefonoContactoEmergencia,(1),(1),str(codigoEquipo),str(now))
     
    cur.execute(sql, values)
    mysql.connection.commit()
    cur.execute("SELECT * FROM usuarios WHERE numeroIdentificacion = (%s) and correoElectronico = (%s)", (numeroIdentificacion, email))
    data = cur.fetchall()
    usuario = data[0]   
      
    if usuario:
      session["loggedin"] = True
      session["email"] = email
      session["nuip"] = numeroIdentificacion
      return  redirect(url_for("login"))
    #Limpiar session
    
    return redirect(url_for("registro"))


#Verificar código de equipo y número de identificación
@app.route("/verificacionRegistro", methods=["POST"])
def verificacionRegistro():
  if request.method == "POST":

    try:
      nuip = request.form["nuip"]
      cod = request.form["cod"]
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM equipos WHERE codigoEquipo = (%s)", [cod])
      dataCodigo = cur.fetchall()
      #print(dataCodigo[0])
            
      cur.execute("SELECT * FROM usuarios WHERE numeroIdentificacion = (%s)", [nuip])
      dataNuip = cur.fetchall()
      
      if dataCodigo and (not dataNuip):
        return jsonify({
          "status":200,
          "existeTodo": True,
          "existeNuip": True,
          "existeCod": True
        })
      elif dataNuip:
        return jsonify({
          "status":200,
          "existeTodo": False,
          "existeNuip": True,
          "existeCod": False
        })
      elif not dataCodigo:
        return jsonify({
          "status":200,
          "existeTodo": False,
          "existeNuip": False,
          "existeCod": False
        })
#Fin de try        
    except expression as identifier:
      return jsonify({
        "status": 500
      })
    
   
        


if __name__ == '__main__':
    app.run(debug=True, port=3000)