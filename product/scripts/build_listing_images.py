"""Render Etsy listing images (2700x2025, 4:3) from the planner PDF."""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PDF = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
W, H = 2700, 2025
FD = "/usr/share/fonts/truetype/crosextra"
CREAM, INK, SAGE, SAGE_LT, PEACH, PEACH_LT, MUTED = (
    "#FBF8F2", "#2F3A36", "#7C9A87", "#E3ECE5", "#F2C9B0", "#FBEDE3", "#7A8580")


def font(name, size):
    return ImageFont.truetype(f"{FD}/{name}.ttf", size)


tmp = Path(tempfile.mkdtemp())
subprocess.run(["pdftoppm", "-r", "150", "-png", str(PDF), str(tmp / "p")], check=True)
PAGES = sorted(tmp.glob("p-*.png"))
pg = lambda n: Image.open(PAGES[n - 1]).convert("RGB")  # 1-indexed
IDX = {"cover": 1, "how": 2, "goals": 3, "year": 4, "jan": 5, "brain": 17, "daily": 18, "weekly": 19,
       "habit": 20, "routine": 21, "dopamine": 22, "task": 23, "budget": 24, "mood": 25, "notes": 26}


def canvas(color=CREAM):
    im = Image.new("RGB", (W, H), color)
    d = ImageDraw.Draw(im)
    return im, d


def place(im, page, height, xy, angle=0):
    p = page.copy()
    p = p.resize((int(p.width * height / p.height), height), Image.LANCZOS)
    if angle:
        p = p.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
    mask = p.split()[-1] if p.mode == "RGBA" else Image.new("L", p.size, 255)
    shadow = Image.new("RGBA", (p.width + 80, p.height + 80), (0, 0, 0, 0))
    sm = Image.new("L", shadow.size, 0)
    sm.paste(mask, (40, 40))
    sm = sm.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.35))
    im.paste((60, 70, 65), (xy[0] - 40 + 14, xy[1] - 40 + 22), sm)
    im.paste(p.convert("RGB"), xy, mask)
    return p.size


def pill(d, xy, text, fill=SAGE, color="white", size=58):
    f = font("Carlito-Bold", size)
    tw = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + tw + 80, y + size + 44], radius=(size + 44) // 2, fill=fill)
    d.text((x + 40, y + 18), text, font=f, fill=color)
    return tw + 80


def centered(d, y, text, f, fill=INK):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


# 1. Hero thumbnail
im, d = canvas()
d.ellipse([-300, 1300, 700, 2300], fill=PEACH_LT)
d.ellipse([2150, -250, 2950, 550], fill=SAGE_LT)
place(im, pg(IDX["daily"]), 1500, (1620, 330), angle=-4)
place(im, pg(IDX["cover"]), 1550, (1180, 300), angle=3)
d.text((140, 260), "2027", font=font("Caladea-Bold", 300), fill=INK)
d.text((150, 600), "ADHD Planner", font=font("Caladea-Bold", 150), fill=INK)
d.text((155, 790), "Printable for Adults", font=font("Caladea-Italic", 90), fill=MUTED)
y = 980
for t in ["26 pages", "Daily · Weekly · Monthly", "Habit + Mood Tracker", "Dopamine Menu"]:
    pill(d, (150, y), t, fill=SAGE if y % 2 == 0 else "#C98F6E")
    y += 150
d.text((155, 1640), "INSTANT DOWNLOAD  ·  US LETTER + A4", font=font("Carlito-Bold", 60), fill=INK)
im.save(OUT / "01-hero.jpg", quality=92)

# 2. What's inside grid
im, d = canvas()
centered(d, 70, "What's inside", font("Caladea-Bold", 130))
centered(d, 225, "26 calm, clutter-free pages designed for ADHD brains", font("Caladea-Italic", 64), MUTED)
keys = ["cover", "year", "jan", "goals", "brain", "daily", "weekly", "habit", "routine", "dopamine", "task", "mood"]
cols, ph = 6, 560
pw = int(ph * 8.5 / 11)
gap = (W - cols * pw) // (cols + 1)
for i, k in enumerate(keys):
    r, c = divmod(i, cols)
    place(im, pg(IDX[k]), ph, (gap + c * (pw + gap), 400 + r * (ph + 160)))
im.save(OUT / "02-whats-inside.jpg", quality=92)

