# Gabung foto produk sebenar (Shopee) dengan reka letak masalah -> penyelesaian.
import os, sys, io, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps
from data import D
H = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(H, 'fonts', 'DejaVuSans-Bold.ttf'); R = os.path.join(H, 'fonts', 'DejaVuSans.ttf')
F = lambda p, s: ImageFont.truetype(p, s)
W = 1080
def wrap(d, t, f, mw):
    out, cur = [], ''
    for w in t.split():
        n = (cur + ' ' + w).strip()
        if d.textlength(n, font=f) <= mw: cur = n
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out
def load(src):
    if src.startswith('http'):
        req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
        return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert('RGB')
    return Image.open(src).convert('RGB')
def make(no, photo, out):
    ttl, m1, m2, pn, s1 = D[no]
    im = Image.new('RGB', (W, W), '#ffffff'); d = ImageDraw.Draw(im)
    # Atas: masalah (merah)
    d.rectangle((0, 0, W, 250), fill='#b91c1c')
    d.rounded_rectangle((40, 28, 250, 76), 24, fill='#ffffff')
    d.text((62, 33), 'MASALAH', font=F(B, 32), fill='#b91c1c')
    tf = F(B, 54); ls = wrap(d, ttl, tf, 1000)
    if len(ls) > 1: tf = F(B, 44); ls = wrap(d, ttl, tf, 1000)
    y = 92
    for l in ls[:2]: d.text((40, y), l, font=tf, fill='#ffffff'); y += tf.size + 10
    d.text((40, y + 4), '✗ ' + m1 + '   ✗ ' + m2, font=F(R, 30), fill='#fecaca')
    # Tengah: foto produk sebenar
    p = ImageOps.contain(photo, (640, 560))
    px, py = (W - p.width) // 2, 255 + (575 - p.height) // 2
    d.rounded_rectangle((px - 8, py - 8, px + p.width + 8, py + p.height + 8), 24, fill='#e5e7eb')
    im.paste(p, (px, py))
    # Bawah: penyelesaian (hijau)
    d.rectangle((0, 840, W, W), fill='#15803d')
    d.rounded_rectangle((40, 858, 340, 906), 24, fill='#ffffff')
    d.text((60, 863), 'PENYELESAIAN', font=F(B, 30), fill='#15803d')
    nf = F(B, 44); nl = wrap(d, pn, nf, 1000)
    if len(nl) > 1: nf = F(B, 36)
    d.text((40, 922), pn, font=nf, fill='#ffffff')
    d.text((40, 990), '✓ ' + s1 + '  •  link dalam komen', font=F(R, 32), fill='#dcfce7')
    im.save(out, quality=90)
if __name__ == '__main__':
    outdir = sys.argv[1] if len(sys.argv) > 1 else '.'
    urls = dict(l.strip().split('|', 1) for l in open(os.path.join(H, 'urls.txt')) if '|' in l)
    for n, u in urls.items():
        try: make(int(n), load(u), os.path.join(outdir, f'{n}.jpg')); print('OK', n)
        except Exception as e: print('GAGAL', n, e)
