#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rapor.pdf (+ rapor/rapor.md) üreticisi — Bölüm 8 tüm başlıklar.

Tek kaynak: icerik blok listesi olarak tutulur; hem PDF (fpdf2, gömülü DejaVu
fontu -> Türkçe + ₺) hem Markdown üretilir. Mimari diyagram PDF'e natif çizilir.

Calistir:  python3 rapor/rapor_uret.py
Gerekli :  pip install fpdf2   (DejaVu fontu sistemde mevcut)
"""

from pathlib import Path
import struct
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace

KOK = Path(__file__).resolve().parent.parent
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

DERIN = (31, 58, 14)
YESIL = (78, 138, 0)
INK = (22, 38, 28)
GRI = (90, 100, 96)
ACIK = (238, 246, 227)
KIRMIZI = (198, 40, 40)


class Rapor(FPDF):
    def footer(self):
        self.set_y(-14)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(*GRI)
        self.cell(0, 8, f"VALEO · S2 Kalite & Iskarta — Yönetişim Raporu · Sayfa {self.page_no()}",
                  align="C")


def yeni_pdf():
    pdf = Rapor(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(18, 16, 18)
    pdf.add_font("DejaVu", "", FONT_R)
    pdf.add_font("DejaVu", "B", FONT_B)
    pdf.add_page()
    return pdf


# ----------------------------------------------------- içerik blokları (tek kaynak)
def icerik():
    B = []
    B.append(("kapak",))
    B.append(("h1", "1. Senaryo ve Persona"))
    B.append(("p", "Senaryo: S2 — Kalite & Iskarta Takibi. Persona: bir VALEO üretim "
                    "tesisinde çalışan Kalite Mühendisi. Amaç, kalite/ıskarta verisinden "
                    "yönetici düzeyinde, tek ekranda okunan bir kontrol paneli üretmek; "
                    "ama asıl hedef bu paneli her seferinde aynı standartta üreten bir "
                    "yönetişim katmanı kurmaktır."))
    B.append(("p", "Panonun yanıtladığı üç karar sorusu:"))
    B.append(("liste", [
        "Hangi hata tipleri toplam hatanın/ıskartanın çoğunu üretiyor? (Pareto · 80/20 odak)",
        "PPM ve ıskarta maliyeti dönemler arasında nasıl değişiyor? (trend, mevcut vs önceki dönem)",
        "En yüksek maliyetli/kritik kayıtlar hangileri ve hangi tespit aşamasında yakalanıyor? "
        "(geç tespit = pahalı)",
    ]))

    B.append(("h1", "2. Yönetişim Mimarisi"))
    B.append(("p", "Çözüm üç katmandan oluşur: (1) tek canlı veri kaynağı, (2) yönetişim + "
                   "üretim katmanı, (3) çalışan çıktı. Yönetişim üç parçayla sağlanır: Kalıcı "
                   "Talimat (Rule), Üretim Standardı (Skill) ve Bağlam (Context) yönetimi. Bunlar "
                   "Claude Project'e kalıcı yüklenir; böylece her sohbette otomatik uygulanır."))
    B.append(("diyagram",))
    B.append(("p", "Şekil 1. Yönetişimli üretim hattı. Sentetik veri Google Sheets'e aktarılır "
                   "(tek kaynak). Kurumsal politika iş Google Workspace'inin Claude'a bağlanmasına "
                   "(Connector) izin vermediğinden, veri Claude'a tek seferlik Project dosyası (CSV) "
                   "olarak verilir; Claude, Rule+Skill+Context kuralları altında Apps Script dashboard "
                   "kodunu üretir. Yayınlanan web app, veriyi aynı Google Sheet'ten SpreadsheetApp ile "
                   "ÇALIŞMA ANINDA (canlı) okur — canlı veri ilkesi bu katmanda korunur ve Doğrulama #5 "
                   "ile kanıtlanır. Yüksek çözünürlüklü hali: rapor/mimari-diyagram.svg."))
    B.append(("p", "Rule (kalici-talimat.md): ≥6 makine-denetlenebilir kural — para ₺ + tr-TR "
                   "binlik, tüm etiketler Türkçe, veri koda gömülmez (bağlı kaynaktan okunur), satır "
                   "içi stil/script yok, WCAG AA + renk tek başına anlam taşımaz, her ekranda boş/"
                   "hata/yüklenme durumu, tarih GG.AA.YYYY. Skill (uretim-standardi.md): tasarım "
                   "sistemi (VALEO paleti, tipografi, boşluk), ekran anatomisi, grafik seçim rehberi, "
                   "metrik tanımları. Context: veriyi sohbete gömmek yerine bağlı okutmak, standardı "
                   "tek seferlik dosya olarak yüklemek."))

    B.append(("h1", "3. Bağlam (Context) Yönetimi"))
    B.append(("p", "Bağlam bütçesi şu ilkelerle yönetildi:"))
    B.append(("liste", [
        "Ham veri her mesaja yapıştırılmadı; Claude'a tek seferlik Project dosyası (CSV) olarak "
        "verildi (kurumsal politika Connector'a izin vermedi). Üretilen dashboard veriyi koda gömmez; "
        "çalışma anında bağlı Sheet'ten okur — veri değişince kod değişmeden güncellenir.",
        "Rule ve Skill, her mesajda tekrarlanmak yerine Project'e bir kez yüklendi (kalıcı bağlam).",
        "Standart, uzun açıklama yerine kısa ve denetlenebilir kurallar olarak yazıldı (düşük token, "
        "yüksek belirlilik).",
        "Dashboard kodu veriyi gömmediği için çıktı sabit boyutlu kaldı; veri büyüse de kod büyümez.",
    ]))

    B.append(("h1", "4. Tur A ve Tur B Karşılaştırması"))
    B.append(("p", "Aynı istek iki ortamda denendi. Tur A: yönetişim olmayan boş sohbet (kontrol "
                   "grubu). Tur B: Rule+Skill+Context yüklü Project. Her tur 2 kez tekrarlandı."))
    B.append(("tablo",
              ["Boyut", "Tur A — Boş Sohbet", "Tur B — Project (Yönetişimli)"],
              [
                  ["Tekrar kararlılığı", "Her denemede farklı yapı/renk/dil", "İki denemede de aynı 4 ekran ve stil"],
                  ["Para/dil", "Bazen $, İngilizce etiketler", "Her zaman ₺ + tr-TR + Türkçe"],
                  ["Veri kaynağı", "Veriyi koda gömme eğilimi", "Üretilen kod Sheet'ten canlı okur (veri gömülmez)"],
                  ["Durumlar", "Boş/hata durumu çoğu kez yok", "Yükleniyor/boş/hata her ekranda"],
                  ["Erişilebilirlik", "Renk tek sinyal", "Etiket + ikon + AA kontrast"],
              ]))
    B.append(("p", "Sonuç: yönetişim katmanı, çıktının kalitesini kişisel/şans faktöründen "
                   "kurala taşıdı; tekrar üretilebilirlik Tur B'de net biçimde sağlandı."))

    B.append(("h1", "5. En Etkili Promptlar"))
    B.append(("p", "Aşağıdaki promptların tam metinleri transcripts/ klasöründe yer alır; "
                   "en etkili olanlar:"))
    B.append(("liste", [
        "Tur B üretim: \"Project'e yüklü veri.csv'yi kullan; üretilen kodda veriyi GÖMME — Apps "
        "Script ile bağlı Google Sheet'ten çalışma anında oku. Üretim standardındaki tasarım "
        "sistemine ve kalıcı talimattaki kurallara birebir uyarak Apps Script web app dashboard'unu "
        "(Kod.gs + index + stil + script) üret.\"",
        "Kararlılık testi: \"Aynı isteği tekrar uygula; çıktının önceki üretimle ekran, stil ve "
        "metrik tanımı açısından aynı olduğunu doğrula, farkları listele.\"",
        "Kural ihlali denemesi: \"KPI'ları $ ile ve İngilizce göster\" → beklenen: Claude kuralı "
        "hatırlatıp ₺ + Türkçe'de ısrar eder (yönetişim çalışıyor).",
        "Canlı veri: \"Google Sheet'te bir hücreyi değiştir → deploy edilen web app URL'sini yenile "
        "→ KPI/grafik güncellenir (Apps Script Sheet'i canlı okur).\"",
    ]))

    B.append(("h1", "6. Engeller ve Çözümler"))
    B.append(("liste", [
        "Engel: Kurumsal politika, iş Google Workspace'inin Claude'a bağlanmasını (Connector) "
        "yasaklıyor. Çözüm: veri Claude'a tek seferlik Project dosyası (CSV) olarak verildi; canlı "
        "veri ilkesi, üretilen dashboard'un Apps Script ile bağlı Sheet'i çalışma anında okumasıyla "
        "korundu (Doğrulama #5 geçer).",
        "Engel: Apps Script HtmlService statik .css/.js servis edemez. Çözüm: CSS/JS tek kaynakta "
        "(kaynak/) tutulup include ile tek stil + tek script partial'ına derlenir (derle_appsscript.py); "
        "'tek tasarım sistemi' kuralının ruhu korunur.",
        "Engel: Apps Script IFRAME sandbox'ta dış CDN (grafik kütüphanesi) riski. Çözüm: grafikler "
        "elle SVG ile çizildi; dış bağımlılık yok, çevrimdışı çalışır.",
        "Engel: Drive'daki VALEO logosunda public paylaşım/CSP/hotlink sorunu. Çözüm: logo sunucuda "
        "DriveApp ile okunup base64 data-URI olarak döndürülür; yüklenmezse 'VALEO' yazı-marka fallback.",
        "Engel: boş sohbette çıktı sapması. Çözüm: Rule+Skill yüklü Project + otomatik kural denetimi "
        "(otomasyon/kural-denetimi.py) ile tekrar üretilebilirlik.",
    ]))

    B.append(("h1", "7. Öz-Değerlendirme"))
    B.append(("p", "Rubrik kontrol listesi (kendi değerlendirmem):"))
    B.append(("tablo",
              ["Kriter", "Durum"],
              [
                  ["Bağlam + Rule (kalıcı talimat)", "Tamam — ≥6 denetlenebilir kural, Project'e yüklü"],
                  ["Skill / Üretim standardı", "Tamam — tasarım sistemi + ekran anatomisi + grafik seçimi"],
                  ["Canlı veri — Apps Script ile Sheet'ten canlı okuma", "Tamam (Doğrulama #5). Not: Connector kurumsal politika nedeniyle kullanılmadı; veri Claude'a dosya olarak verildi"],
                  ["Context yönetimi", "Tamam — bağlı okuma + tek seferlik standart yükleme"],
                  ["İki tur (A boş / B project)", "Tamam — 2'şer tekrar, kararlılık gösterildi"],
                  ["Dashboard (4 ekran, kurallara uygun)", "Tamam — KPI/Trend/Pareto/Tablo + durumlar"],
                  ["Bonus otomasyon", "Tamam — günlük PPM e-posta tetikleyicisi (Apps Script)"],
              ]))
    B.append(("p", "Geliştirme alanı: Şu an dönem ayrımı veriyi tarih ortasından ikiye bölüyor; "
                   "ileride kullanıcı seçilebilir tarih aralığı (örn. son 30 gün vs önceki 30 gün) ve "
                   "hat bazlı PPM hedef çizgileri eklenebilir. Ayrıca erişilebilirlik için grafiklere "
                   "ekran okuyucu dostu veri tablosu alternatifi konabilir."))

    B.append(("h1", "8. Doğrulama ve Kanıt"))
    B.append(("p", "Altı doğrulama senaryosu transcripts/dogrulama.md içinde adım adım yer alır: "
                   "(1) tekrar üretilebilirlik, (2) boş/bozuk veri, (3) kural ihlali denemesi, "
                   "(4) standardın uygulanışı, (5) canlı veri değişikliği, (6) bağlam bütçesi. "
                   "Yönetişim QA betiği (otomasyon/kural-denetimi.py) satır içi stil/script ve gömülü "
                   "veri denetimini 8/8 PASS ile geçer (otomasyon/kanit-log.txt)."))

    B.append(("h1", "9. Ekran Görüntüleri ve Kanıt"))
    B.append(("p", "Aşağıda dashboard'un dört ekranının gerçek görüntüleri yer alır. claude.ai "
                   "(Project/Rule/Skill), iki tur, canlı veri (web app) ve tetikleyici kanıtları "
                   "gerçek oturumlardan eklenir; ilgili PNG'ler ekran-goruntuleri/ klasörüne konup "
                   "rapor yeniden üretildiğinde otomatik olarak buraya gömülür."))
    B.append(("h2", "Dashboard ekranları"))
    B.append(("gorsel", "dashboard-genel.png",
              "E1 — Genel Bakış (6 KPI: Üretim, Hata, PPM, FPY, Iskarta ₺, En Sık Hata)"))
    B.append(("gorsel", "dashboard-trend.png",
              "E2 — Trend (aylık PPM + önceki dönem referansı; aylık ıskarta maliyeti)"))
    B.append(("gorsel", "dashboard-pareto.png",
              "E3 — Pareto (hata tipleri 80/20 + hat bazında kırılım)"))
    B.append(("gorsel", "dashboard-tablo.png",
              "E4 — Kritik Tablo (en yüksek maliyetli kayıtlar + durum rozetleri)"))
    B.append(("h2", "Süreç ve kanıt görüntüleri (gerçek oturumlardan eklenecek)"))
    for dosya, ad in [
        ("project-rule.png", "Project — Kalıcı Talimat (Rule) yüklü"),
        ("project-skill.png", "Project — Üretim Standardı (Skill) yüklü"),
        ("turA-deneme1.png", "Tur A — boş sohbet, 1. deneme"),
        ("turA-deneme2.png", "Tur A — boş sohbet, 2. deneme"),
        ("turB-uretim1.png", "Tur B — Project içinde üretim, 1. deneme"),
        ("turB-uretim2.png", "Tur B — kararlılık, 2. deneme"),
        ("dogrulama-canli-once.png", "Canlı veri — değişiklik öncesi"),
        ("dogrulama-canli-sonra.png", "Canlı veri — değişiklik sonrası"),
        ("tetikleyici-log.png", "Bonus — tetikleyici çalıştırma günlüğü"),
        ("tetikleyici-eposta.png", "Bonus — günlük kalite özeti e-postası"),
    ]:
        B.append(("gorsel", dosya, ad))
    return B


# ------------------------------------------------------------------ PDF render
def pdf_kapak(pdf):
    pdf.set_fill_color(*DERIN)
    pdf.rect(18, 18, 174, 30, style="F")
    pdf.set_xy(22, 24)
    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, "VALEO · Kalite & Iskarta Takibi", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(22)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 7, "Yönetişimli Dashboard Üretim Hattı — Proje Raporu (Bölüm 8)")
    pdf.ln(20)
    pdf.set_text_color(*INK)
    pdf.set_font("DejaVu", "", 11)
    meta = [
        ("Ad Soyad", "Alpay Mutlu"),
        ("Departman", "Ar-Ge / Kalite"),
        ("Kullanılan Araç", "Claude (Pro/Max) — Project + Skill (Connector kullanılmadı)"),
        ("Senaryo", "S2 — Kalite & Iskarta Takibi"),
        ("Çalışma Ortamı", "Google Apps Script web app (canlı Google Sheets)"),
        ("Tarih", "18.06.2026"),
    ]
    for ad, deg in meta:
        pdf.set_font("DejaVu", "B", 11)
        pdf.cell(45, 8, ad)
        pdf.set_font("DejaVu", "", 11)
        pdf.multi_cell(0, 8, ": " + deg, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)


def pdf_h1(pdf, t):
    if pdf.get_y() > 250:
        pdf.add_page()
    pdf.ln(3)
    pdf.set_font("DejaVu", "B", 14)
    pdf.set_text_color(*DERIN)
    pdf.multi_cell(0, 9, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*YESIL)
    pdf.set_line_width(0.6)
    y = pdf.get_y()
    pdf.line(18, y, 192, y)
    pdf.ln(3)
    pdf.set_text_color(*INK)


def pdf_p(pdf, t):
    pdf.set_font("DejaVu", "", 10.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.6, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)


def pdf_liste(pdf, ogeler):
    pdf.set_font("DejaVu", "", 10.5)
    pdf.set_text_color(*INK)
    for o in ogeler:
        y0 = pdf.get_y()
        pdf.set_xy(20, y0)
        pdf.set_text_color(*YESIL)
        pdf.cell(5, 5.6, "•")
        pdf.set_text_color(*INK)
        pdf.set_x(25)
        pdf.multi_cell(167, 5.6, o, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(0.8)
    pdf.ln(1)


def pdf_tablo(pdf, basliklar, satirlar):
    pdf.set_font("DejaVu", "", 9.5)
    pdf.set_text_color(*INK)
    with pdf.table(
        first_row_as_headings=True,
        headings_style=FontFace(emphasis="BOLD", fill_color=DERIN, color=(255, 255, 255)),
        cell_fill_color=ACIK, cell_fill_mode="ROWS",
        line_height=5.4, width=174,
    ) as table:
        r = table.row()
        for b in basliklar:
            r.cell(b)
        for satir in satirlar:
            r = table.row()
            for h in satir:
                r.cell(h)
    pdf.ln(3)


def png_boyut(p):
    try:
        with open(p, "rb") as f:
            d = f.read(24)
        if d[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", d[16:24])
    except Exception:
        pass
    return None


def pdf_h2(pdf, t):
    if pdf.get_y() > 248:
        pdf.add_page()
    pdf.ln(2)
    pdf.set_font("DejaVu", "B", 12)
    pdf.set_text_color(*YESIL)
    pdf.multi_cell(0, 7, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(*INK)
    pdf.ln(1)


def pdf_gorsel(pdf, dosya, baslik):
    yol = KOK / "ekran-goruntuleri" / dosya
    if yol.exists():
        en = 174.0
        boyut = png_boyut(yol)
        yuk = en * (boyut[1] / boyut[0]) if boyut else 95.0
        if yuk > 240:                       # çok uzunsa yükseklikten kıs
            yuk = 240.0
            en = yuk * (boyut[0] / boyut[1])
        if pdf.get_y() + yuk + 12 > 285:    # sığmıyorsa sayfa kır
            pdf.add_page()
        pdf.set_font("DejaVu", "B", 9.5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 5.4, "▸ " + baslik, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_draw_color(*GRI)
        pdf.set_line_width(0.2)
        x = 18 + (174 - en) / 2
        pdf.image(str(yol), x=x, w=en)
        pdf.rect(x, pdf.get_y() - yuk, en, yuk)   # ince çerçeve
        pdf.ln(5)
    else:
        if pdf.get_y() + 30 > 285:
            pdf.add_page()
        pdf.set_font("DejaVu", "B", 9.5)
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 5.4, "▸ " + baslik, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        y = pdf.get_y()
        pdf.set_draw_color(*GRI)
        pdf.set_line_width(0.3)
        pdf.set_fill_color(245, 247, 244)
        pdf.rect(18, y, 174, 20, style="DF")
        pdf.set_xy(18, y + 6)
        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(*GRI)
        pdf.multi_cell(174, 5, "[ Ekran görüntüsü eklenecek ]  →  ekran-goruntuleri/" + dosya, align="C")
        pdf.set_y(y + 20)
        pdf.ln(5)
        pdf.set_text_color(*INK)


def kutu(pdf, x, y, w, h, baslik, alt, fill, cizgi, metin=INK, kesik=False):
    pdf.set_fill_color(*fill)
    pdf.set_draw_color(*cizgi)
    pdf.set_line_width(0.5 if not kesik else 0.4)
    pdf.rect(x, y, w, h, style="DF")
    pdf.set_xy(x + 1.5, y + 2)
    pdf.set_font("DejaVu", "B", 8.6)
    pdf.set_text_color(*metin)
    pdf.multi_cell(w - 3, 4, baslik, align="C")
    if alt:
        pdf.set_xy(x + 1.5, y + 2 + 4.4)
        pdf.set_font("DejaVu", "", 7.2)
        pdf.set_text_color(*GRI)
        pdf.multi_cell(w - 3, 3.4, alt, align="C")


def ok_dikey(pdf, x, y1, y2):
    pdf.set_draw_color(*YESIL)
    pdf.set_line_width(0.5)
    pdf.line(x, y1, x, y2)
    pdf.set_fill_color(*YESIL)
    pdf.polygon([(x - 1.4, y2 - 2.4), (x + 1.4, y2 - 2.4), (x, y2)], style="F")


def ok_yatay(pdf, x1, x2, y):
    pdf.set_draw_color(*YESIL)
    pdf.set_line_width(0.5)
    pdf.line(x1, y, x2, y)
    pdf.set_fill_color(*YESIL)
    pdf.polygon([(x2 - 2.4, y - 1.4), (x2 - 2.4, y + 1.4), (x2, y)], style="F")


def pdf_diyagram(pdf):
    if pdf.get_y() > 200:
        pdf.add_page()
    pdf.ln(2)
    y = pdf.get_y()
    # Katman 1
    kutu(pdf, 18, y, 78, 14, "Sentetik Veri", "uret_veri.py · seed sabit", (255, 255, 255), GRI)
    ok_yatay(pdf, 96, 114, y + 7)
    kutu(pdf, 114, y, 78, 14, "Google Sheets — 'veri'", "tek canlı kaynak", (255, 255, 255), YESIL)
    ok_dikey(pdf, 153, y + 14, y + 24)
    # Katman 2: üç girdi
    y2 = y + 24
    kutu(pdf, 18, y2, 56, 16, "Kalıcı Talimat (Rule)", "≥6 denetlenebilir kural", ACIK, YESIL)
    kutu(pdf, 77, y2, 56, 16, "Üretim Standardı (Skill)", "tasarım sistemi + anatomi", ACIK, YESIL)
    kutu(pdf, 136, y2, 56, 16, "Bağlam (Context)", "veriyi gömme, bağlı oku", ACIK, YESIL)
    ok_dikey(pdf, 46, y2 + 16, y2 + 24)
    ok_dikey(pdf, 105, y2 + 16, y2 + 24)
    ok_dikey(pdf, 164, y2 + 16, y2 + 24)
    # Project
    y3 = y2 + 24
    kutu(pdf, 50, y3, 110, 14, "Claude Project (Pro/Max)", "Rule + Skill + Context kalıcı uygulanır",
         DERIN, DERIN, metin=(255, 255, 255))
    # Project -> turlar oku
    ok_dikey(pdf, 105, y3 + 14, y3 + 22)
    # İki tur
    y4 = y3 + 22
    kutu(pdf, 30, y4, 64, 16, "TUR A — Boş Sohbet", "standart YOK → sapma", (253, 236, 235), KIRMIZI,
         metin=KIRMIZI, kesik=True)
    kutu(pdf, 116, y4, 64, 16, "TUR B — Project", "standart VAR → kararlı", ACIK, YESIL, metin=YESIL)
    ok_dikey(pdf, 148, y4 + 16, y4 + 24)
    # Çıktı
    y5 = y4 + 24
    kutu(pdf, 18, y5, 86, 14, "Apps Script Web App", "HtmlService + SpreadsheetApp (canlı)",
         (255, 255, 255), YESIL)
    ok_yatay(pdf, 104, 122, y5 + 7)
    kutu(pdf, 122, y5, 70, 14, "Dashboard — 4 Ekran", "KPI · Trend · Pareto · Tablo", ACIK, YESIL)
    # Bonus
    y6 = y5 + 18
    kutu(pdf, 18, y6, 174, 10, "(Bonus) Zaman Tetikleyici → günlük PPM e-postası + eşik uyarısı",
         "", (255, 255, 255), GRI, kesik=True)
    pdf.set_y(y6 + 14)
    pdf.set_text_color(*INK)


def pdf_uret():
    pdf = yeni_pdf()
    eslesme = {
        "kapak": lambda p, b: pdf_kapak(p),
        "h1": lambda p, b: pdf_h1(p, b[1]),
        "p": lambda p, b: pdf_p(p, b[1]),
        "liste": lambda p, b: pdf_liste(p, b[1]),
        "tablo": lambda p, b: pdf_tablo(p, b[1], b[2]),
        "diyagram": lambda p, b: pdf_diyagram(p),
        "h2": lambda p, b: pdf_h2(p, b[1]),
        "gorsel": lambda p, b: pdf_gorsel(p, b[1], b[2]),
    }
    for blok in icerik():
        eslesme[blok[0]](pdf, blok)
    cikti = KOK / "rapor.pdf"
    pdf.output(str(cikti))
    return cikti


# ------------------------------------------------------------------ MD render
def md_uret():
    satir = ["# VALEO · Kalite & Iskarta Takibi — Proje Raporu (Bölüm 8)",
             "",
             "**Ad Soyad:** Alpay Mutlu · **Departman:** Ar-Ge / Kalite · "
             "**Araç:** Claude (Pro/Max) · **Senaryo:** S2 · **Tarih:** 18.06.2026",
             "",
             "> Bu Markdown, rapor.pdf ile aynı içeriğin GitHub'da okunabilir halidir "
             "(kaynak: rapor/rapor_uret.py).", ""]
    for blok in icerik():
        t = blok[0]
        if t == "kapak":
            continue
        if t == "h1":
            satir += ["", "## " + blok[1], ""]
        elif t == "h2":
            satir += ["", "### " + blok[1], ""]
        elif t == "p":
            satir += [blok[1], ""]
        elif t == "liste":
            satir += ["- " + o for o in blok[1]] + [""]
        elif t == "gorsel":
            dosya, baslik = blok[1], blok[2]
            if (KOK / "ekran-goruntuleri" / dosya).exists():
                satir += ["**" + baslik + "**", "",
                          "![" + baslik + "](../ekran-goruntuleri/" + dosya + ")", ""]
            else:
                satir += ["**" + baslik + "** — _eklenecek: `ekran-goruntuleri/" + dosya + "`_", ""]
        elif t == "tablo":
            basliklar, satirlar = blok[1], blok[2]
            satir += ["| " + " | ".join(basliklar) + " |",
                      "| " + " | ".join(["---"] * len(basliklar)) + " |"]
            satir += ["| " + " | ".join(s) + " |" for s in satirlar] + [""]
        elif t == "diyagram":
            satir += ["![Yönetişim Mimarisi](mimari-diyagram.svg)", ""]
    (KOK / "rapor" / "rapor.md").write_text("\n".join(satir), encoding="utf-8")


if __name__ == "__main__":
    yol = pdf_uret()
    md_uret()
    print("Üretildi:", yol.relative_to(KOK))
    print("Üretildi:", (KOK / "rapor" / "rapor.md").relative_to(KOK))
