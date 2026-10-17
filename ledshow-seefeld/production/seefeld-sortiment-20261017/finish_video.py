"""Large stationary LED captions, 30 seconds, no audio. All original shows are preserved."""
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

ROOT=Path(__file__).resolve().parent
STORY=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
BUILD=ROOT/'build';ENC=BUILD/'encoded';ENC.mkdir(parents=True,exist_ok=True)
PREVIEW=ROOT/'preview';PREVIEW.mkdir(exist_ok=True)
DEST=ROOT.parents[1]/'videos/schaufenster-unten-led';DEST.mkdir(parents=True,exist_ok=True)
NAME='UNSER_KRAUT_SEEFELD_SORTIMENT_20261017'
FILES=[NAME+'_VORSCHAU_768x512.mp4',NAME+'_192x128.mp4',NAME+'_192x128_KOMPATIBEL.avi']
FF=imageio_ffmpeg.get_ffmpeg_exe()
W,H=768,512
N=STORY['total_frames'];SECONDS=STORY['seconds'];NCARDS=len(STORY['cards'])
WHITE='#f7f9eb';LIME='#c2f475';MINT='#b6f2db'
@lru_cache(maxsize=120)
def font(native_size):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',round(native_size*4))

def compose(background,card,local,record=False):
    assert background.size==(W,H),background.size
    im=Image.new('RGB',(W,H),(4,12,8))
    im.paste(background.convert('RGB'),(-168,0))
    im=ImageEnhance.Brightness(im).enhance(.90 if card['kind']=='product' else .23)
    overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
    if card['kind']=='product':
        for y in range(190):
            alpha=235 if y<116 else round(235*(190-y)/74)
            d.line((0,y,W,y),fill=(3,13,8,alpha))
    d.rectangle((0,400,W,H),fill=(4,20,12,255))
    d.line((28,400,W-28,400),fill=(128,195,66,255),width=3)
    im=Image.alpha_composite(im.convert('RGBA'),overlay)
    d=ImageDraw.Draw(im)
    boxes=[]
    def caption(text,top,initial,fill,minimum=24):
        size=initial
        while size>=minimum:
            f=font(size);b=d.textbbox((0,0),text,font=f,stroke_width=4)
            if b[2]-b[0]<=W-40:break
            size-=.25
        assert size>=minimum,(text,size)
        x=(W-(b[2]-b[0]))/2-b[0];y=top*4-b[1]
        box=d.textbbox((x,y),text,font=f,stroke_width=4)
        assert box[0]>=12 and box[2]<=W-12 and box[1]>=8 and box[3]<=H-12,(text,box)
        d.text((x,y),text,font=f,fill=fill,stroke_width=4,stroke_fill='#020a05')
        boxes.append(dict(text=text,native_font_px=size,native_bbox=[round(v/4,2) for v in box]))
    if card['kind']=='brand':
        caption(card['lines'][0],10,25,WHITE)
        caption(card['lines'][1],45,29,LIME)
    elif card['kind']=='product':caption(card['lines'][0],9,28,WHITE)
    else:
        caption(card['lines'][0],8,43,WHITE)
        caption(card['lines'][1],51,46 if card['slug']=='einladung' else 29,LIME)
    caption(card['footer'],106,21 if card['kind']!='invite' else (17 if card['slug']=='einladung' else 20),
            LIME if card['kind']!='invite' else WHITE,minimum=16)
    # A short shared dark dip between cards; captions stay still throughout each card.
    gain=min(1,local/3,(card['frames']-1-local)/3)
    if gain<1:im=Image.blend(Image.new('RGBA',(W,H),(4,12,8,255)),im,max(0,gain))
    return im.convert('RGB'),boxes

