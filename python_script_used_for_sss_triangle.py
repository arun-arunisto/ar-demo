import bpy, bmesh, math, mathutils

# ─────────────────────────────────────────────────────
# helpers

def create_triangle(name, pts, depth=0.05, mat=None):
    mesh = bpy.data.meshes.new(name+"_mesh")
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm   = bmesh.new()
    verts = [bm.verts.new(p) for p in pts]
    bm.faces.new(verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)['geom']
    extruded_verts = [e for e in geom if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=extruded_verts, vec=(0, depth, 0))

    bm.to_mesh(mesh); bm.free()
    if mat: obj.data.materials.append(mat)
    return obj

def add_tick_mark(A, B, count, mat, tick_len=0.06, tick_thk=0.01):
    vec   = mathutils.Vector((B[0]-A[0], B[2]-A[2]))
    mid   = mathutils.Vector(((A[0]+B[0])/2, (A[2]+B[2])/2))
    perp  = mathutils.Vector((-vec.y, vec.x)).normalized()
    for i in range(count):
        shift = (i - (count - 1)/2) * 0.12
        pos2d = mid + shift * perp
        bpy.ops.mesh.primitive_cube_add(size=1,
            location=(pos2d.x, 0.025, pos2d.y))
        cube = bpy.context.active_object
        cube.scale = (tick_thk, tick_thk, tick_len/2)
        cube.data.materials.append(mat)

def add_vertex_sphere(loc, mat, r=0.04):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc)
    bpy.context.active_object.data.materials.append(mat)

def add_text(label, loc, mat, size=0.3):
    x, y, z = loc
    y_offset = -0.1     # move toward camera
    z_offset = 0.1      # raise above triangle
    bpy.ops.object.text_add(location=(x, y + y_offset, z + z_offset))
    txt = bpy.context.active_object
    txt.data.body = label
    txt.data.extrude = 0.02
    txt.scale = (size, size, size)
    txt.rotation_euler = (math.radians(90), 0, 0)
    txt.data.materials.append(mat)

# ─────────────────────────────────────────────────────
# clean scene
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

# materials
def new_mat(name, col): m = bpy.data.materials.new(name); m.diffuse_color = (*col, 1); return m
mat_tri  = new_mat("Purple", (0.5, 0.1, 0.7))
mat_tick = new_mat("Red",    (1.0, 0.2, 0.2))
mat_pts  = new_mat("Yellow", (1.0, 1.0, 0.2))
mat_txt  = new_mat("Black",  (0.02, 0.02, 0.02))

# triangle coordinates (XZ plane so they stand up in AR)
# Triangle ABC
A = (-3.0, 0, 0)
B = (-5.0, 0, 0)
C = (-4.0, 0, 2.0)

# Triangle PQR (mirrored SSS triangle)
P = (3.0, 0, 0)
Q = (5.0, 0, 0)
R = (4.0, 0, 2.0)

# create triangles
create_triangle("Triangle_ABC", [A, B, C], mat=mat_tri)
create_triangle("Triangle_PQR", [P, R, Q], mat=mat_tri)

# add vertex spheres & labels
for p, label in zip([A, B, C, P, Q, R], ["A", "B", "C", "P", "Q", "R"]):
    add_vertex_sphere(p, mat_pts)
    add_text(label, p, mat_txt, size=0.25)

# side markings (3 per triangle)
add_tick_mark(A, B, 1, mat_tick)
add_tick_mark(B, C, 2, mat_tick)
add_tick_mark(C, A, 3, mat_tick)

add_tick_mark(P, Q, 1, mat_tick)
add_tick_mark(Q, R, 2, mat_tick)
add_tick_mark(R, P, 3, mat_tick)

# ─────────────────────────────────────────────────────
# Export to GLB
export_path = bpy.path.abspath("C:\\Users\\aruna\\Documents\\glb_models\\sss_congruent_triangles_use_this_one.glb")
bpy.ops.export_scene.gltf(filepath=export_path,
                          export_format='GLB',
                          export_apply=True)
print("✅ Exported to:", export_path)
