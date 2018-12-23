# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\11mb.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import binascii

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(383, 424)
        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(300, 20, 71, 31))
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 100, 181, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 271, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 60, 271, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.toolButton_2 = QtWidgets.QToolButton(Dialog)
        self.toolButton_2.setGeometry(QtCore.QRect(300, 60, 71, 31))
        self.toolButton_2.setObjectName("toolButton_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(220, 110, 131, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 370, 121, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 180, 331, 181))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "BIOS Validation e-BAT  Author: Joy"))
        self.toolButton.setText(_translate("Dialog", "Load IWFI"))
        self.radioButton.setText(_translate("Dialog", "16 MB"))
        self.radioButton_2.setText(_translate("Dialog", "32 MB"))
        self.toolButton_2.setText(_translate("Dialog", "Output"))
        self.pushButton.setText(_translate("Dialog", "FIT BIOS TO 11MB"))
        self.pushButton_2.setText(_translate("Dialog", "Clear Log"))

    def pushbutton(self):
        self.toolButton.clicked.connect(self.open_iwfi)
        self.toolButton_2.clicked.connect(self.output_dir)
        self.pushButton.clicked.connect(self.patch)
        self.pushButton_2.clicked.connect(self.clear_log)


    def open_iwfi(self):
        # Open IWFI
        title = "IWFI File"
        path = ""
        file_type = "IWFI files (*.bin)"
        fname = QFileDialog.getOpenFileName(None, title, path, file_type)
        self.lineEdit.setText(str(fname[0]))
        global iwfi_path
        iwfi_path = str(fname[0])

        # File Name
        global iwfi_name
        # Print File name
        iwfi_name = os.path.splitext(iwfi_path)[0]
        iwfi_name = os.path.basename(iwfi_name)
        self.textBrowser.append("============== IWFI Name =================")
        self.textBrowser.append("IWFI name: "+iwfi_name)

        # Get BIOS region begin offset address from IFWI BIN file offset 0x44 0x45.
        if iwfi_path == "":
          self.textBrowser.append("No input do nothing")

        else:

           with open(iwfi_path, 'rb') as ifwi_fileobj:
             ifwi_file = ifwi_fileobj.read()

           low_byte = ifwi_file[0x44]
           high_byte = ifwi_file[0x45]
           # ------------------ TEST -------------------------
           #self.textBrowser.append("Get BIOS region begin offset address from IFWI BIN file offset 0x44 0x45.")
           #self.textBrowser.append("offset 0x44: "+hex(low_byte))
           #self.textBrowser.append("offset 0x45: " + hex(high_byte))
           # ------------------ TEST END-------------------------
           bios_begin = (high_byte << 8) | low_byte
           bios_begin = bios_begin << 0x0C
           self.textBrowser.append("============== IWFI Information =================")
           self.textBrowser.append("BIOS Address from : "+hex(bios_begin))

           # Get BIOS region end offset address from IFWI BIN file offset 0x46 0x47.
           low_byte = ifwi_file[0x46]
           high_byte = ifwi_file[0x47]
           # ------------------ TEST -------------------------
           #self.textBrowser.append("Get BIOS region end offset address from IFWI BIN file offset 0x46 0x47")
           #self.textBrowser.append("offset 0x46: "+hex(low_byte))
           #self.textBrowser.append("offset 0x47: "+hex(high_byte))
           # ------------------ TEST END-------------------------

           bios_end = (high_byte << 8) | low_byte
           bios_end = (bios_end << 0x0C) | 0xFFF
           self.textBrowser.append("BIOS End Address : "+hex(bios_end))


           bios_len = bios_end - bios_begin + 1
           self.textBrowser.append("BIOS Length : "+hex(bios_len))
           self.textBrowser.append("IWFI Length : " + str(len(ifwi_file)))
           ifwi_size = len(ifwi_file)
           if ifwi_size == 16777216:
               print("yes")
               self.radioButton.setChecked(True)
               self.radioButton.toggled.connect(lambda: self.rd1)

    def output_dir(self):
        global output_dir

        title = "Output Folder"
        path = "Y:/"
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(None,
                                                     title,
                                                     path, options=options)

        self.lineEdit_2.setText(str(directory))

        output_dir = str(directory)
        if str(directory) == "":
            self.textBrowser.append("Output folder no input")
        else:
            self.textBrowser.append("============== Output Folder =================")
            self.textBrowser.append("Output folder Path :")
            self.textBrowser.append(output_dir)

    def clear_log(self):
        self.textBrowser.setPlainText("")



    def patch(self):

        # Used IWFI Name create output folder
        default_path = output_dir + "/" + iwfi_name + "_11MB"
        os.mkdir(default_path)
        print(default_path)

        # Read IFWI
        with open(iwfi_path, 'rb') as ifwi_fileobj:
            ifwi_file = ifwi_fileobj.read()

         # Get BIOS region begin offset address from IFWI BIN file offset 0x44 0x45.
        low_byte = ifwi_file[0x44]
        self.textBrowser.append(hex(low_byte))
        high_byte = ifwi_file[0x45]
        bios_begin = (high_byte << 8) | low_byte
        bios_begin = bios_begin << 0x0C

        # Get BIOS region end offset address from IFWI BIN file offset 0x46 0x47.
        low_byte = ifwi_file[0x46]
        high_byte = ifwi_file[0x47]
        bios_end = (high_byte << 8) | low_byte
        bios_end = (bios_end << 0x0C) | 0xFFF
        bios_len = bios_end - bios_begin + 1

        combined_file = bytearray(len(ifwi_file))
        if self.radioButton.isChecked():

            # FSP Path
            self.textBrowser.append("======= Start FIT 16MB IFWI to 11MB BIOS  ========")
            self.textBrowser.append("=== Start FIT 16MB IFWI to 11MB BIOS  ===")
            self.textBrowser.append("Start override offset 0x44 to 0x0")
            self.textBrowser.append("Start override offset 0x44 to 0x16")
            combined_file[0x44] = 0x0
            combined_file[0x45] = 0x16

            for index in range(bios_end):
                if index == 0x44:
                    continue
                elif index == 0x45:
                    continue
                combined_file[index] = ifwi_file[index]


        with open(default_path + "/" + iwfi_name + "_patched_11MB.bin", 'wb') as combined_fileobj:

            combined_fileobj.write(combined_file)
        self.textBrowser.append("All process complete")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    ui.pushbutton()
    MainWindow.show()
    sys.exit(app.exec_())