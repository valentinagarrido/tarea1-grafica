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
import grafica.performance_monitor as pm
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
from model import *

__author__ = "Daniel Calderon"
__license__ = "MIT"


t_total = 60
Z = 1
H = 2
T = 4
P = 0.5

# A class to store the application control
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
    # Agregamos dos nuevas teclas para interactuar
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

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Beauchefville", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)


    # Pipeline para dibujar shapes con texturas
    pipeline = es.SimpleTransformShaderProgram()
    tex_pipeline = es.SimpleTextureTransformShaderProgram()
    


    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)
    
    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory
    
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

    #zombieNode = sg.SceneGraphNode("zombie")
    #zombieNode.childs = [gpuZombie]

    zombiesNode = sg.SceneGraphNode("zombies")
    zombiesList = []
    
    human = bs.createTextureQuad(1, 1)
    gpuHuman = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuHuman)
    gpuHuman.fillBuffers(human.vertices, human.indices, GL_STATIC_DRAW)
    gpuHuman.texture = es.textureSimpleSetup(
        getAssetPath("boy.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    #humanNode = sg.SceneGraphNode("human")
    #humanNode.childs = [gpuHuman]

    humansNode = sg.SceneGraphNode("humans")
    humansList = []
    
    sickHuman = bs.createTextureQuad(1, 1)
    gpuSickHuman = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuSickHuman)
    gpuSickHuman.fillBuffers(sickHuman.vertices, sickHuman.indices, GL_STATIC_DRAW)
    gpuSickHuman.texture = es.textureSimpleSetup(
        getAssetPath("sickboy.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)

    sickHumansNode = sg.SceneGraphNode("sickHumans")

    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [fullBackgroundNode, hinataNode, zombiesNode, humansNode]

    player = Hinata(0.2, P)
    player.set_model(hinataNode)
    player.set_controller(controller)
    
    movingBackground = Background()
    movingBackground.set_model(fullBackgroundNode)

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
    
    store = bs.createTextureQuad(1, 1)
    gpuStore = es.GPUShape().initBuffers()
    tex_pipeline.setupVAO(gpuStore)
    gpuStore.fillBuffers(store.vertices, store.indices, GL_STATIC_DRAW)
    gpuStore.texture = es.textureSimpleSetup(
        getAssetPath("store.png"), GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_LINEAR)
    
    storeNode = sg.SceneGraphNode("store")
    storeNode.transform = tr.scale(0.3,0.75,1)
    storeNode.childs = [gpuStore]
    
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
        if (not controller.end) and (not controller.completed):
            movingBackground.update(delta)
        player.update(delta)
        
        if (t0%T < 0.002) and (not controller.end) and (not controller.completed):
            print(t0)
            for i in range(Z):
                zombieNode = sg.SceneGraphNode("zombie")
                zombieNode.childs = [gpuZombie]
                zombiesNode.childs += [zombieNode]
                z = Zombie(0.2)
                z.set_model(zombieNode)
                zombiesList += [z]
                print("new zombie")
            for i in range(H):
                humanNode = sg.SceneGraphNode("human")
                humanNode.childs = [gpuHuman]
                humansNode.childs += [humanNode]
                h = Human(0.2, P)
                h.set_model(humanNode)
                h.set_status()
                humansList += [h]
                print("new human")
            
                
        for z in zombiesList:
            z.update(delta)           
                
        for h in humansList:
            if h.status == "Dead":
                print("human turned to zombie")
                zombieNode = sg.SceneGraphNode("zombie")
                zombieNode.childs = [gpuZombie]
                zombiesNode.childs += [zombieNode]
                humansNode.childs.remove(h.model)
                h.set_model(zombieNode)
                humansList.remove(h)
                zombiesList += [h]
            h.update(delta)

                
        
        #sceneNode.childs += [zombiesNode, humansNode]
        player.collision(zombiesList + humansList)
        if player.status == "Dead":
            # Se dibuja el grafo de escena con texturas
            controller.end = True
        
        glUseProgram(tex_pipeline.shaderProgram)
            
        sg.drawSceneGraphNode(sceneNode, tex_pipeline, "transform")
        
        if controller.end:
            sg.drawSceneGraphNode(endNode, tex_pipeline, "transform")
        elif controller.completed:
            sg.drawSceneGraphNode(storeNode, tex_pipeline, "transform")
            player.collision([realStore])
            if player.status == "Won":
                sg.drawSceneGraphNode(winNode, tex_pipeline, "transform")


                    
            
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    # freeing GPU memory
    sceneNode.clear()
    endNode.clear()
    winNode.clear()
    storeNode.clear()

    glfw.terminate()