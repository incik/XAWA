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

class LittleClass(QtCore.QObject):  
    def __init__(self,parent):
        QtCore.QObject.__init__(self,parent)
        self.setObjectName('ObjectAddedByPython')
        
    @QtCore.pyqtSlot(int, int, result=int)
    def scitej(self,a,b):
        return a+b

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

            self.window.ui.pushButton.clicked.connect(self.pushButtonClicked)
            self.window.ui.webView.loadFinished.connect(self.loadFinished)
            
            try:
                self.window.ui.webView.page().mainFrame().javaScriptWindowObjectCleared.connect(self.initJavascript)
            except Exception, ex:
                raise ex
            
            self.window.ui.lineEdit.setReadOnly(True)
            self.window.ui.lineEdit.setText(QtCore.QString('tstapp1'))
           
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
            
    def pushButtonClicked(self):
        try:
            #novaUrl = 'http://eudora.incik.cz/xawa/tstapp01.html'
            novaUrl = 'file:///var/www/xawa/tstapp01.html'
            if novaUrl != '':                
                self.window.ui.webView.load(QtCore.QUrl(novaUrl))
            
        except Exception, ex:
            log.logerr(ex)
    
    def initJavascript(self):
        try:
            self.window.ui.webView.page().mainFrame().addToJavaScriptWindowObject('PyLittleClass',LittleClass(self.window))
        except Exception,ex:
            raise ex
            
    def loadFinished(self):
        try:
            novyTitle = self.window.ui.webView.title()
            self.window.setWindowTitle(novyTitle)

        except Exception, ax:
            raise ax
