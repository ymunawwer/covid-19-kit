#!/usr/bin/env python
# coding: utf-8

# In[1]:

print('Please Wait...')

import serial as serial
import face_recognition
import cv2
import numpy as np
import firebase as firebase
import glob
import os
from datetime import datetime
import serial as serial
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel,QDateEdit, QGridLayout,QTimeEdit,QWidget,QFrame,QErrorMessage,QFileDialog,QAction,QToolBar,QComboBox, qApp, QApplication,QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import QSize,Qt, QTimer
from PyQt5.QtGui import *
import sys
import math
import os
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import cv2
import numpy as np
import glob
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import time


# In[2]:




class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)
        
        


# In[3]:


class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        #self.ser = serial.Serial(port='COM3', baudrate=115200, bytesize=8, parity='N', stopbits=1)
        
        self.seperator_vertical = QVSeperationLine()
        self.seperator_horizontal = QHSeperationLine()
        self.initUI()
        self.setWindowTitle("MainWindow")

    def initUI(self):
        self.homeUI()
        
        
    def homeUI(self):
        self.preview_widget = QWidget()
        self.footer_widget = QWidget()
        self.home = True
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.cap = None                                        #  -capture <-> +cap
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QLabel()
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        
        self.temp = QLabel()
        self.temp.setText("Temperature:")
        self.temp.setObjectName("temp")
        
        self.temp_reading = QLabel()
        self.temp_reading.setText("temp_reading")
        self.temp_reading.setObjectName("temp_reading")
        
        self.temp2 = QLabel()
        self.temp2.setText("Temperature 2:")
        self.temp2.setObjectName("temp2")
        
        self.temp2_reading = QLabel()
        self.temp2_reading.setText("Temperature2 Reading")
        self.temp2_reading.setObjectName("temp2_reading")
        
        self.image_label.setScaledContents(True)
        
        self.matplotlibWidget = MatplotlibWidget(self)
        self.threadSample = ThreadSample(self)
        self.threadSample.newSample.connect(self.on_threadSample_newSample)
        self.threadSample.finished.connect(self.on_threadSample_finished)
        
        self.gridLayout = QGridLayout(self) 
        self.gridLayout.addWidget(self.temp,0,0)
        self.gridLayout.addWidget(self.temp_reading,0,1)
        self.gridLayout.addWidget(self.temp2,1,0)
        self.gridLayout.addWidget(self.temp2_reading,1,1)
        
        
        self.horizontalLayout.addWidget(self.image_label)
        self.horizontalLayout.addWidget(self.seperator_vertical)
        self.horizontalLayout.addLayout(self.gridLayout)
        
        self.preview_widget.setLayout(self.horizontalLayout)
        self.preview_widget.setMinimumHeight(200)
        self.preview_widget.setMaximumHeight(200)
        self.preview_widget.setMinimumWidth(600)
        self.preview_widget.setMaximumWidth(600)
        
        
        
        
        self.horizontalLayout2.addWidget(self.matplotlibWidget)
        self.horizontalLayout2.addWidget(self.seperator_vertical)
        #self.horizontalLayout2.addWidget(self.clock)
        self.clock(self.horizontalLayout2)
        
        self.footer_widget.setLayout(self.horizontalLayout2)
        self.footer_widget.setMinimumHeight(250)
        self.footer_widget.setMaximumHeight(250)
        self.footer_widget.setMinimumWidth(600)
        self.footer_widget.setMaximumWidth(600)
        
        self.verticalLayout.addWidget(self.preview_widget)
        self.verticalLayout.addWidget(self.seperator_horizontal)
        self.verticalLayout.addWidget(self.footer_widget)
        #self.verticalLayout.addWidget(self.image_label2)
       
        
        self.timer = QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self._image_counter = 0
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)  
        self.centralWidget().setLayout(self.verticalLayout)
