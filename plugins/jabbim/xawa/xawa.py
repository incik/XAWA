'''
Created on 24.10.2010

@author: incik
'''

#import sys,os,time
#sys.path.append('.')
from include import plugins
from PyQt4 import QtCore #, QtGui
#from PyQt4.QtWebKit import QWebView
#from urllib import quote, unquote
from twisted.python import log
#from twisted.words.protocols.jabber.xmlstream import IQ
#from twisted.words.xish.domish import Element
from pyxl.message import Message
from core import PluginManager

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
            Returns current XAWA version
        '''
        return "0.2.1"
    
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
        
    @QtCore.pyqtSlot(str)
    def sendData(self,data):
        '''
            Sending plain text messages
        '''
        self.rodic.sendData(unicode(data)) # data is 'QString', so we need to convert it into regular UNICODE string

    @QtCore.pyqtSlot(result=str)
    def getMessage(self):
        '''
            Returns received message
        '''
        return self.rodic.receivedMessage

    @QtCore.pyqtSlot(result=str)
    def getData(self):
        '''
            Returns received data (JSON)
        '''
        return self.rodic.receivedData
    
    @QtCore.pyqtSlot()
    def markMessageAsRead(self):
        '''
            Sets received message as read
        '''
        self.rodic.isMessageUnread = False
        
    @QtCore.pyqtSlot()
    def markDataAsRead(self):
        '''
            Sets recieved data as read
        '''
        self.rodic.isDataUnread = False
    
    @QtCore.pyqtSlot(result=bool)    
    def isMessageUnread(self):
        '''
            Returns true/false if the recieved message was already read
        '''
        return self.rodic.isMessageUnread
    
    @QtCore.pyqtSlot(result=bool)    
    def isDataUnread(self):
        '''
            Returns true/false if the recieved data was already read
        '''
        return self.rodic.isDataUnread
    
    
        
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
            
            if (self.main.client != None):            
                senderjid = self.main.client.jid 
                self.sender = unicode(senderjid.user + '@' + senderjid.host)
                
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
        if (msg.body != None):
            if (msg.subject == 'xawa_data'):
                self.receivedData = unicode(msg.body)
                self.isDataUnread = True
            elif (msg.subject == 'xawa_message'):
                self.receivedMessage = unicode(msg.body)
                self.isMessageUnread = True
                
            return True
    
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
    
    def sendData(self,data):
        '''
            sends plain text data - it should be JSON string
        '''
        try:
            self.sendIt(data, 'xawa_data')
        except Exception, ex:
            raise ex
            
    def sendMessage(self,message):
        '''
            sends plain text message to recipient with JID saved in self.recipient
        '''
        try:
            self.sendIt(message, 'xawa_message')
        except Exception, ex:
            raise ex
    
    def sendIt(self,content,type):
        '''
            method for sending plain text through xmpp
        '''
        m = Message(self.recipient)
        m.setBody(content)
        m.setSubject(unicode(type))
        m.setComposing("active")
        try:
            self.main.client.message.sendMessage(msg=m)
        except Exception, ex:
            raise ex
    