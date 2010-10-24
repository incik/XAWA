'''
Created on 24.10.2010

@author: incik
'''

import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView
from urllib import quote, unquote
from twisted.python import log

class config:
    def __init__(self,main):
        self.main = main
        self.config = {}

class Plugin(plugins.PluginBase):
    def __init__(self,main, homedir, plugindir):
        plugins.PluginBase.__init__(self, main, homedir, plugindir)
        self.fname = 'xawa'
        #self.installTranslator()
        self.description = self.tr('Lorem ipsum dolor')
        self.author = "Tomas 'Incik' Vaisar"
        self.name = self.tr('XAWA plugin')
        self.version = '0.01'
        self.category = ['misc']
        self.url = 'http://xawa.vaisar.cz'
        self.count = 0
        
        if main:
            self.loadConfig(homedir)
            self.loadConfig()
            self.window = self.loadWindow("%s/xawaWindow_ui.py" % self.pluginDir, self.main)
            self.window.setWindowIcon(self.main.windowIcon())
        else:
            self.loadConfig(homedir)
            
                        
    def buildMainWindowMenu(self):
        menu=self.mainWindowMenu()
        menu.addAction("Open XAWA Window", self.openWindow);
    
    def on_message(self,msg):
        pass
    
    def openWindow(self):
        try:
            self.window.show()
        except Exception, ex:
            log.logerr(ex)
        