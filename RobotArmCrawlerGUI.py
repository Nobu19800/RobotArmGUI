#!/usr/bin/env python
# -*- coding: cp932 -*-
# -*- Python -*-

"""
 @file RobotArmGUI.py
 @brief Robot Arm GUI
 @date $Date$


"""
import sys
import time
sys.path.append(".")




# Import RTM module
import RTC
import OpenRTM_aist

import ManipulatorCommonInterface_Common_idl
import ManipulatorCommonInterface_MiddleLevel_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import JARA_ARM, JARA_ARM__POA
import JARA_ARM, JARA_ARM__POA

import OgreRTS

import numpy
import math

# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
robotarmgui_spec = ["implementation_id", "RobotArmGUI", 
		 "type_name",         "RobotArmGUI", 
		 "description",       "Robot Arm GUI", 
		 "version",           "1.0.0", 
		 "vendor",            "Miyamoto Nobuhiko", 
		 "category",          "TES", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]

class CrawlerState:
        Forward = 0
        Back = 1
        Right = 2
        Left = 3
        Stop = 4
        Free = 5
        def __init__(self):
                pass

        
# </rtc-template>

##
# @class RobotArmGUI
# @brief Robot Arm GUI
# 
# 
class RobotArmGUI(OpenRTM_aist.DataFlowComponentBase):
	PointMode = 0
        JointMode = 1

        ButtonMode = 0
        SliderMode = 1
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		

		"""
		"""
		self._ManipulatorCommonInterface_CommonPort = OpenRTM_aist.CorbaPort("ManipulatorCommonInterface_Common")
		"""
		"""
		self._ManipulatorCommonInterface_MiddlePort = OpenRTM_aist.CorbaPort("ManipulatorCommonInterface_Middle")

		

		"""
		"""
		self._ManipulatorCommonInterface_Common = OpenRTM_aist.CorbaConsumer(interfaceType=JARA_ARM.ManipulatorCommonInterface_Common)
		"""
		"""
		self._ManipulatorCommonInterface_Middle = OpenRTM_aist.CorbaConsumer(interfaceType=JARA_ARM.ManipulatorCommonInterface_Middle)


                self._d_crawlerPos = RTC.TimedPose2D(RTC.Time(0,0),RTC.Pose2D(RTC.Point2D(0,0),0))
		"""
		"""
		self._crawlerPosIn = OpenRTM_aist.InPort("crawlerPos", self._d_crawlerPos)
		self._d_crawlerTargetPos = RTC.TimedPose2D(RTC.Time(0,0),RTC.Pose2D(RTC.Point2D(0,0),0))
		"""
		"""
		self._crawlerTargetPosOut = OpenRTM_aist.OutPort("crawlerTargetPos", self._d_crawlerTargetPos)


                self._d_crawlerTargetSpeed0 = RTC.TimedDouble(RTC.Time(0,0),0)
		"""
		"""
		self._crawlerTargetSpeed0Out = OpenRTM_aist.OutPort("crawlerTargetSpeed0", self._d_crawlerTargetSpeed0)

                self._d_crawlerTargetSpeed1 = RTC.TimedDouble(RTC.Time(0,0),0)
		"""
		"""
		self._crawlerTargetSpeed1Out = OpenRTM_aist.OutPort("crawlerTargetSpeed1", self._d_crawlerTargetSpeed1)


                self.link = [None, None, None, None]
                self.scale = 1000
                self.l = [0, 0, 0, 0]
                self.l[0] = 0.05*self.scale
                self.l[1] = 0.05*self.scale
                self.l[2] = 0.15*self.scale
                self.l[3] = 0.15*self.scale

                self.clawlerlx = 0.105*self.scale
                self.clawlerly = 0.171*self.scale
                self.clawlerlz = 0.065*self.scale
                

                self.armOffset = numpy.array([0, -0.04*self.scale, self.clawlerlz/2.])

                self.lv = [0, 0, 0, 0]
                self.lv[0] = numpy.array([0, 0, self.l[0]])
                self.lv[1] = numpy.array([0, 0, self.l[1]])
                self.lv[2] = numpy.array([0, self.l[2], 0])
                self.lv[3] = numpy.array([0, 0, -self.l[3]])

                self.link_s = None
                self.link_s2 = None
                self.ls = 0.05*self.scale
                self.lsv = numpy.array([0, 0, self.ls])

                self.lsv2 = self.lv[2]

                self.w = 0.01*self.scale

                self.hand = None
                self.finger = [None, None]

                self.lh = 0.01*self.scale
                self.wh = 0.02*self.scale

                self.lf = 0.02*self.scale
                self.wf = 0.003*self.scale

                self.targetSize = 0.01*self.scale
                self.targetLimit = (self.l[2]+self.l[3])
                self.limitZ = 0.02*self.scale
                
                self.targetPosition = [0, self.l[2], self.limitZ, 0]

                self.gripFlag = False
                self.flen = 0.01*self.scale

                
                self.mode = RobotArmGUI.PointMode

                self.softUpperLimit = [math.pi*90/180,math.pi*105/180,math.pi*90/180,math.pi/2]
                self.softLowerLimit = [-math.pi*90/180,0,0,-math.pi/2]

                
                self.theta = [-0.5, 0.5, 0.5, 0]
                self.hlength = 0.2

                #self.crawlerPos = numpy.array([self.scale*0.1, self.scale*0.1, 0.])
                #self.crawlerOri = [0., 0., math.pi/4]
                self.crawlerPos = numpy.array([0, 0, self.clawlerlz/2])
                self.crawlerOri = [0., 0., 0]

                self.cameraX_offset = 650
                self.cameraY_offset = 200
                self.cameraZ_offset = 550

                self.cameraX = 0
                self.cameraY = 0
                self.cameraZ = 0
                        

                self.crawlerState = CrawlerState.Stop

                self.moveMode = RobotArmGUI.ButtonMode
                

                
                
                
		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		self._ManipulatorCommonInterface_CommonPort.registerConsumer("ManipulatorCommonInterface_Common", "JARA_ARM::ManipulatorCommonInterface_Common", self._ManipulatorCommonInterface_Common)
		self._ManipulatorCommonInterface_MiddlePort.registerConsumer("ManipulatorCommonInterface_Middle", "JARA_ARM::ManipulatorCommonInterface_Middle", self._ManipulatorCommonInterface_Middle)
		
		# Set CORBA Service Ports
		self.addPort(self._ManipulatorCommonInterface_CommonPort)
		self.addPort(self._ManipulatorCommonInterface_MiddlePort)

		# Set InPort buffers
		self.addInPort("crawlerPos",self._crawlerPosIn)
		
		# Set OutPort buffers
		self.addOutPort("crawlerTargetPos",self._crawlerTargetPosOut)


                self.addOutPort("crawlerTargetSpeed0",self._crawlerTargetSpeed0Out)
                self.addOutPort("crawlerTargetSpeed1",self._crawlerTargetSpeed1Out)
		
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		self.RightSpeedSlider.SetSliderValue(0.5)
		self.LeftSpeedSlider.SetSliderValue(0.5)
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
                
                        
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK

	def keyPressed(self, k):
              pass
    
        def keyReleased(self, k):
              pass

        def mouseMoved(self, mx, my, mdx, mdy):
              print mx, my, mdx, mdy
      
      

        def mousePressed(self, b):
              pass

        def mouseReleased(self, b):
              pass

        def dotQuat(self, q1, q2):
                v1 = numpy.array([q1[1], q1[2], q1[3]])
                v2 = numpy.array([q2[1], q2[2], q2[3]])
                v = q1[0]*v2 + q2[0]*v1 + numpy.cross(v1, v2)
                ans = [q1[0]*q2[0] - numpy.dot(v1, v2), v[0], v[1], v[2]]
                return ans

        def ogre_init(self):
                self.CrawlerExist = True
                OgreRTS.OgreObj.SetCameraAutoMoveFlag(False)

                l = 0.3
                w = 0.025
                x = 0
                y = 0.97 - l

                tl_h = l/8

                self.moveModeButton = OgreRTS.OgreObj.CreateButton("moveModeButton")
                self.moveModeButton.SetText("ボタン入力で反映")
                self.moveModeButton.SetPosition(0, y-tl_h*2)
                self.moveModeButton.SetSize(w*12, tl_h)

                self.targetButton = OgreRTS.OgreObj.CreateButton("targetButton")
                self.targetButton.SetText("目標位置")
                self.targetButton.SetPosition(0, y-tl_h)
                self.targetButton.SetSize(w*6, tl_h)

                self.targetButton.SetFontSize(12)
                           
                self.slx = OgreRTS.OgreObj.CreateSlider("pxslider")
                self.sly = OgreRTS.OgreObj.CreateSlider("pyslider")
                self.slz = OgreRTS.OgreObj.CreateSlider("pzslider")
                self.st0 = OgreRTS.OgreObj.CreateSlider("pt0slider")
                self.slx.SetPosition(x+w/6., y)
                self.sly.SetPosition(x+w*3./2.+w/6., y)
                self.slz.SetPosition(x+w*6./2.+w/6., y)
                self.st0.SetPosition(x+w*9./2.+w/6., y)
                self.slx.SetSize(w, l)
                self.sly.SetSize(w, l)
                self.slz.SetSize(w, l)
                self.st0.SetSize(w, l)

                self.slx.SetSliderValue(0.5 + self.targetPosition[0]/self.targetLimit/2)
                self.sly.SetSliderValue(self.targetPosition[1]/self.targetLimit)
                self.slz.SetSliderValue((self.targetPosition[2]-self.limitZ)/(self.targetLimit-self.limitZ))
                self.st0.SetSliderValue(0.5);

                self.JointButton = OgreRTS.OgreObj.CreateButton("jointButton")
                self.JointButton.SetText("目標角度")
                self.JointButton.SetPosition(w*6, y-tl_h)
                self.JointButton.SetSize(w*6, tl_h)
                self.JointButton.SetAlpha(0.5)
                
                self.sj = [None, None, None, None]
                self.sj[0] = OgreRTS.OgreObj.CreateSlider("j0slider")
                self.sj[1] = OgreRTS.OgreObj.CreateSlider("j1slider")
                self.sj[2] = OgreRTS.OgreObj.CreateSlider("j2slider")
                self.sj[3] = OgreRTS.OgreObj.CreateSlider("j3slider")
                for i in range(0, 4):
                      
                      self.sj[i].SetPosition(x+w*3./2.*i+w*12./2.+w/6., y)
                      self.sj[i].SetSize(w, l)
                      if i == 2:
                              self.sj[2].SetSliderValue((self.theta[2]+self.theta[1]-self.softLowerLimit[2])/(self.softUpperLimit[2]-self.softLowerLimit[2]))
                      else:
                              self.sj[i].SetSliderValue((self.theta[i]-self.softLowerLimit[i])/(self.softUpperLimit[i]-self.softLowerLimit[i]))



                self.closeGripperButton = OgreRTS.OgreObj.CreateButton("closeGripperButton")
                self.closeGripperButton.SetText("ハンドを閉じる")
                self.closeGripperButton.SetPosition(w*12, y-tl_h)
                self.closeGripperButton.SetSize(w*6, tl_h)

                self.openGripperButton = OgreRTS.OgreObj.CreateButton("openGripperButton")
                self.openGripperButton.SetText("ハンドを開く")
                self.openGripperButton.SetPosition(w*12, y)
                self.openGripperButton.SetSize(w*6, tl_h)

                self.goHomeButton = OgreRTS.OgreObj.CreateButton("goHomeButton")
                self.goHomeButton.SetText("初期位置へ移動")
                self.goHomeButton.SetPosition(w*12, y+tl_h)
                self.goHomeButton.SetSize(w*6, tl_h)

                self.resumeButton = OgreRTS.OgreObj.CreateButton("resumeButton")
                self.resumeButton.SetText("再開")
                self.resumeButton.SetPosition(w*12, y+tl_h*2)
                self.resumeButton.SetSize(w*6, tl_h)

                self.pauseButton = OgreRTS.OgreObj.CreateButton("pauseButton")
                self.pauseButton.SetText("一時停止")
                self.pauseButton.SetPosition(w*12, y+tl_h*3)
                self.pauseButton.SetSize(w*6, tl_h)

                self.stopButton = OgreRTS.OgreObj.CreateButton("stopButton")
                self.stopButton.SetText("停止")
                self.stopButton.SetPosition(w*12, y+tl_h*4)
                self.stopButton.SetSize(w*6, tl_h)

                

                self.serboONButton = OgreRTS.OgreObj.CreateButton("serboONButton")
                self.serboONButton.SetText("サーボON")
                self.serboONButton.SetPosition(w*12, y+tl_h*5)
                self.serboONButton.SetSize(w*6, tl_h)

                self.serboOFFButton = OgreRTS.OgreObj.CreateButton("serboOFFButton")
                self.serboOFFButton.SetText("サーボOFF")
                self.serboOFFButton.SetPosition(w*12, y+tl_h*6)
                self.serboOFFButton.SetSize(w*6, tl_h)

                self.crawlerExistButton = OgreRTS.OgreObj.CreateButton("crawlerExistButton")
                self.crawlerExistButton.SetText("クローラー非表示")
                self.crawlerExistButton.SetPosition(w*12, y+tl_h*6)
                self.crawlerExistButton.SetSize(w*6, tl_h)

                self.forwordButton = OgreRTS.OgreObj.CreateButton("forwordButton")
                self.forwordButton.SetText("前進")
                self.forwordButton.SetPosition(w*18, y-tl_h)
                self.forwordButton.SetSize(w*6, tl_h)

                self.backButton = OgreRTS.OgreObj.CreateButton("backButton")
                self.backButton.SetText("後退")
                self.backButton.SetPosition(w*18, y)
                self.backButton.SetSize(w*6, tl_h)

                self.rightButton = OgreRTS.OgreObj.CreateButton("rightButton")
                self.rightButton.SetText("右旋回")
                self.rightButton.SetPosition(w*18, y+tl_h)
                self.rightButton.SetSize(w*6, tl_h)

                self.leftButton = OgreRTS.OgreObj.CreateButton("leftButton")
                self.leftButton.SetText("左旋回")
                self.leftButton.SetPosition(w*18, y+tl_h*2)
                self.leftButton.SetSize(w*6, tl_h)

                self.speed0Button = OgreRTS.OgreObj.CreateButton("speed0Button")
                self.speed0Button.SetText("速度0")
                self.speed0Button.SetPosition(w*18, y+tl_h*3)
                self.speed0Button.SetSize(w*6, tl_h)

                self.FreeButton = OgreRTS.OgreObj.CreateButton("FreeButton")
                self.FreeButton.SetText("スライダーでの操作")
                self.FreeButton.SetPosition(w*24, y-tl_h)
                self.FreeButton.SetSize(w*9, tl_h)


                self.speedText = OgreRTS.OgreObj.CreateStaticText("speedText")
                self.speedText.SetText("速度")
                self.speedText.SetPosition(w*24, y)
                self.speedText.SetSize(w*3, tl_h)



                self.speedSlider = OgreRTS.OgreObj.CreateSlider("speedSlider")
                
                self.speedSlider.SetPosition(w*25, y+tl_h)
                self.speedSlider.SetSize(w, l-tl_h)

                self.speedSlider.SetSliderValue(1.0)

                self.rightSpeedText = OgreRTS.OgreObj.CreateStaticText("rightSpeedText")
                self.rightSpeedText.SetText("右車輪")
                self.rightSpeedText.SetPosition(w*27, y)
                self.rightSpeedText.SetSize(w*3, tl_h)

                self.RightSpeedSlider = OgreRTS.OgreObj.CreateSlider("RightSpeedSlider")
                
                self.RightSpeedSlider.SetPosition(w*28, y+tl_h)
                self.RightSpeedSlider.SetSize(w, l-tl_h)

                self.RightSpeedSlider.SetSliderValue(0.5)

                self.LeftSpeedText = OgreRTS.OgreObj.CreateStaticText("LeftSpeedText")
                self.LeftSpeedText.SetText("左車輪")
                self.LeftSpeedText.SetPosition(w*30, y)
                self.LeftSpeedText.SetSize(w*3, tl_h)

                self.LeftSpeedSlider = OgreRTS.OgreObj.CreateSlider("LeftSpeedSlider")
                
                self.LeftSpeedSlider.SetPosition(w*31, y+tl_h)
                self.LeftSpeedSlider.SetSize(w, l-tl_h)

                self.LeftSpeedSlider.SetSliderValue(0.5)
                
                
                
                
                
                self.link[0] = OgreRTS.OgreObj.CreateBody("link0","Link0.mesh")
                self.link[0].SetScale(self.scale/10, self.scale/10, self.scale/10)
                self.link[1] = OgreRTS.OgreObj.CreateBody("link1","Link1.mesh")
                self.link[1].SetScale(self.scale/10, self.scale/10, self.scale/10)
                self.link[2] = OgreRTS.OgreObj.CreateBody("link2","Link2.mesh")
                self.link[2].SetScale(self.scale/10, self.scale/10, self.scale/10)
                self.link[3] = OgreRTS.OgreObj.CreateBody("link3","Link3.mesh")
                self.link[3].SetScale(self.scale/10, self.scale/10, self.scale/10)

                self.link_s = OgreRTS.OgreObj.CreateBody("link_s","Links1.mesh")
                self.link_s.SetScale(self.scale/10, self.scale/10, self.scale/10)

                self.link_s2 = OgreRTS.OgreObj.CreateBody("link_s2","Links2.mesh")
                self.link_s2.SetScale(self.scale/10, self.scale/10, self.scale/10)

                self.hand = OgreRTS.OgreObj.CreateBody("hand","Linkh.mesh")
                self.hand.SetScale(self.scale/10, self.scale/10, self.scale/10)

                self.crawler = OgreRTS.OgreObj.CreateBody("crawler","clawler.mesh")
                self.crawler.SetScale(self.scale/10, self.scale/10, self.scale/10)
                #self.crawler.SetScale(self.clawlerlx, self.clawlerly, self.clawlerlz)

                #self.finger[0] = OgreRTS.OgreObj.CreateBody("finger1","ODEBox.mesh")
                #self.finger[0].SetScale(self.wf, self.wf, self.lf)

                #self.finger[1] = OgreRTS.OgreObj.CreateBody("finger2","ODEBox.mesh")
                #self.finger[1].SetScale(self.wf, self.wf, self.lf)

                OgreRTS.OgreObj.SetFloor("ground", "groundh", "Examples/GrassFloor", 5000, 2)                
                OgreRTS.OgreObj.SetSkyBox("Examples/TrippySkyBox", 10000)
                OgreRTS.OgreObj.SetCameraPosition(self.cameraX+self.cameraX_offset, self.cameraY+self.cameraY_offset, self.cameraZ+self.cameraZ_offset)
                OgreRTS.OgreObj.SetCameraRotation(90, 45, 0)
                OgreRTS.OgreObj.SetLightPosition(0, 0, 3000)

                
                self.targetPoint = OgreRTS.OgreObj.CreateBody("targetPoint","ODEBox.mesh")
                self.targetPoint.SetScale(self.targetSize, self.targetSize, self.targetSize)
                self.targetPoint.SetPosition(self.targetPosition[0],self.targetPosition[1],self.targetPosition[2])
                
                self.updateTargetPosition()

                OgreRTS.OgreObj.setEColor(self.targetPoint, 1, 0, 0, 1)

                
                self.setPosition(self.theta, 0.2)

        


                

        def getCrawlerQuat(self):
                qx = [math.cos(self.crawlerOri[0]/2.), math.sin(self.crawlerOri[0]/2.), 0, 0]
                qy = [math.cos(self.crawlerOri[1]/2.), 0, math.sin(self.crawlerOri[1]/2.), 0]
                qz = [math.cos(self.crawlerOri[2]/2.), 0, 0, math.sin(self.crawlerOri[2]/2.)]
                qxy = self.dotQuat(qy, qx)
                qxyz = self.dotQuat(qz, qxy)

                return qxyz

        def getCrawlerRot(self):
                Ex = numpy.identity(3)

                Sx = math.sin(self.crawlerOri[0])
                Cx = math.cos(self.crawlerOri[0])
                Sy = math.sin(self.crawlerOri[1])
                Cy = math.cos(self.crawlerOri[1])
                Sz = math.sin(self.crawlerOri[2])
                Cz = math.cos(self.crawlerOri[2])
                
                Ex[0][0] = 1
                Ex[0][1] = 0
                Ex[0][2] = 0
                Ex[1][0] = 0
                Ex[1][1] = Cx
                Ex[1][2] = -Sx
                Ex[2][0] = 0
                Ex[2][1] = Sx
                Ex[2][2] = Cx
                
                Ey = numpy.identity(3)

                Ey[0][0] = Cy
                Ey[0][1] = 0
                Ey[0][2] = Sy
                Ey[1][0] = 0
                Ey[1][1] = 1
                Ey[1][2] = 0
                Ey[2][0] = -Sy
                Ey[2][1] = 0
                Ey[2][2] = Cy
                
                Ez = numpy.identity(3)

                Ez[0][0] = Cz
                Ez[0][1] = -Sz
                Ez[0][2] = 0
                Ez[1][0] = Sz
                Ez[1][1] = Cz
                Ez[1][2] = 0
                Ez[2][0] = 0
                Ez[2][1] = 0
                Ez[2][2] = 1

                Rxy = numpy.dot(Ey, Ex)
                Rxyz = numpy.dot(Ez, Rxy)

                return Rxyz

        def setPosition(self, theta, hlength):
                self.theta = theta
                self.hlength = hlength

                self.moveRobot()

        def setCrawlerPos(self, pos, ori):
                self.crawlerPos = pos
                self.crawlerOri = ori

                

                self.moveRobot()
                self.updateTargetPosition()

                

        
              
        def moveRobot(self):
                
                Ecl = self.getCrawlerRot()
                
                E = [0, 0, 0]
                S1 = math.sin(self.theta[0])
                C1 = math.cos(self.theta[0])
                S2 = math.sin(self.theta[1])
                C2 = math.cos(self.theta[1])
                S3 = math.sin(self.theta[2])
                C3 = math.cos(self.theta[2])



                E[0] = numpy.identity(3)
                E[0][0][0] = C1
                E[0][0][1] = -S1
                E[0][0][2] = 0
                E[0][1][0] = S1
                E[0][1][1] = C1
                E[0][1][2] = 0
                E[0][2][0] = 0
                E[0][2][1] = 0
                E[0][2][2] = 1



                E[1] = numpy.identity(3)
                E[1][0][0] = 1
                E[1][0][1] = 0
                E[1][0][2] = 0
                E[1][1][0] = 0
                E[1][1][1] = C2
                E[1][1][2] = -S2
                E[1][2][0] = 0
                E[1][2][1] = S2
                E[1][2][2] = C2



                E[2] = numpy.identity(3)
                E[2][0][0] = 1
                E[2][0][1] = 0
                E[2][0][2] = 0
                E[2][1][0] = 0
                E[2][1][1] = C3
                E[2][1][2] = -S3
                E[2][2][0] = 0
                E[2][2][1] = S3
                E[2][2][2] = C3

                R = [0, 0, 0]
                R[0] = numpy.dot(Ecl, E[0])
                R[1] = numpy.dot(R[0], E[1])
                R[2] = numpy.dot(R[1],E[2])

                

                po = self.crawlerPos + numpy.dot(Ecl, self.armOffset)


                pt = [0, 0, 0, 0]

                pt[0] = numpy.dot(Ecl, self.lv[0]) + po
                pt[1] = pt[0] + numpy.dot(R[0],self.lv[1])
                pt[2] = pt[1] + numpy.dot(R[1],self.lv[2])
                pt[3] = pt[2] + numpy.dot(R[2],self.lv[3])

                pv = [0, 0, 0, 0]
                pv[0] = (po + pt[0])/2.
                pv[1] = (pt[1] + pt[0])/2.
                pv[2] = (pt[2] + pt[1])/2.
                pv[3] = (pt[3] + pt[2])/2.

                theta_s = self.theta[2] + self.theta[1]


                Es = numpy.identity(3)
                Ss = math.sin(theta_s)
                Cs = math.cos(theta_s)
                Es[0][0] = 1
                Es[0][1] = 0
                Es[0][2] = 0
                Es[1][0] = 0
                Es[1][1] = Cs
                Es[1][2] = -Ss
                Es[2][0] = 0
                Es[2][1] = Ss
                Es[2][2] = Cs

                Rs = numpy.dot(R[0], Es)
                pst = pt[1] + numpy.dot(Rs,self.lsv)

                Rs2 = R[1]
                pst2 = pst + numpy.dot(Rs2,self.lsv2)

                psv = (pt[1] + pst)/2.
                psv2 = (pst + pst2)/2.

                
                self.crawler.SetPosition(self.crawlerPos[0],self.crawlerPos[1],self.crawlerPos[2])
                

                for i in range(0, 4):
                        self.link[i].SetPosition(pv[i][0], pv[i][1], pv[i][2])

                self.link_s.SetPosition(psv[0], psv[1], psv[2])
                self.link_s2.SetPosition(psv2[0], psv2[1], psv2[2])

                self.hand.SetPosition(pt[3][0], pt[3][1], pt[3][2]-self.lh)
                #self.finger[0].SetPosition(pt[3][0]+self.wf/2.+self.hlength/2., pt[3][1], pt[3][2]-self.lh-self.lf)
                #self.finger[1].SetPosition(pt[3][0]-self.wf/2.-self.hlength/2., pt[3][1], pt[3][2]-self.lh-self.lf)

                
                qoff = [math.cos(math.pi/4), math.sin(math.pi/4), 0, 0]
                qcraw = self.getCrawlerQuat()

                

                q1 = [math.cos(self.theta[0]/2), 0, 0, math.sin(self.theta[0]/2)]
                q2 = [math.cos(self.theta[1]/2), math.sin(self.theta[1]/2), 0, 0]
                q3 = [math.cos(self.theta[2]/2), math.sin(self.theta[2]/2), 0, 0]
                qs = [math.cos(theta_s/2), math.sin(theta_s/2), 0, 0]
                qco = self.dotQuat(qcraw, qoff)
                qcoffset = [math.cos(math.pi/4), 0, math.sin(math.pi/4), 0]
                qcori = self.dotQuat(qco, qcoffset)
                self.crawler.SetQuaternion(qcori[0],qcori[1],qcori[2],qcori[3])
                self.link[0].SetQuaternion(qco[0],qco[1],qco[2],qco[3])
                qoc = self.dotQuat(qcraw, q1)
                qc1 = self.dotQuat(qoc, qoff)
                self.link[1].SetQuaternion(qc1[0],qc1[1],qc1[2],qc1[3])
                q12 = self.dotQuat(qoc, q2)
                qo2 = self.dotQuat(q12, qoff)
                self.link[2].SetQuaternion(qo2[0],qo2[1],qo2[2],qo2[3])
                q13 = self.dotQuat(q12, q3)
                qo3 = self.dotQuat(q13, qoff)
                self.link[3].SetQuaternion(qo3[0],qo3[1],qo3[2],qo3[3])
                q1s = self.dotQuat(qoc, qs)
                qos = self.dotQuat(q1s, qoff)
                self.link_s.SetQuaternion(qos[0],qos[1],qos[2],qos[3])
                self.link_s2.SetQuaternion(qo2[0],qo2[1],qo2[2],qo2[3])

                #qh = [math.cos(self.theta[3]/2), 0, 0, math.sin(self.theta[3]/2)]
                #q1h = self.dotQuat(q1, qh)
                
                self.hand.SetQuaternion(qc1[0],qc1[1],qc1[2],qc1[3])

                #self.finger[0].SetQuaternion(q1h[0],q1h[1],q1h[2],q1h[3])

                #self.finger[1].SetQuaternion(q1h[0],q1h[1],q1h[2],q1h[3])
                
                """for i in range(0, 4):
                        self.link[i].SetQuaternion(1,0,0,0)
                self.link_s.SetQuaternion(1,0,0,0)
                self.link_s2.SetQuaternion(1,0,0,0)

                self.link[1].Roll(self.theta[0]*180/math.pi)

                self.link[2].Roll(self.theta[0]*180/math.pi)
                self.link[2].Pitch(self.theta[1]*180/math.pi)

                self.link[3].Roll(self.theta[0]*180/math.pi)
                self.link[3].Pitch(self.theta[1]*180/math.pi+self.theta[2]*180/math.pi)

                self.link_s.Roll(self.theta[0]*180/math.pi)
                self.link_s.Pitch(self.theta_s*180/math.pi)

                self.link_s2.Roll(self.theta[0]*180/math.pi)
                self.link_s2.Pitch(self.theta[1]*180/math.pi)"""

                

        def ogre_loop(self):
                r = 0.1
                self.cameraX = (1-r)*self.cameraX + r*self.crawlerPos[0]
                self.cameraY = (1-r)*self.cameraY + r*self.crawlerPos[1]
                self.cameraZ = (1-r)*self.cameraZ + r*self.crawlerPos[2]
                OgreRTS.OgreObj.SetCameraPosition(self.cameraX+self.cameraX_offset, self.cameraY+self.cameraY_offset, self.cameraZ+self.cameraZ_offset)
                
                #if self.crawlerState == CrawlerState.Forward:
                #        self.crawlerPos[1] += 0.01*self.scale
                #elif self.crawlerState == CrawlerState.Back:
                #        self.crawlerPos[1] -= 0.01*self.scale
                #self.setCrawlerPos(self.crawlerPos, self.crawlerOri)
                
                if self._crawlerPosIn.isNew():
                        data = self._crawlerPosIn.read()
                        
                        
                        
                        self.setCrawlerPos(numpy.array([data.data.position.x*self.scale, data.data.position.y*self.scale, self.clawlerlz/2.]),[0,0,data.data.heading])
                        
                if self.mode == RobotArmGUI.PointMode:
                        try:
                                jp = self._ManipulatorCommonInterface_Common._ptr().getFeedbackPosJoint()
                                for i in range(0,4):
                                        self.theta[i] = jp[1][i]
                                lf = self.flen
                                if self.gripFlag:
                                        lf = 0
                                self.setPosition(self.theta, lf)
                        except:
                                pass
                #theta = [0.5, 0.5, 0]
                #self.setPosition(theta, 0.2)
                

        def Simloop(self):
              pass

        def Contacthandler(self, b1, b2):
              pass

        def testClicked(self):
              print 334

        def inputTargetJointAngle(self):
                try:
                        self._ManipulatorCommonInterface_Middle._ptr().movePTPJointAbs(self.theta)
                except:
                        pass
                

        def updateSliderJointAngle(self):
                if self.mode == RobotArmGUI.JointMode:
                        for i in range(0, 4):
                                self.theta[i] = self.sj[i].GetSliderValue()*(self.softUpperLimit[i] - self.softLowerLimit[i]) + self.softLowerLimit[i]
                        lf = self.flen
                        if self.gripFlag:
                                lf = 0
                        self.theta[2] = self.theta[2] - self.theta[1]
                        self.setPosition(self.theta, lf)

                        if self.moveMode == RobotArmGUI.SliderMode:
                                self.inputTargetJointAngle()
                                

        def updateTargetRot(self):
                qcraw = self.getCrawlerQuat()
                qt = [math.cos(self.targetPosition[3]/2), 0, 0, math.sin(self.targetPosition[3]/2)]
                q = self.dotQuat(qcraw, qt)
                self.targetPoint.SetQuaternion(q[0], q[1], q[2], q[3])

        def writeClawlerSpeedData(self):
                self._d_crawlerTargetSpeed0.data = 2*(self.RightSpeedSlider.GetSliderValue() - 0.5)
                self._crawlerTargetSpeed0Out.write()

                self._d_crawlerTargetSpeed1.data = 2*(self.LeftSpeedSlider.GetSliderValue() - 0.5)
                self._crawlerTargetSpeed1Out.write()
        def writeClawlerSpeedDataSelf(self, v0, v1):
                self._d_crawlerTargetSpeed1.data = v1
                self._crawlerTargetSpeed1Out.write()
                
                self._d_crawlerTargetSpeed0.data = v0
                self._crawlerTargetSpeed0Out.write()

                
                
        def updateClawlerSpeed(self):
                speed = self.speedSlider.GetSliderValue()
                if self.crawlerState == CrawlerState.Forward:
                        #self.writeClawlerSpeedDataSelf(speed,speed)
                        self.RightSpeedSlider.SetSliderValue(speed*0.5+0.5)
                        self.LeftSpeedSlider.SetSliderValue(speed*0.5+0.5)
                        
                        
                        
                        
                elif self.crawlerState == CrawlerState.Back:
                        #self.writeClawlerSpeedDataSelf(-speed,-speed)
                        self.RightSpeedSlider.SetSliderValue(-speed*0.5+0.5)
                        self.LeftSpeedSlider.SetSliderValue(-speed*0.5+0.5)

                        
                elif self.crawlerState == CrawlerState.Right:
                        #self.writeClawlerSpeedDataSelf(speed,-speed)
                        self.RightSpeedSlider.SetSliderValue(speed*0.5+0.5)
                        self.LeftSpeedSlider.SetSliderValue(-speed*0.5+0.5)
                elif self.crawlerState == CrawlerState.Left:
                        #self.writeClawlerSpeedDataSelf(-speed,speed)
                        self.RightSpeedSlider.SetSliderValue(-speed*0.5+0.5)
                        self.LeftSpeedSlider.SetSliderValue(speed*0.5+0.5)
                elif self.crawlerState == CrawlerState.Stop:
                        #self.writeClawlerSpeedDataSelf(0,0)
                        self.RightSpeedSlider.SetSliderValue(0.5)
                        self.LeftSpeedSlider.SetSliderValue(0.5)

                self.writeClawlerSpeedData()

        def updateTargetPosition(self):
                E = self.getCrawlerRot()
                #Einv = numpy.linalg.inv(E)
                tp = numpy.array([self.targetPosition[0]+self.armOffset[0], self.targetPosition[1]+self.armOffset[1], self.targetPosition[2]+self.armOffset[2]])
                P = numpy.dot(E, tp)
                self.targetPoint.SetPosition(P[0]+self.crawlerPos[0],P[1]+self.crawlerPos[1],P[2]+self.crawlerPos[2])
                self.updateTargetRot()
                if self.moveMode == RobotArmGUI.SliderMode and self.mode == RobotArmGUI.PointMode:
                        self.inputTargetPosition()
                        
        def inputTargetPosition(self):
                try:
                        
                        
                        
                        px = self.targetPosition[0]/self.scale
                        py = self.targetPosition[1]/self.scale
                        pz = self.targetPosition[2]/self.scale
                        the = self.targetPosition[3]
                                
                        
                        cp = JARA_ARM.CarPosWithElbow([[math.cos(the),-math.sin(the),0,px],[math.sin(the),math.cos(the),0,py],[0,0,1,pz]], 0, 0)
                        
                        self._ManipulatorCommonInterface_Middle._ptr().moveLinearCartesianAbs(cp)
                        
                        self.mode = RobotArmGUI.PointMode
                except:
                        pass

        
                
                
                
        def setClawlerExist(self, e):
                self.CrawlerExist = e
                if e:
                        self.setCrawlerPos(numpy.array([0, 0, self.clawlerlz/2]),[0,0,0])
                else:
                        self.setCrawlerPos(numpy.array([0, 0, -self.clawlerlz/2]),[0,0,0])
                self.crawler.SetVisible(e)
                self.forwordButton.SetVisible(e)
                self.backButton.SetVisible(e)
                self.rightButton.SetVisible(e)
                self.leftButton.SetVisible(e)
                self.speed0Button.SetVisible(e)
                self.FreeButton.SetVisible(e)
                self.speedText.SetVisible(e)
                self.speedSlider.SetVisible(e)
                self.rightSpeedText.SetVisible(e)
                self.RightSpeedSlider.SetVisible(e)
                self.LeftSpeedText.SetVisible(e)
                self.LeftSpeedSlider.SetVisible(e)

        def CEGUICallback(self, fname):
                print fname
                if fname == "targetButtonClicked":
                        self.inputTargetPosition()

                elif fname == "closeGripperButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Middle._ptr().closeGripper()
                        except:
                                pass
                elif fname == "openGripperButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Middle._ptr().openGripper()
                        except:
                                pass
                elif fname == "goHomeButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Middle._ptr().goHome()
                        except:
                                pass
                elif fname == "resumeButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Middle._ptr().resume()
                        except:
                                pass
                elif fname == "pauseButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Middle._ptr().pause()
                        except:
                                pass
                elif fname == "stopButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Middle._ptr().stop()
                        except:
                                pass
                elif fname == "serboONButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Common._ptr().servoON()
                        except:
                                pass
                elif fname == "serboOFFButtonClicked":
                        try:
                                self._ManipulatorCommonInterface_Common._ptr().servoOFF()
                        except:
                                pass
                

                elif fname == "pxsliderSliderChanged":
                        self.targetPosition[0] = (-0.5 + self.slx.GetSliderValue()) * self.targetLimit*2
                        self.updateTargetPosition()
                        
                elif fname == "pysliderSliderChanged":
                        self.targetPosition[1] = (self.sly.GetSliderValue()) * self.targetLimit
                        self.updateTargetPosition()
                elif fname == "pzsliderSliderChanged":
                        self.targetPosition[2] = self.slz.GetSliderValue() * self.targetLimit + self.limitZ
                        self.updateTargetPosition()

                elif fname == "pt0sliderSliderChanged":
                        self.targetPosition[3] = (-0.5 + self.st0.GetSliderValue())*math.pi
                        self.updateTargetPosition()

                        

                elif fname == "j0sliderSliderChanged":
                        self.updateSliderJointAngle()
                elif fname == "j1sliderSliderChanged":
                        self.updateSliderJointAngle()
                elif fname == "j2sliderSliderChanged":
                        self.updateSliderJointAngle()
                elif fname == "j3sliderSliderChanged":
                        self.updateSliderJointAngle()

                elif fname == "jointButtonClicked":
                        if self.mode == RobotArmGUI.JointMode:
                                self.inputTargetJointAngle()
                                self.mode = RobotArmGUI.PointMode
                                self.JointButton.SetAlpha(0.5)
                                
                        else:
                                for i in range(0, 4):
                                      if i == 2:
                                              self.sj[2].SetSliderValue((self.theta[2]+self.theta[1]-self.softLowerLimit[2])/(self.softUpperLimit[2]-self.softLowerLimit[2]))
                                      else:
                                              self.sj[i].SetSliderValue((self.theta[i]-self.softLowerLimit[i])/(self.softUpperLimit[i]-self.softLowerLimit[i]))
                                self.mode = RobotArmGUI.JointMode
                                self.JointButton.SetAlpha(1.0)


                elif fname == "forwordButtonClicked":
                        self.crawlerState = CrawlerState.Forward
                        self.updateClawlerSpeed()
                elif fname == "backButtonClicked":
                        self.crawlerState = CrawlerState.Back
                        self.updateClawlerSpeed()
                elif fname == "rightButtonClicked":
                        self.crawlerState = CrawlerState.Right
                        self.updateClawlerSpeed()
                elif fname == "leftButtonClicked":
                        self.crawlerState = CrawlerState.Left
                        self.updateClawlerSpeed()
                elif fname == "speed0ButtonClicked":
                        self.crawlerState = CrawlerState.Stop
                        self.updateClawlerSpeed()
                elif fname == "FreeButtonClicked":
                        self.crawlerState = CrawlerState.Free
                        self.updateClawlerSpeed()
                elif fname == "speedSliderSliderChanged":
                        self.updateClawlerSpeed()
                elif fname == "LeftSpeedSliderSliderChanged":
                        self.writeClawlerSpeedData()
                elif fname == "RightSpeedSliderSliderChanged":
                        self.writeClawlerSpeedData()

                elif fname == "moveModeButtonClicked":
                        if self.moveMode == RobotArmGUI.ButtonMode:
                                self.moveMode = RobotArmGUI.SliderMode
                                self.moveModeButton.SetText("スライダー入力で反映")
                        else:
                                self.moveMode = RobotArmGUI.ButtonMode
                                self.moveModeButton.SetText("ボタン入力で反映")
                        
                        
                elif fname == "crawlerExistButtonClicked":
                        if self.CrawlerExist:
                                self.crawlerExistButton.SetText("クローラー表示")
                                self.setClawlerExist(False)
                        else:
                                self.crawlerExistButton.SetText("クローラー非表示")
                                self.setClawlerExist(True)
                        

                

def RobotArmGUIInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=robotarmgui_spec)
    manager.registerFactory(profile,
                            RobotArmGUI,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    manager._factory.unregisterObject("RobotArmGUI")
    RobotArmGUIInit(manager)

    # Create a component
    return manager.createComponent("RobotArmGUI")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
        main()
	
        
        #f = JARA_ARM.CarPosWithElbow([[1,0,0,10],[0,1,0,10],[0,0,1,10]], 0, 0)
        #print f
        
        

