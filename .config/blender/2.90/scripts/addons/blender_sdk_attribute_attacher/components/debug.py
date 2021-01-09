import bpy


class CUSTOM_OT_PrintOperator(bpy.types.Operator):
    bl_idname = "attacher.print_operator"
    bl_label = "Print Operator"

    def execute(self, context: bpy.types.Context):
        scene = context.scene
        attacher = scene.attacher

        print("======== Debug Message ===============")
        print(attacher.objects)
        print("======================================")

        return {"FINISHED"}


class CUSTOM_PT_Debug(bpy.types.Panel):
    bl_label = "Debug Panel"
    bl_idname = "OBJECT_PT_attacher_debug"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Attacher"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        layout.operator(CUSTOM_OT_PrintOperator.bl_idname)
        layout.separator()


debug_classes = tuple(
    v for k, v in globals().items() if k.startswith("CUSTOM"))
