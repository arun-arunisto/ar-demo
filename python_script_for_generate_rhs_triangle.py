import bpy
import math
import mathutils

# 🧹 Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 📍 Triangle coordinates
A = (2, 0, 0)
B = (1, 0, 1.5)
C = (0, 0, 0)

P = (6, 0, 0)
Q = (5, 0, 0)
R = (5, 0, 1.5)

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

# 🔤 Add text label
def add_text(label, location):
    bpy.ops.object.text_add(location=location, rotation=(math.radians(90), 0, 0))
    obj = bpy.context.object
    obj.data.body = label
    obj.data.size = 0.3
    obj.data.extrude = 0.01
    obj.name = f"Text_{label}"
    return obj

# 🧱 Create right angle box
def draw_right_angle(pos, size=0.2, offset=0.01):
    verts = [
        (pos[0], pos[1], pos[2] + offset),
        (pos[0] + size, pos[1], pos[2] + offset),
        (pos[0] + size, pos[1], pos[2] + size + offset),
        (pos[0], pos[1], pos[2] + size + offset)
    ]
    edges = [(0, 1), (1, 2), (2, 3)]
    mesh = bpy.data.meshes.new('RightAngle')
    obj = bpy.data.objects.new('RightAngle', mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts, edges, [])
    return obj

def draw_right_angle_at_vertex_old_old(vertex, adj1, adj2, size=0.2, offset=0.01):
    """
    Draw a right angle box at 'vertex', oriented along vectors vertex->adj1 and vertex->adj2.
    """
    v = mathutils.Vector(vertex)
    v1 = (mathutils.Vector(adj1) - v).normalized() * size
    v2 = (mathutils.Vector(adj2) - v).normalized() * size

    # Offset slightly along Y so it doesn't z-fight with the triangle
    offset_vec = mathutils.Vector((0, offset, 0))

    verts = [
        v + offset_vec,
        v + v1 + offset_vec,
        v + v1 + v2 + offset_vec,
        v + v2 + offset_vec
    ]

    edges = [(0, 1), (1, 2), (2, 3)]

    mesh = bpy.data.meshes.new('RightAngle')
    obj = bpy.data.objects.new('RightAngle', mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts, edges, [])

    return obj

def draw_right_angle_at_vertex_old(vertex, adj1, adj2, size=0.2, offset=0.01):
    import mathutils

    v = mathutils.Vector(vertex)
    v1 = (mathutils.Vector(adj1) - v).normalized() * size
    v2 = (mathutils.Vector(adj2) - v).normalized() * size

    # Calculate normal of the triangle plane (vertex, adj1, adj2)
    normal = (mathutils.Vector(adj1) - v).cross(mathutils.Vector(adj2) - v).normalized()

    # Offset along normal instead of fixed Y axis
#    offset_vec = normal * offset
    offset_vec = mathutils.Vector((0, offset, 0))

    verts = [
        v + offset_vec,
        v + v1 + offset_vec,
        v + v1 + v2 + offset_vec,
        v + v2 + offset_vec
    ]

    edges = [(0, 1), (1, 2), (2, 3)]

    mesh = bpy.data.meshes.new('RightAngle')
    obj = bpy.data.objects.new('RightAngle', mesh)
    bpy.context.collection.objects.link(obj)
    mesh.from_pydata(verts, edges, [])
    mesh.update()

    return obj


def draw_right_angle_at_vertex(vertex, adj1, adj2, size=0.2, offset=0.01):
    def create_square(offset_dir):
        v = mathutils.Vector(vertex)
        v1 = (mathutils.Vector(adj1) - v).normalized() * size
        v2 = (mathutils.Vector(adj2) - v).normalized() * size
        offset_vec = mathutils.Vector((0, offset_dir * offset, 0))

        verts = [
            v + offset_vec,
            v + v1 + offset_vec,
            v + v1 + v2 + offset_vec,
            v + v2 + offset_vec
        ]
        edges = [(0, 1), (1, 2), (2, 3)]

        mesh = bpy.data.meshes.new('RightAngle')
        obj = bpy.data.objects.new('RightAngle', mesh)
        bpy.context.collection.objects.link(obj)
        mesh.from_pydata(verts, edges, [])
        mesh.update()
        return obj

    # ⬆️ Draw in +Y and ⬇️ in -Y
    create_square(1)
    create_square(-1)





# ➕ Create mark on side
def draw_side_mark(start, end, count=1, offset=0.01):
    mid = (
        (start[0] + end[0]) / 2,
        (start[1] + end[1]) / 2,
        (start[2] + end[2]) / 2 + offset
    )
    direction = mathutils.Vector((end[2] - start[2], 0, start[0] - end[0])).normalized() * 0.2
    for i in range(count):
        p1 = (
            mid[0] - direction.x / 2 + i * 0.05,
            mid[1],
            mid[2] - direction.z / 2 + i * 0.05
        )
        p2 = (
            mid[0] + direction.x / 2 + i * 0.05,
            mid[1],
            mid[2] + direction.z / 2 + i * 0.05
        )
        mesh = bpy.data.meshes.new('Mark')
        obj = bpy.data.objects.new('Mark', mesh)
        bpy.context.collection.objects.link(obj)
        mesh.from_pydata([p1, p2], [(0, 1)], [])

# ✨ Create triangles
create_triangle("ABC", [A, B, C], (0.6, 0.3, 0.8, 1))
create_triangle("PQR", [P, Q, R], (0.2, 0.7, 0.9, 1))

# 🔠 Add labels
add_text("A", (A[0] + 0.2, A[1], A[2]))
add_text("B", (B[0], B[1], B[2] + 0.3))
add_text("C", (C[0] - 0.3, C[1], C[2]))

add_text("P", (P[0] + 0.2, P[1], P[2]))
add_text("Q", (Q[0] - 0.3, Q[1], Q[2]))
add_text("R", (R[0], R[1], R[2] + 0.3))

# ⊾ Add right angle indicators at B and Q
#draw_right_angle((B[0], B[1], B[2]))
#draw_right_angle((Q[0], Q[1], Q[2]))

draw_right_angle_at_vertex(B, A, C)
draw_right_angle_at_vertex(Q, P, R)

# ➖ Side marks
draw_side_mark(B, C, count=2)  # Mark BC
draw_side_mark(Q, P, count=2)  # Mark QP
draw_side_mark(B, A, count=1)  # Mark AB
draw_side_mark(Q, R, count=1)  # Mark QR

# 💾 Export to GLB (Blender 4.4 compatible)
output_path = bpy.path.abspath("C:\\Users\\aruna\\Documents\\glb_models\\rhs_triangle_model.glb")
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_apply=True
)

print(f"✅ Exported successfully to: {output_path}")
