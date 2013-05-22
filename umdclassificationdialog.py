# -*- coding: utf-8 -*-

#******************************************************************************
#
# UMD
# ---------------------------------------------------------
# Classification for UMD
#
# Copyright (C) 2013 NextGIS (info@nextgis.org)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

import os
import ConfigParser

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from qgis.core import *

import rasterizethread

from ui_umdclassificationdialogbase import Ui_Dialog

class UmdClassificationDialog(QDialog, Ui_Dialog):
  def __init__(self, plugin, metrics, dirs):
    QDialog.__init__(self)
    self.setupUi(self)

    self.plugin = plugin
    self.iface = plugin.iface
    self.metrics = metrics
    self.usedDirs = dirs

    self.btnOk = self.buttonBox.button(QDialogButtonBox.Ok)
    self.btnClose = self.buttonBox.button(QDialogButtonBox.Close)

    self.workThread = None

    self.manageGui()

  def manageGui(self):
    pass

  def reject(self):
    QDialog.reject(self)

  def accept(self):
    self.workThread = rasterizethread.RasterizeThread(self.metrics,
                                                      self.usedDirs,
                                                      "mask.tif"
                                                     )

    self.workThread.rangeChanged.connect(self.setProgressRange)
    self.workThread.updateProgress.connect(self.updateProgress)
    self.workThread.processFinished.connect(self.processFinished)
    self.workThread.processInterrupted.connect(self.processInterrupted)

    self.btnOk.setEnabled(False)
    self.btnClose.setText(self.tr("Cancel"))
    self.buttonBox.rejected.disconnect(self.reject)
    self.btnClose.clicked.connect(self.stopProcessing)

    self.workThread.start()

  def setProgressRange(self, maxValue):
    self.progressBar.setRange(0, maxValue)

  def updateProgress(self):
    self.progressBar.setValue(self.progressBar.value() + 1)

  def processFinished(self):
    self.stopProcessing()
    self.restoreGui()

    #~ if self.chkAddToCanvas.isChecked():
      #~ newLayer = QgsRasterLayer(self.outputFileName, QFileInfo(self.outputFileName).baseName())
#~
      #~ if newLayer.isValid():
        #~ QgsMapLayerRegistry.instance().addMapLayers([newLayer])
      #~ else:
        #~ QMessageBox.warning(self,
                            #~ self.tr("Can't open file"),
                            #~ self.tr("Error loading output VRT-file:\n%1").arg(unicode(self.outputFileName))
                           #~ )

  def processInterrupted( self ):
    self.restoreGui()

  def stopProcessing( self ):
    if self.workThread != None:
      self.workThread.stop()
      self.workThread = None

  def restoreGui(self):
    self.progressBar.setFormat("%p%")
    self.progressBar.setRange(0, 1)
    self.progressBar.setValue(0)

    self.buttonBox.rejected.connect(self.reject)
    self.btnClose.clicked.disconnect(self.stopProcessing)
    self.btnClose.setText(self.tr("Close"))
    self.btnOk.setEnabled(True)