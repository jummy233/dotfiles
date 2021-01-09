from bpy.types import (Operator)
import bpy.types
import bpy

# ------------------------------------------------------------------------
#    Operator
# ------------------------------------------------------------------------

# TODO design operator


class CUSTOM_OT_AddObjectList(Operator):
    """
    Add objects to the object list.
    """
    bl_idname = "custom.attacher_object_list_add"
    bl_label = "Add Object"

    def execute(self, context: bpy.types.Context):
        # TODO
        print("@Add")
        NotImplemented
        return {"FINISHED"}


class CUSTOM_OT_RemoveObjectList(Operator):
    """
    Remove object from object list
    """
    bl_idname = "custom.attacher_object_list_remove"
    bl_label = "Remove Object"

    remove_all = bpy.props.BoolProperty()

    def execute(self, context: bpy.types.Context):
        attacher = context.scene.attacher
        print("@Remove")
        NotImplemented

        return {"FINISHED"}


class CUSTOM_OT_RemoveAttributeList(Operator):
    """
    Remvoe the selected attribute from the focused object list.
    """
    bl_idname = "custom.attacher_alist_remove"
    bl_label = "Remove Attribute"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context):
        attacher = context.scene.attacher
        obj_idx: int = attacher.active_object

        # uninitialized
        if len(attacher.objects) == 0:
            return {"FINISHED"}

        focused_obj = attacher.objects[obj_idx]

        attrs = focused_obj.attributes
        if (len(attrs) > 0):
            focused_attr = attrs[focused_obj.active_attribute]

            if (focused_attr.attr_name in [n.attr_name for n in attrs] and
                    len(attrs) > 0):
                attrs.remove(focused_obj.active_attribute)

        # if it's the last element get deleted, the
        # focused element after deletion should be one idex
        # before.
        attrs_size = len(attrs)
        if focused_obj.active_attribute > attrs_size:
            focused_obj.active_attribute = attrs_size

        return {"FINISHED"}


class CUSTOM_OT_AddAttributeList(Operator):
    """
    Add attribute list operator on popop menu
    """
    bl_idname = "custom.attacher_alist_add"
    bl_label = "Add Attribute"

    remove_all = bpy.props.BoolProperty()

    def execute(self, context: bpy.types.Context):
        attacher = context.scene.attacher

        # currenly focused object
        obj_idx: int = attacher.active_object

        objects: bpy.types.CollectionProperty
        objects = attacher.objects

        if len(objects) == 0:  # objects = attacher.objects
            return {"FINISHED"}
        focused_obj = objects[obj_idx]

        # currently focused attribute.
        if len(attacher.all_attributes) > 0:
            focused_attr = attacher.all_attributes[
                attacher.active_all_attribute
            ]

            obj_attrs: bpy.types.CollectionProperty
            obj_attrs = focused_obj.attributes

            # check if focused_attr is in object' attribute list already.
            # it's not strictly necessary because popup attribute list will
            # not show attributes already in object's attr list.
            # But if later we need to modify the list ui at least this logic
            # is robust.
            if focused_attr.attr_name not in list(n.attr_name for n in
                                                  obj_attrs):
                # add attr to object list
                o = obj_attrs.add()
                o.attr_name = focused_attr.attr_name

                # remove list from all attr.
                if len(attacher.all_attributes) == attacher.active_all_attribute:
                    attacher.active_all_attribute -= 1
                attacher.all_attributes.remove(attacher.active_all_attribute)

        return {"FINISHED"}
