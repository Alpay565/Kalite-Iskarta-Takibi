'use strict';
/*
 * GRAFİKLER — saf SVG üretimi (dış kütüphane/CDN yok).
 * Her fonksiyon bir SVG dizesi döndürür; renkler CSS değişkenlerinden okunur.
 * Erişilebilirlik: role="img" + <title>/<desc> + lejant (renk tek sinyal değil).
 */

var GRAFIK_W = 760, GRAFIK_H = 340;
var KENAR = { sol: 60, sag: 60, ust: 20, alt: 64 };

function kacis(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
  });
}

function tema(ad, varsayilan) {
  try {
    var v = getComputedStyle(document.documentElement).getPropertyValue(ad).trim();
    return v || varsayilan;
  } catch (e) { return varsayilan; }
}

function guzelTavan(m) {
  if (m <= 0) return 1;
  var us = Math.pow(10, Math.floor(Math.log10(m)));
  var n = m / us;
  var k = n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10;
  return k * us;
}

function cizimAlani() {
  return {
    x0: KENAR.sol, x1: GRAFIK_W - KENAR.sag,
    y0: KENAR.ust, y1: GRAFIK_H - KENAR.alt
  };
}

/* y ekseni: 4 aralık ızgara + etiketler. */
function eksenY(a, maxDeger, bicim, sagEksen, sagMax, sagBicim) {
  var renkIzgara = tema('--gri-200', '#E4E9E5');
  var renkMetin = tema('--murekkep', '#16261C');
  var s = '';
  var adim = 4;
  for (var i = 0; i <= adim; i++) {
    var y = a.y1 - (i / adim) * (a.y1 - a.y0);
    var deger = (maxDeger * i) / adim;
    s += '<line x1="' + a.x0 + '" y1="' + y + '" x2="' + a.x1 + '" y2="' + y +
         '" stroke="' + renkIzgara + '" stroke-width="1"/>';
    s += '<text x="' + (a.x0 - 8) + '" y="' + (y + 4) + '" text-anchor="end" ' +
         'font-size="11" fill="' + renkMetin + '">' + kacis(bicim ? bicim(deger) : Math.round(deger)) + '</text>';
    if (sagEksen) {
      var sd = (sagMax * i) / adim;
      s += '<text x="' + (a.x1 + 8) + '" y="' + (y + 4) + '" text-anchor="start" ' +
           'font-size="11" fill="' + renkMetin + '">' + kacis(sagBicim ? sagBicim(sd) : Math.round(sd)) + '</text>';
    }
  }
  return s;
}

function xEtiketleri(a, etiketler, dondur) {
  var renkMetin = tema('--murekkep', '#16261C');
  var n = etiketler.length, s = '';
  for (var i = 0; i < n; i++) {
    var x = a.x0 + (n === 1 ? (a.x1 - a.x0) / 2 : (i + 0.5) * (a.x1 - a.x0) / n);
    if (dondur) {
      s += '<text x="' + x + '" y="' + (a.y1 + 16) + '" text-anchor="end" font-size="11" ' +
           'fill="' + renkMetin + '" transform="rotate(-25 ' + x + ' ' + (a.y1 + 16) + ')">' +
           kacis(etiketler[i]) + '</text>';
    } else {
      s += '<text x="' + x + '" y="' + (a.y1 + 18) + '" text-anchor="middle" font-size="11" ' +
           'fill="' + renkMetin + '">' + kacis(etiketler[i]) + '</text>';
    }
  }
  return s;
}

function lejant(ogeler) {
  // ogeler: [{ad, renk, kesik}]
  var renkMetin = tema('--murekkep', '#16261C');
  var x = KENAR.sol, parcalar = [];
  ogeler.forEach(function (o) {
    var cizgi = o.kesik
      ? '<line x1="' + x + '" y1="10" x2="' + (x + 18) + '" y2="10" stroke="' + o.renk +
        '" stroke-width="3" stroke-dasharray="4 3"/>'
      : '<rect x="' + x + '" y="4" width="18" height="12" rx="2" fill="' + o.renk + '"/>';
    parcalar.push(cizgi +
      '<text x="' + (x + 24) + '" y="14" font-size="12" fill="' + renkMetin + '">' + kacis(o.ad) + '</text>');
    x += 24 + 8 + (String(o.ad).length * 7) + 18;
  });
  return '<g>' + parcalar.join('') + '</g>';
}

