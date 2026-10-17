"""Add the existing, unchanged shop photograph to an independent Blender scene."""
import bpy,math
from mathutils import Vector

def replace_tea_with_vape(scene,repo):
    # Shared environment objects are read-only. Only remove links from the copied scene.
    to_remove=[]
    for ob in scene.objects:
        root=ob
        while root.parent:root=root.parent
        if root.name=='Product tee':to_remove.append(ob)
    assert to_remove,'Tea product geometry missing'
    for ob in to_remove:
        for collection in list(ob.users_collection):
            # scene.copy has a private master collection; unlinking its object keeps the original scene intact.
            if collection==scene.collection:collection.objects.unlink(ob)
    assert not any(ob in scene.objects.values() for ob in to_remove),'Copied product remained linked'
    image=bpy.data.images.load(str(repo/'ledshow-seefeld/assets/raw/vape-mesh-himbeere.png'),check_existing=True)
    image.pack()
    material=bpy.data.materials.new('Unchanged Mesh Flash photograph')
    material.use_nodes=True
    nodes=material.node_tree.nodes;links=material.node_tree.links
    p=nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.65
    p.inputs['Specular IOR Level'].default_value=.12
    tex=nodes.new('ShaderNodeTexImage');tex.image=image
    links.new(tex.outputs['Color'],p.inputs['Base Color'])
    # Pure source-white becomes transparent in the material; no source bitmap is edited.
    bw=nodes.new('ShaderNodeRGBToBW');links.new(tex.outputs['Color'],bw.inputs['Color'])
    gate=nodes.new('ShaderNodeMath');gate.operation='LESS_THAN';gate.inputs[1].default_value=.96
    links.new(bw.outputs['Val'],gate.inputs[0]);links.new(gate.outputs[0],p.inputs['Alpha'])
    material.surface_render_method='DITHERED'
    width=3.10;height=3.70
    vertices=[(-width/2,-.04,0),(width/2,-.04,0),(width/2,-.04,height),(-width/2,-.04,height)]
    mesh=bpy.data.meshes.new('Original vape photo plane');mesh.from_pydata(vertices,[],[(0,1,2,3)])
    uv=mesh.uv_layers.new()
    for loop,coord in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=coord
    ob=bpy.data.objects.new('Vape source photo',mesh);scene.collection.objects.link(ob)
    ob.data.materials.append(material)
    st,en=scene.frame_start,scene.frame_end
    for frac,z,angle in [(0,.28,-.025),(.25,.30,-.015),(.86,.38,.025),(1,.30,.035)]:
        frame=round(st+frac*(en-st));ob.location=(1.35,-.18,z);ob.rotation_euler=(0,0,angle)
        ob.keyframe_insert('location',frame=frame);ob.keyframe_insert('rotation_euler',frame=frame)
