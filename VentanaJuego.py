import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk #pip install pillow
import time
import threading

# Variables
size_area_juego = {"width":600,"height":600}
matriz_cuadros = []
minutos, segundos = 1, 30
madera = 10
colocar_bloques = True

# Ventana Principal
ventana_juego = tk.Tk()

ventana_juego.geometry('1550x800')
ventana_juego.title("Eagle Defender")
ventana_juego.configure(bg = "gray")

# Contiene los bloque, cronometro y area de juego
canva_juego = tk.Canvas(ventana_juego, width = 1550, height = 800, bg = "gray")
canva_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# area de juego donde se van a colocar y los bloques 
area_juego = tk.Canvas(ventana_juego, width = size_area_juego["width"], height = size_area_juego["height"], bg = "#2a2a2a", highlightthickness=0)
area_juego.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Imagen de bloques de madera
img_madera = Image.open("./madera.png")
resize_image = img_madera.resize((50,50))
img = ImageTk.PhotoImage(resize_image)

bloques_madera = tk.Label(canva_juego, text=madera, font="Fixedsys 20",image = img, height=50, width=50, borderwidth=0,compound="center", highlightthickness=0)
bloques_madera.img_madera = img
bloques_madera.place(x=200, y=250)

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
# for i in matriz_cuadros:
# 	print(i)



def onclick(event):
	global madera#, colocar_bloques
	
	if madera > 0 and colocar_bloques:
		item = area_juego.find_closest(event.x, event.y)

		def find_item_location(item, matriz_cuadros):
			for i in range(len(matriz_cuadros)):
				for j in range(len(matriz_cuadros[i])):
					if matriz_cuadros[i][j] == item[0]:
						coords = area_juego.coords(matriz_cuadros[i][j])
						return coords
			return None
		madera-=1

		bloques_madera.configure(text=madera)

		ubicacion = find_item_location(item, matriz_cuadros)
		image = Image.open("./madera.png")
		resize_image = image.resize((dim_cuadros["y2"], dim_cuadros["x2"]))
		img = ImageTk.PhotoImage(resize_image)

		label = tk.Label(area_juego, image = img, height=dim_cuadros["x2"]-5, width=dim_cuadros["y2"]-5)
		label.image = img
		label.place(x=int(ubicacion[0])+1, y=int(ubicacion[1])+1)
	elif not colocar_bloques:
		messagebox.showinfo(title="Sin tiempo", message="El tiempo para colocar bloques a acabado")
	else:
		messagebox.showinfo(title="Sin madera", message="Ya no tiene más bloques de madera")


		
		
		 

	


area_juego.bind("<Button-1>", onclick)





ventana_juego.mainloop()