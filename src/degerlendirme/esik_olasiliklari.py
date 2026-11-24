"""Eşik gerekçelerindeki olasılıkları yeniden hesaplar (veri okumaz).

Kullanım:
    python -m src.degerlendirme.esik_olasiliklari --cikti degerlendirme/esik_olasiliklari_v1.json

Hesaplananlar:
1. Çok sayıda zorunlu eşikte en az birinin şans eseri aşılma olasılığı (bağımsızlık varsayımı).
2. 4.1 tuzak eşiği (28 soru): iki model eşitken yanlış alarm ve gerçek kötüleşmeyi yakalama
   olasılığı, iki modelle: bağımsız binom ve eşleştirilmiş (soru bazında ayrışma).
3. Yargıç kalibrasyonu: %75 uyumun %95 belirsizlik yarı genişliği, 5 pp'nin çift karşılığı,
   kappa için yaklaşık belirsizlik.
4. Holm ailesi seçeneklerinde 5.1 için gereken en büyük ham p sınırı.
Bütün sonuçlar tam (kesin) olasılık hesabıdır; benzetim yoktur, bu yüzden seed gerekmez.
"""
from __future__ import annotations

import argparse
import json
from math import comb, sqrt
from pathlib import Path

N_TUZAK = 28
Z95 = 1.959964


# ---------- 1. Aile düzeyinde yanlış alarm ----------
def en_az_biri(k: int, alfa: float = 0.05) -> float:
    return 1 - (1 - alfa) ** k


# ---------- 2. 4.1 tuzak eşiği ----------
def binom_dagilim(n: int, p: float) -> list[float]:
    return [comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(n + 1)]


def fark_dagilimi_bagimsiz(n: int, p_adaptor: float, p_istemli: float) -> dict[int, float]:
    """Adaptör − istemli farkının dağılımı; iki model birbirinden bağımsız."""
    a, b = binom_dagilim(n, p_adaptor), binom_dagilim(n, p_istemli)
    d: dict[int, float] = {}
    for i, pa in enumerate(a):
        for j, pb in enumerate(b):
            d[i - j] = d.get(i - j, 0.0) + pa * pb
    return d


def fark_dagilimi_eslesik(n: int, q_yalniz_istemli: float, q_yalniz_adaptor: float) -> dict[int, float]:
    """Soru bazında: yalnız istemli başarılı (−1), yalnız adaptör başarılı (+1), aynı sonuç (0)."""
    q0 = 1 - q_yalniz_istemli - q_yalniz_adaptor
    d = {0: 1.0}
    for _ in range(n):
        yeni: dict[int, float] = {}
        for k, p in d.items():
            for adim, q in ((-1, q_yalniz_istemli), (1, q_yalniz_adaptor), (0, q0)):
                yeni[k + adim] = yeni.get(k + adim, 0.0) + p * q
        d = yeni
    return d


def kalma_olasiligi(d: dict[int, float], tolerans: int) -> float:
    """Eşik 'adaptör ≥ istemli − tolerans'; kalma = fark ≤ −(tolerans+1)."""
    return sum(p for k, p in d.items() if k <= -(tolerans + 1))


def tuzak_hesabi(kotulesme: int) -> dict:
    sonuc: dict = {"bagimsiz": [], "eslesik": []}
    for p in (0.70, 0.75, 0.80, 0.85, 0.90):
        esit = fark_dagilimi_bagimsiz(N_TUZAK, p, p)
        kotu = fark_dagilimi_bagimsiz(N_TUZAK, p - kotulesme / N_TUZAK, p)
        sonuc["bagimsiz"].append({
            "basari_orani": p,
            **{f"yanlis_alarm_tol{t}": kalma_olasiligi(esit, t) for t in (1, 2, 3)},
            **{f"yakalama_tol{t}": kalma_olasiligi(kotu, t) for t in (1, 2, 3)},
        })
    for ayrisma in (0.10, 0.15, 0.20, 0.25, 0.30):
        h = ayrisma / 2
        delta = kotulesme / N_TUZAK
        esit = fark_dagilimi_eslesik(N_TUZAK, h, h)
        kotu = fark_dagilimi_eslesik(N_TUZAK, h + delta, h)
        sonuc["eslesik"].append({
            "ayrisma_orani": ayrisma,
            **{f"yanlis_alarm_tol{t}": kalma_olasiligi(esit, t) for t in (1, 2, 3)},
            **{f"yakalama_tol{t}": kalma_olasiligi(kotu, t) for t in (1, 2, 3)},
        })
    # Üçüncü model: adaptör tam `kotulesme` soruda kesin kaybeder, kalan sorularda eşleştirilmiş gürültü.
    sonuc["kesin"] = []
    for ayrisma in (0.10, 0.15, 0.20, 0.25, 0.30):
        h = ayrisma / 2
        gurultu = fark_dagilimi_eslesik(N_TUZAK - kotulesme, h, h)
        kotu = {k - kotulesme: p for k, p in gurultu.items()}
        sonuc["kesin"].append({
            "ayrisma_orani": ayrisma,
            **{f"yakalama_tol{t}": kalma_olasiligi(kotu, t) for t in (1, 2, 3)},
        })
    return sonuc


