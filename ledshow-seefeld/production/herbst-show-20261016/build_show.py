"""54 original cards, unchanged copy and timing, new procedural Blender scenes.
blender -b --python build_show.py -- --stills
"""
import sys,json,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from engine import *
from mathutils import Vector
STORY=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
CAT=json.loads((ROOT/'asset_catalog.json').read_text(encoding='utf-8'))
BUILD=ROOT/'build';BUILD.mkdir(exist_ok=True)
random.seed(261016)
W,H=768,512
THEMES={
 'brand':((.18,.85,.035),'round'), 'oil':((.20,.95,.03),'helix'),
 'care':((.12,.65,.5),'columns'), 'pets':((.10,.55,.8),'round'),
 'food':((.65,.60,.07),'petal'), 'gold':((.85,.38,.035),'square'),
 'active':((.40,.85,.035),'square'), 'balance':((.55,.20,.65),'petal'),
 'relief':((.08,.6,.65),'helix'), 'tea':((.18,.65,.035),'petal'),
 'night':((.10,.20,.70),'round'), 'gift':((.60,.18,.60),'diamond')}
EMIT={theme:material('Theme light '+theme,c,0,.35,1.65) for theme,(c,_) in THEMES.items()}
PHOTO={}
WHITE=material('Natural white packaging',(.78,.80,.76),0,.4)

def oil_bottle(key,height):
    actor=empty('Animated oil '+key);root=empty('Dimensional oil model');root.parent=actor;root.scale=(height/3.32,)*3
    lathe('Amber bottle',[(.04,.36),(.08,.48),(.17,.53),(1.56,.53),(1.70,.49),(1.88,.34),(2.05,.29),(2.21,.29)],AMBER,root)
    lathe('Ribbed cap',[(2.05,.34),(2.09,.38),(2.19,.38),(2.20,.35),(2.62,.35),(2.66,.33)],BLACK,root,n=96,rib=.012)
    lathe('Rounded rubber dropper',[(2.62,.26),(2.72,.22),(3.10,.22),(3.23,.18),(3.30,.10),(3.32,.025)],RUBBER,root)
    lathe('Label rear',[(.20,.534),(1.58,.534)],LABELBACK,root)
    m=image_mat('Original curved oil label '+key,key+'_label.png')
    vs=[];uv=[]
    for row,z in enumerate([.20,1.58]):
        for j in range(49):
            a=-1.48+2.96*j/48;vs.append((.538*sin(a),-.538*cos(a),z));uv.append((j/48,row))
    mesh('Curved original label',vs,[(j,j+1,j+50,j+49) for j in range(48)],m,uv,root)
    return actor

def photo_material(key):
    if key in PHOTO:return PHOTO[key]
    spec=CAT[key]
    m=image_mat('Original texture '+key,spec['file'],True)
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.46
    p.inputs['Specular IOR Level'].default_value=.14
    if spec['green_key']:
        n=m.node_tree.nodes;links=m.node_tree.links
        tex=next(x for x in n if x.type=='TEX_IMAGE')
        dis=n.new('ShaderNodeVectorMath');dis.operation='DISTANCE'
        def lin(x):return x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4
        dis.inputs[1].default_value=tuple(lin(x/255) for x in (19,50,37))
        links.new(tex.outputs['Color'],dis.inputs[0])
        gate=n.new('ShaderNodeMath');gate.operation='GREATER_THAN';gate.inputs[1].default_value=.013
        links.new(dis.outputs['Value'],gate.inputs[0]);links.new(gate.outputs[0],p.inputs['Alpha'])
    PHOTO[key]=m;return m

