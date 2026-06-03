const canvas = document.querySelector("#led");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const W = canvas.width;
const H = canvas.height;
const FPS = 30;
const sceneSeconds = 3.2;
const sceneFrames = Math.round(sceneSeconds * FPS);
const BRAND_GREEN = "#43913d";
const LED_GREEN = "#72ff32";

const scenes = [
  { id: "brand", name: "Hanfblatt", words: ["UNSER", "KRAUT", "SEEFELD"], accent: LED_GREEN, product: "leaf", assets: ["../assets/raw/hanfblatt-01.png"] },
  { id: "cbd", name: "CBD Oele", words: ["CBD", "OELE"], accent: BRAND_GREEN, product: "bottle", assets: ["../assets/raw/cbd-oel-10prozent-premium.jpg", "../assets/raw/cbd-oel-01.png", "../assets/raw/cbd-oel-01.jpg"] },
  { id: "tee", name: "Hanf Tee", words: ["HANF", "TEE"], accent: "#8ecf55", product: "pouch", assets: ["../assets/raw/hanftee-blaetter-01.jpg", "../assets/raw/hanftee-01.jpg", "../assets/raw/hanftee-kraeuter-01.jpg"] },
  { id: "honig", name: "Honig Tirol", words: ["HONIG", "TIROL"], accent: "#ffc247", product: "jar", assets: ["../assets/raw/cannabee-honig-02.jpg", "../assets/raw/cannabee-honig-01.png", "../assets/raw/cannabee-honig-01.jpg"] },
  { id: "vapes", name: "Vapes 18+", words: ["VAPES", "18+"], accent: "#ff4f91", product: "vape", assets: ["../assets/raw/vape-mesh-himbeere.png", "../assets/raw/vape-01.png", "../assets/raw/vape-01.jpg"] },
  { id: "snacks", name: "Seefeld Snack", words: ["SEEFELD", "SNACK"], accent: "#f3ff8c", product: "seeds", assets: ["../assets/raw/seefeld-schokolade-3er-01.jpg", "../assets/raw/hanf-snack-schokolade-01.jpg"] },
  { id: "pflege", name: "Pflege Creme", words: ["PFLEGE", "CREME"], accent: "#89d7ff", product: "cream", assets: ["../assets/raw/pflege-creme-01.jpg"] },
  { id: "tiere", name: "Fuer Tiere", words: ["FUER", "TIERE"], accent: "#d4ff81", product: "paw", assets: ["../assets/raw/tier-cbd-oel-5prozent-01.jpg"] },
  { id: "gift", name: "Geschenk Idee", words: ["SEEFELD", "GESCHENK"], accent: "#ffb55c", product: "gift", assets: ["../assets/raw/hanf-snack-schokolade-01.jpg", "../assets/raw/geschenk-emailletasse-01.jpg"] },
  { id: "cta", name: "Beratung", words: ["KOMM REIN", "WIR BERATEN", "DICH GERNE"], accent: LED_GREEN, product: "leaf", assets: ["../assets/raw/hanfblatt-01.png"] },
];

const totalFrames = scenes.length * sceneFrames;
const imageCache = new Map();
let startTime = performance.now();
let paused = false;
let pauseAt = 0;
let activeIndex = -1;

const sceneName = document.querySelector("#sceneName");
const timecode = document.querySelector("#timecode");
const progress = document.querySelector("#progress");
const toggle = document.querySelector("#toggle");
const restart = document.querySelector("#restart");
const sceneList = document.querySelector("#scenes");

sceneList.innerHTML = scenes
  .map((scene, index) => `<li data-scene="${index}"><span>${scene.name}</span><span>${scene.words.join(" ")}</span></li>`)
  .join("");

for (const scene of scenes) {
  for (const asset of scene.assets || []) {
    const img = new Image();
    img.src = asset;
    img.onload = () => {
      if (!imageCache.has(scene.id)) imageCache.set(scene.id, img);
    };
  }
}

toggle.addEventListener("click", () => {
  paused = !paused;
  if (paused) {
    pauseAt = performance.now();
    toggle.textContent = "Play";
  } else {
    startTime += performance.now() - pauseAt;
    toggle.textContent = "Pause";
    requestAnimationFrame(loop);
  }
});

