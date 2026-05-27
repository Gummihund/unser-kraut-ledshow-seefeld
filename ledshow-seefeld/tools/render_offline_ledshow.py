from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "assets" / "raw"
OUT = ROOT / "output"
FRAMES = OUT / "frames"
MP4 = OUT / "mp4" / "unser-kraut-seefeld-ledshow-192x128.mp4"
GIF = OUT / "preview" / "unser-kraut-seefeld-ledshow-preview.gif"

W, H = 192, 128
FPS = 30
SCENE_SECONDS = 3.2
SCENE_FRAMES = round(FPS * SCENE_SECONDS)
BRAND_GREEN = "#43913d"

SCENES = [
    ("hanfblatt", ["UNSER", "KRAUT", "SEEFELD"], BRAND_GREEN, "leaf", ["hanfblatt-01.png"]),
    ("cbd", ["CBD", "OELE"], BRAND_GREEN, "bottle", ["cbd-oel-01.png", "cbd-oel-01.jpg"]),
    ("tee", ["TEE", "BLUETEN"], "#8ecf55", "pouch", ["hanftee-01.png", "hanftee-01.jpg"]),
    ("honig", ["HONIG", "TIROL"], "#ffc247", "jar", ["cannabee-honig-01.png", "cannabee-honig-01.jpg"]),
    ("vapes", ["VAPES", "18+"], "#ff4f91", "vape", ["vape-01.png", "vape-01.jpg"]),
    ("snacks", ["BIO", "SNACKS"], "#f3ff8c", "seeds", ["hanfsamen-01.png", "hanfsamen-01.jpg"]),
    ("pflege", ["PFLEGE", "CREME"], "#89d7ff", "cream", ["pflege-creme-01.png", "pflege-creme-01.jpg"]),
    ("tiere", ["FUER", "TIERE"], "#d4ff81", "paw", ["tierprodukt-01.png", "tierprodukt-01.jpg"]),
    ("gift", ["GESCHENK", "IDEE"], "#ffb55c", "gift", []),
    ("beratung", ["KOMM", "REIN", "BERATUNG"], BRAND_GREEN, "leaf", ["hanfblatt-01.png"]),
]


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


FONT_BIG = font(23)
FONT_MED = font(17)
FONT_SMALL = font(8)
FONT_TINY = font(7)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def smooth(t: float) -> float:
    return t * t * (3 - 2 * t)


def load_asset(candidates: list[str]) -> Image.Image | None:
    for candidate in candidates:
        path = RAW / candidate
        if path.exists():
            img = Image.open(path).convert("RGBA")
            return trim_white(img)
    return None


