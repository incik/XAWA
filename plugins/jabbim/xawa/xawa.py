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
from pyxl.message import Message

'''
    Static class witch works as a proxy for calling XAWA plugin methods from JavaScript.
'''
class xawa(QtCore.QObject):
    def __init__(self,parent):
        QtCore.QObject.__init__(self,parent.window)
        self.setObjectName('XAWAPluginHandler')
        self.rodic = parent
    
    @QtCore.pyqtSlot()
    def init(self):
        '''
            Dummy method (so far) that's called to determine if the browser even supports XAWA callings
            (we need to fail init in case that someone opens application page in normal browser) 
        '''
        pass
    
    @QtCore.pyqtSlot(result=str)
    def getXawaVersion(self):
        '''
            Returns 
        '''
        return "0.1a"
    
    @QtCore.pyqtSlot(result=str)
    def getRecipient(self):
        '''
            Returns JID of recipient
        '''
        return self.rodic.recipient
    
    @QtCore.pyqtSlot(result=str)
    def getSender(self):
        '''
            Returns JID of sender
        '''
        return self.rodic.sender
        
    @QtCore.pyqtSlot(str)
    def sendMessage(self,message):
        '''
            Sending plain text messages
        '''
        self.rodic.sendMessage(unicode(message)) # message is 'QString', so we need to convert it into regular UNICODE string 

    @QtCore.pyqtSlot(result=str)
    def getData(self):
        '''
            Returns reviced data (JSON)
        '''
        return self.rodic.recivedData
    
    @QtCore.pyqtSlot()
    def markAsRead(self):
        '''
            Sets 
        '''
        self.rodic.isUnread = False
    
    @QtCore.pyqtSlot(result=bool)    
    def isUnread(self):
        '''
            Returns true/false if the message was already read
        '''
        return self.rodic.isUnread
    
    
        
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
            
            self.sender = 'xvaisa00@stud.fit.vutbr.cz'
            
            # registation of event handlers
            self.registerHandler('on_authd', self.on_authd)
            self.registerHandler('on_message', self.on_message, 10)
            
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
        '''
            Adding "Open XAWA Window" into contact's context menu
        '''
        jid = unicode(contact.jid)
        
        if self.main.client.hasFeature(jid,"http://xawa.vaisar.cz/protocol/xawa"):
            # wheee, someone is using our feature!
                
            self.action = menu.addAction(self.tr("Open XAWA window"))
            self.action.setData(QtCore.QVariant(jid))
            self.action.setObjectName("xawa_menu_button")
            
            # tohle je prasecina, ale zatim nevim, jak predat argument do slotu
            self.recipient = jid # now we know who we're going to communicate with, so we save this information

            # when the item is clicked, open xawa window
            QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.openWindow)
    
    def on_message(self,msg):
        '''
            Handling incomming message
        '''
        if (msg.body != None and msg.subject == 'xawa_data'):
            self.recivedData = unicode(msg.body)
            self.isUnread = True
        else:
            pass
    
    def openWindow(self):
        try:
            self.window.show()
        except Exception, ex:
            log.logerr(ex)
            
    def pushButtonClicked(self):
        self.loadApp()
        
    def loadApp(self):
        try:
            appUrl = 'file:///var/www/xawa/tstapp01.html'
            if appUrl != '':                
                self.window.ui.webView.load(QtCore.QUrl(appUrl))
            
        except Exception, ex:
            raise ex
    
    def initJavascript(self):
        try:
            self.window.ui.webView.page().mainFrame().addToJavaScriptWindowObject('xawa',xawa(self))
        except Exception,ex:
            raise ex
            
    def loadFinished(self):
        try:
            novyTitle = self.window.ui.webView.title()
            self.window.setWindowTitle(novyTitle)

        except Exception, ex:
            raise ex
        

            
    def sendMessage(self,message):
        '''
            sends plain text message to recipient with JID saved in self.recipient
        '''
        m = Message(self.recipient)
        m.setBody(message)
        m.setSubject(unicode('xawa_data'))
        m.setComposing("active")
        try:
            self.main.client.message.sendMessage(msg=m)
        except Exception, ex:
            raise ex
        
        
        return message
    