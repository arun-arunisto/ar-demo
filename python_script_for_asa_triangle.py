import bpy
import math
import mathutils

# 📦 Clear all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 🎯 Triangle coordinates
A = (0, 0, 2)
B = (-1.5, 0, 0)
C = (1.5, 0, 0)

R = (4, 0, 2)
P = (5.5, 0, 0)
Q = (2.5, 0, 0)

# 🔺 Create triangle mesh
def create_triangle(name, verts, color):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts, [], [(0, 1, 2)])
    mat = bpy.data.materials.new(name + "_mat")
    mat.diffuse_color = color
    obj.data.materials.append(mat)
    return obj

# 🔤 Add label that faces the camera
def add_text(label, location):
    bpy.ops.object.text_add(location=location, rotation=(math.radians(90), 0, 0))  # Face camera
    obj = bpy.context.object
    obj.data.body = label
    obj.data.size = 0.3
    obj.data.extrude = 0.01
    obj.name = f"Text_{label}"
    return obj

# 🔁 Draw angle arc between two vectors
def draw_angle_arc(center, point1, point2, radius=0.3, steps=16, z_offset=0.01):
    v1 = mathutils.Vector((point1[0] - center[0], point1[1] - center[1], point1[2] - center[2]))
    v2 = mathutils.Vector((point2[0] - center[0], point2[1] - center[1], point2[2] - center[2]))
    v1.normalize()
    v2.normalize()

    angle = v1.angle(v2)
    normal = v1.cross(v2).normalized()
    start = v1 * radius

    verts = []
    for i in range(steps + 1):
        rot = mathutils.Matrix.Rotation(angle * i / steps, 4, normal)
        pt = rot @ start
        verts.append((center[0] + pt.x, center[1] + pt.y, center[2] + pt.z + z_offset))

    curve_data = bpy.data.curves.new('AngleArc', type='CURVE')
    curve_data.dimensions = '3D'
    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(verts) - 1)

    for i, coord in enumerate(verts):
        polyline.points[i].co = (coord[0], coord[1], coord[2], 1)

    curve_obj = bpy.data.objects.new('AngleArc', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    return curve_obj

# ✨ Create triangles
create_triangle("ABC", [A, B, C], (0.7, 0.2, 0.9, 1))   # Purple
create_triangle("PQR", [R, P, Q], (0.2, 0.6, 0.9, 1))   # Blue

# 🏷️ Add point labels (position tweaked for visibility)
add_text("A", (A[0], A[1], A[2] + 0.2))
add_text("B", (B[0] - 0.3, B[1], B[2]))
add_text("C", (C[0] + 0.2, C[1], C[2]))

add_text("R", (R[0], R[1], R[2] + 0.2))
add_text("P", (P[0] + 0.2, P[1], P[2]))
add_text("Q", (Q[0] - 0.3, Q[1], Q[2]))

# 🎯 Draw internal angle arcs
draw_angle_arc(A, B, C)
draw_angle_arc(C, A, B)
draw_angle_arc(R, Q, P)
draw_angle_arc(P, R, Q)

# 💾 Export to GLB file
output_path = bpy.path.abspath("C:\\Users\\aruna\\Documents\\glb_models\\asa_triangle_model.glb")
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_apply=True
)

print(f"✅ Model exported successfully to: {output_path}")
