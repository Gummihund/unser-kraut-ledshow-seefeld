"""Blender 4.5 LTS. Five fully animated 3D scenes, packed original textures.
Build: blender -b --python build_show.py -- --stills
Render: blender -b UNSER_KRAUT_3D.blend --python render_frames.py
Dimensions are artistic reconstructions from packshots, not manufacturer CAD.
"""
import bpy, math, random, sys, json
from pathlib import Path
from mathutils import Vector
from math import pi, sin, cos

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
BUILD=ROOT/'build'
BUILD.mkdir(exist_ok=True)
FPS=30;ACT=180;WIDTH=768;HEIGHT=512
random.seed(42)
bpy.ops.wm.read_factory_settings(use_empty=True)
MAT={}

def material(name,color,metal=0,rough=.3,emission=0):
    m=bpy.data.materials.new(name);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    p.inputs['Coat Weight'].default_value=.3
    if emission:
        p.inputs['Emission Color'].default_value=(*color,1)
        p.inputs['Emission Strength'].default_value=emission
    MAT[name]=m;return m

BLACK=material('Ribbed graphite',(0.006,.009,.007),0,.34)
RUBBER=material('Rubber pipette',(.009,.012,.01),0,.28)
AMBER=material('Amber glass',(.35,.095,.012),.22,.15)
LABELBACK=material('Black label reverse',(.008,.014,.007),.1,.35)
METAL=material('Brushed dark titanium',(.025,.065,.045),.8,.23)
FLOOR=material('Polished forest floor',(.008,.023,.016),.65,.24)
GOLD=material('Champagne gold',(.63,.36,.075),.83,.21)
KRAFT=material('Kraft paper sides',(.43,.245,.095),0,.7)
GREEN=material('Logo enamel',(.11,.38,.018),.25,.24)
LIME=material('Lime plasma',(.14,.8,.018),.05,.35,1.8)
WARM=material('Gold plasma',(.9,.36,.025),.05,.3,2)
MINT=material('Mint plasma',(.05,.65,.3),.05,.3,1.8)
MAT['Ribbed graphite'].node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value=.08

def image_mat(name,file,alpha=False):
    m=material(name,(1,1,1),.02,.4)
    n=m.node_tree.nodes;p=n.get('Principled BSDF')
    img=bpy.data.images.load(str(ASSETS/file),check_existing=True);img.pack();img.filepath='//assets/'+file
    tex=n.new('ShaderNodeTexImage');tex.image=img
    m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
    if alpha:m.node_tree.links.new(tex.outputs['Alpha'],p.inputs['Alpha'])
    p.inputs['Coat Weight'].default_value=0
    p.inputs['Specular IOR Level'].default_value=.18
    p.inputs['Roughness'].default_value=.55
    return m

CBD=image_mat('Original Unser Kraut 10 percent label','cbd-label.png')
TEA=image_mat('Original Hanfblaetter Tee front','tee.png',True)
CHOCO=image_mat('Original Seefeld chocolate front','schoko.png',True)
LOGO=image_mat('Original Unser Kraut logo','brand-original.png',True)

def mesh(name,verts,faces,mat,uv=None,parent=None):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat)
    if uv:
        layer=me.uv_layers.new()
        for poly in me.polygons:
            for li in poly.loop_indices:layer.data[li].uv=uv[me.loops[li].vertex_index]
    if parent:ob.parent=parent
    return ob

def empty(name,loc=(0,0,0)):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob.location=loc;return ob

def lathe(name,profile,mat,parent=None,n=96,rib=0):
    verts=[];faces=[]
    for z,r in profile:
        for i in range(n):
            a=2*pi*i/n;rr=r+(rib if i%2==0 else 0)
            verts.append((rr*sin(a),-rr*cos(a),z))
    for j in range(len(profile)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
    faces.extend([tuple(range(n-1,-1,-1)),tuple((len(profile)-1)*n+i for i in range(n))])
    ob=mesh(name,verts,faces,mat,parent=parent)
    for p in ob.data.polygons:p.use_smooth=True
    return ob

def cube(name,loc,scale,mat,parent=None,bevel=.08):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    ob=bpy.context.object;ob.name=name;ob.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    ob.data.materials.append(mat)
    if bevel:
        mod=ob.modifiers.new('Soft manufactured edges','BEVEL');mod.width=bevel;mod.segments=3
        ob.modifiers.new('Weighted face normals','WEIGHTED_NORMAL')
    if parent:ob.parent=parent
    return ob

def curve(name,pts,mat,r=.025,cyclic=False,parent=None):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1
    cu.bevel_depth=r;cu.bevel_resolution=3
    sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts):p.co=(*co,1)
    sp.use_cyclic_u=cyclic
    ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
    if parent:ob.parent=parent
    return ob

