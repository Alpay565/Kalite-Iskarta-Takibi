# Bonus Otomasyon — Apps Script Zaman Tetikleyicisi

**Ne yapar:** `gunlukKaliteOzeti()` her gün bağlı Sheet'i okur, PPM / toplam hata /
üretim / ıskarta maliyetini hesaplar ve sana **özet e-postası** gönderir. PPM eşiği
(`PPM_ESIK`, varsayılan 25.000) aşılırsa konuya **⚠ uyarı** ekler. (Kod: `dashboard/apps-script/Kod.gs`.)

Bu, "tek otomasyon (+5 bonus)" gereğini Apps Script tetikleyicisiyle karşılar.

## Kurulum (tarayıcıda, ~1 dk)
1. Apps Script editöründe (Sheet > Uzantılar > Apps Script) `Kod.gs` yüklü olsun.
2. Fonksiyon seçiciden **`tetikleyiciKur`**'u seç → **Çalıştır (Run)**.
   - İlk çalıştırmada izin ister: **Mail gönderme** + **Sheets** izinlerini onayla.
   - Bu fonksiyon, her gün ~08:00'de çalışan zaman güdümlü bir tetikleyici oluşturur.
   - Alternatif: sol menü **Tetikleyiciler (Triggers) > Tetikleyici ekle** →
     fonksiyon `gunlukKaliteOzeti`, olay kaynağı **Zaman güdümlü**, **Gün zamanlayıcı**.
3. Hemen test için fonksiyon seçiciden **`gunlukKaliteOzeti`**'ni seçip **Çalıştır** → e-posta gelmeli.

## Kanıt (ekran görüntüleri)
- 📸 `ekran-goruntuleri/tetikleyici-log.png` — **Yürütmeler (Executions)** panelinde
  `gunlukKaliteOzeti` satırının "Tamamlandı" durumu.
- 📸 `ekran-goruntuleri/tetikleyici-eposta.png` — gelen e-posta:
  konu "Günlük Kalite Özeti — PPM …" ve gövdede PPM / hata / üretim / ıskarta ₺.
- (ops.) 📸 Tetikleyiciler panelinde kurulu zaman güdümlü tetikleyici.

## Notlar
- E-posta `Session.getActiveUser().getEmail()` adresine gider (script sahibinin hesabı).
- Eşiği değiştirmek için `Kod.gs` içindeki `PPM_ESIK` değerini güncelle.
- Tetikleyiciyi kaldırmak: Tetikleyiciler panelinde sil veya `tetikleyiciKur` yerine
  ScriptApp üzerinden temizle (fonksiyon zaten eskiyi silip yeniden kurar).