def plate(key,height=2.5):
    if key in ['cbd10','cbd5','cbd20','cbd40','nacht','entlastung','tier5','tier10']:return oil_bottle(key,height)
    spec=CAT[key];aspect=spec['size'][0]/spec['size'][1];maxwidth=5.6 if key in ['schoko_group','closing_original','bio_badges'] else 2.9
    width=min(maxwidth,height*aspect);height=width/aspect;kind=spec['kind']
    root=empty('Product '+key)
    mat=photo_material(key)
    if kind in ['panel','graphic','coin']:
        if kind in ['panel','coin']:
            if kind=='coin':
                bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=width*.48,depth=.15,rotation=(pi/2,0,0),location=(0,0,height/2))
                back=bpy.context.object;back.name='Solid brand medallion';back.data.materials.append(GOLD);back.parent=root
            else:cube('Photo gallery depth',(0,.08,height/2),(width+.055,.14,height+.055),METAL,root,.04)
        front_y=-.105 if kind=='coin' else -.02
        mesh('Unchanged source photograph '+key,[(-width/2,front_y,0),(width/2,front_y,0),(width/2,front_y,height),(-width/2,front_y,height)],[(0,1,2,3)],mat,[(0,0),(1,0),(1,1),(0,1)],root)
        if kind=='panel':
            curve('Fine gold photo frame',[(-width/2-.028,-.025,-.025),(width/2+.028,-.025,-.025),(width/2+.028,-.025,height+.025),(-width/2-.028,-.025,height+.025)],GOLD,.012,True,root)
        return root
    if kind=='dropper':
        profile=[(0,.36),(.03,.47),(.08,.5),(.47,.5),(.52,.46),(.60,.30),(.63,.30),(.635,.37),(.79,.37),(.82,.24),(.95,.23),(.985,.14),(1,.025)]
        depth=width*.36;side=AMBER
    elif kind=='jar':
        profile=[(0,.40),(.025,.47),(.08,.5),(.76,.5),(.82,.45),(.85,.43),(.86,.49),(.98,.49),(1,.43)]
        depth=width*.32;side=AMBER if key not in ['protein','samen'] else KRAFT
    elif key=='pflege':
        profile=[(0,.43),(.02,.49),(.78,.5),(.80,.48),(.82,.46),(.98,.46),(1,.40)]
        depth=width*.25;side=WHITE
    elif kind=='tube':
        profile=[(0,.29),(.02,.34),(.15,.34),(.20,.37),(.90,.48),(.99,.5),(1,.49)]
        depth=width*.16;side=GREEN
    else:
        profile=[(0,.43),(.03,.46),(.15,.47),(.89,.50),(.98,.49),(1,.46)]
        depth=width*.15;side=KRAFT
    verts=[];uv=[];faces=[];cols=18
    for z,r in profile:
        for j in range(cols+1):
            u=j/cols;xx=(u*2-1)*r*width
            yy=-depth*math.sqrt(max(0,1-(u*2-1)**2))
            verts.append((xx,yy,z*height));uv.append((xx/width+.5,z))
    for k in range(len(profile)-1):
        for j in range(cols):
            q=k*(cols+1)+j;faces.append((q,q+1,q+cols+2,q+cols+1))
    front=mesh('Curved photographic product surface '+key,verts,faces,mat,uv,root)
    for p in front.data.polygons:p.use_smooth=True
    # A volumetric rear shell gives the original photographic face actual depth.
    boundary=[k*(cols+1) for k in range(len(profile))]+[(len(profile)-1)*(cols+1)+j for j in range(1,cols+1)]+[k*(cols+1)+cols for k in range(len(profile)-2,-1,-1)]+[j for j in range(cols-1,0,-1)]
    shell=[verts[i] for i in boundary]+[(verts[i][0],depth*.45,verts[i][2]) for i in boundary]
    n=len(boundary);sf=[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]+[tuple(range(n,2*n))]
    mesh('Dimensional product reverse '+key,shell,sf,side,parent=root)
    return root

def star(name,loc,size,mat):
    pts=[]
    for k in range(10):
        a=pi/2+k*pi/5;r=size if k%2==0 else size*.46
        pts.append((r*cos(a),0,r*sin(a)))
    ob=mesh(name,pts,[tuple(range(10))],mat)
    so=ob.modifiers.new('Star thickness','SOLIDIFY');so.thickness=.09
    be=ob.modifiers.new('Star bevel','BEVEL');be.width=.025;be.segments=2
    ob.location=loc;return ob

def botanical_leaf():
    root=empty('Sculpted botanical hemp leaf')
    for i,(angle,length) in enumerate([(-1.18,.80),(-.80,1.25),(-.40,1.60),(0,1.85),(.40,1.60),(.80,1.25),(1.18,.80)]):
        tips=[(0,0,0)]
        for j in range(1,8):
            t=j/8;w=sin(pi*t)*.13*(1.2 if j%2 else .65)
            tips.append((w,0,t*length))
        tips.append((0,0,length))
        for j in range(7,0,-1):
            t=j/8;w=sin(pi*t)*.13*(1.2 if j%2 else .65)
            tips.append((-w,0,t*length))
        ob=mesh('Serrated hemp leaflet',tips,[tuple(range(len(tips)))],GREEN,parent=root)
        ob.rotation_euler.y=angle
        sol=ob.modifiers.new('Living leaf thickness','SOLIDIFY');sol.thickness=.018
        curve('Leaf vein',[(0,-.016,0),(0,-.016,length)],GOLD,.008,parent=ob)
    return root

