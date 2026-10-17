"""Publish an immutable, checked display-project snapshot from a clean Git checkout.

Only files selected by HEAD are copied. Existing different files stop publication;
there is no deletion, replacement, mirroring, or inclusion of local render jobs.
Uses Python's standard library only. Call with --help for arguments.
"""
import argparse
import concurrent.futures as futures
import hashlib
import html
import json
from pathlib import Path
import subprocess
from datetime import datetime, timezone


def digest(path):
    checksum = hashlib.sha256()
    with path.open('rb', buffering=1024 * 1024) as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(block)
    return checksum.hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--destination', required=True, help='New version folder, never the shared development checkout')
    parser.add_argument('--show-config', help='Optional Git-tracked JSON with title, description, links, primary_video, project_dir and technical_checks')
    args = parser.parse_args()
    root = Path(args.repo).resolve()
    target = Path(args.destination).resolve()
    if root == target or root in target.parents or target in root.parents:
        raise RuntimeError('Use a separate snapshot destination.')
    if git(root, 'status', '--porcelain', '--untracked-files=no').strip():
        raise RuntimeError('Commit the reviewed project first; tracked working files must be clean.')
    commit = git(root, 'rev-parse', 'HEAD').decode().strip()
    paths = sorted(p.decode('utf-8') for p in git(root, 'ls-tree', '-r', '--name-only', '-z', 'HEAD').split(b'\0') if p)
    entries = []
    for relative in paths:
        source = root / relative
        if root not in source.resolve().parents or source.is_symlink() or not source.is_file():
            raise RuntimeError(f'Unsafe or missing selected source: {relative}')
        entries.append({'path': relative, 'bytes': source.stat().st_size, 'sha256': digest(source), 'source': 'git'})

    video_dir = 'ledshow-seefeld/videos/schaufenster-unten-led/'
    project_dir = 'ledshow-seefeld/production/herbst-show-20261016/'
    links = [
        ('LED-MP4: 192 × 128, 30 fps, ohne Ton', video_dir + 'UNSER_KRAUT_HERBST_20261016_192x128.mp4'),
        ('Große PC-Vorschau: 768 × 512', video_dir + 'UNSER_KRAUT_HERBST_20261016_VORSCHAU_768x512.mp4'),
        ('AVI-Alternative für den LED-Controller', video_dir + 'UNSER_KRAUT_HERBST_20261016_192x128_KOMPATIBEL.avi'),
        ('Original und Neu synchron vergleichen / alle 54 Tafeln', project_dir + 'VORSCHAU.html'),
        ('Bearbeitbares Blender-Projekt', project_dir + 'UNSER_KRAUT_HERBST_3D.blend'),
        ('Herbst-Show: Inhalt, Bildquellen und Neu-Rendern', project_dir + 'README.md'),
        ('Gesamtes Projekt / README', 'README.md'),
        ('Mit eigenem Codex bearbeiten / Startauftrag', 'START-HIER.md'),
        ('Dieselben Herstellungswerkzeuge einrichten', 'TOOLCHAIN.md'),
        ('Bewertung für Laufkundschaft am Bahnhof', project_dir + 'BAHNHOF-PRUEFUNG.md'),
        ('Display-Register und Geräteeinstellungen', 'ledshow-seefeld/display-register.md'),
        ('PC-übergreifendes Arbeiten und gemeinsame Projektkopie', 'PC-UEBERGREIFEND.md'),
        ('Ablageplan und zukünftige Veröffentlichungen', 'ledshow-seefeld/NAS-ABLAGE.md'),
        ('Dateiliste mit SHA-256', 'DATEIMANIFEST.json'),
        ('Abschließendes Prüfprotokoll', 'PRUEFPROTOKOLL.json'),
    ]
    title = 'Unser Kraut – Herbst-Show 16.10.2026'
    description = 'Vollständige Fassung: 54 Originaltafeln, 3:28 Minuten. Videos ohne Ton. Die MP4 mit 192 × 128 Pixeln ist für das Schaufenster-LED vorgesehen.'
    primary_video = video_dir + 'UNSER_KRAUT_HERBST_20261016_192x128.mp4'
    technical_checks = project_dir + 'export_verification.json'
    if args.show_config:
        config_path = (root / args.show_config).resolve()
        if root not in config_path.parents or config_path.relative_to(root).as_posix() not in paths:
            raise RuntimeError('Show configuration must be a Git-tracked file within the project.')
        config = json.loads(config_path.read_text(encoding='utf-8'))
        title = config['title']
        description = config['description']
        primary_video = config['primary_video']
        project_dir = config['project_dir'].rstrip('/') + '/'
        technical_checks = config['technical_checks']
        links = [(item['label'], item['path']) for item in config['links']]
    if primary_video not in paths or technical_checks not in paths:
        raise RuntimeError('Primary video and technical checks must be present in the selected commit.')
    for _, relative in links:
        if relative not in {'DATEIMANIFEST.json', 'PRUEFPROTOKOLL.json'} and relative not in paths:
            raise RuntimeError(f'Start page link is missing from Git: {relative}')
    items = ''.join(f'<li><a href="{html.escape(link, quote=True)}">{html.escape(label)}</a></li>' for label, link in links)
    generated = {
        'START.html': ('<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            f'<title>{html.escape(title)}</title><style>body{{font:18px/1.6 system-ui;max-width:1000px;margin:40px auto;padding:0 24px;background:#10180e;color:#edf4e7}}a{{color:#c3ed83}}li{{margin:12px 0}}code{{overflow-wrap:anywhere}}</style>'
            f'<h1>{html.escape(title)}</h1><p>{html.escape(description)}</p>'
            f'<ul>{items}</ul><p>Vollständiger Projektstand: <code>{commit}</code>. Alle versionierten Projektdateien einschließlich älterer Shows sind enthalten. Kein Git-Verzeichnis und keine laufenden Renderjobs.</p>'
            '<p>Die technische Videoprüfung ist abgeschlossen; die Wiedergabe am echten LED-Controller bleibt vor Ort zu testen.</p></html>'),
        'ABLAGE.md': (f'# Archiv: {title}\n\n'
            f'{description}\n\nSTART.html öffnet Videos, Blender-Projekt, Vorschau und Dokumentation.\n\n'
            f'Dieser Ordner ist eine eigenständige Momentaufnahme aller Git-versionierten Projektdateien aus Commit `{commit}`. '
            'Die gewohnte Ordnerstruktur bleibt erhalten, damit Vorschauen und relative Bildpfade funktionieren. '
            'Ältere Projektfassungen im übergeordneten Schaufenster-Display-Ordner bleiben unverändert.\n\n'
            f'Die aktuelle LED-Datei liegt unter `{primary_video}`. '
            f'Vorschau und AVI-Alternative liegen daneben. Quellprojekt, Produktbilder, Quellenliste, Storyboard, technische Prüfung und Vorschau liegen unter `{project_dir}`.\n\n'
            'DATEIMANIFEST.json nennt jede Nutzdatei mit Größe und SHA-256. CHECKSUMS.sha256 enthält dieselben Prüfsummen. '
            'PRUEFPROTOKOLL.json wird erst nach erfolgreicher Prüfung aller Zieldateien erstellt. Diese drei Verwaltungsdateien sind vom eigenen Inhaltsmanifest ausgenommen.\n\n'
            'Zum Bearbeiten einen lokalen Git-Clone verwenden. Die gemeinsame Arbeitskopie liegt unter '
            '`\\\\nas-christoph\\Business\\Codex-Projekte\\unser-kraut-ledshow-seefeld`. '
            'Der Ablauf steht in PC-UEBERGREIFEND.md und ledshow-seefeld/NAS-ABLAGE.md.\n'),
    }
    for relative, content in generated.items():
        data = content.encode('utf-8')
        entries.append({'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'source': 'generated'})
    manifest = {'schema': 1, 'git_commit': commit, 'tracked_project_files': len(paths), 'files': entries,
                'excluded_metadata': ['DATEIMANIFEST.json', 'CHECKSUMS.sha256', 'PRUEFPROTOKOLL.json']}
    metadata = {
        'DATEIMANIFEST.json': json.dumps(manifest, ensure_ascii=False, indent=2) + '\n',
        'CHECKSUMS.sha256': ''.join(f"{entry['sha256']}  {entry['path']}\n" for entry in entries),
    }
    all_generated = {**generated, **metadata}

    def preflight(entry):
        destination = target / entry['path']
        if destination.exists() and (not destination.is_file() or digest(destination) != entry['sha256']):
            raise RuntimeError(f'Existing different file; nothing overwritten: {destination}')
    with futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(preflight, entries))
    for relative, content in metadata.items():
        destination = target / relative
        if destination.exists() and digest(destination) != hashlib.sha256(content.encode('utf-8')).hexdigest():
            raise RuntimeError(f'Existing different metadata; nothing overwritten: {destination}')
    target.mkdir(parents=True, exist_ok=True)

    def copy_one(entry):
        destination = target / entry['path']
        if destination.exists():
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + '.publishing')
        with temporary.open('xb', buffering=1024 * 1024) as output:
            if entry['source'] == 'generated':
                output.write(all_generated[entry['path']].encode('utf-8'))
            else:
                with (root / entry['path']).open('rb', buffering=1024 * 1024) as source:
                    for block in iter(lambda: source.read(1024 * 1024), b''):
                        output.write(block)
        temporary.rename(destination)
    with futures.ThreadPoolExecutor(max_workers=4) as pool:
        for number, _ in enumerate(pool.map(copy_one, entries), 1):
            if number % 25 == 0 or number == len(entries):
                print(f'COPIED {number}/{len(entries)}', flush=True)

    def verify(entry):
        path = target / entry['path']
        if path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
            raise RuntimeError(f'Archive verification failed: {path}')
    with futures.ThreadPoolExecutor(max_workers=4) as pool:
        for number, _ in enumerate(pool.map(verify, entries), 1):
            if number % 25 == 0 or number == len(entries):
                print(f'CHECKED {number}/{len(entries)}', flush=True)
    for relative, content in metadata.items():
        destination = target / relative
        if not destination.exists():
            with destination.open('xb') as output:
                output.write(content.encode('utf-8'))
        if digest(destination) != hashlib.sha256(content.encode('utf-8')).hexdigest():
            raise RuntimeError(f'Metadata verification failed: {destination}')
    report = {'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'git_commit': commit,
              'checked_files': len(entries), 'sha256_all_match': True,
              'tracked_project_files': len(paths), 'video_technical_checks': technical_checks,
              'physical_led_playback': 'not tested', 'existing_originals': 'untouched'}
    report_path = target / 'PRUEFPROTOKOLL.json'
    if not report_path.exists():
        with report_path.open('xb') as output:
            output.write((json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    else:
        previous = json.loads(report_path.read_text(encoding='utf-8'))
        if previous.get('git_commit') != commit or previous.get('checked_files') != len(entries) or previous.get('sha256_all_match') is not True:
            raise RuntimeError('Existing verification report belongs to a different snapshot.')
    print(json.dumps({'verified': True, 'files': len(entries), 'git_commit': commit, 'destination': str(target)}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