def ring(name,r,mat,loc=(0,0,0),rot=(0,0,0),thick=.025,parent=None):
    ob=curve(name,[(r*cos(i*2*pi/128),r*sin(i*2*pi/128),0) for i in range(128)],mat,thick,True,parent)
    ob.location=loc;ob.rotation_euler=rot;return ob

def key(ob,frame,loc=None,rot=None,scale=None):
    if loc is not None:ob.location=loc;ob.keyframe_insert('location',frame=frame)
    if rot is not None:ob.rotation_euler=rot;ob.keyframe_insert('rotation_euler',frame=frame)
    if scale is not None:ob.scale=(scale,)*3 if isinstance(scale,(float,int)) else scale;ob.keyframe_insert('scale',frame=frame)

def bottle(name='CBD oil 10 percent'):
    root=empty(name)
    lathe('Amber glass bottle',[(.04,.36),(.08,.48),(.17,.53),(1.56,.53),(1.70,.49),(1.88,.34),(2.05,.29),(2.21,.29)],AMBER,root)
    lathe('Original black screw cap',[(2.05,.34),(2.09,.38),(2.19,.38),(2.20,.35),(2.62,.35),(2.66,.33)],BLACK,root,n=128,rib=.012)
    lathe('Soft pipette bulb',[(2.62,.26),(2.72,.22),(3.10,.22),(3.23,.18),(3.30,.10),(3.32,.025)],RUBBER,root)
    # The front is a curved mesh, not a billboard. Back remains plain black.
    lathe('Plain wrap label back',[(.20,.534),(1.58,.534)],LABELBACK,root)
    vs=[];uv=[]
    for row,z in enumerate([.20,1.58]):
        for i in range(65):
            a=-1.48+2.96*i/64
            vs.append((.538*sin(a),-.538*cos(a),z));uv.append((i/64,row))
    mesh('Photographic label on curved 3D surface',vs,[(i,i+1,i+66,i+65) for i in range(64)],CBD,uv,root)
    return root

def front_plane(name,w,h,depth,mat,parent):
    return mesh(name,[(-w/2,-depth,0),(w/2,-depth,0),(w/2,-depth,h),(-w/2,-depth,h)],[(0,1,2,3)],mat,[(0,0),(1,0),(1,1),(0,1)],parent)

def pouch():
    root=empty('Hanftee dimensional pouch')
    cube('Solid kraft pouch', (0,0,1.22),(1.55,.34,2.44),KRAFT,root,.13)
    front_plane('Original photographic pouch front',1.61,2.50,.183,TEA,root)
    cube('Top heat seal',(0,-.003,2.40),(1.44,.355,.065),KRAFT,root,.02)
    return root

def chocolate():
    root=empty('Seefeld Edition chocolate')
    cube('Dimensional gold foil package',(0,0,1.2),(1.0,.18,2.4),GOLD,root,.035)
    front_plane('Original chocolate packaging photo',1.03,2.43,.101,CHOCO,root)
    return root

def sphere(name,loc,r,mat,parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=r,location=loc)
    ob=bpy.context.object;ob.name=name;ob.data.materials.append(mat)
    for p in ob.data.polygons:p.use_smooth=True
    if parent:ob.parent=parent
    return ob

def light(name,loc,power,color,size,target):
    da=bpy.data.lights.new(name,'AREA');da.energy=power;da.color=color;da.shape='DISK';da.size=size
    ob=bpy.data.objects.new(name,da);bpy.context.collection.objects.link(ob);ob.location=loc
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob

