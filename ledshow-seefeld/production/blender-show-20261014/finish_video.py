"""Add LED typography, encode all delivery formats, and verify full decoding.
Run with ordinary Python: python finish_video.py
Dependencies: Pillow, numpy, imageio-ffmpeg. Blender frames are kept private.
"""
from pathlib import Path
import sys,subprocess,json,math,re
from PIL import Image,ImageDraw,ImageFont
import numpy as np
ROOT=Path(__file__).resolve().parent
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
DEST=ROOT.parents[1]/'videos/schaufenster-unten-led'
DEST.mkdir(parents=True,exist_ok=True)
NAME='UNSER_KRAUT_3D_BLENDER_20261014'
MASTER=DEST/(NAME+'_VORSCHAU_768x512.mp4')
LED=DEST/(NAME+'_192x128.mp4')
AVI=DEST/(NAME+'_192x128_KOMPATIBEL.avi')
W,H=768,512;FPS=30;ACT=180;FRAMES=900
TITLES=[['CBD','ÖLE'],['UNSER','KRAUT'],['HANF','TEE'],['HANF','SCHOKO'],['KOMM','REIN']]
COLORS=['#b4ec65','#93e8b7','#b4ec65','#edc472','#b4ec65']
FONTDIR=Path('C:/Windows/Fonts')
def font(size):
    for path in [FONTDIR/'arialbd.ttf',Path('DejaVuSans-Bold.ttf')]:
        try:return ImageFont.truetype(str(path),size)
        except OSError:pass
    return ImageFont.load_default()
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)

def compose(frame,idx,f):
    im=frame.convert('RGBA')
    # Keep the native LED words clear without flattening the 3D product area.
    shade=Image.new('RGBA',(W,H));arr=np.zeros((H,W,4),dtype=np.uint8)
    arr[:,:,3]=np.clip((340-np.arange(W))/340,0,1)[None,:]*65
    im=Image.alpha_composite(im,Image.fromarray(arr))
    typ=Image.new('RGBA',(W,H));d=ImageDraw.Draw(typ)
    a=round(255*smooth((f/FPS-.12)/.45))
    d.text((30,33),'UNSER KRAUT',font=font(31),fill=(232,239,222,a))
    for row,word in enumerate(TITLES[idx]):
        fs=100
        while d.textbbox((0,0),word,font=font(fs))[2]>282:fs-=1
        offset=round(18*(1-smooth((f/FPS-.12-row*.10)/.55)))
        d.text((28+offset,187+row*92),word,font=font(fs),fill=('#f3f3df' if row==0 else COLORS[idx]),stroke_width=0)
    d.rectangle((32,398,171,402),fill=COLORS[idx])
    if idx==4:d.text((30,457),'unser-kraut.at',font=font(33),fill=(232,239,222,a))
    if a<255:typ.putalpha(typ.getchannel('A').point(lambda v:round(v*a/255)))
    im=Image.alpha_composite(im,typ).convert('RGB')
    # Short cinematic dark transitions; first/last frame meet without a jump.
    gain=min(smooth(f/6),smooth((ACT-1-f)/6))
    if gain<1:im=Image.blend(Image.new('RGB',(W,H),(2,7,4)),im,gain)
    return im

