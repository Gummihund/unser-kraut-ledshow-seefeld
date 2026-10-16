"""Validate an LED export independently of its production scripts; never edits video."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg


def check(path, width=192, height=128, fps=30, seconds=None):
    path = Path(path).resolve(strict=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    header = subprocess.run([ffmpeg, '-hide_banner', '-i', str(path)], capture_output=True, text=True)
    info = header.stderr
    video_lines = [line for line in info.splitlines() if re.search(r'Stream #.*Video:', line)]
    errors = []
    if header.returncode != 1 or len(video_lines) != 1:
        errors.append('Exactly one readable video stream required')
    stream = video_lines[0] if video_lines else ''
    for pattern, label in [
        (r'Video: h264 \(Constrained Baseline\)', 'H.264 Constrained Baseline'),
        (r'\byuv420p\b', 'yuv420p'),
        (rf'\b{width}x{height}\b', f'{width}x{height}'),
        (rf'\b{fps}(?:\.0+)? fps\b', f'{fps} fps'),
    ]:
        if not re.search(pattern, stream):
            errors.append(f'Missing expected format: {label}')
    if 'Audio:' in info:
        errors.append('Audio stream present')
    if re.search(r'rotate\s*:|rotation of', info, re.IGNORECASE):
        errors.append('Rotation metadata present; remove before LED export')
    decoded = subprocess.run([ffmpeg, '-v', 'error', '-noautorotate', '-i', str(path),
                              '-map', '0:v:0', '-progress', 'pipe:1', '-f', 'null', '-'],
                             capture_output=True, text=True)
    counts = re.findall(r'^frame=(\d+)', decoded.stdout, re.MULTILINE)
    frames = int(counts[-1]) if counts else 0
    if decoded.returncode or decoded.stderr.strip() or frames == 0:
        errors.append('Full decode failed: ' + decoded.stderr.strip())
    if seconds is not None and frames != round(seconds * fps):
        errors.append(f'Expected {round(seconds * fps)} frames; got {frames}')
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return {'file': path.name, 'sha256': digest.hexdigest(), 'bytes': path.stat().st_size,
            'expected_width': width, 'expected_height': height, 'expected_fps': fps,
            'decoded_frames': frames, 'duration_from_frames': frames / fps,
            'audio_present': 'Audio:' in info, 'video_stream': stream.strip(),
            'errors': errors, 'passed': not errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--width', type=int, default=192)
    parser.add_argument('--height', type=int, default=128)
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--seconds', type=float)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if min(args.width, args.height, args.fps) <= 0 or (args.seconds is not None and args.seconds <= 0):
        parser.error('Dimensions, fps and duration must be positive')
    result = check(args.file, args.width, args.height, args.fps, args.seconds)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(output + '\n', encoding='utf-8')
    print(output)
    raise SystemExit(0 if result['passed'] else 1)
