
		# TFF Ochoa
		
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageOps

import os # trabajar con directorios
import numpy as np
import matplotlib.pyplot as plt
import math


directorio_raiz = os.getcwd()
hayVis = 0; hayIr=0; hayWv=0; hayPrec=0; hayMap=0
num_imagenes = 0
canal_activo = 0 # 0: mapa_defecto, 1: vis, 2: ir, 3: wv, 4: prec, 5: map

root = Tk()
root.title('AVISPI - Asistente VISual para la Predicción Inmediata')
mainframe = ttk.Frame(root, padding = "3 3 12 12", width = 1500, height = 800)
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))

supframe = ttk.Frame(mainframe)
supframe.grid(column = 0, row = 0, sticky = (W,E))

latframe = ttk.Frame(mainframe)
latframe.grid(column=1, row=1, sticky = (N,S))

canvas = Canvas(mainframe, width = 1200, height = 637, background = "grey") # Antes 1000x750
canvas.grid(column=0, row=1)

root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)


lista_vis_img = []
lista_ir_img = []
lista_wv_img = []
lista_prec_img = []
longitudes = []

# Dibujos y nubes: una única función para dibujar con el ratón: nuevo_punto. Decide dónde ponerla en función de la variable punto.get().
# punto.get(): 0->dibujo, 1-> nube.
dibujos=[] # habrán dos funciones: nuevo_punto y dibujar (esta también considera nubes).
nubes=[[]] # se dibujan junto a dibujos[] en dibujar(). 1ª nub: a[0]. a= [[(x0,y0), (x1,y1){N0}], [(x0,y0), (x1,y1)]{N1} ].
n_nube=0 #Nube actual que se está dibujando.

def cargar_imagenes(): # devuelve: lista_vis[](ir, wv, prec, map), lista_vis_img[][] (ir, wv, prec), imgMapa.
	global hayVis
	hayVis=0
	global hayIr
	hayIr=0
	global hayWv
	hayWv=0
	global hayPrec
	hayPrec=0
	global hayMap
	hayMap=0
	global lista_vis_img
	lista_vis_img = []
	global lista_ir_img
	lista_ir_img = []
	global lista_wv_img
	lista_wv_img = []
	global lista_prec_img
	lista_prec_img = []
	global longitudes
	longitudes = []
	global imgMapa
	global num_imagenes
	
	
	imagenes_mal_cargadas=0
	
	lista_vis = os.listdir('VIS')
	lista_ir = os.listdir('IR')
	lista_wv = os.listdir('WV')
	lista_prec = os.listdir('PREC')
	lista_map = os.listdir('MAP') # solo se cargará el primero. Se crea esto para ver si hay algo en el directorio.
	
	if len(lista_vis)>0:
		hayVis = 1
		longitudes.append(len(lista_vis))
		os.chdir('VIS')
		for i in lista_vis:
			foto = Image.open(i)
			foto = ImageOps.fit(foto, (1200, 637))
			foto = ImageTk.PhotoImage(foto)
			lista_vis_img.append((foto, os.stat(i).st_birthtime))
		lista_vis_img.sort(key = lambda foto : foto[1])
		# hacer visible etiqueta "Visible"
		os.chdir(directorio_raiz)
	
	if len(lista_ir)>0:
		hayIr = 1
		longitudes.append(len(lista_ir))
		os.chdir('IR')
		for i in lista_ir:
			foto = Image.open(i)
			foto = ImageOps.fit(foto, (1200, 637))
			foto = ImageTk.PhotoImage(foto)
			lista_ir_img.append((foto, os.stat(i).st_birthtime))
		lista_ir_img.sort(key = lambda foto : foto[1])
		# hacer visible etiqueta "IR"
		os.chdir(directorio_raiz)
		
	if len(lista_wv)>0:
		hayWv = 1
		longitudes.append(len(lista_wv))
		os.chdir('WV')
		for i in lista_wv:
			foto = Image.open(i)
			foto = ImageOps.fit(foto, (1200, 637))
			foto = ImageTk.PhotoImage(foto)
			lista_wv_img.append((foto, os.stat(i).st_birthtime))
		lista_wv_img.sort(key = lambda foto : foto[1])
		# hacer visible etiqueta "WV"
		os.chdir(directorio_raiz)
		
	if len(lista_prec)>0:
		hayPrec = 1
		longitudes.append(len(lista_prec))
		os.chdir('PREC')
		for i in lista_prec:
			foto = Image.open(i)
			foto = ImageOps.fit(foto, (1200, 637))
			foto = ImageTk.PhotoImage(foto)
			lista_prec_img.append((foto, os.stat(i).st_birthtime))
		lista_prec_img.sort(key = lambda foto : foto[1])
		# hacer visible etiqueta "PREC"
		os.chdir(directorio_raiz)
	
	if len(lista_map)>0:
		hayMap = 1
		os.chdir('MAP')
		imgMapa = Image.open(lista_map[0])
		imgMapa = ImageOps.fit(imgMapa, (1200, 637))
		imgMapa = ImageTk.PhotoImage(imgMapa)
		canvas.delete('all') # https://stackoverflow.com/questions/15839491/how-to-clear-tkinter-canvas
		canvas.create_image(0, 0, image = imgMapa, anchor = 'nw' )
		# hacer visible etiqueta "MAP"
		os.chdir(directorio_raiz)
	if len(longitudes)>1:
		for i in range(len(longitudes)-2):
			if longitudes[i]<longitudes[i+1]:
				imagenes_mal_cargadas = 1
				messagebox.showwarning(message = 'No coincide la cantidad de imágenes introducidas en canales distintos. Imágenes no cargadas.')
				resetear()
	
	try:
		if isinstance(longitudes[0], int):
			num_imagenes = longitudes[0]
		else:
			num_imagenes = 0
	except IndexError:
		messagebox.showwarning(message = 'Longitudes[0] no es un entero. Comprobar imágenes cargadas en carpetas')
	
	if imagenes_mal_cargadas == 0:
		if hayMap == 1:
			canvas.delete('all')
			canvas.create_image(0, 0, image = imgMapa, anchor = 'nw' )
	
