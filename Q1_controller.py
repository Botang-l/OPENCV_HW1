from asyncio.windows_events import NULL
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QThread, pyqtSignal
from Q1_UI import Ui_MainWindow
import cv2
from PIL import Image
import time
import numpy as np
import os
import glob
import threading
import copy

class Camera_Calibration():
    def __init__(self):
        self.ret = []
        self.mtx = []
        self.dist = []
        self.rvecs = []
        self.tvecs = []
        self.imgs = []
        #self.Find_para(data)  
    
    def Find_para(self, data):
        '''self.signal1.emit()'''
        # Defining the dimensions of checkerboard
        CHECKERBOARD = (11,8)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Creating vector to store vectors of 3D points for each checkerboard image
        objpoints = []
        # Creating vector to store vectors of 2D points for each checkerboard image
        imgpoints = [] 


        # Defining the world coordinates for 3D points
        objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

        
        for fname in data:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
                cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

            """
            If desired number of corner are detected,
            we refine the pixel coordinates and display 
            them on the images of checker board
            """
            if ret:
                objpoints.append(objp)
                # refining pixel coordinates for given 2d points.
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret)
            #height, width, channel = img.shape
                self.imgs.append(cv2.resize(img, (600, 500)))
            self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    
class Q1(Camera_Calibration):
    def Find_corner(self): 
        for idx,img in enumerate(self.imgs):
            result_name = 'board'+str(idx+1)+'.jpg'
            cv2.imshow(result_name, img)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            

    def Find_intrinsic(self):
        print("Intrinsic Matrix : \n")
        print(self.mtx)

    def Find_extrinsic(self,number):
        userinput = int(number)
        if(userinput == NULL):
            userinput = 0
        r = cv2.Rodrigues(self.rvecs[userinput])
        print(np.concatenate((r[0],self.tvecs[userinput]),axis =1))


    def Find_distortion(self):     
        print("Distortion : \n")
        print(self.dist)
    

    def Show_result(self):
        #------------------distorted
        for idx,img in enumerate(self.imgs):

            dst = cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
            dst = cv2.resize(dst, (500, 500)) 
            img = cv2.resize(img, (500, 500))
            combine_img=np.hstack([img,dst])
            result_name = 'board'+str(idx+1)+'.jpg'
            cv2.imshow(result_name,combine_img)
            cv2.waitKey(500)
            time.sleep(1)
            cv2.destroyAllWindows()

class Q2(Camera_Calibration):
    def __init__(self):
        super().__init__()
        self.data = []

    def draw(self, img ,imgpts):
        imgpts = np.float32(imgpts).reshape(-1, 2)
        imgpts = imgpts.astype(np.int)
        w = imgpts.shape[0]    
        for i in range(0,w,2):
            img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[i+1]), (0,0,125),200)
        return img

    def Get_Alphabet_and_shift(self, alphabet, ith, func_number):
        if(func_number==0):
            fs = cv2.FileStorage('Dataset_CvDl_Hw1/Q2_Image/Q2_lib/alphabet_lib_onboard.txt',cv2.FILE_STORAGE_READ)
        else:
            fs = cv2.FileStorage('Dataset_CvDl_Hw1/Q2_Image/Q2_lib/alphabet_lib_vertical.txt',cv2.FILE_STORAGE_READ)
            
        alphabet_matrix = fs.getNode('{}'.format(alphabet)).mat() # get the lines of 'K'
        alphabet_matrix = alphabet_matrix.astype(np.float32)
        
        # shift!
        # 1st (+7,+5), 2nd (+4,+5), 3rd (+1,+5)
        # 4th (+7,+2), 5th (+4,+2), 6th (+1,+2)
        if(ith<=3):
            y = 5
        else:
            y = 2
            
        if(ith%3 == 1):
            x = 7
        elif(ith%3 == 2):
            x = 4
        else:
            x = 1
            
        # x平移
        for i in range(alphabet_matrix.shape[0]):
            alphabet_matrix[i,0,0] += x
            alphabet_matrix[i,1,0] += x
        # y平移    
        for i in range(alphabet_matrix.shape[0]):
            alphabet_matrix[i,0,1] += y
            alphabet_matrix[i,1,1] += y
        
        return alphabet_matrix    

    def AR(self, data, msg, num):
        alphabet_set = []
        for idx, c in enumerate(msg):
            matrix = self.Get_Alphabet_and_shift(c, idx+1, num)
            alphabet_set = list(matrix) + alphabet_set
        
        alphabet_set = np.array(alphabet_set)   

        dim0 = alphabet_set.shape[0]
        dim1 = alphabet_set.shape[1]

        alphabet_set = np.reshape(alphabet_set,(dim0*dim1,3))
        print("1")
        print(np.array(self.imgs).shape)
        for idx,img in enumerate(self.data):
            print(idx)
            if self.ret:
                print(np.array(self.rvecs).reshape((-1,1)).shape, "   ", np.array(self.tvecs).shape)
                imgpts, _ = cv2.projectPoints(alphabet_set, self.rvecs[idx], self.tvecs[idx], np.array(self.mtx), np.array(self.dist))
                imgpts = np.reshape(imgpts,(dim0,dim1,2))
                img = self.draw(img, imgpts)

                result_name = 'board'+str(idx+1)+'.jpg'
                cv2.imshow(result_name, img)
                cv2.waitKey(500)
                time.sleep(1)
                cv2.destroyAllWindows()


    def Show_on_board(self, data):
        #word = self.ui.lineEdit.toPlainText()
        self.AR(data,"ABC", 0)


    def Show_vertically(self, data):
        #word = self.ui.lineEdit.toPlainText()
        self.AR(data,"ABC", 1)


