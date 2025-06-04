import bpy, bmesh, math, mathutils

# ─────────────────────────────────────────────────────────────
# helper: create a solid triangular prism in the X-Z plane
def create_triangle(name, pts, depth=0.05, mat=None):
    mesh = bpy.data.meshes.new(name+"_mesh")
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm   = bmesh.new()
    verts = [bm.verts.new(p) for p in pts]
    bm.faces.new(verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # give thickness by extruding along +Y
    geom = bmesh.ops.extrude_face_region(bm, geom=bm.faces)['geom']
    extruded_verts = [e for e in geom if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=extruded_verts, vec=(0, depth, 0))

    bm.to_mesh(mesh); bm.free()
    if mat: obj.data.materials.append(mat)
    return obj

# helper: small cube(s) as tick-mark(s) centred on a side
def add_tick_mark(A, B, count, mat, tick_len=0.06, tick_thk=0.01):
    vec   = mathutils.Vector((B[0]-A[0], B[2]-A[2]))       # 2-D in XZ
    mid   = mathutils.Vector(((A[0]+B[0])/2, (A[2]+B[2])/2))
    perp  = mathutils.Vector((-vec.y, vec.x)).normalized()  # 90° rotate

    for i in range(count):
        shift = (i-(count-1)/2)*0.12      # spread when ≥2 ticks
        pos2d = mid + shift*perp
        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(pos2d.x, 0.025, pos2d.y))
        cube = bpy.context.active_object
        cube.scale = (tick_thk, tick_thk, tick_len/2)
        cube.data.materials.append(mat)

# helper: yellow vertex sphere
def add_vertex_sphere(loc, mat, r=0.04):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc)
    bpy.context.active_object.data.materials.append(mat)

# helper: polyline arc between two edges at a vertex (angle marker)
def create_angle_arc(name, centre, p1, p2, radius=0.4, segs=18, mat=None):
    c = mathutils.Vector(centre)
    v1 = (mathutils.Vector(p1)-c).normalized()
    v2 = (mathutils.Vector(p2)-c).normalized()
    angle = v1.angle(v2)
    axis  = v1.cross(v2)
    if axis.length < 1e-6:
        axis = mathutils.Vector((0,1,0))
    pts = []
    for i in range(segs+1):
        t   = i/segs
        rot = mathutils.Matrix.Rotation(t*angle, 4, axis)
        pt3 = c + (rot @ v1)*radius
        pts.append((pt3.x, pt3.y+0.001, pt3.z))  # lift off face slightly

    mesh = bpy.data.meshes.new(name+"_mesh")
    mesh.from_pydata(pts, [(i,i+1) for i in range(len(pts)-1)], [])
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if mat: obj.data.materials.append(mat)
    return obj

# helper: 3-D text label that faces −Y (towards camera)
#def add_text(label, loc, mat, size=0.3):
#    bpy.ops.object.text_add(location=(loc[0], loc[1]+0.09, loc[2]))
#    txt = bpy.context.active_object
#    txt.data.body = label
#    txt.data.extrude = 0.02
#    txt.scale = (size, size, size)
#    txt.rotation_euler = (math.radians(90), 0, 0)  # stand up in XZ plane
#    txt.data.materials.append(mat)
def add_text(label, loc, mat, size=0.3):
    # Position the text a bit in front of the triangle and slightly above
    x, y, z = loc
    y_offset = -0.1     # move it towards the camera (−Y direction)
    z_offset = 0.1      # raise above the triangle surface

    bpy.ops.object.text_add(location=(x, y + y_offset, z + z_offset))
    txt = bpy.context.active_object
    txt.data.body = label
    txt.data.extrude = 0.02
    txt.scale = (size, size, size)
    txt.rotation_euler = (math.radians(90), 0, 0)  # face −Y direction
    txt.data.materials.append(mat)


# ─────────────────────────────────────────────────────────────
# clean scene
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()

# materials
def new_mat(name,col): m=bpy.data.materials.new(name); m.diffuse_color=(*col,1); return m
mat_tri  = new_mat("Purple",(0.45,0.05,0.65))
mat_tick = new_mat("Red"   ,(1.00,0.05,0.05))
mat_arc  = new_mat("Green" ,(0.10,0.85,0.10))
mat_pts  = new_mat("Yellow",(1.00,1.00,0.20))
mat_txt  = new_mat("Black" ,(0.02,0.02,0.02))

# geometry (XZ plane → upright in AR)
A=(-3.0,0,0);   B=(-1.0,0,0);   C=(-3.5,0,2.0)          # left triangle
P=( 3.0,0,0);   Q=( 1.0,0,0);   R=( 3.5,0,2.0)          # mirrored right

# build triangles
create_triangle("Triangle_ABC",[A,B,C], mat=mat_tri)
create_triangle("Triangle_PQR",[P,R,Q], mat=mat_tri)     # note mirrored order

# vertex spheres & labels
for p,label in zip([A,B,C,P,Q,R],["A","B","C","P","Q","R"]):
    add_vertex_sphere(p, mat_pts)
    add_text(label, p, mat_txt, size=0.25)

# tick marks – AB ≅ PQ (1 tick) ; AC ≅ PR (2 ticks)
add_tick_mark(A,B,1,mat_tick);   add_tick_mark(P,Q,1,mat_tick)
add_tick_mark(A,C,2,mat_tick);   add_tick_mark(P,R,2,mat_tick)

# angle arcs at ∠A and ∠P (included angle) – SAS
create_angle_arc("Arc_A", A, B, C, radius=0.6, mat=mat_arc)
create_angle_arc("Arc_P", P, Q, R, radius=0.6, mat=mat_arc)

# ─────────────────────────────────────────────────────────────
# export GLB
export_path = bpy.path.abspath("C:\\Users\\aruna\\Documents\\glb_models\\sas_congruent_triangles_use_this_one.glb")
bpy.ops.export_scene.gltf(filepath=export_path,
                          export_format='GLB',
                          export_apply=True)
print("✅ GLB exported to:", export_path)
