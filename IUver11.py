import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import gobject
import shelve
import os
import math
from time import gmtime, strftime, sleep
import sys
sys.path.append('./ModificarArchivo')
sys.path.append('./Sistema')
from ModificarArchivo import *
from Sistema import *



class Paciente:
	"""Clase Paciente contiene todos los atributos que son de 
	interes para el estudio"""
	def __init__(self):
		"""Datos basicos del paciente"""
		self.Nombre = ""
		self.Apellido = ""
		self.Edad = ""
		self.Sexo = "Masculino"
		"""Fecha de la carga del paciente dentro del software"""
		self.Fecha = strftime("%H : %M : %S", gmtime())
		"""Estudio a realizar sobre la muestra"""
		self.Test = "GLU"
		"""Numero identificatorio unico de paciente en estudio"""
		self.ID = 0
		"""Posicion dentro del carrusel de muestras"""
		self.Posicion = ""
		""" La prioridad tiene dos estados: Es "True" si se requiere 
		que el estudio para este paciente sea 
		realizado inmediatamente """
		self.Prioridad = False
		""" Boton desactivado de informe """
		self.Informe =  GdkPixbuf.Pixbuf.new_from_file('./Glade/botonnodisponible2.png')
		"""Resultado"""
		self.Resultado = "5 g/ml"
		"""Valor inicial de la barra de progreso"""
		self.Progreso = 1
		
	def Obtener_Lista(self):
		"""Retorna la lista de atributos del objeto paciente"""
		return [self,self.Nombre+" "+self.Apellido,self.ID,self.Fecha, 
		self.Edad,self.Test,self.Posicion,self.Prioridad,self.Progreso,self.Informe]
	def generar_Informe(self):
		"""Maneja los archivos. Crea, modifica y rescribe"""
		"""Crea archivo a partir de un modelo"""
		with open("./Reportes/Reporte-%s.txt" % str(self.ID), "w") as fw, open("./Reportes/Reporte","r") as fr:
			fw.writelines(l for l in fr if "" in l)
		fw.close()
		fr.close()
		"""Modifica el archivo creado con los datos del paciente """
		fileDir = os.path.dirname(os.path.realpath("/media/leandro/Datos/PROYECTO FINAL/SOFTWARE/IntegracionIUHW/Reportes/"))
		print fileDir
		with ModificarArchivo(os.path.join(fileDir,"Reportes/Reporte-"+str(self.ID)+".txt")) as fe: 
			fe.writeline("Paciente: " + self.Apellido + " "+ self.Nombre, 5)
			fe.writeline("Edad: " + self.Edad, 6)
			fe.write("Sexo: " + self.Sexo+"\n", 7)
			fe.write("Copa: " + self.Posicion, 8)
			fe.write(self.Test+ "			" + self.Resultado+ "				"+ "2,8 - 10 mg/mL")
		"""Abre el archivo"""
		reporte = open("./Reportes/Reporte-"+str(self.ID)+".txt","r")
		rep = reporte.read()
		reporte.close()
		return rep
 		
		
