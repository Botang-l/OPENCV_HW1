# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cvdl.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow): 
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1016, 430)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Load_Image = QtWidgets.QGroupBox(self.centralwidget)
        self.Load_Image.setGeometry(QtCore.QRect(20, 20, 221, 351))
        self.Load_Image.setObjectName("Load_Image")
        self.Load_Folder = QtWidgets.QPushButton(self.Load_Image)
        self.Load_Folder.setGeometry(QtCore.QRect(60, 70, 93, 28))
        self.Load_Folder.setObjectName("Load_Folder")
        self.Load_Image_L = QtWidgets.QPushButton(self.Load_Image)
        self.Load_Image_L.setGeometry(QtCore.QRect(60, 150, 93, 28))
        self.Load_Image_L.setObjectName("Load_Image_L")
        self.Load_Image_R = QtWidgets.QPushButton(self.Load_Image)
        self.Load_Image_R.setGeometry(QtCore.QRect(60, 230, 93, 28))
        self.Load_Image_R.setObjectName("Load_Image_R")
        self.Calibration = QtWidgets.QGroupBox(self.centralwidget)
        self.Calibration.setGeometry(QtCore.QRect(270, 20, 221, 351))
        self.Calibration.setObjectName("Calibration")

        self.Find_Extrinsic = QtWidgets.QGroupBox(self.Calibration)
        self.Find_Extrinsic.setGeometry(QtCore.QRect(0, 140, 221, 91))
        self.Find_Extrinsic.setObjectName("Find_Extrinsic")
        self.FindExtrinsic = QtWidgets.QPushButton(self.Find_Extrinsic)
        self.FindExtrinsic.setGeometry(QtCore.QRect(50, 50, 121, 31))
        self.FindExtrinsic.setObjectName("FindExtrinsic")

        self.comboBox = QtWidgets.QComboBox(self.Find_Extrinsic)
        self.comboBox.setGeometry(QtCore.QRect(70, 20, 81, 21))
        self.comboBox.setObjectName("comboBox")
        self.ShowResult = QtWidgets.QPushButton(self.Calibration)
        self.ShowResult.setGeometry(QtCore.QRect(50, 300, 121, 31))


        self.ShowResult.setObjectName("ShowResult")
        self.FindCorners = QtWidgets.QPushButton(self.Calibration)
        self.FindCorners.setGeometry(QtCore.QRect(50, 40, 121, 31))
        self.FindCorners.setObjectName("FindCorners")
        self.FindIntrinsic = QtWidgets.QPushButton(self.Calibration)
        self.FindIntrinsic.setGeometry(QtCore.QRect(50, 90, 121, 31))
        self.FindIntrinsic.setObjectName("FindIntrinsic")
        self.FindDistortion = QtWidgets.QPushButton(self.Calibration)
        self.FindDistortion.setGeometry(QtCore.QRect(50, 250, 121, 31))
        self.FindDistortion.setObjectName("FindDistortion")
        self.Stereo_Disparity_Map = QtWidgets.QGroupBox(self.centralwidget)
        self.Stereo_Disparity_Map.setGeometry(QtCore.QRect(770, 20, 221, 351))
        self.Stereo_Disparity_Map.setObjectName("Stereo_Disparity_Map")
        self.StereoDisparityMap = QtWidgets.QPushButton(self.Stereo_Disparity_Map)
        self.StereoDisparityMap.setGeometry(QtCore.QRect(30, 150, 161, 31))
        self.StereoDisparityMap.setObjectName("StereoDisparityMap")
        self.AugmentedReality = QtWidgets.QGroupBox(self.centralwidget)
        self.AugmentedReality.setGeometry(QtCore.QRect(520, 20, 221, 351))
        self.AugmentedReality.setObjectName("AugmentedReality")
        self.ShowWordsVertically = QtWidgets.QPushButton(self.AugmentedReality)
        self.ShowWordsVertically.setGeometry(QtCore.QRect(30, 210, 161, 31))
        self.ShowWordsVertically.setObjectName("ShowWordsVertically")
        self.lineEdit = QtWidgets.QTextEdit(self.AugmentedReality)
        self.lineEdit.setGeometry(QtCore.QRect(20, 60, 181, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.ShowWordsonBoard = QtWidgets.QPushButton(self.AugmentedReality)
        self.ShowWordsonBoard.setGeometry(QtCore.QRect(30, 150, 161, 31))
        self.ShowWordsonBoard.setObjectName("ShowWordsonBoard")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1016, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Load_Image.setTitle(_translate("MainWindow", "Load Image"))
        self.Load_Folder.setText(_translate("MainWindow", "Load Folder"))
        self.Load_Image_L.setText(_translate("MainWindow", "Load Image_L"))
        self.Load_Image_R.setText(_translate("MainWindow", "Load Image_R"))
        self.Calibration.setTitle(_translate("MainWindow", "1.Calibration"))
        self.Find_Extrinsic.setTitle(_translate("MainWindow", "1.3Find Extrinsic"))
        self.FindExtrinsic.setText(_translate("MainWindow", "1.3 Find Extrinsic"))
        self.ShowResult.setText(_translate("MainWindow", "1.5 ShowResult"))
        self.FindCorners.setText(_translate("MainWindow", "1.1 Find Corners"))
        self.FindIntrinsic.setText(_translate("MainWindow", "1.2 Find Intrinsic"))
        self.FindDistortion.setText(_translate("MainWindow", "1.4 Find Distortion"))
        self.Stereo_Disparity_Map.setTitle(_translate("MainWindow", "3.Stereo Disparity Map"))
        self.StereoDisparityMap.setText(_translate("MainWindow", "3.1 Stereo Disparity Map"))
        self.AugmentedReality.setTitle(_translate("MainWindow", "2.Augmented Reality "))
        self.ShowWordsVertically.setText(_translate("MainWindow", "2.2 ShowWords Vertically"))
        self.ShowWordsonBoard.setText(_translate("MainWindow", "2.1 ShowWords on Board"))

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
