"""
UI for object list.

The object list lists all objects the plugin currently is tracking.
Each object on the list can be unfold, shows a list of attributes it
attached.

There is an "add attribute" buttom on each item, click it will bring up
a popup with the list of all attributes.

NOTE:
    whenever you create a new operators, remember to import it
    here. The plugin will find class name start with CUSTOM_ and
    reigster them to blender.
"""

from .attributes import CUSTOM_OT_AddAttributeListPop
from .attributes import CUSTOM_UL_AttributeListPop

from .ulist import CUSTOM_UL_ObjectList
from .ulist import CUSTOM_UL_AttributeList

from .ops import CUSTOM_OT_AddObjectList
from .ops import CUSTOM_OT_RemoveObjectList
from .ops import CUSTOM_OT_RemoveAttributeList
from .ops import CUSTOM_OT_AddAttributeList

import typing
from bpy.types import (Panel, UIList, Operator)
import bpy


class CUSTOM_PT_AttacherList(Panel):
    """
    The panel for holding object list.
    """
    bl_label = "Object List"
    bl_idname = "CUSTOM_PT_attacher_list"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Attacher"
    bl_context = "objectmode"

    nrows = 10

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        attacher = scene.attacher

        draw_fac = 0
        obj = None

        row = layout.row()  # row 1

        split = layout.split(factor=draw_fac)

        split.template_list(listtype_name="CUSTOM_UL_ObjectList",
                            list_id="ObjectList",
                            dataptr=attacher,
                            propname="objects",
                            active_dataptr=attacher,
                            active_propname="active_object",
                            rows=self.nrows)

        # TODO 2020-10-25:Jimmy:need test with fake data.
        # TODO 2020-10-26:Jimmy:the sub list doesn't shows
        if len(attacher.objects) > 0 and \
                attacher.active_object != -1:
            draw_fac = 0.5
            obj = attacher.objects[attacher.active_object]
            split.template_list(listtype_name="CUSTOM_UL_AttributeList",
                                list_id="AttributeList",
                                dataptr=obj,
                                propname="attributes",
                                active_dataptr=obj,
                                active_propname="active_attribute",
                                rows=self.nrows)

        row = layout.row()  # row 2
        row.operator(CUSTOM_OT_RemoveObjectList.bl_idname,
                     text="Remove Objects", icon="REMOVE").remove_all = True
        # row.operator(CUSTOM_OT_RemoveObjectList.bl_idname,
        #              text="Remove Attributes", icon="REMOVE")
        row.operator(CUSTOM_OT_RemoveAttributeList.bl_idname,
                     text="Remove Attributes", icon="REMOVE")

        row = layout.row()  # row 2
        row.operator(CUSTOM_OT_AddObjectList.bl_idname, icon="PLUS")

        # click add attribute popup list of all sdk attributes.
        row.operator(CUSTOM_OT_AddAttributeListPop.bl_idname, icon="PLUS")


list_classes = tuple(
    v for k, v in globals().items() if k.startswith("CUSTOM"))