def trim_white(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    px = rgba.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and r > 238 and g > 238 and b > 238:
                px[x, y] = (r, g, b, 0)
    bbox = rgba.getbbox()
    return rgba.crop(bbox) if bbox else rgba


ASSETS = {scene[0]: load_asset(scene[4]) for scene in SCENES}


def draw_background(draw: ImageDraw.ImageDraw, img: Image.Image, accent: str, t: float) -> None:
    draw.rectangle((0, 0, W, H), fill=(5, 8, 5))
    ar, ag, ab = hex_to_rgb(accent)
    pulse = math.sin(t * math.tau) * 0.5 + 0.5
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(96, 2, -3):
        a = int((1 - r / 96) * (54 + pulse * 18))
        gd.ellipse((132 - r, 56 - r, 132 + r, 56 + r), fill=(ar, ag, ab, a))
    img.alpha_composite(glow)
    for x in range(-80, W + 60, 18):
        draw.line((round(x + t * 22), 0, round(x + t * 22), H), fill=(67, 145, 61, 28))
    draw.line((0, 120, 42, 113, 78, 124, 112, 116, 153, 103, 192, 106), fill=(ar, ag, ab, 120), width=1)


def draw_product(base: Image.Image, draw: ImageDraw.ImageDraw, scene_id: str, kind: str, accent: str, ease: float, t: float) -> None:
    asset = ASSETS.get(scene_id)
    cx = 132 + math.sin(t * math.tau) * 3
    cy = 64 - (1 - ease) * 18
    if asset:
        size = 74 if scene_id in {"hanfblatt", "beratung"} else 82
        size = round(size + ease * 5)
        product = asset.copy()
        product.thumbnail((size, size), Image.Resampling.LANCZOS)
        product = ImageEnhance.Contrast(product).enhance(1.14)
        product = product.filter(ImageFilter.SHARPEN)
        shadow = Image.new("RGBA", product.size, (*hex_to_rgb(accent), 0))
        alpha = product.getchannel("A").filter(ImageFilter.GaussianBlur(5))
        shadow.putalpha(alpha)
        x = round(cx - product.width / 2)
        y = round(28 - (1 - ease) * 12 if scene_id not in {"hanfblatt", "beratung"} else cy - product.height / 2)
        base.alpha_composite(shadow, (x + 2, y + 2))
        base.alpha_composite(product, (x, y))
        return

    ar, ag, ab = hex_to_rgb(accent)
    fill = (246, 255, 233, 255)
    outline = (ar, ag, ab, 255)
    x, y = round(cx), round(cy)
    if kind == "bottle":
        draw.rounded_rectangle((x - 13, y - 35, x + 13, y + 30), 7, fill=(66, 39, 19), outline=outline, width=2)
        draw.rounded_rectangle((x - 9, y - 48, x + 9, y - 33), 4, fill=(17, 17, 17), outline=outline, width=2)
        draw.rounded_rectangle((x - 15, y - 13, x + 15, y + 12), 4, fill=fill, outline=outline, width=2)
        draw.text((x - 10, y - 6), "CBD", fill=outline, font=FONT_SMALL)
    elif kind == "pouch":
        draw.rounded_rectangle((x - 25, y - 36, x + 25, y + 34), 7, fill=(232, 240, 212), outline=outline, width=2)
        draw.rectangle((x - 19, y - 20, x + 19, y + 16), fill=(31, 50, 29))
        draw.text((x - 11, y - 8), "TEE", fill=outline, font=FONT_SMALL)
    elif kind == "jar":
        draw.rounded_rectangle((x - 21, y - 24, x + 21, y + 28), 9, fill=(246, 178, 63), outline=outline, width=2)
        draw.rounded_rectangle((x - 15, y - 36, x + 15, y - 22), 5, fill=(247, 230, 176), outline=outline, width=2)
        draw.text((x - 16, y), "HONIG", fill=(42, 26, 11), font=FONT_SMALL)
    else:
        draw_leaf(draw, x, y, outline)


def draw_leaf(draw: ImageDraw.ImageDraw, x: int, y: int, color: tuple[int, int, int, int]) -> None:
    for i in range(-3, 4):
        angle = i * 0.38 - math.pi / 2
        ex = x + math.cos(angle) * 22
        ey = y + math.sin(angle) * 22
        draw.ellipse((ex - 8, ey - 18, ex + 8, ey + 18), fill=color, outline=(246, 255, 233, 255), width=1)
    draw.rectangle((x - 2, y + 2, x + 2, y + 35), fill=(246, 255, 233, 255))


def draw_words(draw: ImageDraw.ImageDraw, words: list[str], accent: str, scene_id: str, ease: float) -> None:
    x = 10
    y = 32 if len(words) == 3 else 42
    fnt = FONT_MED if any(len(word) > 6 for word in words) else FONT_BIG
    step = 20 if fnt == FONT_MED else 26
    for i, word in enumerate(words):
        yy = y + i * step
        fill = accent if i == len(words) - 1 and scene_id != "cbd" else "#f6ffe9"
        draw.text((x - 1, yy), word, fill=(0, 0, 0), font=fnt, stroke_width=2, stroke_fill=(0, 0, 0))
        draw.text((x, yy), word, fill=fill, font=fnt)
    draw.rectangle((10, 96, round(54 + ease * 18), 99), fill=accent)


def draw_frame(scene_index: int, frame_in_scene: int) -> Image.Image:
    scene_id, words, accent, kind, _ = SCENES[scene_index]
    t = frame_in_scene / SCENE_FRAMES
    ease = smooth(t)
    img = Image.new("RGBA", (W, H), (5, 8, 5, 255))
    draw = ImageDraw.Draw(img)
    draw_background(draw, img, accent, t)
    draw_product(img, draw, scene_id, kind, accent, ease, t)
    draw_words(draw, words, accent, scene_id, ease)
    bottom = "WIR BERATEN GERN" if scene_id == "beratung" else "UNSER-KRAUT.AT"
    draw.text((8, 115), bottom, fill=accent if scene_id != "beratung" else "#f6ffe9", font=FONT_TINY)
    if scene_id == "vapes":
        draw.rectangle((159, 9, 183, 23), fill="#f6ffe9")
        draw.text((163, 11), "18+", fill="#111111", font=FONT_SMALL)
    for yy in range(frame_in_scene % 4, H, 4):
        draw.line((0, yy, W, yy), fill=(0, 0, 0, 60))
    draw.rectangle((0, 0, W - 1, H - 1), outline=(255, 255, 255, 14))
    return img.convert("RGB")


def clean_output() -> None:
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True, exist_ok=True)
    MP4.parent.mkdir(parents=True, exist_ok=True)
    GIF.parent.mkdir(parents=True, exist_ok=True)


def render_frames() -> list[Image.Image]:
    frames_for_gif: list[Image.Image] = []
    idx = 0
    for scene_index in range(len(SCENES)):
        for frame_in_scene in range(SCENE_FRAMES):
            frame = draw_frame(scene_index, frame_in_scene)
            frame.save(FRAMES / f"frame_{idx:04d}.png", optimize=True)
            if frame_in_scene % 3 == 0:
                frames_for_gif.append(frame.copy())
            idx += 1
    return frames_for_gif


def render_gif(frames: list[Image.Image]) -> None:
    big = [frame.resize((768, 512), Image.Resampling.NEAREST) for frame in frames]
    big[0].save(GIF, save_all=True, append_images=big[1:], duration=100, loop=0, optimize=False)


def render_mp4_if_possible() -> bool:
    try:
        import imageio.v3 as iio
    except ModuleNotFoundError:
        return False
    frames = [iio.imread(path) for path in sorted(FRAMES.glob("frame_*.png"))]
    iio.imwrite(MP4, frames, fps=FPS, codec="libx264", pixelformat="yuv420p", macro_block_size=1)
    return True


def main() -> None:
    clean_output()
    frames = render_frames()
    render_gif(frames)
    mp4_ok = render_mp4_if_possible()
    print(f"Frames: {FRAMES}")
    print(f"GIF preview: {GIF}")
    print(f"MP4: {MP4 if mp4_ok else 'imageio/imageio-ffmpeg fehlt'}")


if __name__ == "__main__":
    main()