def encode():
    frames=[BUILD/'frames'/f'frame_{n:04d}.png' for n in range(1,N+1)]
    assert all(p.is_file() for p in frames),f'All {N} finished backgrounds are required'
    command=[FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','768x512','-r','30','-i','pipe:0',
      '-filter_complex','[0:v]split=2[master][small];[small]scale=192:128:flags=lanczos[native]',
      '-map','[master]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(ENC/FILES[0]),
      '-map','[native]','-an','-c:v','libx264','-profile:v','baseline','-level','3.0','-crf','16','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(ENC/FILES[1])]
    captions=[]
    with (BUILD/'encode.log').open('w') as log:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
        try:
            for card in STORY['cards']:
                for local in range(card['frames']):
                    with Image.open(frames[card['first_frame']+local-1]) as source:im,boxes=compose(source,card,local)
                    process.stdin.write(im.tobytes())
                    if local==card['frames']//2:captions.append(dict(card=card['id'],captions=boxes))
                print('ENCODED_CARD',card['id'],'OF',NCARDS,flush=True)
            process.stdin.close()
            assert process.wait()==0,(BUILD/'encode.log').read_text()
        except BaseException:
            process.kill();process.wait();raise
    subprocess.run([FF,'-y','-v','error','-i',str(ENC/FILES[1]),'-an','-c:v','mpeg4','-q:v','3','-vtag','XVID',str(ENC/FILES[2])],check=True)
    (ROOT/'typography_check.json').write_text(json.dumps(dict(cards=captions,all_bounds_passed=True,
        main_font_minimum_native_px=24,footer_minimum_native_px=16,caption_motion='stationary'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def verify_and_deliver():
    results=[]
    for i,name in enumerate(FILES):
        path=ENC/name
        info=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True).stderr
        size='768x512' if i==0 else '192x128'
        assert size in info and '30 fps' in info and f'Duration: 00:00:{SECONDS:05.2f}' in info,info
        assert 'Audio:' not in info and not re.search(r'rotate\s*:|rotation of',info,re.I),info
        if i==1:assert 'Constrained Baseline' in info and 'yuv420p' in info,info
        decoded=subprocess.run([FF,'-v','error','-i',str(path),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True)
        counts=re.findall(r'^frame=(\d+)',decoded.stdout,re.M)
        assert decoded.returncode==0 and not decoded.stderr and counts and int(counts[-1])==N,decoded.stderr
        results.append(dict(file=name,dimensions=size,fps=30,seconds=SECONDS,frames=N,audio=False,
                            full_decode='passed',bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    sheet=Image.new('RGB',(1536,576),'#06120a');d=ImageDraw.Draw(sheet)
    animated=[]
    for i,card in enumerate(STORY['cards']):
        when=(card['first_frame']-1+card['frames']*.55)/30
        raw=subprocess.run([FF,'-v','error','-ss',str(when),'-i',str(ENC/FILES[1]),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],capture_output=True,check=True).stdout
        assert len(raw)==192*128*3
        im=Image.frombytes('RGB',(192,128),raw)
        im.save(PREVIEW/f'LED_{card["id"]:02d}.png')
        x=(i%4)*384;y=(i//4)*288
        sheet.paste(im.resize((384,256),Image.Resampling.NEAREST),(x,y))
        d.text((x+12,y+260),f'{card["id"]:02d}   {card["seconds"]} Sekunden',font=font(4),fill='#d6e5c8')
    sheet.save(PREVIEW/'LED_KONTAKTBOGEN.png')
    # Small actual-export preview, sampled twice per second across the full loop.
    for sample in range(SECONDS*2):
        raw=subprocess.run([FF,'-v','error','-ss',str(sample*.5+.1),'-i',str(ENC/FILES[1]),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],capture_output=True,check=True).stdout
        animated.append(Image.frombytes('RGB',(192,128),raw).resize((384,256),Image.Resampling.NEAREST))
    animated[0].save(PREVIEW/'SEEFELD_30S.gif',save_all=True,append_images=animated[1:],duration=500,loop=0)
    (ROOT/'export_verification.json').write_text(json.dumps(dict(videos=results,total_cards=NCARDS,physical_controller_test='pending'),indent=2)+'\n',encoding='utf-8')
    for name in FILES:
        target=DEST/name
        if target.exists():raise FileExistsError('Existing final export is preserved: '+str(target))
        os.replace(ENC/name,target)
    print('VERIFIED_AND_DELIVERED: 3 videos, 900 frames each, no audio',flush=True)

if __name__=='__main__':encode();verify_and_deliver()
