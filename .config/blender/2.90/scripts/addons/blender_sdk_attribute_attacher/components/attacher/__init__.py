"""
Attacher panel
  A top level panel that provides some global settings.
  e.g setting the export mode as by scene or by object.
"""


import bpy

from bpy.utils import register_class
from bpy.utils import unregister_class
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator
                       )

from .ops import CUSTOM_OT_Attacher

import logging

"""
 Name convention used
    HT – Header
    MT – Menu
    OT – Operator
    PT – Panel
    UL – UI list
"""

"""
# Class name -> bl_idname
    class CUSTOM_MT_CustomMenu(Menu) -> bl_idname = "OBJECT_MT_custom_menu"
"""


class CUSTOM_PT_AttacherPanel(Panel):
    """
    A top level panel that provides some global settings.
    e.g setting the export mode as by scene or by object.
    """
    bl_label = "Attacher"
    bl_idname = "CUSTOM_PT_attacher_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Attacher"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        attacher = scene.attacher

        row = layout.row()
        row.prop(attacher, "export_mode", text="")
        row.operator(CUSTOM_OT_Attacher.bl_idname)
        layout.separator()


attacher_classes = tuple(v for k, v in globals().items()
                         if k.startswith("CUSTOM"))