# ---------- 3. Kalibrasyon ----------
def kalibrasyon(n: int, uyum: float = 0.75, kappa_sans: float = 0.5) -> dict:
    yari = Z95 * sqrt(uyum * (1 - uyum) / n)
    # Wilson aralığı
    merkez = (uyum + Z95**2 / (2 * n)) / (1 + Z95**2 / n)
    w = Z95 * sqrt(uyum * (1 - uyum) / n + Z95**2 / (4 * n * n)) / (1 + Z95**2 / n)
    # Kappa için kaba yaklaşık standart hata: sqrt(po(1-po)/n) / (1-pe)
    kappa_yari = Z95 * sqrt(uyum * (1 - uyum) / n) / (1 - kappa_sans)
    return {
        "cift": n,
        "uyum_yari_genislik_pp": 100 * yari,
        "wilson_alt_pp": 100 * (merkez - w),
        "wilson_ust_pp": 100 * (merkez + w),
        "bes_pp_kac_cift": 0.05 * n,
        "bir_cift_kac_pp": 100 / n,
        "kappa_yari_genislik": kappa_yari,
    }


# ---------- 4. Holm ----------
def holm_sinirlari(m: int, alfa: float = 0.05) -> list[float]:
    return [alfa / (m - i) for i in range(m)]


def isaret_p(k: int, n: int) -> float:
    """İki yönlü kesin işaret testi."""
    k = max(k, n - k)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k, n + 1)) / 2**n)


def gereken_galibiyet(n: int, alfa: float) -> int:
    return next(k for k in range(n // 2, n + 1) if isaret_p(k, n) < alfa)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cikti", type=Path, required=True, help="JSON çıktı yolu")
    ap.add_argument("--kotulesme", type=int, default=3, help="4.1 için gerçek kötüleşme (soru)")
    args = ap.parse_args()

    sonuc = {
        "aile_yanlis_alarm_alfa_0_05": {
            "17_koruma_esigi": en_az_biri(17),
            "21_koruma_esigi_s2_iki_taban": en_az_biri(21),
            "4_kritik_2.1x2_3.7_4.2": en_az_biri(4),
            "3_kritik_2.1x1_3.7_4.2": en_az_biri(3),
        },
        "tuzak_4_1": tuzak_hesabi(args.kotulesme),
        "kalibrasyon": [kalibrasyon(n) for n in (20, 25, 30, 32, 40)],
        "holm_sinirlari": {f"m={m}": holm_sinirlari(m) for m in (1, 2, 3, 4, 6)},
        "isaret_testi_gereken_galibiyet": {
            f"alfa={alfa:.4f}": {f"n={n}": gereken_galibiyet(n, alfa) for n in (60, 80, 100)}
            for alfa in (0.05, 0.025, 0.05 / 3, 0.0125, 0.05 / 6)
        },
    }
    args.cikti.parent.mkdir(parents=True, exist_ok=True)
    args.cikti.write_text(json.dumps(sonuc, ensure_ascii=False, indent=2), encoding="utf-8")

    a = sonuc["aile_yanlis_alarm_alfa_0_05"]
    print("Aile yanlış alarm:", {k: round(v, 3) for k, v in a.items()})
    for tur in ("bagimsiz", "eslesik"):
        print(f"4.1 {tur}:")
        for r in sonuc["tuzak_4_1"][tur]:
            anahtar = "basari_orani" if tur == "bagimsiz" else "ayrisma_orani"
            print(f"  {anahtar}={r[anahtar]:.2f}  "
                  + "  ".join(f"YA-{t}={r[f'yanlis_alarm_tol{t}']:.3f}" for t in (1, 2, 3)) + "  |  "
                  + "  ".join(f"YK-{t}={r[f'yakalama_tol{t}']:.3f}" for t in (1, 2, 3)))
    print("4.1 kesin (tam N soruda kötüleşme + gürültü):")
    for r in sonuc["tuzak_4_1"]["kesin"]:
        print(f"  ayrisma_orani={r['ayrisma_orani']:.2f}  "
              + "  ".join(f"YK-{t}={r[f'yakalama_tol{t}']:.3f}" for t in (1, 2, 3)))
    for r in sonuc["kalibrasyon"]:
        print(f"Kalibrasyon n={r['cift']}: ±{r['uyum_yari_genislik_pp']:.1f} pp "
              f"(Wilson {r['wilson_alt_pp']:.1f}–{r['wilson_ust_pp']:.1f}), 5 pp = {r['bes_pp_kac_cift']:.2f} çift, "
              f"kappa ±{r['kappa_yari_genislik']:.2f}")
    print("Holm:", {k: [round(x, 4) for x in v] for k, v in sonuc["holm_sinirlari"].items()})
    print("İşaret testi, gereken galibiyet:", sonuc["isaret_testi_gereken_galibiyet"])


if __name__ == "__main__":
    main()
