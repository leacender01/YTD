# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:51:19 2022

@author: arnold
"""
import errno
import subprocess
import sys
import time
import selenium
import yt_dlp

from os import system as CMDsystem
from re import compile as recompile
from warnings import warn as SysWarn
from platform import system as osSystem
from os.path import basename,abspath,join
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome import service, webdriver, remote_connection
from selenium.webdriver.common.by import By
from selenium import webdriver as swebdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from subprocess import PIPE, Popen,STDOUT
from home import Ui_HomePage
from Searching import Ui_SearchingPage
from Command import Ui_Command
#修正exe裡小黑窗出現問題
#隱藏chromeDriver.exe
class HiddenChromeService(service.Service):

    def start(self):
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())

            if osSystem() == 'Windows':
                info = subprocess.STARTUPINFO()
                info.dwFlags = subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = 0  # SW_HIDE (6 == SW_MINIMIZE)
            else:
                info = None

            self.process = subprocess.Popen(
                cmd, env=self.env,
                close_fds=osSystem() != 'Windows',
                startupinfo=info,
                stdout=self.log_file,
                stderr=self.log_file,
                stdin=subprocess.PIPE)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "Executable %s must be in path. %s\n%s" % (
                    basename(self.path), self.start_error_message,
                    str(e)))
        count = 0
        while True:
            self.assert_process_still_running()
            if self.is_connectable():
                break
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can't connect to the Service %s" % (
                    self.path,))
class HiddenChromeWebDriver(webdriver.WebDriver):
    def __init__(self, executable_path=ChromeDriverManager().install(), port=0,
                options=None, service_args=None,
                desired_capabilities=None, service_log_path=None,
                chrome_options=None, keep_alive=True):
        if chrome_options:
            SysWarn('使用自訂選項而非chrome預設',DeprecationWarning, stacklevel=2)
            options = chrome_options

        if options is None:
            # desired_capabilities stays as passed in
            if desired_capabilities is None:
                desired_capabilities = self.create_options().to_capabilities()
        else:
            if desired_capabilities is None:
                desired_capabilities = options.to_capabilities()
            else:
                desired_capabilities.update(options.to_capabilities())

        self.service = HiddenChromeService(
            executable_path,
            port=port,
            service_args=service_args,
            log_path=service_log_path)
        self.service.start()

        try:
            RemoteWebDriver.__init__(
                self,
                command_executor=remote_connection.ChromeRemoteConnection(
                    remote_server_addr=self.service.service_url,
                    keep_alive=keep_alive),
                desired_capabilities=desired_capabilities)
        except Exception:
            self.quit()
            raise
        self._is_remote = False
        
        
#監控YT並下達下載指令
# 需要chromedriver.exe 放在同一資料夾
class LiveMonitor(object):
    def __init__(self, os_type="win"):
        option = swebdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('blink-settings=imagesEnabled=false')
        option.add_argument('--disable-dev-shm-usage')
        # 環境加載 找範例的
        if os_type == "win":
            self.driver = HiddenChromeWebDriver(chrome_options=option)
        if os_type == "linux":
            self.driver = swebdriver.Chrome(ChromeDriverManager().install(), options=option)
        if os_type == "mac":
            raise BaseException
        self.driver.implicitly_wait(3)
        #SysWarn(abspath(r"./chromedriver"))
    # 利用關鍵字抓取正在直播
    # 回傳list 名稱 + 網址
    # 沒有回傳 None 
    def live_check(self, url):
        bsList = self.liveSearch(url)  # 利用BeautifulSoup抓取列表項目
        liveList = self.liveProcess(bsList)  # 分辨資料
        return liveList

    def liveSearch(self, channel_url):
        self.driver.get(channel_url)
        #SysWarn("..............搜尋直播中..............",DeprecationWarning, stacklevel=2)
        liveXpath = "//*[@id='contents' and @class='style-scope ytd-channel-featured-content-renderer']"
        try:
            t = self.driver.find_element(By.XPATH, (liveXpath))
        except selenium.common.exceptions.NoSuchElementException:
            #SysWarn("目前沒有直播",DeprecationWarning, stacklevel=2)
            return None
        return t.get_attribute("innerHTML")  
        
    def liveProcess(self, html):
        liveList = []
        if html is None:
            return liveList
        bsList = BeautifulSoup(html, features="html.parser")
        bsl = bsList.find_all("a", id="video-title")
        for b in bsl:
            liveList.append((b["aria-label"], b["href"]))
        return liveList
        

    # 利用關鍵字抓取預計直播
    # 回傳list 名稱 + 網址
    # 沒有回傳 None 
    def upcomingliveSearch(self, url):
        bsList = self.preliveSearch(url)
        liveList = self.preliveProcess(bsList, preCount=10)
        return liveList

    def preliveSearch(self, channel_url):
        # 到預計直播網頁 利用參數抓取有無直播 無直播會列出所有影片
        #self.driver.get(channel_url + "/videos?view=2&sort=dd&live_view=502&shelf_id=3")
        self.driver.get(channel_url)
        #SysWarn("..............搜尋預計直播中..............",DeprecationWarning, stacklevel=2)
        #liveXpath = "//*[@id='items' and @class='style-scope ytd-grid-renderer']"
        liveXpath = "//*[@id='contents' and @class='style-scope ytd-shelf-renderer']"
        try:
            t = self.driver.find_element(By.XPATH, (liveXpath))
        except selenium.common.exceptions.NoSuchElementException:
            #SysWarn("目前沒有預計直播",DeprecationWarning, stacklevel=2)
            return None
        return t.get_attribute('innerHTML')

    # preCount：判段數量
    def preliveProcess(self, html, preCount=10):
        preLiveList = []
        if html is None:
            return preLiveList
        bsList = BeautifulSoup(html, features="html.parser")
        bsl = bsList.find_all("div", id="meta")
        # 超過數量視為無預定
        if len(bsl) > preCount:
            return preLiveList
        for b in bsl:
            title = b.find_all("a", id="video-title")[0]["title"]
            link = b.find_all("a", id="video-title")[0]["href"]
            preLiveList.append((title, link))
        return preLiveList
    def getChannelName(self,channel_url):
        name = ""
        if channel_url is None:
            return name
        self.driver.get(channel_url)
        liveXpath = "//*[@id='text-container' and @class='style-scope ytd-channel-name']" 
        try:
            t = self.driver.find_element(By.XPATH, (liveXpath))
            name = t.get_attribute('textContent')
            
        except selenium.common.exceptions.NoSuchElementException:
            #SysWarn("找不到名字",DeprecationWarning, stacklevel=2)
            return None
        return  name
        
    #刪除自身
    def close(self):
        self.driver.quit()
        
#搜尋單一頻道子程序
class SearchThread(QtCore.QThread):
    url = 'unknown'
    savepath = r"./"
    signal_str_str = QtCore.pyqtSignal(str,str)
    def __init__(self, url,savepath):
        super().__init__()
        self.url = url
        self.savepath=savepath
        self.lm = LiveMonitor(os_type="win")
        self.runs = True
    def stopsearching(self):
        self.runs = False
        self.lm.close()
    def run(self):
        targetlist = []
        while self.runs:
            for k in self.lm.live_check(self.url):
                inlist = 0
                for old in targetlist:
                    if old == k[1]: #重複跳過
                        #SysWarn("已重複    !!!!!!!!!!!!!!",DeprecationWarning, stacklevel=2)
                        #SysWarn(k[1]," 名稱:",k[0],DeprecationWarning, stacklevel=2)
                        inlist = 1
                        break
    
                if inlist == 0 :#只處理不重複
                    #SysWarn(k[0],DeprecationWarning, stacklevel=2)
                    #SysWarn(k[1],DeprecationWarning, stacklevel=2)
                    if len(k[1]) > 10 :
                        self.signal_str_str.emit(self.savepath,f"https://www.youtube.com{k[1]}")
                        targetlist.append(k[1])
            time.sleep(57)
#下載影片子程序      
class urlThread(QtCore.QThread):
    url = 'unknown'
    index = 1
    stype = 'mp4'
    urlpath=r""
    signal_int_str = QtCore.pyqtSignal(int,str)
    def __init__(self, url, index, stype, urlpath):
        super().__init__()
        self.url = url
        self.index = index-1
        self.stype = stype
        self.urlpath=urlpath
        #SysWarn(self,DeprecationWarning, stacklevel=2)
        #SysWarn('test',DeprecationWarning, stacklevel=2)

    def run(self):
        
        ydl_opts = {
            'format'  : self.stype,
            'outtmpl' : self.urlpath+r"\\%(release_date>%Y%m%d,upload_date>%Y%m%d|Unknown)s\\%(format)s\\%(title)s.%(ext)s",
            'writedescription':True,
            'writethumbnail':True,
            'socket_timeout':20,
            'wait_for_video':(20,30),
            'fixup':'detect_or_warn',
            'sleep_interval_requests':1,
            'live_from_start':True,
            'cookiesfrombrowser':('chrome', ),
            'ffmpeg_location':join(abspath(r"./"),r"ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"),
            'extractor_retries':20,
            'retries':20,
            'file_access_retries':10,
            'progress_hooks': [self.downloadinginfo]
        }
        #SysWarn(join(abspath(r"./"),r"ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"),DeprecationWarning, stacklevel=2)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.url)
    def downloadinginfo(self,d):
        if d['status'] == 'downloading':
            dltype = d['_eta_str'].find("Unknown")
            if self.stype=='bv*+ba/b':
                stype = '影片'
            elif self.stype=='bv':
                stype = '畫面'
            elif self.stype=='ba':
                stype = '音檔'
            if dltype == -1:
                self.signal_int_str.emit(self.index, f"時間:{time.strftime('%H:%M:%S', time.gmtime(d['elapsed']))} 進度:{d['_percent_str']} \n格式:{stype} 剩餘時間:{d['_eta_str']} \nnow downloading:{basename(d['filename'])}")
            else:
                self.signal_int_str.emit(self.index, f"時間:{time.strftime('%H:%M:%S', time.gmtime(d['elapsed']))} 進度:下載中  \n格式:{stype} 剩餘時間:直播中 \nnow downloading:{basename(d['filename'])}")
        elif d['status'] == 'finished':
            self.signal_int_str.emit(self.index, f"完成下載:{basename(d['filename'])}")
#刷新用每秒回報子程序
class threadtime(QtCore.QThread):
    signal_update = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.runs = True
    def stopthread2s(self):
        self.runs = False
    def run(self):
        while self.runs:
            time.sleep(1)
            self.signal_update.emit()

#指令執行內容子程序
class cmd(QtCore.QThread):
    signal_cmd = QtCore.pyqtSignal(str)
    command="unknow"
    def __init__(self,command):
        self.command = command
        super().__init__()
        self.runs = True
        self.process = Popen(
            args=self.command,
            stdout=PIPE,
            stderr=STDOUT,
            shell=True,
            universal_newlines=True,
            encoding='utf8'
        )
    def stoptcmd(self):
        self.runs = False
    def run(self):
        for line in self.process.stdout:
            #SysWarn(line,DeprecationWarning, stacklevel=2)
            self.signal_cmd.emit(line)
        self.signal_cmd.emit("完成操作")
            
        
#用於輸出指令執行內容
class CommandWindow(QtWidgets.QDialog):
    signal_str = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_Command()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.close)
        self.signal_str.connect(self.createcmd)
    def createcmd(self,comands):
        self.cmds = cmd(comands)
        self.cmds.signal_cmd.connect(self.refreshcmd)
        self.cmds.start()
        
    def refreshcmd(self,text):#將文字以空格換行並顯示
        if text == "完成操作":
            self.ui.pushButton.setText("關閉頁面")
            self.ui.pushButton.setEnabled(True)
        text = text.replace(" ","\n")
        textlist = text.split("\n")
        outlist=[]
        poplist=[]
        for line in textlist:
            if line.strip() !="":
                outlist.append(line)
        for idx,tex in enumerate(outlist[:-1]):
            if tex == ":":
                outlist[idx] = outlist[idx-1] + outlist[idx] + outlist[idx+1]
                poplist.append(idx-1)
                poplist.append(idx+1)
            elif tex[-1] == "=" or tex[-1] == ":":
                outlist[idx] = outlist[idx] + outlist[idx+1]
                poplist.append(idx+1)
        for i in reversed(poplist):
            outlist.pop(i)
        self.ui.label.setText("\n".join(outlist))
        

        
#設定監控頻道子頁面
class AddSearchingWindow(QtWidgets.QDialog):
    signal_str = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui = Ui_SearchingPage()
        self.ui.setupUi(self)
        self.ui.btn_yes.clicked.connect(self.passurl)
    def passurl(self):
        url = self.ui.urlInput.text()
        #使用正則表達把YT頻道拉出來,YT頻道前面會有@
        Pattern = r'.*@\w+'
        url = recompile(Pattern).findall(url)[0]
        
        SysWarn(url,DeprecationWarning, stacklevel=2)
        self.signal_str.emit(url)
        self.close()
#主頁面
class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        
        #home tab
        self.SearchList=[]
        self.SearchNameList=[]
        self.Searchpath=[]
        self.Searchwork=[]
        self.DownloadList=[]
        self.Downloadwork=[]
        self.lm1 = LiveMonitor(os_type="win")
        
        self.ui.btn_urlDL.clicked.connect(self.urlDL)
        self.ui.btn_add.clicked.connect(self.addSearching)
        self.ui.btn_del.clicked.connect(self.dellist)
        self.updatethread = threadtime()
        self.updatethread.signal_update.connect(self.refreshDLlist)
        self.updatethread.start()
        
        #merge tab
        
        self.ui.btn_merge_v.clicked.connect(self.merge_v)
        self.ui.btn_merge_a.clicked.connect(self.merge_a)
        self.ui.btn_merge_o.clicked.connect(self.merge_o)
        
        
        #change tab
        self.ui.btn_change_v.clicked.connect(self.change_in)
        self.ui.btn_change_o.clicked.connect(self.change_out)
        
        self.show()
    #close event
    def closeEvent(self,a0:QtGui.QCloseEvent) -> None:
        for woker in self.Searchwork:
            woker.stopsearching()
        self.updatethread.stopthread2s()
        self.lm1.close()
        CMDsystem('taskkill /F /IM conhost.exe')
        super().closeEvent(a0)
    #home tab def
    def downLoadURL(self,path,url):
        #這邊可以增加一次要載的格式
        #https://github.com/yt-dlp/yt-dlp#format-selection-examples:~:text=dlp%20%2Do%20%2D%20BaW_jenozKc-,%E6%A0%BC%E5%BC%8F%E9%81%B8%E6%93%87,-%E9%BB%98%E8%AA%8D%E6%83%85%E6%B3%81%E4%B8%8B
        for idx,ext in enumerate(['bv*+ba/b','bv','ba']):
            self.DownloadList.append("新下載! 請耐心等候開始!")
            self.ui.DLlist.clear()
            self.ui.DLlist.addItems(self.DownloadList)
            
            self.Downloadwork.append(urlThread(url, len(self.DownloadList),ext,path))
            self.Downloadwork[-1].signal_int_str.connect(self.updateDLlist)
            self.Downloadwork[-1].start()
        
    def urlDL(self):
        if self.ui.urlInput.text() != "":
            path = QtWidgets.QFileDialog.getExistingDirectory()
            self.downLoadURL(path, self.ui.urlInput.text())
            self.ui.urlInput.clear()
    def updateDLlist(self,index,text):
        self.DownloadList[index]=text
    def refreshDLlist(self):
        self.ui.DLlist.clear()
        self.ui.DLlist.addItems(self.DownloadList)
        
    def addSearching(self):
        self.addSearching_window = AddSearchingWindow()
        self.addSearching_window.signal_str.connect(self.addlist)
        self.addSearching_window.exec()
    def addlist(self,url):
        if url not in self.SearchList:
            try:
                self.SearchNameList.append(self.lm1.getChannelName(url))
                #SysWarn(self.SearchNameList,DeprecationWarning, stacklevel=2)
                self.SearchList.append(url)
                self.Searchpath.append(QtWidgets.QFileDialog.getExistingDirectory())
                self.ui.Slist.clear()
                self.ui.Slist.addItems(self.SearchNameList)
                
                for idx,surl in enumerate(self.SearchList):
                    new=True
                    for woker in self.Searchwork:
                        if woker.url == surl:
                            new = False
                    if new:
                        self.Searchwork.append(SearchThread(surl,self.Searchpath[idx]))
                        self.Searchwork[-1].signal_str_str.connect(self.downLoadURL)
                        self.Searchwork[-1].start()
            except:
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,"警告","請輸入youtube主頁網址")
                msg_box.exec()
    def dellist(self):
        idx = self.ui.Slist.currentRow()
        if idx>-1:
            for woker in self.Searchwork:
                if woker.url == self.SearchList[idx]:
                    woker.stopsearching()
            self.SearchNameList.pop(idx)
            self.SearchList.pop(idx)
            self.Searchpath.pop(idx)
            self.ui.Slist.clear()
            self.ui.Slist.addItems(self.SearchNameList)
    #merge tab def
    def merge_v(self):
        self.ui.lineEdit_merge_v.setText(QtWidgets.QFileDialog.getOpenFileName()[0])
    def merge_a(self):
        self.ui.lineEdit_merge_a.setText(QtWidgets.QFileDialog.getOpenFileName()[0])
    def merge_o(self):
        if self.ui.lineEdit_merge_o.text() == "":
            #取得影片檔案名稱(去除副檔名及路徑)
            self.ui.lineEdit_merge_o.setText(".".join(self.ui.lineEdit_merge_v.text().split("/")[-1].rsplit('.')[:-1]))
        else:
            SysWarn(self.ui.lineEdit_merge_o.text(),DeprecationWarning, stacklevel=2)
        if self.ui.lineEdit_merge_v.text() != "" and self.ui.lineEdit_merge_a.text() != "" and self.ui.lineEdit_merge_o.text() != "":
            #do
            path = QtWidgets.QFileDialog.getExistingDirectory()
            cmd=f' -i "{self.ui.lineEdit_merge_v.text()}" -i "{self.ui.lineEdit_merge_a.text()}" -map 0:v:? -map 1:a:? "{path}//{self.ui.lineEdit_merge_o.text()}.mkv"'
            cmd = join(abspath(r"./"),r"ffmpeg-master-latest-win64-gpl\bin\ffmpeg") + cmd
            
            self.commandWindow = CommandWindow()
            self.commandWindow.signal_str.emit(cmd)
            self.commandWindow.exec()
            #SysWarn(f"{self.ui.lineEdit_merge_o.text()}.mkv",DeprecationWarning, stacklevel=2)
            self.ui.lineEdit_merge_o.setText("")
        else:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,"警告","請輸入影片檔以及音訊檔")
            msg_box.exec()
            
    #change tab def
    def change_in(self):
        self.ui.lineEdit_change_v.setText(QtWidgets.QFileDialog.getOpenFileName()[0])
    def change_out(self):
        if self.ui.lineEdit_change_o.text() == "":
            #取得影片檔案名稱(去除副檔名及路徑)
            self.ui.lineEdit_change_o.setText(".".join(self.ui.lineEdit_change_v.text().split("/")[-1].rsplit('.')[:-1]))
        else:
            SysWarn(self.ui.lineEdit_change_o.text(),DeprecationWarning, stacklevel=2)
        if self.ui.lineEdit_change_v.text() != "" and self.ui.lineEdit_change_o.text() != "":
            path = QtWidgets.QFileDialog.getExistingDirectory()
            cmd=f' -i "{self.ui.lineEdit_change_v.text()}" "{path}//{self.ui.lineEdit_change_o.text()}.{self.ui.comboBox_change.currentText()}"'
            cmd = join(abspath(r"./"),r"ffmpeg-master-latest-win64-gpl\bin\ffmpeg") + cmd
            
            self.commandWindow = CommandWindow()
            self.commandWindow.signal_str.emit(cmd)
            self.commandWindow.exec()
        else:
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,"警告","請輸入影片檔")
            msg_box.exec()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())