#         self.setCentralWidget(self.scroll)
        self.setGeometry( 300, 300, 400, 700 )

    def read_temp(self):
        temp = []
        while True:
            self.ser.write(b'0x55,0xAA,5,1,4')
            response = self.ser.readline()
            #print(str(response))
            if 'body' in str(response):
                temp.append(str(response))
                #print("temp-"+str(response))
                #print(temp)
            elif 'Vbat' in str(response):
                if len(temp)!=0:
                    print("Done-"+ ' '.join(temp))
                    self.start_webcam()
                    self.update_frame(self.filter(''.join(temp)))
                temp = []
    def filter(self,text):
        
        text = text.replace('bTbody','body')
        text = text.replace('\'','')
        
        text = text.replace('\\r\n\'b\'Tbody','-')
        text = text.replace('\\r','')
        text = text.replace('\r','')
        text = text.replace('\\xa8','')
        text = text.replace('\\xa1\\xe6','')
        text = text.replace('\\n','-')
        text = text.replace(' ','')
        text = text.replace(', ',',')
        text = text.replace('=','_')
        text = text.replace(',','-')
        return text    
        
    
    @QtCore.pyqtSlot()
    def start_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
        self.timer.start()
        
    def closeEvent(self, event):
        print("closing PyQtTest")
        self.cap.close()

    @QtCore.pyqtSlot()
    def update_frame(self,file_name):
        ret, image = self.cap.read()
        self.face_detect(image,file_name)
        simage     = cv2.flip(image, 1)
        self.displayImage(image, True)

    def face_detect(self,image,file_name):
        frame = image
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        i = 0
        face_detect = True
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        self.dirname = 'd:'
                # Only process every other frame of video to save time
        if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                face_detect=False
                name = "Unknown"
                cv2.imwrite(os.path.abspath(os.path.join(self.dirname,(datetime.today().strftime('%Y-%m-%d')+'-'+file_name+'-'+str(++i)+'.png'))),frame)
                #self.storage.upload(self.dirname,(datetime.today().strftime('%Y-%m-%d')+'-'+file_name+'-'+str(i)+'.png'))


                i = i+1
                        

                print("I see someone named {}!".format(name))
                        # # If a match was found in known_face_encodings, just use the first one.
                        # if True in matches:
                        #     first_match_index = matches.index(True)
                        #     name = known_face_names[first_match_index]

                        # Or instead, use the known face with the smallest distance to the new face
                        

                process_this_frame = not process_this_frame


        
    @staticmethod
    @QtCore.pyqtSlot()
    def capture_image(self):
        flag, frame = self.cap.read()
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
      
        self.save_seq += 1

        path = self.save_path                         # 
        if flag:
            QtWidgets.QApplication.beep()
            name = "my_image.jpg"
            cv2.imwrite(os.path.join(self.save_path, "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )), frame)
            self._image_counter += 1

    
    def displayImage(self, img, window=True):
        qformat = QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.image_label.setStyleSheet("""
        QLabel {
            height:300px !important;
            
            }
        """)
            
            self.image_label.setPixmap(QPixmap.fromImage(outImage))
    
    def clock(self,layout):
        self.verticalLayoutClock = QVBoxLayout(self)
        self.dateEdit = QDateEdit(self)
        self.dateEdit.setDisplayFormat("MMM dd yyyy")
        self.dateEdit.setDisabled(True) 
        self.verticalLayoutClock.addWidget(self.dateEdit)
        self.timeEdit = QTimeEdit(self)
        self.timeEdit.setDisplayFormat("hh:mm:ss AP")
        self.timeEdit.setDisabled(True) 
        self.verticalLayoutClock.addWidget(self.timeEdit)
        self.updateTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)
        layout.addLayout(self.verticalLayoutClock)
        
    @QtCore.pyqtSlot(list)
    def on_threadSample_newSample(self, sample):
        self.matplotlibWidget.axis.plot(sample)
        self.matplotlibWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def on_threadSample_finished(self):
        self.samples += 1
        if self.samples <= 2:
            self.threadSample.start()
            
    @QtCore.pyqtSlot()
    def on_pushButtonPlot_clicked(self):
        self.samples = 0
        self.matplotlibWidget.axis.clear()
        self.threadSample.start()
            
    def updateTime(self):
        current = QtCore.QDateTime.currentDateTime()
        self.dateEdit.setDate(current.date())
        self.timeEdit.setTime(current.time())
        
        


# In[4]:


class GalleryWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.scrollView()
    
    def scrollView(self):
        self.home = False
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget() 
        self.widget_image = QWidget() # Widget that contains the collection of Vertical Box
        self.hbox = QHBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox = QVBoxLayout() 
        
        self.gridLayout_gallery = QGridLayout(self) 
        
        
        for img in self.getImage():
            widget_image = QWidget()
            hbox = QHBoxLayout()
            gridLayout_gallery = QGridLayout(self)
            object = QLabel("TextLabel")
            temp = QLabel("Temp:")
            temp_reading = QLabel("Reading")
            temp2 = QLabel("Temp2:")
            temp2_reading = QLabel("Reading")
            
            time = QLabel("Time:")
            time_reading = QLabel("Reading")
            
            date = QLabel("Date:")
            date_reading = QLabel("Reading")
            
            object.setPixmap(QPixmap(img))
            hbox.addWidget(object)
            
            
            gridLayout_gallery.addWidget(time,0,0)
            gridLayout_gallery.addWidget(time_reading,0,1)
            gridLayout_gallery.addWidget(date,1,0)
            gridLayout_gallery.addWidget(date_reading,1,1)
            gridLayout_gallery.addWidget(temp,2,0)
            gridLayout_gallery.addWidget(temp_reading,2,1)
            gridLayout_gallery.addWidget(temp2,3,0)
            gridLayout_gallery.addWidget(temp2_reading,3,1)
            
            
            hbox.addLayout(gridLayout_gallery)
            widget_image.setLayout(hbox)
            widget_image.setMaximumHeight(250)
            widget_image.setMinimumHeight(250)
            self.vbox.addWidget(widget_image)
            
            

        self.widget.setLayout(self.vbox)
        self.widget.setMaximumWidth(350)
        self.widget.setMinimumWidth(350)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setGeometry( 300, 300, 400, 700 )
        self.setCentralWidget(self.scroll)
    
    def getImage(self):
        img_path = []
        for img in glob.glob("d:/*.jpg"):

            img_path.append(img)
        return img_path
    

        


# In[5]:


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)
        
        self.layoutVertical = QtWidgets.QVBoxLayout(self)#QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)

