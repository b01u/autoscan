#!/usr/bin/env python
# coding=utf-8
# author: b0lu
# mail: b0lu@163.com
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from PySide import QtGui
from PySide import QtWebKit
from PySide import QtCore
from PySide import QtNetwork
import time, subprocess, os, codecs

default_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 " +\
    "(KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2"

class QQHttpResponse(object):
    def __init__(self, reply, content):
        self.url = reply.url().toString()
        try:
            self.content = str(content)
        except UnicodeDecodeError:
            self.content = content
        self._reply = reply
        self.status = reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        self.headers = {}
        for header in reply.rawHeaderList():
            self.headers[str(header)] = str(reply.rawHeader(header))

class QQWebPage(QtWebKit.QWebPage):
        def __init__(self, app):
            super(QQWebPage, self).__init__(app)
            self.xss = False
            #self.javaScriptAlert = lambda frame, msg: print msg

        def javaScriptAlert(self, frame, msg):
            if msg == "/b0lu/":
                self.xss = True
                print "There is a xss :"+msg

        def setUserAgent(self, user_agent):
            self.user_agent = user_agent

def replyReadyRead(reply):
    if not hasattr(reply, 'data'):
        reply.data = ''
    reply.data += reply.peek(reply.bytesAvailable())


class QNetManager(QtNetwork.QNetworkAccessManager):
    def createRequest(self, operation, request, data):
        reply = QtNetwork.QNetworkAccessManager.createRequest(self,operation,request,data)
        reply.readyRead.connect(lambda reply=reply: replyReadyRead(reply))
        time.sleep(0.001)
        return reply

class  QBrowser(object):
    def __init__(
        self,
        web_page_class = QQWebPage
    ):
        super( QBrowser, self).__init__()
        self.isLoaded = False    
        try:
            os.environ['DISPLAY'] = ':99'
            process = ['Xvfb', ':99', '-pixdepths', '25']
            FNULL = open(os.devnull, 'w')
            self.xvfb = subprocess.Popen(process, stdout=FNULL, stderr=subprocess.STDOUT)
        except OSError:
            raise Error('xvfb is required')
        
        self.app = QtGui.QApplication.instance() or QtGui.QApplication([])
        #self.app =  QtCore.QCoreApplication([])
        self.page = web_page_class(self.app)
        self.page.setUserAgent(default_user_agent)
        self.page.loadFinished.connect(self._page_loaded_call_back)
        self.page.loadStarted.connect(self._page_started_call_back)
        self.page.setNetworkAccessManager(QNetManager())
        
        self.response = None

        self.net = self.page.networkAccessManager()
        self.net.finished.connect(self._net_finished_call_back)
        
        self.cookie_jar = QtNetwork.QNetworkCookieJar()
        self.net.setCookieJar(self.cookie_jar)

        self.frame = self.page.mainFrame()

        QtWebKit.QWebSettings.setMaximumPagesInCache(0)
        QtWebKit.QWebSettings.setObjectCacheCapacities(0, 0, 0)
        QtWebKit.QWebSettings.globalSettings().setAttribute(QtWebKit.QWebSettings.LocalStorageEnabled, True)
        self.page.setForwardUnsupportedContent(True)
        self.page.settings().setAttribute(QtWebKit.QWebSettings.AutoLoadImages, True)
        self.page.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, False)
        self.page.settings().setAttribute(QtWebKit.QWebSettings.JavaEnabled, False)
        self.page.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)

    def _net_finished_call_back(self, reply):
        if reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute):
            url = self.frame.url().toString()
            url_without_hash = url.split("#")[0]
            if url == reply.url().toString() or url_without_hash == reply.url().toString():
                try:
                    content = reply.data
                except AttributeError:
                    content = reply.readAll()
                self.response = QQHttpResponse(reply, content)

    def load(self, url, method = "get", headers = {}, post_data = ""):
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.CacheLoadControl(0)
        for header in headers:
            if header != "Accept-Encoding":
                request.setRawHeader(QtCore.QByteArray(header), QtCore.QByteArray(headers[header]))
        
        method = getattr(QtNetwork.QNetworkAccessManager, "%sOperation"%method.capitalize())
        self.frame.load(request, method, QtCore.QByteArray(post_data))
        self.isLoaded = False
        self._wait()

    def evaluate(self, script):
        self.frame.evaluateJavaScript("%s"%script)
        self.loop_event()

    def evaluate_js_file(self, jsfile, encoding="utf-8"):
        with codecs.open(jsfile, encoding=encoding) as f:
            js = f.read()
            self.evaluate(js)
            time.sleep(0.5)

    def toHtml(self):
        content = str(self.frame.toHtml())
        return content

    def toText(self):
        return self.frame.toPlainText()

    def _wait(self):
        start_time = time.time()
        while self.isLoaded is False and start_time + 6 < time.time():
            self.loop_event()

    def close(self):
        self.app.quit()
        self.xvfb.terminate()
        del self.page
        del self.frame

    def _page_loaded_call_back(self):
        self.isLoaded = True
        time.sleep(0.01)

    def _page_started_call_back(self):
        self.isLoaded = False
        time.sleep(0.01)

    def loop_event(self):
        start_time = time.time()
        while start_time + 0.1 > time.time():
            time.sleep(0.01)
            self.app.processEvents()