contador = 0 # cuenta la imagen por la que va la secuencia. Empieza por 0.	
def mostrar_vis():
	global contador
	global lista_vis_img # hacer lo mismo en los otros canales
	global canal_activo
	canal_activo=1
	
	if hayVis == 1:
		img = lista_vis_img[contador][0]# En "cargar" las imágenes se guardan ya ajustadas y en su formato.
		canvas.delete('all')
		canvas.create_image(0,0, image = img, anchor = 'nw')
	else:
		messagebox.showwarning(message = "No se han cargado imágenes visibles")
	
	dibujar()
	
def mostrar_ir():
	global contador
	global canal_activo
	canal_activo=2	
	
	if hayIr == 1:
		img = lista_ir_img[contador][0]# En "cargar" las imágenes se guardan ya ajustadas y en su formato.
		canvas.delete('all')
		canvas.create_image(0,0, image = img, anchor = 'nw')
	else:
		messagebox.showwarning(message = "No se han cargado imágenes infrarrojas")
		
	dibujar()
		
def mostrar_wv():
	global contador
	global canal_activo
	canal_activo=3
		
	if hayWv == 1:
		img = lista_wv_img[contador][0]# En "cargar" las imágenes se guardan ya ajustadas y en su formato.
		canvas.delete('all')
		canvas.create_image(0,0, image = img, anchor = 'nw')
	else:
		messagebox.showwarning(message = "No se han cargado imágenes de vapor de agua")
		
	dibujar()
		
def mostrar_prec():
	global contador
	global lista_prec_img
	global canal_activo
	canal_activo=4
		
	if hayPrec == 1:
		img = lista_prec_img[contador][0]# En "cargar" las imágenes se guardan ya ajustadas y en su formato.
		canvas.delete('all')
		canvas.create_image(0,0, image = img, anchor = 'nw')
	else:
		messagebox.showwarning(message = "No se han cargado imágenes de precipitación")
		
	dibujar()

