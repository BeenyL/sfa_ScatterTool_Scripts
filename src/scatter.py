import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
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
        self.setMaximumWidth(650)
        self.setMinimumHeight(250)
        self.setMaximumHeight(255)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.defaultSubDiv = DefaultSubDiv()
        self.defaultRot = DefaultRot()
        self.defaultScl = DefaultScl()
        self.defaultDen = DefaultDensity()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: Bold 20px")
        self.create_poly = QtWidgets.QLabel("Create a Polygon")
        self.create_poly.setStyleSheet("font: Bold 10px")
        self.scatter_rot_lbl = QtWidgets.QLabel("Scatter Rotation")
        self.scatter_rot_lbl.setStyleSheet("font: Bold 10px")
        self.scatter_scl_lbl = QtWidgets.QLabel("Scatter Scale")
        self.scatter_scl_lbl.setStyleSheet("font: Bold 10px")
        self.create_obj_lay = self.create_obj_layout_ui()
        self.sct_cnl_lay = self.sct_cnl_layout_ui()
        self.rnd_rotation_lay = self.rnd_rotation_ui()
        self.rnd_scale_lay = self.rnd_scale_ui()
        self.create_den_sct_lay = self.create_density_scatter_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.create_poly)
        self.main_lay.addLayout(self.create_obj_lay)
        self.main_lay.addWidget(self.scatter_rot_lbl)
        self.main_lay.addLayout(self.rnd_rotation_lay)
        self.main_lay.addWidget(self.scatter_scl_lbl)
        self.main_lay.addLayout(self.rnd_scale_lay)
        self.main_lay.addLayout(self.create_den_sct_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.sct_cnl_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter_object)
        self.cancel_btn.clicked.connect(self.cancel)
        self.shape_btn.clicked.connect(self.create_shape)
        self.sub_ax_sbx.valueChanged.connect(self.update_sub_val_ax)
        self.sub_hgt_sbx.valueChanged.connect(self.update_sub_val_hgt)
        self.sub_bas_sbx.valueChanged.connect(self.update_sub_val_bas)
        self.shape_cmb.currentIndexChanged.connect(self.update_div)

        self.rot_btn.clicked.connect(self.scatter_rotate_object)
        self.min_x_rot_sbx.valueChanged.connect(self.update_rot_min_val_x)
        self.min_y_rot_sbx.valueChanged.connect(self.update_rot_min_val_y)
        self.min_z_rot_sbx.valueChanged.connect(self.update_rot_min_val_z)
        self.max_x_rot_sbx.valueChanged.connect(self.update_rot_max_val_x)
        self.max_y_rot_sbx.valueChanged.connect(self.update_rot_max_val_y)
        self.max_z_rot_sbx.valueChanged.connect(self.update_rot_max_val_z)

        self.scl_btn.clicked.connect(self.scatter_scale_object)
        self.min_x_scl_sbx.valueChanged.connect(self.update_scl_min_val_x)
        self.min_y_scl_sbx.valueChanged.connect(self.update_scl_min_val_y)
        self.min_z_scl_sbx.valueChanged.connect(self.update_scl_min_val_z)
        self.max_x_scl_sbx.valueChanged.connect(self.update_scl_max_val_x)
        self.max_y_scl_sbx.valueChanged.connect(self.update_scl_max_val_y)
        self.max_z_scl_sbx.valueChanged.connect(self.update_scl_max_val_z)

        self.scatter_density_sbx.valueChanged.connect(self.update_sct_den_val)

    def update_sub_val_ax(self):
        self.defaultSubDiv.cur_sub_ax = self.sub_ax_sbx.value()

    def update_sub_val_hgt(self):
        self.defaultSubDiv.cur_sub_hgt = self.sub_hgt_sbx.value()

    def update_sub_val_bas(self):
        self.defaultSubDiv.cur_sub_bas = self.sub_bas_sbx.value()

    def update_rot_min_val_x(self):
        self.defaultRot.min_rot_x = self.min_x_rot_sbx.value()

    def update_rot_min_val_y(self):
        self.defaultRot.min_rot_y = self.min_y_rot_sbx.value()

    def update_rot_min_val_z(self):
        self.defaultRot.min_rot_z = self.min_z_rot_sbx.value()

    def update_rot_max_val_x(self):
        self.defaultRot.max_rot_x = self.max_x_rot_sbx.value()

    def update_rot_max_val_y(self):
        self.defaultRot.max_rot_y = self.max_y_rot_sbx.value()

    def update_rot_max_val_z(self):
        self.defaultRot.max_rot_z = self.max_z_rot_sbx.value()

    def update_scl_min_val_x(self):
        self.defaultScl.min_scl_x = self.min_x_scl_sbx.value()

    def update_scl_min_val_y(self):
        self.defaultScl.min_scl_y = self.min_y_scl_sbx.value()

    def update_scl_min_val_z(self):
        self.defaultScl.min_scl_z = self.min_z_scl_sbx.value()

    def update_scl_max_val_x(self):
        self.defaultScl.max_scl_x = self.max_x_scl_sbx.value()

    def update_scl_max_val_y(self):
        self.defaultScl.max_scl_y = self.max_y_scl_sbx.value()

    def update_scl_max_val_z(self):
        self.defaultScl.max_scl_z = self.max_z_scl_sbx.value()

    def update_sct_den_val(self):
        self.defaultDen.def_density = self.scatter_density_sbx.value() / 100

    @QtCore.Slot()
    def create_shape(self):
        """create polygon tool"""
        if self.shape_cmb.currentText() == "Cube":
            cmds.polyCube(name="Cube",
                          sw=self.defaultSubDiv.cur_sub_ax,
                          sh=self.defaultSubDiv.cur_sub_hgt,
                          sd=self.defaultSubDiv.cur_sub_bas)
        if self.shape_cmb.currentText() == "Sphere":
            cmds.polySphere(name="Sphere",
                            sa=self.defaultSubDiv.cur_sub_ax,
                            sh=self.defaultSubDiv.cur_sub_hgt)
        if self.shape_cmb.currentText() == "Cylinder":
            cmds.polyCylinder(name="Cylinder",
                              sa=self.defaultSubDiv.cur_sub_ax,
                              sh=self.defaultSubDiv.cur_sub_hgt,
                              sc=self.defaultSubDiv.cur_sub_bas)
        if self.shape_cmb.currentText() == "Cone":
            cmds.polyCone(name="Cone",
                          sa=self.defaultSubDiv.cur_sub_ax,
                          sh=self.defaultSubDiv.cur_sub_hgt,
                          sc=self.defaultSubDiv.cur_sub_bas)

    @QtCore.Slot()
    def scatter_object(self):
        """scatter an Object"""
        # scatter object currently responsible for rotation and scale
        vert_list = cmds.ls(selection=True, fl=True)
        scatter_grp = cmds.group(n='scatter_grp')
        object_to_instance = vert_list[0]
        if cmds.objectType(object_to_instance) == 'transform':
            sct_den = random.sample(vert_list, len(vert_list) *
                                    self.defaultDen.def_density)
            for sct_den in vert_list:
                vertex_pos = cmds.xform(sct_den, q=True, ws=True, t=True)
                new_instance = cmds.instance(object_to_instance)

                cmds.move(vertex_pos[0], vertex_pos[1], vertex_pos[2],
                          new_instance)

                rand_rot_x = random.uniform(self.defaultRot.min_rot_x,
                                            self.defaultRot.max_rot_x)
                rand_rot_y = random.uniform(self.defaultRot.min_rot_y,
                                            self.defaultRot.max_rot_y)
                rand_rot_z = random.uniform(self.defaultRot.min_rot_z,
                                            self.defaultRot.max_rot_z)
                cmds.rotate(rand_rot_x,
                            rand_rot_y,
                            rand_rot_z,
                            new_instance, relative=True, objectSpace=True)

                rand_scl_x = random.uniform(self.defaultScl.min_scl_x,
                                            self.defaultScl.max_scl_x)
                rand_scl_y = random.uniform(self.defaultScl.min_scl_y,
                                            self.defaultScl.max_scl_y)
                rand_scl_z = random.uniform(self.defaultScl.min_scl_z,
                                            self.defaultScl.max_scl_z)
                cmds.scale(rand_scl_x,
                           rand_scl_y,
                           rand_scl_z,
                           new_instance, relative=True)

    @QtCore.Slot()
    def scatter_rotate_object(self, new_instance):
        """test"""
        rand_rot_x = random.uniform(self.defaultRot.min_rot_x,
                                    self.defaultRot.max_rot_x)
        rand_rot_y = random.uniform(self.defaultRot.min_rot_y,
                                    self.defaultRot.max_rot_y)
        rand_rot_z = random.uniform(self.defaultRot.min_rot_z,
                                    self.defaultRot.max_rot_z)
        cmds.rotate(rand_rot_x,
                    rand_rot_y,
                    rand_rot_z,
                    new_instance, relative=True, objectSpace=True)

    @QtCore.Slot()
    def scatter_scale_object(self, new_instance):
        """test"""
        rand_scl_x = random.uniform(self.defaultScl.min_scl_x,
                                    self.defaultScl.max_scl_x)
        rand_scl_y = random.uniform(self.defaultScl.min_scl_y,
                                    self.defaultScl.max_scl_y)
        rand_scl_z = random.uniform(self.defaultScl.min_scl_z,
                                    self.defaultScl.max_scl_z)
        cmds.scale(rand_scl_x,
                   rand_scl_y,
                   rand_scl_z,
                   new_instance, relative=True)

    @QtCore.Slot()
    def update_div(self):
        """update subdivision"""
        if self.shape_cmb.currentText() == "Cube":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.cb_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.cb_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.cb_sub_bas
        if self.shape_cmb.currentText() == "Sphere":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.s_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.s_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.s_sub_bas
        if self.shape_cmb.currentText() == "Cylinder":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.cyl_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.cyl_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.cyl_sub_bas
        if self.shape_cmb.currentText() == "Cone":
            self.defaultSubDiv.cur_sub_ax = self.defaultSubDiv.cn_sub_ax
            self.defaultSubDiv.cur_sub_hgt = self.defaultSubDiv.cn_sub_hgt
            self.defaultSubDiv.cur_sub_bas = self.defaultSubDiv.cn_sub_bas

        self.sub_ax_sbx.setValue(self.defaultSubDiv.cur_sub_ax)
        self.sub_hgt_sbx.setValue(self.defaultSubDiv.cur_sub_hgt)
        self.sub_bas_sbx.setValue(self.defaultSubDiv.cur_sub_bas)

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()

    def create_density_scatter_ui(self):
        self.scatter_density_sbx = QtWidgets.QSpinBox()
        self.scatter_density_sbx.setMaximum(100)
        self.scatter_density_sbx.setSuffix(" %")
        self.scatter_density_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox
                                                  .PlusMinus)
        self.scatter_density_sbx.setFixedWidth(100)
        self.scatter_density_sbx.setValue(self.defaultDen.def_density)
        self.scatter_density_lbl = QtWidgets.QLabel("Scatter Density")
        self.scatter_density_lbl.setFixedWidth(80)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_density_lbl, 0, 0)
        layout.addWidget(self.scatter_density_sbx, 0, 1)
        return layout

    def create_obj_layout_ui(self):
        """create polygon sub-div"""
        self.create_shape_cmb()
        self.sub_div_ax_sbx()
        self.sub_div_hgt_sbx()
        self.sub_div_bas_sbx()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.shape_cmb, 0, 0)
        layout.addWidget(self.shape_btn, 0, 1)
        layout.addWidget(self.sub_ax, 0, 3)
        layout.addWidget(self.sub_ax_sbx, 0, 4)
        layout.addWidget(self.sub_hgt, 0, 5)
        layout.addWidget(self.sub_hgt_sbx, 0, 6)
        layout.addWidget(self.sub_bas, 0, 7)
        layout.addWidget(self.sub_bas_sbx, 0, 8)
        return layout

    def sub_div_ax_sbx(self):
        self.sub_ax_sbx = QtWidgets.QSpinBox()
        self.sub_ax_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_ax_sbx.setFixedWidth(50)
        self.sub_ax_sbx.setValue(self.defaultSubDiv.cur_sub_ax)

        self.sub_ax = QtWidgets.QLabel("Sub Axis")
        self.sub_ax.setFixedWidth(60)
        self.sub_ax.setIndent(14)

    def sub_div_hgt_sbx(self):
        self.sub_hgt_sbx = QtWidgets.QSpinBox()
        self.sub_hgt_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_hgt_sbx.setFixedWidth(50)
        self.sub_hgt_sbx.setValue(self.defaultSubDiv.cur_sub_hgt)

        self.sub_hgt = QtWidgets.QLabel("Sub Height")
        self.sub_hgt.setFixedWidth(65)
        self.sub_hgt.setIndent(5)

    def sub_div_bas_sbx(self):
        self.sub_bas_sbx = QtWidgets.QSpinBox()
        self.sub_bas_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.sub_bas_sbx.setFixedWidth(50)
        self.sub_bas_sbx.setValue(self.defaultSubDiv.cur_sub_bas)

        self.sub_bas = QtWidgets.QLabel("Sub Base")
        self.sub_bas.setFixedWidth(60)
        self.sub_bas.setIndent(14)

    def create_shape_cmb(self):
        self.shape_cmb = QtWidgets.QComboBox()
        self.shape_cmb.setFixedWidth(100)
        self.shape_cmb.addItems(['Cube', 'Sphere', 'Cylinder', 'Cone'])
        self.shape_btn = QtWidgets.QPushButton("Create Shape")

    def sct_cnl_layout_ui(self):
        """scatter and cancel layout"""
        self.scatter_btn = QtWidgets.QPushButton("Scatter Object")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scatter_btn, 0, 0)
        layout.addWidget(self.cancel_btn, 0, 1)
        return layout

    def rnd_rotation_ui(self):
        """random roatation layout"""
        self.rot_btn = QtWidgets.QPushButton("Randomize Rotation")
        self.x_rot_sbx()
        self.y_rot_sbx()
        self.z_rot_sbx()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.rot_btn, 0, 0)
        layout.addWidget(self.rotX_lbl, 0, 1)
        layout.addWidget(self.min_x_rot_sbx, 0, 2)
        layout.addWidget(self.x_rot_space, 0, 3)
        layout.addWidget(self.max_x_rot_sbx, 0, 4)
        layout.addWidget(self.rotY_lbl, 0, 5)
        layout.addWidget(self.min_y_rot_sbx, 0, 6)
        layout.addWidget(self.y_rot_space, 0, 7)
        layout.addWidget(self.max_y_rot_sbx, 0, 8)
        layout.addWidget(self.rotZ_lbl, 0, 9)
        layout.addWidget(self.min_z_rot_sbx, 0, 10)
        layout.addWidget(self.z_rot_space, 0, 11)
        layout.addWidget(self.max_z_rot_sbx, 0, 12)
        return layout

    def x_rot_sbx(self):
        self.min_x_rot_sbx = QtWidgets.QSpinBox()
        self.min_x_rot_sbx.setMaximum(360)
        self.min_x_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_rot_sbx.setFixedWidth(50)
        self.min_x_rot_sbx.setValue(self.defaultRot.min_rot_x)

        self.rotX_lbl = QtWidgets.QLabel("X")
        self.rotX_lbl.setFixedWidth(15)
        self.rotX_lbl.setIndent(9)
        self.x_rot_space = QtWidgets.QLabel("-")
        self.x_rot_space.setFixedWidth(10)
        self.x_rot_space.setStyleSheet("font: 20px")

        self.max_x_rot_sbx = QtWidgets.QSpinBox()
        self.max_x_rot_sbx.setMaximum(360)
        self.max_x_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_rot_sbx.setFixedWidth(50)
        self.max_x_rot_sbx.setValue(self.defaultRot.max_rot_x)

    def y_rot_sbx(self):
        self.min_y_rot_sbx = QtWidgets.QSpinBox()
        self.min_y_rot_sbx.setMaximum(360)
        self.min_y_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_rot_sbx.setFixedWidth(50)
        self.min_y_rot_sbx.setValue(self.defaultRot.min_rot_y)

        self.rotY_lbl = QtWidgets.QLabel("Y")
        self.rotY_lbl.setFixedWidth(15)
        self.rotY_lbl.setIndent(9)
        self.y_rot_space = QtWidgets.QLabel("-")
        self.y_rot_space.setFixedWidth(10)
        self.y_rot_space.setStyleSheet("font: 20px")

        self.max_y_rot_sbx = QtWidgets.QSpinBox()
        self.max_y_rot_sbx.setMaximum(360)
        self.max_y_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_rot_sbx.setFixedWidth(50)
        self.max_y_rot_sbx.setValue(self.defaultRot.max_rot_y)

    def z_rot_sbx(self):
        self.min_z_rot_sbx = QtWidgets.QSpinBox()
        self.min_z_rot_sbx.setMaximum(360)
        self.min_z_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_rot_sbx.setFixedWidth(50)
        self.min_z_rot_sbx.setValue(self.defaultRot.min_rot_z)

        self.rotZ_lbl = QtWidgets.QLabel("Z")
        self.rotZ_lbl.setFixedWidth(15)
        self.rotZ_lbl.setIndent(9)
        self.z_rot_space = QtWidgets.QLabel("-")
        self.z_rot_space.setFixedWidth(10)
        self.z_rot_space.setStyleSheet("font: 20px")

        self.max_z_rot_sbx = QtWidgets.QSpinBox()
        self.max_z_rot_sbx.setMaximum(360)
        self.max_z_rot_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_rot_sbx.setFixedWidth(50)
        self.max_z_rot_sbx.setValue(self.defaultRot.max_rot_z)

    def rnd_scale_ui(self):
        """random scale layout"""
        self.scl_btn = QtWidgets.QPushButton("Randomize Scale")
        self.x_scl_sbx()
        self.y_scl_sbx()
        self.z_scl_sbx()

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.scl_btn, 0, 0)
        layout.addWidget(self.sclX_lbl, 0, 1)
        layout.addWidget(self.min_x_scl_sbx, 0, 2)
        layout.addWidget(self.x_scl_space, 0, 3)
        layout.addWidget(self.max_x_scl_sbx, 0, 4)
        layout.addWidget(self.sclY_lbl, 0, 5)
        layout.addWidget(self.min_y_scl_sbx, 0, 6)
        layout.addWidget(self.y_scl_space, 0, 7)
        layout.addWidget(self.max_y_scl_sbx, 0, 8)
        layout.addWidget(self.sclZ_lbl, 0, 9)
        layout.addWidget(self.min_z_scl_sbx, 0, 10)
        layout.addWidget(self.z_scl_space, 0, 11)
        layout.addWidget(self.max_z_scl_sbx, 0, 12)
        return layout

    def x_scl_sbx(self):
        self.min_x_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.min_x_scl_sbx.setDecimals(1)
        self.min_x_scl_sbx.setSingleStep(.1)
        self.min_x_scl_sbx.setMaximum(10)
        self.min_x_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_x_scl_sbx.setFixedWidth(50)
        self.min_x_scl_sbx.setValue(self.defaultScl.min_scl_x)
        self.sclX_lbl = QtWidgets.QLabel("X")
        self.sclX_lbl.setFixedWidth(15)
        self.sclX_lbl.setIndent(9)
        self.x_scl_space = QtWidgets.QLabel("-")
        self.x_scl_space.setFixedWidth(10)
        self.x_scl_space.setStyleSheet("font: 20px")
        self.max_x_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.max_x_scl_sbx.setDecimals(1)
        self.max_x_scl_sbx.setSingleStep(.1)
        self.max_x_scl_sbx.setMaximum(10)
        self.max_x_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_x_scl_sbx.setFixedWidth(50)
        self.max_x_scl_sbx.setValue(self.defaultScl.max_scl_x)

    def y_scl_sbx(self):
        self.min_y_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.min_y_scl_sbx.setDecimals(1)
        self.min_y_scl_sbx.setSingleStep(.1)
        self.min_y_scl_sbx.setMaximum(10)
        self.min_y_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_y_scl_sbx.setFixedWidth(50)
        self.min_y_scl_sbx.setValue(self.defaultScl.min_scl_y)
        self.sclY_lbl = QtWidgets.QLabel("Y")
        self.sclY_lbl.setFixedWidth(15)
        self.sclY_lbl.setIndent(9)
        self.y_scl_space = QtWidgets.QLabel("-")
        self.y_scl_space.setFixedWidth(10)
        self.y_scl_space.setStyleSheet("font: 20px")
        self.max_y_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.max_y_scl_sbx.setDecimals(1)
        self.max_y_scl_sbx.setSingleStep(.1)
        self.max_y_scl_sbx.setMaximum(10)
        self.max_y_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_y_scl_sbx.setFixedWidth(50)
        self.max_y_scl_sbx.setValue(self.defaultScl.max_scl_y)

    def z_scl_sbx(self):
        self.min_z_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.min_z_scl_sbx.setDecimals(1)
        self.min_z_scl_sbx.setSingleStep(.1)
        self.min_z_scl_sbx.setMaximum(10)
        self.min_z_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.min_z_scl_sbx.setFixedWidth(50)
        self.min_z_scl_sbx.setValue(self.defaultScl.min_scl_z)
        self.sclZ_lbl = QtWidgets.QLabel("Z")
        self.sclZ_lbl.setFixedWidth(15)
        self.sclZ_lbl.setIndent(9)
        self.z_scl_space = QtWidgets.QLabel("-")
        self.z_scl_space.setFixedWidth(10)
        self.z_scl_space.setStyleSheet("font: 20px")
        self.max_z_scl_sbx = QtWidgets.QDoubleSpinBox()
        self.max_z_scl_sbx.setDecimals(1)
        self.max_z_scl_sbx.setSingleStep(.1)
        self.max_z_scl_sbx.setMaximum(10)
        self.max_z_scl_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.max_z_scl_sbx.setFixedWidth(50)
        self.max_z_scl_sbx.setValue(self.defaultScl.max_scl_z)


class DefaultSubDiv(object):

    def __init__(self):
        self.cur_sub_ax = 1
        self.cur_sub_hgt = 1
        self.cur_sub_bas = 1
        self.cb_sub_ax = 1
        self.cb_sub_hgt = 1
        self.cb_sub_bas = 1
        self.s_sub_ax = 8
        self.s_sub_hgt = 8
        self.s_sub_bas = 0
        self.cyl_sub_ax = 8
        self.cyl_sub_hgt = 4
        self.cyl_sub_bas = 0
        self.cn_sub_ax = 8
        self.cn_sub_hgt = 3
        self.cn_sub_bas = 0


class DefaultRot(object):

    def __init__(self):
        self.min_rot_x = 0
        self.min_rot_y = 0
        self.min_rot_z = 0
        self.max_rot_x = 360
        self.max_rot_y = 360
        self.max_rot_z = 360


class DefaultScl(object):

    def __init__(self):
        self.min_scl_x = 0.8
        self.min_scl_y = 0.8
        self.min_scl_z = 0.8
        self.max_scl_x = 1.2
        self.max_scl_y = 1.2
        self.max_scl_z = 1.2


class DefaultDensity(object):

    def __init__(self):
        self.def_density = 100