def stills():
    out=ROOT/'preview';out.mkdir(exist_ok=True)
    names=['01_EMERALD_REVEAL','02_OIL_CONSTELLATION','03_BOTANICAL_TEA','04_GOLD_CHOCOLATE','05_BRAND_PORTAL']
    sheet=Image.new('RGB',(1152,2*292),'#07110c');d=ImageDraw.Draw(sheet)
    pix=Image.new('RGB',(1152,2*292),'#07110c')
    for i,name in enumerate(names):
        im=compose(Image.open(ROOT/'build/stills'/(name+'.png')),i,85)
        im.save(out/(name+'.jpg'),quality=94)
        x=(i%3)*384;y=(i//3)*292
        sheet.paste(im.resize((384,256),Image.Resampling.LANCZOS),(x,y))
        d.text((x+12,y+264),' '.join(TITLES[i]),font=font(19),fill='#e0ead3')
        pix.paste(im.resize((192,128),Image.Resampling.LANCZOS).resize((384,256),Image.Resampling.NEAREST),(x,y))
    sheet.save(out/'3D_SHOW_UEBERSICHT.jpg',quality=94)
    pix.save(out/'3D_LED_PIXELVORSCHAU.png')

def encode():
    frames=[ROOT/'build/frames'/f'frame_{i:04d}.png' for i in range(1,FRAMES+1)]
    missing=[p.name for p in frames if not p.exists()]
    if missing:raise RuntimeError(f'{len(missing)} missing Blender frames, starting {missing[:5]}')
    cmd=[FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0',
         '-filter_complex','[0:v]split=2[master][small];[small]scale=192:128:flags=lanczos[native]',
         '-map','[master]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(MASTER),
         '-map','[native]','-an','-c:v','libx264','-profile:v','baseline','-level','3.0','-crf','15','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(LED)]
    log=ROOT/'build/encode.log';gif=[]
    with log.open('w') as err:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=err)
        for k,path in enumerate(frames):
            with Image.open(path) as source:im=compose(source,k//ACT,k%ACT)
            p.stdin.write(im.tobytes())
            if k%6==0:gif.append(im.resize((384,256),Image.Resampling.LANCZOS).quantize(colors=128))
            if k%ACT==0:print('ENCODE_ACT',k//ACT+1,flush=True)
        p.stdin.close();code=p.wait()
    if code:raise RuntimeError(log.read_text())
    gif[0].save(ROOT/'preview'/'3D_SHOW_ANIMIERT.gif',save_all=True,append_images=gif[1:],duration=200,loop=0,optimize=False,disposal=2)
    subprocess.run([FF,'-y','-v','error','-i',str(LED),'-an','-c:v','mpeg4','-q:v','3','-vtag','XVID',str(AVI)],check=True)

def verify():
    results=[]
    for path,res in [(MASTER,'768x512'),(LED,'192x128'),(AVI,'192x128')]:
        probe=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True).stderr
        assert res in probe and '30 fps' in probe and 'Duration: 00:00:30.00' in probe,(path,probe)
        assert 'Audio:' not in probe and 'rotate' not in probe.lower(),(path,probe)
        if path==LED:assert 'Constrained Baseline' in probe and 'yuv420p' in probe,(path,probe)
        dec=subprocess.run([FF,'-v','error','-i',str(path),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True)
        count=re.findall(r'^frame=(\d+)',dec.stdout,re.M)
        assert dec.returncode==0 and not dec.stderr and count and int(count[-1])==FRAMES,(path,dec.stderr,count)
        results.append({'file':path.name,'dimensions':res,'fps':FPS,'frames':FRAMES,'duration_seconds':30,'audio':False,'size_bytes':path.stat().st_size,'decode':'passed'})
    # Inspect true compressed LED frames, not just source stills.
    sheet=Image.new('RGB',(1152,584),'#07110c')
    for i,t in enumerate([2.8,8.8,14.8,20.8,26.8]):
        raw=subprocess.run([FF,'-v','error','-ss',str(t),'-i',str(LED),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],capture_output=True,check=True).stdout
        assert len(raw)==192*128*3
        im=Image.frombytes('RGB',(192,128),raw).resize((384,256),Image.Resampling.NEAREST)
        sheet.paste(im,((i%3)*384,(i//3)*292))
    sheet.save(ROOT/'preview'/'3D_LED_EXPORT_KONTROLLE.png')
    (ROOT/'export_verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('VERIFIED',json.dumps(results),flush=True)

def package():
    import zipfile
    repo=ROOT.parents[2]
    out=ROOT/'build'/'UNSER_KRAUT_Blender_3D_Show_20261014.zip'
    out.parent.mkdir(parents=True,exist_ok=True)
    names=['UNSER_KRAUT_3D.blend','build_show.py','render_frames.py','finish_video.py','README.md','VORSCHAU.html','scene_manifest.json','export_verification.json']
    files=[ROOT/name for name in names]+list((ROOT/'assets').glob('*'))+list((ROOT/'preview').glob('*'))+[MASTER,LED,AVI]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for file in files:
            if file.is_file():z.write(file,'UNSER_KRAUT_3D/'+file.relative_to(repo).as_posix())
        z.writestr('UNSER_KRAUT_3D/START.html','<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=ledshow-seefeld/production/blender-show-20261014/VORSCHAU.html"><a href="ledshow-seefeld/production/blender-show-20261014/VORSCHAU.html">Vorschau starten</a>')
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    print('PACKAGE',str(out),out.stat().st_size,flush=True)

if __name__=='__main__':
    if '--package-only' in sys.argv:package()
    else:
        stills()
        if '--stills' not in sys.argv:encode();verify();package()