def mostrar_map():
	global canal_activo
	canal_activo=5
	
	if hayMap == 1:
				canvas.delete('all')
				canvas.create_image(0,0, image = imgMapa, anchor = 'nw')
	else:
		messagebox.showwarning(message = "No se ha cargado mapa")
		
	dibujar()
		
def siguiente_img(event):
	global contador
	global canal_activo
	contador +=1
		
	try:
		contador = contador % num_imagenes
	except ZeroDivisionError:
		pass
	
	match canal_activo:
		case 0:
			imgMapa = Image.open('NoTocar/fondo.png')
			imgMapa = ImageOps.fit(imgMapa, (750, 750))
			imgMapa = ImageTk.PhotoImage(imgMapa)
			canvas.delete('all')
			canvas.create_image(0, 0, image = imgMapa, anchor = 'nw' )
		case 1:
			mostrar_vis()
		case 2:
			mostrar_ir()
		case 3:
			mostrar_wv()
		case 4:
			mostrar_prec()
		case 5:
			mostrar_map()
			contador -= 1
			try:
				contador = contador % num_imagenes
			except ZeroDivisionError:
				pass
		
	fija_hora('cadena_vacia')
				
				
def anterior_img(event):
	global contador
	global canal_activo
	contador -=1
		
	try:
		contador = contador % num_imagenes
	except ZeroDivisionError:
		pass
	
	match canal_activo:
		case 0:
			imgMapa = Image.open('NoTocar/fondo.png')
			imgMapa = ImageOps.fit(imgMapa, (750, 750))
			imgMapa = ImageTk.PhotoImage(imgMapa)
			canvas.delete('all')
			canvas.create_image(0, 0, image = imgMapa, anchor = 'nw' )
		case 1:
			mostrar_vis()
		case 2:
			mostrar_ir()
		case 3:
			mostrar_wv()
		case 4:
			mostrar_prec()
		case 5:
			mostrar_map()
			contador += 1
			try:
				contador = contador % num_imagenes
			except ZeroDivisionError:
				pass
	fija_hora('cadena_vacia')
	
# Dibujos y nubes: una única función para dibujar con el ratón: nuevo_punto. Decide dónde ponerla en función de la variable punto.get().
# 0->dibujo, 1-> nube.

def nueva_nube():
	global n_nube
	global nubes
	
	if len(nubes[n_nube]) == 0:
		pass
	else:
		nubes.append([])
		n_nube +=1

def nuevo_punto(event):
	global nubes
	global dibujos
	global punto
	global n_nube
	
	tipo_punto=punto.get()
	x0=y0=x1=y1=0
	x0, y0 = event.x-3, event.y-4 # Siempre ha estad x-2, y-2.
	x1, y1 = x0+4, y0+4
    
	if tipo_punto==0: #dibujo
		dibujos.append((x0, y0)) # ya se le han restado 2 píxeles.
		canvas.create_oval((x0,y0,x1,y1), fill='red', width=1)
	else: # Nube
		if len(nubes[n_nube])==0:
			nubes[n_nube].append((x0, y0)) # ya se le han restado 2 píxeles.
			canvas.create_oval((x0,y0,x1,y1), fill='yellow', width=1)
		else:
			nubes[n_nube].append((x0, y0)) # ya se le han restado 2 píxeles.
			canvas.create_oval((x0,y0,x1,y1), fill='green', width=1)			
				
canvas.bind("<Double-Button>", nuevo_punto)
	

