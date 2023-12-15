import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk #pip install pillow
import pygame
import time
import threading
import os
import random
import serial # conectar a Raspberry Pi Pico
import json


# Variables
size_area_juego = {"width":600,"height":600}
matriz_cuadros = []
minutos, segundos = 1, 30
colocar_bloques = True
# Variables de posición del círculo
x_tanque = 286
y_tanque = 15
# Dirección actual del tanque
direccion_tanque = 'down'
turno_atacante = False
puntos = 0
th = False
pausar_cronometro = True
# Bandera para saber si hay una bomba en la pantalla
bomba_en_movimiento = False
tiempo_inicial_atacante = 0
recorrido_x, recorrido_y = 0, 0
tipo_bomba = ""
Rpi_reading = True
dt=""
pausa = ""





# Ventana Principal
def ventanaJuego(ventanaPrincipal, usr1, usr2, rol, canva1, canal, tiempo_turno, ventanas_de_ayuda, text1, text2, 
	salon):
	global minutos, segundos, tiempo_inicial_atacante, Rpi_reading, pausa
	minutos, segundos = tiempo_turno//60, tiempo_turno%60
	tiempo_inicial_atacante = tiempo_turno
	try:
		Rpi = serial.Serial(port = "COM6", baudrate=115200)
		try:
			Rpi.Open()
			print("conectado")
		except:
			if (Rpi.isOpen()):
				print("conectado")
			else:
				print("no conectado")
	except serial.SerialException:
		Rpi_reading = False
		print("no hay conexion seial")
	
	#___________________
	#					\ Musica \___________________

	path = "./musica"
	all_songs = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
	del all_songs[all_songs.index("./musica\\winner_default.mp3")]

	random_song = random.choice(all_songs)
	pygame.mixer.init()
	musica_fondo = pygame.mixer.Sound(random_song)
	pygame.mixer.Channel(3).play(musica_fondo, loops=-1)
	musica_fondo.set_volume(0.7)


	#_______________
	#				\ Pantalla de juego y cuadricula \_______________

	# Contiene los bloque, cronometro y area de juego
	canva_juego = tk.Canvas(ventanaPrincipal, width = 1550, height = 800)
	canva_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


	# Fondo de pantalla
	img_fondo = Image.open("./imagenes/fondo2.png")
	resize_image = img_fondo.resize((1700,900))
	imgF = ImageTk.PhotoImage(resize_image)

	fondoJ = tk.Label(canva_juego, image = imgF)
	fondoJ.img_fondo = imgF
	fondoJ.place(x=0, y=0)

	# volver a pantalla inicial

	#_______________
	#				\ Pausar juego \_______________

	#boton para pausar en la pantalla de juego
	pausar=tk.Button(canva_juego, text= 'Pausa', font= 'Fixedsys 16', bg='grey',fg='black', 
		command=lambda:pausar_juego())
	pausar.place(x=100,y=30)

	def continuar_juego():
		global pausar_cronometro, pausa
		pausar_cronometro = False
		pausa.place_forget()
		for child in canva_juego.winfo_children():
			child.configure(state=tk.NORMAL)
		if not turno_atacante:
			area_juego.bind("<Button-1>", colocarBloques)
		else:
			ventanaPrincipal.bind("<Key>", manejar_evento_teclado)

	def pausar_juego():
		global pausar_cronometro, pausa
		pausar_cronometro = True
		for child in canva_juego.winfo_children():
			child.configure(state=tk.DISABLED)
		if not turno_atacante:
			area_juego.unbind("<Button-1>")
		else:
			ventanaPrincipal.unbind("<Key>")
		#pausar.configure(state=tk.DISABLED)
		# ventana de pausa
		pausa.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

		continuar=tk.Button(pausa, text= 'Continuar partida', font= 'Fixedsys 20', bg='grey',fg='black', 
			command=lambda:continuar_juego())
		continuar.place(relx=0.5, y=70, anchor=tk.CENTER )

		controles=tk.Button(pausa, text= 'Ayuda', font= 'Fixedsys 20', bg='grey',fg='black', 
			command=lambda:ventanas_de_ayuda(text1, text2))
		controles.place(relx=0.5, y=150, anchor=tk.CENTER )

		S_fama=tk.Button(pausa, text= 'Salón de la fama', font= 'Fixedsys 20', bg='grey',fg='black', 
			command=lambda:salon())
		S_fama.place(relx=0.5, y=230, anchor=tk.CENTER )

		guardar=tk.Button(pausa, text= 'Guardar', font= 'Fixedsys 20', bg='grey',fg='black', 
			command=lambda:guardar_partida(bloques_colocados))
		guardar.place(relx=0.5, y=310, anchor=tk.CENTER )

		volver_inicio=tk.Button(pausa, text= 'Volver a inicio', font= 'Fixedsys 20', bg='grey',fg='black', 
			command=lambda:ir_a_inicio())
		volver_inicio.place(relx=0.5, y=390, anchor=tk.CENTER )



	def ir_a_inicio():
		global pausar_cronometro,turno_atacante, th, recorrido_x, recorrido_y,minutos, segundos, direccion_tanque, colocar_bloques,x_tanque,y_tanque, puntos, tiempo_inicial_atacante, Rpi_reading
		th = threading.Thread(target=cronometro)
		Rpi_reading = False
		pausar_cronometro = True
		turno_atacante = False
		colocar_bloques = True
		direccion_tanque = 'down'
		x_tanque = 286
		y_tanque = 15
		canva_juego.destroy()
		canva1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		pygame.mixer.Channel(3).stop()

		time.sleep(1.2)

		Rpi.close()
		minutos, segundos = 1, 30
		pausar_cronometro = False
		Rpi_reading = True
		puntos = 0
		tiempo_inicial_atacante = 0
		recorrido_x, recorrido_y = 0, 0


	# area de juego donde se van a colocar y los bloques
	area_juego = tk.Canvas(canva_juego, width = size_area_juego["width"], height = size_area_juego["height"], 
		bg = "#2a2a2a", highlightthickness=0
	)
	area_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

	# cuadricula de area de juego
	dim_cuadricula = (20, 20)
	dim_cuadros = {	"x1":0, "y1":0, 
					"x2":size_area_juego["width"]//dim_cuadricula[0], 
					"y2":size_area_juego["height"]//dim_cuadricula[1]}

	for i in range(1,dim_cuadricula[0]+1):
		fila = [] # para vaciar lista en la que se agregaran los elementos a agregar en "matriz_cuadros"
		for j in range(1,dim_cuadricula[1]+1):
			cuadro = area_juego.create_rectangle(
				dim_cuadros["x1"]+(j-1)*dim_cuadros["x2"], dim_cuadros["y1"]+(i-1)*dim_cuadros["y2"], 
				dim_cuadros["x2"]*j, dim_cuadros["y2"]*i, 
				fill="#161616", outline="ivory4"
			)
			fila.append(cuadro)
		matriz_cuadros.append(fila)



	#_______________
	#				\ Ventana ayuda \_______________
	
	
	#para que al salir de la ventana de ayuda regrese a la primera pagina de la misma
	def salir_ventana_ayuda(ayuda_widgets):
		ayuda_widgets["ayuda"].pack_forget()
		ayuda_widgets["controles2"].place(relx=0.5, y=700, anchor=tk.N)
		ayuda_widgets["btn_previous"].configure(state=tk.DISABLED)
		ayuda_widgets["btn_next"].configure(state=tk.NORMAL)

	#_______________
	#				\ Nombres de jugadores en pantalla de juego \_______________

	def mostrar_etiqueta_jugador():
		jugador1 = tk.Label (canva_juego, text = usr1[0], font = "Fixedsys 30 ",bg= "grey", 
			fg='black', relief= 'raised'
		)
		jugador1.place(x=200, y=100)
		imgJ1 = Image.open(usr1[5])
		resize_imgJ1 = imgJ1.resize((50,50))
		imgJ1 = ImageTk.PhotoImage(resize_imgJ1)

		label_imgJ1 = tk.Label(canva_juego, image = imgJ1, height=50, width=50, borderwidth=0, 
			highlightthickness=0
		)
		label_imgJ1.imgJ1 = imgJ1
		label_imgJ1.place(x=150, y=100)

		jugador2 = tk.Label (canva_juego, text = usr2[0], font = "Fixedsys 30 ",bg= "grey", 
			fg='black', relief= 'raised'
		)
		jugador2.place(x=1200, y=100)
		imgJ2 = Image.open(usr2[5])
		resize_imgJ2 = imgJ2.resize((50,50))
		imgJ2 = ImageTk.PhotoImage(resize_imgJ2)

		label_imgJ2 = tk.Label(canva_juego, image = imgJ2, height=50, width=50, borderwidth=0, 
			highlightthickness=0
		)
		label_imgJ2.imgJ2 = imgJ2
		label_imgJ2.place(x=1150, y=100)

	mostrar_etiqueta_jugador()

	#_______________________
	#						\ Inventario \__________________________
	'''
	- Se crea de forma iterativa usando la informacion de la matriz bloques
	- Cada fila es un objeto del inventario
	
	bloques[i][0]: nombre del bloque
	bloques[i][1]: cantidad restante
	bloques[i][2]: posicion en pantalla en la que se colocará ese bloque para crear el inventario
	bloques[i][3]: dirección de la imagen que corresponde al bloque
	bloques[i][4]: referencia al widget guardado en una lista
	'''


	# La lista vacía en la posicion 4 de cada bloque se remplazará con la referencia al bloque en el inventario
	bloques = [
		["madera",	10,	(160, 350),	"./imagenes/madera.png"	,	[]	],
		["concreto",10,	(272, 350), "./imagenes/concreto1.png",	[]	],
		["acero", 	10,	(216, 350), "./imagenes/acero1.png"	,	[]	],
		["aguila", 	1,	(328, 350), "./imagenes/eagle.png"	,	[]	],
	]

	destruidos = {
		"madera":	[0,	(1150, 350),	"./imagenes/madera.png"	,	[]	],
		"concreto":	[0,	(1250, 350),	"./imagenes/concreto1.png",	[]	],
		"acero":	[0,	(1200, 350), 	"./imagenes/acero1.png"	,	[]	],
		"aguila":	[0,	(1300, 350), 	"./imagenes/eagle.png"	,	[]	],
	}
	bombas_restantes = {
		"agua":		[5,	(1150, 425),	"./tanque/bola_agua.png",	[]	],
		"fuego":	[5,	(1200, 425),	"./tanque/bola_fuego.png",	[]	],
		"bomba":	[5,	(1250, 425), 	"./tanque/bomba.png",		[]	],
	}

	# mostrar bloques disponibles
	var = tk.IntVar(canva_juego, 3) # Usado para guardar el valor de el Radiobutton seleccionado

	label_inventario = tk.Label(canva_juego, text="Inventario", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
	label_inventario.place(x=160, y=270)
	for bloque in bloques:
		img_bloque = Image.open(bloque[3]) 
		resize_image = img_bloque.resize((50,50)) # ajusta tamaño de imagen
		img = ImageTk.PhotoImage(resize_image)

		index = bloques.index(bloque) # se obtiene el numero de la fila del bloque para usarlo como value del Radiobutton
		Rbtn_bloque = tk.Radiobutton(canva_juego, text=bloque[1], variable=var, value=index, 
			font="Fixedsys 20",image = img, height=50, width=50, borderwidth=0,compound="center", 
			 indicatoron=0, relief=tk.FLAT, selectcolor="red"
		)
		Rbtn_bloque.img_bloque = img
		Rbtn_bloque.place(x=bloque[2][0], y=bloque[2][1])
		bloque[4] = [Rbtn_bloque] # Agrega referencia del widget a bloques[i][4]

	# mostrar bloques destruidos

	label_destruidos = tk.Label(canva_juego, text="Bloques\ndestruidos", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
	label_destruidos.place(x=1150, y=220)
	for bloque in destruidos:
		img_bloque = Image.open(destruidos[bloque][2]) 
		resize_image = img_bloque.resize((50,50)) # ajusta tamaño de imagen
		img = ImageTk.PhotoImage(resize_image)

		label_bloque_destruido = tk.Label(canva_juego, text=destruidos[bloque][0], font="Fixedsys 20",image = img, 
			height=50, width=50, borderwidth=0,compound="center", relief=tk.FLAT
		)
		label_bloque_destruido.img_bloque = img
		label_bloque_destruido.place(x=destruidos[bloque][1][0], y=destruidos[bloque][1][1])
		destruidos[bloque][3] = [label_bloque_destruido] # Agrega referencia del widget a bloques[i][3]


	label_puntos = tk.Label(canva_juego, text=f"Puntos:{puntos}", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
	label_puntos.place(x=1150, y=500)

	#mostrar bombas en inventario

	for bomba in bombas_restantes:
		img_bomba = Image.open(bombas_restantes[bomba][2]) 
		resize_image = img_bomba.resize((50,50)) # ajusta tamaño de imagen
		img = ImageTk.PhotoImage(resize_image)

		label_bomba = tk.Label(canva_juego, text=bombas_restantes[bomba][0], font="Fixedsys 20", image = img, 
			height=50, width=50, borderwidth=0,compound="center", relief=tk.FLAT
		)
		if bomba == "bomba":
			label_bomba.configure(fg="white")
		label_bomba.img_bomba = img
		label_bomba.place(x=bombas_restantes[bomba][1][0], y=bombas_restantes[bomba][1][1])
		bombas_restantes[bomba][3] = [label_bomba] # Agrega referencia del widget a bloques[i][4]




	pausa = tk.Canvas(canva_juego, width=700, height=450, bg="#a2a2a2")
	#_______________________
	#						\ Colocar bloques \__________________________
	"""
	- Los bloques se colocan con un label que tiene una imagen
	- La imagen corresponde al bloque seleccionado en el inventario (radiobutton)
	- Los bloques colocados se guardaran en una lista la cual su nombre corresponde al bloque que guardará
	- La lista de cada bloque se usará para luego poder removerlos de la pantalla
	"""
	#listas para guardar cada uno de los labels se
	bloques_colocados = {
		"madera":	[[],[],[]],
		"concreto":	[[],[],[]],
		"acero":	[[],[],[]],
		"aguila":	[[],[],[]]
	}
	# Colocar bloques
	def colocarBloques(event):
		
		if bloques[var.get()][1] > 0 and colocar_bloques: 
			item = area_juego.find_closest(event.x, event.y)
			def find_item_location(item, matriz_cuadros):
				for i in range(len(matriz_cuadros)):
					for j in range(len(matriz_cuadros[i])):
						if matriz_cuadros[i][j] == item[0]:
							coords = area_juego.coords(matriz_cuadros[i][j])
							return coords

				return None

			''' Referencia de los bloques de inventario creados se guarda en la posicion 3 de la lista "bloques"
				Se usa el valor del RadioButton seleccionado para cambiar el texto del bloque que se seleccionó'''
			selected = bloques[var.get()][4][0]
			bloques[var.get()][1]-=1
			selected.configure(text=bloques[var.get()][1])


			ubicacion = find_item_location(item, matriz_cuadros)
			image = Image.open(bloques[var.get()][3])
			resize_image = image.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
			img = ImageTk.PhotoImage(resize_image)

			label = tk.Label(area_juego, image = img, height=dim_cuadros["x2"]-5, width=dim_cuadros["y2"]-5)
			label.image = img
			if ubicacion == None:
				messagebox.showerror("Imposible de colocar.", "El bloque no puede ser colocado en esa posición.")
			else:
				label.place(x=int(ubicacion[0])+1, y=int(ubicacion[1])+1)
				label.bind("<Button-1>", lambda event, l=label: removerBloque(event,l))
			# añade el label a la lista madera, concreto, acero y aguila, segun corresponda
			if bloques[var.get()][0] == "madera":
				bloques_colocados["madera"][0].append(ubicacion)
				bloques_colocados["madera"][1].append(label)
				bloques_colocados["madera"][2].append(2)
			elif bloques[var.get()][0] == "concreto":
				bloques_colocados["concreto"][0].append(ubicacion)
				bloques_colocados["concreto"][1].append(label)
				bloques_colocados["concreto"][2].append(6)
			elif bloques[var.get()][0] == "acero":
				bloques_colocados["acero"][0].append(ubicacion)
				bloques_colocados["acero"][1].append(label)
				bloques_colocados["acero"][2].append(3)
			else :
				bloques_colocados["aguila"][0].append(ubicacion)
				bloques_colocados["aguila"][1].append(label)
				bloques_colocados["aguila"][2].append(2)
		elif not colocar_bloques:
			messagebox.showinfo(title="Sin tiempo", message="El tiempo para colocar bloques a acabado")
		else:
			if bloques[var.get()][0] == "aguila":
				messagebox.showinfo(title=f"Aguila ya colocada.", 
					message=f"El aguila ya fue colocada en el area de juego."
				)
			else:	
				messagebox.showinfo(title=f"Sin {bloques[var.get()][0]}", 
					message=f"Ya no tiene más bloques de {bloques[var.get()][0]}"
				)

	#_______________________
	#						\ Remover bloques \__________________________
	"""
	- Se usa las listas madera, concreto, acero y aguila, donde se guardaron los bloques colocados
	- Cada label de los bloques tiene un bind con un callback hacia esta funcion (removerBloque)
	- El bind se activa al hacer clic sobre alguno de los bloques colocados
	- Los labels pasan como parametro a la funcion la referencia a ellos mismos
	- La función busca si la referencia al label pasada por el bind está en alguna de las listas de bloques
	- Luego se debe actualizar la cantidad en el inventario y eliminarlo de la lista correspondiente  
	"""
	def removerBloque(event, label):
		if colocar_bloques:
			if label in bloques_colocados["madera"][1]:
				bloques[0][1]+=1
				bloques[0][4][0].configure(text=bloques[0][1])
				i = bloques_colocados["madera"][1].index(label)
				del bloques_colocados["madera"][0][i]
				del bloques_colocados["madera"][1][i]
				del bloques_colocados["madera"][2][i]
			elif label in bloques_colocados["concreto"][1]:
				bloques[1][1]+=1
				bloques[1][4][0].configure(text=bloques[1][1])
				i = bloques_colocados["concreto"][1].index(label)
				del bloques_colocados["concreto"][0][i]
				del bloques_colocados["concreto"][1][i]
				del bloques_colocados["concreto"][2][i]
			elif label in bloques_colocados["acero"][1]:
				bloques[2][1]+=1
				bloques[2][4][0].configure(text=bloques[2][1])
				i = bloques_colocados["acero"][1].index(label)
				del bloques_colocados["acero"][0][i]
				del bloques_colocados["acero"][1][i]
				del bloques_colocados["acero"][2][i]
			elif label in bloques_colocados["aguila"][1]:
				bloques[3][1]+=1
				bloques[3][4][0].configure(text=bloques[3][1])
				i = bloques_colocados["aguila"][1].index(label)
				del bloques_colocados["aguila"][0][i] 
				del bloques_colocados["aguila"][1][i] 
				del bloques_colocados["aguila"][2][i] 
			label.destroy()
		else:
			messagebox.showinfo(title="Sin tiempo.", message="Ya no puede remover los bloques")
	



	#_______________________
	#						\Regenerar bloques \__________________________

	bloques_regen = {
		"madera":	[[],[],[]],
		"concreto":	[[],[],[]],
		"acero":	[[],[],[]],
		"aguila":	[[],[],[]]
	}


	def regenerar_bloques():
		ruta_img_bloque = {
			"madera" : "./imagenes/madera.png",
			"concreto" : "./imagenes/concreto1.png",
			"acero" : "./imagenes/acero1.png",
			"aguila" : "./imagenes/eagle.png"
		}
		for bloque in bloques_regen:
			for i in range(len(bloques_regen[bloque][0])):
					
				image = Image.open(ruta_img_bloque[bloque])
				resize_image = image.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
				img = ImageTk.PhotoImage(resize_image)
				bloques_regen[bloque][1][i].configure(image=img)
				bloques_regen[bloque][1][i].img = img


				if 	not bloques_regen[bloque][1][i] in bloques_colocados[bloque][1] and not (
					x_tanque - 10< bloques_regen[bloque][0][i][0] + dim_cuadros["y2"] and
					x_tanque + 10 > bloques_regen[bloque][0][i][0] and
					y_tanque - 10< bloques_regen[bloque][0][i][1] + dim_cuadros["x2"] and
					y_tanque + 10 > bloques_regen[bloque][0][i][1]
				):
					coord_x = bloques_regen[bloque][0][i][0]+1
					coord_y = bloques_regen[bloque][0][i][1]+1

					bloques_regen[bloque][1][i].place(x=coord_x, y=coord_y)
					bloques_colocados[bloque][0].append(bloques_regen[bloque][0][i])
					bloques_colocados[bloque][1].append(bloques_regen[bloque][1][i])
					bloques_colocados[bloque][2].append(bloques_regen[bloque][2][i])

				bloques_colocados[bloque][2][i] = bloques_regen[bloque][2][i]
				
					

	#_______________________
	#						\ Regenerar bombas \__________________________

	def regenerar_bombas():
		for bomba in bombas_restantes:
			bombas_restantes[bomba][0] = 5
			bombas_restantes[bomba][3][0].configure(text=bombas_restantes[bomba][0])
			

	#_______________________
	#						\ Mostrar ganador \__________________________

	def ganador(jugador):
		global pausar_cronometro, turno_atacante
		pausar_cronometro = True
		turno_atacante = False

		ventanaPrincipal.unbind("<Key>")

		ventana_ganador = tk.Canvas(canva_juego, width=700, height=350, bg="#a2a2a2")
		ventana_ganador.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

		titulo_vent_ganador=tk.Label(ventana_ganador, text= 'El ganador es:', font= 'Fixedsys 25', bg='grey',fg='black')
		titulo_vent_ganador.place(relx=0.5, y=70, anchor=tk.CENTER )

		jugador_ganador = tk.Label (ventana_ganador, text = jugador[0], font = "Fixedsys 30 ",bg= "grey", 
			fg='black', relief= 'raised'
		)
		jugador_ganador.place(relx=0.5, y=170, anchor=tk.CENTER)

		cerrar_vent_ganador=tk.Button(ventana_ganador, text= 'Aceptar', font= 'Fixedsys 20', bg='grey',fg='black', 
			command=lambda:cerrar_ventana_ganador(ventana_ganador))
		cerrar_vent_ganador.place(relx=0.5, y=270, anchor=tk.CENTER )
		elegible = False
		if destruidos["aguila"][0] > 0:
			tiempo_tardado = (tiempo_inicial_atacante-minutos*60-segundos)

			tiempos = []
			with open('salon_fama.txt', 'r') as salon_fama:
				lineas = salon_fama.readlines()

				for linea in lineas:
					datos = linea.strip().split(',')
					tiempos.append(datos)
				print(len(lineas))
				if len(tiempos) <= 1:
					tiempos.append([str(tiempo_tardado),jugador[0],jugador[5],jugador[6]])
				elif len(tiempos) < 5:
					tiempos.append([str(tiempo_tardado),jugador[0],jugador[5],jugador[6]])
					tiempos.sort(key=lambda x: int(x[0]))
				else:
					tiempos.append([str(tiempo_tardado),jugador[0],jugador[5],jugador[6]])
					tiempos.sort(key=lambda x: int(x[0]))
					tiempos = tiempos[:5]
				print(tiempos)
				if [str(tiempo_tardado),jugador[0],jugador[5],jugador[6]] in tiempos:
					elegible = True

			with open('salon_fama.txt', 'w') as salon_fama:
				salon_fama.seek(0)
				for linea in tiempos:
					salon_fama.writelines(f"{linea[0]},{linea[1]},{linea[2]},{linea[3]}\n")

		return elegible			

	def cerrar_ventana_ganador(ventana_ganador):
		ventana_ganador.place_forget()
		ir_a_inicio()

	#_______________________
	#						\ Cronómetro \__________________________


	# Muestra el cronometro en pantalla
	label_crono = tk.Label(canva_juego, text=f"{minutos}:{segundos}", font="Fixedsys 20", width=6)
	label_crono.place(x=700, y=50)

	# funcion que muestra cuenta regresiva
	def cronometro():
		global minutos, segundos, colocar_bloques, tiempo_inicial_atacante
		tiempo_inicial_atacante


		while minutos*60 + segundos >= 0:
			if (tiempo_inicial_atacante != minutos*60 + segundos and 
				(tiempo_inicial_atacante - (minutos*60 + segundos - 1))%25 == 0 and 
				turno_atacante):
				regenerar_bloques()
			if (tiempo_inicial_atacante != minutos*60 + segundos and 
				(tiempo_inicial_atacante - (minutos*60 + segundos - 1))%30 == 0 and 
				turno_atacante):
				regenerar_bombas()
			if not pausar_cronometro:
				segundos-=1
			if segundos >= 0:
				if segundos//10 == 0 and minutos//10 == 0:
					label_crono.configure(text=f"0{minutos}:0{segundos}")
				elif  minutos//10 == 0:
					label_crono.configure(text=f"0{minutos}:{segundos}")
				elif  segundos//10 == 0:
					label_crono.configure(text=f"{minutos}:0{segundos}")
				else:
					label_crono.configure(text=f"{minutos}:{segundos}")
			elif minutos <= 0 and segundos<=0:

				if turno_atacante:
					if destruidos["aguila"][0] == 0:
						ganador(usr1)
					messagebox.showinfo("Sin tiempo.", "Fin del juego.")
				break
			else:
				minutos-=1
				segundos=59
				if minutos//10 == 0:
					label_crono.configure(text=f"0{minutos}:{segundos}")
				else:
					label_crono.configure(text=f"{minutos}:{segundos}")
			time.sleep(1)
		colocar_bloques = False

		return

	#_______________________
	#						\ Guardar Partida \__________________________

	def guardar_partida(bc):
		
		datos_guardados = [
		str(puntos), #0
		str(bloques_colocados["madera"][0]), str(bloques_colocados["madera"][2]), #1
		str(bloques_colocados["acero"][0]), str(bloques_colocados["acero"][2]), #4
		str(bloques_colocados["concreto"][0]), str(bloques_colocados["concreto"][2]), #7
		str(bloques_colocados["aguila"][0]), str(bloques_colocados["aguila"][2]), #10
		str(bloques_regen["madera"][0]), str(bloques_regen["madera"][2]), #13
		str(bloques_regen["acero"][0]), str(bloques_regen["acero"][2]), #16
		str(bloques_regen["concreto"][0]), str(bloques_regen["concreto"][2]), #19
		str(bloques_regen["aguila"][0]), str(bloques_regen["aguila"][2]), #22
		str(tiempo_turno), #23
		str(tiempo_inicial_atacante),
		str(minutos),
		str(segundos),
		str(bombas_restantes["agua"][0]),
		str(bombas_restantes["fuego"][0]),
		str(bombas_restantes["bomba"][0]),
		str(colocar_bloques),
		str(turno_atacante),
		str(x_tanque),
		str(y_tanque),
		str(direccion_tanque),
		str(usr1[0]),str(usr1[1]),str(usr1[2]),str(usr1[3]),str(usr1[4]),str(usr1[5]),str(usr1[6]),
		str(usr2[0]),str(usr2[1]),str(usr2[2]),str(usr2[3]),str(usr2[4]),str(usr2[5]),str(usr2[6]),
		str(bloques[0][1]),
		str(bloques[1][1]),
		str(bloques[2][1]),
		str(bloques[3][1]),
		str(destruidos["madera"][0]),
		str(destruidos["concreto"][0]),
		str(destruidos["acero"][0]),
		str(destruidos["aguila"][0])
		]
		

		with open('partida_guardada_3.json', 'w') as partida_guardada_3:
			with open('partida_guardada_2.json', 'r') as partida_guardada_2:
				new_dict2 = json.load(partida_guardada_2)
			json.dump(new_dict2, partida_guardada_3)
			

		with open('partida_guardada_2.json', 'w') as partida_guardada_2:
			with open('partida_guardada_1.json', 'r') as partida_guardada_1:
				new_dict1 = json.load(partida_guardada_1)
			json.dump(new_dict1, partida_guardada_2)
			

		with open('partida_guardada_1.json', 'w') as partida_guardada_1:
			json.dump(datos_guardados, partida_guardada_1)
		

	# car_partida = tk.Button(canva_juego, text ="cargar_partida", font ="Fixedsys 17", bg='grey', fg='black', 
	# 	command= lambda: cargar_partida())
	# car_partida.place(x=160, y=600)
	# def cargar_partida():
	# 	with open('partida_guardada_1.json', 'r') as partida_guardada_1:
	# 		new_dict1 = json.load(partida_guardada_1)
	# 		new_dict1_list = new_dict1[5][1:].split(", [")
	# 		#datos = new_dict1.split('", "')
	# 		print(new_dict1_list)
	# 		#json.dump(new_dict1, partida_guardada_2)
	# 	#print()

	#_______________________
	#						\ Cambiar turno \__________________________

	# Dar turno al atacante

	dar_turno = tk.Button(canva_juego, text ="Turno Atacante", font ="Fixedsys 17", bg='grey', fg='black', 
		command= lambda: turno_rol("atacante", turno_atacar))
	#
	dar_turno.place(x=160, y=500)
	
	
	turno = tk.Canvas(canva_juego, width=700, height=350, bg="#a2a2a2")
	titulo_turno = tk.Label(turno, text='',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
	titulo_turno.place(relx=0.5, y=70, anchor=tk.CENTER )

	
	btn_aceptar = tk.Button(turno, text='Aceptar', font= 'Fixedsys 20',bg='grey', fg='black', 
		command=lambda: acep_inicio_turno())
	btn_aceptar.place(relx=0.5, y=200, anchor=tk.CENTER )

	def acep_inicio_turno():
		global pausar_cronometro
		pausar_cronometro = False
		turno.place_forget()
		for child in canva_juego.winfo_children():
			child.configure(state=tk.NORMAL)
		if not turno_atacante:
			# Llama a la funcion colocarBloques si se hace clic sobre el area de juego
			area_juego.bind("<Button-1>", colocarBloques)
		else:
			ventanaPrincipal.bind("<Key>", manejar_evento_teclado)
		
		# fondoJf.place_forget()
		# rect = canva_juego.create_rectangle(20, 50, 300, 100, outline="black", fill="red")
		# canva_juego.tag_raise(rect)

	

	def turno_rol(jugador, funcion):
		if len(bloques_colocados["aguila"][1]) <= 0 and jugador == "atacante":
			messagebox.showerror(title=f"Aguila no colocada.", 
					message=f"Debe colocar el aguila antes de dar el turno al atacante."
				)
		else:
			# fondoJf.place(x=0, y=0)
			turno.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
			titulo_turno.configure(text=f'Turno de: {rol[jugador]}')
			global pausar_cronometro
			for child in canva_juego.winfo_children():
				child.configure(state=tk.DISABLED)
			pausar_cronometro = True
			funcion()
		
	def turno_defender():
		global th

		# Crea un thread separado para el cronometro
		th = threading.Thread(target=cronometro)
		th.start()
		

	def turno_atacar():
		global th, turno_atacante, minutos, segundos, tiempo_inicial_atacante
		turno_atacante = True
		for bloque in bloques_colocados:
			for i in range(len(bloques_colocados[bloque][1])):
				bloques_regen[bloque][0].append(bloques_colocados[bloque][0][i])
				bloques_regen[bloque][1].append(bloques_colocados[bloque][1][i])
				if bloque == "concreto":
					bloques_regen[bloque][2].append(6)
				elif bloque == "acero":
					bloques_regen[bloque][2].append(4)
				else:
					bloques_regen[bloque][2].append(2)

		
		dar_turno.place_forget()
		area_juego.unbind("<Button-1>")
		for elem in bloques_colocados:
			for bloque in bloques_colocados[elem][1]:
				bloque.unbind("<Button-1>")
		for bloque in bloques:
			bloque[4][0].configure(state=tk.DISABLED)

		path = "./musica"
		all_songs = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]
		# la canción predeterminada para los jugadores está en la misma carpeta que el resto de canciones
		# entonces se elimina de la lista que será utilizada en la lista de reproduccion
		del all_songs[all_songs.index("./musica\\winner_default.mp3")]

		random_song = random.choice(all_songs)
		# musica fondo
		my_sound = pygame.mixer.Sound(random_song)
		pygame.mixer.Channel(3).play(my_sound)
		my_sound.set_volume(0.4)
		minutos, segundos = tiempo_turno//60, tiempo_turno%60
		if segundos//10 == 0 and minutos//10 == 0:
			label_crono.configure(text=f"0{minutos}:0{segundos}")
		elif  minutos//10 == 0:
			label_crono.configure(text=f"0{minutos}:{segundos}")
		elif  segundos//10 == 0:
			label_crono.configure(text=f"{minutos}:0{segundos}")
		else:
			label_crono.configure(text=f"{minutos}:{segundos}")
		if not colocar_bloques:
			th = threading.Thread(target=cronometro)
			th.start()
		
	#_______________________
	#						\ Usar control \__________________________



	#Rpi = serial.Serial(port = "COM6", baudrate=115200)


	def loop_control():
		global bomba_en_movimiento, tipo_bomba
		while Rpi_reading:
			if (Rpi.isOpen()):
				#
				dt=Rpi.readline() #Esto se recibe en bytes.
				#print("si", dt)
				Dt_s = dt.decode('UTF-8') #Conversión de Byte a String
				#print(Dt_s)
				if "arriba" in Dt_s and not pausar_cronometro:
					mover_tanque_con_joystick("arriba")
				elif "abajo" in Dt_s and not pausar_cronometro:
					mover_tanque_con_joystick("abajo")
				elif "izquierda" in Dt_s and not pausar_cronometro:
					mover_tanque_con_joystick("izquierda")
				elif "derecha" in Dt_s and not pausar_cronometro:
					mover_tanque_con_joystick("derecha")
				else:
					pass

				if "agua" in Dt_s and not bomba_en_movimiento and not pausar_cronometro and turno_atacante:
					bomba_en_movimiento = True
					tipo_bomba = "agua"
					bombas_restantes[tipo_bomba][0] -= 1
					bombas_restantes[tipo_bomba][3][0].configure(text=bombas_restantes[tipo_bomba][0])
					animacion_disparo(direccion_tanque, bola_agua_image)
				elif "fuego" in Dt_s and not bomba_en_movimiento and not pausar_cronometro  and turno_atacante:
					bomba_en_movimiento = True
					tipo_bomba = "fuego"
					bombas_restantes[tipo_bomba][0] -= 1
					bombas_restantes[tipo_bomba][3][0].configure(text=bombas_restantes[tipo_bomba][0])
					animacion_disparo(direccion_tanque, bola_fuego_image)
				elif "bomba" in Dt_s and not bomba_en_movimiento and not pausar_cronometro  and turno_atacante:
					bomba_en_movimiento = True
					tipo_bomba = "bomba"
					bombas_restantes[tipo_bomba][0] -= 1
					bombas_restantes[tipo_bomba][3][0].configure(text=bombas_restantes[tipo_bomba][0])
					animacion_disparo(direccion_tanque, bomba_image)

				if "presionado" in Dt_s and not pausar_cronometro:
					pausar_juego()
					
				elif "presionado" in Dt_s and pausar_cronometro:
					continuar_juego()
					btn_aceptar.invoke()
					


				# if len(Dt_s_pausar) <2:
				# 	if "liberado" in Dt_s or "presionado" in Dt_s:
				# 		Dt_s_pausar.append(Dt_s)
				# else:
				# 	if "liberado" in Dt_s or "presionado" in Dt_s:
				# 		Dt_s_pausar.append(Dt_s)
				# 		Dt_s_pausar.pop(0)
				# print(Dt_s_pausar)
				# if len(Dt_s_pausar) == 2 and "presionado" in Dt_s_pausar[0] and "liberado" in Dt_s_pausar[1]:
				# 	if not juego_pausado:
				# 		pausar_juego()
				# 		juego_pausado = True
				# 	else:
				# 		continuar_juego()
				# 		juego_pausado = False
	
	# Llama a la funcion para dar el turno al defensor justo despues de que se ingresó a la pantalla de juego
	turno_rol("defensor", turno_defender)
	
	Rpi_thread = threading.Thread(target=loop_control)
	Rpi_thread.start()


	
	#_______________________
	#						\ Mover tanque \__________________________

	# Lista de bombas
	bombas = []


	def mover_tanque(event):
		global x_tanque, y_tanque, direccion_tanque

		# Calcula las nuevas coordenadas del tanque según la dirección
		nueva_x = x_tanque
		nueva_y = y_tanque

		if event.keysym == 'w' and y_tanque > 15:
			nueva_y -= 10
			direccion_tanque = 'up'
		elif event.keysym == 'a' and x_tanque > 16:
			nueva_x -= 10
			direccion_tanque = 'left'
		elif event.keysym == 's' and y_tanque < 585:
			nueva_y += 10
			direccion_tanque = 'down'
		elif event.keysym == 'd' and x_tanque < 586:
			nueva_x += 10
			direccion_tanque = 'right'

		# Verifica la colisión con bloques colocados
		colision = False

		for elem in bloques_colocados:
			for coords in bloques_colocados[elem][0]:
				if (
					nueva_x - 10< coords[0] + dim_cuadros["y2"] and
					nueva_x + 10 > coords[0] and
					nueva_y - 10< coords[1] + dim_cuadros["x2"] and
					nueva_y + 10 > coords[1]
				):
					colision = True
					break

		# Si no hay colisión, actualiza la posición del tanque
		if not colision:
			x_tanque = nueva_x
			y_tanque = nueva_y

		actualizar_imagen_tanque()
		area_juego.coords(tanque, x_tanque, y_tanque)


	def mover_tanque_con_joystick(direccion_joystick):

		global x_tanque, y_tanque, direccion_tanque
		if turno_atacante:
			# Calcula las nuevas coordenadas del tanque según la dirección
			nueva_x = x_tanque
			nueva_y = y_tanque

			if direccion_joystick == "arriba" and y_tanque > 15:
				nueva_y -= 10
				direccion_tanque = 'up'
			elif direccion_joystick == "izquierda" and x_tanque > 16:
				nueva_x -= 10
				direccion_tanque = 'left'
			elif direccion_joystick == "abajo" and y_tanque < 585:
				nueva_y += 10
				direccion_tanque = 'down'
			elif direccion_joystick == "derecha" and x_tanque < 586:
				nueva_x += 10
				direccion_tanque = 'right'
			elif direccion_joystick == "nulo":
				pass

			# Verifica la colisión con bloques colocados
			colision = False

			for elem in bloques_colocados:
				for coords in bloques_colocados[elem][0]:
					if (
						nueva_x - 10< coords[0] + dim_cuadros["y2"] and
						nueva_x + 10 > coords[0] and
						nueva_y - 10< coords[1] + dim_cuadros["x2"] and
						nueva_y + 10 > coords[1]
					):
						colision = True
						break

			# Si no hay colisión, actualiza la posición del tanque
			if not colision:
				x_tanque = nueva_x
				y_tanque = nueva_y

			actualizar_imagen_tanque()
			area_juego.coords(tanque, x_tanque, y_tanque)


	#_______________________
	#						\ Disparo, eliminar bloques \__________________________

	# Función para disparar
	def animacion_disparo(direccion, imagen):
	
		frames = animacion_tanque[direccion]
		for frame in frames:
			area_juego.itemconfig(tanque, image=frame)
			ventanaPrincipal.update()
			ventanaPrincipal.after(100)  # Espera 100 milisegundos antes de cambiar al siguiente frame
		# Cambia la imagen del tanque de nuevo a la dirección original
		area_juego.itemconfig(tanque, image=tanque_image_up if direccion == 'up' else
										tanque_image_down if direccion == 'down' else
										tanque_image_left if direccion == 'left' else
										tanque_image_right)
		# Una vez completada la animación, dispara la bomba
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('./tanque/sonido_bomba.wav'))
		disparar(imagen)

	def disparar(imagen):
		global direccion_tanque

		#if len(bombas) == 0:
		if direccion_tanque == 'up':
			bomba_x = x_tanque
			bomba_y = y_tanque - 10
		elif direccion_tanque == 'down':
			bomba_x = x_tanque
			bomba_y = y_tanque + 10
		elif direccion_tanque == 'left':
			bomba_x = x_tanque - 10
			bomba_y = y_tanque
		elif direccion_tanque == 'right':
			bomba_x = x_tanque + 10
			bomba_y = y_tanque
		image = imagen



	
		bomba = area_juego.create_image(bomba_x, bomba_y, image=image)
		bombas.append((bomba, direccion_tanque))
		
	def revisa_colision(bomba, direccion, bomba_x, bomba_y, bombas_a_eliminar):
		global recorrido_x, recorrido_y
		ruta_img_bloque_roto = {
			"concreto" : ["./imagenes/concreto2.png", "./imagenes/concreto3.png"],
			"acero" : ["./imagenes/acero2.png"]
		}	
		for elem in bloques_colocados:
			for i in range(len(bloques_colocados[elem][0])):
				if (
					bomba_x - 10 < bloques_colocados[elem][0][i][0] + dim_cuadros["y2"] and
					bomba_x + 0 > bloques_colocados[elem][0][i][0] and
					bomba_y - 10 < bloques_colocados[elem][0][i][1] + dim_cuadros["x2"] and
					bomba_y + 0 > bloques_colocados[elem][0][i][1]
				):
					if tipo_bomba == "agua":
						bloques_colocados[elem][2][i] -= 2
					elif tipo_bomba == "fuego":
						bloques_colocados[elem][2][i] -= 3
					elif tipo_bomba == "bomba":
						bloques_colocados[elem][2][i] -= 6
					if bloques_colocados[elem][2][i] <= 0:
						bombas_a_eliminar.append((bomba, direccion))
						bloques_colocados[elem][1][i].place_forget()
						destruidos[elem][0] += 1
						destruidos[elem][3][0].configure(text=destruidos[elem][0])
						if destruidos["aguila"][0] > 0:
							if ganador(usr2):
								messagebox.showinfo("Felicidades.", "Felicidades, has entrado al salón de la fama.")
							else:
								messagebox.showinfo("Buen juego.", "No has sido elegido para el salón de la fama.")


						del bloques_colocados[elem][0][i]
						del bloques_colocados[elem][1][i]
						del bloques_colocados[elem][2][i]
						#recorrido_x,recorrido_y = 0, 0
						global puntos
						if elem == "madera":
							puntos += 10
							label_puntos.configure(text=f"Puntos:{puntos}")
						elif elem == "concreto":
							puntos += 50
							label_puntos.configure(text=f"Puntos:{puntos}")
						elif elem == "acero":
							puntos += 25
							label_puntos.configure(text=f"Puntos:{puntos}")
						elif elem == "aguila":
							puntos += 200
							label_puntos.configure(text=f"Puntos:{puntos}")
						break

					else:
						bombas_a_eliminar.append((bomba, direccion))
						#recorrido_x,recorrido_y = 0, 0
						if elem == "concreto":
							damaged_img = ""
							if bloques_colocados[elem][2][i] > 3:
								damaged_img = Image.open(ruta_img_bloque_roto[elem][0])
							else:
								damaged_img = Image.open(ruta_img_bloque_roto[elem][1])
							resize_damaged_img = damaged_img.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
							dmg_img = ImageTk.PhotoImage(resize_damaged_img)
							bloques_colocados[elem][1][i].configure(image = dmg_img)
							bloques_colocados[elem][1][i].dmg_img = dmg_img
						elif elem == "acero":
							damaged_img = Image.open(ruta_img_bloque_roto[elem][0])
							resize_damaged_img = damaged_img.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
							dmg_img = ImageTk.PhotoImage(resize_damaged_img)
							bloques_colocados[elem][1][i].configure(image = dmg_img)
							bloques_colocados[elem][1][i].dmg_img = dmg_img
					return True
				#break

	# Función para mover las bombas
	def mover_bombas():

		global bomba_en_movimiento, recorrido_x, recorrido_y
		bombas_a_eliminar = []
		try:
			bomba_x_inicial = area_juego.coords(bombas[0])[0]
			bomba_y_inicial = area_juego.coords(bombas[0])[1]
		except IndexError:
			pass
		
		for bomba, direccion in bombas:
			if direccion == 'up':
				area_juego.move(bomba, 0, -10)
				recorrido_y +=10
			elif direccion == 'down':
				area_juego.move(bomba, 0, 10)
				recorrido_y +=10
			elif direccion == 'left':
				area_juego.move(bomba, -10, 0)
				recorrido_x +=10
			elif direccion == 'right':
				area_juego.move(bomba, 10, 0)
				recorrido_x +=10

			bomba_coords = area_juego.coords(bomba)
			bomba_x, bomba_y = bomba_coords[0], bomba_coords[1]

				

			
					
			revisa_colision(bomba, direccion, bomba_x, bomba_y, bombas_a_eliminar)
				
			# Comprueba si la bomba está fuera de la pantalla y marca para eliminarla
			if 	(bomba_x < 0 or bomba_x > 586
				or bomba_y < 0 or bomba_y > 585
				or recorrido_x >= 240 
				or recorrido_y >= 240):
				bombas_a_eliminar.append((bomba, direccion))



		for bomba, direccion in bombas_a_eliminar:
			# maneja el error de cuando una bala impacta en 2 bloques a la vez
			try:
				bombas.remove((bomba, direccion))
				area_juego.delete(bomba)
				bomba_en_movimiento = False
				recorrido_x, recorrido_y = 0, 0
			except ValueError:
				pass

		ventanaPrincipal.after(50, lambda: mover_bombas())

	# Función para manejar los eventos del teclado
	def manejar_evento_teclado(event):
		global bomba_en_movimiento, tipo_bomba
		mover_tanque(event)
		if event.keysym == 'j' and not bomba_en_movimiento:
			tipo_bomba = "agua"
			if bombas_restantes[tipo_bomba][0] <= 0:
				messagebox.showinfo("Sin bolas de agua", "No tiene bolas de agua por el momento.")
			else:
				bomba_en_movimiento = True
				bombas_restantes[tipo_bomba][0] -= 1
				bombas_restantes[tipo_bomba][3][0].configure(text=bombas_restantes[tipo_bomba][0])
				animacion_disparo(direccion_tanque, bola_agua_image)
		elif event.keysym == 'k' and not bomba_en_movimiento:
			tipo_bomba = "fuego"
			if bombas_restantes[tipo_bomba][0] <= 0:
				messagebox.showinfo("Sin bolas de agua", "No tiene bolas de agua por el momento.")
			else:
				bomba_en_movimiento = True
				bombas_restantes[tipo_bomba][0] -= 1
				bombas_restantes[tipo_bomba][3][0].configure(text=bombas_restantes[tipo_bomba][0])
				animacion_disparo(direccion_tanque, bola_fuego_image)
		elif event.keysym == 'l' and not bomba_en_movimiento:
			tipo_bomba = "bomba"
			if bombas_restantes[tipo_bomba][0] <= 0:
				messagebox.showinfo("Sin bolas de agua", "No tiene bolas de agua por el momento.")
			else:
				bomba_en_movimiento = True
				bombas_restantes[tipo_bomba][0] -= 1
				bombas_restantes[tipo_bomba][3][0].configure(text=bombas_restantes[tipo_bomba][0])
				animacion_disparo(direccion_tanque, bomba_image)

	# Actualizar la imagen del círculo según la dirección
	def actualizar_imagen_tanque():
		if direccion_tanque == 'up':
			area_juego.itemconfig(tanque, image=tanque_image_up)
		elif direccion_tanque == 'down':
			area_juego.itemconfig(tanque, image=tanque_image_down)
		elif direccion_tanque == 'left':
			area_juego.itemconfig(tanque, image=tanque_image_left)
		elif direccion_tanque == 'right':
			area_juego.itemconfig(tanque, image=tanque_image_right)


	# Cargar imágenes de círculo
	tanque_image_up = ImageTk.PhotoImage(Image.open("./tanque/tanque_arriba_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
	
	tanque_image_down = ImageTk.PhotoImage(Image.open("./tanque/tanque_abajo_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
	
	tanque_image_left = ImageTk.PhotoImage(Image.open("./tanque/tanque_izquierda_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
	
	tanque_image_right = ImageTk.PhotoImage(Image.open("./tanque/tanque_derecha_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))



	# Dibujar el tanque
	tanque = area_juego.create_image(x_tanque, y_tanque, image=tanque_image_down, )
	area_juego.tag_bind(tanque, '<Button-1>', '')


	animacion_tanque = {
		'up': [
			ImageTk.PhotoImage(Image.open("./tanque/tanque_arriba_animacion_1_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_arriba_animacion_2_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_arriba_animacion_3_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
		],
		'down': [
			ImageTk.PhotoImage(Image.open("./tanque/tanque_abajo_animacion_1_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_abajo_animacion_2_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_abajo_animacion_3_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
		],
		'left': [
			ImageTk.PhotoImage(Image.open("./tanque/tanque_izquierda_animacion_1_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_izquierda_animacion_2_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_izquierda_animacion_3_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
		],
		'right': [
			ImageTk.PhotoImage(Image.open("./tanque/tanque_derecha_animacion_1_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_derecha_animacion_2_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"]))),
			ImageTk.PhotoImage(Image.open("./tanque/tanque_derecha_animacion_3_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
		]
	}

	# Cargar imágenes de bombas
	bola_agua_image = ImageTk.PhotoImage(Image.open("./tanque/bola_agua.png"))
	bola_fuego_image = ImageTk.PhotoImage(Image.open("./tanque/bola_fuego.png"))
	bomba_image = ImageTk.PhotoImage(Image.open("./tanque/bomba.png"))
	

	# Iniciar el movimiento de las bombas
	mover_bombas()


