'''
Created on 24.10.2010

@author: incik
'''

import json
from include import plugins
from PyQt4 import QtCore, QtGui
#from PyQt4.QtWebKit import QWebView
from twisted.python import log
from twisted.words.protocols.jabber.xmlstream import IQ
from pyxl.message import Message
from core import PluginManager
import time
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
        return "1.0.0"
    
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
      
    @QtCore.pyqtSlot(str,str,result=bool)
    def sendInvite(self, jid, appInfoJSON):
        '''
            Sends invitation message to user with given JID
        '''
        appInfo = json.loads(unicode(appInfoJSON))
        self.rodic.sendInvite(unicode(jid), appInfo)
        
    
    @QtCore.pyqtSlot(str)
    def sendMessage(self,message):
        '''
            Sends text message in XAWA format
        '''
        self.rodic.sendXawaMessage(unicode(message))
    
    @QtCore.pyqtSlot(str)
    def sendClassicMessage(self,message):
        '''
            Sends classic plain text messages
        '''
        self.rodic.sendMessage(unicode(message)) # message is 'QString', so we need to convert it into regular UNICODE string 
        
    @QtCore.pyqtSlot(str)
    def sendDataInLegacyMode(self,data):
        '''
            Sends plain text messages
        '''
        self.rodic.sendDataInLecagyMode(unicode(data)) # data is 'QString', so we need to convert it into regular UNICODE string

    @QtCore.pyqtSlot(str)
    def sendData(self,data):
        '''
            Sends plain text messages
        '''
        self.rodic.sendXawaData(unicode(data)) # data is 'QString', so we need to convert it into regular UNICODE string


    @QtCore.pyqtSlot()
    def leave(self):
        '''
            Leaves current session
        '''
        self.rodic.leaveSession()

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
        self.description = self.tr('Plugin that implements XAWA API - viz http://xawa.vaisar.cz/docs/xawa.pdf')
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
            self.registerHandler('on_message', self.on_message, priority = 4)
            
            self.window = self.loadWindow("%s/xawaWindow_ui.py" % self.pluginDir, self.main)
            self.window.setWindowIcon(self.main.windowIcon())

            self.window.ui.pushButton.clicked.connect(self.pushButtonClicked)
            self.window.ui.webView.loadFinished.connect(self.loadFinished)
            
            self.windowOpened = False
            
            self.mainFrame = self.window.ui.webView.page().mainFrame() #shortcut
            
            try:
                self.mainFrame.javaScriptWindowObjectCleared.connect(self.initJavascript)
            except Exception, ex:
                raise ex
            
            self.window.ui.lineEdit.setReadOnly(True)
            self.window.ui.lineEdit.setText(QtCore.QString('xawa testing applications'))
           
        else:
            self.loadConfig(homedir)
           
    def on_authd(self):
        '''
            Stuff done when logging in
        '''
        try:
           
            # add observer for custom iq messages
            self.main.client.xmlstream.addObserver("/iq[@type='set']/query[@xmlns='http://xawa.vaisar.cz']/session/invite", self.onInvite, priority = 1)
            self.main.client.xmlstream.addObserver("/iq[@type='set']/query[@xmlns='http://xawa.vaisar.cz']/session", self.onSession, priority = 1)
            self.main.client.xmlstream.addObserver("/iq[@type='set']/query[@xmlns='http://xawa.vaisar.cz']", self.onXawaMessage, priority = 4)
             
            # register our features in client capabilities
            self.registerFeature("http://xawa.vaisar.cz")
            
            if (self.main.client != None):            
                senderjid = self.main.client.jid 
                self.sender = unicode(senderjid.user + '@' + senderjid.host)
                
        except Exception, ex:
            raise ex
            
    '''
    def buildMainWindowMenu(self): 
        menu=self.mainWindowMenu()
        menu.addAction("Open XAWA Window", self.openWindow);
    '''
    
    def buildContactMenu(self,menu,contact):
        '''
            Adding "Open XAWA Window" into contact's context menu
        '''
        jid = unicode(contact.jid)
        
        if self.main.client.hasFeature(jid,"http://xawa.vaisar.cz"):
            # wheee, someone is using our feature!
                
            self.action = menu.addAction(self.tr("Open XAWA window"))
            self.action.setData(QtCore.QVariant(jid))
            self.action.setObjectName("xawa_menu_button")
            
            self.recipient = jid # now we know who we're going to communicate with, so we save this information

            # when the item is clicked, open xawa window
            QtCore.QObject.connect(self.action,QtCore.SIGNAL("triggered ( bool )"),self.openWindow)
    
    def openWindow(self):
        '''
            Opens XAWA window
        '''
        try:
            self.windowOpened = True
            self.window.show()
        except Exception, ex:
            log.logerr(ex)
            
    def pushButtonClicked(self):
        '''
            Handles 
        '''
        self.loadApp()
        
    def loadApp(self,appUrl='http://xawa.vaisar.cz/apps/tstapps.html'):
        '''
            Loads given page in the browser
            @param appUrl: URL of wanted app
        '''    
        self.window.ui.webView.load(QtCore.QUrl(appUrl))
    
    def initJavascript(self):
        '''
            Magic! Let's extend JavaScript with our functionality!
        '''
        try:
            self.mainFrame.addToJavaScriptWindowObject('xawa',xawa(self))
        except Exception,ex:
            raise ex
            
    def loadFinished(self):
        '''
            When pages is loaded ...
        '''
        try:
            novyTitle = self.window.ui.webView.title()
            self.window.setWindowTitle(novyTitle)
            # if onApplicationReady is not implemented, die silently
            self.mainFrame.evaluateJavaScript("try { onApplicationReady(); } catch (err) { alert(err); } null")
        except Exception, ex:
            raise ex
        
    def loadConfiguration(self, conf):
        '''
            Loads configuration from configuration object (resizes window and sets window title)
            @param conf: configuration object
        '''
        if (conf != None):
            if (conf['__window'] != None):
                if (conf['__window']['width'] != None and conf['__window']['height'] != None):
                    self.window.resize(conf['__window']['width'], conf['__window']['height'])
            if (conf['appName'] != None):
                self.window.setWindowTitle(conf['appName'])
        
    def sendInvite(self,jid,appInfo):
        '''
            Sends IQ message with invitation
            @param jid: JID of the user on the other side
            @param appInfo: basic info about app                        
        '''
        iq = IQ(self.main.client.xmlstream, 'set')
        iq['xml:lang'] = self.main.client.xmlLang
        iq['type'] = 'set'
        iq['to'] = jid + '/jabbim'
        q = iq.addElement('query')
        q['xmlns']='http://xawa.vaisar.cz'
        s = q.addElement('session')
        if (appInfo != None):
            s['appName'] = appInfo['appName']
            s['appUrl'] = appInfo['appUrl']
        s.addElement('invite')
        
        conf = s.addElement('configuration')
        conf.addChild(json.dumps(appInfo)) # puts whole string inside the tag
        
        self.main.client.disp(iq['id'])
        d = iq.send()
        
        return d
    
    def onInvite(self, elem):
        '''
            Handles IQ messages with <session><invite /></session>
            @param elem: received element
        '''
        jid = self.main.getJid(elem['from']).userhost()
        q = elem.firstChildElement() # query
        s = q.firstChildElement() # session
        conf = None
        try:
            conf = json.loads(s.children[1].children[0]) # configuration object (if its present)
        except Exception, ex:
            # ok, it should be there, but we can be shure ...
            pass
        
        ques = QtGui.QMessageBox.question(self.main, 'Invitation', 'User ' + jid + ' invites you to join application "' + s['appName'] + '". Do you want to accept?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if ques == QtGui.QMessageBox.Yes:
            self.recipient = jid
            self._acceptInvitation(jid, s['appUrl'], conf)
        else:
            self._refuseInvitation(jid)
                    
        return False
    
    def onSession(self,elem):
        '''
            Handles IQ messages with <session />
            @param elem: received element
        '''
        q = elem.firstChildElement()
        ses = q.firstChildElement()
        res = ses.firstChildElement().name
        if self.windowOpened:
            if res == 'accept':
            # if accepted, let's fire JavaScript 'event'
                self.mainFrame.evaluateJavaScript('onInvitationAccept(); null')
            elif res == 'refuse':
            # if refused, let's fire JavaScript 'event'
                self.mainFrame.evaluateJavaScript('onInvitationRefuse(); null')
            elif res == 'leave':
                self.mainFrame.evaluateJavaScript('try { onSessionLeave(); } catch (err) { alert(err); } null')
        return False
      
    
    def _acceptInvitation(self, jid, url, conf):
        '''
            Sends IQ message with <session><accept /></session> and opens window with given app
            @param jid: JID of user on the other side
            @param url: URL of app ww are invited in
            @param conf: configuration object
        '''
        iq = IQ(self.main.client.xmlstream, 'set')
        iq['xml:lang'] = self.main.client.xmlLang
        iq['type'] = 'set'
        iq['to'] = jid + '/jabbim'
        q = iq.addElement('query')
        q['xmlns']='http://xawa.vaisar.cz'
        s = q.addElement('session')
        s.addElement('accept')
        s['appUrl'] = url
        self.main.client.disp(iq['id'])
        d = iq.send()
               
        ##open window with app
        self.openWindow()
        self.loadApp(url)
        self.loadConfiguration(conf)
        
        return d
    
    def _refuseInvitation(self, jid):
        '''
            Sends IQ message with <session><refuse /></session>
            @param jid: JID of user of the other side            
        '''
        iq = IQ(self.main.client.xmlstream, 'set')
        iq['xml:lang'] = self.main.client.xmlLang
        iq['type'] = 'set'
        iq['to'] = jid + '/jabbim'
        q = iq.addElement('query')
        q['xmlns']='http://xawa.vaisar.cz'
        s = q.addElement('session')
        s.addElement('refuse')
        self.main.client.disp(iq['id'])
        d = iq.send()
                
        return d
    
    def leaveSession(self):
        '''
            Sends IQ message width <session><leave /></session>
        '''
        iq = IQ(self.main.client.xmlstream, 'set')
        iq['xml:lang'] = self.main.client.xmlLang
        iq['type'] = 'set'
        iq['to'] = self.recipient + '/jabbim'
        q = iq.addElement('query')
        q['xmlns']='http://xawa.vaisar.cz'
        s = q.addElement('session')
        s.addElement('leave')
        self.main.client.disp(iq['id'])
        d = iq.send()        
        return d
            
    def on_message(self,msg):
        '''
            Handles incomming message
            @param msg: incomming message
        '''
        if (msg.body != None):
            if (msg.subject == 'xawa_data'):
                # this way is now obsolete 
                self.receivedData = unicode(msg.body)
                self.isDataUnread = True                            
                return False
            elif (msg.subject == 'xawa_message'):
                self.receivedMessage = unicode(msg.body)
                self.isMessageUnread = True               
                return False
        
        return True
        
    def onXawaMessage(self,elem):
        '''
            Handles on IQ messages with text or data
            @param elem: received element
        '''
        q = elem.firstChildElement() # query
        xm = q.firstChildElement() # xawaMessage
        if self.windowOpened:
            if (xm.name == "xawaMessage"):
                b = xm.firstChildElement() # body
                try:
                    escapedString = b.children[0].replace("'","\'")   
                    self.mainFrame.evaluateJavaScript("try { onMessageReceived('" + escapedString + "'); } catch(err) { alert(err); } null")
                except Exception, ex:
                    raise ex
                return False
            elif (xm.name == "xawaData"):
                d = xm.firstChildElement() # data
                try:
                    self.mainFrame.evaluateJavaScript("try { onDataReceived('" + d.children[0] + "'); } catch(err) { alert(err); } null")
                except Exception, ex:
                    raise ex
            
    def sendXawaMessage(self, message):
        '''
            Sends IQ message with text message
            @param message: text of message we want to send
        '''
        iq = IQ(self.main.client.xmlstream, 'set')
        iq['xml:lang'] = self.main.client.xmlLang
        iq['type'] = 'set'
        iq['to'] = self.recipient + '/jabbim'
        q = iq.addElement('query')
        q['xmlns']='http://xawa.vaisar.cz'
        xm = q.addElement('xawaMessage')
        b = xm.addElement('body')
        b.addChild(message)
        self.main.client.disp(iq['id'])
        d = iq.send()
        return d
    
    def sendXawaData(self, data):
        '''
            Sends IQ message with JSON data
            @param data: JSON string with data we want to send
        '''
        iq = IQ(self.main.client.xmlstream, 'set')
        iq['xml:lang'] = self.main.client.xmlLang
        iq['type'] = 'set'
        iq['to'] = self.recipient + '/jabbim'
        q = iq.addElement('query')
        q['xmlns']='http://xawa.vaisar.cz'
        xm = q.addElement('xawaData')
        b = xm.addElement('data')
        b.addChild(data)
        self.main.client.disp(iq['id'])
        d = iq.send()
        return d
     
    
    def sendDataInLecagyMode(self,data):
        '''
            sends plain text data - it should be JSON string
            @param data: JSON string with data we want to send
        '''
        try:
            self.sendIt(data, 'xawa_data')
        except Exception, ex:
            raise ex
            
    def sendMessage(self,message):
        '''
            sends plain text message to recipient with JID saved in self.recipient
            @param message: text of message we want to send
        '''
        try:
            self.sendIt(message, 'xawa_message')
        except Exception, ex:
            raise ex
    
    def sendIt(self,content,type):
        '''
            method for sending plain text through xmpp
            @param content: what to send
            @param type: how to send it
        '''
        m = Message(self.recipient)
        m.setBody(content)
        m.setSubject(unicode(type))
        m.setComposing("active")
        try:
            self.main.client.message.sendMessage(msg=m)
        except Exception, ex:
            raise ex
    