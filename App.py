# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect,url_for, flash, session, json, jsonify, logging
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import date
from datetime import datetime
app = Flask(__name__)

#Conficuración de sesion . permanete
@app.before_request
def session_management():
  session.permanent = True
  
#Mysql connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "piedradelcanada"

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
    cur.execute("SELECT * FROM usuarioconsulta WHERE correoElectronico = (%s) and contraseña = (%s)", (email, contraseña))
    usuario = cur.fetchone()
    if usuario:
      cur.execute("SELECT * FROM usuarios")
      usuarios = cur.fetchall()

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
  cur.execute("SELECT * FROM usuarioconsulta WHERE correoElectronico = (%s) and contraseña = (%s)", (email, contraseña))
  usuario = cur.fetchone()
  if usuario:
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    
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

@app.route("/confirmarPago/<string:id>", methods=["POST"])
def confirmarPago(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET estadoIncripcion=(%s) WHERE idusuarios = (%s)", ("pago", id))
    mysql.connection.commit()
    messages = []
    messages.append("confirmarPago")
    messages.append("¡Se ha guardado el pago correctamente!")
    session["messages"] = messages
    
    return redirect(url_for("loginAdmin"))

@app.route("/entregarKit/<string:id>", methods=["POST"])
def entregarKit(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET estadoKit=(%s) WHERE idusuarios = (%s)", ("Entregado", id))
    mysql.connection.commit()
    messages = []
    messages.append("confirmarPago")
    messages.append("¡Se ha cambiado el estado de entrega del kit correctamente!")
    session["messages"] = messages
    
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
  messages = []
  session['login'] = "active"
  session['registro'] = ""
  if session["loggedin"] == True:
    nuip = session["nuip"]
    email = session["email"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE correoElectronico = (%s) and numeroIdentificacion = (%s)", (email, nuip))
    usuario = cur.fetchone()
    if usuario:
      now = datetime.now()
      print(usuario[8])
      fechaNacimiento = str(usuario[8])
      fechaNacimiento = fechaNacimiento[0:4]
      print(fechaNacimiento)
      edad = (int(format(now.year)) - int(fechaNacimiento))
      
      usuario = list(usuario)
      usuario.append(edad)
      usuario = tuple(usuario)

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
      
      now = datetime.now()
      print(usuario[8])
      fechaNacimiento = str(usuario[8])
      fechaNacimiento = fechaNacimiento[0:4]
      print(fechaNacimiento)
      edad = (int(format(now.year)) - int(fechaNacimiento))
      
      usuario = list(usuario)
      usuario.append(edad)
      usuario = tuple(usuario)
      
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
  session['registro'] = "active"
  session['login'] = ""
  messages = []
  if session["loggedin"] == True:
    return  redirect(url_for("login"))
    
  messages.append("0")
  messages.append("1")
  
  return render_template("auth/registro.html", messages=messages)

#Método de Registro
@app.route("/registro", methods=["POST"])
def registroUsuario():
  if request.method == "POST":
    estadoInscripcion = 'registrado'
    estadoKit = "Sin entregar"
    distancia = request.form['distancia']
    nombre = request.form['nombre']
    apellidos = request.form['apellido']
    email = request.form['email']
    tipoDocumento = request.form['tipoIdentificacion']
    numeroIdentificacion = request.form['numeroIdentificacion']
    fechaNacimiento = request.form['fechaNacimiento']
    sexo = request.form['sexo']
    telefono = request.form['telefono']
    pais = request.form['pais']
    departamento = request.form['departamento']
    ciudad = request.form['ciudad']
    tipoSangre = request.form['tipoSangre']
    seguroMedico = request.form['seguroMedico']
    tallaCamisa = request.form['tallaCamisa']
    nombreContactoEmergencia = request.form['nombreContactoEmergencia']
    telefonoContactoEmergencia = request.form['numeroContactoEmergencia']
    
    if distancia == '10K':
        valorPagar = 55000
    elif distancia == '21K':
        valorPagar = 65000
    else:
        valorPagar = 75000
    
    cur = mysql.connection.cursor()
    
    codigoGrupo = request.form["codigoGrupo"]

    cur.execute("SELECT * FROM codigosequipos WHERE codigo = (%s)", [codigoGrupo])
    nombreEquipo = cur.fetchall()
    cur.execute("SET NAMES utf8;")
    cur.execute("SET CHARACTER SET utf8;")
    cur.execute("SET character_set_connection=utf8;")
    cur.execute("""INSERT INTO usuarios (nombreUsuario, apellidosUsuario, distancia, valorPagar, correoElectronico, tipoIdentificacion, 
    numeroIdentificacion, fechaNacimiento, sexo, telefono, pais,departamento, ciudad, tipoSangre, entidadSalud, tallaCamisa,
    contactoEmergenciaNombre, contactoEmergenciaTelefono, estadoIncripcion, estadoKit,grupo) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
    (nombre,apellidos,distancia,valorPagar,email,tipoDocumento,numeroIdentificacion, 
    fechaNacimiento,sexo,telefono,pais,departamento,ciudad,tipoSangre,seguroMedico,
    tallaCamisa,nombreContactoEmergencia,telefonoContactoEmergencia,estadoInscripcion,estadoKit,nombreEquipo[0][1]))
    mysql.connection.commit()
    cur.execute("SELECT * FROM usuarios WHERE numeroIdentificacion = (%s) and correoElectronico = (%s)", (numeroIdentificacion, email))
    data = cur.fetchall()
    usuario = data[0]
    
    if usuario:

      now = datetime.now()
      print(usuario[8])
      fechaNacimiento = str(usuario[8])
      fechaNacimiento = fechaNacimiento[0:4]
      print(fechaNacimiento)
      edad = (int(format(now.year)) - int(fechaNacimiento))
      
      usuario = list(usuario)
      usuario.append(edad)
      usuario = tuple(usuario)

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
      cur.execute("SELECT * FROM codigosequipos WHERE codigo = (%s)", [cod])
      dataCodigo = cur.fetchall()
            
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