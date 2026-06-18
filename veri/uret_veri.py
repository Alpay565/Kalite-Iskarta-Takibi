#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 — Kalite & Iskarta Takibi: sentetik veri ureticisi.

Determinis­tiktir (sabit seed) — her calistirmada AYNI veriyi uretir; boylece
dashboard tekrar uretilebilir ve transcript'ler dogrulanabilir kalir.

Cikti:
  veri/veri.csv   (Google Sheet'e aktarilacak; sayfa adi: "veri")
  veri/veri.json  (yerel onizleme veri katmani icin)

Sutunlar (tumu Turkce, dashboard'da bu adlarla gosterilir):
  Tarih, Parca No, Hat, Hata Tipi, Hata Adedi, Uretim Adedi, Iskarta Maliyeti, Tespit Asamasi

Not: Veri ASLA dashboard koduna gomulmez. Bu dosya yalnizca ornek/figuran veri
uretir; canli dashboard veriyi bagli Google Sheet'ten (Apps Script) okur.
"""

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
SATIR_SAYISI = 250
BASLANGIC = date(2026, 1, 1)
BITIS = date(2026, 6, 15)  # mevcut vs onceki donem karsilastirmasi icin ~5.5 ay

# Sutun basliklari (tek kaynak) — tam Turkce.
SUTUNLAR = [
    "Tarih", "Parça No", "Hat", "Hata Tipi", "Hata Adedi",
    "Üretim Adedi", "Iskarta Maliyeti", "Tespit Aşaması",
]

HATLAR = ["Hat-1", "Hat-2", "Hat-3", "Hat-4"]

# Otomotiv komponenti hata tipleri — Pareto agirliklariyla (birkaci baskindir).
HATA_TIPLERI = [
    ("Lehim Hatası",      0.30),
    ("Boyut Sapması",     0.22),
    ("Montaj Hatası",     0.16),
    ("Yüzey Çiziği",      0.12),
    ("Conta Sızdırması",  0.09),
    ("Renk Tonu Farkı",   0.07),
    ("Elektriksel Arıza", 0.04),
]

# Hata tipi basina yaklasik birim iskarta maliyeti (TL/adet).
BIRIM_MALIYET = {
    "Lehim Hatası":      85,
    "Boyut Sapması":     60,
    "Montaj Hatası":     120,
    "Yüzey Çiziği":      25,
    "Conta Sızdırması":  95,
    "Renk Tonu Farkı":   30,
    "Elektriksel Arıza": 220,
}

# Tespit asamasi: ne kadar gec tespit, o kadar pahali (kalitesizlik maliyeti).
TESPIT_ASAMALARI = [
    ("Girdi Kontrol",   0.20, 1.0),
    ("Hat İçi",         0.42, 1.6),
    ("Final Kontrol",   0.28, 2.6),
    ("Müşteri Sahası",  0.10, 6.0),
]

# Parca numaralari (VLO = Valeo on eki, ornek).
PARCALAR = [f"VLO-{1000 + i}" for i in range(12)]


def agirlikli_sec(rng, secenekler, agirliklar):
    return rng.choices(secenekler, weights=agirliklar, k=1)[0]


def uret():
    rng = random.Random(SEED)
    gun_araligi = (BITIS - BASLANGIC).days

    hata_adlari = [h[0] for h in HATA_TIPLERI]
    hata_agirlik = [h[1] for h in HATA_TIPLERI]
    asama_adlari = [a[0] for a in TESPIT_ASAMALARI]
    asama_agirlik = [a[1] for a in TESPIT_ASAMALARI]
    asama_carpan = {a[0]: a[2] for a in TESPIT_ASAMALARI}

    satirlar = []
    for _ in range(SATIR_SAYISI):
        gun = BASLANGIC + timedelta(days=rng.randint(0, gun_araligi))
        hat = rng.choice(HATLAR)
        parca = rng.choice(PARCALAR)
        hata_tipi = agirlikli_sec(rng, hata_adlari, hata_agirlik)
        asama = agirlikli_sec(rng, asama_adlari, asama_agirlik)

        uretim = rng.randint(250, 2000)
        # Hata orani %0.2 - %4.5 arasi; Hata Adedi <= Uretim Adedi garanti.
        oran = rng.uniform(0.002, 0.045)
        hata = max(1, min(uretim, round(uretim * oran)))

        # Maliyet = hata x birim maliyet x asama carpani x (+-%15 gurultu)
        gurultu = rng.uniform(0.85, 1.15)
        maliyet = round(hata * BIRIM_MALIYET[hata_tipi] * asama_carpan[asama] * gurultu)

        satirlar.append({
            "Tarih": gun.isoformat(),
            "Parça No": parca,
            "Hat": hat,
            "Hata Tipi": hata_tipi,
            "Hata Adedi": hata,
            "Üretim Adedi": uretim,
            "Iskarta Maliyeti": maliyet,
            "Tespit Aşaması": asama,
        })

    # Tarihe gore sirala (okunabilir, deterministik cikti).
    satirlar.sort(key=lambda r: (r["Tarih"], r["Hat"], r["Parça No"]))
    return satirlar


def yaz(satirlar):
    kok = Path(__file__).resolve().parent

    csv_yol = kok / "veri.csv"
    with csv_yol.open("w", newline="", encoding="utf-8") as f:
        yazici = csv.DictWriter(f, fieldnames=SUTUNLAR)
        yazici.writeheader()
        yazici.writerows(satirlar)

    json_yol = kok / "veri.json"
    with json_yol.open("w", encoding="utf-8") as f:
        json.dump(satirlar, f, ensure_ascii=False, indent=2)

    return csv_yol, json_yol


def ozet(satirlar):
    toplam_uretim = sum(r["Üretim Adedi"] for r in satirlar)
    toplam_hata = sum(r["Hata Adedi"] for r in satirlar)
    toplam_maliyet = sum(r["Iskarta Maliyeti"] for r in satirlar)
    ppm = round(toplam_hata / toplam_uretim * 1_000_000) if toplam_uretim else 0
    fpy = round((1 - toplam_hata / toplam_uretim) * 100, 2) if toplam_uretim else 0

    pareto = {}
    for r in satirlar:
        pareto[r["Hata Tipi"]] = pareto.get(r["Hata Tipi"], 0) + r["Hata Adedi"]
    pareto_sirali = sorted(pareto.items(), key=lambda x: x[1], reverse=True)

    def tr(n):
        return f"{n:,}".replace(",", ".")

    print(f"Satir sayisi      : {len(satirlar)}")
    print(f"Toplam Uretim     : {tr(toplam_uretim)}")
    print(f"Toplam Hata       : {tr(toplam_hata)}")
    print(f"PPM               : {tr(ppm)}")
    print(f"FPY %             : {fpy}")
    print(f"Toplam Iskarta    : {tr(toplam_maliyet)} TL")
    print("Hata Pareto (adet, kumulatif %):")
    kumulatif = 0
    for ad, adet in pareto_sirali:
        kumulatif += adet
        yuzde = round(kumulatif / toplam_hata * 100, 1)
        print(f"  - {ad:<20} {adet:>5}   ({yuzde}%)")


if __name__ == "__main__":
    satirlar = uret()
    csv_yol, json_yol = yaz(satirlar)
    ozet(satirlar)
    print(f"\nYazildi: {csv_yol}")
    print(f"Yazildi: {json_yol}")
