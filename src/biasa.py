# Ambil foto produk sahaja daripada gambar N.jpg (reka letak masalah/penyelesaian)
# dan simpan sebagai biasa/N.jpg: foto produk atas latar putih, tanpa banner MASALAH.
import os, sys, glob
from PIL import Image

def potong(path):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    # Foto produk berada dalam jalur tengah (antara banner merah dan hijau), dalam kotak kelabu
    y0, y1 = int(h * 0.236), int(h * 0.775)
    band = im.crop((0, y0, w, y1))
    px = band.load(); bw, bh = band.size
    xs, ys = [], []
    for y in range(0, bh, 2):
        for x in range(0, bw, 2):
            r, g, b = px[x, y]
            if r < 245 or g < 245 or b < 245: xs.append(x); ys.append(y)
    if not xs: raise ValueError('tiada foto dijumpai')
    # Buang bingkai kelabu (8px) di sekeliling foto
    box = (min(xs) + 13, min(ys) + 13, max(xs) - 12, max(ys) - 12)
    foto = band.crop(box)
    s = max(foto.size) + 80
    out = Image.new('RGB', (s, s), 'white')
    out.paste(foto, ((s - foto.width) // 2, (s - foto.height) // 2))
    if s < 1080: out = out.resize((1080, 1080), Image.LANCZOS)
    return out

if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(os.path.join(root, 'biasa'), exist_ok=True)
    for f in sorted(glob.glob(os.path.join(root, '[0-9]*.jpg'))):
        n = os.path.basename(f)
        try: potong(f).save(os.path.join(root, 'biasa', n), quality=90); print('OK', n)
        except Exception as e: print('GAGAL', n, e)
