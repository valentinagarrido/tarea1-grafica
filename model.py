# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:26:55 2021

@author: hgcol
"""

import glfw
import numpy as np
import grafica.transformations as tr
from random import random
from random import randint

class Hinata():
    # Clase que contiene al modelo de Hinata
    def __init__(self, size, P):
        self.pos = [0,-0.7] # Posicion en el escenario
        self.model = None # Referencia al grafo de escena asociado
        self.controller = None # Referencia del controlador, para acceder a sus variables
        self.size = size # Escala a aplicar al nodo 
        self.radio = 0.1 # distancia para realizar los calculos de colision
        self.status = "Healthy"
        self.life = 1
        self.P = P

    def set_model(self, new_model):
        # Se obtiene una referencia a uno nodo
        self.model = new_model

    def set_controller(self, new_controller):
        # Se obtiene la referncia al controller
        self.controller = new_controller

    def update(self,delta):
        # Se actualiza la posicion del auto

        # Si detecta la tecla [right] presionada se mueve hacia la derecha
        if self.controller.is_right_pressed and self.pos[0] < 0.5:
            self.pos[0] += delta
        # Si detecta la tecla [left] presionada se mueve hacia la izquierda
        if self.controller.is_left_pressed and self.pos[0] > -0.5:
            self.pos[0] -= delta
        # Si detecta la tecla [up] presionada
        if self.controller.is_up_pressed and self.pos[1] <= 1:
            self.pos[1] += delta
        # Si detecta la tecla [down] presionada
        if self.controller.is_down_pressed and self.pos[1] >= -1:
            self.pos[1] -= delta
        #print(self.pos[0], self.pos[1])

        # Se le aplica la transformacion de traslado segun la posicion actual
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1], 0), tr.scale(self.size, self.size, 1)])
        if self.status == "Infected":
            self.life -= self.P*delta
        if self.life <= 0:
            self.status = "Dead"
            
    def collision(self, enemies):
        # Funcion para detectar las colisiones con las cargas

        # Se recorren las cargas 
        for enemy in enemies:
            # si la distancia a la carga es menor que la suma de los radios ha ocurrido en la colision
            if (self.radio+enemy.radio)**2 > ((self.pos[0]- enemy.pos[0])**2 + (self.pos[1]-enemy.pos[1])**2):
                self.status = enemy.status
                return
            
class Background():
    def __init__(self):
        self.model = None
        self.pos = [0,0]

    def set_model(self,new_model):
        self.model = new_model
        
    def update(self,delta):
        self.pos[1] -= delta/2
        if self.pos[1] <= -2:
            self.pos[1] = 0
        self.model.transform = tr.translate(self.pos[0], self.pos[1], 0)
        
class Zombie():
    def __init__(self,size):
        self.size = size
        self.model = None
        self.pos = [random()-0.5,random()*0.4+0.6]
        self.radio = 0.1
        self.status = "Dead"
        
    def set_model(self,new_model):
        self.model = new_model
        
    def update(self,delta):
        self.pos[1] -= delta/2
        self.model.transform = tr.matmul([tr.translate(self.pos[0],self.pos[1],0),
                                          tr.scale(self.size,self.size,1)])
        
class Human():
    def __init__(self,size,P):
        self.size = size
        self.model = None
        self.pos = [random()-0.5,random()*0.3+0.7]
        self.radio = 0.1
        self.status = None
        self.life = 1
        self.P = P
        
    def set_model(self,new_model):
        self.model = new_model
        
    def update(self,delta):
        self.pos[1] -= delta/2
        self.model.transform = tr.matmul([tr.translate(self.pos[0],self.pos[1],0),
                                          tr.scale(self.size,self.size,1)])
        if self.status == "Infected":
            self.life -= self.P*delta
        if self.life <= 0:
            self.status = "Dead"
        
    def set_status(self):
        r = randint(0,1)
        if r == 0:
            self.status = "Healthy"
        else:
            self.status = "Infected"
        
class Store():
    def __init__(self):
        self.model = None
        self.pos = [-0.78, 0.7]
        self.radio = 0.3
        self.status = "Won"
        
    def set_model(self,new_model):
        self.model = new_model
        
    def update(self):
        self.model.transform = tr.matmul([tr.translate(self.pos[0], self.pos[1],0), 
                                          tr.scale(0.5, 0.5, 1)])
        