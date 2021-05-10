# -*- coding: utf-8 -*-
"""
Created on Wed May  5 23:21:37 2021

@author: hgcol
"""

# coding=utf-8
"""Texture Quad in 2D"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import green_shader as gs
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
from model import *
import sys


inp = sys.argv
# el juego durará 1 minuto
t_total = 60
Z = int(inp[1])
H = int(inp[2])
T = int(inp[3])
P = float(inp[4])

# Se crea una clase de controlador para la aplicación
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False
        self.is_v_pressed = False
        self.end = False
        self.completed = False


# global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
#############################################################################################
    # Se agregan nuevas teclas para controlar
    elif key == glfw.KEY_RIGHT:
        if action ==glfw.PRESS:
            controller.is_right_pressed = True
        elif action == glfw.RELEASE:
            controller.is_right_pressed = False
    
    elif key == glfw.KEY_LEFT:
        if action ==glfw.PRESS:
            controller.is_left_pressed = True
        elif action == glfw.RELEASE:
            controller.is_left_pressed = False
        
    elif key == glfw.KEY_UP:
        if action ==glfw.PRESS:
            controller.is_up_pressed = True
        elif action == glfw.RELEASE:
            controller.is_up_pressed = False
    
    elif key == glfw.KEY_DOWN:
        if action ==glfw.PRESS:
            controller.is_down_pressed = True
        elif action == glfw.RELEASE:
            controller.is_down_pressed = False
            
    elif key == glfw.KEY_V:
        if action ==glfw.PRESS:
            controller.is_v_pressed = True
        elif action == glfw.RELEASE:
            controller.is_v_pressed = False
    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Se crea la ventana
    width = 600
    height = 600

    window = glfw.create_window(width, height, "Beauchefville", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Se agrega la función on_key
    glfw.set_key_callback(window, on_key)


    # Se crean los pipelines que se utilizarán
    pipeline = es.SimpleTransformShaderProgram()
    tex_pipeline = es.SimpleTextureTransformShaderProgram()
    green_tex_pipeline = gs.GreenTextureTransformShaderProgram()
    


    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)
    
    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Se crean las formas en la memoria de GPU y se agregan las figuras estáticas a los nodos
    
    background = bs.createTextureQuad(1, 1)
    gpuBackground = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuBackground)
    gpuBackground.fillBuffers(background.vertices, background.indices, GL_STATIC_DRAW)
    gpuBackground.texture = es.textureSimpleSetup(
        getAssetPath("street.png"), GL_CLAMP_TO_EDGE, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    backgroundNode1 = sg.SceneGraphNode("background1")
    backgroundNode1.transform = tr.scale(2.0,2.0,1.0)
    backgroundNode1.childs = [gpuBackground]
    
    
    background2Node = sg.SceneGraphNode("background2")
    background2Node.transform = tr.matmul([tr.translate(0,2,0),tr.scale(2.0,2.0,1.0)])
    background2Node.childs = [gpuBackground]
    
    fullBackgroundNode = sg.SceneGraphNode("fullBackground")
    fullBackgroundNode.childs = [backgroundNode1, background2Node]


    hinata = bs.createTextureQuad(1, 1)
    gpuHinata = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuHinata)
    gpuHinata.fillBuffers(hinata.vertices, hinata.indices, GL_STATIC_DRAW)
    gpuHinata.texture = es.textureSimpleSetup(
        getAssetPath("girl.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    hinataNode = sg.SceneGraphNode("hinata")
    hinataNode.childs = [gpuHinata]
    
    zombie = bs.createTextureQuad(1, 1)
    gpuZombie = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuZombie)
    gpuZombie.fillBuffers(zombie.vertices, zombie.indices, GL_STATIC_DRAW)
    gpuZombie.texture = es.textureSimpleSetup(
        getAssetPath("zombie.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    zombiesNode = sg.SceneGraphNode("zombies")
    # se crea una lista para almacenar posteriormente los modelos de zombies
    zombiesList = []
    
    human = bs.createTextureQuad(1, 1)
    gpuHuman = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuHuman)
    gpuHuman.fillBuffers(human.vertices, human.indices, GL_STATIC_DRAW)
    gpuHuman.texture = es.textureSimpleSetup(
        getAssetPath("boy.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    humansNode = sg.SceneGraphNode("humans")
    # se crea una lista para almacenar posteriormente los modelos de humanos
    humansList = []

    # se crea nodo de escena, que contiene todos los elementos que siempre estarán en la escena
    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [fullBackgroundNode, hinataNode, zombiesNode, humansNode]

    # se crea modelo de Hinata y se le setea modelo y controlador
    player = Hinata(0.2, P)
    player.set_model(hinataNode)
    player.set_controller(controller)
    
    # se crea modelo de fondo dinámico y se setea
    movingBackground = Background()
    movingBackground.set_model(fullBackgroundNode)

    # se crean nodos aparte de la escena para mensajes de "game over", "you win" y para la tienda

    end = bs.createTextureQuad(1, 1)
    gpuEnd = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuEnd)
    gpuEnd.fillBuffers(end.vertices, end.indices, GL_STATIC_DRAW)
    gpuEnd.texture = es.textureSimpleSetup(
        getAssetPath("end.jpg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    endNode = sg.SceneGraphNode("end")
    endNode.transform = tr.scale(2,2,1)
    endNode.childs = [gpuEnd]
    
    win = bs.createTextureQuad(1, 1)
    gpuWin = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuWin)
    gpuWin.fillBuffers(win.vertices, win.indices, GL_STATIC_DRAW)
    gpuWin.texture = es.textureSimpleSetup(
        getAssetPath("win.jpg"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    winNode = sg.SceneGraphNode("win")
    winNode.transform = tr.scale(2,2,1)
    winNode.childs = [gpuWin]
    
    redQuad = bs.createColorQuad(1,0,0)
    gpuRedQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRedQuad)
    gpuRedQuad.fillBuffers(redQuad.vertices, redQuad.indices, GL_STATIC_DRAW)
    
    brownQuad = bs.createColorQuad(0.5,0.25,0)
    gpuBrownQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownQuad)
    gpuBrownQuad.fillBuffers(brownQuad.vertices, brownQuad.indices, GL_STATIC_DRAW)
    
    greyQuad = bs.createColorQuad(0.5,0.5,0.5)
    gpuGreyQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreyQuad)
    gpuGreyQuad.fillBuffers(greyQuad.vertices, greyQuad.indices, GL_STATIC_DRAW)
    
    blueQuad = bs.createColorQuad(0.68,0.85,0.9)
    gpuBlueQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlueQuad)
    gpuBlueQuad.fillBuffers(blueQuad.vertices, blueQuad.indices, GL_STATIC_DRAW)

    scaledRedQuadNode = sg.SceneGraphNode("scaledRedQuad")
    scaledRedQuadNode.transform = tr.scale(0.6,1.1,1)
    scaledRedQuadNode.childs = [gpuRedQuad]
    
    scaledBrownQuadNode = sg.SceneGraphNode("scaledBrownQuad")
    scaledBrownQuadNode.transform = tr.matmul([tr.translate(0.12,0,0), tr.scale(0.35,0.25,1)])
    scaledBrownQuadNode.childs = [gpuBrownQuad]
    
    scaledGreyQuadNode = sg.SceneGraphNode("scaledGreyQuad")
    scaledGreyQuadNode.transform = tr.matmul([tr.translate(-0.35,0,0), tr.scale(0.3,1.1,1)])
    scaledGreyQuadNode.childs = [gpuGreyQuad]
    
    scaledBlueQuad1Node = sg.SceneGraphNode("scaledBlueQuad1")
    scaledBlueQuad1Node.transform = tr.matmul([tr.translate(0.05,0.3,0), tr.scale(0.2,0.2,1)])
    scaledBlueQuad1Node.childs = [gpuBlueQuad]
    
    scaledBlueQuad2Node = sg.SceneGraphNode("scaledBlueQuad2")
    scaledBlueQuad2Node.transform = tr.matmul([tr.translate(0.05,-0.3,0), tr.scale(0.2,0.2,1)])
    scaledBlueQuad2Node.childs = [gpuBlueQuad]
    
    storeNode = sg.SceneGraphNode("store")
    storeNode.childs += [scaledRedQuadNode, scaledBrownQuadNode, scaledGreyQuadNode,
                         scaledBlueQuad1Node, scaledBlueQuad2Node]
    
    # se crea modelo de tienda, se setea y se actualiza
    realStore = Store()
    realStore.set_model(storeNode)
    realStore.update()
    
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)    
    t0 = glfw.get_time()
    
    
    
    while not glfw.window_should_close(window):
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        if t0 >= t_total:
            controller.completed = True
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        
        # se actualiza la posición del fondo si el juego no ha terminado
        if (not controller.end) and (not controller.completed):
            movingBackground.update(delta)
        player.update(delta)
        
        # si el tiempo corresponde y el jeugo continúa, se crean Z zombies y H humanos
        # se crean modelos para zombies y humanos y se agregan a las listas
        
        if (t0%T < 0.0015) and (not controller.end) and (not controller.completed):
            print(t0)
            for i in range(Z):
                zombieNode = sg.SceneGraphNode("zombie")
                zombieNode.childs = [gpuZombie]
                zombiesNode.childs += [zombieNode]
                z = Zombie(0.2)
                z.set_model(zombieNode)
                zombiesList += [z]
            for i in range(H):
                humanNode = sg.SceneGraphNode("human")
                humanNode.childs = [gpuHuman]
                humansNode.childs += [humanNode]
                h = Human(0.2, P)
                h.set_model(humanNode)
                h.set_status()
                humansList += [h]
            
        # se actualizan los zombies/humanos y se eliminan para liberar memoria        
        for z in zombiesList:
            if z.pos[1] <= -1:
                zombiesNode.childs.remove(z.model)
                zombiesList.remove(z)
            z.update(delta)           
                
        for h in humansList:
            if h.pos[1] <= -1:
                humansNode.childs.remove(h.model)
                humansList.remove(h)
            if h.status == "Dead":
                zombieNode = sg.SceneGraphNode("zombie")
                zombieNode.childs = [gpuZombie]
                zombiesNode.childs += [zombieNode]
                humansNode.childs.remove(h.model)
                h.set_model(zombieNode)
                humansList.remove(h)
                zombiesList += [h]
            h.update(delta)

        # se hace colisionar al jugador con zombies y humanos
        player.collision(zombiesList + humansList)
        
        # se termina el juego si es que el jugador muere (se transforma en zombie)
        if player.status == "Dead":
            controller.end = True
        
        # Se señala el shader que se utulizarán para dibujar el grafo de escena
        glUseProgram(tex_pipeline.shaderProgram)
        
        # se dibuja
        sg.drawSceneGraphNode(sceneNode, tex_pipeline, "transform")
        
        # si se presiona la tecla V, se visualizan los humanos infectados de color verde
        # utilizando otro shader
        
        if controller.is_v_pressed:
            if player.status == "Infected":
                glUseProgram(green_tex_pipeline.shaderProgram)
                sg.drawSceneGraphNode(player.model, green_tex_pipeline, "transform")
            for h in humansList:
                if h.status == "Infected":
                    glUseProgram(green_tex_pipeline.shaderProgram)
                    sg.drawSceneGraphNode(h.model, green_tex_pipeline, "transform")
        # si el juego termina (jugador es zombie) se dibuja el nodo correspondiente
        if controller.end:
            sg.drawSceneGraphNode(endNode, tex_pipeline, "transform")
        # si el juego se completa se dibuja la tienda
        # si el jugador toca la tienda, el juego termina y se dibuja el nodo correspondiente
        elif controller.completed:
            glUseProgram(pipeline.shaderProgram)
            sg.drawSceneGraphNode(storeNode, pipeline, "transform")
            player.collision([realStore])
            if player.status == "Won":
                glUseProgram(tex_pipeline.shaderProgram)
                sg.drawSceneGraphNode(winNode, tex_pipeline, "transform")


                    
            
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    # freeing GPU memory
    sceneNode.clear()
    endNode.clear()
    winNode.clear()
    storeNode.clear()

    glfw.terminate()