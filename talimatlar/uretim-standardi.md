# Üretim Standardı (Skill) — Kalite & Iskarta Dashboard

> **Nereye konur:** Bu dosya Claude'a **Skill** olarak (veya Project bilgi/knowledge
> dosyası olarak) yüklenir. `kalici-talimat.md` (Rule) *ne* yapılacağını ve sınırları;
> bu dosya *nasıl* yapılacağını — tasarım sistemi ve üretim reçetesi — tanımlar.
> İkisi birlikte, aynı dashboard'un her seferinde aynı kalitede üretilmesini sağlar.

---

## 1. Amaç
Kalite Mühendisi'nin günlük kararları için **tek bakışta okunan** bir kontrol paneli.
Tasarım kararları kişisel zevke değil bu standarda dayanır → çıktı **tekrar
üretilebilir** olur.

---

## 2. Tasarım Sistemi (Design Tokens)
Tüm değerler CSS değişkeni olarak tanımlanır; bileşenler sabit kod yerine bu
token'ları kullanır.

### Renk — VALEO paleti
| Token | Değer | Kullanım |
|---|---|---|
| `--valeo-yesil` | `#82E600` | Birincil vurgu, **mevcut dönem** serisi, KPI vurgusu |
| `--valeo-yesil-koyu` | `#4E8A00` | İkincil vurgu, hover, ikincil seri |
| `--valeo-derin` | `#1F3A0E` | Başlık şeridi zemini, koyu yüzey |
| `--murekkep` | `#16261C` | Gövde metni (AA) |
| `--gri-referans` | `#9AA3A0` | **Önceki/referans dönem** serisi, ızgara |
| `--gri-300` `--gri-200` `--gri-100` | `#C9D1CC` `#E4E9E5` `#F1F4F1` | Kenarlık, ayraç, yüzey |
| `--zemin` | `#F6F9F4` | Sayfa zemini (çok hafif yeşil tint) |
| `--kart` | `#FFFFFF` | Kart yüzeyi |
| `--basari` | `#2E7D32` | Hedef içi / iyi |
| `--uyari` | `#B26A00` | İzlenecek (amber, AA için koyu) |
| `--tehlike` | `#C62828` | Kritik / eşik aşımı |