def dibujar():
	global dibujos
	global nubes
	global n_nube
	global nubes_predichas
	
	for i in range(len(dibujos)):
		x=dibujos[i][0]
		y=dibujos[i][1]
		canvas.create_oval((x,y,x+4,y+4), fill='red', width=1)
		
	for i in range(len(nubes)):
		for j in range(len(nubes[i])):
			x=nubes[i][j][0]
			y=nubes[i][j][1]
			if j==0:
				canvas.create_oval((x,y,x+4,y+4), fill='yellow', width=1)
			else:
				canvas.create_oval((x,y,x+4,y+4), fill='green', width=1)
	if prediccion_hecha ==1:
		for i in range(1,len(nubes_predichas)):
			for j in range(len(nubes_predichas[i])):
				x=nubes_predichas[i][j][0]
				y=nubes_predichas[i][j][1]
				canvas.create_oval((x,y,x+4,y+4), fill='blue', width=1)

		
	
def borra_dibujo():
	global dibujos
	global longitudes
	
	dibujos=[]
	if len(longitudes)>0:
		actualiza_img()

def borra_nubes():
	global nubes
	global n_nube
	global longitudes
	
	nubes=[[]]
	n_nube=0
	if len(longitudes)>0:
		actualiza_img()

def borra_pred():
	global alfa
	global nubes_cerradas
	global nubes_predichas
	global parametros
	global prediccion_hecha
	global ro
	
	alfa = []
	nubes_cerradas = []
	nubes_predichas = []
	parametros = []
	prediccion_hecha = 0
	ro = []

def actualiza_img():
	global contador
	global canal_activo
		
	try:
		contador = contador % num_imagenes
	except ZeroDivisionError:
		pass
	
	match canal_activo:
		case 0:
			imgMapa = Image.open('NoTocar/fondo.png')
			imgMapa = ImageOps.fit(imgMapa, (750, 750))
			imgMapa = ImageTk.PhotoImage(imgMapa)
			canvas.delete('all')
			canvas.create_image(0, 0, image = imgMapa, anchor = 'nw' )
		case 1:
			mostrar_vis()
		case 2:
			mostrar_ir()
		case 3:
			mostrar_wv()
		case 4:
			mostrar_prec()
		case 5:
			mostrar_map()


def guardar_prediccion():
	messagebox.showinfo(message = "Por desarrollar")
	
def resetear():
	global hayVis
	hayVis=0
	global hayIr
	hayIr=0
	global hayWv
	hayWv=0
	global hayPrec
	hayPrec=0
	global hayMap
	hayMap=0

	global lista_vis_img
	lista_vis_img = []
	global lista_ir_img
	lista_ir_img = []
	global lista_wv_img
	lista_wv_img = []
	global lista_prec_img
	lista_prec_img = []
	global longitudes
	longitudes = []
	
	global imgMapa
	imgMapa = Image.open('NoTocar/fondo.png')
	imgMapa = ImageOps.fit(imgMapa, (1200, 637))
	imgMapa = ImageTk.PhotoImage(imgMapa)
	canvas.delete('all')
	canvas.create_image(0, 0, image = imgMapa, anchor = 'nw' )
	
	try:
		os.chdir('VIS')
		os.remove('.DS_Store')
	except FileNotFoundError:
		pass
	os.chdir(directorio_raiz)

	try:
		os.chdir('IR')
		os.remove('.DS_Store')
	except FileNotFoundError:
		pass
	os.chdir(directorio_raiz)
	
	try:
		os.chdir('WV')
		os.remove('.DS_Store')
	except FileNotFoundError:
		pass
	os.chdir(directorio_raiz)

	try:
		os.chdir('PREC')
		os.remove('.DS_Store')
	except FileNotFoundError:
		pass
	os.chdir(directorio_raiz)

	try:
		os.chdir('MAP')
		os.remove('.DS_Store')
	except FileNotFoundError:
		pass
	os.chdir(directorio_raiz)
	
	borra_dibujo()
	borra_nubes()
	borra_pred()
	cargar_imagenes()
	
	print('-------------------')


# Selección de canal:
canalframe = ttk.Frame(latframe)
canalframe.grid(column = 0, row = 0)
Label(canalframe, text='Sel. capa').pack(anchor='w')