def setup_scene(name,idx,color):
    scene=bpy.data.scenes.new(name);bpy.context.window.scene=scene
    scene.render.engine='BLENDER_EEVEE_NEXT'
    scene.render.resolution_x=WIDTH;scene.render.resolution_y=HEIGHT;scene.render.resolution_percentage=100
    scene.render.fps=FPS;scene.frame_start=idx*ACT+1;scene.frame_end=(idx+1)*ACT
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
    scene.render.filepath='//build/frames/frame_'
    scene.render.film_transparent=False
    scene.render.use_file_extension=True
    scene.view_settings.view_transform='AgX'
    try:scene.view_settings.look='AgX - Medium High Contrast'
    except Exception:pass
    scene.view_settings.exposure=-.25
    if hasattr(scene,'eevee'):
        scene.eevee.taa_render_samples=24
        scene.eevee.use_raytracing=False
    world=bpy.data.worlds.new(name+' World');scene.world=world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs[0].default_value=(.012,.025,.016,1)
    world.node_tree.nodes['Background'].inputs[1].default_value=.23
    scene.use_nodes=True;n=scene.node_tree.nodes;n.clear()
    rl=n.new('CompositorNodeRLayers');rl.scene=scene
    gl=n.new('CompositorNodeGlare');gl.glare_type='FOG_GLOW';gl.quality='MEDIUM';gl.threshold=1.3
    out=n.new('CompositorNodeComposite');scene.node_tree.links.new(rl.outputs['Image'],gl.inputs['Image']);scene.node_tree.links.new(gl.outputs['Image'],out.inputs['Image'])
    # Background tunnel: real nested 3D portal frames receding into depth.
    for j in range(5 if idx==2 else 8):
        r=2.45+j*.10;y=1.5+j*1.25
        if idx==3:
            for rr,ma,th in [(r,METAL,.07),(r-.08,WARM,.014)]:
                curve('Gold architectural tunnel',[(1.1-rr,y,1.6-rr),(1.1+rr,y,1.6-rr),(1.1+rr,y,1.6+rr),(1.1-rr,y,1.6+rr)],ma,th,True)
        elif idx==2:
            pts=[]
            for k in range(160):
                a=2*pi*k/160;rr=r*(1+.09*cos(5*a))
                pts.append((1.1+rr*cos(a),y,1.6+rr*sin(a)))
            curve('Botanical petal portal',pts,LIME,.016,True)
        else:
            ring('Receding portal '+str(j),r,METAL,(1.1,y,1.6),(pi/2,0,0),.08)
            ring('Portal inner light '+str(j),r-.08,LIME,(1.1,y-.03,1.6),(pi/2,0,0),.012)
    cube('Reflective stage floor',(0,1,-.26),(32,32,.3),FLOOR,None,.02)
    # Product platform is actual bevelled geometry.
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=2.0,depth=.22,location=(1.15,0,-.02))
    platform=bpy.context.object;platform.name='Floating machined pedestal';platform.data.materials.append(METAL)
    mod=platform.modifiers.new('Machined bevel','BEVEL');mod.width=.10;mod.segments=3
    platform.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    for r in (1.72,1.93):ring('Pedestal light',r,color,(1.15,0,.103),thick=.019)
    light('Soft key',(-3.5,-4.5,6.5),500,(.84,1,.80),5,(1.2,0,1.6))
    light('Warm rim',(4.0,2.8,4.8),700,(1,.62,.23),3,(1.2,0,1.8))
    light('Front label fill',(1.5,-6,2.5),350,(1,.98,.86),3,(1.1,0,1.4))
    light('Emerald edge',(-2,1.5,3.8),300,(.20,1,.24),3,(1.1,0,1.5))
    camera_data=bpy.data.cameras.new(name+' Camera');cam=bpy.data.objects.new('Cinematic camera',camera_data);scene.collection.objects.link(cam);scene.camera=cam
    camera_data.lens=48;camera_data.clip_end=120
    camera_data.dof.use_dof=False
    # Animate real dolly/orbit moves with controlled readability during the hold.
    start=scene.frame_start
    positions=[(-.60,-10.1,3.8),(.7,-9.5,3.15),(1.2,-9.4,2.9),(.1,-10.2,3.35)]
    for f,pos in zip([start,start+38,start+140,start+179],positions):
        target=Vector((.0,.0,1.75))
        key(cam,f,loc=pos,rot=(target-Vector(pos)).to_track_quat('-Z','Y').to_euler())
    return scene

