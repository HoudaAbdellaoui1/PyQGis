# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RequeteAttributaire
                                 A QGIS plugin
 geoinfo2
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-06-02
        git sha              : $Format:%H$
        copyright            : (C) 2021 by ABDELLAOUI_Houda
        email                : abdellaouihouda2@gmail.com
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
from PyQt5.QtWidgets import QFileDialog
from idna import unicode
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import (QgsProject,QgsVectorLayer)
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .RequeteAttributaire_dialog import RequeteAttributaireDialog
import os.path
import processing


class RequeteAttributaire:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RequeteAttributaire_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Requete_attributaire')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RequeteAttributaire', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/RequeteAttributaire/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Requete_attributaire'),
                action)
            self.iface.removeToolBarIcon(action)

    def layer_name(self, name: str):
        return QgsProject.instance().mapLayersByName(name)[0]

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ", "", '.txt')
        self.dlg.output.setText(str(filename))

    def close(self):
        self.dlg.close()

    def ok(self):
        Selectedlayer1 = self.dlg.comboBox_vector.currentText()
        Selectedlayer2 = self.dlg.comboBox_inters.currentText()

        a = processing.run("qgis:selectbylocation", {
            "INPUT": self.layer_name(Selectedlayer1),
            "PREDICATE": 0,
            "INTERSECT": self.layer_name(Selectedlayer2),
            "METHOD": 0
        })
        self.iface.actionZoomToSelected().trigger()
        print(a)

    # def test(self):
    #     print ("DID IT !")

    def getAttribute(self):
        self.dlg.comboBox_2.clear()
        selectedLayer = QgsProject.instance().mapLayersByName(self.dlg.comboBox.currentText())[0]
        fields = selectedLayer.fields()
        self.dlg.comboBox_2.addItem("")
        for field in fields:
            self.dlg.comboBox_2.addItem(field.name())

    def query(self):
        self.dlg.queryspace.setText(self.dlg.comboBox_2.currentText())

    def run_query(self):
        query=self.dlg.queryspace.text()
        layer = QgsProject.instance().mapLayersByName(self.dlg.comboBox.currentText())[0]
        print(query)
        result=layer.selectByExpression(query)
        self.iface.actionZoomToSelected().trigger()
        print(result)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = RequeteAttributaireDialog()
            #self.dlg.btn_run.clicked.connect(self.test)
            #layers = self.iface.legendInterface().layers()
            layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
            layer_list = []
            for layer in layers:
                layer_list.append(layer.name())
            self.dlg.comboBox.addItems(layer_list)

            layer_list = ["", ]
            layer_list2 = ["", ]
            for layer in layers:
                layer_list.append(layer.name())
            self.dlg.comboBox_vector.clear()
            self.dlg.comboBox_vector.addItems(layer_list)

            selectedLayerIndex = self.dlg.comboBox_vector.currentIndex()
            selectedLayer1 = layers[selectedLayerIndex]

            for layer in layers:
                if layer != selectedLayer1:
                    layer_list2.append(layer.name())
            self.dlg.comboBox_inters.clear()
            self.dlg.comboBox_inters.addItems(layer_list2)

            self.dlg.comboBox.setCurrentText("")
            self.dlg.comboBox.currentIndexChanged.connect(lambda : self.getAttribute())
            self.dlg.comboBox_2.currentIndexChanged.connect(lambda :self.query())
            self.dlg.btn_run.clicked.connect(lambda: self.run_query())
            self.dlg.browse_btn.clicked.connect(self.select_output_file)
            self.dlg.btn_run_2.clicked.connect(self.ok)
            self.dlg.buttonBox.clicked.connect(self.close)


        self.dlg.buttonBox.clicked.connect(lambda : self.dlg.close())
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            filename = self.dlg.output.text()
            output_file = open(filename, 'w')

            selectedLayerIndex = self.dlg.comboBox_vector.currentIndex()
            selectedLayer = layers[selectedLayerIndex]
            fields = selectedLayer.pendingFields()
            fieldnames = [field.name() for field in fields]

            for f in selectedLayer.getFeatures():
                line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                unicode_line = line.encode('utf-8')
                output_file.write(unicode_line)
            output_file.close()
            pass
