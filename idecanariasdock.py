# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name : IDECANARIAS Search
Description          : Perform querys in toponimia
Date                 : 15/May/14
copyright            : (C) 2014 by Felix J. Hdez
email                : fhernandeze@grafcan.es
 ***************************************************************************/

Revision:
 - 170313: syntax pep8 and try make
 - 170313: connect to local database, file .database

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

http://qgis.org/pyqgis-cookbook/plugins.html

"""
import os
import sys
import traceback
# import base64
import re
import psycopg2
# import pprint
# import tempfile
import math

from datetime import datetime

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtXml
# from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QHttp

from qgis.core import *
# import qgis.utils

from ui_idecanariasdock import Ui_IDECanariasDock

from utils import *


class IDECanariasDock(QtGui.QDockWidget):
    """
    """

    def __init__(self, iface):
        """
        """
        self.iface = iface
        self.canvas = iface.mapCanvas()
        QtGui.QDialog.__init__(self)

        # Set up the user interface from Designer.
        self.ui = Ui_IDECanariasDock()
        self.ui.setupUi(self)
        self.http = QHttp()
        self.httpogr = QHttp()
        self.url = QUrl()
        self._radio = 0
        self._point = None
        self._pointutm = None
        self.i = None
        self.conn_string = ""

        self.layer = None
        self.layerid = ''

        self.chkRemote = False
        self.chkBBOX = False

        self.tblResultHeader = [u'Nombre', u'Clasificación', u'Localización']

        self.ui.tblResult.setHorizontalHeaderLabels(self.tblResultHeader)

        self.connect(
            self.ui.txtSearch,
            SIGNAL("returnPressed(void)"),
            self.onClick_btnSearch
        )
        self.connect(
            self.ui.tblResult,
            SIGNAL("cellDoubleClicked(int,int)"),
            self.onDblClick_tblResult
        )
        """self.connect(
            self.ui.chkRemote,
            SIGNAL("clicked()"),
            self.onClick_chkRemote
        )"""
        self.connect(
            self.http,
            QtCore.SIGNAL("done(bool)"),
            self.onDone_http
        )
        self.connect(
            self.httpogr,
            QtCore.SIGNAL("done(bool)"),
            self.onDone_httpogr
        )
        self.connect(
            self.ui.radiodms,
            SIGNAL("toggled(bool)"),
            self.__setRadiodms
        )
        self.connect(
            self.ui.radiodm,
            SIGNAL("toggled(bool)"),
            self.__setRadiodm
        )
        self.connect(
            self.ui.radiod,
            SIGNAL("toggled(bool)"),
            self.__setRadiod
        )
        self.connect(
            self.ui.radioutm,
            SIGNAL("toggled(bool)"),
            self.__setRadioutm
        )
        self.connect(
            self.ui.btnGet,
            SIGNAL("clicked()"),
            self.onClick_btnGet
        )
        self.connect(
            self.ui.btnGo,
            SIGNAL("clicked()"),
            self.onClick_btnGo
        )
        self.connect(
            self.ui.txtCoordinates,
            SIGNAL("returnPressed(void)"),
            self.onClick_btnGo
        )
        self.connect(
            self.ui.btnClipboard,
            SIGNAL("clicked()"),
            self.onClick_btnClipboard
        )

        baseDirectory = os.path.dirname(__file__)

        def fillPath(x):
            return os.path.join(baseDirectory, x)

        databasePath, filenamelog = map(
            fillPath, ['.database', 'idecanarias.log']
        )

        # Log file
        self.DEBUG = True
        self.filenamelog = filenamelog
        self.Log("init app")

        try:
            databaseName, databaseUser, databasePassword, databaseHost = open(
                databasePath).read().splitlines()
            self.conn_string = (
                "host='%s' dbname='%s' user='%s' password='%s'" % (
                    databaseHost, databaseName, databaseUser, databasePassword
                )
            )
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            self.Log(str(exceptionTraceback))
            self.chkRemote = True

    def Log(self, msg):
        """
        """
        if self.DEBUG:
            f = open(self.filenamelog, "a")
            f.write("%s: %s\n" % (datetime.now(), msg.encode('utf-8')))
            f.close()

    def alert(self, msg):
        """
        """
        QtGui.QMessageBox.warning(self, u'Búsquedas IDECANARIAS', msg)

    def __setRadiodms(self, checked):
        """
        """
        if checked:
            self._radio = 0
        self.reverse_action(None)

    def __setRadiodm(self, checked):
        """
        """
        if checked:
            self._radio = 1
        self.reverse_action(None)

    def __setRadiod(self, checked):
        """
        """
        if checked:
            self._radio = 2
        self.reverse_action(None)

    def __setRadioutm(self, checked):
        """
        """
        if checked:
            self._radio = 3
        self.reverse_action(None)

    def onClick_btnLoad(self):
        """
        """
        _pointutm = None
        data = ""

        # check num items selected
        rows = self.ui.tblResult.selectionModel().selectedRows()
        rowscount = len(rows)

        if rowscount == 0:
            QMessageBox.warning(
                self, "Aviso", 'Debe seleccionar algún elemento'
            )
            return False

        if rowscount == 1:
            self.onDblClick_tblResult(rows[0].row(), 0)
            return False

        # for idx in self.ui.tblResult.selectedItems():
        for idx in rows:
            _pointutm = pointFromWGS84(
                QgsPoint(self.lid[idx.row()][6], self.lid[idx.row()][7])
            )
            fid = """<ms:capa fid="%d">
                <ms:Nombre>%s</ms:Nombre>
                <ms:Clasificacion>%s</ms:Clasificacion>
                <ms:Localizacion>%s</ms:Localizacion>
                <ms:msGeometry><gml:Point srsName="EPSG:32628">
                    <gml:coordinates>%f,%f</gml:coordinates></gml:Point>
                </ms:msGeometry>
            </ms:capa>""" % (
                int(idx.row()) + 1,
                self.lid[idx.row()][3],
                self.lid[idx.row()][2],
                self.lid[idx.row()][1],
                _pointutm[0],
                _pointutm[1]
            )
            data += fid

        # FILE
        filename = os.path.join(str(QtCore.QDir.tempPath()), "XXXXXX.gml")
        file = QtCore.QTemporaryFile(filename)
        file.setAutoRemove(False)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            self.alert(
                self.tr("No puedo escribir en %1:\n%2.").arg(
                    filename
                ).arg(file.errorString())
            )
            return False

        # id = 1
        # nombre = "test"
        bbox = ""
        gml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<wfs:FeatureCollection'
            ' xmlns:ms="http://mapserver.gis.umn.edu/mapserver"'
            ' xmlns:wfs="http://www.opengis.net/wfs"'
            ' xmlns:gml="http://www.opengis.net/gml"'
            ' xmlns:ogc="http://www.opengis.net/ogc"'
            ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            ' xsi:schemaLocation="http://www.opengis.net/wfs '
            ' http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">'
            '<gml:boundedBy>'
            '<gml:Box srsName="EPSG:32628">'
            '    <gml:coordinates>%s</gml:coordinates>'
            '</gml:Box>'
            '</gml:boundedBy>'
            '<gml:featureMember>%s</gml:featureMember>'
            '</wfs:FeatureCollection>'
        ) % (bbox, data)
        outstr = QtCore.QTextStream(file)
        outstr.setCodec("UTF-8")
        outstr << gml
        filename = str(file.fileName())
        file.close()

        texto = self.ui.txtSearch.text()
        if not texto:
            texto = "consulta"

        # basename = os.path.basename(filename)
        self.iface.addVectorLayer(filename, "%s" % (texto), 'ogr')
        src = self.canvas.layers()[0].srs()
        dest = self.canvas.mapRenderer().destinationSrs()
        coodTrans = QgsCoordinateTransform(src, dest)
        extent = self.canvas.layers()[0].extent()
        newextent = coodTrans.transform(extent)
        self.canvas.setExtent(newextent)
        self.canvas.refresh()

    def onClick_chkRemote(self):
        """
        """
        self.ui.tblResult.clear()
        self.ui.tblResult.setRowCount(0)
        self.ui.tblResult.setHorizontalHeaderLabels(self.tblResultHeader)

    def onClick_btnClipboard(self):
        """
        """
        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(self.ui.txtCoordinates.text())

    def onClick_btnGet(self):
        """
        """
        ct = ClickTool(self.iface, self.reverse_action)
        self.iface.mapCanvas().setMapTool(ct)

    def onClick_btnGo(self):
        """
        develop er to parse this:
        28º 07' 9.7249'' S, 15º 25' 30.9814'' O
        28º 07.16208' S, 15º 25.51637' O
        28.11936800, -15.42527283
        458232.06, 3110498.55

        Algorithm
        lat = 45 + (25 / 60) + (2.98 / 3600)
        lng = 10 + (11 / 60) + (30.29 / 3600)
        """

        lat = None
        lng = None
        x = None
        y = None

        texto = self.ui.txtCoordinates.text().encode('utf-8')
        if not texto:
            texto = "28º 07' 9.7249'' N, 15º 25' 30.9814'' O"
            texto = "28º 07' 9.7248'' N, 15º 25' 30.9822'' O"

        patterndms = (
            r"^([\d]{1,3})\º ([\d]{1,3})\'"
            r" ([\d]{1,3}(\.\d+)?)\'\'"
            r" ([NS]),\s*([\d]{1,3})\º ([\d]{1,3})\'"
            r" ([\d]{1,3}(\.\d+)?)\'\' ([EO])$"
        )
        m = re.match(patterndms, texto, re.UNICODE)
        if m:
            lat = int(m.group(1)) + \
                (float(m.group(2)) / 60) + \
                (float(m.group(3)) / 3600)
            lng = int(m.group(6)) + \
                (float(m.group(7)) / 60) + \
                (float(m.group(8)) / 3600)
            if m.group(5) == "S":
                lat = -lat
            if m.group(10) == "O":
                lng = -lng
            self.ui.radiodms.setChecked(True)

        patterndm = (
            r"^([\d]{1,3})\º ([\d]{1,3}(\.\d+)?)\'"
            r" ([NS]),\s*([\d]{1,3})\º ([\d]{1,3}(\.\d+)?)\' ([EO])$"
        )
        m = re.match(patterndm, texto, re.UNICODE)
        if m:
            lat = int(m.group(1)) + (float(m.group(2)) / 60)
            lng = int(m.group(5)) + (float(m.group(6)) / 60)
            if m.group(4) == "S":
                lat = -lat
            if m.group(8) == "O":
                lng = -lng
            self.ui.radiodm.setChecked(True)

        patterndm = r"^(\-?[\d]{1,3}(\.\d+)?),\s*(\-?[\d]{1,3}(\.\d+)?)$"
        m = re.match(patterndm, texto, re.UNICODE)
        if m:
            lat = float(m.group(1))
            lng = float(m.group(3))
            self.ui.radiod.setChecked(True)

        # convert to UTM
        self.Log("%s, %s (%s)" % (lat, lng, type(texto)))

        if lat and lng:
            point = QgsPoint(lng, lat)
            self._point = point
            self._pointutm = pointFromWGS84(point)
            x = self._pointutm[0]
            y = self._pointutm[1]

        m = re.match(r"^(\d+(\.\d+)?),\s*(\d+(\.\d+)?)$", texto)
        if m:
            x = float(m.group(1))
            y = float(m.group(3))
            self._pointutm = QgsPoint(x, y)
            self._point = pointToWGS84(self._pointutm)
            self.ui.radioutm.setChecked(True)

        if x and y:

            # create layer
            if not QgsMapLayerRegistry.instance().mapLayer(self.layerid):
                self.layer = QgsVectorLayer(
                    "Point", u'Resultados de conversión', "memory"
                )
                self.provider = self.layer.dataProvider()
                self.layer.setCrs(get_dest_projection())

                # add fields
                self.provider.addAttributes([
                    QgsField("nombre", QtCore.QVariant.String),
                    QgsField("x", QtCore.QVariant.Double),
                    QgsField("y", QtCore.QVariant.Double),
                ])

                # Makes fields visible
                self.layer.updateFields()

                # Labels on
                label = self.layer.label()
                label.setLabelField(QgsLabel.Text, 0)
                self.layer.enableLabels(True)

                # add layer if not already
                QgsMapLayerRegistry.instance().addMapLayer(self.layer)

                # store layer id
                self.layerid = QgsMapLayerRegistry.instance(
                ).mapLayers().keys()[-1]
                self.canvas.refresh()

            text = ""
            text, ok = QtGui.QInputDialog.getText(
                self, u'IDECanarias', u'Introduzca una descripción:'
            )

            # add a feature
            fields = self.layer.pendingFields()
            fet = QgsFeature(fields)
            fet.setGeometry(QgsGeometry.fromPoint(self._pointutm))
            fet[0] = text
            fet[1] = self._pointutm[0]
            fet[2] = self._pointutm[1]
            self.provider.addFeatures([fet])

            # update layer's extent when new features have been added
            # because change of extent in provider is not
            # propagated to the layer
            self.layer.updateExtents()

            # Get current extent
            scale = 1
            extent = self.canvas.extent()
            width = extent.width() * scale
            height = extent.height() * scale

            # Recenter
            rect = QgsRectangle(
                x - width / 2.0,
                y - height / 2.0,
                x + width / 2.0,
                y + height / 2.0
            )

            # Set the extent to our new rectangle
            self.canvas.setExtent(rect)

            # Refresh the map
            self.canvas.refresh()
        else:
            self.alert("Coordenadas incorrectas")

    def reverse_action(self, point):
        """
        """
        if point and (point != self._pointutm):
            self._pointutm = point

        if self._pointutm is None:
            return

        pt = pointToWGS84(self._pointutm)
        self._point = pt

        latitude = pt[1]    # 28....
        longitude = pt[0]   # -16....

        # Convert to deg, min, secs
        latitude_sign = 0
        if latitude < 0:
            latitude_sign = -1

        longitude_sign = 0
        if longitude < 0:
            longitude_sign = -1

        latitude_deg = math.floor(math.fabs(latitude))
        latitude_min = math.floor((math.fabs(latitude) - latitude_deg) * 60)
        latitude_min_ = (math.fabs(latitude) - latitude_deg) * 60
        latitude_sec = (
            (math.fabs(latitude) - latitude_deg) * 60 - latitude_min
        ) * 60

        latitude_dir = "S"
        if latitude_sign == 0:
            latitude_dir = "N"

        longitude_deg = math.floor(math.fabs(longitude))
        longitude_min = math.floor((math.fabs(longitude) - longitude_deg) * 60)
        longitude_min_ = (math.fabs(longitude) - longitude_deg) * 60
        longitude_sec = (
            (math.fabs(longitude) - longitude_deg) * 60 - longitude_min
        ) * 60

        longitude_dir = "O"
        if longitude_sign == 0:
            longitude_dir = "E"

        data = ""
        if self._radio == 0:
            data = (
                u"%02.0fº %02.0f\'"
                u" %06.4f\'\' %s, %02.0fº %02.0f\' %06.4f\'\' %s"
            ) % (
                latitude_deg, latitude_min, latitude_sec, latitude_dir,
                longitude_deg, longitude_min, longitude_sec, longitude_dir
            )
        elif self._radio == 1:
            data = (
                u"%02.0fº %08.5f\' %s, %02.0fº %08.5f\' %s"
            ) % (
                latitude_deg, latitude_min_, latitude_dir,
                longitude_deg, longitude_min_, longitude_dir
            )
        elif self._radio == 2:
            data = u"%.8f, %.8f" % (latitude, longitude)
        elif self._radio == 3:
            data = u"%s, %s" % (
                '{0:.2f}'.format(self._pointutm[0]),
                '{0:.2f}'.format(self._pointutm[1])
            )
        else:
            data = ""
        self.ui.txtCoordinates.setText(data)

    def onClick_btnSearch(self):
        """
        TODO: 121203, limit bbox search
        /busquedas/toponimoxmlbbox/1/10/151186.2703860851,2928780.363515307,682750.3992649722,3334856.301118972/0/0/?texto=chineguas
        """
        texto = self.ui.txtSearch.text()
        if not texto:
            texto = "grafcan"

        if self.chkRemote:
            self.http.setHost('visor.grafcan.es', 80)
            if not self.ui.chkBBOX.isChecked():
                url = QUrl('/busquedas/toponimoxml/1/50/?texto=%s' % texto)
            else:
                self.Log("retrive bbox")
                _bbox = None
                _bbox = self.canvas.extent()
                bbox = [
                    _bbox.xMinimum(), _bbox.yMinimum(),
                    _bbox.xMaximum(), _bbox.yMaximum()
                ]
                url = QUrl(
                    (
                        '/busquedas/toponimoxmlbbox'
                        '/1/10/%s,%s,%s,%s/0/0/?texto=%s'
                    ) % (
                        bbox[0], bbox[1], bbox[2], bbox[3],
                        texto
                    )
                )
            path = url.toEncoded()
            self.http.get(str(path))
        else:
            try:
                conn = psycopg2.connect(self.conn_string)
                conn.set_client_encoding('LATIN1')
                cursor = conn.cursor()
                if not self.ui.chkBBOX.isChecked():
                    sql = (
                        "select id, nombre, clasificacion,"
                        " localizacion from grafcan.gettoponimo('%s', 1, 50)"
                    ) % texto
                else:
                    _bbox = None
                    _bbox = self.canvas.extent()
                    bbox = [
                        _bbox.xMinimum(), _bbox.yMinimum(),
                        _bbox.xMaximum(), _bbox.yMaximum()
                    ]
                    sql = (
                        "select id, nombre, clasificacion,"
                        " localizacion from grafcan.gettoponimo"
                        "('%s', 1, 50, %f, %f, %f, %f, true,"
                        "'30,39,160,10,11,12,13,15,16,17,18,40,50,"
                        "14,19,20,21,31,32,33,34,35,36,37,38,151,"
                        "152,153,154,191')"
                    ) % (
                        texto,
                        float(bbox[0]), float(bbox[1]),
                        float(bbox[2]), float(bbox[3])
                    )
                cursor.execute(sql)
                self.ui.lblResult.setText(
                    (
                        u"%d lugar(es) encontrados"
                        u"(Haz doble click para ver su localización)"
                    ) % cursor.rowcount
                )
                self.lid = []
                lidd = []
                self.ui.tblResult.clear()
                self.ui.tblResult.setRowCount(0)
                self.ui.tblResult.setHorizontalHeaderLabels(
                    self.tblResultHeader
                )
                for record in cursor.fetchall():
                    lidd.append("%s - %s [%s]" % (
                        record[3], record[2], record[1])
                    )
                    self.lid.append(record)
                    row = self.ui.tblResult.rowCount()
                    self.ui.tblResult.insertRow(row)
                    item001 = QtGui.QTableWidgetItem(record[1])
                    item002 = QtGui.QTableWidgetItem(record[2])
                    item003 = QtGui.QTableWidgetItem(record[3])
                    self.ui.tblResult.setItem(row, 0, item001)
                    self.ui.tblResult.setItem(row, 1, item002)
                    self.ui.tblResult.setItem(row, 2, item003)
                self.ui.tblResult.resizeColumnsToContents()
                cursor.close()
            except:
                exceptionValue = sys.exc_info()[1]
                self.alert(
                    u"Database connection failed!\n -> %s" % exceptionValue
                )

    def onDblClick_tblResult(self, i, j):
        """
        """
        if self.chkRemote:
            id = self.lid[i][0]
            self.i = i
            self.httpogr.setHost('visor.grafcan.es', 80)
            self.httpogr.get(
                '/busquedas/toponimiagml/1/50/qgis/1/%d/' % int(id)
            )
        else:
            id = self.lid[i][0]
            localizacion = self.lid[i][3]
            clasificacion = self.lid[i][2]
            nombre = self.lid[i][1]
            fngml = "grafcan.gettoponimo_gml"
            try:
                conn = psycopg2.connect(self.conn_string)
                conn.set_client_encoding('LATIN1')

                # GEOM
                cursor = conn.cursor()
                sql = "select * from %s(%d)" % (fngml, id)
                cursor.execute(sql)
                row = cursor.fetchone()
                gml = ""
                if row[0]:
                    geometria = row[0]
                cursor.close()

                # FILE
                filename = os.path.join(
                    str(QtCore.QDir.tempPath()), "XXXXXX.gml"
                )
                file = QtCore.QTemporaryFile(filename)
                file.setAutoRemove(False)
                if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
                    self.alert(
                        u"No puedo escribir en %s:\n%s." % (
                            filename, file.errorString()
                        )
                    )
                    return False

                bbox = ""
                gml = (
                    '<?xml version="1.0" encoding="UTF-8"?>'
                    '<wfs:FeatureCollection'
                    ' xmlns:ms="http://mapserver.gis.umn.edu/mapserver"'
                    ' xmlns:wfs="http://www.opengis.net/wfs"'
                    ' xmlns:gml="http://www.opengis.net/gml"'
                    ' xmlns:ogc="http://www.opengis.net/ogc"'
                    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
                    ' xsi:schemaLocation="http://www.opengis.net/wfs'
                    ' http://schemas.opengis.net/wfs/1.0.0/WFS-basic.xsd">'
                    '<gml:boundedBy>'
                    '<gml:Box srsName="EPSG:32628">'
                    '<gml:coordinates>%s</gml:coordinates>'
                    '</gml:Box>'
                    '</gml:boundedBy>'
                    '<gml:featureMember>'
                    '<ms:capa fid="1">'
                    '<ms:Nombre>%s</ms:Nombre>'
                    '<ms:Clasificacion>%s</ms:Clasificacion>'
                    '<ms:Localizacion>%s</ms:Localizacion>'
                    '<ms:msGeometry>%s</ms:msGeometry>'
                    '</ms:capa>'
                    '</gml:featureMember>'
                    '</wfs:FeatureCollection>'
                ) % (
                    bbox, nombre, clasificacion, localizacion, geometria
                )

                outstr = QtCore.QTextStream(file)
                outstr.setCodec("UTF-8")
                outstr << gml
                filename = str(file.fileName())
                file.close()

                layerid = self.iface.addVectorLayer(
                    filename, "%s_%s" % (nombre, id), 'ogr'
                )
                src = layerid.crs()
                dest = self.canvas.mapRenderer().destinationCrs()
                coodTrans = QgsCoordinateTransform(src, dest)
                # extent = self.canvas.layers()[0].extent()
                extent = layerid.extent()
                newextent = coodTrans.transform(extent)
                self.canvas.setExtent(newextent)
                self.canvas.refresh()

            except:
                self.Log(traceback.print_exc())
                self.alert(traceback.print_exc())

    def onDone_httpogr(self, error):
        """
        """
        filename = os.path.join(str(QtCore.QDir.tempPath()), "XXXXXX.gml")
        file = QtCore.QTemporaryFile(filename)
        file.setAutoRemove(False)

        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            self.alert(
                u"No puedo escribir en %1:\n%2." % (
                    filename, file.errorString()
                )
            )
            return False

        self.Log("Save")
        outstr = QtCore.QTextStream(file)
        outstr.setCodec("UTF-8")
        all = str(self.httpogr.readAll()).decode('utf-8')
        outstr << all
        filename = str(file.fileName())
        file.close()
        # basename = os.path.basename(filename)

        id = None
        nombre = None
        if self.i is not None:
            id = self.lid[self.i][0]
            nombre = self.lid[self.i][3]

            # show in qgis
            # basename = os.path.basename(filename)
            layerid = self.iface.addVectorLayer(
                filename, "%s_%s" % (nombre, id), 'ogr'
            )
            # src = QgsCoordinateReferenceSystem()
            # src.createFromSrid(32628)
            # src = self.canvas.layers()[0].crs()
            src = layerid.crs()
            dest = self.canvas.mapRenderer().destinationCrs()
            coodTrans = QgsCoordinateTransform(src, dest)
            # extent = self.canvas.layers()[0].extent()
            extent = layerid.extent()
            newextent = coodTrans.transform(extent)
            self.canvas.setExtent(newextent)
            self.canvas.refresh()

    def onDone_http(self, error):
        """
        """
        doc = QtXml.QDomDocument("IDE")
        response = str(self.http.readAll())
        doc.setContent(response)
        id = nombre = clasificacion = localizacion = None

        self.ui.tblResult.clear()
        self.ui.tblResult.setRowCount(0)
        self.ui.tblResult.setHorizontalHeaderLabels(self.tblResultHeader)

        self.lid = []
        lidd = []
        root = doc.documentElement()
        node = root.firstChild()
        while (not node.isNull()):
            if(node.toElement().tagName() == "row"):
                child = node.firstChild()
                while (not child.isNull()):
                    if(child.toElement().tagName() == "id"):
                        try:
                            child2 = child.firstChild()
                            id = child2.toText().data()
                            # lidd.append(e["id"])
                        except:
                            QMessageBox.warning(
                                self,
                                "Error",
                                "Could not parse xml file. Problem %s." % (
                                    child2.toElement().tagName()
                                )
                            )
                    elif (child.toElement().tagName() == "nombre"):
                        try:
                            child2 = child.firstChild()
                            nombre = child2.toText().data()
                            # lidd.append(e["nombre"])
                        except:
                            QMessageBox.warning(
                                self,
                                "Error",
                                "Could not parse xml file. Problem %s." % (
                                    child2.toElement().tagName()
                                )
                            )
                    elif (child.toElement().tagName() == "clasificacion"):
                        try:
                            child2 = child.firstChild()
                            clasificacion = child2.toText().data()
                        except:
                            QMessageBox.warning(
                                self,
                                "Error",
                                "Could not parse xml file. Problem %s." % (
                                    child2.toElement().tagName()
                                )
                            )
                    elif (child.toElement().tagName() == "localizacion"):
                        try:
                            child2 = child.firstChild()
                            localizacion = child2.toText().data()
                        except:
                            QMessageBox.warning(
                                self,
                                "Error",
                                "Could not parse xml file. Problem %s." % (
                                    child2.toElement().tagName()
                                )
                            )
                    elif (child.toElement().tagName() == "x"):
                        try:
                            child2 = child.firstChild()
                            x = child2.toText().data()
                        except:
                            QMessageBox.warning(
                                self,
                                "Error",
                                "Could not parse xml file. Problem %s." % (
                                    child2.toElement().tagName()
                                )
                            )
                    elif (child.toElement().tagName() == "y"):
                        try:
                            child2 = child.firstChild()
                            y = child2.toText().data()
                        except:
                            QMessageBox.warning(
                                self,
                                "Error",
                                "Could not parse xml file. Problem %s." % (
                                    child2.toElement().tagName()
                                )
                            )
                    child = child.nextSibling()
                e = (
                    id,
                    localizacion,
                    clasificacion,
                    nombre,
                    nombre,
                    0.0, x[0], y[0]
                )
                lidd.append(
                    "%s - %s [%s]" % (clasificacion, localizacion, nombre)
                )

            self.lid.append(e)
            row = self.ui.tblResult.rowCount()
            self.ui.tblResult.insertRow(row)
            item001 = QtGui.QTableWidgetItem(nombre)
            item002 = QtGui.QTableWidgetItem(clasificacion)
            item003 = QtGui.QTableWidgetItem(localizacion)
            self.ui.tblResult.setItem(row, 0, item001)
            self.ui.tblResult.setItem(row, 1, item002)
            self.ui.tblResult.setItem(row, 2, item003)
            node = node.nextSibling()

        self.ui.lblResult.setText(
            (
                u'%d lugar(es) encontrados '
                u'(Haz doble click para ver su localización)'
            ) % len(self.lid)
        )

        self.ui.tblResult.resizeColumnsToContents()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = IDECanariasDock()
    app.addDockWidget(dialog)
    dialog.show()
    sys.exit(app.exec_())
