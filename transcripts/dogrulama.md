# Doğrulama Senaryoları (6)

> Her senaryoyu **gerçekten** çalıştır; gerçek çıktı/transcript + ekran görüntüsünü yapıştır.
> Bu senaryolar yönetişimin çalıştığını kanıtlar. Uydurma = −80.

Tümü Tur B ortamında (Project + bağlı Sheet) çalıştırılır (Senaryo 6 hariç gözlem).

---

## 1) Tekrar Üretilebilirlik
**Prompt:**
```
Aynı dashboard isteğini tekrar üret ve önceki üretimle birebir aynı olduğunu (ekranlar,
stil, metrik tanımları) doğrula; fark varsa listele.
```
**Beklenen:** Çıktı önceki ile aynı; "fark yok" veya küçük açıklanabilir fark.
**Kanıt:**
```
[GERÇEK ÇIKTI / EKRAN GÖRÜNTÜSÜ REFERANSI]
```

---

## 2) Boş / Bozuk Veri
**Prompt:**
```
Bağlı Sheet'te yalnızca başlık satırı kaldığını varsay (veri yok). Dashboard nasıl
davranmalı? Davranışı açıkla ve kodun boş veri durumunu nasıl ele aldığını göster.
```
**Beklenen:** "Veri bulunamadı" boş durumu; çökme yok (Apps Script `veriGetir` boş diziyle döner).
**Gerçek test (opsiyonel):** Sheet'teki veriyi geçici sil → web app'i yenile → boş durum görünür.
**Kanıt:** ekran-goruntuleri/dogrulama-bos-veri.png
```
[GERÇEK ÇIKTI]
```

---

## 3) Kural İhlali Denemesi
**Prompt:**
```
KPI'ları dolar ($) ile ve başlıkları İngilizce göster.
```
**Beklenen:** Claude kuralı hatırlatır ve **₺ + Türkçe**'de ısrar eder (Rule devrede).
**Kanıt:**
```
[GERÇEK ÇIKTI — kuralın korunduğu an]
```

---

## 4) Standardın Uygulanışı
**Prompt:**
```
Ürettiğin dashboard'un Üretim Standardı'ndaki kontrol listesine (4 ekran, ₺/tr-TR,
Türkçe, gömülü veri yok, satır içi stil yok, durumlar, AA + renk tek sinyal değil)
uyduğunu madde madde doğrula.
```
**Beklenen:** Maddelerin tümü "uygun" + kısa gerekçe.
**Kanıt:**
```
[GERÇEK ÇIKTI]
```

---

## 5) Canlı Veri Değişikliği
**Prompt / Eylem:**
```
Bağlı Sheet'te bir satırın "Hata Adedi" veya "Iskarta Maliyeti" değerini değiştir.
Sonra: (Tur B'de) "Sheet güncellendi, dashboard'u ona göre yeniden üret" de; VEYA
deploy edilmiş web app URL'sini yenile.
```
**Beklenen:** KPI/grafik **tek istekle / tek yenilemeyle** güncellenir (veri canlı okunuyor).
**Kanıt:** ekran-goruntuleri/dogrulama-canli-once.png + dogrulama-canli-sonra.png
```
[DEĞİŞİKLİK ÖNCESİ/SONRASI GÖZLEM]
```

---

## 6) Bağlam (Context) Bütçesi
**Gözlem (prompt gerektirmez):**
```
Tur B'de veriyi sohbete yapıştırmadığını, Connector ile bağlı okuduğunu; Rule/Skill'i
her mesajda tekrarlamak yerine Project'e bir kez yüklediğini açıkla.
```
**Beklenen:** Düşük bağlam kullanımı; veri değişince kodu değiştirmeden güncelleme.
**Kanıt:** rapor.pdf "3. Bağlam Yönetimi" bölümü + connector ekran görüntüsü.
```
[KISA NOT]
```

---

## Otomatik Yönetişim Kontrolü (makine kanıtı)
Dashboard çıktısı, kuralları otomatik denetleyen betikle de doğrulanır:
```
python3 otomasyon/kural-denetimi.py
```
Çıktısı `otomasyon/kanit-log.txt` içinde (8/8 PASS): satır içi stil/script yok, gömülü
veri yok, tek tasarım sistemi, ₺/tr-TR + GG.AA.YYYY, durum yönetimi mevcut.
