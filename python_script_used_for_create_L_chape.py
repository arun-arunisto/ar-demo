import bpy
import os

# === CONFIG ===
output_path = r"C:\Users\aruna\Documents\glb_models\L_shape.glb"

# === CLEAN SCENE ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# === POSITIONS FOR L SHAPE ===
cube_positions = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 0, 2),
    (1, 0, 0),
]

# === CREATE CUBES ===
created_objects = []
for pos in cube_positions:
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    obj = bpy.context.active_object
    created_objects.append(obj)

# === JOIN CUBES ===
bpy.ops.object.select_all(action='DESELECT')
for obj in created_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = created_objects[0]
bpy.ops.object.join()
l_shape = bpy.context.active_object

# === CREATE MATERIAL WITH PINK COLOR ===
mat = bpy.data.materials.new(name="PinkMaterial")
mat.use_nodes = True

# Access node tree
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.9, 0.2, 0.6, 1)  # Pink RGBA

# Assign material
if len(l_shape.data.materials) == 0:
    l_shape.data.materials.append(mat)
else:
    l_shape.data.materials[0] = mat

# === EXPORT TO GLB ===
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_apply=True,
    export_materials='EXPORT'
)

print(f"✅ Exported with pink color to {output_path}")
