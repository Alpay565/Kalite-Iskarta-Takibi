#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kaynak/ (tek kaynak) -> apps-script/stil.html + apps-script/script.html üretir.

Amac: tasarim sistemi (CSS) ve istemci mantigi (JS) TEK yerde tutulur; Apps Script
editorune yapistirilacak HtmlService parcalari buradan deterministik uretilir.
Boylece kopya tutmaz, DRY kalir.

Calistir:  python3 dashboard/derle_appsscript.py
"""

from pathlib import Path

KOK = Path(__file__).resolve().parent
KAYNAK = KOK / "kaynak"
HEDEF = KOK / "apps-script"

# JS birlestirme sirasi onemli (veri katmani -> grafikler -> uygulama).
JS_DOSYALAR = ["veri-katmani.js", "grafikler.js", "uygulama.js"]

UYARI = ("<!-- OTOMATIK URETILDI: dashboard/derle_appsscript.py "
         "— bu dosyayi ELLE DUZENLEMEYIN; kaynak/ icindeki dosyalari duzenleyip "
         "betigi yeniden calistirin. -->\n")


def oku(ad):
    return (KAYNAK / ad).read_text(encoding="utf-8").rstrip() + "\n"


def main():
    HEDEF.mkdir(parents=True, exist_ok=True)

    css = oku("tasarim-sistemi.css")
    (HEDEF / "stil.html").write_text(
        UYARI + "<style>\n" + css + "</style>\n", encoding="utf-8"
    )

    js = "\n".join(oku(d) for d in JS_DOSYALAR)
    # Guvenlik: </script> dizisi JS icine kacarsa parcalanmayi onle.
    js = js.replace("</script>", "<\\/script>")
    (HEDEF / "script.html").write_text(
        UYARI + "<script>\n" + js + "</script>\n", encoding="utf-8"
    )

    print("Uretildi:")
    print("  -", (HEDEF / "stil.html").relative_to(KOK.parent))
    print("  -", (HEDEF / "script.html").relative_to(KOK.parent))


if __name__ == "__main__":
    main()
