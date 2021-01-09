"""
The entire plugin has one top level property: `attacher`. All other custom
properties are member of attacher.


attacher will be registered as a property of bpy.types.Context at runtime, so
that other components can access it.
"""

import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       CollectionProperty,
                       )
from bpy.types import PropertyGroup
from typing import Dict


class CUSTOM_AttributeListItemProperties(PropertyGroup):
    """
    Attribute list item.
    """

    attr_name = StringProperty(
        name="attribute",
        description="Attribute",
        default="<Unknow>"
    )

    # TODO 2020-10-26:Jimmy:we don't know what attributes look like yet.


class CUSTOM_ObjectListProperties(PropertyGroup):
    """
    Object list item.

    Each item corresponds to an object in the scene.
    Each item also has their own attribute list.
    """
    ref = PointerProperty(
        name="Object",
        type=bpy.types.Object,
    )

    # Attribute list.
    attributes = CollectionProperty(
        name="Attribute List",
        type=CUSTOM_AttributeListItemProperties,
    )

    # Index of the active attribute.
    active_attribute = IntProperty()


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------


class CUSTOM_AttacherProperties(PropertyGroup):
    """
    Top level property.
    All other properties can be accessed from here.

    Notice `AllAttributeList` is the list shows up on popup menu, it contains
    all attributes provide by the sdk.
    `AttributeList` in each object property is the list of attributes they
    attached to.
    """

    # Export by scene or by object.
    # By scene means export all objects in the scene by default.
    # By object means only export objects selected by the user.
    export_mode = EnumProperty(
        name="Export mode",
        description="How to export objects",
        items=[('by_scene', "By scene", "Export by scene"),
               ('by_object', "By object", "Export by select object"),
               ],
    )

    # The list of objects that is currently tracked by the plugin.
    # If export_mode is by scene, all objects will be on the list.
    # If export_mode is by object, only objects with attributes attached
    # will be on the list.
    objects = CollectionProperty(
        name="Object list",
        type=CUSTOM_ObjectListProperties,
    )

    # The index of current active object.
    active_object = IntProperty()

    # The list of all attributes.
    all_attributes = CollectionProperty(
        name="All Attribute list",
        type=CUSTOM_AttributeListItemProperties,
    )

    # The index of current active attribute on popup.
    active_all_attribute = IntProperty()


# some helper functions to access properties.


def attribute_table(context: bpy.types.Context) -> Dict:
    """
    take a snapshot of the state of objects and their
    attached attributes.
    @param context: blender context with `attacher` object patched in.
    @return: Dictionary from object to list of attributes.
    """
    # 2020-11-22 Jimmy: For exporting the ormat.
    # TODO this is a demo, needs to fit for the real attributes.
    attacher = context.scene.attacher
    objects = attacher.objects
    return {}


# Note: the order is important since object properties depends on
#       attribute properties.
property_classes = (CUSTOM_AttributeListItemProperties,
                    CUSTOM_ObjectListProperties,
                    )