canal=IntVar()
Radiobutton(canalframe, text='Vis', variable = canal, value = 1, command = mostrar_vis).pack(anchor='w')
Radiobutton(canalframe, text='IR', variable = canal, value = 2, command = mostrar_ir).pack(anchor='w')
Radiobutton(canalframe, text='WV', variable = canal, value = 3, command = mostrar_wv).pack(anchor='w')
Radiobutton(canalframe, text='Prec', variable = canal, value = 4, command = mostrar_prec).pack(anchor='w')
Radiobutton(canalframe, text='Map', variable = canal, value = 5, command = mostrar_map).pack(anchor='w')


# Selección tipo punto:
puntoframe = ttk.Frame(latframe)
puntoframe.grid(column=0, row=1)
Label(puntoframe, text='Tipo punto').pack(anchor='w')

punto=IntVar()
Radiobutton(puntoframe, text='Dibujo', variable = punto, value = 0).pack(anchor='w')
Radiobutton(puntoframe, text='Nube', variable = punto, value = 1).pack(anchor='w')

boton_NuevaNube = ttk.Button(puntoframe, text='Nueva Nube', command = nueva_nube).pack(anchor='w')
boton_Borra_Dibujo = ttk.Button(puntoframe, text='Borra dibujo', command = borra_dibujo).pack(anchor='w')
boton_Borra_Nube = ttk.Button(puntoframe, text='Borra nubes', command = borra_nubes).pack(anchor='w')


# Panel superior:
horaframe = ttk.Frame(supframe)
horaframe.grid(column=0, row=0)
	
	
Label(horaframe, text='Hora 1ª obs.:').grid(column=0, row=0)
hora = StringVar()
horaEntry = Entry(horaframe, textvariable = hora, width = 5)
horaEntry.grid(column=1, row=0)

Label(horaframe, text='Intervalo (minutos):').grid(column=3, row=0)
intervalo = StringVar()
intervaloEntry = Entry(horaframe, textvariable = intervalo, width = 3)
intervaloEntry.grid(column=4, row=0)

muestrahora=StringVar()
horaLabel = Label(horaframe, textvariable = muestrahora).grid(column=5, row=0)
muestrahora.set('hh:mm')

def fija_hora(cadena_vacia): # internamente, la hora será 60*h + m
	global muestrahora
	global intervalo
	global hora
	
	h = hora.get()
	if len(h) == 5:
		try:
			hora_interna = (int(h[0])*10 + int(h[1]))*60 + int(h[3])*10 + int(h[4])
			hora_interna = hora_interna + int(intervalo.get())*(contador)
			horas = str(int(hora_interna / 60))
			minutos = str(hora_interna % 60)
			if len(horas)==1:
				horas = '0' + horas
			if len(minutos)==1:
				minutos = '0'+ minutos
			hora_interna = horas + ':' + minutos
			muestrahora.set(hora_interna)
		except ValueError:
			messagebox.showwarning(message="Hora o intervalo incorrecto.")
			
prediccion_hecha=0
nubes_cerradas=[]
alfa=[]
ro=[]
parametros=[]
nubes_predichas = []

def media_angulos(lista):
	if len(lista)>0:
		senSum = sum([np.sin(a) for a in lista])
		cosSum = sum([np.cos(a) for a in lista])
		return math. atan2(senSum, cosSum)

def agrad(rad): # Lista
	return [180*r/np.pi for r in rad]

