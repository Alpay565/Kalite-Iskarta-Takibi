# Tur B — Project İçinde (Yönetişimli Üretim)

> **Amaç:** Rule + Skill + Context yüklü Project'te, **Project'e yüklü veri dosyasıyla**
> dashboard üretmek. Beklenen: çıktı **tekrar üretilebilir** (2 denemede de aynı standart),
> kurallar otomatik uygulanır.
>
> **DÜRÜSTLÜK NOTU:** Promptları gerçekten çalıştır; gerçek transcript + ekran görüntülerini
> yapıştır. Uydurma = −80.

## Ön Koşullar (docs/kurulum-kilavuzu.md'de adım adım)
- Project oluşturuldu; **talimatlar/kalici-talimat.md** içeriği Project talimatına yapıştırıldı.
- **talimatlar/uretim-standardi.md** Skill/Project bilgisi olarak yüklendi.
- **veri/veri.csv** Claude Project'e **dosya** olarak yüklendi (Connector kurumsal politika nedeniyle kullanılmadı). Aynı CSV ayrıca Google Sheet'e aktarıldı (sayfa adı `veri`) — dashboard bunu canlı okuyacak.

## Kullanılacak Prompt (aynen) — Üretim
```
Project'e yüklü veri.csv'yi kullan; üretilen kodda veriyi GÖMME — Apps Script ile bağlı
Google Sheet'ten çalışma anında oku. Yüklü Üretim
Standardı'ndaki tasarım sistemine ve Kalıcı Talimat'taki kurallara birebir uyarak, S2
Kalite & Iskarta panosunu Google Apps Script web app olarak üret. Dosyaları ayrı ver:
Kod.gs (doGet + veriGetir Sheet'ten canlı + logoGetir), index (HTML iskelet), stil
(<style>), script (<script>). 4 ekran olsun: Genel Bakış (KPI), Trend, Pareto, Kritik
Tablo. Para ₺ + tr-TR, etiketler Türkçe, boş/hata/yüklenme durumları dahil.
```

## Beklenen (kuralların uygulandığının kanıtı)
- ₺ + tr-TR binlik ayraç; tüm etiketler Türkçe.
- Veri Sheet'ten okunuyor (gömülü dizi yok).
- 4 ekran + her ekranda durum yönetimi.
- VALEO paleti + logo; satır içi stil/script yok.

---

## 1. Deneme — GERÇEK Transcript
> Claude'un yüklü `veri.csv`'yi kullandığı ve üretilen kodun Sheet'ten **canlı okuyacak** şekilde yazıldığı görünmeli.

```
[BURAYA 1. ÜRETİMİN GERÇEK TRANSCRIPT'İNİ YAPIŞTIR]
```
**Paylaşım linki:** _[...]_
**Ekran görüntüsü:** ekran-goruntuleri/turB-uretim1.png

---

## 2. Deneme (Kararlılık) — GERÇEK Transcript
> Aynı promptu tekrar çalıştır (veya "aynı isteği tekrar uygula" de). Amaç: çıktının
> aynı kaldığını göstermek.

Ek prompt:
```
Aynı isteği tekrar uygula. Önceki üretimle ekran sayısı, stil ve metrik tanımları
açısından aynı olduğunu doğrula; varsa farkları listele.
```

```
[BURAYA 2. ÜRETİMİN GERÇEK TRANSCRIPT'İNİ YAPIŞTIR]
```
**Paylaşım linki:** _[...]_
**Ekran görüntüsü:** ekran-goruntuleri/turB-uretim2.png

---

## Kısa Değerlendirme
> İki üretimin **aynı** çıktığını ve Tur A'dan **farkını** 1–2 cümleyle yaz.

```
[BURAYA GÖZLEMİNİ YAZ]
```
