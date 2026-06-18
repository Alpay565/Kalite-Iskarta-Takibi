'use strict';
/*
 * UYGULAMA — orkestrasyon ve ekran render'ı.
 * Durumlar: yükleniyor / boş / hata her bölümde ele alınır.
 * Satır içi style/onclick KULLANILMAZ (kural #4); olaylar delegasyonla bağlanır.
 */

var Durum = {
  veri: null, hata: null, yukleniyor: true,
  aktifEkran: 'e1', filtreHat: 'Hepsi'
};

document.addEventListener('DOMContentLoaded', baslat);

function baslat() {
  sekmeleriKur();
  logoYukle();
  guncellemeZamani();

  var icerik = document.getElementById('icerik');
  if (icerik) {
    icerik.addEventListener('click', function (e) {
      if (e.target.closest('[data-aksiyon="yenile"]')) yenidenYukle();
    });
  }
  var filtre = document.getElementById('filtreHat');
  if (filtre) {
    filtre.addEventListener('change', function () {
      Durum.filtreHat = filtre.value; ciz();
    });
  }
  yenidenYukle();
}

/* ------------------------------------------------------------------- yükleme */
function yenidenYukle() {
  Durum.yukleniyor = true; Durum.hata = null;
  ciz();
  veriYukle().then(function (satirlar) {
    Durum.veri = Array.isArray(satirlar) ? satirlar : [];
    Durum.yukleniyor = false;
    filtreSecenekleriDoldur();
    ciz();
  }).catch(function (e) {
    Durum.hata = (e && e.message) ? e.message : 'Bilinmeyen hata';
    Durum.yukleniyor = false;
    ciz();
  });
}

function filtreliVeri() {
  var v = Durum.veri || [];
  if (Durum.filtreHat && Durum.filtreHat !== 'Hepsi') {
    v = v.filter(function (r) { return r[SUTUN.hat] === Durum.filtreHat; });
  }
  return v;
}

/* --------------------------------------------------------------- ana render */
function ciz() {
  var icerik = document.getElementById('icerik');
  var bilgi = document.getElementById('kayitBilgi');
  if (!icerik) return;

  if (Durum.yukleniyor) { icerik.innerHTML = durumIcerik('yukleniyor'); if (bilgi) bilgi.textContent = ''; return; }
  if (Durum.hata) { icerik.innerHTML = durumIcerik('hata', Durum.hata); if (bilgi) bilgi.textContent = ''; return; }

  var veri = filtreliVeri();
  if (bilgi) {
    bilgi.textContent = sayiBicim(veri.length) + ' kayıt' +
      (Durum.filtreHat !== 'Hepsi' ? ' · ' + Durum.filtreHat : '');
  }
  if (!veri.length) { icerik.innerHTML = durumIcerik('bos'); return; }

  var harita = { e1: ekranE1, e2: ekranE2, e3: ekranE3, e4: ekranE4 };
  icerik.innerHTML = (harita[Durum.aktifEkran] || ekranE1)(veri);
}

/* ---------------------------------------------------------------- E1 KPI'lar */
function ekranE1(satirlar) {
  var d = donemAyir(satirlar);
  var m = metrikler(satirlar);
  var mev = metrikler(d.mevcut), onc = metrikler(d.onceki);

  function delta(alan, dusukIyi) {
    var a = mev[alan], b = onc[alan];
    if (!b) return null;
    var fark = (a - b) / b * 100;
    var yon = fark > 0.5 ? 'artis' : (fark < -0.5 ? 'azalis' : 'duz');
    var iyi = (yon === 'duz') ? true : (dusukIyi ? fark < 0 : fark > 0);
    return { yuzde: Math.abs(fark), yon: yon, iyi: iyi };
  }

  var kartlar = [
    kpiKart('Toplam Üretim', sayiBicim(m.toplamUretim) + ' adet', delta('toplamUretim', false)),
    kpiKart('Toplam Hata', sayiBicim(m.toplamHata) + ' adet', delta('toplamHata', true)),
    kpiKart('PPM', sayiBicim(m.ppm), delta('ppm', true)),
    kpiKart('FPY', yuzdeBicim(m.fpy, 2), delta('fpy', false)),
    kpiKart('Toplam Iskarta', paraBicim(m.toplamMaliyet), delta('toplamMaliyet', true)),
    kpiKart('En Sık Hata', m.enSikHata, null)
  ];

  var not = '<p class="dipnot">PPM = (Σ Hata ÷ Σ Üretim) × 1.000.000 · ' +
    'FPY = (1 − Σ Hata ÷ Σ Üretim) × 100 · ' +
    'Değişim oku mevcut dönemi önceki döneme kıyaslar.</p>';

  return '<div class="kpi-izgara">' + kartlar.join('') + '</div>' + not;
}

