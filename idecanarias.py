# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IDECanarias
                                 A QGIS plugin
 Perform querys in local toponimia
                              -------------------
        begin                : 2014-05-14
        copyright            : (C) 2014 by Felix Jose Hernandez
        email                : fhernandeze@grafcan.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4 import QtCore
from PyQt4 import QtGui
# import resources_rc
import os.path

from idecanariasdock import IDECanariasDock


class IDECanarias:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QtCore.QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(
            self.plugin_dir, 'i18n', 'idecanarias_{}.qm'.format(locale)
        )
        if os.path.exists(localePath):
            self.translator = QtGui.QTranslator()
            self.translator.load(localePath)

            if QtCore.qVersion() > '4.3.3':
                QtCore.QCoreApplication.installTranslator(self.translator)

        # TODO: 140514, install dock
        self.dock = IDECanariasDock(self.iface)
        self.iface.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock)

    def initGui(self):
        pass

    def unload(self):
        pass

    def run(self):
        pass
