
from ...util import Do, Foreach, TRec, recurse
from typing import TYPE_CHECKING, cast, Callable
if TYPE_CHECKING:
    from ...properties import CUSTOM_AttacherProperties
from bpy.types import (Operator)
import bpy
from ... import config


import logging


class CUSTOM_OT_Attacher(Operator):
    bl_label = "Refresh"
    bl_idname = "custom.attacher"
    bl_description = "Change the current loaded list."

    def execute(self, context):
        attacher: CUSTOM_AttacherProperties
        attacher = context.scene.attacher

        mode: bpy.types.EnumProperty
        mode = attacher.export_mode

        if str(mode) == "by_scene":
            logging.debug("refresh by scene")
            self.by_scene(context)
        elif str(mode) == "by_object":
            logging.debug("refresh by object ")
            raise NotImplementedError
        else:
            raise RuntimeError("Unknown export mode.")
        return {'FINISHED'}

    def by_scene(self, context):
        """
        handle refresh by scene
        """
        logging.debug("mode: export by scene.")
        refresh_objects(context)


def refresh_objects(context: bpy.types.Context):
    """
    Initialize the context.attacher.objects
    @ Need to traverse both attacher object list and scene.objects.
      - Traverse attacher.objects to make sure not adding existed
        object.
      - Traverse scene.objects to make sure deleted objects won't appear in
        the object list.
    """
    attacher = context.scene.attacher
    alist = attacher.objects

    # set old list idx
    attacher.active_obj = len(alist) - 1

    old_hash = list(hash(n.ref) for n in alist)
    scene_hash = list(hash(n) for n in context.scene.objects)

    if config.DEBUG:
        logging.debug("oldlist: {}".format([n.ref.name for n in alist]))
        logging.debug("scenelist: {}".format(
            [n.name for n in context.scene.objects]))
        logging.debug("\n")

    for scene_obj in context.scene.objects:  # add to alist if not there.
        if hash(scene_obj) not in old_hash:
            o = alist.add()
            o.ref = scene_obj
            o.name = scene_obj.name

    # Do this until there is no None in alist.
    # This is tail recurse optimized, no performance issue.
    # for prop in alist:
    #     if hash(obj := prop.ref) not in scene_hash and obj is not None:
    #             attacher.active_obj -= 1
    #             alist.remove(alist.find(obj.name))

    def try_remove():
        for prop in alist:
            obj = prop.ref
            if obj is None:
                return True
            elif hash(obj) not in scene_hash:
                attacher.active_obj -= 1
                alist.remove(alist.find(obj.name))

    while (try_remove()):
        continue

    attacher.active_obj = len(alist) - 1


def add_object_to_list(context: bpy.types.Context):
    """
    Add the current focused object to list.
    """
    logging.debug("add_object_to_list")
    scene = context.scene
    active_obj = context.active_object

    if hash(active_obj) in (
            hash(n.ref) for n in scene.attacher.objects):
        return

    o = scene.attacher.objects.add()
    o.ref = active_obj
    o.name = active_obj.name


def remove_object_from_list(context: bpy.types.Context, obj):
    """
    Remove an object from list.
    """
    logging.debug("remove_object_from_list")
    scene = context.scene
    if hash(obj) not in (
            hash(n.ref) for n in scene.attacher.objects):
        return
    scene.attacher.objects.remove(obj.name)
