#!/usr/bin/env python3
"""星空テーマの画像を作る(packs/starry/theme/ に 4 枚)。

    pip3 install pillow   # 依存は Pillow だけ
    python3 tools/make_images.py

乱数はシード固定なので、何度走らせても同じ画像になる(差分が出ない)。
どれも 1 枚 2 MiB・合計 16 MiB(docs/slots.md §2.10 / §2.12 の上限)よりずっと小さい。

- sky.png     1080x1920 夜空(紺 → 藍の縦グラデーション + 薄い天の川の帯 + 暗い星)。app / fow の背景(below)
- stars.png   256x256   透過の星の粒(白 / 淡い黄、濃さはまちまち)。端をまたぐ粒は反対側にも描くので repeat で継ぎ目が出ない。
                        postTile に above で重ねる
- button.png  96x96     透過の藍色の角丸のにじみ。actionButton の背景(fill)
- heart.png   128x128   透過の淡い黄色の星のアイコン。favorite_border(いいね)の差し替え
"""

from __future__ import annotations

import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "packs", "starry", "theme")
PALE_YELLOW = (255, 244, 200)
WHITE = (255, 255, 255)


def lerp(a: tuple[int, ...], b: tuple[int, ...], t: float) -> tuple[int, ...]:
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def sky(w: int = 1080, h: int = 1920) -> Image.Image:
    rnd = random.Random(1)
    # 縦グラデーション: 上 = 深い紺、下 = 藍。1 列だけ作って横に伸ばす。
    top, mid, bottom = (5, 8, 24), (14, 18, 52), (43, 30, 104)
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        col.putpixel((0, y), lerp(top, mid, t / 0.55) if t < 0.55 else lerp(mid, bottom, (t - 0.55) / 0.45))
    img = col.resize((w, h))

    # 天の川: 左下 → 右上の斜めの帯を、ぼかしたマスクで薄く明るくする。
    band = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(band)
    x0, y0, x1, y1 = -200, int(h * 0.78), w + 200, int(h * 0.18)
    nx, ny = y1 - y0, -(x1 - x0)
    n = math.hypot(nx, ny)
    for half, alpha in ((230, 40), (140, 70), (60, 95)):
        ox, oy = nx / n * half, ny / n * half
        d.polygon([(x0 + ox, y0 + oy), (x1 + ox, y1 + oy), (x1 - ox, y1 - oy), (x0 - ox, y0 - oy)], fill=alpha)
    band = band.filter(ImageFilter.GaussianBlur(90))
    glow = Image.new("RGB", (w, h), (150, 150, 210))
    img = Image.composite(glow, img, band.point(lambda v: v * 45 // 100))

    # 暗い星: 帯の中ほど多く。明るい粒は stars.png(上に重ねる)に任せる。
    d = ImageDraw.Draw(img)
    for _ in range(2600):
        x, y = rnd.randrange(w), rnd.randrange(h)
        density = band.getpixel((x, y)) / 95
        if rnd.random() > 0.25 + 0.75 * density:
            continue
        base = img.getpixel((x, y))
        k = rnd.uniform(0.15, 0.55)
        c = lerp(base, PALE_YELLOW if rnd.random() < 0.3 else WHITE, k)
        if rnd.random() < 0.12:
            d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=c)
        else:
            d.point((x, y), fill=c)
    return img


def stars(size: int = 256, count: int = 40) -> Image.Image:
    rnd = random.Random(2)
    s = 4  # 4 倍で描いて縮める(粒の縁をなめらかに)
    big = Image.new("RGBA", (size * s, size * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    for _ in range(count):
        x, y = rnd.uniform(0, size), rnd.uniform(0, size)
        r = rnd.choice((0.7, 0.9, 1.1, 1.4, 1.8, 2.3))
        a = rnd.randint(90, 255)
        c = (PALE_YELLOW if rnd.random() < 0.35 else WHITE) + (a,)
        # タイルの端をまたぐ粒は反対側にも描く(repeat で継ぎ目が出ない)。
        for dx in (-size, 0, size):
            for dy in (-size, 0, size):
                cx, cy = (x + dx) * s, (y + dy) * s
                d.ellipse((cx - r * s, cy - r * s, cx + r * s, cy + r * s), fill=c)
                if r >= 1.8:  # 大きめの粒には薄い十字の光
                    arm = r * 3 * s
                    d.line((cx - arm, cy, cx + arm, cy), fill=c[:3] + (a // 4,), width=s // 2)
                    d.line((cx, cy - arm, cx, cy + arm), fill=c[:3] + (a // 4,), width=s // 2)
    return big.resize((size, size), Image.LANCZOS)


def button(size: int = 96) -> Image.Image:
    img = Image.new("RGBA", (size, size), (80, 70, 200, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((14, 14, size - 15, size - 15), radius=20, fill=200)
    mask = mask.filter(ImageFilter.GaussianBlur(7))
    core = Image.new("L", (size, size), 0)
    ImageDraw.Draw(core).rounded_rectangle((24, 24, size - 25, size - 25), radius=14, fill=90)
    core = core.filter(ImageFilter.GaussianBlur(5))
    img.putalpha(mask)
    # 中心を少し明るく(藍 → 淡い藍)。
    light = Image.new("RGBA", (size, size), (150, 140, 255, 0))
    light.putalpha(core)
    return Image.alpha_composite(img, light)


def star_icon(size: int = 128) -> Image.Image:
    s = 4
    n = size * s
    c = n / 2
    outer, inner = n * 0.40, n * 0.40 * 0.45
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = outer if i % 2 == 0 else inner
        pts.append((c + r * math.cos(ang), c + 0.03 * n + r * math.sin(ang)))
    shape = Image.new("L", (n, n), 0)
    ImageDraw.Draw(shape).polygon(pts, fill=255)
    shape = shape.resize((size, size), Image.LANCZOS)
    # にじみ(外側の光)+ 本体。
    glow = shape.filter(ImageFilter.GaussianBlur(6)).point(lambda v: v * 55 // 100)
    img = Image.new("RGBA", (size, size), PALE_YELLOW + (0,))
    img.putalpha(glow)
    body = Image.new("RGBA", (size, size), PALE_YELLOW + (0,))
    body.putalpha(shape)
    return Image.alpha_composite(img, body)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for name, im in (("sky.png", sky()), ("stars.png", stars()), ("button.png", button()), ("heart.png", star_icon())):
        path = os.path.join(OUT, name)
        im.save(path, optimize=True)
        print(f"{os.path.relpath(path)}: {im.size[0]}x{im.size[1]} {im.mode} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
