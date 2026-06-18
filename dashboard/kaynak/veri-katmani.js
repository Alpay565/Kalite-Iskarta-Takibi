'use strict';
/*
 * VERİ KATMANI — tek giriş noktası.
 * Görünüm katmanı veriyi NASIL geldiğini bilmez; yalnız tüketir.
 *  - Apps Script ortamı  : google.script.run -> sunucudaki veriGetir() (Sheet'ten canlı)
 *  - Yerel önizleme       : veri.json fetch
 * Kodda GÖMÜLÜ VERİ YOKTUR.
 */

/* Sütun adları tek kaynak (Sheet başlıklarıyla birebir aynı olmalı). */
var SUTUN = {
  tarih: 'Tarih',
  parca: 'Parça No',
  hat: 'Hat',
  hataTipi: 'Hata Tipi',
  hataAdedi: 'Hata Adedi',
  uretimAdedi: 'Üretim Adedi',
  maliyet: 'Iskarta Maliyeti',
  asama: 'Tespit Aşaması'
};

var AY_ADI = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz',
              'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];

/* ----------------------------------------------------------------- yükleme */
function veriYukle() {
  if (typeof google !== 'undefined' && google.script && google.script.run) {
    return new Promise(function (coz, ret) {
      google.script.run
        .withSuccessHandler(coz)
        .withFailureHandler(function (e) {
          ret(new Error(e && e.message ? e.message : 'Sunucu verisi okunamadı'));
        })
        .veriGetir();
    });
  }
  var yol = (typeof window !== 'undefined' && window.YEREL_VERI_YOLU) ||
    (typeof document !== 'undefined' && document.body && document.body.getAttribute('data-veri')) ||
    '../veri/veri.json';
  return fetch(yol).then(function (y) {
    if (!y.ok) throw new Error('Veri yüklenemedi (HTTP ' + y.status + ')');
    return y.json();
  });
}

/* ------------------------------------------------------------ biçimlendirme */
function sayisal(v) { var n = Number(v); return isNaN(n) ? 0 : n; }

function sayiBicim(n) {
  return new Intl.NumberFormat('tr-TR').format(Math.round(sayisal(n)));
}
function paraBicim(n) { return sayiBicim(n) + ' ₺'; }
function yuzdeBicim(n, basamak) {
  basamak = (basamak == null) ? 0 : basamak;
  return new Intl.NumberFormat('tr-TR', {
    minimumFractionDigits: basamak, maximumFractionDigits: basamak
  }).format(sayisal(n)) + '%';
}

/* Tarih: Sheet Date veya 'YYYY-MM-DD' gelebilir -> normalize et. */
function isoTarih(d) {
  if (d instanceof Date && !isNaN(d)) {
    return d.getFullYear() + '-' +
      String(d.getMonth() + 1).padStart(2, '0') + '-' +
      String(d.getDate()).padStart(2, '0');
  }
  return String(d == null ? '' : d).slice(0, 10);
}
function tarihBicim(d) {
  var p = isoTarih(d).split('-');
  return p.length === 3 ? (p[2] + '.' + p[1] + '.' + p[0]) : isoTarih(d);
}
function ayAnahtari(d) { return isoTarih(d).slice(0, 7); } // YYYY-MM

/* --------------------------------------------------------------- dönüşümler */
function metrikler(satirlar) {
  var tu = 0, th = 0, tm = 0, hataAdet = {};
  satirlar.forEach(function (r) {
    tu += sayisal(r[SUTUN.uretimAdedi]);
    th += sayisal(r[SUTUN.hataAdedi]);
    tm += sayisal(r[SUTUN.maliyet]);
    var t = r[SUTUN.hataTipi];
    if (t) hataAdet[t] = (hataAdet[t] || 0) + sayisal(r[SUTUN.hataAdedi]);
  });
  var enSik = Object.keys(hataAdet).sort(function (a, b) {
    return hataAdet[b] - hataAdet[a];
  })[0] || '—';
  return {
    toplamUretim: tu,
    toplamHata: th,
    toplamMaliyet: tm,
    ppm: tu ? Math.round(th / tu * 1e6) : 0,
    fpy: tu ? (1 - th / tu) * 100 : 0,
    enSikHata: enSik
  };
}

