"""Gemeinsamer Abruf: öffnet nur https-Adressen (kein file:, ftp: oder eigenes Schema)."""
import urllib.request
from urllib.parse import urlsplit


def oeffne(ziel, daten=None, timeout=30):
    adresse = ziel.full_url if isinstance(ziel, urllib.request.Request) else ziel
    if urlsplit(adresse).scheme != "https":
        raise ValueError("nur https erlaubt: %s" % adresse.split("?")[0])
    return urllib.request.urlopen(ziel, daten, timeout=timeout)  # nosec B310 - Schema oben auf https geprüft
