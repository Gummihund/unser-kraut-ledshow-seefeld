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
LED_GREEN = "#72ff32"

SCENES = [
    ("hanfblatt", ["UNSER", "KRAUT", "SEEFELD"], LED_GREEN, "leaf", ["hanfblatt-01.png"]),
    ("cbd", ["CBD", "OELE"], BRAND_GREEN, "bottle", ["cbd-oel-10prozent-premium.jpg", "cbd-oel-01.png", "cbd-oel-01.jpg"]),
    ("tee", ["HANF", "TEE"], "#8ecf55", "pouch", ["hanftee-blaetter-01.jpg", "hanftee-01.jpg", "hanftee-kraeuter-01.jpg"]),
    ("honig", ["HONIG", "TIROL"], "#ffc247", "jar", ["cannabee-honig-02.jpg", "cannabee-honig-01.png", "cannabee-honig-01.jpg"]),
    ("vapes", ["VAPES", "18+"], "#ff4f91", "vape", ["vape-mesh-himbeere.png", "vape-01.png", "vape-01.jpg"]),
    ("snacks", ["SEEFELD", "SNACK"], "#f3ff8c", "seeds", ["seefeld-schokolade-3er-01.jpg", "hanf-snack-schokolade-01.jpg"]),
    ("pflege", ["PFLEGE", "CREME"], "#89d7ff", "cream", ["pflege-creme-01.jpg"]),
    ("tiere", ["FUER", "TIERE"], "#d4ff81", "paw", ["tier-cbd-oel-5prozent-01.jpg"]),
    ("gift", ["SEEFELD", "GESCHENK"], "#ffb55c", "gift", ["hanf-snack-schokolade-01.jpg", "geschenk-emailletasse-01.jpg"]),
    ("beratung", ["KOMM", "REIN", "BERATUNG"], LED_GREEN, "leaf", ["hanfblatt-01.png"]),
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
FONT_CTA = font(14)
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
            if "hanfblatt" in candidate:
                return tint_leaf(img, LED_GREEN)
            if "pflege-creme" in candidate:
                return prepare_care_asset(img)
            return trim_white(img)
    return None


def prepare_care_asset(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    w, h = rgba.size
    crop = rgba.crop((round(w * 0.12), round(h * 0.04), round(w * 0.86), round(h * 0.96)))
    cw, ch = crop.size
    out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    src = crop.load()
    dst = out.load()
    box_limit = round(cw * 0.55)
    for y in range(ch):
        for x in range(box_limit):
            r, g, b, a = src[x, y]
            if a and not (r > 242 and g > 242 and b > 242):
                dst[x, y] = (r, g, b, a)

    draw = ImageDraw.Draw(out)
    bottle_x = round(cw * 0.61)
    bottle_y = round(ch * 0.10)
    bottle_w = round(cw * 0.26)
    bottle_h = round(ch * 0.82)
    draw.rounded_rectangle(
        (bottle_x, bottle_y, bottle_x + bottle_w, bottle_y + bottle_h),
        radius=round(bottle_w * 0.18),
        fill=(255, 255, 250, 255),
        outline=(226, 242, 246, 220),
        width=2,
    )
    draw.rounded_rectangle(
        (
            bottle_x + round(bottle_w * 0.14),
            bottle_y + round(bottle_h * 0.06),
            bottle_x + bottle_w - round(bottle_w * 0.14),
            bottle_y + round(bottle_h * 0.22),
        ),
        radius=round(bottle_w * 0.10),
        fill=(255, 255, 255, 255),
        outline=(235, 238, 238, 210),
        width=1,
    )
    label_y = bottle_y + round(bottle_h * 0.66)
    draw.rectangle((bottle_x + 4, label_y, bottle_x + bottle_w - 4, label_y + 4), fill=(157, 47, 77, 255))
    draw.rectangle((bottle_x + 8, label_y + 12, bottle_x + bottle_w - 8, label_y + 14), fill=(157, 47, 77, 220))
    return out


def tint_leaf(img: Image.Image, color: str) -> Image.Image:
    rgba = img.convert("RGBA")
    tinted = Image.new("RGBA", rgba.size, (*hex_to_rgb(color), 0))
    alpha = Image.new("L", rgba.size, 0)
    src = rgba.load()
    dst = alpha.load()
    w, h = rgba.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = src[x, y]
            if not a:
                continue
            darkness = 255 - min(255, (r + g + b) // 3)
            dst[x, y] = max(0, min(255, round(a * darkness / 255)))
    tinted.putalpha(alpha.filter(ImageFilter.GaussianBlur(0.25)))
    bbox = tinted.getbbox()
    return tinted.crop(bbox) if bbox else tinted


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
    cx = (146 if scene_id == "beratung" else 132) + math.sin(t * math.tau) * 3
    cy = 64 - (1 - ease) * 18
    if asset:
        size = {
            "hanfblatt": 88,
            "beratung": 70,
            "honig": 94,
            "snacks": 104,
            "pflege": 92,
            "tiere": 94,
            "gift": 90,
        }.get(scene_id, 82)
        size = round(size + ease * 5)
        product = asset.copy()
        product.thumbnail((size, size), Image.Resampling.LANCZOS)
        product = ImageEnhance.Contrast(product).enhance(1.14)
        product = product.filter(ImageFilter.SHARPEN)
        x = round(cx - product.width / 2)
        if scene_id in {"hanfblatt", "beratung"}:
            y = round(cy - product.height / 2)
        else:
            y = round(30 - (1 - ease) * 12)
        if scene_id != "pflege":
            shadow = Image.new("RGBA", product.size, (*hex_to_rgb(accent), 0))
            alpha = product.getchannel("A").filter(ImageFilter.GaussianBlur(5))
            alpha = alpha.point(lambda value: round(value * 0.76))
            shadow.putalpha(alpha)
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
    if scene_id == "beratung":
        cta_lines = ["KOMM REIN", "WIR BERATEN", "DICH GERNE"]
        for i, word in enumerate(cta_lines):
            yy = 25 + i * 18
            fill = accent if i == 2 else "#f6ffe9"
            draw.text((x - 1, yy), word, fill=(0, 0, 0), font=FONT_CTA, stroke_width=2, stroke_fill=(0, 0, 0))
            draw.text((x, yy), word, fill=fill, font=FONT_CTA)
        draw.rectangle((10, 86, round(58 + ease * 18), 89), fill=accent)
        return

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
    if scene_id == "beratung":
        draw.rounded_rectangle((8, 111, 73, 125), radius=4, fill=(5, 8, 5), outline=accent, width=1)
        draw.text((13, 113), "IM SHOP", fill="#f6ffe9", font=FONT_SMALL)
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
