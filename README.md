# S2 — Kalite & Iskarta Takibi · Yönetişimli Dashboard Üretim Hattı

AdAstra × VALEO Kurumsal YZ Programı — **Ödev #1**

> 🟢 **İlk kez mi başlıyorsun? → [BAŞLANGIÇ kılavuzu (`BASLANGIC.md`)](BASLANGIC.md)**
> Ne yapman gerektiğini sıfırdan, adım adım anlatır.

| | |
|---|---|
| **Ad Soyad** | Alpay Mutlu |
| **Departman** | Ar-Ge / Kalite |
| **Senaryo** | S2 — Kalite & Iskarta Takibi |
| **Persona** | Kalite Mühendisi |
| **Kullanılan Araç** | **Claude (Pro/Max)** — Project + Skill + Connector |
| **Çalışma Ortamı** | Google Apps Script web app (canlı Google Sheets) |

> **Bu ödevin özü dashboard çizmek değil**, aynı dashboard'u her seferinde **aynı
> standartta** üreten bir **yönetişim katmanı** (Kalıcı Talimat + Üretim Standardı +
> Bağlam yönetimi) kurmaktır.

## Panonun Yanıtladığı 3 Karar Sorusu
1. Hangi hata tipleri toplam hatanın çoğunu üretiyor? (**Pareto / 80-20**)
2. PPM ve ıskarta maliyeti dönemler arası nasıl değişiyor? (**Trend** — mevcut vs önceki)
3. En yüksek maliyetli/kritik kayıtlar hangileri, hangi tespit aşamasında? (**Kritik Tablo**)

## Repo Yapısı
```
talimatlar/      kalici-talimat.md (Rule) · uretim-standardi.md (Skill)
veri/            uret_veri.py · veri.csv · veri.json
dashboard/       apps-script/ (Kod.gs,index,stil,script,appsscript.json) ·
                 kaynak/ (CSS+JS tek kaynak) · yerel-onizleme.html · derle_appsscript.py · OKUBENI.md
transcripts/     tur-A.md · tur-B.md · dogrulama.md  (gerçek transcript için şablon)
rapor/           rapor_uret.py · rapor.md · mimari-diyagram.svg
rapor.pdf        Proje raporu (Bölüm 8 tüm başlıklar + diyagram)
docs/            kurulum-kilavuzu.md (uçtan uca, tarayıcı tabanlı)
otomasyon/       kural-denetimi.py · kanit-log.txt · tetikleyici-kanit.md
ekran-goruntuleri/ OKUBENI.md (hangi görüntü hangi adla)
```

## Nasıl Çalıştırılır (özet)
Tam adımlar: **`docs/kurulum-kilavuzu.md`**. Kısaca:
1. Project oluştur → `kalici-talimat.md`'yi talimata yapıştır, `uretim-standardi.md`'yi Skill/bilgi yükle.
2. `veri/veri.csv`'yi Google Sheet'e aktar (sayfa adı `veri`) → **Connector** ile bağla.
3. **Tur A** (boş sohbet) ve **Tur B** (Project + canlı Sheet) turlarını çalıştır.
4. Sheet → **Uzantılar > Apps Script** → `dashboard/apps-script/` dosyalarını koy → **Deploy > Web app**.
5. 6 doğrulama senaryosu + ekran görüntüleri + rapor.

### Yerel araçlar (opsiyonel, sadece bilgisayarında Python/Node varsa)
- Veri üret: `python3 veri/uret_veri.py`
- Apps Script parçalarını derle: `python3 dashboard/derle_appsscript.py`
- Yönetişim denetimi: `python3 otomasyon/kural-denetimi.py`
- Rapor üret: `python3 rapor/rapor_uret.py`

## Veri Sözlüğü
| Sütun | Tür | Açıklama |
|---|---|---|
| Tarih | tarih (ISO) | Üretim/kayıt günü; ekranda GG.AA.YYYY |
| Parça No | metin | Parça kodu (örn. VLO-1003) |
| Hat | metin | Üretim hattı (Hat-1..Hat-4) |
| Hata Tipi | metin | Hata kategorisi (Lehim Hatası, Boyut Sapması, …) |
| Hata Adedi | tam sayı | Hatalı adet (≤ Üretim Adedi) |
| Üretim Adedi | tam sayı | Üretilen toplam adet |
| Iskarta Maliyeti | tam sayı (₺) | Iskarta/yeniden işleme maliyeti |
| Tespit Aşaması | metin | Girdi Kontrol / Hat İçi / Final Kontrol / Müşteri Sahası |

**Metrikler:** PPM = (ΣHata ÷ ΣÜretim) × 1.000.000 · FPY % = (1 − ΣHata ÷ ΣÜretim) × 100 ·
Toplam Iskarta = Σ Iskarta Maliyeti.

## Kanıt Haritası (teslimden önce doldur)
| Rubrik kalemi | Kanıt |
|---|---|
| Bağlam + Rule | `talimatlar/kalici-talimat.md` · 📸 project-rule.png |
| Skill / Üretim standardı | `talimatlar/uretim-standardi.md` · 📸 project-skill.png |
| Canlı veri (Connector) | 📸 connector-bagli.png · Tur B transcript · Doğrulama #5 |
| Context yönetimi | rapor.pdf §3 |
| İki tur (A/B) | `transcripts/tur-A.md`, `tur-B.md` + 📸 |
| Dashboard | `dashboard/apps-script/` · Web app URL: _[buraya]_ · 📸 dashboard-*.png |
| Bonus otomasyon | `otomasyon/tetikleyici-kanit.md` + 📸 tetikleyici-log/eposta |
| Rapor | `rapor.pdf` |

## Linkler (doldur)
- **Web app URL:** _[Apps Script deploy linki]_
- **Google Sites (ops.):** _[link]_
- **Claude paylaşım linkleri:** Tur A _[..]_ · Tur B _[..]_

## Dürüstlük Notu
Transcript'ler ve ekran görüntüleri **gerçek** olmalıdır (uydurma/elle düzenlenmiş = −80).
Bu repo şablon + tam promptlar + çalışan kod sağlar; gerçek oturum kanıtlarını sen eklersin.
