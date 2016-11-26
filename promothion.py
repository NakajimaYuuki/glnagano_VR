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
import vizhtml

viz.setMultiSample(4)
viz.fov(60)
#viz.MainView.collision( viz.ON )
viz.go()
#　viz.go(viz.FULLSCREEN)

tracker = vizcam.addWalkNavigate(moveScale=1.0)
tracker.setPosition([0,1.8,0])
viz.link(tracker,viz.MainView)
viz.mouse.setVisible(True)



#　設定ファイルは外出ししたい

# あたり判定をセット
manager = vizproximity.Manager()
manager.setDebug(viz.ON)

#Add main viewpoint as proximity target
target = vizproximity.Target(viz.MainView)
manager.addTarget(target)

lab = vizfx.addChild('resource/modern_lobby.osgb')
lab.enable(viz.LIGHTING) #　これをすると部屋が暗くなる(ライトが有効になる？)   

# マウスの設定
viz.mouse.setTrap(True)  #アプリ内でしか動けなくなる
viz.mouse.setCursor(True) # カーソルが見えるかどうか
viz.mouse.setOverride(viz.ON) 

# 鳩のロゴ
pigion_proj = vizfx.addProjector(texture=viz.addTexture('resource/pigion.jpg'), 
                                 pos=(-8, 3.5, 3.0), euler=(-90, 0, 0),blend=vizfx.BLEND_AVERAGE)

vizfx.getComposer().addEffect(pigion_proj.getEffect())

#　鳩のロゴと同じ場所にtexquad
pigion = viz.addTexQuad(size=4.5, pos= (-8, 3.5, 3.0), alpha=0)
# 鳩のロゴ用のセンサー
pigion_sensor = vizproximity.Sensor( vizproximity.CircleArea(4),source=pigion)
manager.addSensor(pigion_sensor)

# 鳩の説明
pigon_board = viz.addTexQuad(pos=[-8, 3.5, 3.0] )
pigon_texture = viz.addTexture('resource/pigon_descrption.JPG')
pigon_board.texture(pigon_texture)
pigon_board.billboard(viz.BILLBOARD_YAXIS)
pigon_board.visible(False)


# プロジェクターの表示
projector = viz.add('resource/Electronics_Overhead-Projector.osgb', pos=[0.7, 1.2, 5.4], euler=(180, 0, 0))
projector.collideBox()
projector_sound= projector.playsound('sound/brownie8.wav', viz.LOOP)
projector_sound.volume(0.2)
# プロジェクター用のセンサー
projector_sensor = vizproximity.Sensor( vizproximity.CircleArea(3),source=projector)
manager.addSensor(projector_sensor)
#　説明
proj_board = viz.addTexQuad(pos=(1.4, 2.4, 5.4) )
proj_texture = viz.addTexture('resource/projector.JPG')
proj_board.texture(proj_texture)
proj_board.billboard(viz.BILLBOARD_YAXIS)
proj_board.visible(False)

# ペッパー
peppar = viz.addChild('resource/Pepper.osgb', pos= (-9, .6, -4.7), euler=(-90, 0, 0))
peppar_sensor = vizproximity.Sensor( vizproximity.CircleArea(3),source=peppar)
manager.addSensor(peppar_sensor)

# ペッパーの紹介
peppr_obj = viz.add('box.wrl', pos=[-8.5, 2.8, -4.7], color=viz.WHITE)
pepper_video = viz.addVideo('resource/pepper.avi') 
peppr_obj.texture(pepper_video) 
pepper_video.setFrame(10) 
peppr_obj.alpha(0)

# wifi
wifi = viz.add('resource/wifi.osgb', pos=[-2, 2, 0])
wifi.addAction(vizact.spin(0, 1, 0, 10, viz.FOREVER))

