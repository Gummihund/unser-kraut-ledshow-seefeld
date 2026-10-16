"""Extract original pixels for Blender texture mapping. No invented packaging."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageFilter,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent;A=ROOT/'assets'
STORY=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
USED={x for c in STORY['cards'] for x in c['assets']}
PROFILES={
 'dropper':['cbd10','cbd5','cbd20','cbd40','nacht','entlastung','tier5','tier10','speiseoel','spray'],
 'jar':['fatburner','mann','gelenke','darm','nougat','samen','protein'],
 'tube':['trocken','kuehl','warm','pflege'],
 'pouch':['tee'],
 'panel':['akut','frau','buch','bad','seife','tasse','tasse2','honig','schoko_group'],
}
profiles={key:kind for kind,keys in PROFILES.items() for key in keys}
manual={'pflege':(775,162,1052,1388)}
special={
 'pet_snacks_original':(15,(0,22,92,128)),
 'pet_care_original':(16,(99,37,183,128)),
 'sos_original':(35,(0,0,86,128)),
 'dog_original':(36,(100,60,192,128)),
 'organic':(10,(0,33,65,114)),
 'bio_badges':(21,(0,68,192,128)),
 'leaf':(7,(0,0,69,105)),
 'paw':(34,(0,36,53,103)),
 'natural_leaf':(37,(0,31,34,125)),
 'closing_original':(54,(0,0,192,104)),
 'mug_angle_original':(50,(94,44,183,128)),
}
catalog={}
for key in sorted(USED):
    if key=='stars':continue
    if key=='logo':
        im=Image.open(A/'logo.png').convert('RGBA');kind='coin';keyed=False
    elif key in special:
        number,box=special[key]
        im=Image.open(ROOT/'reference'/f'card_{number:02d}.png').crop(box).convert('RGBA')
        kind='graphic';keyed=key!='closing_original'
    else:
        im=Image.open(A/(key+'.jpg')).convert('RGBA');kind=profiles.get(key,'panel');keyed=False
        if key in manual:im=im.crop(manual[key])
        elif im.getchannel('A').getextrema()[0]<255:
            im=im.crop(im.getchannel('A').getbbox())
        else:
            rgb=np.asarray(im)[:,:,:3].astype(int)
            mask=(np.min(rgb,axis=2)<235)
            # Ignore isolated peripheral compression spots while retaining labels.
            yy,xx=np.where(mask)
            if len(xx):
                x0,x1=np.percentile(xx,[.2,99.8]).astype(int);y0,y1=np.percentile(yy,[.1,99.9]).astype(int)
                im=im.crop((max(0,x0-4),max(0,y0-4),min(im.width,x1+5),min(im.height,y1+5)))
    im=ImageOps.contain(im,(850,1100),Image.Resampling.LANCZOS)
    filename=key+'_texture.png';im.save(A/filename)
    if key in ['cbd10','cbd5','cbd20','cbd40','nacht','entlastung','tier5','tier10']:
        im.crop((round(im.width*.02),round(im.height*.53),round(im.width*.98),round(im.height*.975))).save(A/(key+'_label.png'))
    catalog[key]={'file':filename,'size':list(im.size),'kind':kind,'green_key':keyed,'original_pixels':True}
(ROOT/'asset_catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
keys=list(catalog);font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',17)
for page in range((len(keys)+19)//20):
    sheet=Image.new('RGB',(1250,4*268),'#9d9f9c');d=ImageDraw.Draw(sheet)
    for j,key in enumerate(keys[page*20:page*20+20]):
        im=ImageOps.contain(Image.open(A/catalog[key]['file']).convert('RGBA'),(240,235))
        x=(j%5)*250;y=(j//5)*268;sheet.paste(im,(x+(250-im.width)//2,y),im)
        d.text((x+9,y+239),key,font=font,fill='black')
    (ROOT/'build').mkdir(exist_ok=True)
    sheet.save(ROOT/'build'/f'texture_contact_{page+1}.jpg',quality=94)
print('Textures',len(catalog))