**Kontrast kuralı:** Parlak yeşil (`#82E600`) metin için kullanılmaz (AA'yı geçmez);
yalnız dolgu/şerit/vurgu. Metin daima `--murekkep` veya daha koyu tondur. Koyu zemin
(başlık şeridi) üstünde metin beyazdır.

### Tipografi
- Yazı ailesi: sistem yığını (`-apple-system, Segoe UI, Roboto, Arial, sans-serif`).
- Ölçek (token): `--yazi-kpi: 30px` · `--yazi-baslik: 18px` · `--yazi-govde: 14px` ·
  `--yazi-kucuk: 12px`. Sayılar `font-variant-numeric: tabular-nums`.

### Boşluk ve biçim
- Boşluk skalası: `--bosluk-1:4px` `--bosluk-2:8px` `--bosluk-3:12px` `--bosluk-4:16px`
  `--bosluk-5:24px`.
- Köşe yarıçapı: `--kose:10px`. Kenarlık: `1px solid var(--gri-200)`.
- **Gölge/3B yok**; ayrım kenarlık ve boşlukla sağlanır. Gereksiz animasyon yok.

---

## 3. Ekran Anatomisi (her ekranda aynı iskelet)
```
┌──────────────────────────────────────────────────────────────┐
│  [VALEO logo]  Başlık            Son güncelleme: GG.AA.YYYY SS  │  ← üst şerit (koyu yeşil)
├──────────────────────────────────────────────────────────────┤
│  Sekmeler:  Genel Bakış | Trend | Pareto | Kritik Tablo        │
│  Filtre:   [Hat ▼]                                             │  ← filtre çubuğu
├──────────────────────────────────────────────────────────────┤
│  İÇERİK (KPI satırı / grafik gövdesi / tablo)                  │
│  · yükleniyor → iskelet · boş → "Veri bulunamadı" · hata → mesaj │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Ekranlar (4 sekme — sabit)
- **E1 · Genel Bakış:** 6 KPI kartı — Toplam Üretim, Toplam Hata, **PPM**, **FPY %**,
  **Toplam Iskarta (₺)**, En Sık Hata Tipi. Her kart: ad + büyük değer + küçük
  bağlam (örn. önceki döneme göre ok/işaret + etiket).
- **E2 · Trend:** Aylık **PPM** ve **Iskarta Maliyeti** çizgi grafiği; **mevcut dönem
  (yeşil)** vs **önceki dönem (gri)**. Renk + çizgi tipi/işaretle ayrılır (renk tek
  sinyal değil).
- **E3 · Pareto:** Hata Tipi **Pareto** (sütun = adet, azalan; çizgi = kümülatif %;
  **%80 eşik çizgisi**). Altında Hat bazında hata kırılımı (sütun).
- **E4 · Kritik Tablo:** En yüksek maliyetli/kritik kayıtlar tablosu — Tarih, Hat,
  Parça No, Hata Tipi, Hata Adedi, Iskarta Maliyeti (₺), Tespit Aşaması, **Durum**.
  Durum = renk + **etiket + ikon** (⚠ Kritik / ● İzle / ✓ Normal).

---

## 5. Grafik Seçim Rehberi
| Veri sorusu | Grafik | Neden |
|---|---|---|
| Zaman içinde değişim | **Çizgi** | Eğilimi gösterir; dönem kıyası net |
| Kategoriler arası kıyas | **Sütun** | Uzunluk kıyaslaması kolay |
| "Az sayıda hata çoğu maliyeti üretiyor mu?" | **Pareto** (sütun+kümülatif) | 80/20 odaklama |
| Tekil kritik kayıtlar | **Tablo** | Kesin değer + aksiyon |

Yasak: pasta grafik (çok kategoride okunmaz), 3B grafik, ikiz eksende yanıltıcı ölçek.
Tüm grafikler **SVG** ile elde çizilir (dış CDN bağımlılığı yok → Apps Script sandbox
güvenli, çevrimdışı çalışır).

---

## 6. Veri Katmanı (zorunlu ayrım)
- Tek giriş noktası: `veriYukle()`. Apps Script ortamında `google.script.run` ile
  sunucudaki `veriGetir()` çağrılır (Sheet'ten canlı). Yerel önizlemede `veri.json`
  fetch edilir. **Görünüm katmanı veriyi nasıl geldiğini bilmez; sadece tüketir.**
- Kodda sabit veri **yok**. Sütun adları tek bir `SUTUN` haritasında toplanır.

---

## 7. Metrik Tanımları (sabit)
- **PPM** = (Σ Hata Adedi ÷ Σ Üretim Adedi) × 1.000.000
- **FPY %** = (1 − Σ Hata Adedi ÷ Σ Üretim Adedi) × 100
- **Toplam Iskarta** = Σ Iskarta Maliyeti (₺)
- **Dönem ayrımı:** veri ortadaki tarihten ikiye bölünür → son yarı "mevcut", ilk
  yarı "önceki".

---

## 8. Çıktı Dosya Yapısı (Apps Script web app)
| Dosya | Tür | İçerik |
|---|---|---|
| `Kod.gs` | Script | `doGet`, `include`, `veriGetir` (Sheet'ten canlı), `logoGetir`, (bonus) `gunlukKaliteOzeti` |
| `index` | HTML | İskelet; `include('stil')` + `include('script')`; satır içi stil/mantık yok |
| `stil` | HTML | Tek `<style>` — tasarım sistemi |
| `script` | HTML | Tek `<script>` — veri katmanı + grafikler + ekran mantığı |
| `appsscript.json` | Manifest | Zaman dilimi, web app erişimi, OAuth kapsamları |

---

## 9. Tamamlandı Kontrol Listesi (Definition of Done)
- [ ] 4 ekran da render oluyor; gereksiz kaydırma yok.
- [ ] Tüm para `₺` + `tr-TR` binlik; tarih `GG.AA.YYYY`.
- [ ] Tüm etiketler Türkçe.
- [ ] Kodda gömülü veri yok; veri bağlı kaynaktan okunuyor.
- [ ] Satır içi `style=`/mantık yok; stil tek dosyadan.
- [ ] Yükleniyor / boş / hata durumları her bölümde çalışıyor.
- [ ] Renk tek başına anlam taşımıyor (etiket+ikon mevcut).
- [ ] VALEO paleti + logo uygulanmış; metin kontrastı AA.
