# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:51:19 2022

@author: arnold
"""

import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from home import Ui_HomePage
import yt_dlp
import time


class urlThread(QtCore.QThread):
    thread_name = 'unknown'
    sleep_seconds = 1
    def __init__(self, thread_name, sleep_seconds):
        super().__init__()
        self.thread_name = thread_name
        self.sleep_seconds = sleep_seconds
        print(self)

    def run(self):
        print(self.ui.urlInput.text())
        if self.ui.urlInput.text() !="":
            self.urlpath = QtWidgets.QFileDialog.getExistingDirectory()
            
            self.DownloadList.append("新下載!")
            self.slm.setStringList(self.DownloadList)
            ydl_opts = {
                'format'  : 'mp4',
                'outtmpl' : self.urlpath+r"\\%(upload_date)s\\%(title)s.%(ext)s",
                'writedescription':True,
                'writethumbnail':True,
                'socket_timeout':20,
                'wait_for_video':10,
                'fixup':'detect_or_warn',
                'live_from_start':True,
                'ffmpeg_location':os.path.abspath(r"./")+r"\\ffmpeg.exe",
                'extractor_retries':20,
                'retries':20,
                'file_access_retries':10,
                'progress_hooks': [self.downloadinginfo]
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(self.ui.urlInput.text())
            print(error_code)
    def downloadinginfo(self,d):
        
        if d['status'] == 'downloading' and (time.time()-self.t)>1:
            self.t=time.time()
            self.DownloadList[-1]=f"進度:{d['_percent_str']} eta:{d['_eta_str']} now downloading:{os.path.basename(d['filename'])}"
            self.slm.setStringList(self.DownloadList)
            #print("==============================================")
            #print(f"進度:{d['_percent_str']} eta:{d['_eta_str']} now downloading:{os.path.basename(d['filename'])}")
            #print("==============================================")
        elif d['status'] == 'finished':
            self.DownloadList[-1]=f"完成下載:{os.path.basename(d['filename'])}"
            self.slm.setStringList(self.DownloadList)
            print(f"完成下載:{os.path.basename(d['filename'])}")
            
            
class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_HomePage()
        self.ui.setupUi(self)
        
        self.slm = QtCore.QStringListModel()
        self.ui.DLlist.setModel(self.slm)
        self.SearchList=[]
        self.DownloadList=[]
        self.urlpath = ""
        self.t=time.time()
        self.ui.btn_urlDL.clicked.connect(self.callurl)
        
        self.show()
    def callurl(self):
        work1 = urlThread('work 1', 2)
        work1.start()
    def urlDL(self):
        print(self.ui.urlInput.text())
        if self.ui.urlInput.text() !="":
            self.urlpath = QtWidgets.QFileDialog.getExistingDirectory()
            
            self.DownloadList.append("新下載!")
            self.slm.setStringList(self.DownloadList)
            ydl_opts = {
                'format'  : 'mp4',
                'outtmpl' : self.urlpath+r"\\%(upload_date)s\\%(title)s.%(ext)s",
                'writedescription':True,
                'writethumbnail':True,
                'socket_timeout':20,
                'wait_for_video':10,
                'fixup':'detect_or_warn',
                'live_from_start':True,
                'ffmpeg_location':os.path.abspath(r"./")+r"\\ffmpeg.exe",
                'extractor_retries':20,
                'retries':20,
                'file_access_retries':10
                #'progress_hooks': [self.downloadinginfo]
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(self.ui.urlInput.text())
            print(error_code)
    def downloadinginfo(self,d):
        
        if d['status'] == 'downloading' and (time.time()-self.t)>1:
            self.t=time.time()
            self.DownloadList[-1]=f"進度:{d['_percent_str']} eta:{d['_eta_str']} now downloading:{os.path.basename(d['filename'])}"
            self.slm.setStringList(self.DownloadList)
            #print("==============================================")
            #print(f"進度:{d['_percent_str']} eta:{d['_eta_str']} now downloading:{os.path.basename(d['filename'])}")
            #print("==============================================")
        elif d['status'] == 'finished':
            self.DownloadList[-1]=f"完成下載:{os.path.basename(d['filename'])}"
            self.slm.setStringList(self.DownloadList)
            print(f"完成下載:{os.path.basename(d['filename'])}")

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())