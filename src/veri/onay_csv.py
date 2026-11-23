"""Bir JSONL taslağından insan onay kuyruğu (CSV) üretir.

Kullanım:
  python -m src.veri.onay_csv --girdi inceleme/genel_kontrol_v2_taslak.jsonl \
      --cikti inceleme/genel_kontrol_v2_onay.csv

- Yalnızca asistanın yazdığı, kilitli olmayan taslaklar için kullanılır (test/tuzak için değil).
- Çıktı zaten varsa, doldurulmuş onay/not hücreleri kimliğe göre korunur.
- `bilgi_ogeleri` alanı olan kayıtlarda öğeler " | " ile birleştirilir ve ayrı bir bilgi onayı sütunu açılır.
- Sonunda onay dağılımını yazar. "düzelt"/"duzelt", "hayır"/"hayir" ve büyük/küçük harf aynı sayılır;
  hücredeki yazım değiştirilmez. evet/hayir/duzelt dışındaki değerler kimlikleriyle listelenir.
"""
import argparse
import csv
import json
from pathlib import Path

ONAY = "onay (evet/hayir/duzelt)"
BILGI_ONAY = "bilgi_ogeleri_dogru_mu (evet/hayir/duzelt)"
DOLDURULAN = [ONAY, BILGI_ONAY, "not"]
GECERLI = {"evet", "hayir", "duzelt"}
_TR = str.maketrans({"ı": "i", "İ": "i", "ü": "u", "Ü": "u", "ö": "o", "Ö": "o",
                     "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g", "ç": "c", "Ç": "c"})


def normal_onay(deger: str) -> str:
    """Onay hücresini karşılaştırma için sadeleştirir: "Düzelt", "düzelt", "duzelt" -> "duzelt"."""
    return deger.strip().translate(_TR).lower()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--girdi", type=Path, required=True)
    ap.add_argument("--cikti", type=Path, required=True)
    a = ap.parse_args()

    kayitlar = [json.loads(s) for s in a.girdi.read_text(encoding="utf-8").splitlines() if s.strip()]

    eski: dict[str, dict] = {}
    if a.cikti.exists():
        with a.cikti.open(encoding="utf-8-sig", newline="") as f:
            eski = {r["id"]: r for r in csv.DictReader(f)}

    alanlar = ["id", "grup", "kategori", "prompt", "bilgi_ogeleri"] + DOLDURULAN
    with a.cikti.open("w", encoding="utf-8-sig", newline="") as f:  # utf-8-sig: Excel Türkçe karakteri doğru açar
        w = csv.DictWriter(f, fieldnames=alanlar)
        w.writeheader()
        for k in kayitlar:
            satir = {
                "id": k["id"], "grup": k["grup"], "kategori": k["kategori"], "prompt": k["prompt"],
                "bilgi_ogeleri": " | ".join(k.get("bilgi_ogeleri", [])),
            }
            onceki = eski.get(k["id"], {})
            for s in DOLDURULAN:
                satir[s] = onceki.get(s, "")
            if "bilgi_ogeleri" not in k:
                satir[BILGI_ONAY] = "-"  # bu kayıtta bilgi öğesi yok
            w.writerow(satir)

    # "-" betiğin kendi yer tutucusudur; insan doldurması sayılmaz.
    korunan = sum(1 for k in kayitlar
                  if any(eski.get(k["id"], {}).get(s, "").strip() not in ("", "-") for s in DOLDURULAN))
    print(f"{len(kayitlar)} satır yazıldı -> {a.cikti} (korunan dolu satır: {korunan})")

    # Onay dağılımı: yazım farkları (ü/u, ı/i, büyük/küçük harf) aynı değer sayılır.
    for s in (ONAY, BILGI_ONAY):
        sayim: dict[str, int] = {}
        tanimsiz = []
        for k in kayitlar:
            d = normal_onay(eski.get(k["id"], {}).get(s, ""))
            if s == BILGI_ONAY and "bilgi_ogeleri" not in k:
                continue  # yer tutuculu satır
            d = d or "(boş)"
            sayim[d] = sayim.get(d, 0) + 1
            if d not in GECERLI and d != "(boş)":
                tanimsiz.append(k["id"])
        print(f"{s}: {dict(sorted(sayim.items()))}" + (f" | tanımsız değer: {tanimsiz}" if tanimsiz else ""))


if __name__ == "__main__":
    main()
