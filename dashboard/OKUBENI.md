# Dashboard — Apps Script Web App

S2 Kalite & Iskarta panosu. Google Apps Script web app olarak çalışır; veriyi bağlı
Google Sheet'ten **canlı** okur. Grafikler elle SVG ile çizilir (dış CDN yok → Apps
Script sandbox'ta güvenli, çevrimdışı çalışır).

## Klasörler
```
apps-script/      >>> Apps Script editörüne kopyalanacak DOSYALAR (asıl çıktı)
  Kod.gs          doGet · include · veriGetir (Sheet'ten canlı) · logoGetir (Drive→base64) · (bonus) gunlukKaliteOzeti
  index.html      HTML iskelet — include('stil') + include('script'); satır içi stil/script YOK
  stil.html       <style> — TEK tasarım sistemi (üretilmiş)
  script.html     <script> — istemci mantığı (üretilmiş)
  appsscript.json manifest (zaman dilimi, web app, OAuth kapsamları)
kaynak/           TEK KAYNAK düz dosyalar (DRY) — apps-script/{stil,script}.html bunlardan üretilir
  tasarim-sistemi.css   VALEO paleti + tüm bileşen stilleri (tek stil kaynağı)
  veri-katmani.js       ortam algılar: google.script.run (Apps Script) | fetch veri.json (yerel)
  grafikler.js          SVG çizgi/sütun/Pareto grafikleri
  uygulama.js           4 ekran + yükleniyor/boş/hata durumları + sekme/filtre/logo
yerel-onizleme.html  tarayıcıda önizleme (kaynak/ + ../veri/veri.json)
derle_appsscript.py  kaynak/ -> apps-script/{stil,script}.html üretir
```

## Derleme (kaynak değişince)
```
python3 dashboard/derle_appsscript.py
```
`kaynak/tasarim-sistemi.css` ve `kaynak/*.js` dosyalarını okuyup `apps-script/stil.html`
ve `apps-script/script.html`'i yeniden üretir. **apps-script/{stil,script}.html'i elle
düzenleme**; kaynağı düzenle, betiği çalıştır.

## Deploy (özet — tam adım: docs/kurulum-kilavuzu.md §6)
1. Google Sheet (sayfa adı `veri`) → **Uzantılar > Apps Script**.
2. Editörde dosyaları oluştur: `Kod` (script) ve `index`, `stil`, `script` (HTML) — adlar **birebir**.
   > ⚠️ `index/stil/script` dosyalarını **+ → HTML** ile oluştur (Script değil); yoksa
   > `Unexpected token '<'` hatası alırsın. Yalnız `Kod` Script (`.gs`).
3. **Dağıt > Yeni dağıtım > Web uygulaması** → yetkilendir (Sheets + Drive + Mail) → Web app URL.

## Tasarım / Kurallar (özet)
- Para `₺` + `tr-TR` binlik; tarih `GG.AA.YYYY`; tüm etiketler Türkçe.
- Veri **koda gömülmez**; bağlı Sheet'ten okunur (`veriGetir`).
- Satır içi `style=`/`onclick` yok; stil tek dosyadan; olaylar JS'te delegasyonla.
- Her bölümde **yükleniyor / boş / hata** durumu.
- Renk tek başına anlam taşımaz: durum rozetleri **ikon + etiket** içerir; AA kontrast.
- VALEO paleti: parlak yeşil `#82E600` (vurgu/mevcut dönem), koyu yeşil `#4E8A00`, gri = referans.

## Önizleme
- **En kolay:** sana gönderilen tek dosyalık statik önizlemeyi tarayıcıda aç.
- **Yerel sunucu ile:** `dashboard/` içinde basit bir HTTP sunucu çalıştırıp
  `yerel-onizleme.html`'i aç (fetch için `file://` yerine `http://` gerekir).
- **Gerçek:** deploy edilmiş web app URL'si (canlı Sheet).

## Yönetişim denetimi
`python3 otomasyon/kural-denetimi.py` → satır içi stil/script, gömülü veri, tek tasarım
sistemi vb. otomatik kontrol (8/8 PASS, bkz. `otomasyon/kanit-log.txt`).
