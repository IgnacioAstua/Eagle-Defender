"""
Índice

1. Musica
2. Pantalla de juego y cuadricula
3. Nombres de jugadores en pantalla de juego
4. Inventario
5. Colocar bloques
6. Remover bloques
7. Cronómetro
8. Cambiar turno

"""



import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk #pip install pillow
import pygame
import time
import threading
import os
import random

# Variables
size_area_juego = {"width":600,"height":600}
matriz_cuadros = []
minutos, segundos = 1, 30
colocar_bloques = True
# Variables de posición del círculo
x_tanque = 286
y_tanque = 15
# Dirección actual del círculo
direccion_tanque = 'down'
turno_atacante = False
puntos = 0
th = False
pausar_cronometro = False
# Bandera para saber si hay una bomba en la pantalla
bomba_en_movimiento = False



# Ventana Principal
def ventanaJuego(ventanaPrincipal, usr1, usr2, rol, canva1):

	#___________________
	#					\ 1. Musica \___________________

	path = "./musica"
	all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]

	random_song = random.choice(all_mp3)
	pygame.mixer.init()
	musica_fondo = pygame.mixer.Sound(random_song)
	pygame.mixer.Channel(0).play(musica_fondo, loops=-1)
	musica_fondo.set_volume(0.7)


	#_______________
	#				\ 2. Pantalla de juego y cuadricula \_______________

	# Contiene los bloque, cronometro y area de juego
	canva_juego = tk.Canvas(ventanaPrincipal, width = 1550, height = 800)
	canva_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


	# Fondo de pantalla
	img_fondo = Image.open("./fondo2.png")
	resize_image = img_fondo.resize((1700,900))
	imgF = ImageTk.PhotoImage(resize_image)

	fondoJ = tk.Label(canva_juego, image = imgF)
	fondoJ.img_fondo = imgF
	fondoJ.place(x=0, y=0)

	# volver a pantalla inicial

	#boton para pausar en la pantalla de juego
	pausar=tk.Button(canva_juego, text= 'Pausa', font= 'Fixedsys 16', bg='grey',fg='black', command=lambda:pausar_juego())
	pausar.place(x=100,y=30)

	def continuar_juego(pausa):
		global pausar_cronometro
		pausar_cronometro = False
		pausa.place_forget()
		pausar.configure(state=tk.NORMAL)


	def pausar_juego():
		global pausar_cronometro
		pausar_cronometro = True
		pausar.configure(state=tk.DISABLED)
		# ventana de pausa
		pausa = tk.Canvas(canva_juego, width=700, height=350, bg="#a2a2a2")
		pausa.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


		volver_inicio=tk.Button(pausa, text= 'Volver a inicio', font= 'Fixedsys 20', bg='grey',fg='black', command=lambda:ir_a_inicio())
		volver_inicio.place(relx=0.5, y=100, anchor=tk.CENTER )
		
		# titulo_turno = tk.Label(turno, text=f'Turno de: {rol[jugador]}',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
		# titulo_turno.place(relx=0.5, y=70, anchor=tk.CENTER )

		# btn_aceptar = tk.Button(turno, text='Aceptar', font= 'Fixedsys 20',bg='grey', fg='black', command=lambda: turno.place_forget())
		# btn_aceptar.place(relx=0.5, y=200, anchor=tk.CENTER )

		continuar=tk.Button(pausa, text= 'Continuar partida', font= 'Fixedsys 20', bg='grey',fg='black', command=lambda:continuar_juego(pausa))
		continuar.place(relx=0.5, y=200, anchor=tk.CENTER )

	def ir_a_inicio():
		global pausar_cronometro, th, minutos, segundos, colocar_bloques,x_tanque,y_tanque, puntos
		th = threading.Thread(target=cronometro)
		pausar_cronometro = True
		colocar_bloques = True
		x_tanque = 286
		y_tanque = 15
		canva_juego.destroy()
		canva1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		pygame.mixer.quit()
		time.sleep(1.1)
		minutos, segundos = 1, 30
		pausar_cronometro = False
		puntos = 0

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
	#				\ 3. Nombres de jugadores en pantalla de juego \_______________

	with open('registro.txt', 'r') as archivo:
			lineas = archivo.readlines()
			for linea in lineas:
				datos = linea.strip().split(',')
				#Prueba
				if datos[0] == usr1:
					jugador1 = tk.Label (canva_juego, text = datos[0], font = "Fixedsys 30 ",bg= "grey", 
						fg='black', relief= 'raised'
					)
					jugador1.place(x=200, y=100)
					imgJ1 = Image.open(datos[5])
					resize_imgJ1 = imgJ1.resize((50,50))
					imgJ1 = ImageTk.PhotoImage(resize_imgJ1)

					label_imgJ1 = tk.Label(canva_juego, image = imgJ1, height=50, width=50, borderwidth=0, 
						highlightthickness=0
					)
					label_imgJ1.imgJ1 = imgJ1
					label_imgJ1.place(x=150, y=100)

				elif datos[0] == usr2:
					jugador2 = tk.Label (canva_juego, text = datos[0], font = "Fixedsys 30 ",bg= "grey", 
						fg='black', relief= 'raised'
					)
					jugador2.place(x=1200, y=100)
					imgJ2 = Image.open(datos[5])
					resize_imgJ2 = imgJ2.resize((50,50))
					imgJ2 = ImageTk.PhotoImage(resize_imgJ2)

					label_imgJ2 = tk.Label(canva_juego, image = imgJ2, height=50, width=50, borderwidth=0, 
						highlightthickness=0
					)
					label_imgJ2.imgJ2 = imgJ2
					label_imgJ2.place(x=1150, y=100)


	#_______________________
	#						\ 4. Inventario \__________________________
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
		["madera",	10,	(160, 350),	"./madera.png"	,[]	],
		["concreto",10,	(216, 350), 	"./concreto.png",[]	],
		["acero", 	10,	(272, 350), 	"./acero.png"	,[]	],
		["aguila", 	1,	(328, 350), 	"./eagle.png"	,[]	],
	]

	destruidos = {
		"madera":	[0,	(1150, 350),	"./madera.png"	,[]	],
		"concreto":	[0,	(1200, 350),	"./concreto.png",[]	],
		"acero":	[0,	(1250, 350), 	"./acero.png"	,[]	],
		"aguila":	[0,	(1300, 350), 	"./eagle.png"	,[]	],
	}

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
	#_______________________
	#						\ 5. Colocar bloques \__________________________
	"""
	- Los bloques se colocan con un label que tiene una imagen
	- La imagen corresponde al bloque seleccionado en el inventario (radiobutton)
	- Los bloques colocados se guardaran en una lista la cual su nombre corresponde al bloque que guardará
	- La lista de cada bloque se usará para luego poder removerlos de la pantalla
	"""
	#listas para guardar cada uno de los labels se
	bloques_colocados = {
		"madera":[[],[]],
		"concreto":[[],[]],
		"acero":[[],[]],
		"aguila":[[],[]]
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
				bloques_colocados["madera"][1].append(label)
				bloques_colocados["madera"][0].append(ubicacion)
			elif bloques[var.get()][0] == "concreto":
				bloques_colocados["concreto"][1].append(label)
				bloques_colocados["concreto"][0].append(ubicacion)
			elif bloques[var.get()][0] == "acero":
				bloques_colocados["acero"][1].append(label)
				bloques_colocados["acero"][0].append(ubicacion)
			else :
				bloques_colocados["aguila"][1].append(label)
				bloques_colocados["aguila"][0].append(ubicacion)
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
	#						\ 6. Remover bloques \__________________________
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
			elif label in bloques_colocados["concreto"][1]:
				bloques[1][1]+=1
				bloques[1][4][0].configure(text=bloques[1][1])
				i = bloques_colocados["concreto"][1].index(label)
				del bloques_colocados["concreto"][0][i]
				del bloques_colocados["concreto"][1][i]
			elif label in bloques_colocados["acero"][1]:
				bloques[2][1]+=1
				bloques[2][4][0].configure(text=bloques[2][1])
				i = bloques_colocados["acero"][1].index(label)
				del bloques_colocados["acero"][0][i]
				del bloques_colocados["acero"][1][i]
			elif label in bloques_colocados["aguila"][1]:
				bloques[3][1]+=1
				bloques[3][4][0].configure(text=bloques[3][1])
				i = bloques_colocados["aguila"][1].index(label)
				del bloques_colocados["aguila"][0][i] 
				del bloques_colocados["aguila"][1][i] 
			label.place_forget()
		else:
			messagebox.showinfo(title="Sin tiempo.", message="Ya no puede remover los bloques")
	# Llama a la funcion colocarBloques si se hace clic sobre el area de juego
	area_juego.bind("<Button-1>", colocarBloques)
	

	#_______________________
	#						\ 7. Cronómetro \__________________________


	# Muestra el cronometro en pantalla
	label_crono = tk.Label(canva_juego, text=f"{minutos}:{segundos}", font="Fixedsys 20", width=6)
	label_crono.place(x=700, y=50)

	# funcion que muestra cuenta regresiva
	def cronometro():
		global minutos, segundos, colocar_bloques


		while minutos*60 + segundos >= 0:
			if pausar_cronometro:
				pass
			else:
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
					ventanaPrincipal.unbind("<Key>")
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
	#						\ 8. Cambiar turno \__________________________

	# Dar turno al atacante

	dar_turno = tk.Button(canva_juego, text ="Turno Atacante", font ="Fixedsys 17", bg='grey', fg='black', command= lambda: turno_rol("atacante", turno_atacar))
	#
	dar_turno.place(x=160, y=500)
	
	turno = tk.Canvas(canva_juego, width=700, height=350, bg="#a2a2a2")
	def turno_rol(jugador, funcion):
		if len(bloques_colocados["aguila"][1]) <= 0 and jugador == "atacante":
			messagebox.showerror(title=f"Aguila no colocada.", 
					message=f"Debe colocar el aguila antes de dar el turno al atacante."
				)
		else:
			turno.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

			titulo_turno = tk.Label(turno, text=f'Turno de: {rol[jugador]}',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
			titulo_turno.place(relx=0.5, y=70, anchor=tk.CENTER )

			btn_aceptar = tk.Button(turno, text='Aceptar', font= 'Fixedsys 20',bg='grey', fg='black', command=lambda: turno.place_forget())
			btn_aceptar.place(relx=0.5, y=200, anchor=tk.CENTER )
			funcion()

	def turno_defender():
		global th
		# Crea un thread separado para el cronometro
		th = threading.Thread(target=cronometro)
		th.start()
		

	def turno_atacar():
		global th, turno_atacante
		turno_atacante = True
		dar_turno.place_forget()
		area_juego.unbind("<Button-1>")
		ventanaPrincipal.bind("<Key>", manejar_evento_teclado)
		for elem in bloques_colocados:
			for bloque in bloques_colocados[elem][1]:
				bloque.unbind("<Button-1>")
		for bloque in bloques:
			bloque[4][0].configure(state=tk.DISABLED)

		path = "./musica"
		all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]

		random_song = random.choice(all_mp3)
		# musica fondo
		my_sound = pygame.mixer.Sound(random_song)
		pygame.mixer.Channel(0).play(my_sound)
		my_sound.set_volume(0.4)
		# duración de la canción en segundos
		duracion_cancion = pygame.mixer.Sound(random_song).get_length()
		global minutos, segundos
		minutos, segundos = int(duracion_cancion//60), int(duracion_cancion%60 )
		label_crono.configure(text=f"{minutos}:{segundos}")
		if not colocar_bloques:
			th = threading.Thread(target=cronometro)
			th.start()
		
		
	# Llama a la funcion para dar el turno al defensor justo despues de que se ingresó a la pantalla de juego
	turno_rol("defensor", turno_defender)


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



	# Función para disparar
	def animacion_disparo(direccion):
		frames = animacion_tanque[direccion]
		for frame in frames:
			area_juego.itemconfig(tanque, image=frame)
			ventanaPrincipal.update()
			ventanaPrincipal.after(100)  # Espera 100 milisegundos antes de cambiar al siguiente frame
		# Cambia la imagen del tanque de nuevo a la dirección original
		area_juego.itemconfig(tanque, image=circle_image_up if direccion == 'up' else
										circle_image_down if direccion == 'down' else
										circle_image_left if direccion == 'left' else
										circle_image_right)
		# Una vez completada la animación, dispara la bomba
		pygame.mixer.Channel(1).play(pygame.mixer.Sound('./tanque/sonido_bomba.wav'))
		disparar()

	def disparar():
		global direccion_tanque

		#if len(bombas) == 0:
		if direccion_tanque == 'up':
			bomba_x = x_tanque
			bomba_y = y_tanque - 10
			image = bomba_image_up
		elif direccion_tanque == 'down':
			bomba_x = x_tanque
			bomba_y = y_tanque + 10
			image = bomba_image_down
		elif direccion_tanque == 'left':
			bomba_x = x_tanque - 10
			bomba_y = y_tanque
			image = bomba_image_left
		elif direccion_tanque == 'right':
			bomba_x = x_tanque + 10
			bomba_y = y_tanque
			image = bomba_image_right



	
		bomba = area_juego.create_image(bomba_x, bomba_y, image=image)
		bombas.append((bomba, direccion_tanque))
		#print(bomba)
		# print(canva_juego.winfo_children())
		


	# Función para mover las bombas
	def mover_bombas(recorrido_x, recorrido_y):
		global bomba_en_movimiento
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

			# Comprueba si la bomba está fuera de la pantalla y marca para eliminarla
			if (bomba_x < 0 or bomba_x > 586 or bomba_y < 0 or bomba_y > 585 or recorrido_x >= 240 or recorrido_y >= 240):
				bombas_a_eliminar.append((bomba, direccion))
				recorrido_x, recorrido_y = 0, 0


			for elem in bloques_colocados:
				for i in range(len(bloques_colocados[elem][0])):
					if (
						bomba_x - 10 < bloques_colocados[elem][0][i][0] + dim_cuadros["y2"] and
						bomba_x + 0 > bloques_colocados[elem][0][i][0] and
						bomba_y - 10 < bloques_colocados[elem][0][i][1] + dim_cuadros["x2"] and
						bomba_y + 0 > bloques_colocados[elem][0][i][1]
					):
						bombas_a_eliminar.append((bomba, direccion))
						bloques_colocados[elem][1][i].place_forget()
						destruidos[elem][0] += 1
						destruidos[elem][3][0].configure(text=destruidos[elem][0])
						del bloques_colocados[elem][0][i]
						del bloques_colocados[elem][1][i]
						recorrido_x,recorrido_y = 0, 0
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


			



		for bomba, direccion in bombas_a_eliminar:
			bombas.remove((bomba, direccion))
			area_juego.delete(bomba)
			bomba_en_movimiento = False

		ventanaPrincipal.after(50, lambda: mover_bombas(recorrido_x, recorrido_y))

	# Función para manejar los eventos del teclado
	def manejar_evento_teclado(event):
		global bomba_en_movimiento
		mover_tanque(event)
		if event.keysym == 'space' and not bomba_en_movimiento:
			# Dispara la animación antes de disparar la bomba
			bomba_en_movimiento = True
			animacion_disparo(direccion_tanque)

	# Actualizar la imagen del círculo según la dirección
	def actualizar_imagen_tanque():
		if direccion_tanque == 'up':
			area_juego.itemconfig(tanque, image=circle_image_up)
		elif direccion_tanque == 'down':
			area_juego.itemconfig(tanque, image=circle_image_down)
		elif direccion_tanque == 'left':
			area_juego.itemconfig(tanque, image=circle_image_left)
		elif direccion_tanque == 'right':
			area_juego.itemconfig(tanque, image=circle_image_right)

	# # Crear una ventana Tkinter
	# ventana = tk.Tk()
	# ventana.title("Juego con círculo")

	# # Crear un lienzo (canvas) en la ventana
	# canvas = tk.Canvas(area_juego, width=400, height=400, bg='green')
	# canvas.pack()

	# Cargar imágenes de círculo
	circle_image_up = ImageTk.PhotoImage(Image.open("./tanque/tanque_arriba_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
	circle_image_down = ImageTk.PhotoImage(Image.open("./tanque/tanque_abajo_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
	circle_image_left = ImageTk.PhotoImage(Image.open("./tanque/tanque_izquierda_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))
	circle_image_right = ImageTk.PhotoImage(Image.open("./tanque/tanque_derecha_.png").resize((dim_cuadros["y2"], dim_cuadros["x2"])))


	# Dibujar el círculo
	tanque = area_juego.create_image(x_tanque, y_tanque, image=circle_image_down, )
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
	bomba_image_up = ImageTk.PhotoImage(Image.open("./tanque/bomba_3.png"))#.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
	bomba_image_down = ImageTk.PhotoImage(Image.open("./tanque/bomba_3.png"))#.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
	bomba_image_left = ImageTk.PhotoImage(Image.open("./tanque/bomba_3.png"))#.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
	bomba_image_right = ImageTk.PhotoImage(Image.open("./tanque/bomba_3.png"))#.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
	

	# Iniciar el movimiento de las bombas
	mover_bombas(0, 0)