restart.addEventListener("click", () => {
  startTime = performance.now();
  paused = false;
  toggle.textContent = "Pause";
});

function loop(now) {
  if (paused) return;
  const elapsed = (now - startTime) / 1000;
  drawShow(elapsed);
  requestAnimationFrame(loop);
}

function drawShow(seconds) {
  const frame = Math.floor(seconds * FPS) % totalFrames;
  const sceneIndex = Math.floor(frame / sceneFrames);
  const sceneFrame = frame % sceneFrames;
  const scene = scenes[sceneIndex];
  const t = sceneFrame / sceneFrames;
  const ease = smooth(t);

  drawBackground(scene, t);
  drawScanlines(t);
  drawProduct(scene, ease, t);
  drawWords(scene, ease);
  drawCornerInfo(scene, t);

  if (sceneIndex !== activeIndex) updateSceneUi(sceneIndex);
  sceneName.textContent = scene.name;
  timecode.textContent = `${seconds.toFixed(1)}s`;
  progress.style.width = `${((frame + 1) / totalFrames) * 100}%`;
}

function updateSceneUi(index) {
  activeIndex = index;
  for (const item of sceneList.children) item.classList.toggle("active", Number(item.dataset.scene) === index);
}

function drawBackground(scene, t) {
  ctx.fillStyle = "#050805";
  ctx.fillRect(0, 0, W, H);

  const pulse = Math.sin(t * Math.PI * 2) * 0.5 + 0.5;
  const grad = ctx.createRadialGradient(132, 56, 2, 132, 56, 112);
  grad.addColorStop(0, hexAlpha(scene.accent, 0.42 + pulse * 0.12));
  grad.addColorStop(0.36, hexAlpha(scene.accent, 0.12));
  grad.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);

  ctx.fillStyle = "rgba(67,145,61,0.11)";
  for (let x = -80; x < W + 60; x += 18) {
    ctx.fillRect(Math.round(x + t * 22), 0, 1, H);
  }

  ctx.strokeStyle = hexAlpha(scene.accent, 0.5);
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(0, 120);
  ctx.bezierCurveTo(44, 110, 68, 134, 110, 116);
  ctx.bezierCurveTo(150, 100, 164, 116, 192, 104);
  ctx.stroke();
}

function drawScanlines(t) {
  ctx.fillStyle = "rgba(0,0,0,0.24)";
  for (let y = Math.floor(t * 4) % 4; y < H; y += 4) {
    ctx.fillRect(0, y, W, 1);
  }
  ctx.strokeStyle = "rgba(255,255,255,0.05)";
  ctx.strokeRect(0.5, 0.5, W - 1, H - 1);
}

function drawWords(scene, ease) {
  const x = 10;
  if (scene.id === "cta") {
    const lines = ["KOMM REIN", "WIR BERATEN", "DICH GERNE"];
    ctx.textBaseline = "top";
    ctx.font = "900 14px Arial";
    ctx.lineWidth = 3;
    lines.forEach((word, i) => {
      const yy = 25 + i * 18;
      ctx.strokeStyle = "rgba(0,0,0,0.88)";
      ctx.fillStyle = i === 2 ? scene.accent : "#f6ffe9";
      ctx.strokeText(word, x, yy);
      ctx.fillText(word, x, yy);
    });
    ctx.fillStyle = scene.accent;
    ctx.fillRect(10, 86, 48 + ease * 18, 3);
    return;
  }

  const y = scene.words.length === 3 ? 32 : 42;
  const fontSize = scene.words.some((word) => word.length > 6) ? 17 : 23;

  ctx.textBaseline = "top";
  ctx.font = `900 ${fontSize}px Arial`;
  ctx.lineWidth = 3;

  scene.words.forEach((word, i) => {
    const yy = y + i * (fontSize + 3);
    ctx.strokeStyle = "rgba(0,0,0,0.86)";
    ctx.fillStyle = i === scene.words.length - 1 && scene.id !== "cbd" ? scene.accent : "#f6ffe9";
    ctx.strokeText(word, x, yy);
    ctx.fillText(word, x, yy);
  });

  ctx.fillStyle = scene.accent;
  ctx.fillRect(10, 96, 44 + ease * 18, 3);
}

