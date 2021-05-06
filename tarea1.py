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

Z = 1
T = 2

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.is_up_pressed = False
        self.is_down_pressed = False
        self.is_left_pressed = False
        self.is_right_pressed = False


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
    else:
        print('Unknown key')


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Textured Quad", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)


    # Pipeline para dibujar shapes con texturas
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

    zombiesNode = sg.SceneGraphNode("zombies")
    zombiesList = []

    sceneNode = sg.SceneGraphNode("world")
    sceneNode.childs = [fullBackgroundNode, hinataNode]

    player = Hinata(0.2)
    player.set_model(hinataNode)
    player.set_controller(controller)
    
    movingBackground = Background()
    movingBackground.set_model(fullBackgroundNode)


    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)    
    t0 = glfw.get_time()
    
    while not glfw.window_should_close(window):
        t1 = glfw.get_time()
        delta = t1 -t0
        t0 = t1
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        
        movingBackground.update(delta)
        player.update(delta)
        
        if t0%T < 0.05:
            counter = 0
            print(t0)
            for i in range(Z):
                zombieNode = sg.SceneGraphNode("zombie"+str(i))
                zombieNode.childs = [gpuZombie]
                zombiesNode.childs += [zombieNode]
                z = Zombie(0.2)
                z.set_model(zombieNode)
                zombiesList += [z]
                
        if zombiesList != []:
            for z in zombiesList:
                z.update(delta)
                

        sceneNode.childs += [zombiesNode]
        # Telling OpenGL to use our shader program
        glUseProgram(tex_pipeline.shaderProgram)
                
        # Se dibuja el grafo de escena con texturas
        glUseProgram(tex_pipeline.shaderProgram)
        
        sg.drawSceneGraphNode(sceneNode, tex_pipeline, "transform")
        
        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    # freeing GPU memory
    sceneNode.clear()

    glfw.terminate()