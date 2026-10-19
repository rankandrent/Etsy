"""Generate the 2027 ADHD Planner printable (US Letter + A4) as PDFs."""
import calendar
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

YEAR = 2027
FONT_DIR = "/usr/share/fonts/truetype/crosextra"
pdfmetrics.registerFont(TTFont("Head", f"{FONT_DIR}/Caladea-Bold.ttf"))
pdfmetrics.registerFont(TTFont("HeadIt", f"{FONT_DIR}/Caladea-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Body", f"{FONT_DIR}/Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", f"{FONT_DIR}/Carlito-Bold.ttf"))

INK = HexColor("#2F3A36")
SAGE = HexColor("#7C9A87")
SAGE_LT = HexColor("#E3ECE5")
CREAM = HexColor("#FBF8F2")
PEACH = HexColor("#F2C9B0")
PEACH_LT = HexColor("#FBEDE3")
LINE = HexColor("#C9D3CC")
MUTED = HexColor("#7A8580")

MONTHS = list(calendar.month_name)[1:]
DOW = ["M", "T", "W", "T", "F", "S", "S"]


class Planner:
    def __init__(self, path, size):
        self.W, self.H = size
        self.c = canvas.Canvas(str(path), pagesize=size)
        self.c.setTitle(f"{YEAR} ADHD Planner")
        self.c.setAuthor("Plumoss Paper")
        self.m = 36  # margin
        self.page_no = 0

    # ---------- primitives ----------
    def bg(self):
        c = self.c
        c.setFillColor(CREAM)
        c.rect(0, 0, self.W, self.H, stroke=0, fill=1)

    def header(self, title, subtitle=None):
        self.bg()
        c, m = self.c, self.m
        c.setFillColor(SAGE)
        c.roundRect(m, self.H - m - 6, 34, 6, 3, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Head", 26)
        c.drawString(m, self.H - m - 36, title)
        if subtitle:
            c.setFont("HeadIt", 12)
            c.setFillColor(MUTED)
            c.drawString(m, self.H - m - 54, subtitle)
        return self.H - m - (70 if subtitle else 54)

    def footer(self):
        c = self.c
        c.setFont("Body", 8)
        c.setFillColor(MUTED)
        c.drawCentredString(self.W / 2, 18, f"{YEAR} ADHD Planner  ·  Plumoss Paper  ·  personal use only")

    def end(self):
        self.footer()
        self.c.showPage()
        self.page_no += 1

    def box(self, x, y_top, w, h, label=None, fill=SAGE_LT, lines=0, label_color=INK):
        c = self.c
        c.setFillColor(fill)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.roundRect(x, y_top - h, w, h, 8, stroke=1, fill=1)
        inner_top = y_top
        if label:
            c.setFillColor(label_color)
            c.setFont("BodyB", 10.5)
            c.drawString(x + 10, y_top - 16, label.upper())
            inner_top = y_top - 24
        if lines:
            gap = (inner_top - (y_top - h) - 6) / lines
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            for i in range(1, lines + 1):
                ly = inner_top - i * gap + 2
                c.line(x + 10, ly, x + w - 10, ly)
        return y_top - h

    def checkbox(self, x, y, s=9):
        c = self.c
        c.setStrokeColor(SAGE)
        c.setLineWidth(1)
        c.setFillColor(HexColor("#FFFFFF"))
        c.roundRect(x, y, s, s, 2, stroke=1, fill=1)

    def check_lines(self, x, y_top, w, n, gap):
        c = self.c
        for i in range(n):
            y = y_top - (i + 1) * gap
            self.checkbox(x, y + 2)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            c.line(x + 16, y + 1, x + w, y + 1)

    def dot_grid(self, x, y_bot, w, h, step=14):
        c = self.c
        c.setFillColor(LINE)
        yy = y_bot + step / 2
        while yy < y_bot + h:
            xx = x + step / 2
            while xx < x + w:
                c.circle(xx, yy, 0.8, stroke=0, fill=1)
                xx += step
            yy += step

    def date_line(self, label="Date"):
        c = self.c
        c.setFont("Body", 10)
        c.setFillColor(MUTED)
        x = self.W - self.m - 170
        c.drawString(x, self.H - self.m - 34, f"{label}:")
        c.setStrokeColor(LINE)
        c.line(x + 34, self.H - self.m - 36, self.W - self.m, self.H - self.m - 36)

    # ---------- pages ----------
    def cover(self):
        c, W, H = self.c, self.W, self.H
        self.bg()
        c.setFillColor(SAGE_LT)
        c.circle(W * 0.85, H * 0.86, 150, stroke=0, fill=1)
        c.setFillColor(PEACH_LT)
        c.circle(W * 0.12, H * 0.12, 190, stroke=0, fill=1)
        c.setFillColor(PEACH)
        c.circle(W * 0.78, H * 0.22, 46, stroke=0, fill=1)
        c.setFillColor(INK)
        c.setFont("Head", 120)
        c.drawCentredString(W / 2, H * 0.55, str(YEAR))
        c.setFont("Head", 40)
        c.drawCentredString(W / 2, H * 0.55 - 58, "ADHD Planner")
        c.setFont("HeadIt", 16)
        c.setFillColor(MUTED)
        c.drawCentredString(W / 2, H * 0.55 - 90, "one small step at a time")
        c.setFillColor(SAGE)
        c.roundRect(W / 2 - 40, H * 0.55 - 112, 80, 4, 2, stroke=0, fill=1)
        c.setFont("Body", 11)
        c.setFillColor(INK)
        c.drawCentredString(W / 2, 70, "This planner belongs to  ______________________________")
        c.showPage()
        self.page_no += 1

    def how_to_use(self):
        y = self.header("How to use this planner", "There is no wrong way. Use what helps, skip what doesn't.")
        tips = [
            ("Start with a brain dump", "Empty every thought onto the Brain Dump page. Your brain is for having ideas, not holding them."),
            ("Pick only 3", "Each day choose just three priorities. Finishing 3 feels better than failing 15."),
            ("Break it down", "Stuck? Use the Task Breakdown page to turn one scary task into tiny 5-minute steps."),
            ("Use your Dopamine Menu", "Low energy? Pick an 'appetizer' from your menu instead of doom-scrolling."),
            ("Track gently", "Missed a day on the habit tracker? Leave it blank and keep going. No guilt, just data."),
            ("Print what you need", "Print extra daily or weekly pages any time. Works great in a binder or on a tablet."),
        ]
        c, m = self.c, self.m
        bw = self.W - 2 * m
        bh = (y - 60 - 5 * 12) / 6
        for i, (t, d) in enumerate(tips):
            top = y - i * (bh + 12)
            self.box(m, top, bw, bh, fill=SAGE_LT if i % 2 == 0 else PEACH_LT)
            c.setFillColor(SAGE)
            c.circle(m + 30, top - bh / 2, 15, stroke=0, fill=1)
            c.setFillColor(HexColor("#FFFFFF"))
            c.setFont("Head", 16)
            c.drawCentredString(m + 30, top - bh / 2 - 5, str(i + 1))
            c.setFillColor(INK)
            c.setFont("BodyB", 14)
            c.drawString(m + 58, top - bh / 2 + 6, t)
            c.setFont("Body", 10.5)
            c.setFillColor(MUTED)
            c.drawString(m + 58, top - bh / 2 - 10, d)
        self.end()

    def mini_month(self, x, y_top, w, month, h=None):
        c = self.c
        c.setFillColor(INK)
        c.setFont("BodyB", 10)
        c.drawString(x, y_top - 10, MONTHS[month - 1].upper())
        cw = w / 7
        c.setFont("BodyB", 7)
        c.setFillColor(SAGE)
        for i, d in enumerate(DOW):
            c.drawCentredString(x + cw * i + cw / 2, y_top - 24, d)
        c.setFont("Body", 7.5)
        c.setFillColor(INK)
        for r, week in enumerate(calendar.Calendar(0).monthdayscalendar(YEAR, month)):
            for i, d in enumerate(week):
                if d:
                    c.drawCentredString(x + cw * i + cw / 2, y_top - 36 - r * 11, str(d))

    def year_glance(self):
        y = self.header(f"{YEAR} at a glance")
        m = self.m
        cols, rows = 3, 4
        gw = (self.W - 2 * m - 2 * 24) / cols
        gh = (y - 40) / rows
        for i in range(12):
            r, col = divmod(i, cols)
            x = m + col * (gw + 24)
            top = y - r * gh
            self.box(x - 6, top + 4, gw + 12, gh - 10, fill=SAGE_LT if (r + col) % 2 == 0 else PEACH_LT)
            self.mini_month(x + 6, top - 4, gw - 12, i + 1)
        self.end()

    def month_page(self, month):
        y = self.header(f"{MONTHS[month - 1]} {YEAR}", "Monthly overview")
        c, m = self.c, self.m
        side = 150
        gw = self.W - 2 * m - side - 12
        weeks = calendar.Calendar(0).monthdayscalendar(YEAR, month)
        cw = gw / 7
        c.setFont("BodyB", 9)
        c.setFillColor(SAGE)
        for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
            c.drawCentredString(m + cw * i + cw / 2, y - 12, d)
        top = y - 20
        rh = (top - 44) / len(weeks)
        for r, week in enumerate(weeks):
            for i, d in enumerate(week):
                x = m + i * cw
                yt = top - r * rh
                c.setFillColor(HexColor("#FFFFFF") if d else SAGE_LT)
                c.setStrokeColor(LINE)
                c.setLineWidth(0.7)
                c.rect(x, yt - rh, cw, rh, stroke=1, fill=1)
                if d:
                    c.setFillColor(INK)
                    c.setFont("BodyB", 10)
                    c.drawString(x + 5, yt - 13, str(d))
        sx = m + gw + 12
        bh = (top - 44 - 24) / 3
        self.box(sx, top, side, bh, "Focus this month", lines=5)
        self.box(sx, top - bh - 12, side, bh, "Important dates", fill=PEACH_LT, lines=5)
        self.box(sx, top - 2 * (bh + 12), side, bh, "Notes", lines=5)
        self.end()

    def brain_dump(self):
        y = self.header("Brain dump", "Get it all out. Sort it later.")
        self.date_line()
        m = self.m
        w = (self.W - 2 * m - 12) / 2
        h = (y - 44 - 12) / 2
        self.box(m, y, w, h, "To do", lines=12)
        self.box(m + w + 12, y, w, h, "Worries", fill=PEACH_LT, lines=12)
        self.box(m, y - h - 12, w, h, "Ideas", fill=PEACH_LT, lines=12)
        self.box(m + w + 12, y - h - 12, w, h, "Remember", lines=12)
        self.end()

    def daily(self):
        y = self.header("Daily plan", "Pick 3. Do 1. Celebrate any of it.")
        self.date_line()
        c, m = self.c, self.m
        full = self.W - 2 * m
        left = full * 0.55
        right = full - left - 12
        # one thing
        self.box(m, y, full, 46, "If I only do one thing today...", fill=PEACH_LT)
        y -= 58
        col_top = y
        # top 3
        h3 = 104
        self.box(m, y, left, h3, "Top 3 priorities")
        self.check_lines(m + 12, y - 22, left - 24, 3, 25)
        y -= h3 + 12
        # time blocks
        hours = ["7", "8", "9", "10", "11", "12", "1", "2", "3", "4", "5", "6", "7", "8"]
        tb = y - 44
        self.box(m, y, left, tb, "Time blocks")
        gap = (tb - 30) / len(hours)
        for i, hr in enumerate(hours):
            ly = y - 26 - (i + 1) * gap
            c.setFont("BodyB", 8.5)
            c.setFillColor(SAGE)
            c.drawRightString(m + 28, ly + 4, hr)
            c.setStrokeColor(LINE)
            c.line(m + 34, ly + 2, m + left - 10, ly + 2)
        # right column
        rx = m + left + 12
        ry = col_top
        self.box(rx, ry, right, 150, "Other tasks", fill=SAGE_LT)
        self.check_lines(rx + 12, ry - 20, right - 24, 6, 20)
        ry -= 162
        # water + meds + mood
        self.box(rx, ry, right, 54, "Water", fill=PEACH_LT)
        for i in range(8):
            cx = rx + 18 + i * ((right - 30) / 8)
            c.setStrokeColor(SAGE)
            c.setFillColor(HexColor("#FFFFFF"))
            c.roundRect(cx, ry - 44, 14, 18, 3, stroke=1, fill=1)
        ry -= 66
        self.box(rx, ry, right, 54, "Energy  ·  Mood", fill=SAGE_LT)
        for i in range(5):
            cx = rx + 22 + i * ((right - 40) / 5)
            c.setStrokeColor(SAGE)
            c.setFillColor(HexColor("#FFFFFF"))
            c.circle(cx + 6, ry - 36, 8, stroke=1, fill=1)
            c.setFont("Body", 7.5)
            c.setFillColor(MUTED)
            c.drawCentredString(cx + 6, ry - 39, str(i + 1))
        ry -= 66
        self.box(rx, ry, right, 40, "Meds / vitamins taken", fill=PEACH_LT)
        self.checkbox(rx + right - 52, ry - 30); self.checkbox(rx + right - 30, ry - 30)
        c.setFont("Body", 7); c.setFillColor(MUTED)
        c.drawString(rx + right - 52, ry - 38, "AM"); c.drawString(rx + right - 30, ry - 38, "PM")
        ry -= 52
        self.box(rx, ry, right, ry - 44, "Today's wins (big or tiny)", fill=SAGE_LT, lines=6)
        self.end()

    def weekly(self):
        y = self.header("Weekly plan", "Week of ____________________")
        c, m = self.c, self.m
        full = self.W - 2 * m
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        w = (full - 12) / 2
        h = (y - 44 - 3 * 10) / 4
        for i, d in enumerate(days):
            r, col = divmod(i, 2)
            x = m + col * (w + 12)
            self.box(x, y - r * (h + 10), w, h, d, fill=SAGE_LT if i % 2 == 0 else PEACH_LT)
            self.check_lines(x + 12, y - r * (h + 10) - 20, w - 24, 4, (h - 30) / 4)
        x = m + w + 12
        self.box(x, y - 3 * (h + 10), w, h, "This week's focus", fill=HexColor("#FFFFFF"), lines=4)
        self.end()

    def habit_tracker(self):
        y = self.header("Habit tracker", "Month: ____________________     Tiny habits count.")
        c, m = self.c, self.m
        full = self.W - 2 * m
        name_w = 120
        cell = (full - name_w) / 31
        rows = 14
        rh = min(30, (y - 120) / rows)
        c.setFont("BodyB", 7)
        c.setFillColor(SAGE)
        for d in range(31):
            c.drawCentredString(m + name_w + d * cell + cell / 2, y - 10, str(d + 1))
        top = y - 16
        for r in range(rows):
            yt = top - r * rh
            c.setFillColor(SAGE_LT if r % 2 == 0 else HexColor("#FFFFFF"))
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            c.rect(m, yt - rh, name_w, rh, stroke=1, fill=1)
            for d in range(31):
                c.rect(m + name_w + d * cell, yt - rh, cell, rh, stroke=1, fill=1)
        by = top - rows * rh - 14
        w = (full - 12) / 2
        self.box(m, by, w, by - 44, "What helped this month", fill=PEACH_LT, lines=4)
        self.box(m + w + 12, by, w, by - 44, "What I'll try next month", lines=4)
        self.end()

    def routine(self):
        y = self.header("Daily routines", "Same steps, less thinking. Check them off.")
        c, m = self.c, self.m
        full = self.W - 2 * m
        w = (full - 12) / 2
        h = y - 44
        for i, (t, fill) in enumerate([("Morning routine", PEACH_LT), ("Evening routine", SAGE_LT)]):
            x = m + i * (w + 12)
            self.box(x, y, w, h, t, fill=fill)
            n = 12
            gap = (h - 40) / n
            for k in range(n):
                ly = y - 30 - (k + 1) * gap
                c.setFont("Body", 8)
                c.setFillColor(MUTED)
                c.drawString(x + 12, ly + 4, "time")
                c.setStrokeColor(LINE)
                c.line(x + 34, ly + 2, x + 64, ly + 2)
                c.line(x + 72, ly + 2, x + w - 30, ly + 2)
                self.checkbox(x + w - 24, ly + 2)
        self.end()

    def dopamine_menu(self):
        y = self.header("Dopamine menu", "Healthy options for when your brain wants a hit.")
        c, m = self.c, self.m
        full = self.W - 2 * m
        items = [
            ("Appetizers", "quick 1-5 min boosts", PEACH_LT),
            ("Mains", "longer, deeply satisfying", SAGE_LT),
            ("Sides", "pair with boring tasks", SAGE_LT),
            ("Desserts", "fun, use sparingly", PEACH_LT),
            ("Specials", "occasional big treats", PEACH_LT),
            ("Avoid list", "drains me, not helps me", SAGE_LT),
        ]
        w = (full - 12) / 2
        h = (y - 44 - 2 * 12) / 3
        for i, (t, sub, fill) in enumerate(items):
            r, col = divmod(i, 2)
            x = m + col * (w + 12)
            top = y - r * (h + 12)
            self.box(x, top, w, h, t, fill=fill, lines=6)
            c.setFont("HeadIt", 9)
            c.setFillColor(MUTED)
            c.drawRightString(x + w - 10, top - 16, sub)
        self.end()

    def task_breakdown(self):
        y = self.header("Task breakdown", "Too big? Make the next step stupidly small.")
        c, m = self.c, self.m
        full = self.W - 2 * m
        self.box(m, y, full, 50, "The big scary task", fill=PEACH_LT)
        y -= 62
        self.box(m, y, full, 40, "Why it matters to me")
        y -= 52
        h = y - 44 - 82
        self.box(m, y, full, h, "Tiny steps  (aim for 5-15 minutes each)", fill=HexColor("#FFFFFF"))
        n = 12
        gap = (h - 30) / n
        for k in range(n):
            ly = y - 26 - (k + 1) * gap
            c.setFillColor(SAGE)
            c.setFont("BodyB", 9)
            c.drawRightString(m + 26, ly + 4, f"{k + 1}.")
            c.setStrokeColor(LINE)
            c.line(m + 32, ly + 2, m + full - 120, ly + 2)
            c.setFont("Body", 7.5)
            c.setFillColor(MUTED)
            c.drawString(m + full - 110, ly + 4, "min")
            c.line(m + full - 94, ly + 2, m + full - 40, ly + 2)
            self.checkbox(m + full - 28, ly + 2)
        y -= h + 12
        w = (full - 12) / 2
        self.box(m, y, w, 70, "Reward when done", fill=PEACH_LT, lines=2)
        self.box(m + w + 12, y, w, 70, "Body double / accountability", lines=2)
        self.end()

    def budget(self):
        y = self.header("Monthly budget", "Month: ____________________   No shame, just numbers.")
        c, m = self.c, self.m
        full = self.W - 2 * m
        w = (full - 12) / 2
        self.box(m, y, w, 120, "Income", fill=SAGE_LT, lines=4)
        self.box(m + w + 12, y, w, 120, "Savings goal", fill=PEACH_LT, lines=4)
        y -= 132
        h = y - 44 - 82
        self.box(m, y, full, h, "Bills & expenses", fill=HexColor("#FFFFFF"))
        cols = [("Item", 0), ("Due", 0.45), ("Budget", 0.6), ("Actual", 0.75), ("Paid", 0.92)]
        c.setFont("BodyB", 9)
        c.setFillColor(SAGE)
        for t, fx in cols:
            c.drawString(m + 12 + fx * (full - 24), y - 34, t.upper())
        n = 16
        gap = (h - 46) / n
        for k in range(n):
            ly = y - 40 - (k + 1) * gap
            c.setStrokeColor(LINE)
            c.line(m + 12, ly + 2, m + full - 12, ly + 2)
            self.checkbox(m + 12 + 0.92 * (full - 24) + 6, ly + 4, 8)
        y -= h + 12
        third = (full - 24) / 3
        for i, t in enumerate(["Total income", "Total spent", "Left over"]):
            self.box(m + i * (third + 12), y, third, 70, t, fill=PEACH_LT if i == 1 else SAGE_LT)
        self.end()

    def mood_tracker(self):
        y = self.header("Mood & energy", "Month: ____________________")
        c, m = self.c, self.m
        full = self.W - 2 * m
        # key
        key = [("Great", HexColor("#9CC5A1")), ("Good", HexColor("#C9DFC4")), ("Okay", HexColor("#F3E3B5")),
               ("Low", PEACH), ("Hard", HexColor("#E6A9A0"))]
        kx = m
        for t, col in key:
            c.setFillColor(col)
            c.roundRect(kx, y - 14, 14, 14, 3, stroke=0, fill=1)
            c.setFillColor(INK)
            c.setFont("Body", 9.5)
            c.drawString(kx + 18, y - 11, t)
            kx += 70
        y -= 30
        cols = 2
        w = (full - 12) / cols
        rh = (y - 44 - 140) / 16
        for d in range(31):
            col, r = divmod(d, 16)
            x = m + col * (w + 12)
            yt = y - r * rh
            c.setFont("BodyB", 9)
            c.setFillColor(SAGE)
            c.drawRightString(x + 18, yt - rh / 2 - 3, str(d + 1))
            for k, lab in enumerate(["mood", "energy"]):
                c.setStrokeColor(LINE)
                c.setFillColor(HexColor("#FFFFFF"))
                c.roundRect(x + 26 + k * 22, yt - rh + 3, 16, rh - 6, 3, stroke=1, fill=1)
            c.setStrokeColor(LINE)
            c.line(x + 74, yt - rh + 4, x + w - 6, yt - rh + 4)
        c.setFont("Body", 7)
        c.setFillColor(MUTED)
        c.drawString(m + 26, y + 3, "mood  energy   note")
        by = y - 16 * rh - 14
        self.box(m, by, full, by - 44, "Patterns I notice (sleep, food, meds, people, weather...)", fill=PEACH_LT, lines=4)
        self.end()

    def goals(self):
        y = self.header("Goals that feel good", "Big picture -> this quarter -> this month")
        c, m = self.c, self.m
        full = self.W - 2 * m
        self.box(m, y, full, 70, f"My word for {YEAR}", fill=PEACH_LT)
        y -= 82
        w = (full - 12) / 2
        h = (y - 44 - 12) / 2
        for i, q in enumerate(["Q1  Jan - Mar", "Q2  Apr - Jun", "Q3  Jul - Sep", "Q4  Oct - Dec"]):
            r, col = divmod(i, 2)
            x = m + col * (w + 12)
            top = y - r * (h + 12)
            self.box(x, top, w, h, q, fill=SAGE_LT if (r + col) % 2 == 0 else HexColor("#FFFFFF"))
            self.check_lines(x + 12, top - 22, w - 24, 7, (h - 34) / 7)
        self.end()

    def notes(self):
        y = self.header("Notes")
        m = self.m
        w = self.W - 2 * m
        self.box(m, y, w, y - 44, fill=HexColor("#FFFFFF"))
        self.dot_grid(m + 4, 48, w - 8, y - 52)
        self.end()

    def build(self):
        self.cover()
        self.how_to_use()
        self.goals()
        self.year_glance()
        for mo in range(1, 13):
            self.month_page(mo)
        self.brain_dump()
        self.daily()
        self.weekly()
        self.habit_tracker()
        self.routine()
        self.dopamine_menu()
        self.task_breakdown()
        self.budget()
        self.mood_tracker()
        self.notes()
        self.c.save()
        return self.page_no


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "product/output")
    out.mkdir(parents=True, exist_ok=True)
    for name, size in [("US-Letter", LETTER), ("A4", A4)]:
        n = Planner(out / f"{YEAR}-ADHD-Planner-{name}.pdf", size).build()
        print(f"{name}: {n} pages")
