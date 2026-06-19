# Kurulum Kılavuzu (Uçtan Uca)

Bu kılavuz, repodaki dosyalarla ödevin **gerçek** kanıtlarını üretmen için adım adım
yol gösterir. Her şey **tarayıcı tabanlıdır** (iş bilgisayarına kurulum gerekmez).

İçindekiler: 0) Veri · 1) Project + Rule · 2) Skill · 3) Sheet + veri yükleme ·
4) Tur A · 5) Tur B · 6) Apps Script deploy · 7) Google Sites (ops.) ·
8) Doğrulama · 9) Bonus tetikleyici · 10) Rapor · 11) Teslim.

---

## 0) Veri Hazır
`veri/veri.csv` zaten üretildi (~250 satır). Yeniden üretmek istersen (opsiyonel, bilgisayarında Python varsa):
`python3 veri/uret_veri.py`. Aksi halde mevcut `veri/veri.csv`'yi kullan.

## 1) Claude Project + Kalıcı Talimat (Rule)
1. claude.ai → sol menü → **Projects** → **New project** → ad: `S2 Kalite & Iskarta`.
2. Project → **Instructions / Talimatlar** alanını aç.
3. `talimatlar/kalici-talimat.md` dosyasının **tamamını** kopyalayıp buraya yapıştır → kaydet.
4. 📸 **Ekran görüntüsü:** `ekran-goruntuleri/project-rule.png` (talimat alanında kuralların göründüğü hal).

## 2) Üretim Standardı (Skill / Project Bilgisi)
1. Project sayfasında sağdaki **"Files" (Dosyalar)** kutusunun sağ üstündeki **`+`** işaretine tıkla
   (veya kutunun ortasındaki "Add PDFs, documents, or other text…" alanına tıkla).
2. Bilgisayarına indirdiğin `talimatlar/uretim-standardi.md` dosyasını seç → yükle. Dosya listede görünür.
   - `.md` kabul edilmezse `.txt` olarak yeniden adlandır ya da içeriğini kopyalayıp yapıştır.
   - Not: Bazı arayüzlerde bu bölüm "Knowledge / Bilgi" adıyla geçebilir; işlev aynıdır (proje bilgisi).
3. 📸 `ekran-goruntuleri/project-skill.png`.

