# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_idecanariasdock.ui'
#
# Created: Mon Mar 13 10:22:15 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_IDECanariasDock(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setGeometry(QtCore.QRect(0, 0, 494, 367))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setFloating(True)
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab001 = QtGui.QWidget()
        self.tab001.setMinimumSize(QtCore.QSize(472, 0))
        self.tab001.setObjectName(_fromUtf8("tab001"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab001)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtSearch = QtGui.QLineEdit(self.tab001)
        self.txtSearch.setObjectName(_fromUtf8("txtSearch"))
        self.verticalLayout.addWidget(self.txtSearch)
        self.chkBBOX = QtGui.QCheckBox(self.tab001)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkBBOX.sizePolicy().hasHeightForWidth())
        self.chkBBOX.setSizePolicy(sizePolicy)
        self.chkBBOX.setObjectName(_fromUtf8("chkBBOX"))
        self.verticalLayout.addWidget(self.chkBBOX)
        self.tblResult = QtGui.QTableWidget(self.tab001)
        self.tblResult.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblResult.sizePolicy().hasHeightForWidth())
        self.tblResult.setSizePolicy(sizePolicy)
        self.tblResult.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblResult.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblResult.setShowGrid(True)
        self.tblResult.setColumnCount(3)
        self.tblResult.setObjectName(_fromUtf8("tblResult"))
        self.tblResult.setRowCount(0)
        self.verticalLayout.addWidget(self.tblResult)
        self.lblResult = QtGui.QLabel(self.tab001)
        self.lblResult.setObjectName(_fromUtf8("lblResult"))
        self.verticalLayout.addWidget(self.lblResult)
        self.tabWidget.addTab(self.tab001, _fromUtf8(""))
        self.tab002 = QtGui.QWidget()
        self.tab002.setObjectName(_fromUtf8("tab002"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab002)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_7 = QtGui.QGroupBox(self.tab002)
        self.groupBox_7.setEnabled(True)
        self.groupBox_7.setTitle(_fromUtf8(""))
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.layoutWidget_2 = QtGui.QWidget(self.groupBox_7)
        self.layoutWidget_2.setGeometry(QtCore.QRect(0, 0, 226, 50))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.radioutm = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioutm.setObjectName(_fromUtf8("radioutm"))
        self.gridLayout_3.addWidget(self.radioutm, 1, 0, 1, 1)
        self.radiodms = QtGui.QRadioButton(self.layoutWidget_2)
        self.radiodms.setChecked(True)
        self.radiodms.setObjectName(_fromUtf8("radiodms"))
        self.gridLayout_3.addWidget(self.radiodms, 0, 0, 1, 1)
        self.radiodm = QtGui.QRadioButton(self.layoutWidget_2)
        self.radiodm.setObjectName(_fromUtf8("radiodm"))
        self.gridLayout_3.addWidget(self.radiodm, 0, 1, 1, 1)
        self.radiod = QtGui.QRadioButton(self.layoutWidget_2)
        self.radiod.setObjectName(_fromUtf8("radiod"))
        self.gridLayout_3.addWidget(self.radiod, 1, 1, 1, 1)
        self.layoutWidget = QtGui.QWidget(self.groupBox_7)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 55, 301, 127))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.txtCoordinates = QtGui.QLineEdit(self.layoutWidget)
        self.txtCoordinates.setObjectName(_fromUtf8("txtCoordinates"))
        self.gridLayout_2.addWidget(self.txtCoordinates, 0, 0, 1, 1)
        self.btnGet = QtGui.QPushButton(self.layoutWidget)
        self.btnGet.setObjectName(_fromUtf8("btnGet"))
        self.gridLayout_2.addWidget(self.btnGet, 3, 0, 1, 1)
        self.btnClipboard = QtGui.QPushButton(self.layoutWidget)
        self.btnClipboard.setObjectName(_fromUtf8("btnClipboard"))
        self.gridLayout_2.addWidget(self.btnClipboard, 2, 0, 1, 1)
        self.btnGo = QtGui.QPushButton(self.layoutWidget)
        self.btnGo.setObjectName(_fromUtf8("btnGo"))
        self.gridLayout_2.addWidget(self.btnGo, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_7)
        self.tabWidget.addTab(self.tab002, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        Dialog.setWidget(self.dockWidgetContents)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("IDECanariasDock", "Búsquedas IDECanarias", None))
        self.chkBBOX.setText(_translate("IDECanariasDock", "Limitar la búsqueda a la extensión actual", None))
        self.lblResult.setText(_translate("IDECanariasDock", "Encontrado (s)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab001), _translate("IDECanariasDock", "Lugar", None))
        self.radioutm.setText(_translate("IDECanariasDock", "UTM", None))
        self.radiodms.setText(_translate("IDECanariasDock", "Grad. Min. Seg.", None))
        self.radiodm.setText(_translate("IDECanariasDock", "Grad. Min.", None))
        self.radiod.setText(_translate("IDECanariasDock", "Grados", None))
        self.btnGet.setText(_translate("IDECanariasDock", "Empezar captura", None))
        self.btnClipboard.setText(_translate("IDECanariasDock", "Copiar al portapapeles", None))
        self.btnGo.setText(_translate("IDECanariasDock", "Ir", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab002), _translate("IDECanariasDock", "Coordenadas", None))

