#-*- coding:utf-8
VERSION = 'v1'

import os
import sys
import maya

sys.path.append(r'../Qt.py/python')
from Qt import __binding__, QtGui, QtCore, QtWidgets
if __binding__ == 'PySide2':
    import pyside2uic as pysideuic
    from shiboken2 import wrapInstance
elif __binding__ == 'PySide':
    import pysideuic
    from shiboken import wrapInstance

import maya.OpenMayaUI as apiUI

def getMainWindow():
    pointer = apiUI.MQtUtil.mainWindow()
    if pointer is not None:
        _MainWindow = wrapInstance(long(pointer), QtWidgets.QWidget)
    return _MainWindow

#####################UI########################
class Main_Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)
        self.inint_widget()

    def selectFile(self, ftype):
        if self.sourcefname is not None and os.path.isfile(self.sourcefname):
            directory = self.sourcefname
        else:
            directory = QtCore.QDir.currentPath()
        dialog = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select fbx file', directory,  'fbx files (*fbx)')
        if dialog[0] != 0:
            if ftype == 'source':
                self.sourcefname = str(dialog[0])
                self.sourceflineEdit.setText(str(dialog[0]))
            else:
                self.targetfname = str(dialog[0])
                self.targetflineEdit.setText(str(dialog[0]))

    def run(self, sourceFile, targetFile):
        import merge
        reload(merge)
        print(sourceFile, targetFile)
        merge.main(sourceFile, targetFile)

    def inint_widget(self):
        QV_0_ayout   = QtWidgets.QVBoxLayout()
        QV_A_ayout   = QtWidgets.QHBoxLayout()       
        QV_B_ayout   = QtWidgets.QHBoxLayout()
        QV_C_ayout   = QtWidgets.QVBoxLayout()
        QV_D_ayout   = QtWidgets.QHBoxLayout()
        QV_E_ayout   = QtWidgets.QHBoxLayout()

        self.sourcefname = ''
        self.sourceflineEdit = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel('Source:       ')
        QV_A_ayout.addWidget(label)
        QV_A_ayout.addWidget(self.sourceflineEdit)
        sourceBrouseBtn = QtWidgets.QPushButton('...')
        QV_A_ayout.addWidget(sourceBrouseBtn)
        sourceBrouseBtn.clicked.connect(lambda: self.selectFile('source'))

        self.targetfname = ''
        self.targetflineEdit = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel('Target:       ')
        QV_B_ayout.addWidget(label)
        QV_B_ayout.addWidget(self.targetflineEdit)
        targetBrouseBtn = QtWidgets.QPushButton('...')
        QV_B_ayout.addWidget(targetBrouseBtn)
        targetBrouseBtn.clicked.connect(lambda: self.selectFile('target'))

        QV_0_ayout.addLayout(QV_D_ayout)
        QV_0_ayout.addLayout(QV_E_ayout)
        QV_0_ayout.addLayout(QV_A_ayout)
        QV_0_ayout.addLayout(QV_B_ayout)

        # self.seqListTextField = QtWidgets.QLineEdit()
        # self.seqListTextField.setFixedHeight(20)
        # self.seqListTextField.setPlaceholderText('Enter Seq Seperate With Comma')
        # self.seqListTextField.setToolTip('s026, s027')
        # self.seqListTextField.setObjectName('testLineEdit')

        button_layout = QtWidgets.QLabel(' ')
        runBtn = QtWidgets.QPushButton('Transfer')
        QV_C_ayout.addWidget(runBtn)
        runBtn.clicked.connect(lambda: self.run(self.sourcefname, self.targetfname))
        # shotgun_button = QtWidgets.QPushButton('OPEN_SHOTGUN')
        # QV_C_ayout.addWidget(self.seqListTextField)
        # QV_C_ayout.addWidget(shotgun_button)
        # shotgun_button.setStyleSheet("background-color: orange")
        
        QVlayout = QtWidgets.QVBoxLayout()    
        QVlayout.addLayout(QV_0_ayout)
        QVlayout.addLayout(QV_C_ayout)

        w = QtWidgets.QWidget()
        w.setLayout(QVlayout)
        self.setCentralWidget(w)
        self.setWindowTitle('Animation Retarget Tool')

########################################################

def run():
    global main_window
    try:
        main_window.close()
    except:
        pass
    maya_main_wid = getMainWindow()
    main_window = Main_Window(parent = maya_main_wid)
    main_window.show()
    main_window.setMinimumSize(600,250)
    main_window.setMaximumSize(600,250)

if __name__ == '__main__':
    run()