# 3-6. Feature images
features = [
    ("03-daily.jpg", "daily", "Daily Plan", ["Pick just 3 priorities", "Hour-by-hour time blocks", "Water, mood & meds check", "Celebrate today's wins"]),
    ("04-habit-tracker.jpg", "habit", "Habit Tracker", ["Track up to 14 habits", "31-day grid, any month", "Reflect on what helped", "No-guilt design"]),
    ("05-dopamine-menu.jpg", "dopamine", "Dopamine Menu", ["Healthy quick boosts", "Pair fun with boring tasks", "Know your energy drains", "Fridge-friendly"]),
    ("06-task-breakdown.jpg", "task", "Task Breakdown", ["Beat task paralysis", "Tiny 5-15 min steps", "Built-in reward", "Body-double prompt"]),
]
for fn, key, title, bullets in features:
    im, d = canvas()
    d.ellipse([1500, 200, 2700, 1400], fill=SAGE_LT)
    place(im, pg(IDX[key]), 1740, (1300, 140))
    d.text((140, 300), title, font=font("Caladea-Bold", 150), fill=INK)
    d.rounded_rectangle([145, 500, 285, 518], radius=9, fill=SAGE)
    y = 640
    for b in bullets:
        d.ellipse([150, y + 22, 190, y + 62], fill=PEACH)
        d.text((230, y), b, font=font("Carlito-Regular", 80), fill=INK)
        y += 170
    d.text((145, 1700), "2027 ADHD Planner  ·  printable PDF", font=font("Caladea-Italic", 60), fill=MUTED)
    im.save(OUT / fn, quality=92)

# 7. Monthly calendars
im, d = canvas()
centered(d, 70, "12 dated 2027 monthly calendars", font("Caladea-Bold", 120))
centered(d, 215, "Monday start  ·  focus, dates & notes sidebar", font("Caladea-Italic", 64), MUTED)
for i in range(5):
    place(im, pg(IDX["jan"] + i * 2), 1400, (110 + i * 420, 420), angle=(i - 2) * 2)
im.save(OUT / "07-monthly.jpg", quality=92)

# 8. How it works / sizes
im, d = canvas()
centered(d, 100, "How it works", font("Caladea-Bold", 140))
steps = [("1", "Purchase", "Checkout securely on Etsy"), ("2", "Download", "Get your PDFs instantly"),
         ("3", "Print or go digital", "Home printer, print shop,\nGoodNotes or Notability")]
bw = 760
for i, (n, t, s) in enumerate(steps):
    x = 130 + i * (bw + 70)
    d.rounded_rectangle([x, 420, x + bw, 1250], radius=60, fill=SAGE_LT if i != 1 else PEACH_LT)
    d.ellipse([x + bw / 2 - 90, 500, x + bw / 2 + 90, 680], fill=SAGE)
    f = font("Caladea-Bold", 120)
    d.text((x + bw / 2 - d.textlength(n, font=f) / 2, 515), n, font=f, fill="white")
    f = font("Carlito-Bold", 78)
    d.text((x + bw / 2 - d.textlength(t, font=f) / 2, 760), t, font=f, fill=INK)
    f = font("Carlito-Regular", 56)
    for j, line in enumerate(s.split("\n")):
        d.text((x + bw / 2 - d.textlength(line, font=f) / 2, 900 + j * 75), line, font=f, fill=MUTED)
centered(d, 1420, "Includes US Letter (8.5x11\") + A4 (210x297mm)", font("Carlito-Bold", 80))
centered(d, 1560, "This is a digital file. No physical item will be shipped.", font("Caladea-Italic", 64), MUTED)
im.save(OUT / "08-how-it-works.jpg", quality=92)

# Pinterest pin (1000x1500)
pin = Image.new("RGB", (1000, 1500), CREAM)
pd = ImageDraw.Draw(pin)
pd.ellipse([550, -150, 1150, 450], fill=SAGE_LT)
place(pin, pg(IDX["daily"]), 760, (420, 520), angle=-4)
place(pin, pg(IDX["cover"]), 780, (90, 560), angle=3)
pd.text((70, 70), "2027 ADHD", font=font("Caladea-Bold", 120), fill=INK)
pd.text((70, 210), "Planner", font=font("Caladea-Bold", 120), fill=INK)
pd.text((75, 360), "that actually works for your brain", font=font("Caladea-Italic", 46), fill=MUTED)
pd.rounded_rectangle([70, 1370, 930, 1450], radius=40, fill=SAGE)
t = "26 printable pages · instant download"
f = font("Carlito-Bold", 40)
pd.text((500 - pd.textlength(t, font=f) / 2, 1388), t, font=f, fill="white")
pin.save(OUT / "pinterest-pin.jpg", quality=92)
print("done", sorted(p.name for p in OUT.iterdir()))
