#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
import os
from __builtin__ import __import__
from GLog import elog, getDlog
from os.path import dirname

class pluginsManager(object):
    def __init__(self):
        self.pack = "plugins"
        self.path = dirname( dirname(__file__) )+os.path.sep +self.pack
        self.dlog = getDlog(__name__)
        
    
    def loadPlugins(self):
        plugins =  [file for file in os.listdir(self.path) if file.endswith(".py") and file != "__init__.py" and not file.startswith("_")]
        return plugins
    
    def run(self, dreq):
        plugins = [p.split(".")[0] for p in self.loadPlugins()]
        for plugin in plugins:
            try:
                cplugin = __import__(self.pack + "."+plugin, fromlist = [plugin, ])   
                vulc = cplugin.getPluginClass()
                self.dlog.debug("[Audit Plugin]Loading Plugin --> %s"%str(vulc))
                c = vulc(dreq)
                c.audit()
            except Exception,e:
                elog.exception(e)
 
pm = pluginsManager()