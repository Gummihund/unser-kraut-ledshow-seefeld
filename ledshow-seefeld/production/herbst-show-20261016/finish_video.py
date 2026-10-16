"""Encode, fully decode-check and package the complete 54-card Blender show."""
from pathlib import Path
import sys,json,re,subprocess,os,zipfile
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[3]/'tools/led-motion-runtime'))
import imageio_ffmpeg
from compose import STORY,compose,contact_sheets,font,layout
FF=imageio_ffmpeg.get_ffmpeg_exe()
BUILD=ROOT/'build';ENC=BUILD/'encoded';ENC.mkdir(exist_ok=True)
DEST=ROOT.parents[1]/'videos/schaufenster-unten-led'
NAME='UNSER_KRAUT_HERBST_20261016'
FILES=[NAME+'_VORSCHAU_768x512.mp4',NAME+'_192x128.mp4',NAME+'_192x128_KOMPATIBEL.avi']
TOTAL=STORY['total_frames']

def encode():
    frames=[BUILD/'frames'/f'frame_{n:04d}.png' for n in range(1,TOTAL+1)]
    missing=[f.name for f in frames if not f.exists() or f.stat().st_size<2000]
    assert not missing,(len(missing),missing[:5])
    cmd=[FF,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','768x512','-r','30','-i','pipe:0',
      '-filter_complex','[0:v]split=2[master][small];[small]scale=192:128:flags=lanczos[native]',
      '-map','[master]','-an','-c:v','libx264','-crf','19','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(ENC/FILES[0]),
      '-map','[native]','-an','-c:v','libx264','-profile:v','baseline','-level','3.0','-crf','17','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(ENC/FILES[1])]
    with (BUILD/'encode.log').open('w') as err:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=err)
        for card in STORY['cards']:
            for frame in range(card['first_frame'],card['last_frame']+1):
                with Image.open(frames[frame-1]) as source:im=compose(source,card['id'],frame-card['first_frame'])
                p.stdin.write(im.tobytes())
            print('ENCODE_CARD',card['id'],'OF 54',flush=True)
        p.stdin.close();result=p.wait()
    assert result==0,(BUILD/'encode.log').read_text()
    subprocess.run([FF,'-y','-v','error','-i',str(ENC/FILES[1]),'-an','-c:v','mpeg4','-q:v','3','-vtag','XVID',str(ENC/FILES[2])],check=True)

def verify():
    results=[]
    for index,name in enumerate(FILES):
        file=ENC/name;dimensions='768x512' if index==0 else '192x128'
        info=subprocess.run([FF,'-hide_banner','-i',str(file)],capture_output=True,text=True).stderr
        assert dimensions in info and '30 fps' in info and 'Duration: 00:03:28.00' in info,(name,info)
        assert 'Audio:' not in info and 'rotate' not in info.lower(),(name,info)
        if index==1:assert 'Constrained Baseline' in info and 'yuv420p' in info,(name,info)
        dec=subprocess.run([FF,'-v','error','-i',str(file),'-progress','pipe:1','-f','null','-'],capture_output=True,text=True)
        count=re.findall(r'^frame=(\d+)',dec.stdout,re.M)
        assert dec.returncode==0 and not dec.stderr and count and int(count[-1])==TOTAL,(name,dec.stderr,count)
        results.append({'file':name,'dimensions':dimensions,'fps':30,'frames':TOTAL,'seconds':208,'audio':False,'size_bytes':file.stat().st_size,'full_decode':'passed'})
    # Every final compressed LED card is sampled and retained as a native-pixel overview.
    native_samples=[]
    for c in STORY['cards']:
        t=(c['first_frame']-1+c['frames']*.58)/30
        raw=subprocess.run([FF,'-v','error','-ss',str(t),'-i',str(ENC/FILES[1]),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],capture_output=True,check=True).stdout
        assert len(raw)==192*128*3
        native_samples.append(Image.frombytes('RGB',(192,128),raw))
        items,_=layout(c['id']);assert [x[0] for x in items]==c['lines']
    for page in range(3):
        sheet=Image.new('RGB',(1536,1410),'#07110b');d=ImageDraw.Draw(sheet)
        for j,im in enumerate(native_samples[page*20:page*20+20]):
            x=(j%4)*384;y=(j//4)*282
            sheet.paste(im.resize((384,256),Image.Resampling.NEAREST),(x,y));d.text((x+8,y+258),f'{page*20+j+1:02d}',font=font(18),fill='#dce6d0')
        sheet.save(ROOT/'preview'/f'LED_EXPORT_{page+1}.jpg',quality=95)
    (ROOT/'export_verification.json').write_text(json.dumps({'videos':results,'source_cards':54,'output_cards':54,'exact_caption_lines':True,'same_order':True,'same_timing':True,'sampled_compressed_cards':54,'physical_controller_test':'pending'},ensure_ascii=False,indent=2),encoding='utf-8')
    DEST.mkdir(parents=True,exist_ok=True)
    for name in FILES:os.replace(ENC/name,DEST/name)
    print('VERIFIED 54 CARDS / 6240 FRAMES / 3 FILES',flush=True)

def viewer():
    import html
    options=''.join(f'<option value="{(c["first_frame"]-1)/30}">{c["id"]:02d} · {html.escape(" ".join(c["lines"])[:75] or "Schokolade")}</option>' for c in STORY['cards'])
    rows=''.join(f'<tr><td>{c["id"]:02d}</td><td>{(c["first_frame"]-1)/30:g} s</td><td>{"<br>".join(html.escape(s) for s in c["lines"]) or "Produktmotiv ohne zusätzlichen Text"}</td></tr>' for c in STORY['cards'])
    template=(ROOT/'viewer_template.html').read_text(encoding='utf-8')
    (ROOT/'VORSCHAU.html').write_text(template.replace('@@OPTIONS@@',options).replace('@@ROWS@@',rows),encoding='utf-8')

def package():
    repo=ROOT.parents[2];out=ROOT.parents[3]/'output'/'UNSER_KRAUT_Herbst_3D_Komplett_20261016.zip'
    files=[]
    for p in ROOT.rglob('*'):
        if not p.is_file() or 'build' in p.relative_to(ROOT).parts or p.suffix in ['.blend1','.pyc'] or '__pycache__' in p.parts:continue
        if p.parent.name=='preview' and re.fullmatch(r'\d{2}\.jpg',p.name):continue
        files.append(p)
    files += [DEST/name for name in FILES]
    files.append(DEST/'DISPLAY-Schaufenster-226-192x128.mp4')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,'UNSER_KRAUT_HERBST/'+p.relative_to(repo).as_posix())
        z.writestr('UNSER_KRAUT_HERBST/START.html','<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=ledshow-seefeld/production/herbst-show-20261016/VORSCHAU.html"><a href="ledshow-seefeld/production/herbst-show-20261016/VORSCHAU.html">Vorschau öffnen</a>')
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    print('PACKAGE',str(out),out.stat().st_size,flush=True)

if __name__=='__main__':
    if '--package-only' in sys.argv:viewer();package()
    else:contact_sheets();encode();verify();viewer();package()