def sparks(scene,mat,count=42):
    root=empty('Orbiting particle constellation',(1.15,0,1.65))
    for i in range(count):
        a=2*pi*i/count;r=random.uniform(1.5,2.5)
        sphere('Luminous particle '+str(i),(r*cos(a),random.uniform(-.2,1.6),r*sin(a)*.85),random.uniform(.012,.045),mat,root)
    st=scene.frame_start
    key(root,st,rot=(0,0,0));key(root,st+179,rot=(0,pi*.5,.35))
    return root

def trails(scene,mat):
    st=scene.frame_start
    for j in range(3):
        root=empty('Rotating 3D energy orbit '+str(j),(1.15,2.15,1.7))
        pts=[]
        for i in range(121):
            a=(i/120)*pi*1.7;r=1.65+j*.20
            pts.append((r*cos(a),r*sin(a),.18*sin(a*2)))
        curve('Plasma arc',pts,mat,.018,parent=root)
        sphere('Arc core',pts[-1],.05,mat,root)
        key(root,st,rot=(.9+j*.4,.15*j,j*1.2))
        key(root,st+179,rot=(.9+j*.4,.15*j+1.0,j*1.2+2.6))

def leaf(name,parent):
    # Stylized geometric botanical leaves, not replacement product photography.
    verts=[(0,0,0),(.16,0,.25),(0,.05,.85),(-.16,0,.25)]
    ob=mesh(name,verts,[(0,1,2),(0,2,3)],GREEN,parent=parent)
    sol=ob.modifiers.new('Leaf thickness','SOLIDIFY');sol.thickness=.018
    return ob

scenes=[]
sc=setup_scene('01_EMERALD_REVEAL',0,LIME);scenes.append(sc)
hero=bottle();st=sc.frame_start
for f,loc,rot,scale in [(st,(1.15,.2,.5),(.2,0,-.65),.05),(st+35,(1.15,0,.35),(.05,-.05,.10),1.04),(st+95,(1.15,0,.42),(.04,.04,-.06),1.06),(st+155,(1.15,0,.35),(0,0,.05),1.04),(st+179,(1.15,0,.5),(0,.02,.3),1.03)]:key(hero,f,loc,rot,scale)
trails(sc,LIME);sparks(sc,LIME)

sc=setup_scene('02_OIL_CONSTELLATION',1,MINT);scenes.append(sc);st=sc.frame_start
for i,(x,y,z,scale) in enumerate([(-.1,.65,.5,.76),(1.2,-.15,.35,1.02),(2.55,.6,.65,.76)]):
    ob=bottle('Unser Kraut oil model '+str(i))
    key(ob,st,loc=(x,y,5+i),rot=(.1,.4,.7-i*.5),scale=scale)
    key(ob,st+38,loc=(x,y,z),rot=(.04,-.08,(-.10+i*.1)),scale=scale)
    key(ob,st+138,loc=(x,y,z+.13),rot=(-.03,.08,.12-i*.08),scale=scale)
    key(ob,st+179,loc=(x,y,z),rot=(0,0,-.1+i*.1),scale=scale)
trails(sc,MINT);sparks(sc,MINT,30)

sc=setup_scene('03_BOTANICAL_TEA',2,LIME);scenes.append(sc);st=sc.frame_start
ob=pouch()
key(ob,st,loc=(1.2,0,1.3),rot=(0,0,-.8),scale=.05)
key(ob,st+36,loc=(1.2,0,.45),rot=(.05,0,-.08),scale=1.2)
key(ob,st+140,loc=(1.2,0,.6),rot=(-.05,.04,.12),scale=1.2)
key(ob,st+179,loc=(1.2,0,.45),rot=(.05,0,.2),scale=1.2)
for i in range(18):
    a=2*pi*i/18
    root=empty('Botanical orbit '+str(i),(1.15,0,1.8))
    l=leaf('Sculpted botanical leaf',root);l.location=(2.05*cos(a),.8*sin(a),1.5*sin(a));l.rotation_euler=(.2,a,-a)
    key(root,st,rot=(0,.0,0));key(root,st+179,rot=(.25,.5,1.2))
