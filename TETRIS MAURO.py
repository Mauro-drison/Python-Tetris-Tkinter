import tkinter as tk
import random
from tkinter import messagebox

class ventana_principal():
    def __init__(self):
        self.ventana=tk.Tk()
        self.ventana.title("TETRIS DE MAURO")
        self.longitud_lados=30
        self.f = 20
        self.c = 12
        self.columna = self.c*self.longitud_lados
        self.fila = self.f*self.longitud_lados 
        #determinamos el tamaño de la ventana       
        self.canvas = tk.Canvas(self.ventana, width=self.columna, height=self.fila)
        self.canvas.grid(row=1, column=0)
        #lista con los objetos almacenados
        self.lista_de_bloques = []
        self.leabel = tk.Label(self.ventana, text="TRABAJO FINAL DE PRIMERO")
        self.leabel.grid(row=0, column=0)      
     
       
        self.figuras_del_tetris()        
        self.bloque_actual = None
        #la actualizacion del juego cada milisegundo 
        self.FPS = 250
        self.ventana.after(self.FPS, self.actualizar_juego)
        #lista de bloques donde se almacenen los diferentes bloques que caen al limite inferior        
        self.agregar_un_tablero_a_la_lista()
        self.dibujar_cuadrados_por_filas_columnas()
        #se colocan los teclados
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress-Left>", self.bloque_de_movimiento_horizontal)
        self.canvas.bind("<KeyPress-Right>", self.bloque_de_movimiento_horizontal)
        self.canvas.bind("<KeyPress-Up>", self.rotar_bloque)
        self.canvas.bind("<KeyPress-Down>", self.suelo)
        #se agrega un tablero vacio a la lista de bloques   
    def agregar_un_tablero_a_la_lista(self):
        for i in range(self.f):
            
            i_fila = ['' for j in range(self.c)]
            
            self.lista_de_bloques.append(i_fila)
    #1:dibujamos el tablero del juego usando solo filas y columnas fyc con el metodo canvas
    def dibujar_untablero_porfc(self, c, f, color="#CCCCCC"):
        #ubicacion
        x0 = c*self.longitud_lados
        y0 = f*self.longitud_lados
        #alto y ancho
        x1 = c*self.longitud_lados+self.longitud_lados
        y1 = f*self.longitud_lados+self.longitud_lados
        print(x0, y0)
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")
   
#viw se dibuja el tablero
    def dibujar_cuadrados_por_filas_columnas(self):
         
        for fl in range(self.f):
          
            for cl in range(self.c):               
               
                self.dibujar_untablero_porfc( cl, fl)


#estas son las formas distintas que van a tener los bloques del tetris, usamos diccionarios.
    def figuras_del_tetris(self):
        self.formast ={
            "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
            "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
            "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
            "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
            "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
            "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
            "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
        }
        self.color_formast = { 
            
            "O": "red",
            "Z": "Cyan",
            "S": "blue",
            "T": "yellow",
            "I": "green",
            "L": "purple",
            "J": "orange",
        }

#se crea la figura correspondiente
    def crear_figura(self,  c, f, lista_de_celdas, color="#CCCCCC"):
        for celda in lista_de_celdas:
    
            celda_c, celda_f = celda
            cl = celda_c + c
            fl = celda_f + f
             
            if 0 <= c < self.c and 0 <= f < self.f:
                
                self.dibujar_untablero_porfc( cl, fl, color)

#realiza el movimiento de la figura o el objeto
    def movimiento_de_figura(self, bloque, direccion=[0, 1]):

        #se crean los contenedores de las variables que vamos a utilizar
        self.forma_figura = bloque['tipo']
        self.ci, self.fi = bloque['cf'] 
        self.lista_de_celdas = bloque['lista_de_celdas']
        
        self.crear_figura( self.ci, self.fi, self.lista_de_celdas)
        
        #se dibuja una nueva figura de tetris en otra ubicacion
        self.dc, self.df = direccion
        self.nueva_columna, self.nueva_fila = self.ci + self.dc, self.fi + self.df
        bloque['cf'] = [self.nueva_columna, self.nueva_fila]
        self.crear_figura( self.nueva_columna, self.nueva_fila, self.lista_de_celdas,  self.color_formast[self.forma_figura])


#se realiza el chequeo para ver si la figura puede continuar o no puede conticuar
    def chequeo_movimiento(self, bloque, direccion=[0, 0]):

        cc, cf = bloque['cf']
        lista_de_celdas = bloque['lista_de_celdas']

        for celda in lista_de_celdas:
            celda_c, celda_f = celda
            c = celda_c + cc + direccion[0]
            f = celda_f + cf + direccion[1]
        #en esta parte verifica si el objeto llego a la parte de abajo 
            if c < 0 or c >= self.c or f >= self.f:
              
                return False
        
            if f >= 0 and self.lista_de_bloques[f][c]:
                return False
        
        return True