/* Veriyi tarih ortasından ikiye böler: önceki / mevcut dönem. */
function donemAyir(satirlar) {
  var sirali = satirlar.slice().sort(function (a, b) {
    var x = isoTarih(a[SUTUN.tarih]), y = isoTarih(b[SUTUN.tarih]);
    return x < y ? -1 : (x > y ? 1 : 0);
  });
  var orta = Math.floor(sirali.length / 2);
  return { onceki: sirali.slice(0, orta), mevcut: sirali.slice(orta) };
}

/* Aylık seri: [{ay, etiket, uretim, hata, maliyet, ppm}] (kronolojik). */
function aylikSeri(satirlar) {
  var harita = {};
  satirlar.forEach(function (r) {
    var ay = ayAnahtari(r[SUTUN.tarih]); if (!ay) return;
    if (!harita[ay]) harita[ay] = { ay: ay, uretim: 0, hata: 0, maliyet: 0 };
    harita[ay].uretim += sayisal(r[SUTUN.uretimAdedi]);
    harita[ay].hata += sayisal(r[SUTUN.hataAdedi]);
    harita[ay].maliyet += sayisal(r[SUTUN.maliyet]);
  });
  return Object.keys(harita).sort().map(function (k) {
    var o = harita[k];
    o.ppm = o.uretim ? Math.round(o.hata / o.uretim * 1e6) : 0;
    o.etiket = AY_ADI[parseInt(k.slice(5, 7), 10) - 1] || k;
    return o;
  });
}

/* Pareto: {dizi:[{ad, adet, kumulatif%}], toplam}. */
function paretoHesap(satirlar) {
  var harita = {};
  satirlar.forEach(function (r) {
    var t = r[SUTUN.hataTipi]; if (!t) return;
    harita[t] = (harita[t] || 0) + sayisal(r[SUTUN.hataAdedi]);
  });
  var dizi = Object.keys(harita).map(function (k) {
    return { ad: k, adet: harita[k] };
  }).sort(function (a, b) { return b.adet - a.adet; });
  var toplam = dizi.reduce(function (s, x) { return s + x.adet; }, 0);
  var kum = 0;
  dizi.forEach(function (x) { kum += x.adet; x.kumulatif = toplam ? kum / toplam * 100 : 0; });
  return { dizi: dizi, toplam: toplam };
}

/* Hat bazında hata adedi: [{ad, adet}]. */
function hatBazli(satirlar) {
  var harita = {};
  satirlar.forEach(function (r) {
    var h = r[SUTUN.hat]; if (!h) return;
    harita[h] = (harita[h] || 0) + sayisal(r[SUTUN.hataAdedi]);
  });
  return Object.keys(harita).sort().map(function (k) { return { ad: k, adet: harita[k] }; });
}

/* Benzersiz hat listesi (filtre için). */
function hatlar(satirlar) {
  var k = {};
  satirlar.forEach(function (r) { if (r[SUTUN.hat]) k[r[SUTUN.hat]] = 1; });
  return Object.keys(k).sort();
}

/* p. yüzdelik (0-100) — eşik hesabı için. */
function yuzdelik(degerler, p) {
  if (!degerler.length) return 0;
  var s = degerler.slice().sort(function (a, b) { return a - b; });
  var i = Math.min(s.length - 1, Math.floor(p / 100 * s.length));
  return s[i];
}

/* Kritik kayıtlar: maliyete göre azalan ilk n; her birine Durum etiketi. */
function kritikKayitlar(satirlar, n) {
  var maliyetler = satirlar.map(function (r) { return sayisal(r[SUTUN.maliyet]); });
  var esikKritik = yuzdelik(maliyetler, 75);
  var esikIzle = yuzdelik(maliyetler, 50);
  return satirlar.slice()
    .sort(function (a, b) { return sayisal(b[SUTUN.maliyet]) - sayisal(a[SUTUN.maliyet]); })
    .slice(0, n || 12)
    .map(function (r) {
      var m = sayisal(r[SUTUN.maliyet]);
      var durum = (m >= esikKritik)
        ? { ad: 'Kritik', ikon: '⚠', sinif: 'tehlike' }
        : (m >= esikIzle)
          ? { ad: 'İzle', ikon: '●', sinif: 'uyari' }
          : { ad: 'Normal', ikon: '✓', sinif: 'basari' };
      return { satir: r, durum: durum };
    });
}