function drawCornerInfo(scene, t) {
  if (scene.id === "cta") {
    roundRect(8, 111, 65, 14, 4, "#050805", scene.accent);
    ctx.font = "900 8px Arial";
    ctx.fillStyle = "#f6ffe9";
    ctx.fillText("IM SHOP", 13, 113);
  }

  if (scene.id === "vapes") {
    ctx.fillStyle = "#f6ffe9";
    ctx.fillRect(159, 9, 24, 14);
    ctx.fillStyle = "#111";
    ctx.font = "900 10px Arial";
    ctx.fillText("18+", 163, 11);
  }

  const blink = Math.floor(t * 8) % 2 === 0;
  ctx.fillStyle = blink ? hexAlpha(scene.accent, 0.9) : "rgba(255,255,255,0.18)";
  ctx.fillRect(181, 116, 3, 3);
  ctx.fillRect(186, 116, 3, 3);
}

function drawProduct(scene, ease, t) {
  const img = imageCache.get(scene.id);
  if (img) {
    const sizes = { brand: 88, cta: 70, honig: 94, snacks: 104, pflege: 92, tiere: 94, gift: 90 };
    const size = (sizes[scene.id] || 82) + ease * 5;
    const ratio = img.width && img.height ? img.width / img.height : 1;
    const dw = ratio >= 1 ? size : size * ratio;
    const dh = ratio >= 1 ? size / ratio : size;
    const centerX = (scene.id === "cta" ? 146 : 132) + Math.sin(t * Math.PI * 2) * 2;
    const x = centerX - dw / 2;
    const y = scene.id === "brand" || scene.id === "cta" ? 64 - dh / 2 - (1 - ease) * 18 : 30 - (1 - ease) * 12;
    ctx.save();
    ctx.shadowColor = scene.id === "pflege" ? "rgba(0,0,0,0.34)" : scene.accent;
    ctx.shadowBlur = scene.id === "pflege" ? 5 : 13;
    ctx.shadowOffsetX = scene.id === "pflege" ? 2 : 0;
    ctx.shadowOffsetY = scene.id === "pflege" ? 4 : 0;
    if (scene.id === "brand" || scene.id === "cta") {
      drawTintedImage(img, x, y, dw, dh, scene.accent);
    } else {
      ctx.drawImage(img, x, y, dw, dh);
    }
    ctx.restore();
    return;
  }

  const cx = 132 + Math.sin(t * Math.PI * 2) * 3;
  const cy = 64 - (1 - ease) * 18;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.scale(0.92 + ease * 0.08, 0.92 + ease * 0.08);
  ctx.shadowColor = scene.accent;
  ctx.shadowBlur = 13;
  ctx.fillStyle = "#f8fff0";
  ctx.strokeStyle = scene.accent;
  ctx.lineWidth = 2;

  if (scene.product === "bottle") drawBottle(scene.accent);
  if (scene.product === "pouch") drawPouch(scene.accent);
  if (scene.product === "jar") drawJar(scene.accent);
  if (scene.product === "vape") drawVape(scene.accent);
  if (scene.product === "seeds") drawSeeds(scene.accent);
  if (scene.product === "cream") drawCream(scene.accent);
  if (scene.product === "paw") drawPaw(scene.accent);
  if (scene.product === "gift") drawGift(scene.accent);
  if (scene.product === "leaf") drawLeaf(scene.accent);

  ctx.restore();
}

function drawTintedImage(img, x, y, w, h, color) {
  const off = document.createElement("canvas");
  off.width = Math.max(1, Math.round(w));
  off.height = Math.max(1, Math.round(h));
  const offCtx = off.getContext("2d");
  offCtx.drawImage(img, 0, 0, off.width, off.height);
  offCtx.globalCompositeOperation = "source-in";
  offCtx.fillStyle = color;
  offCtx.fillRect(0, 0, off.width, off.height);
  ctx.drawImage(off, x, y);
}

