import tkinter as tk
from tkinter import filedialog, messagebox
from VentanaJuego import ventanaJuego
from PIL import Image, ImageTk #pip install pillow
import pygame # mixer para reproducir canciones
import os #direcciones del sistema
import threading # funciones de la playlist de musica
import time # sleep , Clock tick
import random # playlist en orden aleatoria
#import shutil #copiar canciones favoritas a carpeta "favoritas"
#Ventana Pricipal
ventana1 = tk.Tk()

ventana1.geometry('1550x800')
ventana1.title("Eagle Defender")
ventana1.configure(bg = "green")

#Canva principal
canva1 = tk.Canvas(ventana1, width = 1550, height = 800, bg = "green")
canva1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#Fondo principal
fondo1 = tk.PhotoImage(file = "./imagenes/fondo1.png")
fondoP = tk.Label(canva1, image = fondo1)
fondoP.place(x=0, y=0)



def insert_into_playlist(playlist, music_file):
	playlist.append(music_file)

not_stopping = True
def play_playlist(channel, play_list, paused):
	for music_file in play_list:
		sound = pygame.mixer.Sound(music_file)
		channel.queue(sound)
		while channel.get_busy() and not_stopping:
			pygame.time.Clock().tick(10)

	paused.clear()

def start_playlist(channel, play_list, paused_music):
	music_thread = threading.Thread(target=play_playlist, args=(channel, play_list, paused_music))
	music_thread.start()

def pause_music(channel):
	channel.pause()

def resume_music(channel):
	channel.unpause()

pygame.mixer.init()

path = "./bg_music"
all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]

playlist_channel = pygame.mixer.Channel(3)  # Use channel 1 for the playlist

playList = []
for songs in all_mp3:
	random_song = random.choice(all_mp3)
	all_mp3.pop(all_mp3.index(random_song))
	insert_into_playlist(playList, random_song)

paused_music = threading.Event()

start_playlist(playlist_channel, playList, paused_music)

# # Your GUI or button handling code here
# while True:
#     # Simulate a button click to pause music, replace this with your actual button click event
#     time.sleep(1)
#     pause_music(playlist_channel)

#     # Simulate a button click to resume music, replace this with your actual button click event
#     time.sleep(1)
#     resume_music(playlist_channel)

 
# Continue with the rest of your program
# ...

# Wait for the music thread to finish before exiting (optional)
# music_thread.join()






