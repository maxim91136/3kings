"""Sicherheits-Regeln der Seite: Kopfzeilen, CSP-Hashes, keine Inline-Handler, Escaping.

Läuft ohne Netz. Schlägt an, wenn eine Änderung an site/index.html die
Content-Security-Policy stumm bricht (dann Hash in site/_headers nachtragen).
"""
import base64
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


def kopfzeilen():
    werte = {}
    zeilen = (SITE / "_headers").read_text(encoding="utf-8").splitlines()
    assert zeilen[0] == "/*", "_headers muss mit /* beginnen"
    for z in zeilen[1:]:
        if ":" in z:
            k, v = z.strip().split(":", 1)
            werte[k.strip()] = v.strip()
    return werte


def csp():
    teile = [t.strip() for t in kopfzeilen()["Content-Security-Policy"].split(";") if t.strip()]
    return {t.split(" ", 1)[0]: t.split(" ", 1)[1] if " " in t else "" for t in teile}


class Kopfzeilen(unittest.TestCase):
    PFLICHT = [
        "Content-Security-Policy", "Strict-Transport-Security", "X-Content-Type-Options",
        "X-Frame-Options", "Referrer-Policy", "Permissions-Policy",
        "Cross-Origin-Opener-Policy", "Cross-Origin-Resource-Policy",
        "X-Robots-Tag", "Cache-Control",
    ]

    def test_pflichtfelder_vorhanden(self):
        for k in self.PFLICHT:
            self.assertIn(k, kopfzeilen(), k)

    def test_hsts_ohne_unterdomains_und_preload(self):
        # Gleiche Linie wie bei cyberlage.org: ein Jahr, sonst nichts.
        self.assertEqual(kopfzeilen()["Strict-Transport-Security"], "max-age=31536000")

    def test_csp_strikt(self):
        c = csp()
        self.assertEqual(c["default-src"], "'none'")
        self.assertEqual(c["frame-ancestors"], "'none'")
        self.assertEqual(c["object-src"], "'none'")
        self.assertEqual(c["base-uri"], "'none'")
        self.assertNotIn("'unsafe-inline'", c["script-src"])
        self.assertNotIn("'unsafe-eval'", c["script-src"])

    def test_csp_hashes_passen_zu_index(self):
        html = (SITE / "index.html").read_text(encoding="utf-8")
        erwartet = {
            "'sha256-%s'" % base64.b64encode(hashlib.sha256(b.encode("utf-8")).digest()).decode()
            for b in re.findall(r"<script>(.*?)</script>", html, flags=re.S)
        }
        erlaubt = set(re.findall(r"'sha256-[^']+'", csp()["script-src"]))
        self.assertTrue(erwartet, "keine Inline-Skripte gefunden")
        self.assertEqual(erwartet - erlaubt, set(), "fehlende Hashes in site/_headers")
        self.assertEqual(erlaubt - erwartet, set(), "veraltete Hashes in site/_headers")


class Seite(unittest.TestCase):
    def setUp(self):
        self.html = (SITE / "index.html").read_text(encoding="utf-8")

    def test_keine_inline_handler_im_markup(self):
        self.assertEqual(re.findall(r"\son[a-z]+\s*=\s*[\"']", self.html), [])

    def test_escaping_schuetzt_anfuehrungszeichen(self):
        self.assertIn('.replace(/"/g,"&quot;").replace(/\'/g,"&#39;")', self.html)

    def test_quellenlinks_nur_https(self):
        self.assertIn('href="${e(/^https:\\/\\//.test(s.url)?s.url:"#")}"', self.html)

    def test_kein_eval(self):
        self.assertIsNone(re.search(r"\beval\(|new Function", self.html))


if __name__ == "__main__":
    unittest.main()
