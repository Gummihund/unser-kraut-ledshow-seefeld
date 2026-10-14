"""Resume-safe render of the packed Blender project; all five scenes."""
import bpy,sys,time
from pathlib import Path
ROOT=Path(bpy.data.filepath).resolve().parent
OUT=ROOT/'build'/'frames';OUT.mkdir(parents=True,exist_ok=True)
start=time.monotonic()
limit=None
if '--benchmark' in sys.argv:limit=4
count=0
for scene in sorted(bpy.data.scenes,key=lambda s:s.name):
    bpy.context.window.scene=scene
    if limit:frames=[scene.frame_start+50,scene.frame_start+70,scene.frame_start+90,scene.frame_start+110]
    else:frames=range(scene.frame_start,scene.frame_end+1)
    for f in frames:
        path=OUT/f'frame_{f:04d}.png'
        if path.exists() and path.stat().st_size>1000:continue
        scene.frame_set(f);scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True,scene=scene.name)
        count+=1
        if count%10==0 or limit:print('PROGRESS',f,'elapsed',round(time.monotonic()-start,1),flush=True)
    if limit:break
print('RENDER_DONE',count,round(time.monotonic()-start,1),flush=True)
