"""Derive six packed scenes from the finished autumn Blender project. Run in Blender."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

import bpy

ROOT = Path(__file__).resolve().parent
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=ROOT.parents[2])
options = parser.parse_args(args)
source = options.repo.resolve() / 'ledshow-seefeld/production/herbst-show-20261016'
source_blend = source / 'UNSER_KRAUT_HERBST_3D.blend'
original = json.loads((source / 'storyboard.json').read_text(encoding='utf-8'))
plan = [
    ('marke', 1, 5, ['UNSER KRAUT', 'HANF & CBD'], 'KOMM REIN', 'brand'),
    ('einladung', 7, 4, ['KOMM', 'REIN'], 'WIR BERATEN DICH', 'invite'),
    ('tee', 39, 5, ['BIO HANFTEE'], 'KOMM REIN', 'product'),
    ('pflege', 11, 5, ['CBD PFLEGE'], 'KOMM REIN', 'product'),
    ('geschenke', 49, 5, ['GESCHENKE'], 'KOMM REIN', 'product'),
    ('willkommen', 45, 4, ['KOMM', 'GERNE REIN'], 'UNSER KRAUT', 'invite'),
]
cards = []
start = 1
for i, (slug, source_id, seconds, lines, footer, kind) in enumerate(plan, 1):
    old = original['cards'][source_id - 1]
    frames = seconds * 30
    cards.append(dict(id=i, slug=slug, kind=kind, seconds=seconds, frames=frames,
                      first_frame=start, last_frame=start + frames - 1,
                      source_card=source_id, source_first=old['first_frame'],
                      source_last=old['last_frame'],
                      sample_first=old['first_frame'] + round((old['frames']-1) * .25),
                      sample_last=old['first_frame'] + round((old['frames']-1) * .86),
                      lines=lines, footer=footer, scene=f'{i:02d}_{slug}'))
    start += frames
story = dict(title='Unser Kraut – Bahnhof-Kurzfassung', date='2026-10-17',
             fps=30, seconds=28, total_frames=840, native_size=[192, 128],
             master_size=[768, 512], cards=cards,
             source_project='ledshow-seefeld/production/herbst-show-20261016/UNSER_KRAUT_HERBST_3D.blend',
             source_sha256=hashlib.sha256(source_blend.read_bytes()).hexdigest(),
             source_commit='603592164356233482e8d09033601830ff60f853')
assert start - 1 == 840
(ROOT / 'storyboard.json').write_text(json.dumps(story, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

bpy.ops.wm.open_mainfile(filepath=str(source_blend))
selected = []
for card in cards:
    scene = next(s for s in bpy.data.scenes if s.name.startswith(f'{card["source_card"]:02d}_'))
    selected.append(scene)
for scene in list(bpy.data.scenes):
    if scene not in selected:
        bpy.data.scenes.remove(scene)
for card, scene in zip(cards, selected):
    scene.name = card['scene']
    scene['source_card'] = card['source_card']
    scene['output_seconds'] = card['seconds']
    scene['sample_first'] = card['sample_first']
    scene['sample_last'] = card['sample_last']
    scene.render.resolution_x = 768
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.frame_set(card['sample_first'])
bpy.context.window.scene = selected[0]
bpy.data.orphans_purge(do_recursive=True)
bpy.ops.file.pack_all()
assert all(image.packed_file for image in bpy.data.images if image.source == 'FILE')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'UNSER_KRAUT_BAHNHOF_28S.blend'), compress=True)

assets = ROOT / 'assets'
assets.mkdir(exist_ok=True)
sources = json.loads((source / 'asset_sources.json').read_text(encoding='utf-8'))
records = []
for key in ['logo', 'tee', 'trocken', 'seife']:
    candidates = [p for p in (source/'assets').iterdir() if p.stem in {key, key+'_texture'}]
    for image in candidates:
        shutil.copy2(image, assets/image.name)
        records.append(dict(file=image.name, inherited_from=f'herbst-show-20261016/assets/{image.name}',
                            sha256=hashlib.sha256(image.read_bytes()).hexdigest(),
                            original_source=next((x for x in sources if x['key']==key), None)))
(ROOT/'asset_sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PREPARED: 6 scenes, 840 frames, 28 seconds, packed textures', flush=True)
