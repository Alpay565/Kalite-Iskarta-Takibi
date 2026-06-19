# 🟢 BAŞLANGIÇ — Sıfırdan Adım Adım (hiç bilmeyenler için)

Bu dosya, **senin** ne yapman gerektiğini en basit haliyle anlatır. Kod hazır;
sen çoğunlukla **kopyala–yapıştır** ve birkaç tıklama yapacaksın.

> 💡 **GitHub'da bir dosyanın içeriğini kopyalama:** dosyayı aç → sağ üstteki
> **"Copy raw file"** (kopyala) ikonuna bas. İndirmek için yanındaki
> **"Download raw file"** ikonu.
>
> Bu repo: **https://github.com/Alpay565/Kalite-Iskarta-Takibi**

Süreç 7 bölüm: 1) Google Sheet → 2) Claude Project → 3) Veriyi Claude'a ekle → 4) İki tur →
5) Apps Script (dashboard) → 6) Doğrulama+Bonus → 7) Teslim.

> ℹ️ **Not:** İş Google Workspace'i kurumsal politika nedeniyle Claude'a **Connector** ile
> bağlanmıyor. Bu yüzden veriyi Claude'a **dosya** olarak veriyoruz. "Canlı veri" yine
> sağlanıyor: ürettiğimiz dashboard (Apps Script) Google Sheet'i çalışma anında okuyor
> (Bölüm 6, canlı veri testi). Veri **sentetik** olduğu için bu tamamen uygundur.
Her adımda **📸** gördüğün yerde ekran görüntüsü al (sonra rapora/teslime gerekli).

---

## BÖLÜM 1 — Google Sheet hazırla (veriyi koy)
1. Tarayıcıda **sheets.new** yaz → boş bir Google Sheet açılır.
2. GitHub'da `veri/veri.csv` dosyasını aç → **Download raw file** ile indir.
3. Sheet'te: **Dosya → İçe aktar → Yükle** → indirdiğin `veri.csv`'yi seç → **İçe aktar**.
4. Alttaki sayfa sekmesinin adına **çift tıkla**, adını **`veri`** yap.
   *(Bu isim önemli; kod tam olarak bu sayfayı okuyor.)*

## BÖLÜM 2 — Claude'da Proje kur (yönetişim)
5. **claude.ai** → sol menü **Projects → New project** → ad: `S2 Kalite`.
6. Projede **"Instructions / Talimatlar"** alanını aç.
   GitHub'da `talimatlar/kalici-talimat.md` içeriğini **kopyala → yapıştır → kaydet**. → 📸 (`project-rule.png`)
7. Projede **sağdaki "Files" (Dosyalar) kutusunun sağ üstündeki `+`** işaretine tıkla
   → bilgisayarına indirdiğin `talimatlar/uretim-standardi.md` dosyasını seç ve yükle.
   *(`.md` kabul etmezse `.txt` yap ya da içeriğini kopyalayıp o alana yapıştır.)* → 📸 (`project-skill.png`)
   > Not: Bazı arayüzlerde bu bölüm "Knowledge/Bilgi" adıyla geçer; işlev aynıdır.

