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


# Ventana Principal
def ventanaJuego(ventanaPrincipal, usr1, usr2):

	path = "./musica"
	all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]

	random_song = random.choice(all_mp3)
	# musica fondo
	pygame.mixer.init()
	pygame.mixer.Channel(0).play(pygame.mixer.Sound(random_song), loops=-1)

	# Contiene los bloque, cronometro y area de juego
	canva_juego = tk.Canvas(ventanaPrincipal, width = 1550, height = 800)
	canva_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

	# area de juego donde se van a colocar y los bloques 
	area_juego = tk.Canvas(ventanaPrincipal, width = size_area_juego["width"], height = size_area_juego["height"], 
		bg = "#2a2a2a", highlightthickness=0
	)
	area_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

	# Fondo de pantalla
	img_fondo = Image.open("./fondo2.png")
	resize_image = img_fondo.resize((1700,900))
	imgF = ImageTk.PhotoImage(resize_image)

	fondoJ = tk.Label(canva_juego, image = imgF)
	fondoJ.img_fondo = imgF
	fondoJ.place(x=0, y=0)

	#Jugador 1
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


	# Agrega cada uno de los bloques a la pantalla, formando el inventario
	# La lista vacía en la posicion 4 de cada bloque se remplazará con la referencia al bloque en el inventario
	bloques = [
		["madera",	10,	(200,250),	"./madera.png"	,[]	],
		["concreto",10,	(200,306), 	"./concreto.png",[]	],
		["acero", 	10,	(200,362), 	"./acero.png"	,[]	],
	]

	# Usado para guardar el valor de el Radiobutton seleccionado
	var = tk.IntVar()


	'''
	bloque[0] es el nombre del bloque
	bloque[1] es la cantidad restante
	bloque[2] es la posicion en pantalla en la que se colocará ese bloque para crear el inventario
	bloque[3] es dirección de la imagen que corresponde al bloque
	bloque[4] es dirección de la imagen que corresponde al bloque
	'''
	for bloque in bloques:
		img_bloque = Image.open(bloque[3]) 
		resize_image = img_bloque.resize((50,50)) # ajusta tamaño de imagen
		img = ImageTk.PhotoImage(resize_image)

		index = bloques.index(bloque)
		label_bloque = tk.Radiobutton(canva_juego, text=bloque[1], variable=var, value=index, 
			font="Fixedsys 20",image = img, height=50, width=50, borderwidth=0,compound="center", 
			 indicatoron=0, relief=tk.FLAT, selectcolor="red"
		)
		label_bloque.img_bloque = img
		label_bloque.place(x=bloque[2][0], y=bloque[2][1])
		# Agrega la referencia al Radiobutton reciencreado al cuadro al que correponde 
		# en la posición 4 de bloque (elemento de la lista bloques)
		bloque[4] = [label_bloque]

	# Muestra el cronometro en pantalla
	label_crono = tk.Label(canva_juego, text=f"{minutos}:{segundos}", font="Fixedsys 20", width=6)
	label_crono.place(x=700, y=50)

	# funcion que muestra cuenta regresiva
	def cronometro():
		global minutos, segundos, colocar_bloques	
		for i in range(minutos*60 + segundos):
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
			elif minutos <0:
				print("sin tiempo")
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

	# Crea un thread separado para el cronometro
	th = threading.Thread(target=cronometro)
	th.start()

	# cuadricula de area de juego
	dim_cuadricula = (20, 20)
	dim_cuadros = {	"x1":0, "y1":0, 
					"x2":size_area_juego["width"]//dim_cuadricula[0], 
					"y2":size_area_juego["height"]//dim_cuadricula[1]}

	for i in range(1,dim_cuadricula[0]+1):
		fila = []
		for j in range(1,dim_cuadricula[1]+1):
			cuadro = area_juego.create_rectangle(
				dim_cuadros["x1"]+(j-1)*dim_cuadros["x2"], dim_cuadros["y1"]+(i-1)*dim_cuadros["y2"], 
				dim_cuadros["x2"]*j, dim_cuadros["y2"]*i, 
				fill="#242424", outline=""
			)
			fila.append(cuadro)
		matriz_cuadros.append(fila)

	#listas para guardar cada uno de los labels se
	madera = []
	concreto = []
	acero = []
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
			bloques[var.get()][1]-=1

			''' Referencia de los bloques de inventario creados se guarda en la posicion 3 de la lista "bloques"
				Se usa el valor del RadioButton seleccionado para cambiar el texto del bloque que se seleccionó'''
			selected = bloques[var.get()][4][0]
			selected.configure(text=bloques[var.get()][1])

			ubicacion = find_item_location(item, matriz_cuadros)
			image = Image.open(bloques[var.get()][3])
			resize_image = image.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
			img = ImageTk.PhotoImage(resize_image)

			label = tk.Label(area_juego, image = img, height=dim_cuadros["x2"]-5, width=dim_cuadros["y2"]-5)
			# añade el label a la lista madera, concreto y acero, segun corresponda
			if bloques[var.get()][0] == "madera":
				madera.append(label)
			if bloques[var.get()][0] == "concreto":
				concreto.append(label)
			else :
				acero.append(label)
			label.image = img
			label.place(x=int(ubicacion[0])+1, y=int(ubicacion[1])+1)
			label.bind("<Button-1>", lambda event, l=label: removerBloque(event,l))
		elif not colocar_bloques:
			messagebox.showinfo(title="Sin tiempo", message="El tiempo para colocar bloques a acabado")
		else:
			# Para convertir el nombre de la varible guardada para el numero del bloque seleccionado
			messagebox.showinfo(title=f"Sin {bloques[var.get()][0]}", 
				message=f"Ya no tiene más bloques de {bloques[var.get()][0]}"
			)
	def removerBloque(event, label):
		if label in madera:
			bloques[0][1]+=1
			bloques[0][4][0].configure(text=bloques[0][1])
			i = madera.index(label)
			del madera[i]
		elif label in concreto:
			bloques[1][1]+=1
			bloques[1][4][0].configure(text=bloques[1][1])
			i = concreto.index(label)
			del concreto[i]
		elif label in acero:
			bloques[2][1]+=1
			bloques[2][4][0].configure(text=bloques[2][1])
			i = acero.index(label)
			del acero[i]
		label.place_forget()

	area_juego.bind("<Button-1>", colocarBloques)
	

	# Colocar bloques
	# def onclick(event):
		
	# 	if bloques[var.get()][1] > 0 and colocar_bloques:
	# 		item = area_juego.find_closest(event.x, event.y)

	# 		def find_item_location(item, matriz_cuadros):
	# 			for i in range(len(matriz_cuadros)):
	# 				for j in range(len(matriz_cuadros[i])):
	# 					if matriz_cuadros[i][j] == item[0]:
	# 						coords = area_juego.coords(matriz_cuadros[i][j])
	# 						return coords
	# 			return None
	# 		bloques[var.get()][1]-=1

	# def iniciar_juego():
	# 	#
	# 	canva_juego.destroy()
	# 	ventanaJuego(ventanaPrincipal)