class ThreadSample(QtCore.QThread):
    newSample = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadSample, self).__init__(parent)

    def run(self):
        randomSample = random.sample(range(0, 10), 10)

        self.newSample.emit(randomSample)


# In[6]:


class QHSeperationLine(QFrame):
  '''
  a horizontal seperation line\n
  '''
  def __init__(self):
    super().__init__()
    self.setMinimumWidth(1)
    self.setFixedHeight(20)
    self.setFrameShape(QtWidgets.QFrame.HLine)
    self.setFrameShadow(QtWidgets.QFrame.Sunken)
    self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
    return

class QVSeperationLine(QFrame):
  '''
  a vertical seperation line\n
  '''
  def __init__(self):
    super().__init__()
    self.setFixedWidth(20)
    self.setMinimumHeight(1)
    self.setFrameShape(QtWidgets.QFrame.VLine)
    self.setFrameShadow(QtWidgets.QFrame.Sunken)
    self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
    return


# In[7]:


class Overlay(QWidget):

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
    
    def paintEvent(self, event):
    
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.setPen(QPen(Qt.NoPen))
        
        for i in range(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QBrush(QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QBrush(QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height()/2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20)
        
        painter.end()
        
        
    
    
    def showEvent(self, event):
    
        self.timer = self.startTimer(50)
        self.counter = 0
    
    def timerEvent(self, event):
    
        self.counter += 1
        self.update()
        if self.counter == 600:
            self.killTimer(self.timer)
            self.hide()


# In[8]:



class ARCWindow(QMainWindow):
    def __init__(self):
        self.home = True
        QMainWindow.__init__(self)
        self.seperator_vertical = QVSeperationLine()
        self.seperator_horizontal = QHSeperationLine()
        #self.homeUI()
        self.setMinimumSize(QSize(640, 480))    
        self.setWindowTitle("ARC") 
        self.statusmessage("Ready")
        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            pass #quit

#         self.status = QStatusBar()
#         self.setStatusBar(self.status)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(GalleryWindow(), "gallery")

        self.goto()

   
            


        self.save_path = ""

        

        # Set the default camera.
        #self.select_camera(0)
        
#       menuBar
    
    
        self.menubarUI()
    
    
    

        
        
#         Toolbar

        self.toolbarUI()
         
        #         scrollview
        #self.scrollView()
        
        
        
        #gridLayout = QGridLayout(self)     
        #centralWidget.setLayout(gridLayout)  
        
        #time = QLabel("Time:", self)
        #temp = QLabel("temp:", self)
        #image = QLabel("Image:", self)
        
        #time.setAlignment(QtCore.Qt.AlignRight) 
        
        #temp.setAlignment(QtCore.Qt.AlignRight) 
        #gridLayout.addWidget(time, 0, 1)
        #gridLayout.addWidget(temp, 1, 1)
        #gridLayout.addWidget(temp, 0, 0,2,2)
        self.overlay = Overlay(self.centralWidget())
        self.overlay.hide()
    
    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    
    def goto(self):
        #name = 'main' if self.home else 'gallery'
        if self.home:
            self.name = 'main'
            self.home = False
        else:
            self.name = 'gallery'
            self.home=True
        if self.name in self.m_pages:
            widget = self.m_pages[self.name]
            self.stacked_widget.setCurrentWidget(widget)
            #self.setWindowTitle(widget.windowTitle())
        
   
    

        
    @QtCore.pyqtSlot()
    def capture_image(self):
        flag, frame = self.cap.read()
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.current_camera_name = 0
        self.save_seq += 1
        
        path = self.save_path                         # 
        if flag:
            QtWidgets.QApplication.beep()
            name = "my_image.jpg"
            cv2.imwrite(os.path.join(self.save_path, "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )), frame)
            self._image_counter += 1

    
    
            
        
    def toolbarUI(self):
        
        
        plotGraph = QAction(QIcon(os.path.join('icon', 'chart_line.jpg')), 'Plot', self)
        plotGraph.setShortcut('Ctrl+P')
        
        plotGraph.setStatusTip("Plot Graph")
        #self.pushButtonPlot.setText("Plot")
       # plotGraph.triggered.connect(self.on_pushButtonPlot_clicked)
        #self.pushButtonPlot.clicked.connect(self.on_pushButtonPlot_clicked)
        
        

        exitAct = QAction(QIcon(os.path.join('icon', 'exit.jpg')), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip("Exit")
        exitAct.triggered.connect(qApp.quit)

        msg = 'Gallery' if self.home else 'Home'
        
        
           
        
        changePageAct = QAction(QIcon(os.path.join('icon', 'gallery.png')), msg, self)
        
        changePageAct.triggered.connect(self.goto)
        changePageAct.setStatusTip(msg)
        
        
        
        self.toolbar = self.addToolBar('tools')
        self.toolbar.setIconSize(QSize(22, 22))
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(plotGraph)
        self.toolbar.addAction(changePageAct)
        
        camera_toolbar = QToolBar("Camera")
        camera_toolbar.setIconSize(QSize(22, 22))
        self.addToolBar(camera_toolbar)

        photo_action = QAction(QIcon(os.path.join('icon', 'camera-black.png')), "Take photo...", self)
        photo_action.setStatusTip("Take photo of current view")
        #photo_action.triggered.connect(self.take_photo)
        photo_action.triggered.connect(MainWindow.capture_image)
        camera_toolbar.addAction(photo_action)

        change_folder_action = QAction(QIcon(os.path.join('icon', 'blue-folder-horizontal-open.png')), "Change save location...", self)
        change_folder_action.setStatusTip("Change folder where photos are saved.")
        change_folder_action.triggered.connect(self.change_folder)
        camera_toolbar.addAction(change_folder_action)

        camera_selector = QComboBox()
        camera_selector.addItems([c.description() for c in self.available_cameras])
        camera_selector.currentIndexChanged.connect( self.select_camera )

        camera_toolbar.addWidget(camera_selector)
    
    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda i, e, s: self.alert(s))
        self.capture.imageCaptured.connect(lambda d, i: self.statusmessage("Image %04d captured" % self.save_seq))

        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0
        
        

        
        
        
    
    def change_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Snapshot save location", "")
        if path:
            self.save_path = path
            self.save_seq = 0
            
    
 
    def alert(self, s):
        """
        Handle errors coming from QCamera dn QCameraImageCapture by displaying alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)
        
        
    def menubarUI(self):
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        
    def statusmessage(self,msg):
        self.statusBar().showMessage(msg)
        

        
        
    def resizeEvent(self, event):
    
        self.overlay.resize(event.size())
        event.accept()
        
    def take_photo(self):
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.save_path, "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )))
        self.save_seq += 1
        
        
    


            

    
    def closeEvent(self, event):
        #self
        print('test')



def make_label(master, x, y, h, w, *args, **kwargs):
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0) # don't shrink
    f.place(x=x, y=y)
    label = Label(f, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label


# In[ ]:



    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    

    # Now use a palette to switch to dark colors:
#     palette = QPalette()
#     palette.setColor(QPalette.Window, QColor(53, 53, 53))
#     palette.setColor(QPalette.WindowText, Qt.white)
#     palette.setColor(QPalette.Base, QColor(25, 25, 25))
#     palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
#     palette.setColor(QPalette.ToolTipBase, Qt.white)
#     palette.setColor(QPalette.ToolTipText, Qt.white)
#     palette.setColor(QPalette.Text, Qt.white)
#     palette.setColor(QPalette.Button, QColor(53, 53, 53))
#     palette.setColor(QPalette.ButtonText, Qt.white)
#     palette.setColor(QPalette.BrightText, Qt.red)
#     palette.setColor(QPalette.Link, QColor(42, 130, 218))
#     palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
#     palette.setColor(QPalette.HighlightedText, Qt.black)
#     app.setPalette(palette)
    
    
    mainWin = ARCWindow()
    mainWin.show()
    sys.exit( app.exec_() )














b'====================================\r\n'
b'T Ambience = 33.372 C\r\n'
b'1234.534\r\n'
b'1229.298\r\n'
b'vs = -5.236\r\n'
b'vs = -1.632, calibrate modify\r\n'
b'vs = -1.667, emissivity compensate\r\n'
b'to1 = 32.360\r\n'
b'to2 = 33.207\r\n'
b'T Object = 32.671 C\r\n'
b'T body = 32.557 C, ambience compensate\r\n'
b'T body = 36.196 C, weak low\r\n'
b'cfg.mode = 1\r\n'