## BÖLÜM 3 — Veriyi Claude'a ekle (dosya olarak)
8. GitHub'dan **`veri/veri.csv`**'yi indir (Download raw file). Sonra **`uretim-standardi.md`**'yi
   eklediğin gibi: sağdaki **"Files"** kutusunun **`+`**'sına tıkla → **`veri.csv`**'yi yükle.
   - Artık projedeki sohbetler hem üretim standardını hem örnek veriyi görür.
   - *(Connector kullanmıyoruz; canlı veri Bölüm 5'teki Apps Script panosu ile sağlanıyor.)*

## BÖLÜM 4 — İki tur (kanıt sohbetleri)
> Amaç: yönetişimin işe yaradığını göstermek. **Gerçek** sohbetler olmalı (uydurma yasak).

9. **Tur A (kontrol):** Projeye **GİRMEDEN** normal yeni bir sohbet aç.
   `transcripts/tur-A.md`'deki promptu yapıştır, gönder. Bir **boş sohbet** daha açıp tekrar yap.
   → 📸 (`turA-deneme1.png`, `turA-deneme2.png`). Sohbeti "Share" ile linkle.
10. **Tur B (yönetişimli):** Projenin **içinde** yeni sohbet aç.
    `transcripts/tur-B.md`'deki üretim promptunu yapıştır. Sonra "aynı isteği tekrar uygula" promptu.
    → 📸 (`turB-uretim1.png`, `turB-uretim2.png`)
11. Aldığın gerçek transcript metinlerini `transcripts/` dosyalarındaki boş alanlara yapıştır.

## BÖLÜM 5 — Dashboard'u çalıştır (Apps Script) — TARAYICIDA
12. Bölüm 1'deki Google Sheet'i aç → üst menü **Uzantılar → Apps Script**.
13. Açılan editörde 4 dosya oluştur (içerikleri GitHub `dashboard/apps-script/`'ten kopyala):
    - Soldaki **`Code.gs`** zaten var → içini sil, **`Kod.gs`** içeriğini yapıştır.
    - Sol üstte **+ → HTML** → ad **`index`** → `index.html` içeriği.
    - Aynı şekilde **`stil`** (← `stil.html`) ve **`script`** (← `script.html`).
    > ⚠️ **ÇOK ÖNEMLİ — dosya tipi:** `+`'ya basınca **"HTML"** seç (**"Script" DEĞİL**).
    > `index`, `stil`, `script` üçü de **HTML dosyası**; yalnız **`Kod`** Script (`.gs`).
    > Yanlışlıkla Script seçip HTML yapıştırırsan **`Syntax error: Unexpected token '<'`** alırsın
    > → o dosyayı **sil** (adın yanındaki **⋮ → Sil**), sonra **`+` → HTML** ile yeniden oluştur.
    > Adlar birebir `index`, `stil`, `script`, `Kod` olmalı (Apps Script HTML'lere `.html` ekler).
14. **Kaydet** (💾). Sağ üstte **Deploy → New deployment → Web app**:
    *Execute as: Me* · *Who has access: Anyone* → **Deploy**.
    *(Kurum hesabın "Anyone"a izin vermezse "Anyone within VALEO" veya "Only myself" seç.)*
15. **İzin iste** çıkar → onayla (Sheets + Drive + Mail).
16. Sana bir **Web app URL** verir → aç. **Dashboard çalışır!** → 📸 her sekmeyi
    (`dashboard-genel.png`, `dashboard-trend.png`, `dashboard-pareto.png`, `dashboard-tablo.png`).
    > Bu 4 görüntünün hazır örneklerini repodaki `ekran-goruntuleri/` klasöründe bulabilirsin.

## BÖLÜM 6 — Doğrulama + Bonus
17. **Canlı veri testi:** Sheet'te bir "Hata Adedi" hücresini değiştir → Web app URL'sini
    **yenile** → sayı güncellenir. → 📸 (`dogrulama-canli-once.png`, `dogrulama-canli-sonra.png`)
18. **(Bonus)** Apps Script'te fonksiyon listesinden **`tetikleyiciKur`** seç → **Run** → izin ver.
    Günlük e-posta tetikleyicisi kurulur. → 📸 (`tetikleyici-log.png`, `tetikleyici-eposta.png`)

## BÖLÜM 7 — Topla ve teslim et
19. Tüm ekran görüntülerini `ekran-goruntuleri/` klasörüne, `ekran-goruntuleri/OKUBENI.md`'deki
    **adlarla** koy. *(rapor.pdf'i yeniden üretirsen bu görüntüler otomatik gömülür.)*
20. `rapor.pdf`'i aç, kapaktaki **ad/departman** doğru mu bak.
21. Her şeyi ödev yönergesindeki hocanın reposuna
    (**github.com/kupakoray/Homework-Uploads**) `Alpay-Mutlu/` klasörü olarak yükle.

---

### Takıldığında
- Daha teknik/ayrıntılı anlatım: **`docs/kurulum-kilavuzu.md`**
- Dashboard klasörü ve dosyalar: **`dashboard/OKUBENI.md`**
- Hangi ekran görüntüsü hangi adla: **`ekran-goruntuleri/OKUBENI.md`**
- Tetikleyici (bonus) ayrıntısı: **`otomasyon/tetikleyici-kanit.md`**

> ⚠️ **Önemli:** Transcript ve ekran görüntüleri **gerçek** olmalı. Bu repo kodu,
> şablonları ve hazır dashboard görüntülerini sağlar; claude.ai oturum kanıtlarını
> sen kendi hesabından üretip eklersin.
