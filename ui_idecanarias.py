# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_idecanarias.ui'
#
# Created: Wed May 14 15:06:25 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_IDECanarias(object):
    def setupUi(self, IDECanarias):
        IDECanarias.setObjectName(_fromUtf8("IDECanarias"))
        IDECanarias.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(IDECanarias)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(IDECanarias)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), IDECanarias.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IDECanarias.reject)
        QtCore.QMetaObject.connectSlotsByName(IDECanarias)

    def retranslateUi(self, IDECanarias):
        IDECanarias.setWindowTitle(QtGui.QApplication.translate("IDECanarias", "IDECanarias", None, QtGui.QApplication.UnicodeUTF8))

