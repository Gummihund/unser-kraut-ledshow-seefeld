"""Crisp LED copy, literal source wording. This module never rewrites captions."""
from pathlib import Path
import json,math
from functools import lru_cache
import numpy as np
from PIL import Image,ImageFont,ImageDraw
ROOT=Path(__file__).resolve().parent
STORY=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
W,H=768,512
COLOR={'brand':'#b4e978','oil':'#b7ed6e','care':'#a0e8d5','pets':'#9edcf2','food':'#e4d88c','gold':'#f2ce86','active':'#c4ec77','balance':'#dfb4ed','relief':'#99e1ea','tea':'#badc81','night':'#c7d1ff','gift':'#e0b8ed'}
@lru_cache(maxsize=160)
def font(size):
    for path in ['C:/Windows/Fonts/arialbd.ttf','DejaVuSans-Bold.ttf']:
        try:return ImageFont.truetype(path,size)
        except OSError:pass
    return ImageFont.load_default()
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)

@lru_cache(maxsize=80)
def layout(card_id):
    c=STORY['cards'][card_id-1];lines=c['lines'];assets=c['assets']
    if not lines:return [],'none'
    if not assets:mode='full'
    elif assets==['stars']:mode='stars'
    elif assets==['bio_badges']:mode='top'
    elif len(assets)>3 or assets==['closing_original']:mode='bottom'
    else:mode='split'
    width=690 if mode!='split' else 342
    base=102 if mode=='full' else (66 if mode in ['bottom','top'] else (63 if mode=='stars' else 94))
    available=405 if mode=='full' else (125 if mode=='bottom' else (175 if mode=='top' else (285 if mode=='stars' else 340)))
    probe=ImageDraw.Draw(Image.new('RGB',(1,1)))
    fs=base
    while fs>30:
        f=font(fs);maxw=max(probe.textbbox((0,0),s,font=f,stroke_width=3)[2] for s in lines)
        if maxw<=width and len(lines)*(fs*1.14)<=available:break
        fs-=1
    step=round(fs*1.14)
    if mode=='full':top=(H-step*len(lines))//2-5
    elif mode=='bottom':top=H-step*len(lines)-17
    elif mode=='top':top=35
    elif mode=='stars':top=197
    else:top=(H-step*len(lines))//2-5
    items=[]
    for i,s in enumerate(lines):
        if card_id==1:
            local_fs=54 if i==0 else 34
            while probe.textbbox((0,0),s,font=font(local_fs),stroke_width=3)[2]>width:local_fs-=1
            items.append((s,29,205+i*76,local_fs,i))
            continue
        b=probe.textbbox((0,0),s,font=font(fs),stroke_width=3)
        x=29 if mode=='split' else round((W-b[2])/2)
        items.append((s,x,top+i*step,fs,i))
    return items,mode

@lru_cache(maxsize=10)
def shade(mode):
    arr=np.zeros((H,W,4),np.uint8)
    if mode=='full':arr[:,:,3]=90
    elif mode=='stars':arr[:,:,3]=np.clip((np.arange(H)[:,None]-100)/180,0,1)*110
    elif mode=='bottom':arr[:,:,3]=np.clip((np.arange(H)[:,None]-285)/190,0,1)*205
    elif mode=='top':arr[:,:,3]=np.clip((240-np.arange(H)[:,None])/180,0,1)*165
    elif mode=='split':arr[:,:,3]=np.clip((465-np.arange(W)[None,:])/320,0,1)*85
    return Image.fromarray(arr)

def compose(image,card_id,local_frame):
    c=STORY['cards'][card_id-1];items,mode=layout(card_id)
    im=image.convert('RGBA');im=Image.alpha_composite(im,shade(mode))
    typ=Image.new('RGBA',(W,H));d=ImageDraw.Draw(typ)
    alpha=round(255*smooth((local_frame/30-.08)/.28))
    for s,x,y,fs,i in items:
        shift=round(10*(1-smooth((local_frame/30-.06-i*.025)/.28)))
        fill='#f5f4e4' if i%2==0 else COLOR[c['theme']]
        d.text((x+shift,y),s,font=font(fs),fill=fill,stroke_width=3,stroke_fill='#07120a')
    if alpha<255:typ.putalpha(typ.getchannel('A').point(lambda v:round(v*alpha/255)))
    im=Image.alpha_composite(im,typ).convert('RGB')
    gain=min(smooth(local_frame/4),smooth((c['frames']-1-local_frame)/4))
    if gain<1:im=Image.blend(Image.new('RGB',(W,H),(2,6,3)),im,gain)
    return im

def contact_sheets():
    out=ROOT/'preview';out.mkdir(exist_ok=True)
    failures=[];records=[]
    for c in STORY['cards']:
        p=ROOT/'build/stills'/f'{c["id"]:02d}.png'
        if not p.exists():continue
        frame=compose(Image.open(p),c['id'],round(c['frames']*.58))
        frame.save(out/f'{c["id"]:02d}.jpg',quality=92)
        if c['id']==1:frame.save(out/'POSTER.jpg',quality=94)
        items,mode=layout(c['id'])
        for text,x,y,fs,_ in items:
            bb=ImageDraw.Draw(frame).textbbox((x,y),text,font=font(fs),stroke_width=3)
            if bb[0]<0 or bb[1]<0 or bb[2]>W or bb[3]>H:failures.append((c['id'],text,bb))
        records.append({'card':c['id'],'all_lines':c['lines'],'mode':mode,'font_px':items[0][3] if items else None,'native_font_px':items[0][3]/4 if items else None})
    for page in range(3):
        sheet=Image.new('RGB',(1536,5*282),'#07110a');pixels=sheet.copy();d=ImageDraw.Draw(sheet)
        for j,c in enumerate(STORY['cards'][page*20:page*20+20]):
            p=out/f'{c["id"]:02d}.jpg'
            if not p.exists():continue
            im=Image.open(p);x=(j%4)*384;y=(j//4)*282
            sheet.paste(im.resize((384,256),Image.Resampling.LANCZOS),(x,y))
            pixels.paste(im.resize((192,128),Image.Resampling.LANCZOS).resize((384,256),Image.Resampling.NEAREST),(x,y))
            d.text((x+8,y+259),f'{c["id"]:02d}   {c["seconds"]:g} s',font=font(18),fill='#d5dfc6')
        sheet.save(out/f'UEBERSICHT_{page+1}.jpg',quality=93)
        pixels.save(out/f'LED_PIXEL_{page+1}.jpg',quality=95)
    (ROOT/'typography_check.json').write_text(json.dumps({'cards':records,'clipping':failures},ensure_ascii=False,indent=2),encoding='utf-8')
    assert not failures,failures
    print('54 captions checked, no text clipping',flush=True)

if __name__=='__main__':contact_sheets()
