"""Minimal Blender 5.x add-on template."""

bl_info = {
    "name": "Simple_hair5",
    "author": "Your Name",
    "version": (0, 17, 0),
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


def get_or_create_collection(
    collection_name: str,
    color_tag: str | None = None,
) -> bpy.types.Collection:
    """Get existing collection or create a new one under the scene root collection."""
    collection = bpy.data.collections.get(collection_name)
    if collection is not None:
        return collection

    collection = bpy.data.collections.new(collection_name)
    if color_tag is not None:
        collection.color_tag = color_tag
    bpy.context.scene.collection.children.link(collection)
    return collection


def move_object_to_collection(obj: bpy.types.Object, target_collection: bpy.types.Collection) -> None:
    """Move object to the target collection only."""
    for linked_collection in list(obj.users_collection):
        linked_collection.objects.unlink(obj)
    target_collection.objects.link(obj)


def split_numeric_suffix(name: str, base_name: str) -> str:
    """Return numeric suffix for names like base, base1, base2."""
    if not name.startswith(base_name):
        return ""

    suffix = name[len(base_name):]
    if suffix.isdigit():
        return suffix
    return ""


def find_existing_partner_object(base_name: str, suffix: str) -> bpy.types.Object | None:
    """Find an existing partner object with same numeric suffix."""
    if suffix == "":
        candidate_names = (base_name,)
    else:
        candidate_names = (f"{base_name}{suffix}",)

    for candidate_name in candidate_names:
        existing_object = bpy.data.objects.get(candidate_name)
        if existing_object is not None:
            return existing_object

    return None


def find_existing_bevel_object(suffix: str) -> bpy.types.Object | None:
    """Find existing bevel partner (prefer bevel*, then bavel* for compatibility)."""
    if suffix == "":
        candidate_names = ("bevel", "bavel")
    else:
        candidate_names = (f"bevel{suffix}", f"bavel{suffix}")

    for candidate_name in candidate_names:
        existing_object = bpy.data.objects.get(candidate_name)
        if existing_object is not None:
            return existing_object

    return None


def choose_partner_name(base_name: str, suffix: str) -> str:
    """Choose partner name that follows hair suffix policy."""
    if suffix:
        return f"{base_name}{suffix}"
    return unique_object_name(base_name)


class DEMO_OT_create_curves(bpy.types.Operator):
    """Create hair/taper/bavel objects with unique suffixes and collection routing."""

    bl_idname = "demo.create_curves"
    bl_label = "Create hair/taper/bavel"

    def execute(self, context):
        created_names = []
        created_objects = {}

        active_collection = context.collection

        hair_name = unique_object_name("hair")
        hair_suffix = split_numeric_suffix(hair_name, "hair")

        bpy.ops.curve.primitive_bezier_curve_add(location=(0.0, 0.0, 0.0))
        hair_object = context.view_layer.objects.active
        hair_object.name = hair_name
        if hair_object.data is not None:
            hair_object.data.name = hair_name
        move_object_to_collection(hair_object, active_collection)

        created_objects["hair"] = hair_object
        created_names.append(hair_name)

        taper_object = find_existing_partner_object("taper", hair_suffix)
        if taper_object is None:
            taper_name = choose_partner_name("taper", hair_suffix)
            bpy.ops.curve.primitive_bezier_curve_add(location=(1.5, 0.0, 0.0))
            taper_object = context.view_layer.objects.active
            taper_object.name = taper_name
            if taper_object.data is not None:
                taper_object.data.name = taper_name
            move_object_to_collection(taper_object, get_or_create_collection("taper", color_tag="COLOR_04"))
            created_names.append(taper_name)

        created_objects["taper"] = taper_object

        bavel_object = find_existing_bevel_object(hair_suffix)
        if bavel_object is None:
            bavel_name = choose_partner_name("bevel", hair_suffix)
            bpy.ops.curve.primitive_bezier_circle_add(location=(3.0, 0.0, 0.0))
            bavel_object = context.view_layer.objects.active
            bavel_object.name = bavel_name
            if bavel_object.data is not None:
                bavel_object.data.name = bavel_name
            move_object_to_collection(bavel_object, get_or_create_collection("bevel", color_tag="COLOR_04"))
            created_names.append(bavel_name)

        created_objects["bavel"] = bavel_object

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
