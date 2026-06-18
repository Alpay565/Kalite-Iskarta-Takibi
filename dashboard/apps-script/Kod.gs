/**
 * S2 — Kalite & Iskarta Paneli · Apps Script sunucu tarafı
 * --------------------------------------------------------
 * Önerilen kurulum: bu script Google Sheet'ten açılır (Uzantılar > Apps Script),
 * yani "container-bound"tur. Böylece veriyi bağlı Sheet'ten CANLI okur ve
 * SHEET_ID gerekmez. Bağımsız (standalone) kullanacaksan SHEET_ID'yi doldur.
 *
 * Web app olarak yayınla: Dağıt (Deploy) > Yeni dağıtım > Web uygulaması.
 */

var SAYFA_ADI = 'veri';                                  // Sheet'teki sayfa adı
var SHEET_ID = '';                                        // boş = bağlı Sheet; doluysa o ID
var LOGO_DRIVE_ID = '19SWUei7Rio5AbOEFv682ObI4kJugYGMU';  // VALEO logosu (Drive)
var PPM_ESIK = 25000;                                     // (bonus) günlük uyarı eşiği

function doGet() {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setTitle('VALEO · Kalite & Iskarta Paneli')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/** HTML parçalarını (stil/script) index'e enjekte eder. */
function include(ad) {
  return HtmlService.createHtmlOutputFromFile(ad).getContent();
}

function _sayfa_() {
  var ss = SHEET_ID ? SpreadsheetApp.openById(SHEET_ID) : SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error('Spreadsheet bulunamadı. SHEET_ID girin veya script\'i Sheet\'ten açın.');
  var sh = ss.getSheetByName(SAYFA_ADI);
  if (!sh) throw new Error('Sayfa bulunamadı: "' + SAYFA_ADI + '". Sheet sekme adını kontrol edin.');
  return sh;
}

/** Bağlı Sheet'i CANLI okur; satırları nesne dizisi olarak döndürür. */
function veriGetir() {
  var sh = _sayfa_();
  var aralik = sh.getDataRange().getValues();
  if (aralik.length < 2) return [];                       // yalnız başlık / boş -> boş durum
  var basliklar = aralik.shift().map(function (b) { return String(b).trim(); });
  var tz = Session.getScriptTimeZone() || 'Europe/Istanbul';
  return aralik
    .filter(function (r) { return r.join('').trim() !== ''; })   // boş satırları at
    .map(function (r) {
      var o = {};
      basliklar.forEach(function (b, i) {
        var v = r[i];
        if (v instanceof Date) v = Utilities.formatDate(v, tz, 'yyyy-MM-dd'); // tarihi temiz string'e
        o[b] = v;
      });
      return o;
    });
}

/** VALEO logosunu Drive'dan okuyup base64 data-URI döndürür (public paylaşım/CSP derdi yok). */
function logoGetir() {
  try {
    var cache = CacheService.getScriptCache();
    var anahtar = 'valeo_logo_' + LOGO_DRIVE_ID;
    var onbellek = cache.get(anahtar);
    if (onbellek) return onbellek;
    var blob = DriveApp.getFileById(LOGO_DRIVE_ID).getBlob();
    var uri = 'data:' + blob.getContentType() + ';base64,' + Utilities.base64Encode(blob.getBytes());
    try { cache.put(anahtar, uri, 21600); } catch (e) { /* 100KB üstüyse önbelleğe alma */ }
    return uri;
  } catch (e) {
    return '';   // istemci "VALEO" yazı-marka fallback gösterir
  }
}

/* ---------------------------------------------------------------- yardımcı */
function _binlik_(n) {
  n = Math.round(Number(n) || 0);
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');   // tr-TR binlik (nokta)
}

/* ============================ (BONUS) OTOMASYON =========================== */
/**
 * Günlük Kalite Özeti — zaman güdümlü tetikleyiciyle çalışır.
 * PPM eşiği aşılırsa konuya uyarı ekler ve özet e-postası gönderir.
 */
function gunlukKaliteOzeti() {
  var veri = veriGetir();
  if (!veri.length) return;
  var tu = 0, th = 0, tm = 0;
  veri.forEach(function (r) {
    tu += Number(r['Üretim Adedi']) || 0;
    th += Number(r['Hata Adedi']) || 0;
    tm += Number(r['Iskarta Maliyeti']) || 0;
  });
  var ppm = tu ? Math.round(th / tu * 1e6) : 0;
  var uyari = ppm > PPM_ESIK;
  var konu = (uyari ? '⚠ ' : '') + 'Günlük Kalite Özeti — PPM ' + _binlik_(ppm);
  var govde =
    'VALEO Kalite & Iskarta — Günlük Özet\n\n' +
    'PPM: ' + _binlik_(ppm) + (uyari ? '  (EŞİK AŞILDI: ' + _binlik_(PPM_ESIK) + ')' : '') + '\n' +
    'Toplam Hata: ' + _binlik_(th) + '\n' +
    'Toplam Üretim: ' + _binlik_(tu) + '\n' +
    'Toplam Iskarta Maliyeti: ' + _binlik_(tm) + ' ₺\n';
  MailApp.sendEmail(Session.getActiveUser().getEmail(), konu, govde);
}

/** Tetikleyiciyi bir kez kurar (her gün ~08:00). Editörden bir kez çalıştırın. */
function tetikleyiciKur() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'gunlukKaliteOzeti') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('gunlukKaliteOzeti').timeBased().everyDays(1).atHour(8).create();
}
