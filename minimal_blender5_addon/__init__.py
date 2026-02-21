"""Minimal Blender 5.x add-on template."""

bl_info = {
    "name": "Simple_hair5",
    "author": "Your Name",
    "version": (0, 13, 0),
    "blender": (5, 0, 0),
    "location": "3D View > N Panel > SH5",
    "description": "A minimal starter add-on template for Blender 5.x",
    "category": "3D View",
}

import bpy

TAB_NAME = "SH5"
BASE_OBJECT_NAMES = ("hair", "taper", "bavel")
COLLECTION_BY_BASE_NAME = {
    "taper": "taper",
    "bavel": "bevel",
}


def unique_object_name(base_name: str) -> str:
    """Return a unique object name by appending trailing numbers when needed."""
    if bpy.data.objects.get(base_name) is None:
        return base_name

    index = 1
    while True:
        candidate = f"{base_name}{index}"
        if bpy.data.objects.get(candidate) is None:
            return candidate
        index += 1


def get_or_create_collection(collection_name: str) -> bpy.types.Collection:
    """Get existing collection or create a new one under the scene root collection."""
    collection = bpy.data.collections.get(collection_name)
    if collection is not None:
        return collection

    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def move_object_to_collection(obj: bpy.types.Object, target_collection: bpy.types.Collection) -> None:
    """Move object to the target collection only."""
    for linked_collection in list(obj.users_collection):
        linked_collection.objects.unlink(obj)
    target_collection.objects.link(obj)


class DEMO_OT_create_curves(bpy.types.Operator):
    """Create hair/taper/bavel objects with unique suffixes and collection routing."""

    bl_idname = "demo.create_curves"
    bl_label = "Create hair/taper/bavel"

    def execute(self, context):
        created_names = []
        created_objects = {}

        active_collection = context.collection

        for index, base_name in enumerate(BASE_OBJECT_NAMES):
            object_name = unique_object_name(base_name)
            collection_name = COLLECTION_BY_BASE_NAME.get(base_name)
            location = (float(index) * 1.5, 0.0, 0.0)

            if base_name == "bavel":
                bpy.ops.curve.primitive_bezier_circle_add(location=location)
            else:
                bpy.ops.curve.primitive_bezier_curve_add(location=location)

            created_object = context.view_layer.objects.active
            created_object.name = object_name
            if created_object.data is not None:
                created_object.data.name = object_name

            if collection_name is None:
                target_collection = active_collection
            else:
                target_collection = get_or_create_collection(collection_name)

            move_object_to_collection(created_object, target_collection)

            created_objects[base_name] = created_object
            created_names.append(object_name)

        hair_object = created_objects.get("hair")
        taper_object = created_objects.get("taper")
        bavel_object = created_objects.get("bavel")

        if hair_object is not None and taper_object is not None:
            hair_object.data.taper_object = taper_object

        if hair_object is not None and bavel_object is not None:
            hair_object.data.bevel_mode = "OBJECT"
            hair_object.data.bevel_object = bavel_object

        self.report({"INFO"}, f"Created objects: {', '.join(created_names)}")
        return {"FINISHED"}


class DEMO_PT_panel(bpy.types.Panel):
    """Simple panel shown in the 3D View N-panel."""

    bl_label = "SH5"
    bl_idname = "DEMO_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = TAB_NAME

    def draw(self, context):
        layout = self.layout
        layout.label(text="3D View > Nパネル > SH5")
        layout.operator(DEMO_OT_create_curves.bl_idname, icon="CURVE_DATA")


classes = (DEMO_OT_create_curves, DEMO_PT_panel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
