#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
This script demonstrates how to use keyboard callbacks. 
When a key is pressed, its value will be printed out. 
Also the screen will toggle between black and white. 
""" 
import viz
import vizfx
import vizshape
import vizact
import viztask
import time
# viz.go()

# 文字の表示
text3D_G = viz.addText3D('G', pos=[-0.2, 1.76, 2],align=viz.ALIGN_CENTER_BOTTOM,color=viz.WHITE,scale=[0.8, 0.9, 1],font='Times New Roman')
text3D_L = viz.addText3D('L', pos=[0.24, 1.76, 2],align=viz.ALIGN_CENTER_BOTTOM,color=viz.WHITE,scale=[0.8, 0.9, 1],font='Times New Roman')
text3D_GL = viz.addText3D('GEEKLAB', pos=[0.0, 1.48, 2],align=viz.ALIGN_CENTER_BOTTOM,color=viz.WHITE,scale=[0.18, 0.2, 1],font='Times New Roman')
text3D_nagnao = viz.addText3D('NAGANO', pos=[0.00, 1.19, 2],align=viz.ALIGN_CENTER_BOTTOM,color=viz.WHITE, scale=[0.17, 0.2, 1],font='Times New Roman')


# 画像の表示
# Load texture 
pic = viz.addTexture('resource/logo.png') 
quad = viz.addTexQuad() 
quad.setSize([500*0.002, 688*0.002])
quad.setPosition([0, 1.8, 1.98]) #put quad in view 
quad.texture(pic)
quad.alpha(0)


def Logo():
	'''ロゴの表示'''	
	viztask.schedule(logo_start())
	
def logo_start():
	sound = viz.addAudio('sound/Omega-FlyHyperspace.wav') 
	sound.play() 
	
	fadeout = vizact.fadeTo(0,time=2)
	fadein = vizact.fadeTo(1,time=4)
	yield viztask.waitTime( 2 )
	text3D_G.addAction(fadeout)
	text3D_L.addAction(fadeout)
	text3D_GL.addAction(fadeout)
	text3D_nagnao.addAction(fadeout)
	
	quad.addAction(fadein)
	yield viztask.waitTime(0.1)
	yield quad.addAction(fadeout)

Logo()