trails(sc,LIME);sparks(sc,LIME,30)

sc=setup_scene('04_GOLD_CHOCOLATE',3,WARM);scenes.append(sc);st=sc.frame_start
for i in range(3):
    ob=chocolate();x=1.15+(i-1)*.9
    key(ob,st,loc=(1.15,.4,1.2),rot=(0,0,(i-1)*1.5),scale=.04)
    key(ob,st+40,loc=(x,abs(i-1)*.35,.5+(.2 if i==1 else 0)),rot=(0,-.1,(i-1)*-.20),scale=1.10)
    key(ob,st+135,loc=(x,abs(i-1)*.35,.65+(.2 if i==1 else 0)),rot=(.03,.08,(i-1)*-.20),scale=1.10)
    key(ob,st+179,loc=(x,abs(i-1)*.35,.5),rot=(0,-.1,(i-1)*-.25),scale=1.10)
for i in range(14):
    a=2*pi*i/14;r=random.uniform(1.8,2.7)
    ob=cube('Floating gold shard',(1.15+r*cos(a),random.uniform(.1,1.2),1.7+r*sin(a)*.7),(.12,.12,.12),GOLD,bevel=.025)
    p=tuple(ob.location)
    key(ob,st,loc=p,rot=(0,0,0));key(ob,st+179,loc=(p[0],p[1],p[2]+.25),rot=(2,3,1))
trails(sc,WARM);sparks(sc,WARM,40)

sc=setup_scene('05_BRAND_PORTAL',4,LIME);scenes.append(sc);st=sc.frame_start
coin=empty('Rotating Unser Kraut brand medallion',(1.15,0,1.9))
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1.25,depth=.14,rotation=(pi/2,0,0))
ob=bpy.context.object;ob.name='Solid gold brand medallion';ob.data.materials.append(GOLD);ob.parent=coin
front_plane('Original logo on enamel',2.62,2.62,.082,LOGO,coin).location.z=-1.31
ring('Medallion luminous rim',1.25,LIME,(0,-.09,0),(pi/2,0,0),.025,coin)
key(coin,st,loc=(1.15,0,1.95),rot=(0,0,-1.4),scale=.04)
key(coin,st+43,loc=(1.15,0,1.95),rot=(0,0,.12),scale=1.08)
key(coin,st+138,loc=(1.15,0,2.05),rot=(0,0,-.10),scale=1.08)
key(coin,st+179,loc=(1.15,0,1.95),rot=(0,0,0),scale=1.08)
trails(sc,LIME);sparks(sc,LIME,50)

# Remove factory placeholder scene, pack dependencies, save an editable project.
for scene in list(bpy.data.scenes):
    if scene not in scenes:bpy.data.scenes.remove(scene)
bpy.context.window.scene=scenes[0]
for sc in scenes:
    sc.frame_set(sc.frame_start+85)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'UNSER_KRAUT_3D.blend'))
(ROOT/'scene_manifest.json').write_text(json.dumps({'blender':bpy.app.version_string,'fps':FPS,'frames':ACT*len(scenes),'duration_seconds':ACT*len(scenes)/FPS,'master_resolution':[WIDTH,HEIGHT],'scenes':[s.name for s in scenes],'model_note':'Artistic packaging reconstructions from original packshots. Original front label textures, plain unseen reverse.'},indent=2),encoding='utf-8')
print('PROJECT_SAVED',flush=True)
if '--stills' in sys.argv:
    (BUILD/'stills').mkdir(exist_ok=True)
    for sc in scenes:
        bpy.context.window.scene=sc;sc.frame_set(sc.frame_start+85)
        sc.render.filepath=str(BUILD/'stills'/(sc.name+'.png'))
        bpy.ops.render.render(write_still=True,scene=sc.name)
    print('STILLS_DONE',flush=True)