function svgSar(ic, baslik, lej) {
  return '<svg viewBox="0 0 ' + GRAFIK_W + ' ' + (GRAFIK_H + 22) + '" width="100%" ' +
    'preserveAspectRatio="xMidYMid meet" role="img" aria-label="' + kacis(baslik) + '">' +
    '<title>' + kacis(baslik) + '</title>' +
    (lej ? '<g transform="translate(0,0)">' + lej + '</g>' : '') +
    '<g transform="translate(0,' + (lej ? 22 : 0) + ')">' + ic + '</g>' +
    '</svg>';
}

/* --------------------------------------------------------------- çizgi grafik */
/* opts: { seriler:[{ad,renk,kesik?,deger:[...]}], etiketler:[...], yBicim, baslik,
 *         referans?:{deger, ad, renk} } */
function cizgiGrafik(opts) {
  var a = cizimAlani();
  var tumDeger = [];
  opts.seriler.forEach(function (s) { tumDeger = tumDeger.concat(s.deger); });
  if (opts.referans) tumDeger.push(opts.referans.deger);
  var max = guzelTavan(Math.max.apply(null, tumDeger.concat([1])));
  var n = opts.etiketler.length;
  function px(i) { return a.x0 + (n === 1 ? (a.x1 - a.x0) / 2 : i * (a.x1 - a.x0) / (n - 1)); }
  function py(v) { return a.y1 - (v / max) * (a.y1 - a.y0); }

  var ic = eksenY(a, max, opts.yBicim) + xEtiketleri(a, opts.etiketler, false);

  if (opts.referans) {
    var yr = py(opts.referans.deger);
    ic += '<line x1="' + a.x0 + '" y1="' + yr + '" x2="' + a.x1 + '" y2="' + yr +
      '" stroke="' + opts.referans.renk + '" stroke-width="2" stroke-dasharray="6 4"/>';
  }

  opts.seriler.forEach(function (s) {
    var d = s.deger.map(function (v, i) { return (i ? 'L' : 'M') + px(i) + ' ' + py(v); }).join(' ');
    ic += '<path d="' + d + '" fill="none" stroke="' + s.renk + '" stroke-width="3" ' +
      (s.kesik ? 'stroke-dasharray="5 4" ' : '') + 'stroke-linejoin="round"/>';
    s.deger.forEach(function (v, i) {
      ic += '<circle cx="' + px(i) + '" cy="' + py(v) + '" r="3.5" fill="' + s.renk + '"/>';
    });
  });

  var lej = lejant(opts.seriler.map(function (s) { return { ad: s.ad, renk: s.renk, kesik: s.kesik }; })
    .concat(opts.referans ? [{ ad: opts.referans.ad, renk: opts.referans.renk, kesik: true }] : []));
  return svgSar(ic, opts.baslik, lej);
}

/* --------------------------------------------------------------- sütun grafik */
/* opts: { kategoriler:[...], degerler:[...], renk, yBicim, baslik, vurguSon? } */
function sutunGrafik(opts) {
  var a = cizimAlani();
  var max = guzelTavan(Math.max.apply(null, opts.degerler.concat([1])));
  var n = opts.degerler.length;
  var bandGen = (a.x1 - a.x0) / n;
  var sutunGen = bandGen * 0.6;
  var renk = opts.renk || tema('--valeo-yesil-koyu', '#4E8A00');
  var renkVurgu = tema('--valeo-yesil', '#82E600');
  function py(v) { return a.y1 - (v / max) * (a.y1 - a.y0); }

  var ic = eksenY(a, max, opts.yBicim) + xEtiketleri(a, opts.kategoriler, true);
  opts.degerler.forEach(function (v, i) {
    var x = a.x0 + i * bandGen + (bandGen - sutunGen) / 2;
    var y = py(v);
    var dolgu = (opts.vurguSon && i === n - 1) ? renkVurgu : renk;
    ic += '<rect x="' + x + '" y="' + y + '" width="' + sutunGen + '" height="' + (a.y1 - y) +
      '" rx="3" fill="' + dolgu + '"><title>' + kacis(opts.kategoriler[i] + ': ' +
      (opts.yBicim ? opts.yBicim(v) : v)) + '</title></rect>';
  });
  return svgSar(ic, opts.baslik, null);
}

