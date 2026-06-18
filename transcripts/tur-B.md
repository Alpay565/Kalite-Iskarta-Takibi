# Tur B — Project İçinde (Yönetişimli Üretim)

> **Amaç:** Rule + Skill + Context yüklü Project'te, **bağlı Sheet'ten canlı veriyle**
> dashboard üretmek. Beklenen: çıktı **tekrar üretilebilir** (2 denemede de aynı standart),
> kurallar otomatik uygulanır.
>
> **DÜRÜSTLÜK NOTU:** Promptları gerçekten çalıştır; gerçek transcript + ekran görüntülerini
> yapıştır. Uydurma = −80.

## Ön Koşullar (docs/kurulum-kilavuzu.md'de adım adım)
- Project oluşturuldu; **talimatlar/kalici-talimat.md** içeriği Project talimatına yapıştırıldı.
- **talimatlar/uretim-standardi.md** Skill/Project bilgisi olarak yüklendi.
- **veri/veri.csv** Google Sheet'e aktarıldı (sayfa adı: `veri`) ve **Connector** ile Project'e bağlandı.

## Kullanılacak Prompt (aynen) — Üretim
```
Bağlı Google Sheet'teki "veri" sayfasını CANLI oku; veriyi koda gömme. Yüklü Üretim
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
> Connector'ın **bağlı** olduğu ve Claude'un Sheet'i **canlı okuduğu** an ekran görüntüsünde görünmeli.

```
[BURAYA 1. ÜRETİMİN GERÇEK TRANSCRIPT'İNİ YAPIŞTIR]
```
**Paylaşım linki:** _[...]_
**Ekran görüntüleri:** ekran-goruntuleri/turB-uretim1.png · ekran-goruntuleri/connector-bagli.png

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
