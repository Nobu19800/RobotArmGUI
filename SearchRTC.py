#!/usr/bin/env python
# -*- coding: cp932 -*-
# -*- Python -*-

"""
 @file SearchRTC.py
 @brief RTC�̌����A�f�[�^�|�[�g�ڑ��֘A�̃N���X


"""
import sys
import time
sys.path.append(".")




import RTC
import OpenRTM_aist
from OpenRTM_aist import CorbaNaming
from OpenRTM_aist import RTObject
from OpenRTM_aist import CorbaConsumer
from omniORB import CORBA
import CosNaming




##
# @brief �|�[�g��ڑ�����֐�
# @param obj1 �ڑ�����f�[�^�|�[�g
# @param obj2 �ڑ�����f�[�^�|�[�g
# @param c_name �R�l�N�^��
#

def ConnectCorbaPort(obj1, obj2, c_name):

    obj1.disconnect_all()
    
    obj2.disconnect_all()

    # connect ports
    conprof = RTC.ConnectorProfile(c_name, "", [obj1,obj2], [])
    

    ret = obj2.connect(conprof)

##
# @brief �f�[�^�|�[�g��ڑ�����֐�
# @param obj1 �ڑ�����f�[�^�|�[�g
# @param obj2 �ڑ�����f�[�^�|�[�g
# @param c_name �R�l�N�^��
#

def ConnectDataPort(obj1, obj2, c_name):

    subs_type = "Flush"

    obj1.disconnect_all()
    
    obj2.disconnect_all()

    # connect ports
    conprof = RTC.ConnectorProfile(c_name, "", [obj1,obj2], [])
    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                    OpenRTM_aist.NVUtil.newNV("dataport.interface_type",
                                                         "corba_cdr"))

    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                    OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type",
                                                         "push"))

    OpenRTM_aist.CORBA_SeqUtil.push_back(conprof.properties,
                                    OpenRTM_aist.NVUtil.newNV("dataport.subscription_type",
                                                         subs_type))

    ret = obj2.connect(conprof)

##
# @brief namevalue���X�g����w�肵���L�[�̒l���擾
# @param nvlist namevalue���X�g
# @param name ���O
# @return �l
#
def nvlist_getValue(nvlist, name):
    
    for item in nvlist:
        if name == item.name:
            return item.value.value()
    
    return None

##
# @brief �eRTC�̃p�X���擾����֐�
# @param context �l�[�~���O�R���e�L�X�g
# @param rtclist RTC�̃��X�g
# @param name ���݂̃p�X��
#
def ListRecursive(context, rtclist, name):
   m_blLength = 100
   bl = context.list(m_blLength)
   cont = True
   while cont:
      for i in bl[0]:
         if i.binding_type == CosNaming.ncontext:
            next_context = context.resolve(i.binding_name)
            name_buff = name[:]
            name.append(i.binding_name[0].id)
            ListRecursive(next_context,rtclist,name)
            name = name_buff
         elif i.binding_type == CosNaming.nobject:
             if len(rtclist) > m_blLength:
                  break
             if i.binding_name[0].kind == 'rtc':
                  name_buff = name[:]
                  name_buff.append(i.binding_name[0].id)
                  tkm = OpenRTM_aist.CorbaConsumer()
                  tkm.setObject(context.resolve(i.binding_name))
                  inobj = tkm.getObject()._narrow(RTC.RTObject)
                  rtcname = i.binding_name[0].id+"."+i.binding_name[0].kind
                  rtclist[rtcname] = {"RTC":inobj,"ports":{}}
                  try:
                       pin = inobj.get_ports()
                       for p in pin:
                            
                            
                            profile = p.get_port_profile()
                            #props = nvlist_to_dict(profile.properties)
                            tp_n = profile.name.split('.')[1]
                            
                            
                            rtclist[rtcname]["ports"][tp_n] = {"port":p,"type":nvlist_getValue(profile.properties, "port.port_type")}
                            
                            
                  except:
                        pass
                  
                  
      if CORBA.is_nil(bl[1]):
           cont = False
      else:
           bl = i.next_n(m_blLength)

