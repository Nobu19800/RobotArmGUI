#!/usr/bin/env python
# -*- Python -*-
# -*- coding: utf-8 -*-

import datetime

import sys,os,platform
import subprocess
import rtctree.tree


try:
    tree = rtctree.tree.RTCTree("localhost")
    print tree
except:
    if os.name == 'posix':
        subprocess.Popen("rtm-naming".split(" "))
    elif os.name == 'nt':
        subprocess.Popen("cmd /c rtm-naming.bat")
    

