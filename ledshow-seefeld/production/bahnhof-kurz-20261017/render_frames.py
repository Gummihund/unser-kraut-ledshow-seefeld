"""Produce complete background frames, reusing only verified finished source renders."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

import bpy

ROOT = Path(__file__).resolve().parent
story = json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source-cache', type=Path)
parser.add_argument('--first-card', type=int, default=1)
parser.add_argument('--last-card', type=int, default=6)
options = parser.parse_args(args)
out = ROOT/'build/frames'
out.mkdir(parents=True,exist_ok=True)
records=[]
rendered={}
started=time.monotonic()
def complete(path):
    try:
        with path.open('rb') as f:
            if f.read(8)!=b'\x89PNG\r\n\x1a\n':return False
            f.seek(-12,2)
            return f.read()==b'\x00\x00\x00\x00IEND\xaeB`\x82'
    except OSError:return False
for card in story['cards']:
    if not options.first_card<=card['id']<=options.last_card:continue
    scene=bpy.data.scenes[card['scene']]
    bpy.context.window.scene=scene
    for local in range(card['frames']):
        number=card['first_frame']+local
        source_frame=round(card['sample_first']+local/(card['frames']-1)*(card['sample_last']-card['sample_first']))
        key=(card['scene'],source_frame)
        target=out/f'frame_{number:04d}.png'
        cached=options.source_cache/f'frame_{source_frame:04d}.png' if options.source_cache else None
        if complete(target):mode='existing_complete_variant_frame'
        elif cached and complete(cached):shutil.copy2(cached,target);mode='finished_original_blender_frame'
        elif key in rendered:shutil.copy2(rendered[key],target);mode='repeated_mapped_blender_frame'
        else:
            scene.frame_set(source_frame)
            scene.render.filepath=str(target)
            bpy.ops.render.render(write_still=True,scene=scene.name)
            mode='rendered_with_blender'
        assert complete(target),target
        rendered[key]=target
        records.append(dict(frame=number,card=card['id'],source_frame=source_frame,mode=mode,
                            sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
    print('BACKGROUND_CARD_DONE',card['id'],'OF 6',flush=True)
(ROOT/'render_provenance.json').write_text(json.dumps(dict(
    blender=bpy.app.version_string,source_project_sha256=story['source_sha256'],
    frames=len(records),seconds_elapsed=round(time.monotonic()-started,2),
    note='Only finished PNGs with valid PNG signature and IEND are reused. All frame sizes and pixels are decoded again at composition. No running render jobs adopted.',
    frame_map=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('BACKGROUNDS_DONE',len(records),flush=True)
