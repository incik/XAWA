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
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish.domish import Element

class LittleClass(QtCore.QObject):  
    def __init__(self,parent):
        QtCore.QObject.__init__(self,parent.window)
        self.setObjectName('ObjectAddedByPython')
        self.rodic = parent
        
    @QtCore.pyqtSlot(int, int, result=int)
    def scitej(self,a,b):
        return a+b
    
    @QtCore.pyqtSlot(result=str)
    def printInfo(self):
        return self.rodic.sendMessage('ahoj')
    
    @QtCore.pyqtSlot(result=str)
    def sendDummyMessage(self):
        #iq = IQ(self.parent().main.client.xmlstream, 'set')    
        return self.parent.sendMessage('ahoj')
    
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
            
            self.registerHandler('on_authd', self.on_authd)
            
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
            
    def on_authd(self):
        try:
            self.registerFeature("http://xawa.vaisar.cz/protocol/xawa")
        except Exception, ex:
            raise ex
            
                        
    def buildMainWindowMenu(self):
        menu=self.mainWindowMenu()
        menu.addAction("Open XAWA Window", self.openWindow);
    
    def buildContactMenu(self,menu,contact):
        jid = unicode(contact.jid)
        
        if self.main.client.hasFeature(jid,"http://xawa.vaisar.cz/protocol/xawa"):
            # wheee, nekdo pouziva nasi feature!
            
            self.action = menu.addAction(self.tr("Open XAWA window"))
            self.action.setData(QtCore.QVariant(jid))
            self.action.setObjectName("xawa_menu_button")

            QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.openWindow)
    
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
            self.window.ui.webView.page().mainFrame().addToJavaScriptWindowObject('PyLittleClass',LittleClass(self))
        except Exception,ex:
            raise ex
            
    def loadFinished(self):
        try:
            novyTitle = self.window.ui.webView.title()
            self.window.setWindowTitle(novyTitle)

        except Exception, ax:
            raise ax
        

            
    def sendMessage(self,message):
            
        #iq = IQ(self.parent().main.client.xmlstream, 'set')
        '''
        result = 'ok'
        try:
            message = Element((None,'message'))
            message['from'] = 'johntestovic@jabbim.cz/Jabbim'
            message['to'] = 'incik@jabbim.cz/Lenicka'
            body = message.addElement('body', None, 'Zdar!')
         
            self.main.client.xmlstream.send(message)
            result = 'jo'
        except Exception, ex:
            result = ex;
        '''
        
        return message
    