import tkinter as tk
#Ventana Pricipal
ventana1 = tk.Tk()

ventana1.geometry('1550x800')
ventana1.title("Eagle Defender")
ventana1.configure(bg = "green")

#Canva principal
canva1 = tk.Canvas(ventana1, width = 1550, height = 800, bg = "green")
canva1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#Fondo principal
fondo1 = tk.PhotoImage(file = "fondo1.PNG")
fondoP = tk.Label(canva1, image = fondo1)
fondoP.place(x=0, y=0)

#Ventana de inicio de sesion
inicio_sesion = tk.Canvas(ventana1, width=900, height=563)
fondo2 = tk.PhotoImage(file='inicio.png')
fondo_inicio = tk.Label(inicio_sesion, image= fondo2)
fondo_inicio.place(x=0, y=0)
nombre_txt = tk.Label(inicio_sesion, text='Nombre de usuario:',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
nombre_txt.place(x=268, y=100)
entrada_nommbre = tk.Entry(inicio_sesion,font= "Fixedsys 25", bg= 'grey', width=20, relief="sunken")
entrada_nommbre.place(x=255, y=175)
clave_txt = tk.Label(inicio_sesion, text='Contrseña:',font= 'Fixedsys 25', bg='grey', fg='black', relief= 'raised')
clave_txt.place(x=350, y=300)
entrada_clave = tk.Entry(inicio_sesion,font= "Fixedsys 25", bg= 'grey', width=20, relief="sunken", show='*')
entrada_clave.place(x=255, y=375)

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
foto = tk.Button(registro, text='Agregar fotografía', font= 'Fixedsys 20',bg='grey', fg='black')
foto.place(x=500, y=145)
cancion = tk.Button(registro, text='Canción favorita', font= 'Fixedsys 20',bg='grey', fg='black')
cancion.place(x=518, y=225)
redes = tk.Button(registro, text='Conectar redes sociales', font= 'Fixedsys 20',bg='grey', fg='black')
redes.place(x=470, y=305)

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
tituloP.place(x=430, y=100)

#Boton de inicio de sesion
iniciar = tk.Button(canva1, text='Iniciar Sesión', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: inicio_sesion.pack(side=tk.TOP, pady=50))
iniciar.place(x=605, y=300)
salir_inicio = tk.Button(inicio_sesion, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: inicio_sesion.pack_forget())
salir_inicio.place(x=10, y=10)

#Boton de registro
registrarse = tk.Button(canva1, text= 'Registrarse', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: registro.pack(side=tk.TOP, pady=50))
registrarse.place(x=640, y=400)
salir_registro = tk.Button(registro, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: registro.pack_forget())
salir_registro.place(x=10, y=10)

#Boton salon de la fama
salon_fama = tk.Button(canva1, text='Salón de la fama', font= 'Fixedsys 25',bg='grey', fg='black', command= lambda: salon_canva.pack(side=tk.TOP, pady=100))
salon_fama.place(x=590, y=500)
salir_salon = tk.Button(salon_canva, text = "Volver", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: salon_canva.pack_forget())
salir_salon.place(x=10, y=10)

#Boton de ajustes
ajust=tk.Button(canva1, text ="Ajustes", font ="Fixedsys 25", bg='grey', fg='black', command= lambda: ajustes_canva.pack(side= tk.TOP, pady=50))
ajust.place(x=680, y=600)
salir_ajustes=tk.Button(ajustes_canva, text= 'Volver', font= 'Fixedsys 16', bg='grey',fg='black', command= lambda: ajustes_canva.pack_forget())
salir_ajustes.place(x=10,y=10)

#Boton de salida
salirP=tk.Button(canva1, text = "Salir", font = "Fixedsys 16",bg='grey', fg='black', command = lambda: ventana1.destroy())
salirP.place(x=20,y=10)









ventana1.mainloop()