def predecir():
	# Comprueba que no se haya realizado ninguna predicción previa
	# No permite introducir nuevas nubes.
	# Comprueba que todas las listas de nubes tienen al menos dos elementos. No, pero solo predice las que tengan dos.
	# Por cada lista de nubes crea listas: alfa[], ro[] (con un elemento menos que la correspondiente lista de nubes).
	# Crea única lista de predicciones.
	# Añade a la lista una predicción.
	# Dibuja la predicción.
	global alfa
	global ro
	global parametros
	global prediccion_hecha
	global nubes_cerradas
	global nubes
	global nubes_predichas
	
	if prediccion_hecha==0:
		n_nubes = len(nubes)
	else:
		n_nubes = len(nubes_cerradas)
		
	if prediccion_hecha==0:
		nubes_cerradas=[]
		for i in range(n_nubes):
			if len(nubes[i])>1:
				nubes_cerradas.append(nubes[i]) # a partir de ahora solo se tendrán en cuenta estas nubes, aunque se dibujen otras.
		n_nubes=len(nubes_cerradas)
		if n_nubes == 0:
			messagebox.showwarning(message='No hay nubes cargadas. Dibuje nubes.')
			return
		# ahora solo hay una matriz no vacía de nubes en la que todas las nubes tienen dos o más elementos. n_nubes es la cantidad de nubes (empezando por 1).
		# nubes_cerradas n_nubes TRABAJAR SOLO CON ESTO.

	
	if prediccion_hecha==0: # crear listas rumbos y distancias
		alfa = []
		ro = []
		nubes_predichas.append([])
		for i in range(n_nubes):
			alfa.append([])
			ro.append([])
			nubes_predichas[0].append(nubes_cerradas[i][len(nubes_cerradas[i])-1]) # Las primeras nubes de la matriz de predicción no deben dibujarse.
			for j in range(len(nubes_cerradas[i]) - 1):
				dx = nubes_cerradas[i][j+1][0] - nubes_cerradas[i][j][0]
				dy = nubes_cerradas[i][j+1][1] - nubes_cerradas[i][j][1]
				if dx>0:
					alfa[i].append(np.pi/2 + np.arctan(dy/dx))
				if dx < 0:
					alfa[i].append(np.pi/2 + np.arctan(dy/dx) + np.pi) # en los cuadrantes 3 y 4, la fórmula del caso dx>0 cuenta ángulos desde 180º.
				if dx == 0:
					if dy < 0:
						alfa[i].append(0)
					else:
						alfa[i].append(np.pi)
				ro[i].append(np.sqrt(dx**2 + dy**2))
		# Calcula valores medios de alfa y ro. Los guarda en parametros=[(a0, r0, da0), (a1, r1, da1),  ...]:
		for i in range(n_nubes):
			#m_a = media_angulos(alfa[i]) #  mean[0,350]->175 Mejor coger el último álgulo, dibujando los puntos con espacio suficiente para evitar sensibilidad.
			a_final = alfa[i][len(alfa[i])-1]
			m_r = np.mean(ro[i])
			da = []
			if len(nubes_cerradas[i]) > 2:
				for j in range(len(ro[i])-1):
					da.append((alfa[i][j+1]-alfa[i][j])%(2*np.pi))
					da_final = media_angulos(da)
					#da_final = (np.pi/5) # da de pruebas
				print('alfa:' + str(agrad(alfa[i])))
				print('da:'+ str(agrad(da)))
				print('da_final: '+ str(da_final*180/np.pi))
			else:
				da_final = 0
					
			parametros.append((a_final, m_r, da_final))
	
	# La matriz de predicciones se actualiza, haya predicción previa o no. En este punto no debe estar vacía.
	p = []
	p_0 = nubes_predichas[len(nubes_predichas)-1] 
	for i in range(n_nubes): # p = p_0 + vector_rumbo_distancia
		t = len(nubes_predichas) # tiempo para a_1 = a_0 + da*t
		x = p_0[i][0]
		y = p_0[i][1]
		a = parametros[i][0]
		r = parametros[i][1]
		da = parametros[i][2]
		
		dx = r*np.cos(np.pi/2 - a - da*t)
		dy = -r*np.sin(np.pi/2 - a - da*t)
		p.append((x + dx, y + dy))

	nubes_predichas.append(p)
	prediccion_hecha = 1
		
	dibujar()
	
ttk.Button(latframe, text='Predicción', command = predecir).grid(column=0, row = 5)
ttk.Button(latframe, text='Reset', command = resetear).grid(column=0, row = 6)


horaEntry.bind('<Return>', fija_hora)
intervaloEntry.bind('<Return>', fija_hora)

root.bind('<Right>', siguiente_img)
root.bind('<Left>', anterior_img)

resetear()
cargar_imagenes()


root.mainloop()