#Variables globales para rutas de archivos y nombres de usuario
ruta_foto = ""
ruta_cancion = ""
usr1 = ["Jugador 1","","","","","./imagenes/perfil_placeholder.png","./musica/winner_default.mp3"]
usr2 = ["Jugador 2","","","","","./imagenes/perfil_placeholder.png","./musica/winner_default.mp3"]

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
						usr1 = datos

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
						usr2 = datos

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
fondo2 = tk.PhotoImage(file='./imagenes/inicio.png')
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
	global ruta_foto
	global ruta_cancion
	
	if nickname and nombre and correo and contrasena and edad:

		# Guardar los datos en un archivo de texto llamado 'registro.txt'
		with open('registro.txt', 'r+') as archivo:
			# Revisa que no haya usuarios registrados con el mismo nombre o correo
			lineas = archivo.readlines()
			usuario_no_registrado = True
			for linea in lineas:
				datos = linea.strip().split(',')
				if datos[2] == correo and datos[0] == nickname:
					messagebox.showerror("Error", "Nombre de usuario y correo en uso.")
					usuario_no_registrado = False
					return usuario_no_registrado
				elif datos[0] == nickname:
					messagebox.showerror("Error", "Nombre de usuario está en uso.")
					usuario_no_registrado = False
					return usuario_no_registrado
				elif datos[2] == correo:
					messagebox.showerror("Error", "Correo está vinculado a otro usuario.")
					usuario_no_registrado = False
					return usuario_no_registrado
			if usuario_no_registrado:

				# Si el ususario no agrega foto o canción, se usarán valores por defecto
				if ruta_foto == "" and ruta_cancion == "":
					msj = messagebox.askquestion("Sin foto ni canción", "No se agregó foto ni canción.\nSe agregarán una foto y canción por defecto.\n¿Desea continuar?")
					if msj == "yes":
						ruta_foto = "./imagenes/perfil_placeholder.png"
						ruta_cancion = "./winner_default.mp3"
						# Escribir los datos en el archivo separados por comas
						archivo.write(f"{nickname},{nombre},{correo},{contrasena},{edad},{ruta_foto},{ruta_cancion} \n")
						messagebox.showinfo("Registro exitoso.", "Se registró sin foto ni canción personalizada.")
					else:
						messagebox.showinfo("No registrado.", "Se canceló el registro.")


				elif ruta_foto == "":
					msj = messagebox.askquestion("Sin foto.", "No se agregó foto.\nSe agregarán una foto por defecto.\n¿Desea continuar?")
					if msj == "yes":
						ruta_foto = "./imagenes/perfil_placeholder.png"
						# Escribir los datos en el archivo separados por comas
						archivo.write(f"{nickname},{nombre},{correo},{contrasena},{edad},{ruta_foto},{ruta_cancion} \n")
						messagebox.showinfo("Registro exitoso.", "Se registró sin foto personalizada.")
					else:
						messagebox.showinfo("No registrado.", "Se canceló el registro.")
				elif ruta_cancion == "":
					
					msj = messagebox.askquestion("Sin canción.", "No se agregó canción.\nSe agregarán una canción por defecto.\n¿Desea continuar?")
					if msj == "yes":
						ruta_cancion = "./winner_default.mp3"
						# Escribir los datos en el archivo separados por comas
						archivo.write(f"{nickname},{nombre},{correo},{contrasena},{edad},{ruta_foto},{ruta_cancion} \n")
						messagebox.showinfo("Registro exitoso.", "Se registró sin canción personalizada.")
					else:
						messagebox.showinfo("No registrado.", "Se canceló el registro.")
				else:
					# Escribir los datos en el archivo separados por comas
					archivo.write(f"{nickname},{nombre},{correo},{contrasena},{edad},{ruta_foto},{ruta_cancion} \n")
					messagebox.showinfo("Registro exitoso.", "Se registró completado con éxito.")



			ruta_foto = ""
			ruta_cancion = ""


		registro.pack_forget()
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
musica_txt.place(relx=0.5, y=25, anchor=tk.N)
mute = tk.Button(ajustes_canva, text='No', font= 'Fixedsys 20',bg='grey', fg='black')
mute.place(x=400,y=80)
unmute = tk.Button(ajustes_canva, text='Sí', font= 'Fixedsys 20',bg='grey', fg='black')
unmute.place(x=220, y=80)
volumen_txt = tk.Label(ajustes_canva, text= 'Volumen', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
volumen_txt.place(relx=0.5, y=175, anchor=tk.N)
menos = tk.Button(ajustes_canva, text='-', font= 'Fixedsys 20',bg='grey', fg='black')
menos.place(x=420,y=230)
mas = tk.Button(ajustes_canva, text='+', font= 'Fixedsys 20',bg='grey', fg='black')
mas.place(x=220, y=230)
tiempo_turno = tk.Label(ajustes_canva, text= 'Tiempo por turno', font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
tiempo_turno.place(relx=0.5, y=325, anchor=tk.N)
slider_tiempo = tk.Scale(ajustes_canva, label="0", from_="1", to="180", width=20, length=300, showvalue=0, 
	orient=tk.HORIZONTAL, font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised',  command=lambda segundos: tiempo_en_min(int(segundos)))
slider_tiempo.set(90)
slider_tiempo.place(relx=0.5, y=380, anchor=tk.N)


def tiempo_en_min(segundos):
	if segundos%60//10 == 0 and segundos//60//10 == 0:
		slider_tiempo.configure(label=f"0{segundos//60}:0{segundos%60}")
	elif  segundos//60//10 == 0:
		slider_tiempo.configure(label=f"0{segundos//60}:{segundos%60}")
	elif  segundos%60//10 == 0:
		slider_tiempo.configure(label=f"{segundos//60}:0{segundos%60}")
	else:
		slider_tiempo.configure(label=f"{segundos//60}:{segundos%60}")


#Ventana salon de la fama
salon_canva = tk.Canvas(ventana1, width=700, height=447)


def exit_salon():
	salon_canva.pack_forget()
	pygame.mixer.Channel(0).stop()
	pygame.mixer.Channel(3).unpause()

def salon():

	salon_canva.delete('all')

	salon_canva.pack(side=tk.TOP, pady=100)

	fondo3 = Image.open("./imagenes/pared.png")
	f3 = ImageTk.PhotoImage(fondo3)
	fondo_salon = tk.Label(salon_canva, image=f3)
	fondo_salon.image = f3
	fondo_salon.place(x=0, y=0)

	mejores_txt = tk.Label(salon_canva, text= 'Mejores Tiempos', font= 'Fixedsys 25',bg='grey', fg='black', relief='raised')
	mejores_txt.place(relx=0.5, y=20, anchor=tk.N)

	salir_salon = tk.Button(salon_canva, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: exit_salon())
	salir_salon.place(x=10, y=10)

	with open('salon_fama.txt', 'r+') as salon_fama:
		lineas = salon_fama.readlines()
		play_btn = []
		for i in range(len(lineas)):
			datos = lineas[i].strip().split(',')
			posicion = tk.Label(salon_canva,  text= f"{i + 1}." , width=2, font= 'Fixedsys 25',bg='grey', fg='black', relief='raised')
			posicion.place(x=20, y=90 +70*(i))

			formato_tiempo = "00:00"
			minutos, segundos = int(datos[0])//60, int(datos[0])%60
			if segundos//10 == 0 and minutos//10 == 0:
				formato_tiempo= f"0{minutos}:0{segundos}"
			elif  minutos//10 == 0:
				formato_tiempo= f"0{minutos}:{segundos}"
			elif  segundos//10 == 0:
				formato_tiempo= f"{minutos}:0{segundos}"
			else:
				formato_tiempo= f"{minutos}:{segundos}"
			time = tk.Label(salon_canva,  text=formato_tiempo, width=6, font= 'Fixedsys 25',bg='grey', fg='black', relief='raised')
			time.place(x=75, y=90 +70*(i))

			play = tk.Button(salon_canva,  text="▷", width=3, font= 'Fixedsys 17',bg='grey', fg='black', relief='raised', command=lambda i=i:salon_play(lineas[i], i, play_btn))
			play.place(x=225, y=90 +70*(i))
			play_btn.append(play)

			imgJ_salon = Image.open(datos[2])
			resize_imgJ_salon = imgJ_salon.resize((50,50))
			imgJ_salon = ImageTk.PhotoImage(resize_imgJ_salon)

			label_imgJ_salon = tk.Label(salon_canva, image = imgJ_salon, height=50, width=50, borderwidth=0, highlightthickness=0)
			label_imgJ_salon.imgJ_salon = imgJ_salon
			label_imgJ_salon.place(x=285, y=90 +70*(i))

			name = tk.Label(salon_canva,  text=datos[1], font= 'Fixedsys 25',bg='grey', fg='black', relief='raised')
			name.place(x=335, y=90 +70*(i))

def salon_play(linea, i, play_btn):
	if play_btn[i].cget("text") == "▷":
		for play_btns in play_btn:
			if play_btns.cget("text") == "||":
				play_btns.configure(text="▷")
		play_btn[i].configure(text="||")
		datos = linea.strip().split(',')
		pygame.mixer.init()
		my_sound = pygame.mixer.Sound(datos[3])
		pygame.mixer.Channel(0).play(my_sound)
		my_sound.set_volume(0.7)
		pygame.mixer.Channel(3).pause()
	else:
		pygame.mixer.Channel(3).unpause()
		play_btn[i].configure(text="▷")
		pygame.mixer.Channel(0).pause()

#Ventana de ayuda
text_controles = """Teclas:
 - W: mover tanque hacia arriba
 - A: mover tanque hacia la izquierda
 - S: mover tanque hacia abajo
 - D: mover tanque hacia la derecha
 - Espacio: disparar
Resistencia bloques:
 - Concreto: 1 bomba, 2 bolas de fuego, 2 bolas de agua
 - Acero: 1 bomba, 1 bolas de fuego, 2 bolas de agua
 - Madera: 1 de cualquier tipo de poder
¿Cómo ganar? (según el rol)
 - Atacante: derrivando el aguila antes de que finalice
 el tiempo.
 - Defensor: si el aguila no fue derribada por el 
 atacante al finalizar el tiempo."""




#Titulo principal
tituloP = tk.Label (canva1, text = "Eagle Defender", font = "Fixedsys 80 ",bg= "grey", fg='black', relief= 'raised')
tituloP.place(relx=0.5, y=70, anchor=tk.N)

#Jugador 1
jugador1 = tk.Label (canva1, text = "Jugador 1", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
jugador1.place(x=200, y=100)
imgJ1 = Image.open("./imagenes/perfil_placeholder.png")
resize_imgJ1 = imgJ1.resize((50,50))
imgJ1 = ImageTk.PhotoImage(resize_imgJ1)

label_imgJ1 = tk.Label(canva1, image = imgJ1, height=50, width=50, borderwidth=0, highlightthickness=0)
label_imgJ1.imgJ1 = imgJ1
label_imgJ1.place(x=150, y=100)

#Jugador 2
jugador2 = tk.Label (canva1, text = "Jugador 2", font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
jugador2.place(x=1200, y=100)
imgJ2 = Image.open("./imagenes/perfil_placeholder.png")
resize_imgJ2 = imgJ2.resize((50,50))
imgJ2 = ImageTk.PhotoImage(resize_imgJ2)

label_imgJ2 = tk.Label(canva1, image = imgJ2, height=50, width=50, borderwidth=0, highlightthickness=0)
label_imgJ2.imgJ2 = imgJ2
label_imgJ2.place(x=1150, y=100)

# Boton para ir a la pantalla de juego
iniciar_juego = tk.Button(canva1, text='Iniciar Juego', font= 'Fixedsys 25',bg='grey', fg='black', command = lambda: iniciarJuego())
iniciar_juego.place(relx=0.5, y=225, anchor=tk.N)

#Boton de inicio de sesion
iniciar = tk.Button(canva1, text='Iniciar Sesión', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: inicio_sesion.pack(side=tk.TOP, pady=50))
iniciar.place(relx=0.5, y=325, anchor=tk.N)
salir_inicio = tk.Button(inicio_sesion, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: inicio_sesion.pack_forget())
salir_inicio.place(x=10, y=10)

#Boton de registro
registrarse = tk.Button(canva1, text= 'Registrarse', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: registro.pack(side=tk.TOP, pady=50))
registrarse.place(relx=0.5, y=425, anchor=tk.N)
salir_registro = tk.Button(registro, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: registro.pack_forget())
salir_registro.place(x=10, y=10)

#Boton salon de la fama
salon_fama = tk.Button(canva1, text='Salón de la fama', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: salon())
salon_fama.place(relx=0.5, y=525, anchor=tk.N)

#Boton de ajustes
ajust=tk.Button(canva1, text ="Ajustes", font ="Fixedsys 25", bg='grey', fg='black', command= lambda: ajustes_canva.pack(side= tk.TOP, pady=50))
ajust.place(relx=0.5, y=625, anchor=tk.N)
salir_ajustes=tk.Button(ajustes_canva, text= 'Volver', font= 'Fixedsys 16', bg='grey',fg='black', command= lambda: ajustes_canva.pack_forget())
salir_ajustes.place(x=10,y=10)

def jijijija():

	ayuda = tk.Canvas(ventana1, width=900, height=563)
	ayuda.pack(side= tk.TOP, pady=50)
	fondo_ayuda = tk.Label(ayuda, image= fondo2)
	fondo_ayuda.place(x=0, y=0)
	titulo_ayuda = tk.Label(ayuda, text='Controles de juego:',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
	titulo_ayuda.place(relx=0.5, y=30, anchor=tk.CENTER)
	controles = tk.Label(ayuda, text=text_controles, height=15, width=55, font= 'Fixedsys 17', justify=tk.LEFT, bg='grey', fg='black', relief= 'raised')
	controles.place(relx=0.5, y=70, anchor=tk.N)
	controles2 = tk.Label(ayuda, text="yes", height=15, width=55, font= 'Fixedsys 17', justify=tk.LEFT, bg='grey', fg='black', relief= 'raised')
	controles2.place(relx=0.5, y=700, anchor=tk.N)
	btn_previous = tk.Button(ayuda, text= 'Anterior', font= 'Fixedsys 16', bg='grey',fg='black', state=tk.DISABLED, command= lambda: siguiente_pag_controles(0, "previous"))
	btn_previous.place(relx=0.5, y=545, anchor=tk.E)
	btn_next = tk.Button(ayuda, text= 'Siguiente', font= 'Fixedsys 16', bg='grey',fg='black', command= lambda: siguiente_pag_controles(0, "next"))
	btn_next.place(relx=0.5, y=545, anchor=tk.W)

	def siguiente_pag_controles(i, btn):
		btn_previous.configure(state=tk.DISABLED)
		btn_next.configure(state=tk.DISABLED)
		for i in range(64):
			if btn == "next":
				controles2.place(relx=0.5, y=700 - i*10, anchor=tk.N)
			else:
				controles2.place(relx=0.5, y=70 + i*10, anchor=tk.N)

			time.sleep(0.001)
			ventana1.update()
		if btn == "next":
			btn_previous.configure(state=tk.NORMAL)
			btn_next.configure(state=tk.DISABLED)
		else:
			btn_previous.configure(state=tk.DISABLED)
			btn_next.configure(state=tk.NORMAL)
	ayuda_widgets = {
		"ayuda"		:	ayuda, 
		"controles2":	controles2, 
		"btn_previous":	btn_previous, 
		"btn_next"	:	btn_next
		}
	salir_ayuda=tk.Button(ayuda, text= 'Volver', font= 'Fixedsys 16', bg='grey',fg='black', command= lambda: salir_ventana_ayuda(ayuda_widgets))
	salir_ayuda.place(x=10,y=10)

#Boton de ayuda
ayud = tk.Button(canva1, text ="Ayuda", font ="Fixedsys 25", bg='grey', fg='black', command= lambda: jijijija())
ayud.place(relx=0.85, y=625, anchor=tk.N)

#para que al salir de la ventana de ayuda regrese a la primera pagina de la misma
def salir_ventana_ayuda(ayuda_widgets):
	ayuda_widgets["ayuda"].pack_forget()
	ayuda_widgets["controles2"].place(relx=0.5, y=700, anchor=tk.N)
	ayuda_widgets["btn_previous"].configure(state=tk.DISABLED)
	ayuda_widgets["btn_next"].configure(state=tk.NORMAL)

#Boton de salida
salirP=tk.Button(canva1, text = "Salir", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: on_closing())
salirP.place(x=95,y=30)

#jugar sin iniciar sesion
jugarR=tk.Button(canva1, text = "Jugar rapido", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: jugar_rapido())
jugarR.place(x=150,y=30)

#Ventana de inicio de sesion
select_rol = tk.Canvas(ventana1, width=900, height=563)
fondo_select_rol = tk.Label(select_rol, image= fondo2)
fondo_select_rol.place(x=0, y=0)
titulo_select = tk.Label(select_rol, text='Elija quién será el atacante:',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
titulo_select.place(x=105, y=100)





btn_jugar = tk.Button(select_rol, text='Jugar', font= 'Fixedsys 20',bg='grey', fg='black', command=lambda: jugar())
btn_jugar.place(x=400, y=450)

salir_select_rol = tk.Button(select_rol, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: select_rol.pack_forget())
salir_select_rol.place(x=10, y=10)

var_rol = tk.IntVar()

#Jugador 1
jugador1_rol = tk.Radiobutton (select_rol, text = usr1[0], variable=var_rol, selectcolor="#a27272", indicatoron=0,value=0,font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
jugador1_rol.place(x=360, y=210)
imgJ1_rol = Image.open(usr1[5])
resize_imgJ1_rol = imgJ1_rol.resize((50,50))
imgJ1_rol = ImageTk.PhotoImage(resize_imgJ1_rol)

label_imgJ1_rol = tk.Radiobutton(select_rol, image = imgJ1_rol, variable=var_rol, selectcolor="#a27272", indicatoron=0,value=0,height=59, width=59, borderwidth=0, highlightthickness=0)
label_imgJ1_rol.imgJ1_rol = imgJ1_rol
label_imgJ1_rol.place(x=300, y=210)

#Jugador 2
jugador2_rol = tk.Radiobutton (select_rol, text = usr2[0], variable=var_rol, selectcolor="#a27272", indicatoron=0,value=1,font = "Fixedsys 30 ",bg= "grey", fg='black', relief= 'raised')
jugador2_rol.place(x=360, y=280)
imgJ2_rol = Image.open(usr2[5])
resize_imgJ2_rol = imgJ2_rol.resize((50,50))
imgJ2_rol = ImageTk.PhotoImage(resize_imgJ2_rol)

label_imgJ2_rol = tk.Radiobutton(select_rol, image = imgJ2_rol, variable=var_rol, selectcolor="#a27272", indicatoron=0,value=1,height=59, width=59, borderwidth=0, highlightthickness=0)
label_imgJ2_rol.imgJ2_rol = imgJ2_rol
label_imgJ2_rol.place(x=300, y=280)

def iniciarJuego():
	if jugador1.cget("text") != "Jugador 1" and jugador2.cget("text") != "Jugador 2":

		select_rol.pack(side=tk.TOP, pady=50)
		jugador1_rol.configure(text=usr1[0])

		#Muestra la foto de perfil junto al nombre de usuario
		imgJ1_rol = Image.open(usr1[5])
		resize_imgJ1_rol = imgJ1_rol.resize((50,50))
		imgJ1_rol = ImageTk.PhotoImage(resize_imgJ1_rol)
		label_imgJ1_rol.imgJ1_rol = imgJ1_rol
		label_imgJ1_rol.configure(image=imgJ1_rol)


		jugador2_rol.configure(text=usr2[0])

		#Muestra la foto de perfil junto al nombre de usuario
		imgJ2_rol = Image.open(usr2[5])
		resize_imgJ2_rol = imgJ2_rol.resize((50,50))
		imgJ2_rol = ImageTk.PhotoImage(resize_imgJ2_rol)
		label_imgJ2_rol.imgJ2_rol = imgJ2_rol
		label_imgJ2_rol.configure(image=imgJ2_rol)

	else:
		messagebox.showerror("Error", "Dos jugadores deben haber iniciado sesión para iniciar el juego.")


def jugar():
	canal = pygame.mixer
	canva1.place_forget()
	select_rol.pack_forget()
	rol = {"atacante":"", "defensor":""}
	if var_rol.get() == 0:
		rol["atacante"], rol["defensor"] = usr1[0], usr2[0]
		ventanaJuego(ventana1, usr2, usr1, rol, canva1, canal)
	else:
		rol["atacante"], rol["defensor"] = usr2[0], usr1[0]
		ventanaJuego(ventana1, usr1, usr2, rol, canva1, canal, slider_tiempo.get())

def jugar_rapido():
	canal = pygame.mixer
	canva1.place_forget()
	rol = {"atacante":"Jugador 1", "defensor":"Jugador 2"}
	ventanaJuego(ventana1, usr1, usr2, rol, canva1, canal, slider_tiempo.get())






def on_closing():

	if messagebox.askokcancel("Salir", "¿Está seguro que quiere salir del juego?"):
		not_stopping = False
		pygame.mixer.quit()
		ventana1.destroy()

ventana1.protocol("WM_DELETE_WINDOW", on_closing)


#jugar_rapido()
ventana1.mainloop()