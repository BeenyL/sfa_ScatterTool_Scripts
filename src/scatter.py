import maya.OpenMayaUI as omui
import maya.cmds as cmds
import random
from PySide2 import QtWidgets, QtGui, QtCore
from shiboken2 import wrapInstance



def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter UI")
        self.setMinimumWidth(600)
        self.setMaximumWidth(800)
        self.setMinimumHeight(200)
        self.setMaximumHeight(400)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)

        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: Bold 20px")
        self.create_obj_lay = self.create_obj_layout_ui()
        self.sel_cnl_lay = self.sel_cnl_layout_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.create_obj_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.sel_cnl_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.cancel_btn.clicked.connect(self.cancel)
        self.shape_btn.clicked.connect(self.createShape)

    @QtCore.Slot()
    def createShape(self):
        if self.shape_cmb.currentText() == "Cube":
            cmds.polyCube(name="Cube")
        if self.shape_cmb.currentText() == "Sphere":
            cmds.polySphere(name="Sphere")
        if self.shape_cmb.currentText() == "Cylinder":
            cmds.polyCylinder(name="Cylinder")
        if self.shape_cmb.currentText() == "Cone":
            cmds.polyCone(name="Cone")

    @QtCore.Slot()
    def selectObject(self):
        """Select an Object"""
        cmds.select(self.shape_cmb.currentText())

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()

    def create_obj_layout_ui(self):
        self.shape_cmb = QtWidgets.QComboBox()
        self.shape_cmb.setFixedWidth(100)
        self.shape_cmb.addItems(['Cube', 'Sphere', 'Cylinder', 'Cone'])
        self.shape_btn = QtWidgets.QPushButton("Create Shape")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.shape_cmb, 0, 0)
        layout.addWidget(self.shape_btn, 0, 1)
        return layout

    def sel_cnl_layout_ui(self):
        self.select_btn = QtWidgets.QPushButton("Select Object")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.select_btn, 0, 0)
        layout.addWidget(self.cancel_btn, 0, 1)
        return layout


class RandomScatter(object):
    random.seed(1234)

    '''cubeList = cmds.ls( 'myCube*' )
    if len(cubeList) > 0:
        cmds.delete(cubeList)'''

    result = cmds.polyCube(w=1, h=1, d=1, name='myCube#')

    transformName = result[0]

    instanceGroupName = cmds.group(empty=True,
                                   name=transformName + '_instance_grp#')

    for i in range(0, 50):
        instanceResult = cmds.instance(transformName,
                                       name=transformName + '_instance#')

        cmds.parent(instanceResult, instanceGroupName)

        x = random.uniform(-10, 10)
        y = random.uniform(0, 20)
        z = random.uniform(-10, 10)

        cmds.move(x, y, z, instanceResult)

        xRot = random.uniform(0, 360)
        yRot = random.uniform(0, 360)
        zRot = random.uniform(0, 360)

        cmds.rotate(xRot, yRot, zRot, instanceResult)

        scalingFactor = random.uniform(0.3, 1.5)

        cmds.scale(scalingFactor, scalingFactor, scalingFactor, instanceResult)

    cmds.hide(transformName)

    cmds.xform(instanceGroupName, centerPivots=True)