/* --------------------------------------------------------------- Pareto grafik */
/* opts: { dizi:[{ad,adet,kumulatif}], yBicim, baslik, esik? } */
function paretoGrafik(opts) {
  var a = cizimAlani();
  var adetler = opts.dizi.map(function (x) { return x.adet; });
  var max = guzelTavan(Math.max.apply(null, adetler.concat([1])));
  var n = opts.dizi.length;
  var bandGen = (a.x1 - a.x0) / n;
  var sutunGen = bandGen * 0.6;
  var renkSutun = tema('--valeo-yesil-koyu', '#4E8A00');
  var renkCizgi = tema('--murekkep', '#16261C');
  var renkEsik = tema('--tehlike', '#C62828');
  var esik = opts.esik || 80;
  function py(v) { return a.y1 - (v / max) * (a.y1 - a.y0); }
  function pyYuzde(p) { return a.y1 - (p / 100) * (a.y1 - a.y0); }
  function px(i) { return a.x0 + (i + 0.5) * bandGen; }

  var ic = eksenY(a, max, opts.yBicim, true, 100, function (p) { return Math.round(p) + '%'; });
  ic += xEtiketleri(a, opts.dizi.map(function (x) { return x.ad; }), true);

  // sütunlar
  opts.dizi.forEach(function (x, i) {
    var px0 = a.x0 + i * bandGen + (bandGen - sutunGen) / 2;
    var y = py(x.adet);
    ic += '<rect x="' + px0 + '" y="' + y + '" width="' + sutunGen + '" height="' + (a.y1 - y) +
      '" rx="3" fill="' + renkSutun + '"><title>' + kacis(x.ad + ': ' + x.adet + ' adet') +
      '</title></rect>';
  });

  // %80 eşik çizgisi
  var ye = pyYuzde(esik);
  ic += '<line x1="' + a.x0 + '" y1="' + ye + '" x2="' + a.x1 + '" y2="' + ye +
    '" stroke="' + renkEsik + '" stroke-width="1.5" stroke-dasharray="6 4"/>';
  ic += '<text x="' + (a.x1) + '" y="' + (ye - 5) + '" text-anchor="end" font-size="11" fill="' +
    renkEsik + '">%' + esik + ' eşiği</text>';

  // kümülatif % çizgisi
  var d = opts.dizi.map(function (x, i) {
    return (i ? 'L' : 'M') + px(i) + ' ' + pyYuzde(x.kumulatif);
  }).join(' ');
  ic += '<path d="' + d + '" fill="none" stroke="' + renkCizgi + '" stroke-width="2.5" stroke-linejoin="round"/>';
  opts.dizi.forEach(function (x, i) {
    ic += '<circle cx="' + px(i) + '" cy="' + pyYuzde(x.kumulatif) + '" r="3.5" fill="' + renkCizgi + '">' +
      '<title>' + kacis('Kümülatif: ' + Math.round(x.kumulatif) + '%') + '</title></circle>';
  });

  var lej = lejant([
    { ad: 'Hata adedi', renk: renkSutun },
    { ad: 'Kümülatif %', renk: renkCizgi },
    { ad: '%' + esik + ' eşiği', renk: renkEsik, kesik: true }
  ]);
  return svgSar(ic, opts.baslik, lej);
}
