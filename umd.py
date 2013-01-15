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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

import umddialog
import aboutdialog

import resources_rc

class UmdPlugin:
  def __init__(self, iface):
    self.iface = iface

    try:
      self.QgisVersion = unicode(QGis.QGIS_VERSION_INT)
    except:
      self.QgisVersion = unicode(QGis.qgisVersion)[ 0 ]

    # For i18n support
    userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/umd"
    systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/umd"

    overrideLocale = QSettings().value("locale/overrideFlag", QVariant(False)).toBool()
    if not overrideLocale:
      localeFullName = QLocale.system().name()
    else:
      localeFullName = QSettings().value("locale/userLocale", QVariant("")).toString()

    if QFileInfo(userPluginPath).exists():
      translationPath = userPluginPath + "/i18n/umd_" + localeFullName + ".qm"
    else:
      translationPath = systemPluginPath + "/i18n/umd_" + localeFullName + ".qm"

    self.localePath = translationPath
    if QFileInfo(self.localePath).exists():
      self.translator = QTranslator()
      self.translator.load(self.localePath)
      QCoreApplication.installTranslator(self.translator)

  def initGui(self):
    if int(self.QgisVersion) < 10900:
      qgisVersion = str(self.QgisVersion[ 0 ]) + "." + str(self.QgisVersion[ 2 ]) + "." + str(self.QgisVersion[ 3 ])
      QMessageBox.warning(self.iface.mainWindow(),
                           QCoreApplication.translate("UMD", "Error"),
                           QCoreApplication.translate("UMD", "Quantum GIS %1 detected.\n").arg(qgisVersion) +
                           QCoreApplication.translate("UMD", "This version of UMD requires at least QGIS version 1.9.0. Plugin will not be enabled."))
      return None

    self.actionRun = QAction(QCoreApplication.translate("UMD", "UMD"), self.iface.mainWindow())
    self.actionRun.setIcon(QIcon(":/icons/umd.png"))
    self.actionRun.setWhatsThis("Classification for UMD")
    self.actionAbout = QAction(QCoreApplication.translate("UMD", "About UMD..."), self.iface.mainWindow())
    self.actionAbout.setIcon(QIcon(":/icons/about.png"))
    self.actionAbout.setWhatsThis("About UMD")

    self.iface.addPluginToMenu(QCoreApplication.translate("UMD", "UMD"), self.actionRun)
    self.iface.addPluginToMenu(QCoreApplication.translate("UMD", "UMD"), self.actionAbout)
    self.iface.addToolBarIcon(self.actionRun)

    self.actionRun.triggered.connect(self.run)
    self.actionAbout.triggered.connect(self.about)

  def unload(self):
    self.iface.unregisterMainWindowAction(self.actionRun)

    self.iface.removeToolBarIcon(self.actionRun)
    self.iface.removePluginMenu(QCoreApplication.translate("UMD", "UMD"), self.actionRun)
    self.iface.removePluginMenu(QCoreApplication.translate("UMD", "UMD"), self.actionAbout)

  def run(self):
    d = umddialog.UmdDialog(self.iface)
    d.show()
    d.exec_()

  def about(self):
    d = aboutdialog.AboutDialog()
    d.exec_()
