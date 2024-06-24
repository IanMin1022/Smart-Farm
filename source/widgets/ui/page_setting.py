# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgets/ui/page_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1920, 860)
        Form.setStyleSheet("QWidget#Form\n"
"{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.settings_area = QtWidgets.QLabel(Form)
        self.settings_area.setGeometry(QtCore.QRect(40, 40, 910, 800))
        self.settings_area.setStyleSheet("border-radius : 30px;\n"
"border: 3px solid rgb(0, 135, 68);\n"
"")
        self.settings_area.setText("")
        self.settings_area.setObjectName("settings_area")
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(13)
        self.set_freq_label = QtWidgets.QLabel(Form)
        self.set_freq_label.setGeometry(QtCore.QRect(120, 150, 481, 50))
        self.set_freq_label.setStyleSheet("font: 75 35pt \"나눔스퀘어 Bold\";\n"
"color: rgb(0, 135, 68);")
        self.set_freq_label.setObjectName("set_freq_label")
        self.set_freq_spin = QtWidgets.QDoubleSpinBox(Form)
        self.set_freq_spin.setGeometry(QtCore.QRect(120, 230, 465, 80))
        self.set_freq_spin.setStyleSheet("""
                QDoubleSpinBox {
                font: 75 30pt '나눔스퀘어 Bold';
                padding-right: 0px; /* space for the buttons */
                border: 2px solid rgb(128, 128, 128); /* boundary box */
                border-radius: 5px; /* rounded corners */
                padding-left: 30px; /* move text 10px to the right */
                }
                QDoubleSpinBox::up-button {
                width: 50px; /* width of the up button */
                height: 40px; /* height of the up button */
                subcontrol-position: top right; /* position the up button */
                }
                QDoubleSpinBox::down-button {
                width: 50px; /* width of the down button */
                height: 40px; /* height of the down button */
                subcontrol-position: bottom right; /* position the down button */
                }
                QDoubleSpinBox::up-arrow {
                width: 15px; /* width of the up arrow */
                height: 15px; /* height of the up arrow */
                }
                QDoubleSpinBox::down-arrow {
                width: 15px; /* width of the down arrow */
                height: 15px; /* height of the down arrow */
        }
        """
        )
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(30)
        self.set_freq_spin.setFont(font)
        self.set_freq_spin.setDecimals(0)
        self.set_freq_spin.setMinimum(1.0)
        self.set_freq_spin.setMaximum(100.0)
        self.set_freq_spin.setSingleStep(1.0)
        self.set_freq_spin.setProperty("value", 5.0)
        self.set_freq_spin.setObjectName("set_freq_spin")
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(13)
        self.save_label = QtWidgets.QLabel(Form)
        self.save_label.setGeometry(QtCore.QRect(90, 340, 481, 60))
        self.save_label.setStyleSheet("font: 75 35pt \"나눔스퀘어 Bold\";\n"
"color: rgb(0, 135, 68);")
        self.save_label.setObjectName("save_label")
        font = QtGui.QFont()
        font.setFamily("나눔스퀘어")
        font.setPointSize(30)
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(120, 425, 281, 80))
        self.save_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.save_button.setStyleSheet("QPushButton:hover\n"
"{ \n"
"    background-color: rgb(0, 135, 68);\n"
"    border-radius: 15px;\n"
"    font: 75 35pt \"Arial\";\n"
"    color: white;  \n"
"}\n"
"\n"
"QPushButton\n"
"{ \n"
"    border-radius: 15px;\n"
"    border: 4px solid rgb(0, 135, 68);\n"
"    font: 75 35pt \"나눔스퀘어 Bold\";\n"
"    color: rgb(0, 135, 68);\n"
"}\n"
"")
        self.save_button.setObjectName("save_button")
        self.activate_box = QtWidgets.QCheckBox(Form)
        self.activate_box.setGeometry(QtCore.QRect(440, 434, 455, 60))
        self.activate_box.setStyleSheet("QCheckBox::indicator { width: 35; height: 35; }")
        self.activate_box.setObjectName("activate_box")
        self.activate_label = QtWidgets.QLabel(Form)
        self.activate_label.setGeometry(QtCore.QRect(503, 438, 420, 50))
        self.activate_label.setStyleSheet("font: 75 30pt \"나눔스퀘어 Bold\";\n"
"color: rgb(0, 135, 68);")
        self.activate_label.setObjectName("activate_label")
        self.connection_area = QtWidgets.QLabel(Form)
        self.connection_area.setGeometry(QtCore.QRect(970, 40, 910, 800))
        self.connection_area.setStyleSheet("border-radius : 30px;\n"
"border: 3px solid rgb(0, 135, 68);\n"
"")
        self.connection_area.setText("")
        self.connection_area.setObjectName("connection_area")
        self.port_label = QtWidgets.QLabel(Form)
        self.port_label.setGeometry(QtCore.QRect(1062, 140, 700, 60))
        self.port_label.setStyleSheet("font: 75 35pt \"나눔스퀘어 Bold\";\n"
"color: rgb(0, 135, 68);")
        self.port_label.setObjectName("port_label")
        self.comment_label = QtWidgets.QLabel(Form)
        self.comment_label.setGeometry(QtCore.QRect(1070, 215, 655, 50))
        self.comment_label.setStyleSheet("font: 75 30pt \"나눔스퀘어\";\n"
"color: rgb(50, 50, 50);")
        self.comment_label.setObjectName("comment_label")
        self.port_combo = QtWidgets.QComboBox(Form)
        self.port_combo.setGeometry(QtCore.QRect(1070, 293, 455, 80))
        self.port_combo.setStyleSheet("""
                QComboBox {
                font: 30pt '나눔스퀘어';
                border: 2px solid rgb(128, 128, 128); /* boundary box */
                border-radius: 5px; /* rounded corners */
                padding-left: 20px; /* move text 10px to the right */
                padding-bottom: 7px; /* move text 7px to the top */
                }
                QComboBox::drop-down {
                width: 40px; /* width of the drop-down button */
                height: 77px; /* height of the drop-down button */
                }
                QComboBox::down-arrow {
                width: 20px; /* width of the down arrow */
                height: 20px; /* height of the down arrow */
                }
        """
        )
        self.port_combo.setEditable(True)
        self.port_combo.setCurrentText("")
        self.port_combo.setObjectName("port_combo")
        self.refresh_button = QtWidgets.QPushButton(Form)
        self.refresh_button.setGeometry(QtCore.QRect(1540, 300, 155, 60))
        self.refresh_button.setStyleSheet("QPushButton\n"
"{ \n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border: 0px solid;\n"
"    font: 75 30pt \"나눔스퀘어\";\n"
"    color: gray;  \n"
"}\n"
"\n"
"QPushButton:hover\n"
"{ \n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border: 0px solid;\n"
"    color: rgb(0, 135, 68);\n"
"}\n"
"")
        self.refresh_button.setObjectName("refresh_button")
        self.conn_button = QtWidgets.QPushButton(Form)
        self.conn_button.setGeometry(QtCore.QRect(1080, 412, 281, 80))
        self.conn_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.conn_button.setStyleSheet("QPushButton:hover\n"
"{ \n"
"    background-color: rgb(0, 135, 68);\n"
"    border-radius: 15px;\n"
"    font: 75 35pt \"Arial\";\n"
"    color: white;  \n"
"}\n"
"\n"
"QPushButton\n"
"{ \n"
"    border-radius: 15px;\n"
"    border: 4px solid rgb(0, 135, 68);\n"
"    font: 75 35pt \"나눔스퀘어 Bold\";\n"
"    color: rgb(0, 135, 68);\n"
"}\n"
"")
        self.conn_button.setObjectName("conn_button")
        self.connection_label = QtWidgets.QLabel(Form)
        self.connection_label.setGeometry(QtCore.QRect(1010, 60, 291, 60))
        self.connection_label.setStyleSheet("font: 75 40pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(0, 135, 68);")
        self.connection_label.setObjectName("connection_label")
        self.settings_label = QtWidgets.QLabel(Form)
        self.settings_label.setGeometry(QtCore.QRect(90, 60, 291, 70))
        self.settings_label.setStyleSheet("font: 75 40pt \"나눔스퀘어 ExtraBold\";\n"
"color: rgb(0, 135, 68);")
        self.settings_label.setObjectName("settings_label")
        
        self.connection_area.raise_()
        self.settings_area.raise_()
        self.set_freq_label.raise_()
        self.set_freq_spin.raise_()
        self.save_label.raise_()
        self.save_button.raise_()
        self.activate_box.raise_()
        self.activate_label.raise_()
        self.port_combo.raise_()
        self.port_label.raise_()
        self.conn_button.raise_()
        self.connection_label.raise_()
        self.comment_label.raise_()
        self.settings_label.raise_()
        self.refresh_button.raise_()

        self.retranslateUi(Form)
        self.port_combo.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.set_freq_label.setText(_translate("Form", "Update period(s)"))
        self.save_label.setText(_translate("Form", "Save Settings"))
        self.save_button.setText(_translate("Form", "Save"))
        self.activate_label.setText(_translate("Form", "Activate saved settings"))
        self.port_label.setText(_translate("Form", "Waiting..."))
        self.conn_button.setText(_translate("Form", "Connect"))
        self.connection_label.setText(_translate("Form", "Connection"))
        self.comment_label.setText(_translate("Form", "You can also type the port name"))
        self.settings_label.setText(_translate("Form", "Settings"))
        self.refresh_button.setText(_translate("Form", "Refresh"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
