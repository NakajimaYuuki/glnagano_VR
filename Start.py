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
import vizcam
import vizshape
import oculus
import vizconnect
import vizproximity
viz.go()
view = viz.MainView

KEYS = { 'forward'	: viz.KEY_UP
		,'back' 	: viz.KEY_DOWN
		,'left' 	: viz.KEY_LEFT
		,'right'	: viz.KEY_RIGHT
		,'reset'	: 'r'
		,'camera'	: 'c'
		,'help'		: ' '
}

# oculus の設定
hmd = oculus.Rift()
if hmd.getSensor():
	supportPositionTracking = hmd.getSensor().getSrcMask() & viz.LINK_POS
	if supportPositionTracking:
		# Add camera bounds model
		camera_bounds = hmd.addCameraBounds()
		camera_bounds.visible(False)

		# Change color of bounds to reflect whether position was tracked
		def CheckPositionTracked():
			if hmd.getSensor().getStatus() & oculus.STATUS_POSITION_TRACKED:
				camera_bounds.color(viz.GREEN)
			else:
				camera_bounds.color(viz.RED)
		vizact.onupdate(0, CheckPositionTracked)

	navigationNode = viz.addGroup()
	viewLink = viz.link(navigationNode, viz.MainView)
	viewLink.preMultLinkable(hmd.getSensor())

	# オキュラスの高さはみない	
	# profile = hmd.getProfile()
	# if profile:
	#     viewLink.setOffset([0,profile.eyeHeight,0])
	# else:
	#     viewLink.setOffset([0,1.8,0])
	viewLink.setOffset([0,1.8,0])

	#　角度の変更
	MOVE_SPEED = 2.0
	def UpdateView():
		yaw,pitch,roll = viewLink.getEuler()
		m = viz.Matrix.euler(yaw,0,0)
		dm = viz.getFrameElapsed() * MOVE_SPEED
		high = viz.getFrameElapsed() * MOVE_SPEED
		if viz.key.isDown(KEYS['forward']):
			m.preTrans([0,0,dm])
		if viz.key.isDown(KEYS['back']):
			m.preTrans([0,0,-dm])
		if viz.key.isDown(KEYS['left']):
			m.preTrans([-dm,0,0])
		if viz.key.isDown(KEYS['right']):
			m.preTrans([dm,0,0])

		navigationNode.setPosition(m.getPosition(), viz.REL_PARENT)
	vizact.ontimer(0,UpdateView)
else: # 繋がってないとき
	tracker = vizcam.addWalkNavigate(moveScale=2.0)
	tracker.setPosition([0,1.8,0])
	viz.link(tracker,viz.MainView)
	viz.mouse.setVisible(True)

# grid　表示
grid = vizshape.addGrid()
grid.color(viz.GREEN)
viz.clearcolor(viz.BLACK)

viz.mouse.setTrap(True)  #アプリ内でしか動けなくなる
viz.mouse.setVisible(False)
viz.mouse.setOverride(viz.ON) 

text3D = viz.addText3D(u'Press Enter Key', 
                       pos=[0,2.2,2],
                       align=viz.ALIGN_CENTER_BOTTOM,
                       color=viz.WHITE,
                       scale=[0.1, 0.05, 0.1],
                       font='Times New Roman')
text3D.setEncoding(viz.ENCODING_UTF8)
text3D.add(vizact.sequence(vizact.moveTo((0,2.1 ,2),speed=0.03),vizact.moveTo((0,2.2 ,2),speed=0.03),viz.FOREVER))
text3D.setThickness(0.001)

def myTask():
	sound = viz.addAudio('sound/samplerButton.wav') 
	sound.play() 
	
	fadeout = vizact.fadeTo(0,time=2)
	yield text3D.addAction(fadeout)
	yield text3D.disable(True)
	yield grid.addAction(fadeout)
	yield viztask.waitTime( 3 )
	# ここでGLNAGANOのロゴ表示
	import opning
	yield opning.Logo()
	yield viztask.waitTime( 10 )
	import promothion

	promothion
	

def mykeyboard(whichKey):

	if whichKey == viz.KEY_RETURN:
		text3D.endAction()
		viztask.schedule( myTask() )

viz.callback(viz.KEYDOWN_EVENT, mykeyboard)

