"""Render all 6,240 native animation frames; restart safely after interruption."""
import bpy,time,json,sys,argparse
from pathlib import Path
ROOT=Path(bpy.data.filepath).resolve().parent
STORY=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
OUT=ROOT/'build/frames';OUT.mkdir(parents=True,exist_ok=True)
start=time.monotonic();count=0
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
parser=argparse.ArgumentParser();parser.add_argument('--first-card',type=int,default=1);parser.add_argument('--last-card',type=int,default=54)
options=parser.parse_args(args)
def complete(path):
    try:
        if path.stat().st_size<2000:return False
        with path.open('rb') as stream:stream.seek(-12,2);return stream.read()==b'\x00\x00\x00\x00IEND\xaeB`\x82'
    except OSError:return False
for c,scene in zip(STORY['cards'],sorted(bpy.data.scenes,key=lambda x:x.name)):
    if not options.first_card<=c['id']<=options.last_card:continue
    assert scene.name.startswith(f'{c["id"]:02d}_')
    bpy.context.window.scene=scene
    for frame in range(c['first_frame'],c['last_frame']+1):
        p=OUT/f'frame_{frame:04d}.png'
        if complete(p):continue
        scene.frame_set(frame);scene.render.filepath=str(p)
        bpy.ops.render.render(write_still=True,scene=scene.name)
        count+=1
    print('CARD_DONE',c['id'],'FRAME',c['last_frame'],'OF',STORY['total_frames'],'ELAPSED',round(time.monotonic()-start,1),flush=True)
print('RENDER_DONE',count,'ELAPSED',round(time.monotonic()-start,1),flush=True)