#se guardan los bloques en la lista donde los bloques llegan a la parte de abajo
    def guardar_bloques_lista(self, bloque):
        
        self.forma_figura = bloque['tipo']
        self.ci, self.fi = bloque['cf'] 
        self.lista_de_celdas = bloque['lista_de_celdas']
        
        for celdas in self.lista_de_celdas:
            celda_c, celda_f = celdas
            c = celda_c + self.ci
            f = celda_f + self.fi
            
            self.lista_de_bloques[f][c] = self.forma_figura


#mover horizontalmente el bloque
    def bloque_de_movimiento_horizontal(self, evento):
        self.direccion = [0, 0]
        if evento.keysym == 'Left':
            self.direccion = [-1, 0]
        elif evento.keysym == 'Right':
            self.direccion = [1, 0]
        else:
            return

        if self.bloque_actual is not None and self.chequeo_movimiento(self.bloque_actual, self.direccion):
            self.movimiento_de_figura( self.bloque_actual, self.direccion)

#------------------------------------------------------------------------------------------------------------------------------------------
#sirve para rotar los objetos
    def rotar_bloque(self, evento):
        
        if self.bloque_actual is None:
            return 
        
        #logra que el objeto pueda rotar
        self.lista_de_celdas = self.bloque_actual['lista_de_celdas']
        self.lista_de_rotacion = []
        for celdas in self.lista_de_celdas:
            celda_c, celda_f = celdas
            self.rotar_celda = [celda_f, -celda_c]
            self.lista_de_rotacion.append(self.rotar_celda)

        #bloquear despues de rotar
        self.bloque_despues_de_rotar = {
            'tipo': self.bloque_actual['tipo'], 
            'lista_de_celdas': self.lista_de_rotacion,
            'cf': self.bloque_actual['cf']
        }

        if self.chequeo_movimiento(self.bloque_despues_de_rotar):
            cc, cf = self.bloque_actual['cf']
            self.crear_figura( cc, cf, self.bloque_actual['lista_de_celdas'])
            self.crear_figura( cc, cf, self.lista_de_rotacion, self.color_formast[self.bloque_actual['tipo']])
            self.bloque_actual = self.bloque_despues_de_rotar

#-------------------------------------------------------------------------------------------------------------------------------------------
#sirve para que el bloque llegue a la parte de abajo, con mas velocidad 
    def suelo(self, evento):

        if self.bloque_actual is None:
            return

        self.lista_de_celdas = self.bloque_actual['lista_de_celdas']
        cc, cf = self.bloque_actual['cf']
        min_altura = 20

        for celdas in self.lista_de_celdas:
            celda_c, celda_f = celdas

            c, f = celda_c + cc, celda_f + cf
            
#            if self.lista_de_bloques[f][c]:
#                return
            h = 0

            for fi in range(f+1, self.f):
                if self.lista_de_bloques[fi][c]:
                    break

                else:
                    h += 1

            if h < min_altura:
                min_altura = h

        self.abajo = [0, min_altura]

        if self.chequeo_movimiento(self.bloque_actual, self.abajo):
            self.movimiento_de_figura( self.bloque_actual, self.abajo)    
#---------------------------------------------------------------------------------------------------------------------------------------
#generar objeto aleatorio
    def generar_nuevo_bloque(self):
        #para eligir la figura aleatoriamente
        self.tipo = random.choice(list(self.formast.keys()))
        #ubicacion en colunmas y filas
        self.cf = [self.c // 2, 0]
        #se genera el bloque aleatoriamente
        self.nuevo_bloque = {
            'tipo': self.tipo,
            'lista_de_celdas': self.formast[self.tipo],
            'cf': self.cf
        }

        return self.nuevo_bloque

#generar con este metodo un objeto aleatorio
    def actualizar_juego(self):
        self.ventana.update()
        if self.bloque_actual is None:
            self.nuevo_bloque = self.generar_nuevo_bloque()
            self.movimiento_de_figura(self.nuevo_bloque)
            self.bloque_actual = self.nuevo_bloque
            if not self.chequeo_movimiento(self.bloque_actual, [0, 0]):
                self.opcione_de_mensaje= messagebox.askretrycancel(message="¿Desea reintentar?", title="Título")
                if self.opcione_de_mensaje:
                    self.lista_de_bloques.clear()
                    self.agregar_un_tablero_a_la_lista()
                    self.dibujar_cuadrados_por_filas_columnas()
                    self.bloque_actual = None
                    self.ventana.after(self.FPS, self.actualizar_juego)

                else:
                    self.ventana.destroy()
                return
        else:
            
            if self.chequeo_movimiento(self.bloque_actual, [0, 1]):
                self.movimiento_de_figura(self.bloque_actual, [0, 1])
            else:
                self.guardar_bloques_lista(self.bloque_actual)
                self.bloque_actual = None

        self.ventana.after(self.FPS, self.actualizar_juego)

#se inicia la funcion
    def iniciar(self):
        self.ventana.mainloop()


ventanaPrincipal=ventana_principal()
ventanaPrincipal.iniciar()

