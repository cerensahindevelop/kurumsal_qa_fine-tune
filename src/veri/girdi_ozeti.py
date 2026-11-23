"""Girdi klasörlerinin SHA-256 özetini ve kilit manifestini yazar.

Bu betik dosya İÇERİĞİ basmaz. Yalnızca göreli yol, bayt, satır sayısı ve
SHA-256 özeti yazar. Bu yüzden kilitli setlere (test, tuzak, Türkçe
değerlendirme) dokunabilen az sayıdaki betikten biridir.

Kullanım:
    python -m src.veri.girdi_ozeti \
        --girdi "/home/aipc/Desktop/Gruplu Veriler" /home/aipc/Desktop/fine_tuneVeriler \
        --cikti env/2026-11-23_girdi_sha256.json \
        --kilit-cikti degerlendirme/kilit_manifesti_v1.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import hashlib
import json
from pathlib import Path

# Kilitli sayılan dosyalar (girdi köküne göre göreli, glob deseni).
# Bu desenlere uyan dosyalar 11. aşamaya kadar yalnızca bu tür betiklerle açılır.
VARSAYILAN_KILITLI = [
    "degerlendirme/test.jsonl",
    "degerlendirme/tuzak_sorular.jsonl",
    "degerlendirme/Türkçe Değerlendirme/*",
    "05_tuzak_sorular/*",
    "06_genel_turkce/degerlendirme/*",
]

SATIR_SAYILAN = {".jsonl", ".csv", ".txt", ".md", ".py"}


def sha256_hesapla(yol: Path, parca: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with yol.open("rb") as f:
        while blok := f.read(parca):
            h.update(blok)
    return h.hexdigest()


def satir_say(yol: Path) -> int:
    with yol.open("rb") as f:
        return sum(1 for _ in f)


def kok_tara(kok: Path, kilitli_desenler: list[str]) -> list[dict]:
    kayitlar = []
    for yol in sorted(p for p in kok.rglob("*") if p.is_file()):
        goreli = yol.relative_to(kok).as_posix()
        kayitlar.append(
            {
                "kok": str(kok),
                "yol": goreli,
                "bayt": yol.stat().st_size,
                "satir": satir_say(yol) if yol.suffix.lower() in SATIR_SAYILAN else None,
                "sha256": sha256_hesapla(yol),
                "kilitli": any(fnmatch.fnmatch(goreli, d) for d in kilitli_desenler),
            }
        )
    return kayitlar


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--girdi", nargs="+", required=True, type=Path, help="Taranacak kök klasörler")
    ap.add_argument("--cikti", required=True, type=Path, help="Tüm dosyaların özeti (JSON)")
    ap.add_argument("--kilit-cikti", type=Path, help="Yalnızca kilitli dosyaların manifesti (JSON)")
    ap.add_argument("--kilitli", nargs="*", default=VARSAYILAN_KILITLI, help="Kilitli glob desenleri")
    a = ap.parse_args()

    zaman = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    tum = []
    for kok in a.girdi:
        if not kok.is_dir():
            raise SystemExit(f"Girdi klasörü yok: {kok}")
        tum.extend(kok_tara(kok, a.kilitli))

    a.cikti.parent.mkdir(parents=True, exist_ok=True)
    a.cikti.write_text(
        json.dumps({"olusturma": zaman, "dosyalar": tum}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    kilitli = [k for k in tum if k["kilitli"]]
    if a.kilit_cikti:
        a.kilit_cikti.parent.mkdir(parents=True, exist_ok=True)
        a.kilit_cikti.write_text(
            json.dumps(
                {"olusturma": zaman, "desenler": a.kilitli, "dosyalar": kilitli},
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )
    # Ekrana yalnızca toplu sayılar yazılır.
    print(f"dosya={len(tum)} kilitli={len(kilitli)} cikti={a.cikti}")


if __name__ == "__main__":
    main()
