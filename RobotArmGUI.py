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
# </rtc-template>

##
# @class RobotArmGUI
# @brief Robot Arm GUI
# 
# 
class RobotArmGUI(OpenRTM_aist.DataFlowComponentBase):
	
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

                self.link = [None, None, None, None]
                self.scale = 1000
                self.l = [0, 0, 0, 0]
                self.l[0] = 0.05*self.scale
                self.l[1] = 0.05*self.scale
                self.l[2] = 0.15*self.scale
                self.l[3] = 0.15*self.scale

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
                self.limitZ = 0.03*self.scale
                
                self.targetPosition = [0, self.l[2], self.limitZ]

                self.gripFlag = False
                self.flen = 0.01*self.scale

                
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
                OgreRTS.OgreObj.SetCameraAutoMoveFlag(True)

                l = 0.3
                w = 0.03
                x = 0
                y = 0.97 - l

                tl_h = l/6

                self.targetButton = OgreRTS.OgreObj.CreateButton("targetButton")
                self.targetButton.SetText("目標位置")
                self.targetButton.SetPosition(0, y-tl_h)
                self.targetButton.SetSize(w*6, tl_h)

                self.targetButton.SetFontSize(15)
                           
                self.slx = OgreRTS.OgreObj.CreateSlider("pxslider")
                self.sly = OgreRTS.OgreObj.CreateSlider("pyslider")
                self.slz = OgreRTS.OgreObj.CreateSlider("pzslider")
                self.slx.SetPosition(x+w/2., y)
                self.sly.SetPosition(x+w*2+w/2., y)
                self.slz.SetPosition(x+w*4+w/2., y)
                self.slx.SetSize(w, l)
                self.sly.SetSize(w, l)
                self.slz.SetSize(w, l)

                self.slx.SetSliderValue(0.5 + self.targetPosition[0]/self.targetLimit/2)
                self.sly.SetSliderValue(0.5 + self.targetPosition[1]/self.targetLimit/2)
                self.slz.SetSliderValue((self.targetPosition[2]-self.limitZ)/(self.targetLimit-self.limitZ))


                self.JointButton = OgreRTS.OgreObj.CreateButton("jointButton")
                self.JointButton.SetText("目標角度")
                self.JointButton.SetPosition(w*6, y-tl_h)
                self.JointButton.SetSize(w*6, tl_h)
                

                self.sj0 = OgreRTS.OgreObj.CreateSlider("jxslider")
                self.sj1 = OgreRTS.OgreObj.CreateSlider("jyslider")
                self.sj2 = OgreRTS.OgreObj.CreateSlider("jzslider")
                self.sj0.SetPosition(x+w*6+w/2., y)
                self.sj1.SetPosition(x+w*8+w/2., y)
                self.sj2.SetPosition(x+w*10+w/2., y)
                self.sj0.SetSize(w, l)
                self.sj1.SetSize(w, l)
                self.sj2.SetSize(w, l)


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
                self.serboONButton.SetPosition(w*18, y-tl_h)
                self.serboONButton.SetSize(w*6, tl_h)

                self.serboOFFButton = OgreRTS.OgreObj.CreateButton("serboOFFButton")
                self.serboOFFButton.SetText("サーボOFF")
                self.serboOFFButton.SetPosition(w*18, y)
                self.serboOFFButton.SetSize(w*6, tl_h)
                
                
                
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

                self.finger[0] = OgreRTS.OgreObj.CreateBody("finger1","ODEBox.mesh")
                self.finger[0].SetScale(self.wf, self.wf, self.lf)

                self.finger[1] = OgreRTS.OgreObj.CreateBody("finger2","ODEBox.mesh")
                self.finger[1].SetScale(self.wf, self.wf, self.lf)

                OgreRTS.OgreObj.SetFloor("ground", "groundh", "Examples/GrassFloor", 5000, 2)                
                OgreRTS.OgreObj.SetSkyBox("Examples/TrippySkyBox", 10000)
                OgreRTS.OgreObj.SetCameraPosition(550, 0, 550)
                OgreRTS.OgreObj.SetCameraRotation(90, 45, 0)

                
                self.targetPoint = OgreRTS.OgreObj.CreateBody("targetPoint","ODESphere.mesh")
                self.targetPoint.SetScale(self.targetSize, self.targetSize, self.targetSize)
                self.targetPoint.SetPosition(self.targetPosition[0],self.targetPosition[1],self.targetPosition[2])
                OgreRTS.OgreObj.setEColor(self.targetPoint, 1, 0, 0, 1)

                self.theta = [-0.5, 0.5, 0.5, 0]
                self.moveRobot(self.theta, 0.2)
      
        def moveRobot(self, theta, hlength):
                E = [0, 0, 0]
                S1 = math.sin(theta[0])
                C1 = math.cos(theta[0])
                S2 = math.sin(theta[1])
                C2 = math.cos(theta[1])
                S3 = math.sin(theta[2])
                C3 = math.cos(theta[2])



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
                R[0] = E[0]
                R[1] = numpy.dot(E[0], E[1])
                R[2] = numpy.dot(R[1],E[2])


                pt = [0, 0, 0, 0]

                pt[0] = self.lv[0]
                pt[1] = pt[0] + numpy.dot(R[0],self.lv[1])
                pt[2] = pt[1] + numpy.dot(R[1],self.lv[2])
                pt[3] = pt[2] + numpy.dot(R[2],self.lv[3])

                pv = [0, 0, 0, 0]
                pv[0] = pt[0]/2.
                pv[1] = (pt[1] + pt[0])/2.
                pv[2] = (pt[2] + pt[1])/2.
                pv[3] = (pt[3] + pt[2])/2.

                theta_s = theta[2] + theta[1]


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

                for i in range(0, 4):
                        self.link[i].SetPosition(pv[i][0], pv[i][1], pv[i][2])

                self.link_s.SetPosition(psv[0], psv[1], psv[2])
                self.link_s2.SetPosition(psv2[0], psv2[1], psv2[2])

                self.hand.SetPosition(pt[3][0], pt[3][1], pt[3][2]-self.lh)
                self.finger[0].SetPosition(pt[3][0]+self.wf/2.+hlength/2., pt[3][1], pt[3][2]-self.lh-self.lf)
                self.finger[1].SetPosition(pt[3][0]-self.wf/2.-hlength/2., pt[3][1], pt[3][2]-self.lh-self.lf)

                qoff = [math.cos(math.pi/4), math.sin(math.pi/4), 0, 0]

                q1 = [math.cos(theta[0]/2), 0, 0, math.sin(theta[0]/2)]
                q2 = [math.cos(theta[1]/2), math.sin(theta[1]/2), 0, 0]
                q3 = [math.cos(theta[2]/2), math.sin(theta[2]/2), 0, 0]
                qs = [math.cos(theta_s/2), math.sin(theta_s/2), 0, 0]
                self.link[0].SetQuaternion(qoff[0],qoff[1],qoff[2],qoff[3])
                qo1 = self.dotQuat(q1, qoff)
                self.link[1].SetQuaternion(qo1[0],qo1[1],qo1[2],qo1[3])
                q12 = self.dotQuat(q1, q2)
                qo2 = self.dotQuat(q12, qoff)
                self.link[2].SetQuaternion(qo2[0],qo2[1],qo2[2],qo2[3])
                q13 = self.dotQuat(q12, q3)
                qo3 = self.dotQuat(q13, qoff)
                self.link[3].SetQuaternion(qo3[0],qo3[1],qo3[2],qo3[3])
                q1s = self.dotQuat(q1, qs)
                qos = self.dotQuat(q1s, qoff)
                self.link_s.SetQuaternion(qos[0],qos[1],qos[2],qos[3])
                self.link_s2.SetQuaternion(qo2[0],qo2[1],qo2[2],qo2[3])

                qh = [math.cos(theta[3]/2), 0, 0, math.sin(theta[3]/2)]
                q1h = self.dotQuat(q1, qh)
                qoh = self.dotQuat(q1h, qoff)
                self.hand.SetQuaternion(qoh[0],qoh[1],qoh[2],qoh[3])

                self.finger[0].SetQuaternion(q1h[0],q1h[1],q1h[2],q1h[3])

                self.finger[1].SetQuaternion(q1h[0],q1h[1],q1h[2],q1h[3])
                
                """for i in range(0, 4):
                        self.link[i].SetQuaternion(1,0,0,0)
                self.link_s.SetQuaternion(1,0,0,0)
                self.link_s2.SetQuaternion(1,0,0,0)

                self.link[1].Roll(theta[0]*180/math.pi)

                self.link[2].Roll(theta[0]*180/math.pi)
                self.link[2].Pitch(theta[1]*180/math.pi)

                self.link[3].Roll(theta[0]*180/math.pi)
                self.link[3].Pitch(theta[1]*180/math.pi+theta[2]*180/math.pi)

                self.link_s.Roll(theta[0]*180/math.pi)
                self.link_s.Pitch(theta_s*180/math.pi)

                self.link_s2.Roll(theta[0]*180/math.pi)
                self.link_s2.Pitch(theta[1]*180/math.pi)"""

                

        def ogre_loop(self):
                try:
                        
                        jp = self._ManipulatorCommonInterface_Common._ptr().getFeedbackPosJoint()
                        for i in range(0,4):
                                self.theta[i] = jp[1][i]
                        lf = self.flen
                        if self.gripFlag:
                                lf = 0
                        self.moveRobot(self.theta, lf)
                except:
                        pass
                #theta = [0.5, 0.5, 0]
                #self.moveRobot(theta, 0.2)
                

        def Simloop(self):
              pass

        def Contacthandler(self, b1, b2):
              pass

        def testClicked(self):
              print 334

        def CEGUICallback(self, fname):
                print fname
                if fname == "targetButtonClicked":
                        
                        try:
                                px = self.targetPosition[0]/self.scale
                                py = self.targetPosition[1]/self.scale
                                pz = self.targetPosition[2]/self.scale + self.limitZ/self.scale
                                
                                cp = JARA_ARM.CarPosWithElbow([[1,0,0,px],[0,1,0,py],[0,0,1,pz]], 0, 0)
                                self._ManipulatorCommonInterface_Middle._ptr().moveLinearCartesianAbs(cp)
                                
                        except:
                                pass

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
                        self.targetPoint.SetPosition(self.targetPosition[0],self.targetPosition[1],self.targetPosition[2])
                        
                elif fname == "pysliderSliderChanged":
                        self.targetPosition[1] = (-0.5 + self.sly.GetSliderValue()) * self.targetLimit*2
                        self.targetPoint.SetPosition(self.targetPosition[0],self.targetPosition[1],self.targetPosition[2])
                elif fname == "pzsliderSliderChanged":
                        self.targetPosition[2] = self.slz.GetSliderValue() * self.targetLimit + self.limitZ
                        self.targetPoint.SetPosition(self.targetPosition[0],self.targetPosition[1],self.targetPosition[2])



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
        
        