class MainWindow_controller(QtWidgets.QMainWindow):
    
    '''signal1 = pyqtSignal() #clare'''

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        '''self.signal1.connect(q1)'''
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Q1 = Q1()
        self.Q2 = Q2() 
        self.Q3 = None
        self.Q1_data = None
        self.Q2_data = None
        self.Q3L_data = None   
        self.Q3R_data = None
        self.setup_control()

    def Using_find_extrinsic(self):
        section = int(self.ui.comboBox.currentText())-1
        self.Q1.Find_extrinsic(section)


    def setup_control(self):
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        #self.ui.pushButton.setText('Print message!')
        self.clicked_counter = 0
        self.ui.Load_Folder.clicked.connect(self.Load_Folder)
        
        self.ui.Load_Image_L.clicked.connect(self.Load_Image_L)
        self.ui.Load_Image_R.clicked.connect(self.Load_Image_R)
        #self.ui.StereoDisparityMap.clicked.connect(self.Q3.Stereo_Disparity_Map)

        self.ui.FindCorners.clicked.connect(self.Q1.Find_corner)
        self.ui.FindIntrinsic.clicked.connect(self.Q1.Find_intrinsic)
        self.ui.FindDistortion.clicked.connect(self.Q1.Find_distortion)
        self.ui.ShowResult.clicked.connect(self.Q1.Show_result)

        choices = [str(i) for i in range(1,16)]
        self.ui.comboBox.addItems(choices)
        self.ui.FindExtrinsic.clicked.connect(self.Using_find_extrinsic)
        self.ui.ShowWordsonBoard.clicked.connect(self.Q2.Show_on_board)
        self.ui.ShowWordsVertically.clicked.connect(self.Q2.Show_vertically)

    def Load_Folder(self):
        self.Q1_data = glob.glob('./Dataset_CvDl_Hw1/Q1_Image/*.bmp')
        #self.Q1.Find_para(self.Q1_data)
        self.Q2_data = glob.glob('./Dataset_CvDl_Hw1/Q2_Image/*.bmp')
        #self.Q2.Find_para(self.Q2_data)
        self.Q3L_data = glob.glob('./Dataset_CvDl_Hw1/Q3_Image/imL.png')
        self.Q3R_data = glob.glob('./Dataset_CvDl_Hw1/Q3_Image/imR.png')
        print('done')

    def Load_Image_L(self):
        self.Q3L_data = glob.glob('./Dataset_CvDl_Hw1/Q3_Image/imL.png')
        print('done')

    def Load_Image_R(self):
        self.Q3R_data = glob.glob('./Dataset_CvDl_Hw1/Q3_Image/imR.png')
        print('done')
    #@QtCore.pyqtSlot(int)
    #def on_value_changed(self, value):
    #    self.textEdit.append("Value: {}".format(value))
    
    
            

    