def setup(card):
    num=card['id'];theme=card['theme'];color,style=THEMES[theme];emit=EMIT[theme]
    sc=bpy.data.scenes.new(f'{num:02d}_{theme.upper()}');bpy.context.window.scene=sc
    sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=W;sc.render.resolution_y=H;sc.render.resolution_percentage=100;sc.render.fps=30
    sc.frame_start=card['first_frame'];sc.frame_end=card['last_frame'];sc.render.filepath='//build/frames/frame_'
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB';sc.render.image_settings.compression=20
    sc.eevee.taa_render_samples=12;sc.eevee.use_raytracing=False
    sc.view_settings.view_transform='AgX';sc.view_settings.exposure=-.20
    try:sc.view_settings.look='AgX - Medium High Contrast'
    except Exception:pass
    world=bpy.data.worlds.new(sc.name+' atmosphere');world.use_nodes=True;sc.world=world
    world.node_tree.nodes['Background'].inputs[0].default_value=(.01,.018,.013,1);world.node_tree.nodes['Background'].inputs[1].default_value=.22
    sc.use_nodes=True;nodes=sc.node_tree.nodes;nodes.clear()
    rl=nodes.new('CompositorNodeRLayers');rl.scene=sc
    glare=nodes.new('CompositorNodeGlare');glare.glare_type='FOG_GLOW';glare.quality='MEDIUM';glare.threshold=1.4
    comp=nodes.new('CompositorNodeComposite');sc.node_tree.links.new(rl.outputs['Image'],glare.inputs['Image']);sc.node_tree.links.new(glare.outputs['Image'],comp.inputs['Image'])
    wide=len(card['assets'])>3 or not card['lines'] or card['assets'] in [['closing_original'],['bio_badges']]
    textonly=not card['assets']
    center=0 if wide or textonly or card['assets']==['stars'] else 1.35
    # Architectural depth varies with the product family.
    for j in range(5):
        rr=2.25+j*.18;y=1.8+j*1.2;z=1.7
        if style in ['square','diamond']:
            pts=[(-rr,-rr),(rr,-rr),(rr,rr),(-rr,rr)]
            if style=='diamond':pts=[(0,-rr*1.2),(rr*1.2,0),(0,rr*1.2),(-rr*1.2,0)]
            curve('Architectural depth',[(center+x,y,z+zz) for x,zz in pts],emit,.015 if j else .026,True)
        elif style=='columns':
            for side in [-1,1]:
                cube('Mint architectural fin',(center+side*rr,y,z),(.045,.08,4.4),METAL,None,.015)
                curve('Light seam',[(center+side*rr,y-.05,-.25),(center+side*rr,y-.05,3.8)],emit,.019)
        else:
            pts=[]
            for k in range(100):
                a=2*pi*k/100;r=rr*(1+.075*cos(5*a)) if style=='petal' else rr
                pts.append((center+r*cos(a),y,z+r*sin(a)))
            curve('Deep luminous portal',pts,emit,.015 if j else .022,True)
    floor=FLOOR
    cube('Reflective floor',(0,1,-.24),(24,24,.24),floor,None,.01)
    if not textonly:
        radius=2.3 if wide else 1.7
        bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=.17,location=(center,0,-.02))
        ob=bpy.context.object;ob.name='Floating product stage';ob.data.materials.append(METAL)
        bevel=ob.modifiers.new('Stage soft rim','BEVEL');bevel.width=.075;bevel.segments=2
        ring('Stage luminous lip',radius-.07,emit,(center,0,.08),thick=.018)
    st,en=sc.frame_start,sc.frame_end
    orbit=empty('Orbiting light sculpture',(center,1.4,1.8))
    pts=[]
    for j in range(160):
        a=j/159*pi*3.6;r=1.6+.1*sin(a*3)
        pts.append((r*cos(a),.7*sin(a),1.2*sin(a*.55)))
    curve('Floating energy helix',pts,emit,.016,parent=orbit)
    key(orbit,st,rot=(.1,.2,num*.13));key(orbit,en,rot=(.35,.5,num*.13+.8))
    dust=empty('Volumetric particle orbit',(center,0,1.7))
    for j in range(20):
        a=random.random()*2*pi;r=random.uniform(1.4,2.8)
        sphere('Floating light mote',(r*cos(a),random.uniform(.3,2.0),r*sin(a)*.7),random.uniform(.015,.035),emit,dust)
    key(dust,st,rot=(0,0,0));key(dust,en,rot=(0,.35,.55))
    light('Softbox',(-3,-4,6),500,(.85,1,.85),5,(center,0,1.6))
    light('Warm contour',(4,2,4.5),650,(1,.65,.27),3,(center,0,1.5))
    light('Label soft fill',(0,-5,3),300,(1,1,.94),4,(center,0,1.5))
    light('Colored edge',(-2,1,3.8),250,tuple(min(1,c*1.8+.1) for c in color),3,(center,0,1.5))
    cd=bpy.data.cameras.new('Dolly camera '+str(num));cam=bpy.data.objects.new('Camera',cd);sc.collection.objects.link(cam);sc.camera=cam
    cd.lens=48;cd.clip_end=80
    for t,pos in [(0,(-.5,-10.3,3.5)),(.25,(.2,-9.6,3.15)),(.78,(.8,-9.6,2.95)),(1,(.0,-10.0,3.25))]:
        f=round(st+t*(en-st));target=Vector((0,0,1.6))
        key(cam,f,loc=pos,rot=(target-Vector(pos)).to_track_quat('-Z','Y').to_euler())
    return sc,center