function kpiKart(ad, deger, delta) {
  var alt;
  if (delta) {
    var ok = delta.yon === 'artis' ? '▲' : (delta.yon === 'azalis' ? '▼' : '▬');
    var sinif = delta.iyi ? 'iyi' : 'kotu';
    alt = '<div class="kpi-delta ' + sinif + '">' + ok + ' ' + yuzdeBicim(delta.yuzde, 1) +
      ' <span class="kpi-delta-not">önceki döneme göre</span></div>';
  } else {
    alt = '<div class="kpi-delta noter">— referans yok</div>';
  }
  return '<div class="kpi-kart"><div class="kpi-ad">' + kacis(ad) + '</div>' +
    '<div class="kpi-deger">' + kacis(deger) + '</div>' + alt + '</div>';
}

/* ----------------------------------------------------------------- E2 Trend */
function ekranE2(satirlar) {
  var seri = aylikSeri(satirlar);
  if (!seri.length) return durumIcerik('bos');
  var etik = seri.map(function (s) { return s.etiket; });
  var ppm = seri.map(function (s) { return s.ppm; });
  var maliyet = seri.map(function (s) { return s.maliyet; });

  var yari = Math.max(1, Math.floor(seri.length / 2));
  var refPpm = Math.round(ppm.slice(0, yari).reduce(function (s, x) { return s + x; }, 0) / yari);
  var yesil = tema('--valeo-yesil-koyu', '#4E8A00');
  var gri = tema('--gri-referans', '#9AA3A0');

  var g1 = cizgiGrafik({
    baslik: 'Aylık PPM eğilimi',
    etiketler: etik,
    yBicim: function (v) { return sayiBicim(v); },
    seriler: [{ ad: 'Mevcut dönem PPM', renk: yesil, deger: ppm }],
    referans: { deger: refPpm, ad: 'Önceki dönem ort. (' + sayiBicim(refPpm) + ')', renk: gri }
  });
  var g2 = sutunGrafik({
    baslik: 'Aylık Iskarta Maliyeti',
    kategoriler: etik, degerler: maliyet,
    yBicim: function (v) { return sayiBicim(v); },
    vurguSon: true
  });
  return grafikKart('Aylık PPM Eğilimi (dönem karşılaştırmalı)', g1) +
    grafikKart('Aylık Iskarta Maliyeti (₺)', g2);
}

/* ---------------------------------------------------------------- E3 Pareto */
function ekranE3(satirlar) {
  var p = paretoHesap(satirlar);
  if (!p.dizi.length) return durumIcerik('bos');
  var g1 = paretoGrafik({
    baslik: 'Hata Tipi Pareto', dizi: p.dizi,
    yBicim: function (v) { return sayiBicim(v); }, esik: 80
  });
  var hb = hatBazli(satirlar);
  var g2 = sutunGrafik({
    baslik: 'Hat Bazında Hata Adedi',
    kategoriler: hb.map(function (x) { return x.ad; }),
    degerler: hb.map(function (x) { return x.adet; }),
    yBicim: function (v) { return sayiBicim(v); }
  });
  return grafikKart('Hata Tipi Pareto (80/20 Odak)', g1) +
    grafikKart('Hat Bazında Hata Adedi', g2);
}

/* ------------------------------------------------------------ E4 Kritik tablo */
function ekranE4(satirlar) {
  var kayitlar = kritikKayitlar(satirlar, 12);
  if (!kayitlar.length) return durumIcerik('bos');
  var govde = kayitlar.map(function (k) {
    var r = k.satir, dr = k.durum;
    return '<tr>' +
      '<td>' + kacis(tarihBicim(r[SUTUN.tarih])) + '</td>' +
      '<td>' + kacis(r[SUTUN.hat]) + '</td>' +
      '<td>' + kacis(r[SUTUN.parca]) + '</td>' +
      '<td>' + kacis(r[SUTUN.hataTipi]) + '</td>' +
      '<td class="say">' + sayiBicim(r[SUTUN.hataAdedi]) + '</td>' +
      '<td class="say">' + paraBicim(r[SUTUN.maliyet]) + '</td>' +
      '<td>' + kacis(r[SUTUN.asama]) + '</td>' +
      '<td><span class="rozet ' + dr.sinif + '">' + dr.ikon + ' ' + dr.ad + '</span></td>' +
      '</tr>';
  }).join('');
  var tablo = '<table class="tablo"><thead><tr>' +
    '<th>Tarih</th><th>Hat</th><th>Parça No</th><th>Hata Tipi</th>' +
    '<th class="say">Hata</th><th class="say">Iskarta (₺)</th>' +
    '<th>Tespit Aşaması</th><th>Durum</th></tr></thead><tbody>' + govde + '</tbody></table>';
  return grafikKart('En Yüksek Maliyetli 12 Kayıt', tablo);
}

