"""JSONL dosyalarında bir ifadenin kaç kayıtta geçtiğini sayar; içerik basmaz.

Kullanım:
  python -m src.veri.ifade_say --girdi <dosya.jsonl> [<dosya2.jsonl> ...] \
      --ifade "anlaşılır bir dille anlatır mısın" [--ifade "..."]

- Kilitli setlerde de kullanılabilir: çıktı yalnızca dosya adı, kayıt sayısı ve eşleşme sayısıdır.
  Kayıt metni, kimlik veya eşleşen bölüm yazılmaz.
- Arama, kaydın bütün metin alanlarında yapılır; büyük/küçük harf ve Türkçe İ/ı farkı yok sayılır.
"""
import argparse
import json
from pathlib import Path


def kucuk(metin: str) -> str:
    """Türkçeye uygun küçük harf: 'İ' -> 'i', 'I' -> 'ı'."""
    return metin.replace("İ", "i").replace("I", "ı").lower()


def metinler(deger) -> list[str]:
    """Bir JSON değerindeki bütün dizgeleri toplar (iç içe liste ve sözlükler dahil)."""
    if isinstance(deger, str):
        return [deger]
    if isinstance(deger, dict):
        return [m for v in deger.values() for m in metinler(v)]
    if isinstance(deger, list):
        return [m for v in deger for m in metinler(v)]
    return []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--girdi", type=Path, nargs="+", required=True)
    ap.add_argument("--ifade", action="append", required=True)
    a = ap.parse_args()

    ifadeler = [kucuk(i) for i in a.ifade]
    for yol in a.girdi:
        kayitlar = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()]
        birlesik = [kucuk(" ".join(metinler(k))) for k in kayitlar]
        sayilar = {ham: sum(ara in m for m in birlesik) for ham, ara in zip(a.ifade, ifadeler)}
        print(f"{yol.name}: kayıt={len(kayitlar)} " + " ".join(f"[{i!r}]={n}" for i, n in sayilar.items()))


if __name__ == "__main__":
    main()
