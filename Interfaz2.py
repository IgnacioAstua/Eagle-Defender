import tkinter as tk
from tkinter import filedialog, messagebox
from VentanaJuego import ventanaJuego
from PIL import Image, ImageTk #pip install pillow
import pygame
#Ventana Pricipal
ventana1 = tk.Tk()

ventana1.geometry('1550x800')
ventana1.title("Eagle Defender")
ventana1.configure(bg = "green")

#Canva principal
canva1 = tk.Canvas(ventana1, width = 1550, height = 800, bg = "green")
canva1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#Fondo principal
fondo1 = tk.PhotoImage(file = "fondo1.png")
fondoP = tk.Label(canva1, image = fondo1)
fondoP.place(x=0, y=0)

#Variables globales para rutas de archivos y nombres de usuario
ruta_foto = ""
ruta_cancion = ""
usr1 = ""
usr2 = ""

#Función para subir la foto
def seleccionar_foto():
	foto_path = filedialog.askopenfilename(filetypes=[("Archivos PNG", "*.png")])
	# Aquí se podría asignar la ruta a una variable o algo así
	global ruta_foto
	if foto_path:
		#Ver la ruta
		print("Ruta de la foto:", foto_path)
	ruta_foto = foto_path

def seleccionar_cancion():
	cancion_path = filedialog.askopenfilename(filetypes=[("Archivos MP#", "*.mp3")])
	# Aquí se podría asignar la ruta a una variable o algo así
	global ruta_cancion
	if cancion_path:
		#Ver la ruta
		print("Ruta de la cancion:", cancion_path)
	ruta_cancion = cancion_path

#Verifica el usuario y si está registrado
def validacion_inicio_sesion():
	# Obtener los datos ingresados en las entradas
	nombre_usuario = entrada_nommbre.get()
	contrasena = entrada_clave.get()

	if nombre_usuario and contrasena:
	# Leer y buscar los usuarios registrados en el archivo 'registro.txt'
		with open('registro.txt', 'r') as archivo:
			lineas = archivo.readlines()
			for linea in lineas:
				datos = linea.strip().split(',')
				if (len(datos) == 5 or len(datos) == 7) and datos[0] == nombre_usuario and datos[3] == contrasena:
					#Prueba
					if jugador1.cget("text") == "Jugador 1":

						# Cambia el placeholder "Jugador 1" por el nombre de usuario del jugador
						jugador1.configure(text=nombre_usuario)

						#Muestra la foto de perfil junto al nombre de usuario
						imgJ1 = Image.open(datos[5])
						resize_imgJ1 = imgJ1.resize((50,50))
						imgJ1 = ImageTk.PhotoImage(resize_imgJ1)
						label_imgJ1.imgJ1 = imgJ1
						label_imgJ1.configure(image=imgJ1)

						#para poder pasar los nombre de usuario a la pantalla de juego
						global usr1
						usr1 = nombre_usuario

						messagebox.showinfo("Completado", "Inicio de sesión exitoso.")
					elif jugador1.cget("text") != "Jugador 1" and jugador2.cget("text") == "Jugador 2":
						# Cambia el placeholder "Jugador 1" por el nombre de usuario del jugador
						jugador2.configure(text=nombre_usuario)

						#Muestra la foto de perfil junto al nombre de usuario
						imgJ2 = Image.open(datos[5])
						resize_imgJ2 = imgJ2.resize((50,50))
						imgJ2 = ImageTk.PhotoImage(resize_imgJ2)
						label_imgJ2.imgJ2 = imgJ2
						label_imgJ2.configure(image=imgJ2)

						#para poder pasar los nombre de usuario a la pantalla de juego
						global usr2
						usr2 = nombre_usuario

						messagebox.showinfo("Completado", "Inicio de sesión exitoso.")
					else:
						messagebox.showerror("Error", "Ya hay dos usuarios que iniciaron sesión")
					return

		# Si no se encontró una coincidencia, imprimir "Usuario no existente"(prueba)
		messagebox.showerror("Error", "Usuario no encontrado.")
		return
	else:
		messagebox.showerror("Error", "Ingrese un nombre y contraseña válidos")
		return