class App():
	"""Clase que crea la interfaz con el usuario"""
	def __init__(self):
		"""Contructor de la interfaz de usuario"""
		self.builder = Gtk.Builder()
		"""Carga del archivo .glade que contiene las 
		ventanas de la IU"""
		self.builder.add_from_file("./Glade/UIversion9.glade")
		"""Conexion de la senales especificadas en el archivo 
		.glade con las funciones de la presente clase"""
		self.builder.connect_signals(self)
		
		"""Variables utiles en la clase App"""
		
		"""Utilizada para almacenar las posiciones del carrusel ya 
		ocupadas"""
		self.Posiciones_ocupadas = []
		"""Identificador y contador de pacientes ingresados"""
		self.ID = 1

		"""Carga de los gif que aparecen en algunas pantallas"""
		animacion = GdkPixbuf.PixbufAnimation.new_from_file("./Glade/cargando.gif")
		self.imagen = Gtk.Image()
		self.imagen.set_from_animation(animacion)
		
		animacion2 = GdkPixbuf.PixbufAnimation.new_from_file("./Glade/Trabajando4.gif")
		self.imagen2 = Gtk.Image()
		self.imagen2.set_from_animation(animacion2)
		
		"""Carga de las imagenes que conforman el boton de informe"""
		self.botonInformeOFF = GdkPixbuf.Pixbuf.new_from_file('./Glade/botonnodisponible2.png')
		self.botonInformeON = GdkPixbuf.Pixbuf.new_from_file('./Glade/botondisponible.png')
		"""A continuacion se rescatan las ventanas principales alojadas 
		en el archivo .glade"""
		
		"""Bienvenida""" 
		self.w1 = self.builder.get_object("Bienvenida")
		self.box = self.builder.get_object("box2") 
		self.box.add(self.imagen)
		"""Cargando""" 
		self.w2 = self.builder.get_object("Cargando") 
		"""VENTANA DE MENUS PRINCIPALES"""
		self.w3 = self.builder.get_object("MenuPpal") 
		"""VENTANA DE INICIO DEL DIA1""" 
		self.w4 = self.builder.get_object("InicioDia1")
		self.w41 = self.builder.get_object("InicioDia2")
		"""DEMOSTRACION""" 
		self.w5 = self.builder.get_object("Demostracion1")
		self.w51 = self.builder.get_object("Demostracion2")
		self.box1 = self.builder.get_object("box7") 
		self.box1.add(self.imagen2) 
		"""VENTANA DE INICIO DE RUTINA"""
		self.w6 = self.builder.get_object("InicioRutina1")
		self.w61 = self.builder.get_object("Informe")
		self.w61a = self.builder.get_object("textoInforme")
		self.w6a = self.builder.get_object("cellrendererInforme")
		"""VENTANA DE ADMINISTRADOR"""
		self.w7 = self.builder.get_object("Administrador")
		self.w71 = self.builder.get_object("OperacionesManuales")
		self.w71a = self.builder.get_object("OM_Punta")
		self.w71b = self.builder.get_object("OM_Carruseles")
		self.w71c = self.builder.get_object("OM_Dilutor")
		self.w71d = self.builder.get_object("Warning_dialog")
		"""VENTANA DE FIN DE DIA"""	
		self.w8 = self.builder.get_object("FinDeDia1")
		self.w81 = self.builder.get_object("FinDeDia2")

		"""Luego se obtienen subestructuras dentro de las ventana de 
		Lista de pacientes (InicioRutina)"""
		self.Tree = self.builder.get_object("treeview")
		self.Lista = self.builder.get_object("Lista")

		"""Constantes que indican la posiciones del dato especificado
		 dentro de la lista creada"""
		self.LObject = 0
		self.LPaciente = 1
		self.LID = 2
		self.LFecha = 3
		self.LEdad = 4
		self.LTest = 5
		self.LPosicion = 6
		self.LPrioridad = 7
		self.LProgreso = 8
		self.LInforme = 9
		
		"""Apartado de configuracion del estilo de las ventanas: 
		Forma de botones, colores, etc.
		Se utiliza el lenguaje de programacion CSS"""
		screen = Gdk.Screen.get_default()
		css_provider = Gtk.CssProvider()
		css_provider.load_from_path('./Glade/prueba.css')
		context = Gtk.StyleContext()
		context.add_provider_for_screen(screen, css_provider,  
		Gtk.STYLE_PROVIDER_PRIORITY_USER)
		
		"""Muesta la primera ventana"""
		self.w1.show_all()
		self.autoanalizador = Sistema()

	def abrir_ventana_cargando(self, widget, data = None):
		"""Senal que se ejecuta al clickear sobre la primer ventana. 
		Oculta ventana anterior y abre la siguiente """
		#print("Bandera")
		
		#sleep(4)
		#self.w3.show_all()
		self.w1.hide()
		self.w2.show_all()
		#self.w2.show_all()
		
	def abrir_menu_principal(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre 
		la ventana anterior"""	
		#print("Bandera1")
		self.w2.hide()
		self.w3.show_all()
		
	def abrir_inicio_dia(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre
		la ventana anterior. Oculta la anterior y muestra una serie de 
		necesarios pasos que se realizan al iniciar el dia."""	
		#print("Bandera2")
		self.w3.hide()
		self.w4.show_all()
	def abrir_inicio_dia_2(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre
		la ventana anterior. Oculta la anterior y muestra una serie de 
		necesarios pasos que se realizan al iniciar el dia."""	
		#print("Bandera2")
		self.w4.hide()
		self.w41.show_all()
		
		self.autoanalizador.Inicio_dia()
	
	def abrir_demo(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre
		la ventana anterior. Oculta la anterior y abre una nueva en la
		que se solicitan que se realizen ciertas acciones para 
		iniciar una rutina demostrativa precargada."""
		self.w3.hide()
		self.w5.show_all()
	def abrir_demo2(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre
		la ventana anterior. Oculta la anterior y abre una nueva en la
		que se solicitan que se realizen ciertas acciones para 
		iniciar una rutina demostrativa precargada."""
		self.w5.hide()
		self.w51.show_all()
		
		self.autoanalizador.Demostracion()
		
	def abrir_inicio_rutina(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre
		la ventana anterior. Oculta la anterior y abre una nueva en la
		que se solicitan que se realizen ciertas acciones para 
		iniciar una rutina demostrativa precargada."""
		self.w3.hide()
		self.w6.show_all()
	def comenzar(self, widget, data=None):
		#Rutina comenzar
		autoanalizador.Rutina()	
	def abrir_administrador(self, widget, data=None):
		self.w3.hide()
		self.w7.show_all()
	def abrir_operaciones_manuales(self, widget, data=None):
		self.w7.hide()
		self.w71.show_all()
		self.w71d.run()
		self.w71d.hide()
	def abrir_OM_Punta(self, widget, data=None):
		self.w71a.show_all()
		self.w71.hide()
	def	mover_punta_a_estacion_muestra(self, widget, data=None):
		self.autoanalizador.mover_punta_a_estacion_muestra()
		print "Moviento punta a estación muestra"
	def	mover_punta_a_estacion_reactivos(self, widget, data=None):
		self.autoanalizador.mover_punta_a_estacion_reactivos()
		print "Moviento punta a estación muestra"
	def	mover_punta_a_estacion_lavado(self, widget, data=None):
		self.autoanalizador.mover_punta_a_estacion_lavado()
		print "Moviento punta a estación muestra"
	def	mover_punta_a_estacion_dispensado_de_mezcla(self, widget, data=None):
		self.autoanalizador.mover_punta_a_estacion_dispensado_de_mezcla()
		print "Moviento punta a estación muestra"
	def abrir_OM_Carruseles(self, widget, data=None):
		self.w71b.show_all()
		self.w71.hide()
	def mover_carrusel_M(self, widget, data=None):
		self.autoanalizador.mover_carrusel_M(data.get_text())
		print "Moviendo a posicion M"
	def mover_carrusel_R(self, widget, data=None):
		self.autoanalizador.mover_carrusel_R(data.get_text())
		print "Moviendo a posicion R"
	def abrir_OM_Dilutor(self, widget, data=None):
		self.w71c.show_all()
		self.w71.hide()
	def aspirar_volumen(self, widget, data):
		print data.get_text()
		self.autoanalizador.aspirar_volumen(data.get_text())
		
	def dispensar_volumen(self, widget, data):
		print data.get_text()
		self.autoanalizador.dispensar_volumen(data.get_text())
	
	def abrir_fin_dia(self, widget, data=None):
		"""Funcion que se ejecuta al presionar click sobre
		la ventana anterior. Oculta la anterior y muestra una serie de 
		necesarios pasos que se realizan al iniciar el dia."""
		self.w2.hide()
		self.w8.show_all()
	def abrir_fin_dia2(self, widget, data=None):
		self.w8.hide()
		self.w81.show_all()
		
		self.autoanalizador.Inicio_dia()
		
	def abrir_informe(self, widget, event):
		"""Senial que abre una ventana con el infome del paciente sele
		ccionado"""
		path_array = widget.get_path_at_pos(event.x, event.y)
		path = path_array[0][0]
		col = path_array[1]
		col_title = col.get_title()
		if (col_title =='Informe de Resultado'):
			selection = self.Tree.get_model()
			iter_selection = selection.get_iter(path)
			Paciente = self.Lista.get_value(iter_selection, 0)
			Paciente.Progreso = 100
			rep = Paciente.generar_Informe()
			self.w61a.get_buffer().set_text(rep)
			self.Lista.set_value(iter_selection, self.LInforme, self.botonInformeON)
			self.Lista.set_value(iter_selection, self.LProgreso, 100)
			self.w61.show_all()
			
		
	def on_Dlg_DatosPaciente_clicked(self, widget, data=None):
		"""Senal que se activa dentro de la ventana de inicio rutina 
		#al presionar el boton de anadir paciente. Se abre una ventana 
		de dialogo con los campos a completar sobre este nuevo 
		paciente"""
		
		DialogoAdd = Ventana_dialogo()
		"""Creacion de nuevo objeto de la clase Ventana_dialogo, 
		que maneja la informacion obtenida de los cuadros de dialogos"""
		
		Respuesta, Nuevo_paciente = DialogoAdd.run()
		"""La funcion run() de la clase Ventana dialogo retorna la 
		#respuesta (SI/NO guardar nuevo paciente) y un objeto del tipo 
		paciente que contiene los datos ingresados"""
		print Respuesta
		print Nuevo_paciente
		
		if Respuesta == -5:
			self.ID += 1
			print Nuevo_paciente.ID
			if (Nuevo_paciente.ID == 0):
				Nuevo_paciente.ID = self.ID
				"""Asignacion del ID UNICO"""
			if (Nuevo_paciente.Prioridad):
				"""Si la prioridad es True, se ubica al paciente primero 
				en la lista de trabajos"""
				self.Lista.insert(0,Nuevo_paciente.Obtener_Lista())
			else:
				self.Lista.append(Nuevo_paciente.Obtener_Lista())
				"""Si la prioridad es False, se coloca al nuevo paciente
				al final de la lista"""
				
				
	def on_Dlg_Editar_clicked(self, widget, data=None):
		"""Se activa al seleccionar un paciente de la lista y clickear 
		en el boton EDITAR, en caso de que quiera modificarse algun 
		valor ingresado."""

		selection = self.Tree.get_selection()
		model, selection_iter = selection.get_selected()
		"""Se toman los datos existentes y se precargan en la misma
		ventana de dialogo que se genera al carrgar un nuevo paciente"""
		if (selection_iter):
			Paciente_Seleccionado = self.Lista.get_value(selection_iter,
			 0) 
			DialogoAdd = Ventana_dialogo(Paciente_Seleccionado)
			Respuesta, Nuevo_paciente = DialogoAdd.run()
			
			if (Respuesta == -5):
				self.Lista.set(selection_iter,self.LObject,Nuevo_paciente
							, self.LPaciente, (Nuevo_paciente.Nombre+
							" "+Nuevo_paciente.Apellido)
							, self.LID, Nuevo_paciente.ID
							, self.LFecha, Nuevo_paciente.Fecha
							, self.LEdad, Nuevo_paciente.Edad
							, self.LTest, Nuevo_paciente.Test
							, self.LPosicion, Nuevo_paciente.Posicion
							, self.LPrioridad, Nuevo_paciente.Prioridad)
							
				if (Nuevo_paciente.Prioridad):
					self.Lista.move_after(selection_iter, None) 
				else:
					self.Lista.move_before(selection_iter, None)
										
	def on_eliminar_paciente(self, widget, data=None):
		"""Elimina el paciente seleccionado de la lista de trabajos"""
		selection = self.Tree.get_selection()
		model, selection_iter = selection.get_selected()
		Pos_eliminada = self.Lista.get_value(selection_iter, self.LPosicion)
		self.Posiciones_ocupadas.remove(Pos_eliminada)
		self.Lista.remove(selection_iter)
	def on_ocultar(self, widget, data=None):
		self.w61.hide()
		self.w71a.hide()
		self.w71b.hide()
		self.w71c.hide()
		self.w3.show_all()
				
	def volver_menu(self, widget, data = None):
		"""Retorno al menu principal"""
		self.w4.hide()
		self.w41.hide()
		self.w5.hide()
		self.w51.hide()
		self.w6.hide()
		self.w7.hide()
		self.w71.hide()
		self.w8.hide()
		self.w81.hide()

		self.w3.show_all()
			
	def cerrar_ventana(self, widget):
		Gtk.main_quit()

class Ventana_dialogo(App):
	"""Clase encargada del manejo de las ventanas de dialogo creadas
	luego de clickear en anadir paciente o editar paciente"""
	def __init__(self, Paciente0=None):
		"""Creacion del contrusctor y posterior obtencion de los objetos
		 ventana disenados dentro del archivo .glade """
		self.builder2 = Gtk.Builder()
		self.builder2.add_from_file("./Glade/Dialogo1v05.glade")
		self.builder2.connect_signals(self)

		"""Sentencia condicional necesaria para diferencia la creacion
		de un nuevo objeto paciente de uno que se quiera modificar"""
		if (Paciente0):
			self.Paciente0 = Paciente0
		else:
			self.Paciente0 = Paciente()
	def capturar_codigo(self, widget, data=None):
		self.Paciente0.ID = int(widget.get_text())
		#print widget.get_text()
		self.result = -5
		#self.on_definir_clicked(widget)
		#print self.Paciente0.ID
		
		for pos in Aplicacion.Posiciones_ocupadas:
			posicion = "pos"+str(Aplicacion.Posiciones_ocupadas[Aplicacion.Posiciones_ocupadas.index(pos)])
			Objposicion = self.builder2.get_object(posicion)
			Objposicion.set_active(True)
			if self.Paciente0.Posicion in Aplicacion.Posiciones_ocupadas:
				Objposicion.set_active(False)
				Aplicacion.Posiciones_ocupadas.remove(self.Paciente0.Posicion)
		self.Posiciones.show_all()
			
	def on_buttonsexo_toggled(self, widget, data=None):
		"""Senal producida al presionar el togglebutton correspondiente
		al sexo del paciente ingresado"""
		
		if not (widget.get_label() == "Masculino"):
			self.Paciente0.Sexo = "Femenino"
			print "Sexo"
		else:
			self.Paciente0.Sexo = "Masculino"
	
	def on_prioridad_toggled(self, widget, data=None):
		"""Senal originada al presionar sobre el checkbutton que define 
		si el paceinte ingresado debe ser o no procesado de urgencia"""
		if (widget.get_active()):
			self.Paciente0.Prioridad = True
			print self.Paciente0.Prioridad
		else:
			self.Paciente0.Prioridad = False
			
	def on_combobox1_changed(self, widget, data=None):
		"""Seleccion del test a realizara a traves de una lista 
		desplegable con test preestablecidos"""
		self.Paciente0.Test = self.Tests[self.ComboBox.get_active()][0]
	
	def on_definir_clicked(self, widget, data=None):
		"""funcion ejecutada al presionar el boton de Definir ubicacion
		#dentro del carrusel de muestras. Se abre una nueva ventana que
		representa el carrusel con todas sus posiciones marcando las que
		ya se encuentran ocupadas"""
		for pos in Aplicacion.Posiciones_ocupadas:
			posicion = "pos"+str(Aplicacion.Posiciones_ocupadas[Aplicacion.Posiciones_ocupadas.index(pos)])
			Objposicion = self.builder2.get_object(posicion)
			Objposicion.set_active(True)
			if self.Paciente0.Posicion in Aplicacion.Posiciones_ocupadas:
				Objposicion.set_active(False)
				Aplicacion.Posiciones_ocupadas.remove(self.Paciente0.Posicion)
		self.Posiciones.show_all()
	
	def on_posicion_clicked(self, widget , data=None):
		"""senal al presionar sobre una de las posiciones del carrusel
		de muestras"""
		if widget.get_name() in Aplicacion.Posiciones_ocupadas:
			#print "POSICION OCUPADA"
			widget.set_active(True)
					
		else:
			self.Paciente0.Posicion = widget.get_name()
			Aplicacion.Posiciones_ocupadas.append(self.Paciente0.Posicion)
			widget.set_active(True)
			#print Aplicacion.Posiciones_ocupadas
			self.Posiciones.hide()
			self.Dlg2.destroy()
			

	def run(self):
		"""Esta funcion crea las ventanas de dialogo: 
		Elegir metodo de carga de datos y subisguientes etapas para 
		cargar un nuevo paciente"""
		self.Dlg0  = self.builder2.get_object("Dialogo0")
		self.Dlg1  = self.builder2.get_object("Dialogo1")
		self.Dlg2  = self.builder2.get_object("lectorCodigodeBarras")
		self.Codigo = self.builder2.get_object("Codigo")
		self.Tests = self.builder2.get_object("Tests")
		self.ComboBox = self.builder2.get_object("combobox1")
		self.dNombre = self.builder2.get_object("Nombre")
		self.dNombre.set_text(self.Paciente0.Nombre)
		self.dApellido = self.builder2.get_object("Apellido")
		self.dApellido.set_text(self.Paciente0.Apellido)
		self.dEdad = self.builder2.get_object("Edad")
		self.dEdad.set_text(self.Paciente0.Edad)
		self.dSexo = self.builder2.get_object("Sexo")
		self.dPrioridad = self.builder2.get_object("Prioridad")
		self.dPrioridad.set_active(self.Paciente0.Prioridad)
		self.Posiciones = self.builder2.get_object("PosicionesMuestras")
		
		"""ventana de dialogo que consulta sobre el metodo de carga:
		MANUAL O POR CODIGO DE BARRAS"""
		self.result0 = self.Dlg0.run()
		self.Dlg0.destroy()
		if(self.result0 == 1):
			"""la respuesta 1 corresponde al boton MANUAL"""
			self.result = self.Dlg1.run()
			print self.result
			"""Se obtienen los valores de los campos ingresados y se 
		almancenan en el objeto paciente"""
			self.Paciente0.Nombre = self.dNombre.get_text()
			self.Paciente0.Apellido = self.dApellido.get_text()
			self.Paciente0.Edad = self.dEdad.get_text()
			self.Dlg1.hide()
			return self.result, self.Paciente0 
		else:
			print "LECTURA POR COGIDO DE BARRAS"
			self.result = -5
			self.Dlg2.run()
			#self.on_definir_clicked(self.Posiciones)
			
			#print self.Paciente0
			return self.result, self.Paciente0
			self.Dlg2.destroy()

		"""retorna el resultado del dialogo (ACEPTAR/CANCELAR)Y EL 
		objeto paciente cargado"""
		
		
		
if __name__ == "__main__":
	Aplicacion = App()
	Gtk.main()

