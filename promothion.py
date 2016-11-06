#!/usr/bin/env python
# -*- coding: utf-8 -*-

import viz
import vizact
import vizfx
import viztask 
import vizcam
import vizshape
import oculus
import vizconnect
import vizproximity

viz.setMultiSample(4)
viz.fov(60)
viz.go()
#　viz.go(viz.FULLSCREEN)


# Key commands
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
	# Check if HMD supports position tracking
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

	profile = hmd.getProfile()
	if profile:
		viewLink.setOffset([0,profile.eyeHeight,0])
	else:
		viewLink.setOffset([0,1.8,0])

	# Setup arrow key navigation
	MOVE_SPEED = 2.0
	def UpdateView():
		yaw,pitch,roll = viewLink.getEuler()
		m = viz.Matrix.euler(yaw,0,0)
		dm = viz.getFrameElapsed() * MOVE_SPEED
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

# あたり判定
#Create proximity manager
manager = vizproximity.Manager()
manager.setDebug(viz.ON)

#Add main viewpoint as proximity target
target = vizproximity.Target(viz.MainView)
manager.addTarget(target)


lab = vizfx.addChild('lab.osgb')
lab.enable(viz.LIGHTING) #　これをすると部屋が暗くなる(ライトが有効になる？)   

# マウスの設定
viz.mouse.setTrap(True)  #アプリ内でしか動けなくなる
viz.mouse.setCursor(True) # カーソルが見えるかどうか

# 鳩のロゴ
pigion_proj = vizfx.addProjector(texture=viz.addTexture('resource/pigion.jpg'), pos=(-3,4.0, 5.0), blend=vizfx.BLEND_AVERAGE)
vizfx.getComposer().addEffect(pigion_proj.getEffect())

#　鳩のロゴと同じ場所にtexquad
pigion = viz.addTexQuad(size=4.5)
pigion.setPosition([-3.5, 4, 6.9]) #　初期位置
pigion.alpha(0.0)
# 鳩のロゴ用のセンサー
pigion_sensor = vizproximity.Sensor( vizproximity.CircleArea(4),source=pigion)
manager.addSensor(pigion_sensor)


# プロジェクターの表示
projector = viz.add('box.wrl', pos=[2.2, 0.3, 6.5], scale=(.257*2, .221*2, .134*2), color=viz.WHITE)
projector.collideBox()
projector_sound= projector.playsound('sound/brownie8.wav', viz.LOOP)
projector_sound.volume(0.2)
projector_upper = viz.addChild('box.wrl', pos=[2.2, .52, 6.5], scale=(.257*2, 0.01, .134*2), color=viz.BLACK)
# プロジェクター用のセンサー
projector_sensor = vizproximity.Sensor( vizproximity.CircleArea(8),source=projector)
manager.addSensor(projector_sensor)


# ペッパー
peppar = viz.addTexQuad( )
peppar_texture = viz.addTexture('resource/pepper.jpg', pos= [2, 1, 6])
peppar.texture(peppar_texture)
peppar.billboard(viz.BILLBOARD_YAXIS)
peppar_sensor = vizproximity.Sensor( vizproximity.CircleArea(3),source=peppar)
manager.addSensor(peppar_sensor)

# ギーラボの紹介プレゼン、画像の用意
movieImages = viz.cycle( [ viz.addTexture('resource/introduction/glnagano%d.jpg' % i) for i in range(1,6) ] )
screen = viz.addTexQuad()
screen.setPosition([2, 4.7, 7.3])
screen.setScale([0.789*5, 0.62*5, 1])

# ギークラボ長野へようこそ 
text3D = viz.addText3D('welcome to geeklab NAGANO', 
                       pos=[0,2.3,2],
                       align=viz.ALIGN_CENTER_BOTTOM,
                       color=viz.YELLOW,
                       scale=[0.1, 0.05, 0.1],
                       font='Comic Sans MS')
text3D.addAction(vizact.moveTo([0,2.0 ,2],speed=0.1))
text3D.addAction(vizact.fadeTo(0,time=2))


#ギークラボ長野紹介プレゼン資料表示
def NextMovieFrame():
    screen.texture(movieImages.next())

vizact.ontimer(5.0/1, NextMovieFrame)



#説明画面の一覧
#　プロジェクター
proj_board = viz.addTexQuad(pos=[2.2, 2.6, 6.8] )
proj_texture = viz.addTexture('resource/projector.JPG')
proj_board.texture(proj_texture)
proj_board.billboard(viz.BILLBOARD_YAXIS)
proj_board.visible(False)

# 鳩の絵
pigon_board = viz.addTexQuad(pos=[-2.2, 2.3, 6.8] )
pigon_texture = viz.addTexture('resource/pigon_descrption.JPG')
pigon_board.texture(pigon_texture)
pigon_board.billboard(viz.BILLBOARD_YAXIS)
pigon_board.visible(False)

# ペッパーの紹介
pepper_sound = viz.addAudio('resource/welcome.mp3') 

# センサーが検知した時
def EnterProximity(e):
	if e.sensor == projector_sensor:
		proj_board.visible(True)
	if e.sensor == pigion_sensor:
		pigon_board.visible(True)
	if e.sensor == peppar_sensor:
		pepper_sound.loop(viz.ON) 
		pepper_sound.play()

		

# センサーから出たとき
def ExitProximity(e):
	if e.sensor == projector_sensor:
		proj_board.visible(False)
	if e.sensor == pigion_sensor:
		pigon_board.visible(False)
	if e.sensor == peppar_sensor:
		pepper_sound.stop() 
		

manager.onEnter(None,EnterProximity)
manager.onExit(None,ExitProximity)