function drawBottle(accent) {
  roundRect(-13, -35, 26, 65, 7, "#422713", accent);
  roundRect(-9, -48, 18, 15, 4, "#111", accent);
  roundRect(-15, -13, 30, 25, 4, "#f9ffe9", accent);
  ctx.fillStyle = accent;
  ctx.font = "900 9px Arial";
  ctx.fillText("CBD", -10, -6);
}

function drawPouch(accent) {
  roundRect(-25, -36, 50, 70, 7, "#e8f0d4", accent);
  ctx.fillStyle = "#1f321d";
  ctx.fillRect(-19, -20, 38, 36);
  ctx.fillStyle = accent;
  ctx.font = "900 10px Arial";
  ctx.fillText("TEE", -11, -8);
}

function drawJar(accent) {
  roundRect(-21, -24, 42, 52, 9, "#f6b23f", accent);
  roundRect(-15, -36, 30, 14, 5, "#f7e6b0", accent);
  ctx.fillStyle = "#2a1a0b";
  ctx.font = "900 9px Arial";
  ctx.fillText("HONIG", -16, 0);
}

function drawVape(accent) {
  ctx.rotate(-0.24);
  roundRect(-7, -45, 14, 86, 7, "#101010", accent);
  ctx.fillStyle = accent;
  ctx.fillRect(-4, -22, 8, 37);
  ctx.fillStyle = "#f6ffe9";
  ctx.fillRect(-4, -38, 8, 7);
}

function drawSeeds(accent) {
  ctx.fillStyle = "#f6ffe9";
  for (let i = 0; i < 18; i++) {
    const a = i * 1.75;
    const r = 8 + (i % 4) * 5;
    ellipse(Math.cos(a) * r, Math.sin(a) * r, 5, 3, a, "#d9c16a", accent);
  }
  roundRect(-27, 16, 54, 18, 6, "#1c2818", accent);
  ctx.fillStyle = accent;
  ctx.font = "900 8px Arial";
  ctx.fillText("BIO", -8, 20);
}

function drawCream(accent) {
  roundRect(-22, -18, 44, 46, 8, "#f6ffe9", accent);
  roundRect(-16, -33, 32, 16, 5, "#dbf6ff", accent);
  ctx.fillStyle = "#173326";
  ctx.font = "900 8px Arial";
  ctx.fillText("CREME", -16, 1);
}

function drawPaw(accent) {
  ellipse(0, 10, 17, 14, 0, "#f6ffe9", accent);
  ellipse(-19, -8, 8, 10, -0.4, "#f6ffe9", accent);
  ellipse(-6, -17, 8, 11, -0.1, "#f6ffe9", accent);
  ellipse(8, -16, 8, 11, 0.1, "#f6ffe9", accent);
  ellipse(21, -7, 8, 10, 0.4, "#f6ffe9", accent);
}

function drawGift(accent) {
  roundRect(-27, -11, 54, 39, 5, "#f6ffe9", accent);
  ctx.fillStyle = accent;
  ctx.fillRect(-4, -11, 8, 39);
  ctx.fillRect(-27, 3, 54, 8);
  ctx.strokeStyle = accent;
  ctx.strokeRect(-13, -29, 13, 18);
  ctx.strokeRect(0, -29, 13, 18);
}

function drawLeaf(accent) {
  ctx.fillStyle = accent;
  ctx.strokeStyle = "#f6ffe9";
  ctx.lineWidth = 1.5;
  for (let i = -3; i <= 3; i++) {
    ctx.save();
    ctx.rotate(i * 0.34);
    ellipse(0, -21, 10, 31, 0, accent, "#f6ffe9");
    ctx.restore();
  }
  ctx.fillStyle = "#f6ffe9";
  ctx.fillRect(-2, 3, 4, 35);
}

function roundRect(x, y, w, h, r, fill, stroke) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.strokeStyle = stroke;
  ctx.stroke();
}

function ellipse(x, y, rx, ry, rot, fill, stroke) {
  ctx.beginPath();
  ctx.ellipse(x, y, rx, ry, rot, 0, Math.PI * 2);
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.strokeStyle = stroke;
  ctx.stroke();
}

function smooth(t) {
  return t * t * (3 - 2 * t);
}

function hexAlpha(hex, alpha) {
  const n = Number.parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}

requestAnimationFrame(loop);
