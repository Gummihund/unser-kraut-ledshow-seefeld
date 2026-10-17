"""Derive eight packed scenes from the finished autumn Blender project. Run in Blender."""
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
    ('marke', 1, 4, ['UNSER KRAUT', 'HANF & CBD'], 'SEEFELD', 'brand'),
    ('oele', 4, 4, ['CBD ÖLE'], 'UNSER KRAUT', 'product'),
    ('tee', 39, 4, ['BIO HANFTEE'], 'ZUM GENIESSEN', 'product'),
    ('einladung', 7, 3, ['KOMM', 'REIN'], 'WIR BERATEN DICH', 'invite'),
    ('vapes', 39, 4, ['VAPES'], '18+', 'product'),
    ('pflege', 11, 4, ['CBD PFLEGE'], 'UNSER KRAUT', 'product'),
    ('geschenke', 49, 4, ['GESCHENKE'], 'ZUM MITNEHMEN', 'product'),
    ('willkommen', 45, 3, ['KOMM', 'GERNE REIN'], 'UNSER KRAUT', 'invite'),
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
    if slug=='vapes':cards[-1]['cache_reuse_allowed']=False
    start += frames
story = dict(title='Unser Kraut – Seefeld-Sortiment', date='2026-10-17',
             fps=30, seconds=30, total_frames=900, native_size=[192, 128],
             master_size=[768, 512], cards=cards,
             source_project='ledshow-seefeld/production/herbst-show-20261016/UNSER_KRAUT_HERBST_3D.blend',
             source_sha256=hashlib.sha256(source_blend.read_bytes()).hexdigest(),
             source_commit='603592164356233482e8d09033601830ff60f853')
assert start - 1 == 900
(ROOT / 'storyboard.json').write_text(json.dumps(story, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

sys.path.insert(0,str(ROOT))
bpy.ops.wm.open_mainfile(filepath=str(source_blend))
original_scenes={c['id']:next(s for s in bpy.data.scenes if s.name.startswith(f"{c['id']:02d}_")) for c in original['cards']}
selected = []
for card in cards:
    scene = original_scenes[card['source_card']]
    if card['slug']=='vapes':
        scene=scene.copy()
        scene.name='Independent vape environment'
        from vape_scene import replace_tea_with_vape
        replace_tea_with_vape(scene, options.repo.resolve())
    selected.append(scene)
for scene in list(bpy.data.scenes):
    if scene not in selected:
        bpy.data.scenes.remove(scene)
for card, scene in zip(cards, selected):
    scene.name = card['scene']
    for node in scene.node_tree.nodes:
        if node.type=='R_LAYERS':node.scene=scene
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
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'UNSER_KRAUT_SEEFELD_30S.blend'), compress=True)

assets = ROOT / 'assets'
assets.mkdir(exist_ok=True)
sources = json.loads((source / 'asset_sources.json').read_text(encoding='utf-8'))
records = []
for key in ['logo', 'tee', 'trocken', 'seife', 'cbd10']:
    candidates = [p for p in (source/'assets').iterdir() if p.stem in {key, key+'_texture', key+'_label'}]
    for image in candidates:
        shutil.copy2(image, assets/image.name)
        records.append(dict(file=image.name, inherited_from=f'herbst-show-20261016/assets/{image.name}',
                            sha256=hashlib.sha256(image.read_bytes()).hexdigest(),
                            original_source=next((x for x in sources if x['key']==key), None)))
vape_source=options.repo.resolve()/'ledshow-seefeld/assets/raw/vape-mesh-himbeere.png'
shutil.copy2(vape_source,assets/vape_source.name)
records.append(dict(file=vape_source.name,inherited_from='ledshow-seefeld/assets/raw/'+vape_source.name,sha256=hashlib.sha256(vape_source.read_bytes()).hexdigest(),product_url='https://www.unser-kraut.at/vapes',image_url='https://static.wixstatic.com/media/76f9c9_7269afac671e4ad79f11e4e1b696514d~mv2.png/v1/fit/w_900,h_900,q_95/file.png',usage='Unchanged source pixels; white-background transparency applied in Blender material only.'))
(ROOT/'asset_sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PREPARED: 8 scenes, 900 frames, 30 seconds, packed textures', flush=True)
