#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KURAL DENETİMİ (yönetişim QA) — dashboard çıktısının kalıcı talimattaki
makine-denetlenebilir kurallara uyup uymadığını otomatik kontrol eder.

Calistir:  python3 otomasyon/kural-denetimi.py
Cikis kodu: tum kontroller PASS ise 0, aksi halde 1.
"""

import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
DASH = KOK / "dashboard"
KAYNAK = DASH / "kaynak"
APPS = DASH / "apps-script"

# Denetlenecek kaynak HTML'ler (Apps Script teslimi + yerel onizleme).
HTML_DOSYALAR = [APPS / "index.html", DASH / "yerel-onizleme.html"]
JS_DOSYALAR = list(KAYNAK.glob("*.js")) + [APPS / "script.html"]

VERI_SUTUNLARI = ["Üretim Adedi", "Hata Adedi", "Iskarta Maliyeti", "Tespit Aşaması"]

sonuc = []  # (ad, gecti, ayrinti)


def ekle(ad, gecti, ayrinti=""):
    sonuc.append((ad, gecti, ayrinti))


def oku(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


# C1 — Satır içi stil (style="...") yasak.
ihlal = []
for p in HTML_DOSYALAR:
    if re.search(r'style\s*=\s*"', oku(p)):
        ihlal.append(p.name)
ekle("C1 Satır içi stil (style=) yok", not ihlal, ", ".join(ihlal))

# C2 — Satır içi olay (onclick= vb.) yasak; olaylar JS'te delegasyonla bağlanır.
ihlal = []
for p in HTML_DOSYALAR:
    if re.search(r'\son[a-z]+\s*=\s*"', oku(p)):
        ihlal.append(p.name)
ekle("C2 Satır içi olay (on*=) yok", not ihlal, ", ".join(ihlal))

# C3 — Apps Script index.html'de gömülü <script> yok (mantık include ile gelir).
idx = oku(APPS / "index.html")
ekle("C3 index.html'de inline <script> yok", "<script" not in idx)

# C4 — Gömülü veri yok: hiçbir kaynakta "Sütun Adı": <sayı> kalıbı bulunmamalı.
desen = re.compile(r'["\'](' + "|".join(map(re.escape, VERI_SUTUNLARI)) + r')["\']\s*:\s*-?\d')
ihlal = []
for p in JS_DOSYALAR:
    if desen.search(oku(p)):
        ihlal.append(p.name)
ekle("C4 Kodda gömülü veri yok", not ihlal, ", ".join(ihlal))

# C5 — Veri bağlı kaynaktan okunuyor (fetch + google.script.run mevcut).
vk = oku(KAYNAK / "veri-katmani.js")
ekle("C5 Veri bağlı kaynaktan (fetch + google.script.run)",
     ("fetch(" in vk) and ("google.script.run" in vk))

# C6 — Tek stil kaynağı: kaynak/ içinde tam 1 CSS; kaynak HTML'de <style> yok.
css_sayisi = len(list(KAYNAK.glob("*.css")))
style_ihlal = [p.name for p in HTML_DOSYALAR if "<style" in oku(p)]
ekle("C6 Tek tasarım sistemi dosyası", css_sayisi == 1 and not style_ihlal,
     f"css={css_sayisi}" + (("; <style> in " + ", ".join(style_ihlal)) if style_ihlal else ""))

# C7 — Para/dil: para biçimi tr-TR + ₺; tarih GG.AA.YYYY dönüşümü mevcut.
ekle("C7 Para tr-TR + ₺ ve GG.AA.YYYY biçimi",
     ("Intl.NumberFormat('tr-TR')" in vk) and ("₺" in vk) and ("tarihBicim" in vk))

# C8 — Durum yönetimi: yükleniyor/boş/hata üçü de ele alınmış.
uy = oku(KAYNAK / "uygulama.js")
ekle("C8 Yükleniyor/boş/hata durumları",
     all(s in uy for s in ["yukleniyor", "'bos'", "'hata'"]))

# ----------------------------------------------------------------- raporla
print("=" * 64)
print("  KURAL DENETİMİ — dashboard yönetişim QA")
print("=" * 64)
hepsi_gecti = True
for ad, gecti, ayrinti in sonuc:
    isaret = "PASS" if gecti else "FAIL"
    satir = f"  [{isaret}] {ad}"
    if ayrinti and not gecti:
        satir += f"  -> {ayrinti}"
    print(satir)
    hepsi_gecti = hepsi_gecti and gecti
print("-" * 64)
print("  SONUÇ:", "TÜM KONTROLLER PASS ✓" if hepsi_gecti else "BAŞARISIZ ✗")
print("=" * 64)

sys.exit(0 if hepsi_gecti else 1)
