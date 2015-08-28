#!/bin/env python
# -*- coding: utf-8 -*-

##
#   @file OgreRTC.py
#   @brief Ogre3D、CEGUIをRTCで操作する関数群

import OpenRTM_aist
import RTC
import os.path
import sys
import imp
import time

sys.path += ['./']

import OgreRTS



EndFlag = True


    

##
# @brief マネージャを立ち上げる関数
def ManagerStart():
    OgreRTS.OgreObj = OgreObj
    OgreRTS.SimObj = SimulationObj
    
    
    
    OgreRTS.mgr = OpenRTM_aist.Manager.init(['test7.py'])
    
    OgreRTS.mgr.activateManager()
    OgreRTS.mgr.runManager(True)


##
# @brief RTCを立ち上げる関数
def RTCStart(fName): 
    
    OgreRTS.m_comp = RTCInit(fName)

    global EndFlag

    EndFlag = True

    OgreRTS.OgreObj.SetRTC()
    while(EndFlag):
        time.sleep(1)
    
    
    
    time.sleep(3)
    

##
# @brief RTCを停止する関数
def RTCStop():
    
    global EndFlag
    
    
    #OgreRTS.mgr.unregisterComponent(OgreRTS.m_comp)
    OgreRTS.m_comp.exit()
    OgreRTS.mgr.unloadAll()
    
    
    OgreRTS.m_comp = None
    EndFlag = False
    

    
    
    #time.sleep(3)


##
# @brief ファイルよりRTCを読み込む関数
# @param fName ファイルパス
def RTCInit(fName):
    
    dname = os.path.dirname(os.path.relpath(fName))
    sys.path.append(dname)
    
    root, ext = os.path.splitext(fName)

    pathName = os.path.dirname(fName)
    fileName = os.path.basename(root)

    print pathName, fileName

    (file, pathname, description) = imp.find_module(fileName,[pathName])
    print file, pathname, description
    MyCallBack = imp.load_module(fileName, file, pathname, description)
    

    if OgreRTS.mgr:
        return MyCallBack.MyModuleInit(OgreRTS.mgr)



##
# @brief キーを押したときに呼び出されるコールバック関数
# @param k キー
def keyPressed(k):
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.keyPressed(k)

##
# @brief キーを離したときに呼び出されるコールバック関数
# @param k キー
def keyReleased(k):
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.keyReleased(k)


##
# @brief マウスを動かしたときに呼び出されるコールバック関数
# @param mx X座標
# @param my Y座標
# @param mdx 移動量(X)
# @param mdy 移動量(Y)
def mouseMoved(mx, my, mdx, mdy):
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.mouseMoved(mx, my, mdx, mdy)



##
# @brief マウスのボタンを押したときに呼び出されるコールバック関数
# @param b ボタン
def mousePressed(b):
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.mousePressed(b)



##
# @brief マウスのボタンを離したときに呼び出されるコールバック関数
# @param b ボタン
def mouseReleased(b):
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.mouseReleased(b)



##
# @brief ファイル読み込み時に呼び出されるコールバック関数
def ogre_init():
    if OgreRTS.m_comp:
        OgreRTS.m_comp.ogre_init()
            

##
# @brief 描画更新時に呼び出されるコールバック関数
def ogre_loop():
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.ogre_loop()


##
#シミュレーション更新時に呼び出されるコールバック関数
##
def Simloop():
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.Simloop()



##
# @brief シミュレーションで接触が発生した時に呼び出されるコールバック関数
# @param b1 ボディ1
# @param b2 ボディ2
def Contacthandler(b1, b2):
    
    if OgreRTS.m_comp:
        OgreRTS.m_comp.Contacthandler(b1, b2)

##
# @brief GUIのアクションに対するコールバック
# @param fname コールバック名
def CEGUICallback(fname):
    if OgreRTS.m_comp:
        OgreRTS.m_comp.CEGUICallback(fname)
        try:
            method = getattr(OgreRTS.m_comp, fname)
        except AttributeError:
            return
        method()


    
