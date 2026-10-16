"""Shared procedural Blender geometry and lighting helpers. Original images remain packed textures."""
import bpy, math, random, sys, json
from pathlib import Path
from mathutils import Vector
from math import pi, sin, cos
ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
BUILD = ROOT / 'build'
BUILD.mkdir(exist_ok=True)
FPS = 30
ACT = 180
WIDTH = 768
HEIGHT = 512
random.seed(42)
bpy.ops.wm.read_factory_settings(use_empty=True)
MAT = {}

def material(name, color, metal=0, rough=0.3, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    p.inputs['Coat Weight'].default_value = 0.3
    if emission:
        p.inputs['Emission Color'].default_value = (*color, 1)
        p.inputs['Emission Strength'].default_value = emission
    MAT[name] = m
    return m
BLACK = material('Ribbed graphite', (0.006, 0.009, 0.007), 0, 0.34)
RUBBER = material('Rubber pipette', (0.009, 0.012, 0.01), 0, 0.28)
AMBER = material('Amber glass', (0.35, 0.095, 0.012), 0.22, 0.15)
LABELBACK = material('Black label reverse', (0.008, 0.014, 0.007), 0.1, 0.35)
METAL = material('Brushed dark titanium', (0.025, 0.065, 0.045), 0.8, 0.23)
FLOOR = material('Polished forest floor', (0.008, 0.023, 0.016), 0.65, 0.24)
GOLD = material('Champagne gold', (0.63, 0.36, 0.075), 0.83, 0.21)
KRAFT = material('Kraft paper sides', (0.43, 0.245, 0.095), 0, 0.7)
GREEN = material('Logo enamel', (0.11, 0.38, 0.018), 0.25, 0.24)
LIME = material('Lime plasma', (0.14, 0.8, 0.018), 0.05, 0.35, 1.8)
WARM = material('Gold plasma', (0.9, 0.36, 0.025), 0.05, 0.3, 2)
MINT = material('Mint plasma', (0.05, 0.65, 0.3), 0.05, 0.3, 1.8)
MAT['Ribbed graphite'].node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value = 0.08

def image_mat(name, file, alpha=False):
    m = material(name, (1, 1, 1), 0.02, 0.4)
    n = m.node_tree.nodes
    p = n.get('Principled BSDF')
    img = bpy.data.images.load(str(ASSETS / file), check_existing=True)
    img.pack()
    img.filepath = '//assets/' + file
    tex = n.new('ShaderNodeTexImage')
    tex.image = img
    m.node_tree.links.new(tex.outputs['Color'], p.inputs['Base Color'])
    if alpha:
        m.node_tree.links.new(tex.outputs['Alpha'], p.inputs['Alpha'])
    p.inputs['Coat Weight'].default_value = 0
    p.inputs['Specular IOR Level'].default_value = 0.18
    p.inputs['Roughness'].default_value = 0.55
    return m

def mesh(name, verts, faces, mat, uv=None, parent=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if uv:
        layer = me.uv_layers.new()
        for poly in me.polygons:
            for li in poly.loop_indices:
                layer.data[li].uv = uv[me.loops[li].vertex_index]
    if parent:
        ob.parent = parent
    return ob

def empty(name, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    return ob

def lathe(name, profile, mat, parent=None, n=96, rib=0):
    verts = []
    faces = []
    for z, r in profile:
        for i in range(n):
            a = 2 * pi * i / n
            rr = r + (rib if i % 2 == 0 else 0)
            verts.append((rr * sin(a), -rr * cos(a), z))
    for j in range(len(profile) - 1):
        for i in range(n):
            a = j * n + i
            b = j * n + (i + 1) % n
            faces.append((a, b, b + n, a + n))
    faces.extend([tuple(range(n - 1, -1, -1)), tuple(((len(profile) - 1) * n + i for i in range(n)))])
    ob = mesh(name, verts, faces, mat, parent=parent)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob

def cube(name, loc, scale, mat, parent=None, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    ob.data.materials.append(mat)
    if bevel:
        mod = ob.modifiers.new('Soft manufactured edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        ob.modifiers.new('Weighted face normals', 'WEIGHTED_NORMAL')
    if parent:
        ob.parent = parent
    return ob

def curve(name, pts, mat, r=0.025, cyclic=False, parent=None):
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    cu.resolution_u = 1
    cu.bevel_depth = r
    cu.bevel_resolution = 3
    sp = cu.splines.new('POLY')
    sp.points.add(len(pts) - 1)
    for p, co in zip(sp.points, pts):
        p.co = (*co, 1)
    sp.use_cyclic_u = cyclic
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob

def ring(name, r, mat, loc=(0, 0, 0), rot=(0, 0, 0), thick=0.025, parent=None):
    ob = curve(name, [(r * cos(i * 2 * pi / 128), r * sin(i * 2 * pi / 128), 0) for i in range(128)], mat, thick, True, parent)
    ob.location = loc
    ob.rotation_euler = rot
    return ob

def key(ob, frame, loc=None, rot=None, scale=None):
    if loc is not None:
        ob.location = loc
        ob.keyframe_insert('location', frame=frame)
    if rot is not None:
        ob.rotation_euler = rot
        ob.keyframe_insert('rotation_euler', frame=frame)
    if scale is not None:
        ob.scale = (scale,) * 3 if isinstance(scale, (float, int)) else scale
        ob.keyframe_insert('scale', frame=frame)

def sphere(name, loc, r, mat, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=r, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    if parent:
        ob.parent = parent
    return ob

def light(name, loc, power, color, size, target):
    da = bpy.data.lights.new(name, 'AREA')
    da.energy = power
    da.color = color
    da.shape = 'DISK'
    da.size = size
    ob = bpy.data.objects.new(name, da)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    ob.rotation_euler = (Vector(target) - ob.location).to_track_quat('-Z', 'Y').to_euler()
    return ob