##
# @brief
# @param naming �l�[�~���O�R���e�L�X�g
# @param rtclist RTC�̃��X�g
# @param name ���݂̃p�X��
def rtc_get_rtclist(naming, rtclist, name):
    name_cxt = naming.getRootContext()
    ListRecursive(name_cxt,rtclist,name)
    
    return 0


##
# @class SearchRTC
# @brief RTC�̌����A�|�[�g�̐ڑ��Ȃǂ��s�����߂̃N���X
# 
# 
class SearchRTC:

	##
	# @brief �R���X�g���N�^
	# @param manager Maneger Object
	# @param address IP�A�h���X
	# 
	def __init__(self, manager, address):
		self.c_list = {}
		self.result = True
		orb = manager._orb
		self.result = True
		try:
			namingserver = CorbaNaming(orb, address)
		except:
			self.result = False
			return
		if namingserver:
			_path = ['/', address]
			
			rtc_get_rtclist(namingserver,self.c_list,_path)

	

	##
	# @brief RTC�̃A�N�e�B�u��
	# @param self
	# @param rtc RTC��
	def activeComponent(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			if rtc.get_owned_contexts()[0].get_component_state(rtc) == OpenRTM_aist.RTC.INACTIVE_STATE:
				rtc.get_owned_contexts()[0].activate_component(rtc)
				return True
		return False

	##
	# @brief RTC�̔�A�N�e�B�u��
	# @param self
	# @param rtc RTC��
	def deactiveComponent(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			if rtc.get_owned_contexts()[0].get_component_state(rtc) == OpenRTM_aist.RTC.ACTIVE_STATE:
				rtc.get_owned_contexts()[0].deactivate_component(rtc)
				return True
		return False

	##
	# @brief RTC�̃��Z�b�g
	# @param self
	# @param rtc RTC��
	def resetComponent(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			if rtc.get_owned_contexts()[0].get_component_state(rtc) == OpenRTM_aist.RTC.ERROR_STATE:
				rtc.get_owned_contexts()[0].reset_component(rtc)
				return True
		return False

	##
	# @brief RTC�̏�Ԏ擾
	# @param self
	# @param rtc RTC��
	def getComponentState(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			return rtc.get_owned_contexts()[0].get_component_state(rtc)
			
		return -99

	##
	# @brief ���O����|�[�g�I�u�W�F�N�g�擾
	# @param self
	# @param rtc RTC��
	# @param name �|�[�g��
	def getPort_Name(self, rtc_name, port_name):
		if rtc_name in self.c_list:
			if port_name in self.c_list[rtc_name]["ports"]:
				return self.c_list[rtc_name]["ports"][port_name]
		return None
		
	##
	# @brief �|�[�g�ڑ�
	# @param self
	# @param dataPortObj �f�[�^�|�[�g�I�u�W�F�N�g
	# @param RTC_Name �ڑ���̃f�[�^�|�[�g��L����RTC��
	# @param dataPortName �ڑ���̃f�[�^�|�[�g��
	def connectPort(self, dataPortObj, RTC_Name, dataPortName):
		p = self.getPort_Name(RTC_Name,dataPortName)
		if p == None:
			return False
		
		if p["type"] == "CorbaPort":
			ConnectCorbaPort(dataPortObj, p["port"], dataPortName)
		else:
			ConnectDataPort(dataPortObj, p["port"], dataPortName)
		
		return True

def main():
        mgr = OpenRTM_aist.Manager.init(sys.argv)
        mgr.activateManager()
        mgr.runManager(True)

        s = SearchRTC(mgr,"localhost")
        p = s.getPort_Name("MySecondComponent0.rtc","in")
        s.connectPort(p["port"],"MySecondComponent0.rtc","out")
        

if __name__ == "__main__":
    main()