"""Minimal Blender 5.x add-on template."""

bl_info = {
    "name": "Simple_hair5",
    "author": "Your Name",
    "version": (0, 9, 0),
    "blender": (5, 0, 0),
    "location": "3D View > N Panel > Blender5Tab",
    "description": "A minimal starter add-on template for Blender 5.x",
    "category": "3D View",
}

import math

import bpy

TAB_NAME = "Blender5Tab"
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


def create_bezier_curve_object(
    name: str,
    location: tuple[float, float, float],
    target_collection: bpy.types.Collection,
) -> bpy.types.Object:
    """Create a minimal 3D Bézier curve object with two control points."""
    curve_data = bpy.data.curves.new(name=name, type="CURVE")
    curve_data.dimensions = "3D"

    spline = curve_data.splines.new(type="BEZIER")
    spline.bezier_points.add(1)

    point0 = spline.bezier_points[0]
    point1 = spline.bezier_points[1]

    point0.co = (0.0, 0.0, 0.0)
    point0.handle_left_type = "AUTO"
    point0.handle_right_type = "AUTO"

    point1.co = (0.0, 0.0, 1.0)
    point1.handle_left_type = "AUTO"
    point1.handle_right_type = "AUTO"

    curve_object = bpy.data.objects.new(name=name, object_data=curve_data)
    curve_object.location = location
    target_collection.objects.link(curve_object)
    return curve_object


def create_bezier_circle_object(
    name: str,
    location: tuple[float, float, float],
    target_collection: bpy.types.Collection,
) -> bpy.types.Object:
    """Create a Bezier circle curve object and rotate it 90 degrees on Y."""
    curve_data = bpy.data.curves.new(name=name, type="CURVE")
    curve_data.dimensions = "3D"

    spline = curve_data.splines.new(type="BEZIER")
    spline.bezier_points.add(3)

    radius = 0.5
    handle = radius * 0.5522847498
    coords = (
        (radius, 0.0, 0.0),
        (0.0, radius, 0.0),
        (-radius, 0.0, 0.0),
        (0.0, -radius, 0.0),
    )
    handles_right = (
        (radius, handle, 0.0),
        (-handle, radius, 0.0),
        (-radius, -handle, 0.0),
        (handle, -radius, 0.0),
    )
    handles_left = (
        (radius, -handle, 0.0),
        (handle, radius, 0.0),
        (-radius, handle, 0.0),
        (-handle, -radius, 0.0),
    )

    for i, point in enumerate(spline.bezier_points):
        point.co = coords[i]
        point.handle_left_type = "FREE"
        point.handle_right_type = "FREE"
        point.handle_left = handles_left[i]
        point.handle_right = handles_right[i]

    spline.use_cyclic_u = True

    curve_object = bpy.data.objects.new(name=name, object_data=curve_data)
    curve_object.location = location
    curve_object.rotation_euler[1] = math.radians(90.0)
    target_collection.objects.link(curve_object)
    return curve_object


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

            if collection_name is None:
                target_collection = active_collection
            else:
                target_collection = get_or_create_collection(collection_name)

            location = (float(index) * 1.5, 0.0, 0.0)
            if base_name == "bavel":
                created_object = create_bezier_circle_object(
                    name=object_name,
                    location=location,
                    target_collection=target_collection,
                )
            else:
                created_object = create_bezier_curve_object(
                    name=object_name,
                    location=location,
                    target_collection=target_collection,
                )

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
        layout.label(text="3D View > Nパネル > Blender5Tab")
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
