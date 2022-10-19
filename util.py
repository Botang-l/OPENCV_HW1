import cv2
import numpy as np
import copy
from util import *

class Camera_Calibration():
    def __init__(self):
        # the parameter generated after Camera Calibrate
        self.ret = []
        self.mtx = []
        self.dist = []
        self.rvecs = []
        self.tvecs = []
        self.data = []
        # 3D points are called object points and 2D image points are called image points.
        self.imgpoints = []
        self.objpoints = []
        # the chessboard size
        self.CHECKERBOARD = []
        # the inmage index can't find chess board corners
        self.findcornersfail = [] 
    
    def Find_para(self, data):
        '''self.signal1.emit()'''
        # Defining the dimensions of checkerboard
        self.CHECKERBOARD = (11,8)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.data = data


        # Defining the world coordinates for 3D points
        objp = np.zeros((1, self.CHECKERBOARD[0]*self.CHECKERBOARD[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:self.CHECKERBOARD[0], 0:self.CHECKERBOARD[1]].T.reshape(-1, 2)

        for idx, fname in enumerate(data):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(gray, self.CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
                cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
            
            if ret:  
                # refining pixel coordinates for given 2d points.
                corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                self.imgpoints.append(corners)  
                self.objpoints.append(objp)
                self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(
                    self.objpoints, self.imgpoints, gray.shape[::-1],None,None)
            else:
                self.findcornersfail.append(idx)
            
    
class Q1(Camera_Calibration):
    def Find_corner(self): 
        for idx,fname in enumerate(self.data):
            if (idx not in self.findcornersfail):
                img = cv2.imread(fname)
                img = cv2.drawChessboardCorners(img, self.CHECKERBOARD, self.imgpoints[idx],True)
                img = cv2.resize(img, (600, 500))
                result_name = 'board'+str(idx+1)+'.jpg'
                cv2.imshow(result_name, img)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
            

    def Find_intrinsic(self):
        print("Intrinsic Matrix : \n")
        print(self.mtx)

    def Find_extrinsic(self,number):
        userinput = int(number)
        if ((userinput in self.findcornersfail) or userinput == None):
            print("We can't find the extrinsic matrix in this picture")
        else:
            r = cv2.Rodrigues(self.rvecs[userinput])
            print(np.concatenate((r[0],self.tvecs[userinput]),axis =1))

    def Find_distortion(self):     
        print("Distortion : \n")
        print(self.dist)
    

    def Show_result(self):
        for idx, fname in enumerate(self.data):
            if (idx not in self.findcornersfail):
                img = cv2.imread(fname)
                dst = cv2.undistort(img, self.mtx, self.dist, None, self.mtx)
                dst = cv2.resize(dst, (500, 500)) 
                img = cv2.resize(img, (500, 500))
                combine_img=np.hstack([img,dst])
                result_name = 'board'+str(idx+1)+'.jpg'
                cv2.imshow(result_name,combine_img)
                cv2.waitKey(500)
                cv2.destroyAllWindows()

class Q2(Camera_Calibration):

    def draw(self, img ,imgpts):
        imgpts = np.float32(imgpts).reshape(-1, 2)
        imgpts = imgpts.astype(np.int)
        w = imgpts.shape[0]    
        for i in range(0,w,2):
            img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[i+1]), (0,0,250),20)
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

    def AR(self, msg, num):
        alphabet_set = []
        for idx, c in enumerate(msg):
            matrix = self.Get_Alphabet_and_shift(c, idx+1, num)
            alphabet_set = list(matrix) + alphabet_set
        
        alphabet_set = np.array(alphabet_set)   

        dim0 = alphabet_set.shape[0]
        dim1 = alphabet_set.shape[1]

        alphabet_set = np.reshape(alphabet_set,(dim0*dim1,3))
    
        for idx,fname in enumerate(self.data):
            img = cv2.imread(fname)
            if (idx not in self.findcornersfail):
                imgpts, _ = cv2.projectPoints(alphabet_set, self.rvecs[idx], self.tvecs[idx], np.array(self.mtx), np.array(self.dist))
                imgpts = np.reshape(imgpts,(dim0,dim1,2))
                img = self.draw(img, imgpts)
                img = cv2.resize(img, (500, 500))
                result_name = 'board'+str(idx+1)+'.jpg'
                
                cv2.imshow(result_name, img)
                cv2.waitKey(500)
                cv2.destroyAllWindows()


    def Show_on_board(self, word):
        #word = self.ui.lineEdit.toPlainText()
        self.AR(word, 0)


    def Show_vertically(self, word):
        #word = self.ui.lineEdit.toPlainText()
        self.AR(word, 1)


class Q3():
    def __init__(self):
        self.dataL = []
        self.dataR = []
        self.disparity = []
        self.imgL = []
        self.imgR = []

    def click(self, event, x, y, imgL, imgR):
        if event == cv2.EVENT_LBUTTONDOWN:
            #reset pic
            imgR = copy.deepcopy(self.imgR)
            #draw
            img = cv2.cvtColor(np.copy(self.disparity), cv2.COLOR_GRAY2BGR)
            img_dot = cv2.cvtColor(np.copy(self.disparity), cv2.COLOR_GRAY2BGR)
            cv2.circle(img_dot, (x,y), 25, (255,0,0), -1)

            print('Left image coordinate: (', x , '' , y, ')')
            z = img[y][x][0]
                
            if img[y][x][0] != 0:
                x1 = x - int(z % self.imgL.shape[1])
                y1 = y - int(z / self.imgL.shape[1]) 
                print(x1, y1)
                cv2.circle(imgR, (x1,y1), 25, (0,255,0), -1)
                
            cv2.namedWindow('imgR',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('imgR', int(imgR.shape[1]/4), int(imgR.shape[0]/4))
            cv2.imshow('imgR', imgR)           
            cv2.waitKey(0)

    def Get_Disparity_Map(self):

        # control windows size
        self.imgL = cv2.imread(self.dataL[0])
        self.imgR = cv2.imread(self.dataR[0])
        imgL_gray = cv2.imread(self.dataL[0], 0)
        imgR_gray = cv2.imread(self.dataR[0], 0)

        stereo = cv2.StereoBM_create(numDisparities=256, blockSize=25)
        self.disparity = stereo.compute(imgL_gray,imgR_gray)
        self.disparity = cv2.normalize(self.disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        # Stereo Disparity Map
        cv2.namedWindow('imgL',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('imgL', int(self.disparity.shape[1]/4), int(self.disparity.shape[0]/4))
        cv2.setMouseCallback('imgL', self.click)
        cv2.imshow('imgL', self.imgL)
          
        cv2.namedWindow('disparity',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('disparity', int(self.disparity.shape[1]/4), int(self.disparity.shape[0]/4))
        cv2.imshow('disparity', self.disparity)   

        cv2.waitKey(0)
        cv2.destroyAllWindows()