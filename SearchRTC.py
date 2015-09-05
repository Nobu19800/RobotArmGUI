#!/usr/bin/env python
# -*- coding: cp932 -*-
# -*- Python -*-

"""
 @file SearchRTC.py
 @brief RTCの検索、データポート接続関連のクラス


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
# @brief ポートを接続する関数
# @param obj1 接続するデータポート
# @param obj2 接続するデータポート
# @param c_name コネクタ名
#

def ConnectCorbaPort(obj1, obj2, c_name):

    obj1.disconnect_all()
    
    obj2.disconnect_all()

    # connect ports
    conprof = RTC.ConnectorProfile(c_name, "", [obj1,obj2], [])
    

    ret = obj2.connect(conprof)

##
# @brief データポートを接続する関数
# @param obj1 接続するデータポート
# @param obj2 接続するデータポート
# @param c_name コネクタ名
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
# @brief namevalueリストから指定したキーの値を取得
# @param nvlist namevalueリスト
# @param name 名前
# @return 値
#
def nvlist_getValue(nvlist, name):
    
    for item in nvlist:
        if name == item.name:
            return item.value.value()
    
    return None

##
# @brief 各RTCのパスを取得する関数
# @param context ネーミングコンテキスト
# @param rtclist RTCのリスト
# @param name 現在のパス名
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
# @param naming ネーミングコンテキスト
# @param rtclist RTCのリスト
# @param name 現在のパス名
def rtc_get_rtclist(naming, rtclist, name):
    name_cxt = naming.getRootContext()
    ListRecursive(name_cxt,rtclist,name)
    
    return 0


##
# @class SearchRTC
# @brief RTCの検索、ポートの接続などを行うためのクラス
# 
# 
class SearchRTC:

	##
	# @brief コンストラクタ
	# @param manager Maneger Object
	# @param address IPアドレス
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
	# @brief RTCのアクティブ化
	# @param self
	# @param rtc RTC名
	def activeComponent(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			if rtc.get_owned_contexts()[0].get_component_state(rtc) == OpenRTM_aist.RTC.INACTIVE_STATE:
				rtc.get_owned_contexts()[0].activate_component(rtc)
				return True
		return False

	##
	# @brief RTCの非アクティブ化
	# @param self
	# @param rtc RTC名
	def deactiveComponent(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			if rtc.get_owned_contexts()[0].get_component_state(rtc) == OpenRTM_aist.RTC.ACTIVE_STATE:
				rtc.get_owned_contexts()[0].deactivate_component(rtc)
				return True
		return False

	##
	# @brief RTCのリセット
	# @param self
	# @param rtc RTC名
	def resetComponent(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			if rtc.get_owned_contexts()[0].get_component_state(rtc) == OpenRTM_aist.RTC.ERROR_STATE:
				rtc.get_owned_contexts()[0].reset_component(rtc)
				return True
		return False

	##
	# @brief RTCの状態取得
	# @param self
	# @param rtc RTC名
	def getComponentState(self, rtc_name):
		if rtc_name in self.c_list:
			rtc = self.c_list[rtc_name]["RTC"]
			return rtc.get_owned_contexts()[0].get_component_state(rtc)
			
		return -99

	##
	# @brief 名前からポートオブジェクト取得
	# @param self
	# @param rtc RTC名
	# @param name ポート名
	def getPort_Name(self, rtc_name, port_name):
		if rtc_name in self.c_list:
			if port_name in self.c_list[rtc_name]["ports"]:
				return self.c_list[rtc_name]["ports"][port_name]
		return None
		
	##
	# @brief ポート接続
	# @param self
	# @param dataPortObj データポートオブジェクト
	# @param RTC_Name 接続先のデータポートを有するRTC名
	# @param dataPortName 接続先のデータポート名
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