SCENES=[]
for card in STORY['cards']:
    sc,center=setup(card);SCENES.append(sc)
    st,en=sc.frame_start,sc.frame_end;dur=en-st
    assets=card['assets']
    if assets==['stars']:
        for i in range(5):
            ob=star('Five supplied rating stars',((i-2)*.75,.2,2.9),.27,GOLD)
            key(ob,st,rot=(0,0,-.25));key(ob,en,rot=(0,.2,.2))
    for k,asset in enumerate(assets):
        if asset=='stars':continue
        n=len(assets);wide=n>3 or not card['lines'] or assets in [['closing_original'],['bio_badges']]
        if asset=='leaf':ob=botanical_leaf();height=2.4
        else:
            height=3.0 if n==1 else (2.15 if n>3 else 2.5)
            if asset in ['schoko_group','closing_original']:height=3.45
            if asset=='bio_badges':height=2.0
            if asset=='pfoten':height=1.12
            if card['id']==16 and asset=='pet_care_original':height=2.25
            if asset in ['bio_badges','pet_snacks_original','dog_original','schoko_group']:height=2.5
            ob=plate(asset,height)
        if wide:
            x=(k-(n-1)/2)*.90;z=.9 if n>3 else .35;y=abs(k-(n-1)/2)*.2
        else:
            x=center+(k-(n-1)/2)*1.10;z=.35+(.12 if k%2 else 0);y=abs(k-(n-1)/2)*.24
        if asset=='leaf':z=.75
        if asset=='bio_badges':z=.03
        if asset=='pfoten':z=.20;y=-.42
        angle=(k-(n-1)/2)*-.13
        # A restrained sculptural entrance followed by a clear reading hold.
        key(ob,st,loc=(x,y,z+.30),rot=(0,.08,angle-.35),scale=.08)
        key(ob,st+min(21,max(10,int(dur*.20))),loc=(x,y,z),rot=(.025,-.035,angle),scale=1.0)
        key(ob,st+int(dur*.78),loc=(x,y,z+.10),rot=(-.025,.035,angle+.07),scale=1.0)
        key(ob,en,loc=(x,y,z),rot=(0,-.015,angle+.10),scale=1.0)
    sc.frame_set(st+round(dur*.58))

for sc in list(bpy.data.scenes):
    if sc not in SCENES:bpy.data.scenes.remove(sc)
bpy.context.window.scene=SCENES[0]
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'UNSER_KRAUT_HERBST_3D.blend'),compress=True)
print('PROJECT_SAVED',len(SCENES),flush=True)
if '--stills' in sys.argv:
    (BUILD/'stills').mkdir(exist_ok=True)
    for card,sc in zip(STORY['cards'],SCENES):
        bpy.context.window.scene=sc;sc.frame_set(sc.frame_start+round((sc.frame_end-sc.frame_start)*.58))
        sc.render.filepath=str(BUILD/'stills'/f'{card["id"]:02d}.png')
        bpy.ops.render.render(write_still=True,scene=sc.name)
        print('STILL_DONE',card['id'],flush=True)
print('BUILD_DONE',flush=True)