#机とバリスタ
table = viz.addChild('resource/COWVRT3672+-+COALESSE-TBL,RECT,VENEER,36X72X28.osgb', pos=[-3, 0, 6])
barista = viz.add('resource/8000s.osgb', pos=[-3.5, 0.75, 5.8], euler=(90, 0, 0))
coffee =  viz.add('resource/Nescafe+simple.osgb', pos=[-3.0, 0.75, 5.6], euler=(0, 0, 0), scale=(4, 4, 4))
barista_sensor = vizproximity.Sensor( vizproximity.CircleArea(1.5),source=barista)
manager.addSensor(barista_sensor)

#　コーヒーカップ
cup = viz.add('resource/Mug.osgb', pos=[-3.3, 0.93, 5.72], alpha=(0))
coffee_sound = viz.addAudio('sound/kaffeemaschine.wav')
coffee_sound.volume(.1) 

#　テレビとファミコン
tv = viz.add('resource/TV+Stand.osgb', pos=[5.8, 0.7, 4.0], euler=(90, 0, 0))
famicon =  viz.add('resource/Famicom.osgb', pos=[6.05, 1.4, 3.65], euler=(-90, 0, 0))
famicon_sensor = vizproximity.Sensor( vizproximity.CircleArea(1.5),source=famicon)
manager.addSensor(famicon_sensor)
mario = viz.add('resource/NES+mario.osgb', pos=[5.9, 1.6, 3.9], scale=(0.007, 0.007, 0.007), euler=(-90,0,0), alpha=(0))
mario_bgm = famicon.playsound('sound/mario1.mid', viz.LOOP)
mario_bgm.volume(1)

# ギーラボの紹介プレゼン、画像の用意
movieImages = viz.cycle( [ viz.addTexture('resource/introduction/glnagano%d.jpeg' % i) for i in range(1, 39) ] )
screen = viz.addTexQuad()
screen.setPosition([0, 2.67, 6.33])
screen.setScale([0.789*3.01, 0.62*2.19, 1])

# ギークラボ長野へようこそ 
text3D = viz.addText3D('welcome to geeklab NAGANO', 
                       pos=[0,2.3,2],
                       align=viz.ALIGN_CENTER_BOTTOM,
                       color=viz.YELLOW,
                       scale=[0.1, 0.05, 0.1],
                       font='Comic Sans MS')

text3D.add(vizact.sequence(vizact.moveTo((0,2.0 ,2),speed=0.1),vizact.moveTo((0,2.3 ,2),speed=0.1),viz.FOREVER))


# 取得元のURL http://dova-s.jp/bgm/play3394.html
# sound = viz.addAudio('sound/基地出撃５分前.mp3', viz.LOOP, volume=0.1) 
# sound.volume(.1) 
# sound.play() 

# ギークラボ長野紹介プレゼン資料表示
def NextMovieFrame():
    screen.texture(movieImages.next())

vizact.ontimer(5.0/1, NextMovieFrame)

# センサーが検知した時
def enter_proximity(e):
	if e.sensor == projector_sensor:
		proj_board.visible(True)
	if e.sensor == pigion_sensor:
		pigon_board.visible(True)
	if e.sensor == peppar_sensor:
		peppr_obj.alpha(1)
		pepper_video.play() 
	if e.sensor == barista_sensor:
		coffee_sound.play()
		cup.alpha(1)
	if e.sensor == famicon_sensor:
		mario.alpha(1)
# センサーから出たとき
def exit_proximity(e):
	if e.sensor == projector_sensor:
		proj_board.visible(False)
	if e.sensor == pigion_sensor:
		pigon_board.visible(False)
	if e.sensor == peppar_sensor:
		peppr_obj.alpha(0)
		pepper_video.stop()
	if e.sensor == barista_sensor:
		cup.alpha(0)
	if e.sensor == famicon_sensor:
		mario.alpha(0)

manager.onEnter(None,enter_proximity) #センサーに入った時
manager.onExit(None,exit_proximity)   #センサーから出たとき

