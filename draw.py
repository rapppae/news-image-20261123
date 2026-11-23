#!/usr/bin/env python3
"""Poster berita dunia Senin 23 November 2026.

Renderer prosedural stdlib-only: menggambar koran satu halaman
1024x1024 dari bentuk geometris + font bitmap 5x7 buatan sendiri.
Tidak ada dependensi di luar standard library.
"""

import struct
import zlib

W = 1024
H = 1024

PAPER = (246, 242, 232)
INK = (22, 26, 34)
NAVY = (16, 36, 64)
NAVY_SOFT = (28, 56, 92)
RED = (176, 32, 32)
GOLD = (196, 132, 26)
SEA = (36, 82, 122)
SEA_DARK = (22, 58, 90)
SMOKE = (120, 122, 126)
FLAME = (232, 116, 24)
FLAME2 = (240, 178, 40)
PANEL = (255, 255, 255)
RULE = (150, 148, 138)
MUTED = (88, 88, 84)

GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
}


class Sheet:
    """Kanvas RGB sederhana dengan primitif gambar."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def dot(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = (y * self.w + x) * 3
            self.px[o] = col[0]
            self.px[o + 1] = col[1]
            self.px[o + 2] = col[2]

    def rect(self, x, y, w, h, col):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.dot(xx, yy, col)

    def frame(self, x, y, w, h, col, t=2):
        self.rect(x, y, w, t, col)
        self.rect(x, y + h - t, w, t, col)
        self.rect(x, y, t, h, col)
        self.rect(x + w - t, y, t, h, col)

    def disc(self, cx, cy, r, col):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.dot(xx, yy, col)

    def tri(self, ax, ay, bx, by, cx, cy, col):
        # isi segitiga lewat scanline
        ys = sorted([ay, by, cy])
        for y in range(ys[0], ys[2] + 1):
            xs = []
            for (x1, y1, x2, y2) in ((ax, ay, bx, by), (bx, by, cx, cy), (cx, cy, ax, ay)):
                if y1 == y2:
                    continue
                if min(y1, y2) <= y <= max(y1, y2):
                    t = (y - y1) / (y2 - y1)
                    xs.append(int(x1 + t * (x2 - x1)))
            if len(xs) >= 2:
                for x in range(min(xs), max(xs) + 1):
                    self.dot(x, y, col)

    def hline(self, x, y, w, col, t=1):
        self.rect(x, y, w, t, col)

    def glyph(self, x, y, ch, s, col):
        pat = GLYPHS.get(ch, GLYPHS[" "])
        for r in range(7):
            for c in range(5):
                if pat[r][c] == "1":
                    self.rect(x + c * s, y + r * s, s, s, col)

    def text(self, x, y, s, col, msg):
        cx = x
        for ch in msg.upper():
            self.glyph(cx, y, ch, s, col)
            cx += 6 * s
        return cx

    def text_w(self, msg, s):
        return len(msg) * 6 * s - s

    def center(self, y, s, col, msg):
        self.text((self.w - self.text_w(msg, s)) // 2, y, s, col, msg)

    def wrap(self, msg, max_chars):
        words = msg.split(" ")
        lines = []
        cur = ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, col, msg, max_chars, leading):
        yy = y
        for ln in self.wrap(msg, max_chars):
            self.text(x, yy, s, col, ln)
            yy += 7 * s + leading
        return yy


def tag(sheet, x, y, label, col):
    """Label kecil berlatar warna."""
    w = sheet.text_w(label, 2) + 16
    sheet.rect(x, y, w, 26, col)
    sheet.text(x + 8, y + 5, 2, (255, 255, 255), label)
    return w


def panel(sheet, x, y, w, h):
    sheet.rect(x, y, w, h, PANEL)
    sheet.frame(x, y, w, h, RULE, 2)


def ship_scene(sheet, x, y, w, h):
    """Kapal kargo di laut dengan asap dan api di geladak."""
    sheet.rect(x, y, w, h, SEA)
    sheet.rect(x, y + int(h * 0.62), w, h - int(h * 0.62), SEA_DARK)
    # ombak
    for i in range(6):
        wx = x + 12 + i * 52
        wy = y + int(h * 0.68) + (i % 2) * 14
        sheet.rect(wx, wy, 34, 4, (150, 190, 220))
    # lambung kapal
    hx, hy, hw, hh = x + 30, y + int(h * 0.42), w - 60, 44
    sheet.rect(hx, hy, hw, hh, (32, 34, 40))
    sheet.tri(hx + hw, hy, hx + hw, hy + hh, hx + hw - 34, hy + hh, (32, 34, 40))
    # kontainer
    cols = [(176, 32, 32), (196, 132, 26), (36, 82, 122), (90, 120, 60)]
    for i in range(5):
        cx = hx + 14 + i * 52
        sheet.rect(cx, hy - 30, 46, 28, cols[i % 4])
        sheet.frame(cx, hy - 30, 46, 28, (20, 20, 20), 1)
    # cerobong + asap
    sheet.rect(hx + hw - 70, hy - 62, 26, 34, (60, 60, 64))
    for (sx, sy, r) in ((hx + hw - 56, hy - 76, 16), (hx + hw - 44, hy - 96, 20),
                        (hx + hw - 26, hy - 112, 15), (hx + hw - 8, hy - 126, 11)):
        sheet.disc(sx, sy, r, SMOKE)
    # api di geladak
    sheet.tri(hx + 90, hy, hx + 108, hy - 44, hx + 126, hy, FLAME)
    sheet.tri(hx + 118, hy, hx + 132, hy - 30, hx + 148, hy, FLAME2)
    sheet.tri(hx + 150, hy, hx + 162, hy - 38, hx + 176, hy, FLAME)


def build():
    s = Sheet(W, H, PAPER)

    # ---- masthead ----
    s.rect(0, 0, W, 148, NAVY)
    s.rect(0, 148, W, 5, GOLD)
    s.center(18, 7, (255, 255, 255), "THE WORLD TODAY")
    s.center(84, 3, (214, 196, 140), "MONDAY, 23 NOVEMBER 2026")
    s.center(120, 2, (170, 190, 214), "ONE DAY  -  TEN STORIES  -  AROUND THE GLOBE")

    # ---- lead story ----
    panel(s, 24, 172, 976, 268)
    tag(s, 44, 188, "LEAD STORY", RED)
    ship_scene(s, 44, 224, 380, 196)
    s.text(452, 196, 2, RED, "BALTIC SEA  -  OFF FINLAND")
    y = s.para(452, 224, 3, INK,
               "RUSSIAN CARGO SHIP STILL BURNING AFTER DRONE STRIKE",
               26, 6)
    s.para(452, y + 10, 2, MUTED,
           "The vessel kept burning into Monday after the attack in the "
           "Baltic Sea, as fire crews worked through the night to "
           "contain the blaze and keep it from spreading.",
           40, 4)

    # ---- row 2: Kyiv + Indonesia ----
    panel(s, 24, 460, 478, 168)
    tag(s, 44, 476, "UKRAINE", NAVY_SOFT)
    s.para(44, 512, 3, INK, "14 MISSING AFTER RUSSIAN DRONE HITS KYIV BUILDING", 22, 5)
    s.para(44, 588, 2, MUTED, "Zelenskiy says rescuers are searching the rubble.", 34, 3)

    panel(s, 522, 460, 478, 168)
    tag(s, 542, 476, "INDONESIA", RED)
    s.para(542, 512, 3, INK, "FACTORY FIRE KILLS SEVERAL, DOZENS MISSING", 22, 5)
    s.para(542, 588, 2, MUTED, "Firefighters battled the blaze as families waited for news.", 34, 3)

    # ---- row 3: three panels ----
    boxes = [
        (24, 648, 312, 158, "COP31", NAVY_SOFT,
         "CLIMATE DRAFT DROPS FOSSIL FUELS",
         "Turkiye's final draft omits fossil fuels."),
        (356, 648, 312, 158, "SOUTH KOREA", RED,
         "EDUCATION MINISTER QUITS OVER AI EXAM SCANDAL",
         "Choi Kyo-jin resigns after the cheating scandal."),
        (688, 648, 312, 158, "NEPAL - INDIA", NAVY_SOFT,
         "NEPAL PM IN INDIA FOR STATE VISIT",
         "Shah holds talks with PM Modi in India."),
    ]
    for (bx, by, bw, bh, tg, tc, head, deck) in boxes:
        panel(s, bx, by, bw, bh)
        tag(s, bx + 20, by + 16, tg, tc)
        s.para(bx + 20, by + 52, 2, INK, head, 24, 4)
        s.para(bx + 20, by + 116, 2, MUTED, deck, 26, 3)

    # ---- bottom strip: four quick stories ----
    strip = [
        ("CRICKET", "INDIA SMASH RECORD 720/9D IN WELLINGTON TEST VS NEW ZEALAND"),
        ("UNITED NATIONS", "STATES AGREE TO KEEP TALKING ON LETHAL AI WEAPONS"),
        ("SENEGAL", "MIGRANT BOAT CAPSIZES: AT LEAST 4 DEAD, DOZENS MISSING"),
        ("PORTUGAL", "THOUSANDS MARCH IN LISBON OVER COST OF LIVING"),
    ]
    sx = 24
    for (tg, head) in strip:
        panel(s, sx, 826, 238, 138)
        s.text(sx + 14, 842, 2, RED, tg)
        s.para(sx + 14, 872, 2, INK, head, 17, 4)
        sx += 246

    # ---- footer ----
    s.hline(24, 984, 976, RULE, 2)
    s.text(24, 996, 2, MUTED, "SOURCES: REUTERS, AP, BBC")
    s.text(1024 - 24 - s.text_w("MONDAY 23 NOVEMBER 2026", 2), 996, 2, MUTED,
           "MONDAY 23 NOVEMBER 2026")
    return s


def png_bytes(sheet):
    raw = bytearray()
    for y in range(sheet.h):
        raw.append(0)
        raw.extend(sheet.px[y * sheet.w * 3:(y + 1) * sheet.w * 3])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        c += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return c

    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", sheet.w, sheet.h, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", comp)
    out += chunk(b"IEND", b"")
    return out


if __name__ == "__main__":
    data = png_bytes(build())
    with open("entry.png", "wb") as f:
        f.write(data)
    print(len(data), "bytes")
