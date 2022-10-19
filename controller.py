#from asyncio.windows_events import NULL
from PyQt5 import QtWidgets
from UI import Ui_MainWindow
import glob
from util import *

class MainWindow_controller(QtWidgets.QMainWindow):
    
    '''signal1 = pyqtSignal() #clare'''
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        '''self.signal1.connect(q1)'''
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Q1 = Q1()
        self.Q2 = Q2() 
        self.Q3 = Q3()
        
        self.setup_control()

    def Using_find_extrinsic(self):
        section = int(self.ui.comboBox.currentText())-1
        self.Q1.Find_extrinsic(section)

    def ShowWordsonBoard_get_word(self):
        word = self.ui.lineEdit.toPlainText()
        self.Q2.Show_on_board(word)

    def ShowWordsVertically_get_word(self):
        word = self.ui.lineEdit.toPlainText()
        self.Q2.Show_vertically(word)

    def setup_control(self):
        # qpushbutton doc: https://doc.qt.io/qt-5/qpushbutton.html
        #self.ui.pushButton.setText('Print message!')
        self.clicked_counter = 0
        self.ui.Load_Folder.clicked.connect(self.Load_Folder)
        
        self.ui.Load_Image_L.clicked.connect(self.Load_Image_L)
        self.ui.Load_Image_R.clicked.connect(self.Load_Image_R)
        self.ui.StereoDisparityMap.clicked.connect(self.Q3.Get_Disparity_Map)

        self.ui.FindCorners.clicked.connect(self.Q1.Find_corner)
        self.ui.FindIntrinsic.clicked.connect(self.Q1.Find_intrinsic)
        self.ui.FindDistortion.clicked.connect(self.Q1.Find_distortion)
        self.ui.ShowResult.clicked.connect(self.Q1.Show_result)

        choices = [str(i) for i in range(1,16)]
        self.ui.comboBox.addItems(choices)
        self.ui.FindExtrinsic.clicked.connect(self.Using_find_extrinsic)
        self.ui.ShowWordsonBoard.clicked.connect(self.ShowWordsonBoard_get_word)
        self.ui.ShowWordsVertically.clicked.connect(self.ShowWordsVertically_get_word)

    def Load_Folder(self):
        Q1_data = glob.glob('./Dataset_CvDl_Hw1/Q1_Image/*.bmp')
        self.Q1.Find_para(Q1_data)
        Q2_data = glob.glob('./Dataset_CvDl_Hw1/Q2_Image/*.bmp')
        self.Q2.Find_para(Q2_data)
        
        print('done')

    def Load_Image_L(self):
        self.Q3.dataL = glob.glob('./Dataset_CvDl_Hw1/Q3_Image/imL.png')
        print('done')

    def Load_Image_R(self):
        self.Q3.dataR = glob.glob('./Dataset_CvDl_Hw1/Q3_Image/imR.png')
        print('done')
    
    
            

    