## 3) Google Sheet + Veriyi Claude'a yükle
> Not: İş Workspace'i kurumsal politika nedeniyle Claude'a **Connector** ile bağlanmıyor; veriyi
> Claude'a **dosya** olarak veriyoruz. Canlı veri ilkesi, dashboard'un (Apps Script) Sheet'i çalışma
> anında okumasıyla korunur (bkz. §6 ve Doğrulama #5). Veri sentetik olduğundan bu tamamen uygundur.
1. [sheets.new](https://sheets.new) → yeni Sheet → **Dosya > İçe aktar** → `veri/veri.csv` yükle.
   **Sayfa (sekme) adını `veri` yap.** Sheet'i adlandır (örn. `S2-Kalite-Veri`) ve kaydet.
   *(Bu Sheet, Apps Script panosunun canlı okuyacağı kaynaktır.)*
2. claude.ai → Project → sağdaki **"Files"** kutusunun **`+`**'sına tıkla → `veri/veri.csv`'yi yükle.
   (Claude bu örnek veriyle dashboard'u üretir; üretilen kod veriyi gömmez, Sheet'ten canlı okur.)

## 4) Tur A — Boş Sohbet (Kontrol)
1. **Project DIŞINDA** yeni boş sohbet aç.
2. `transcripts/tur-A.md` içindeki promptu çalıştır — **2 kez** (iki ayrı boş sohbet).
3. Gerçek transcript'leri `transcripts/tur-A.md`'ye yapıştır; 📸 `turA-deneme1.png`, `turA-deneme2.png`.

## 5) Tur B — Project İçinde (Yönetişimli)
1. **Project içinde** yeni sohbet aç (Rule + Skill + yüklü `veri.csv` aktif).
2. `transcripts/tur-B.md` üretim promptunu çalıştır; Claude'un yüklü veriden ürettiğini ve kodun
   Sheet'ten **canlı okuyacak** biçimde yazıldığını gör.
3. Kararlılık için aynı isteği **tekrar** çalıştır.
4. Üretilen kodları (`Kod.gs`, `index`, `stil`, `script`) bir sonraki adımda Apps Script'e koyacaksın.
   > Not: Claude'un ürettiği kod, repodaki `dashboard/apps-script/` ile **eşdeğer** olmalı
   > (yönetişim sayesinde). İstersen doğrudan repodaki dosyaları da kullanabilirsin.
5. Gerçek transcript'leri yapıştır; 📸 `turB-uretim1.png`, `turB-uretim2.png`.

## 6) Apps Script Web App (Dashboard'u Çalıştır) — TARAYICIDA
> Önerilen: script Sheet'e **bağlı (container-bound)** olsun; böylece veriyi otomatik okur.

1. **3. adımdaki Google Sheet'i aç** → menü: **Uzantılar > Apps Script**.
2. Açılan editörde şu dosyaları oluştur (içerikleri `dashboard/apps-script/`'ten kopyala):
   - `Kod.gs` (zaten `Code.gs` vardır → içeriğini değiştir)
   - **+ > HTML** → ad: `index` → içerik: `index.html`
   - **+ > HTML** → ad: `stil` → içerik: `stil.html`
   - **+ > HTML** → ad: `script` → içerik: `script.html`
   - (Manifesti görmek için) ⚙ **Project Settings > "Show appsscript.json"** işaretle → `appsscript.json` içeriğini yapıştır.
   > ⚠️ **Dosya tipi kritik:** `+` menüsünden **HTML** seç (Script DEĞİL). `index`, `stil`,
   > `script` → **HTML**; yalnız `Kod` → **Script (.gs)**. Yanlışlıkla Script seçersen
   > **`Syntax error: Unexpected token '<'`** alırsın → o dosyayı sil, `+ > HTML` ile yeniden yap.
   > Dosya adları **birebir** `index`, `stil`, `script`, `Kod` olmalı (include bunlara göre çalışır).
3. **Kaydet** (💾). **Dağıt (Deploy) > Yeni dağıtım > Tür: Web uygulaması.**
   - "Execute as": **Me** · "Who has access": **Anyone** (kurum hesabında engelliyse **Anyone within VALEO** veya **Only myself**).
4. **Yetkilendir** (Authorize) — istenen izinler: Sheets (mevcut), **Drive (logo için)**, **Mail (bonus)**.
5. Verilen **Web app URL**'sini aç → dashboard çalışır. 📸 `dashboard-genel.png`, `dashboard-pareto.png`, vb.

**Logo notu:** Logo, sunucudaki `logoGetir()` ile senin Drive'ından okunur (ID kod içinde).
Drive iznini onayladığında otomatik gelir; public paylaşım gerekmez. Gelmezse "VALEO"
yazı-markası görünür (hata değil, fallback).

**Deploy etmeden hızlı önizleme (opsiyonel):** repodaki `dashboard/yerel-onizleme.html`'i
bir yerel sunucu ile açabilirsin. Sana ayrıca **tek dosyalık statik önizleme** gönderildi;
onu çift tıklayıp tarayıcıda direkt görebilirsin.

## 7) Google Sites'a Gömme (Opsiyonel)
1. [sites.google.com](https://sites.google.com) → yeni site → **Insert > Embed > By URL** → Web app URL'sini yapıştır.
2. Yayınla; 📸 `sites-embed.png`. Linki README'ye ekle.

## 8) Doğrulama (6 senaryo)
`transcripts/dogrulama.md`'deki 6 senaryoyu çalıştır; özellikle:
- **Senaryo 5 (canlı veri):** Sheet'te bir hücreyi değiştir → **web app URL'sini yenile** → değer güncellenir. 📸 önce/sonra.
Ayrıca makine kanıtı (bilgisayarında Python varsa): `python3 otomasyon/kural-denetimi.py` → 8/8 PASS.

## 9) Bonus — Apps Script Tetikleyici
`otomasyon/tetikleyici-kanit.md`'yi izle: Apps Script editöründe `tetikleyiciKur` fonksiyonunu
bir kez çalıştır (veya **Tetikleyiciler** menüsünden zaman güdümlü ekle) → `gunlukKaliteOzeti`
her gün çalışır, PPM özet e-postası gönderir. 📸 execution log + gelen e-posta.

## 10) Rapor (rapor.pdf)
`rapor.pdf` repoda hazır (Bölüm 8 tüm başlıklar + mimari diyagram). İçeriği güncellemek
istersen `rapor/rapor.md`'yi okuyabilir, dilersen `rapor/rapor.html` benzeri bir kaynaktan
tarayıcıda "Yazdır → PDF kaydet" ile yeniden üretebilirsin. Adı/bilgileri kontrol et.

## 11) Teslim
README'deki **Kanıt Haritası**nı doldur (linkler + ekran görüntüleri yerleştir), commit'le,
sonra **instructor reposuna** (`github.com/kupakoray/Homework-Uploads`) `Alpay-Mutlu/`
klasörü olarak yükle (ödev yönergesine göre PR/branch).

---

### Ekran Görüntüsü Kontrol Listesi
`ekran-goruntuleri/OKUBENI.md`'deki adlarla kaydet: project-rule, project-skill,
turA-deneme1/2, turB-uretim1/2, dashboard-genel/pareto/tablo,
dogrulama-canli-once/sonra, dogrulama-bos-veri, tetikleyici-log, tetikleyici-eposta,
(ops.) sites-embed.