/* ------------------------------------------------------------------ yardımcı */
function grafikKart(baslik, ic) {
  return '<section class="kart"><h2 class="kart-baslik">' + kacis(baslik) + '</h2>' +
    '<div class="grafik-govde">' + ic + '</div></section>';
}

function durumIcerik(tip, mesaj) {
  if (tip === 'yukleniyor') {
    return '<div class="durum" role="status" aria-live="polite">' +
      '<div class="iskelet iskelet-satir"></div>' +
      '<div class="iskelet-izgara">' +
      '<div class="iskelet iskelet-kutu"></div><div class="iskelet iskelet-kutu"></div>' +
      '<div class="iskelet iskelet-kutu"></div><div class="iskelet iskelet-kutu"></div></div>' +
      '<div class="durum-mesaj">Veri yükleniyor…</div></div>';
  }
  if (tip === 'hata') {
    return '<div class="durum hata" role="alert">' +
      '<div class="durum-ikon">⚠</div>' +
      '<div class="durum-baslik">Veri yüklenemedi</div>' +
      '<div class="durum-mesaj">' + kacis(mesaj || '') + '</div>' +
      '<button class="btn" type="button" data-aksiyon="yenile">Tekrar dene</button></div>';
  }
  return '<div class="durum bos">' +
    '<div class="durum-ikon">∅</div>' +
    '<div class="durum-baslik">Veri bulunamadı</div>' +
    '<div class="durum-mesaj">' + kacis(mesaj || 'Seçili filtre için kayıt bulunmuyor.') + '</div></div>';
}

/* -------------------------------------------------------------- sekme/filtre */
function sekmeleriKur() {
  var dugmeler = document.querySelectorAll('[data-ekran]');
  Array.prototype.forEach.call(dugmeler, function (d) {
    d.addEventListener('click', function () {
      Durum.aktifEkran = d.getAttribute('data-ekran');
      Array.prototype.forEach.call(dugmeler, function (x) {
        var aktif = x === d;
        x.classList.toggle('aktif', aktif);
        x.setAttribute('aria-selected', aktif ? 'true' : 'false');
      });
      ciz();
    });
  });
}

function filtreSecenekleriDoldur() {
  var filtre = document.getElementById('filtreHat');
  if (!filtre) return;
  var mevcut = Durum.filtreHat || 'Hepsi';
  var secenekler = ['Hepsi'].concat(hatlar(Durum.veri || []));
  filtre.innerHTML = secenekler.map(function (h) {
    return '<option value="' + kacis(h) + '"' + (h === mevcut ? ' selected' : '') + '>' +
      kacis(h === 'Hepsi' ? 'Tüm Hatlar' : h) + '</option>';
  }).join('');
}

/* ------------------------------------------------------------------ logo/üst */
function logoYukle() {
  var img = document.getElementById('logo');
  if (!img) return;
  function yaziMarka() {
    var span = document.createElement('span');
    span.className = 'logo-yazi';
    span.textContent = 'VALEO';
    if (img.parentNode) img.parentNode.replaceChild(span, img);
  }
  img.addEventListener('error', yaziMarka);
  if (typeof google !== 'undefined' && google.script && google.script.run) {
    google.script.run
      .withSuccessHandler(function (uri) { if (uri) { img.src = uri; } else { yaziMarka(); } })
      .withFailureHandler(yaziMarka)
      .logoGetir();
  } else {
    var url = (typeof window !== 'undefined' && window.YEREL_LOGO_URL) ||
      (document.body && document.body.getAttribute('data-logo'));
    if (url) { img.src = url; } else { yaziMarka(); }
  }
}

function guncellemeZamani() {
  var el = document.getElementById('guncelleme');
  if (!el) return;
  var d = new Date();
  el.textContent = 'Son güncelleme: ' + tarihBicim(d) + ' ' +
    String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
}
