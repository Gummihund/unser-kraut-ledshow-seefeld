"""Literal visible copy from the supplied 54-card source video.
Only wrapping/layout is changed. No assertions are revalidated or added.
"""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
DATA=[
(['UNSER KRAUT','DEIN FACHGESCHÄFT'],['logo'],'brand'),
(['VERTRAUEN','DURCH','KOMPETENZ.'],[],'brand'),
(['5,0 VON 5 STERNEN','GOOGLE','TRUSTED SHOPS','HEROLD'],['stars'],'gold'),
(['WENN DIR','ALLES','ZUVIEL WIRD','NATURKRAFT','CBD ÖL'],['cbd10'],'oil'),
(['MACHT NICHT','BERAUSCHT','LEGAL IN DER EU'],[],'oil'),
(['HOL DIR','DEIN PASSENDES'],['cbd5','cbd20','cbd40','nacht','entlastung','cbd10'],'oil'),
(['NEU BEI','HANF & CBD?','WIR ERKLÄREN','ES DIR GERNE.'],['leaf'],'brand'),
(['HAUTPFLEGE','FÜR HÖHERE','ANSPRÜCHE','GESUCHT?'],['pflege'],'care'),
(['ENTDECKE UNSER','großes Sortiment','an Bio','GESICHTS- &','KÖRPERPFLEGE'],[],'care'),
(['ZERTIFIZIERTE','BIO - ORGANIC','KOSMETIK','MIT CBD'],['organic'],'care'),
(['Spezial PFLEGE','TROCKENE','HAUT'],['trocken'],'care'),
(['ERSTE HILFE','FÜR DEINE','HAUT'],['akut'],'care'),
(['Großes Sortiment','für','HUND','KATZE & PFERD'],[],'pets'),
(['CBD ÖL','Tropfen'],['tier5','tier10'],'pets'),
(['ANTISTRESS','GELENKE','VERDAUUNG'],['pet_snacks_original'],'pets'),
(['TIERPFLEGE'],['spray','pfoten','pet_care_original'],'pets'),
(['REINE NATUR','FÜR DEINE','GESUNDE','KÜCHE'],[],'food'),
(['OMEGA 3','Quelle'],['samen'],'food'),
(['OMEGA 3','Quelle'],['speiseoel'],'food'),
(['BIO','Schoko','Creme'],['nougat'],'gold'),
(['BIO AUS','ÖSTERREICH'],['bio_badges'],'food'),
(['Für','SPORT - FIGUR','& ENERGIE'],[],'active'),
(['VEGANE','PROTEINE','für die Figur'],['protein'],'active'),
(['HANF','FATBURNER','mit Kräutern'],['fatburner'],'active'),
(['WOHLBEFINDEN','FÜR','SIE & IHN'],[],'balance'),
(['FÜR','DIE','FRAU'],['frau'],'balance'),
(['FÜR','DEN MANN'],['mann'],'balance'),
(['DEINE GELENKE','GEZIELT','UNTERSTÜTZEN'],['gelenke'],'active'),
(['ANSTRENGENDEN','TAG','GEHABT?'],[],'relief'),
(['KÜHLENDE','MUSKEL &','GELENKS','CREME'],['kuehl'],'relief'),
(['WÄRMENDE','MUSKEL &','GELENKS','CREME'],['warm'],'gold'),
(['HOL DIR','ERLEICHTERUNG','FÜR','KOPF & KÖRPER'],[],'relief'),
(['CBD ÖL','ENTLASTUNG'],['entlastung'],'relief'),
(['ANTISTRESS','BEWEGUNG','VERDAUUNG'],['paw'],'pets'),
(['HANF','FLEISCH','SNACKS'],['sos_original'],'pets'),
(['SOS BEI','STRESS &','UNRUHE'],['dog_original'],'pets'),
(['100% NATUR','OHNE ZUSÄTZE','GETREIDEFREI'],['natural_leaf'],'pets'),
(['HAST DU','AUSZEIT','NÖTIG?'],[],'tea'),
(['ENTSPANNENDE','BIO','HANF TEES'],['tee'],'tea'),
(['WENN DIR DAS','LEBEN','SAURES GIBT...'],[],'tea'),
(['HOL DIR','HANF & CBD'],['leaf'],'tea'),
(['HAB GUTE','NÄCHTE','CBD/CBN ÖL'],['nacht'],'night'),
(['UNRUHIGES','BAUCH','GEFÜHL?'],['darm'],'balance'),
(['FACH','BÜCHER'],['buch'],'brand'),
(['KOMM','GERNE','REIN.'],['logo'],'brand'),
(['WIR NEHMEN','UNS ZEIT.'],[],'brand'),
(['DU SUCHST','EIN','BESONDERES','GESCHENK?'],[],'gift'),
(['CBD','BADE','KUGELN'],['bad'],'gift'),
(['CBD','SEIFEN'],['seife'],'gift'),
(['KUNSTDESIGN','AUS TIROL'],['tasse','mug_angle_original'],'gift'),
(['SCHENKE EIN','BESONDERES','STÜCK','SEEFELD'],[],'gold'),
([],['schoko_group'],'gold'),
(['IMKER','HANFHONIG','AUS MÖSERN','BEI SEEFELD'],['honig'],'gold'),
(['MODERN LIFESTYLE','FROM NATURE'],['closing_original'],'brand'),
]
TIMING=[120,105,135,120,90,165,120,150,120,150,120,120,90,120,150,150,90,120,90,150,90,90,90,150,90,120,120,120,90,105,105,90,120,90,120,120,90,90,75,90,105,120,120,105,75,75,150,210,75,75,75,255,120,150]
assert len(DATA)==len(TIMING)==54 and sum(TIMING)==6240
start=0;cards=[]
for i,((lines,assets,theme),duration) in enumerate(zip(DATA,TIMING)):
    cards.append({'id':i+1,'lines':lines,'assets':assets,'theme':theme,'first_frame':start+1,'last_frame':start+duration,'frames':duration,'seconds':duration/30,'reference':f'reference/card_{i+1:02d}.png'})
    start+=duration
out={'title':'DISPLAY Schaufenster 226 – Herbst 2026','date':'2026-10-16','fps':30,'width':192,'height':128,'total_frames':6240,'seconds':208,'source_filename':'DISPLAY Schaufenster 226 - 192 x 128.mp4','source_sha256':'b542f489d8a42242aa08bb7905f28e879705fd3ab2a93a91835f1b3fc790bed9','copy_policy':'Original visible copy retained, including spelling and assertions. Only wrapping and design change. Assertions are supplied advertising copy, not independent verification.','cards':cards}
(ROOT/'storyboard.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('54 cards / 6240 frames / all original captions entered')