#Ventana de inicio de sesion
inicio_sesion = tk.Canvas(ventana1, width=900, height=563)
fondo2 = tk.PhotoImage(file='inicio.png')
fondo_inicio = tk.Label(inicio_sesion, image= fondo2)
fondo_inicio.place(x=0, y=0)
nombre_txt = tk.Label(inicio_sesion, text='Nickname:',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
nombre_txt.place(x=268, y=100)
entrada_nommbre = tk.Entry(inicio_sesion,font= "Fixedsys 25", bg= 'grey', width=20, relief="sunken")
entrada_nommbre.place(x=255, y=175)
clave_txt = tk.Label(inicio_sesion, text='Contraseña:',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
clave_txt.place(x=350, y=300)
entrada_clave = tk.Entry(inicio_sesion,font= "Fixedsys 25", bg= 'grey', width=20, relief="sunken", show='*')
entrada_clave.place(x=255, y=375)
btn_sesion = tk.Button(inicio_sesion, text='Iniciar Sesión', font= 'Fixedsys 20',bg='grey', fg='black', command=validacion_inicio_sesion)
btn_sesion.place(x=255, y=450)

def registro_usuario():
	# Obtener los datos ingresados en las entradas
	nickname = entrada_nick.get()
	nombre = entrada_nombre2.get()
	correo = entrada_correo.get()
	contrasena = entrada_contrasena.get()
	edad = entrada_edad.get()

	if nickname and nombre and correo and contrasena and edad:

		# Guardar los datos en un archivo de texto llamado 'registro.txt'
		with open('registro.txt', 'a') as archivo:
			# Escribir los datos en el archivo separados por comas
			archivo.write(f"{nickname},{nombre},{correo},{contrasena},{edad},{ruta_foto},{ruta_cancion} \n")

			messagebox.showinfo("¡Felicidades!", "Registro completado con éxito.")

			registro.destroy()
			inicio_sesion.pack(side=tk.TOP, pady=50)

		return


		# Leer y mostrar el contenido del archivo en la consola (solo para comprobar)
		with open('registro.txt', 'r') as archivo:
			contenido = archivo.read()
			print("Contenido del archivo 'registro.txt':")
			print(contenido)

	else:
		messagebox.showerror("Error", "Datos incorrectos. Por favor, complete todos los campos.")
		return

#Ventana de registro
registro = tk.Canvas(ventana1, width=900, height=563, bg='green')
fondo_registro = tk.Label(registro, image=fondo2)
fondo_registro.place(x=0, y=0)
nick_txt = tk.Label(registro, text= 'Nickname:', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
nick_txt.place(x=150, y=15)
entrada_nick = tk.Entry(registro, font= "Fixedsys 25", bg= 'grey', width=15, relief="sunken")
entrada_nick.place(x=100, y=75)
nombre2_txt = tk.Label(registro, text= 'Nombre:', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
nombre2_txt.place(x=178, y=135)
entrada_nombre2 = tk.Entry(registro, font= "Fixedsys 25", bg= 'grey', width=15, relief="sunken")
entrada_nombre2.place(x=100, y=195)
correo_txt = tk.Label(registro, text= 'Correo:', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
correo_txt.place(x=178, y=255)
entrada_correo = tk.Entry(registro, font= "Fixedsys 25", bg= 'grey', width=15, relief="sunken")
entrada_correo.place(x=100, y=315)
contrasena_txt = tk.Label(registro, text= 'Contraseña:', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
contrasena_txt.place(x=140, y=375)
entrada_contrasena = tk.Entry(registro, font= "Fixedsys 25", bg= 'grey', width=15, relief="sunken", show= '*')
entrada_contrasena.place(x=100, y=435)
edad_txt = tk.Label(registro, text= 'Edad:', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
edad_txt.place(x=595, y=15)
entrada_edad = tk.Entry(registro, font= "Fixedsys 25", bg= 'grey', width=15, relief="sunken")
entrada_edad.place(x=500, y=75)
foto = tk.Button(registro, text='Agregar fotografía', font= 'Fixedsys 20',bg='grey', fg='black', command=seleccionar_foto)
foto.place(x=500, y=145)
cancion = tk.Button(registro, text='Canción favorita', font= 'Fixedsys 20',bg='grey', fg='black', command=seleccionar_cancion)
cancion.place(x=518, y=225)
redes = tk.Button(registro, text='Conectar redes sociales', font= 'Fixedsys 20',bg='grey', fg='black')
redes.place(x=470, y=305)
btn_registro = tk.Button(registro, text='Registrarse', font= 'Fixedsys 20',bg='grey', fg='black', command=registro_usuario)
btn_registro.place(x=518, y=385)


# Boton de registro con la llamada a la función registro_usuario
btn_registro = tk.Button(registro, text='Registrarse', font='Fixedsys 20', bg='grey', fg='black', command=registro_usuario)
btn_registro.place(x=518, y=385)

#Ventana de ajustes
ajustes_canva = tk.Canvas(ventana1, width=664, height=465, bg='grey')
musica_txt = tk.Label(ajustes_canva, text= 'Música', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
musica_txt.place(x=275, y=25)
mute = tk.Button(ajustes_canva, text='No', font= 'Fixedsys 20',bg='grey', fg='black')
mute.place(x=400,y=80)
unmute = tk.Button(ajustes_canva, text='Sí', font= 'Fixedsys 20',bg='grey', fg='black')
unmute.place(x=220, y=80)
volumen_txt = tk.Label(ajustes_canva, text= 'Volumen', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
volumen_txt.place(x=270, y=175)
menos = tk.Button(ajustes_canva, text='-', font= 'Fixedsys 20',bg='grey', fg='black')
menos.place(x=420,y=230)
mas = tk.Button(ajustes_canva, text='+', font= 'Fixedsys 20',bg='grey', fg='black')
mas.place(x=220, y=230)
idioma_txt = tk.Label(ajustes_canva, text= 'Idioma', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
idioma_txt.place(x=285, y=325)
espanol = tk.Button(ajustes_canva, text='Español', font= 'Fixedsys 20',bg='grey', fg='black')
espanol.place(x=400,y=380)
ingles = tk.Button(ajustes_canva, text='English', font= 'Fixedsys 20',bg='grey', fg='black')
ingles.place(x=150, y=380)

#Ventana salon de la fama
salon_canva = tk.Canvas(ventana1, width=700, height=447)
fondo3 = tk.PhotoImage(file='pared.png')
fondo_salon = tk.Label(salon_canva, image=fondo3)
fondo_salon.place(x=0, y=0)
mejores_txt = tk.Label(salon_canva, text= 'Mejores Puntuaciones', font= 'Fixedsys 25',bg='grey', fg='black', relief='raised')
mejores_txt.place(x=165, y=20)

#Titulo principal
tituloP = tk.Label (canva1, text = "Eagle Defender", font = "Fixedsys 80 ",bg= "grey", fg='black', relief= 'raised')
tituloP.place(x=500, y=70)

#Jugador 1
jugador1 = tk.Label (canva1, text = "Jugador 1", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
jugador1.place(x=200, y=100)
imgJ1 = Image.open("./perfil_placeholder.png")
resize_imgJ1 = imgJ1.resize((50,50))
imgJ1 = ImageTk.PhotoImage(resize_imgJ1)

label_imgJ1 = tk.Label(canva1, image = imgJ1, height=50, width=50, borderwidth=0, highlightthickness=0)
label_imgJ1.imgJ1 = imgJ1
label_imgJ1.place(x=150, y=100)

#Jugador 2
jugador2 = tk.Label (canva1, text = "Jugador 2", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
jugador2.place(x=1200, y=100)
imgJ2 = Image.open("./perfil_placeholder.png")
resize_imgJ2 = imgJ2.resize((50,50))
imgJ2 = ImageTk.PhotoImage(resize_imgJ2)

label_imgJ2 = tk.Label(canva1, image = imgJ2, height=50, width=50, borderwidth=0, highlightthickness=0)
label_imgJ2.imgJ2 = imgJ2
label_imgJ2.place(x=1150, y=100)

# Boton para ir a la pantalla de juego
jugar = tk.Button(canva1, text='Iniciar Juego', font= 'Fixedsys 25',bg='grey', fg='black', command = lambda: iniciar_juego())
jugar.place(x=618, y=225)

#Boton de inicio de sesion
iniciar = tk.Button(canva1, text='Iniciar Sesión', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: inicio_sesion.pack(side=tk.TOP, pady=50))
iniciar.place(x=605, y=325)
salir_inicio = tk.Button(inicio_sesion, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: inicio_sesion.pack_forget())
salir_inicio.place(x=10, y=10)

#Boton de registro
registrarse = tk.Button(canva1, text= 'Registrarse', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: registro.pack(side=tk.TOP, pady=50))
registrarse.place(x=640, y=425)
salir_registro = tk.Button(registro, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: registro.pack_forget())
salir_registro.place(x=10, y=10)

#Boton salon de la fama
salon_fama = tk.Button(canva1, text='Salón de la fama', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: salon_canva.pack(side=tk.TOP, pady=100))
salon_fama.place(x=590, y=525)
salir_salon = tk.Button(salon_canva, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: salon_canva.pack_forget())
salir_salon.place(x=10, y=10)

#Boton de ajustes
ajust=tk.Button(canva1, text ="Ajustes", font ="Fixedsys 25", bg='grey', fg='black', command= lambda: ajustes_canva.pack(side= tk.TOP, pady=50))
ajust.place(x=680, y=625)
salir_ajustes=tk.Button(ajustes_canva, text= 'Volver', font= 'Fixedsys 16', bg='grey',fg='black', command= lambda: ajustes_canva.pack_forget())
salir_ajustes.place(x=10,y=10)

#Boton de salida
salirP=tk.Button(canva1, text = "Salir", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: ventana1.destroy())
salirP.place(x=95,y=30)

#jugar sin iniciar sesion
salirP=tk.Button(canva1, text = "Jugar rapido", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: jugar_rapido())
salirP.place(x=150,y=30)


def iniciar_juego():
	# https://stackoverflow.com/questions/63251775/how-to-delete-and-recreate-a-canvas-tkinter-canvas
	if jugador1.cget("text") != "Jugador 1" and jugador2.cget("text") != "Jugador 2":
		canva1.destroy()
		ventanaJuego(ventana1, usr1, usr2)
	else:
		messagebox.showerror("Error", "Dos jugadores deben haber iniciado sesión para iniciar el juego.")
def jugar_rapido():
	canva1.destroy()
	ventanaJuego(ventana1, "Jugador 1", "Jugador 2")









ventana1.mainloop()