# Jana video menegak 9:16 (Threads/Reels/TikTok) untuk satu produk: masalah -> produk -> penyelesaian.
# Guna: python src/video.py <no> [outdir]
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageOps
from data import D
from make import F, B, R, wrap, load, H

W, HT, FPS = 1080, 1920, 30
RED, GREEN, WHITE = (185, 28, 28), (21, 128, 61), (255, 255, 255)

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def photo_for(no):
    urls = dict(l.strip().split('|', 1) for l in open(os.path.join(H, 'urls.txt')) if '|' in l)
    try: return load(urls[str(no)])
    except Exception:
        # Ambil semula foto dari gambar N.jpg (kawasan tengah, buang bingkai kelabu)
        im = Image.open(os.path.join(H, '..', f'{no}.jpg')).convert('RGB')
        band = im.crop((0, 252, W, 838))
        bg = Image.new('RGB', band.size, WHITE)
        from PIL import ImageChops
        x0, y0, x1, y1 = ImageChops.difference(band, bg).convert('L').point(lambda v: 255 if v > 12 else 0).getbbox()
        return band.crop((x0 + 10, y0 + 10, x1 - 10, y1 - 10))

def centered(d, y, text, font, fill, mw=960):
    for l in wrap(d, text, font, mw):
        d.text(((W - d.textlength(l, font=font)) / 2, y), l, font=font, fill=fill); y += font.size + 14
    return y

def pill(d, cx, y, text, font, fg, bg):
    tw = d.textlength(text, font=font); pad = 34
    d.rounded_rectangle((cx - tw / 2 - pad, y, cx + tw / 2 + pad, y + font.size + 30), (font.size + 30) // 2, fill=bg)
    d.text((cx - tw / 2, y + 12), text, font=font, fill=fg)

def frames(no):
    ttl, m1, m2, pn, s1 = D[no]
    photo = photo_for(no)
    base = ImageOps.contain(photo, (900, 900))
    fT, fX, fP, fN, fS, fC = F(B, 92), F(R, 54), F(B, 44), F(B, 70), F(R, 52), F(B, 56)
    # Babak (saat): 0-4 masalah, 4-9 produk, 9-13 penyelesaian
    total = 13.0
    for i in range(int(total * FPS)):
        t = i / FPS
        if t < 4:  # MASALAH
            im = Image.new('RGB', (W, HT), RED); d = ImageDraw.Draw(im)
            pill(d, W / 2, 470, 'MASALAH', fP, RED, WHITE)
            # tajuk muncul dari bawah
            k = ease(t / 0.6); y0 = 620 + int((1 - k) * 120)
            lay = Image.new('RGBA', (W, HT)); ld = ImageDraw.Draw(lay)
            y = centered(ld, y0, ttl, fT, (255, 255, 255, int(255 * k)))
            im.paste(lay, (0, 0), lay); d = ImageDraw.Draw(im)
            y += 60
            for j, m in enumerate((m1, m2)):
                if t > 1.2 + j * 0.8:
                    a = ease((t - 1.2 - j * 0.8) / 0.4)
                    c = tuple(int(WHITE[q] * (1 - a) * 0 + (254, 202, 202)[q] * a + RED[q] * (1 - a)) for q in range(3))
                    y = centered(d, y, '✗ ' + m, fX, c) + 20
                else: y += fX.size + 34
        elif t < 9:  # PRODUK
            u = t - 4
            im = Image.new('RGB', (W, HT), (243, 244, 246)); d = ImageDraw.Draw(im)
            # sapuan putih dari atas pada permulaan
            pill(d, W / 2, 220, 'INI JAWAPANNYA', fP, WHITE, GREEN)
            s = 0.85 + 0.15 * ease(u / 0.8) + 0.04 * (u / 5)  # zoom perlahan
            p = base.resize((int(base.width * s), int(base.height * s)), Image.LANCZOS)
            px, py = (W - p.width) // 2, 400 + (1000 - p.height) // 2
            d.rounded_rectangle((px - 14, py - 14, px + p.width + 14, py + p.height + 14), 36, fill=WHITE)
            im.paste(p, (px, py)); d = ImageDraw.Draw(im)
            if u > 1.0:
                a = ease((u - 1.0) / 0.5)
                lay = Image.new('RGBA', (W, HT)); ld = ImageDraw.Draw(lay)
                centered(ld, 1470 + int((1 - a) * 60), pn, fN, (17, 24, 39, int(255 * a)))
                im.paste(lay, (0, 0), lay)
            if u < 0.35:  # peralihan dari merah
                cover = int(HT * (1 - ease(u / 0.35)))
                d.rectangle((0, HT - cover, W, HT), fill=RED)
        else:  # PENYELESAIAN
            u = t - 9
            im = Image.new('RGB', (W, HT), GREEN); d = ImageDraw.Draw(im)
            th = ImageOps.contain(photo, (560, 560))
            tx, ty = (W - th.width) // 2, 300
            d.rounded_rectangle((tx - 12, ty - 12, tx + th.width + 12, ty + th.height + 12), 30, fill=WHITE)
            im.paste(th, (tx, ty))
            pill(d, W / 2, 940, 'PENYELESAIAN', fP, GREEN, WHITE)
            y = centered(d, 1050, pn, fN, WHITE) + 20
            if u > 0.5:
                a = ease((u - 0.5) / 0.4)
                c = tuple(int((220, 252, 231)[q] * a + GREEN[q] * (1 - a)) for q in range(3))
                y = centered(d, y, '✓ ' + s1, fS, c) + 60
            else: y += fS.size + 74
            if u > 1.3:  # CTA berdenyut
                pulse = 1 + 0.05 * abs(((u - 1.3) * 2) % 2 - 1)
                fc = F(B, int(56 * pulse)); txt = 'LINK DALAM KOMEN ↓'
                tw = d.textlength(txt, font=fc); h = fc.size + 40
                d.rounded_rectangle((W / 2 - tw / 2 - 40, y, W / 2 + tw / 2 + 40, y + h), h // 2, fill=(250, 204, 21))
                d.text((W / 2 - tw / 2, y + 18), txt, font=fc, fill=(17, 24, 39))
            if u < 0.35:
                cover = int(HT * (1 - ease(u / 0.35)))
                d.rectangle((0, 0, W, cover), fill=(243, 244, 246))
        yield im

def render(no, out):
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{HT}', '-r', str(FPS), '-i', '-',
           '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', '-c:a', 'aac', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for im in frames(no): p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    if p.returncode: raise SystemExit('ffmpeg gagal')

if __name__ == '__main__':
    no = int(sys.argv[1]); outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(H, '..', 'video')
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f'{no}.mp4'); render(no, out); print('OK', out)
