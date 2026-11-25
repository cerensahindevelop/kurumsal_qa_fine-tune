"""
Ne yapar:
    Değerlendirme eşiklerinin gerekçesi olan olasılıkları hesaplar ve bir dosyaya yazar.
    Eşik, bir modelin "geçti" sayılması için ulaşması gereken sınırdır.
    Bu betik hiçbir veri dosyası okumaz; yalnızca hesap yapar.

Neden var:
    Eşik belgesinde (evaluation/thresholds_v1.md) "tolerans 2 soru" gibi kararlar var.
    Bu kararların neden böyle seçildiği sayılarla gösterilmeli.
    Sayılar elle hesaplanırsa hata yapılabilir; bu betik onları her seferinde aynı biçimde üretir.

Nasıl çalıştırılır (terminalde, proje klasöründeyken):
    python -m src.evaluation.threshold_probabilities --output evaluation/threshold_probabilities_v2.json

    --output: sonuçların yazılacağı dosya.
    --degradation: tuzak hesabında modelin kaç soru daha kötü varsayılacağı. Varsayılan 3.

Hesaplanan dört konu:
    1. Çok sayıda kontrol yapıldığında, iyi bir modelin bile şans eseri en az birinden kalma olasılığı.
    2. Tuzak soruları eşiği (4.1): 28 soruda, iki model aslında eşitken "kaldı" deme olasılığı
       ve model gerçekten kötüleşmişken bunu yakalama olasılığı.
    3. Yargıç modelin insanla ne kadar uyumlu olduğunu ölçerken sonucun ne kadar kesin olduğu.
    4. İşaret testi tablosu: kaç karşılaştırmanın kaçını kazanmak gerektiği.

Rastgelelik yok:
    Bütün sonuçlar kesin formüllerle hesaplanır; deneme yanılma (benzetim) yoktur.
    Bu yüzden her çalıştırmada aynı sayılar çıkar ve seed (rastgeleliği sabitleyen sayı) gerekmez.

Eski sürüm:
    İlk sürümün çıktısı archive/degerlendirme/threshold_probabilities_v1.json dosyasındadır.
    O dosyada anahtar adları Türkçedir. Her eski adın yeni karşılığı LEGACY_OUTPUT_KEYS listesindedir.
    Sayılar iki sürümde de aynı formüllerle hesaplanır.
"""
from __future__ import annotations

import argparse
import json
from math import comb, sqrt
from pathlib import Path

# Tuzak setindeki soru sayısı. Dosyadan sayılarak doğrulandı: 28.
TRAP_QUESTION_COUNT = 28

# İstatistikte %95 güven aralığı için kullanılan sabit sayı.
# Bir ölçümün "gerçek değeri büyük olasılıkla bu aralıkta" dediğimiz sınırı belirler.
Z_SCORE_95 = 1.959964

# Hesaplarda denenen sabit değerler. Eski ve yeni anahtar eşlemesi de bu listelerden kurulur.
TOLERANCES = (1, 2, 3)                                   # Tuzak eşiğinde denenen tolerans (soru sayısı)
SUCCESS_RATES = (0.70, 0.75, 0.80, 0.85, 0.90)           # Modelin tuzak sorularındaki varsayılan başarı oranı
DISAGREEMENT_RATES = (0.10, 0.15, 0.20, 0.25, 0.30)      # İki modelin farklı sonuç verdiği soruların oranı
CALIBRATION_PAIR_COUNTS = (20, 25, 30, 32, 40)           # Yargıç ayarı için denenen cevap çifti sayıları
HOLM_TEST_COUNTS = (1, 2, 3, 4, 6)                       # Tarihî Holm hesabında denenen test sayıları
SIGN_TEST_DECISION_COUNTS = (60, 80, 100)                # İşaret testinde örnek karar sayıları
SIGN_TEST_ALPHAS = (0.05, 0.025, 0.05 / 3, 0.0125, 0.05 / 6)
# Tablo sütunları: 0,05 eşik 1.1 ve 5.1 için kullanılır.
# 0,025 ve 0,0167 eski Holm hesabından kalır; eski sürümle karşılaştırılabilsin diye duruyor.
TABLE_ALPHAS = (("0.05", 0.05), ("0.025", 0.025), ("0.0167", 0.05 / 3))

# İlk sürümdeki (v1) Türkçe anahtar adlarının yeni karşılıkları.
# İç içe anahtarlar dahil her biri açıkça yazılır; böylece eski dosya tam olarak çevrilebilir.
LEGACY_OUTPUT_KEYS = {
    "aile_yanlis_alarm_alfa_0_05": "family_wise_false_alarm_alpha_0_05",
    "17_koruma_esigi": "17_guard_thresholds",
    "21_koruma_esigi_s2_iki_taban": "21_guard_thresholds_s2_two_baselines",
    "4_kritik_2.1x2_3.7_4.2": "4_critical_2.1x2_3.7_4.2",
    "3_kritik_2.1x1_3.7_4.2": "3_critical_2.1x1_3.7_4.2",
    "tuzak_4_1": "trap_4_1",
    "bagimsiz": "independent",
    "eslesik": "paired",
    "kesin": "exact_degradation",
    "basari_orani": "success_rate",
    "ayrisma_orani": "disagreement_rate",
    **{f"yanlis_alarm_tol{t}": f"false_alarm_tolerance_{t}" for t in TOLERANCES},
    **{f"yakalama_tol{t}": f"detection_tolerance_{t}" for t in TOLERANCES},
    "kalibrasyon": "calibration",
    "cift": "pairs",
    "uyum_yari_genislik_pp": "agreement_half_width_percentage_points",
    "wilson_alt_pp": "wilson_lower_percentage_points",
    "wilson_ust_pp": "wilson_upper_percentage_points",
    "bes_pp_kac_cift": "pairs_per_5_percentage_points",
    "bir_cift_kac_pp": "percentage_points_per_pair",
    "kappa_yari_genislik": "kappa_half_width",
    "holm_sinirlari": "holm_thresholds",
    **{f"m={m}": f"test_count={m}" for m in HOLM_TEST_COUNTS},
    "isaret_testi_gereken_galibiyet": "sign_test_minimum_wins",
    **{f"alfa={alpha:.4f}": f"alpha={alpha:.4f}" for alpha in SIGN_TEST_ALPHAS},
    **{f"n={n}": f"decision_count={n}" for n in SIGN_TEST_DECISION_COUNTS},
    "isaret_testi_galibiyet_tablosu_n_1_100": "sign_test_minimum_wins_table_1_to_100",
    "n": "decision_count",
    **{f"alfa_{label}": f"alpha_{label}" for label, _ in TABLE_ALPHAS},
    **{f"alfa_{label}_p": f"alpha_{label}_p_value" for label, _ in TABLE_ALPHAS},
}


# ---------- 1. Çok sayıda kontrolde şans eseri kalma ----------
def family_wise_error_rate(check_count: int, alpha: float = 0.05) -> float:
    """
    Ne yapar:
        Birbirinden bağımsız birçok kontrol yapıldığında, iyi bir modelin bile
        şans eseri en az bir kontrolden kalma olasılığını hesaplar.

    Neden var:
        Tek bir kontrolde şans eseri yanlış alarm olasılığı küçüktür, örneğin yüzde 5.
        Ama 17 kontrol yapılınca bu küçük olasılıklar birikir ve neredeyse yüzde 60 olur.
        Bu sayı, yalnızca birkaç kontrolü "kritik" (kalınca model düşer) saymamızın gerekçesidir.

    Ne alır:
        check_count: Kontrol sayısı. Örnek: 3
        alpha: Tek bir kontrolün şans eseri yanlış alarm verme olasılığı. Varsayılan: 0.05 (yüzde 5).

    Ne döndürür:
        En az bir yanlış alarm olasılığı. Örnek: 3 kontrol için 0.1426 (yüzde 14,3).

    Nasıl çalışır:
        Önce hiçbir kontrolün yanlış alarm vermeme olasılığı bulunur: (1 − 0,05) üssü kontrol sayısı.
        Bu sayı 1'den çıkarılınca "en az biri yanlış alarm verir" olasılığı elde edilir.
    """
    return 1 - (1 - alpha) ** check_count


# ---------- 2. Tuzak soruları eşiği (4.1) ----------
def binomial_probabilities(trial_count: int, success_probability: float) -> list[float]:
    """
    Ne yapar:
        Belli sayıda soruda, tam 0, tam 1, tam 2 ... doğru cevap verilme olasılıklarını hesaplar.
        Buna istatistikte binom dağılımı denir.

    Neden var:
        Bir modelin tuzak sorularında kaç doğru yapacağı şansa da bağlıdır.
        Aşağıdaki karşılaştırma hesapları bu olasılıklar üzerine kurulur.

    Ne alır:
        trial_count: Soru sayısı. Örnek: 28
        success_probability: Bir soruyu doğru cevaplama olasılığı. Örnek: 0.80 (yüzde 80)

    Ne döndürür:
        Her doğru sayısı için bir olasılık; listenin sırası doğru sayısıdır.
        Örnek (3 soru, yüzde 50): [0.125, 0.375, 0.375, 0.125]
        Yani hiç doğru olmaması yüzde 12,5; tam bir doğru yüzde 37,5 olasılıklıdır.
    """
    return [
        comb(trial_count, i) * success_probability**i * (1 - success_probability) ** (trial_count - i)
        for i in range(trial_count + 1)
    ]


def difference_distribution_independent(question_count: int, adapter_success: float,
                                        baseline_success: float) -> dict[int, float]:
    """
    Ne yapar:
        Adaptörün doğru sayısı ile hazır modelin (baseline) doğru sayısı arasındaki farkın
        her değer için olasılığını hesaplar. İki modelin birbirinden tamamen bağımsız davrandığını varsayar.
        Adaptör, ince ayarla eğittiğimiz modeldir; baseline ise karşılaştırdığımız hazır modeldir.

    Neden var:
        "Adaptör baseline'dan 2 soru fazla kaçırırsa kalsın" gibi bir kuralın ne kadar sık
        yanlış alarm vereceğini görmek için farkın olasılıkları gerekir.
        Bağımsızlık varsayımı kötümserdir: gerçekte iki model çoğu soruda benzer davranır.
        Bu yüzden bu hesap, yanlış alarmın en kötü durumunu gösterir.

    Ne alır:
        question_count: Soru sayısı. Örnek: 28
        adapter_success: Adaptörün bir soruyu doğru cevaplama olasılığı. Örnek: 0.80
        baseline_success: Baseline'ın bir soruyu doğru cevaplama olasılığı. Örnek: 0.80

    Ne döndürür:
        Her fark değeri için olasılık. Fark = adaptörün doğru sayısı − baseline'ın doğru sayısı.
        Örnek (28 soru, ikisi de yüzde 80): {-1: 0.13, 0: 0.13, 1: 0.13, ...}

    Nasıl çalışır:
        İki modelin bütün olası doğru sayısı ikilileri tek tek denenir.
        Her ikilinin olasılığı, farkına göre aynı kutuya eklenir.
    """
    adapter_distribution = binomial_probabilities(question_count, adapter_success)
    baseline_distribution = binomial_probabilities(question_count, baseline_success)
    distribution: dict[int, float] = {}
    for adapter_correct, adapter_probability in enumerate(adapter_distribution):
        for baseline_correct, baseline_probability in enumerate(baseline_distribution):
            difference = adapter_correct - baseline_correct
            distribution[difference] = distribution.get(difference, 0.0) + adapter_probability * baseline_probability
    return distribution


def difference_distribution_paired(question_count: int, baseline_only_rate: float,
                                   adapter_only_rate: float) -> dict[int, float]:
    """
    Ne yapar:
        Aynı farkın olasılıklarını, soru soru karşılaştırarak hesaplar.
        Her soruda üç durum vardır:
        yalnız baseline doğru bildi (fark 1 azalır),
        yalnız adaptör doğru bildi (fark 1 artar),
        ikisi aynı sonucu verdi (fark değişmez).

    Neden var:
        Gerçekte iki model soruların çoğunda aynı sonucu verir.
        Bu hesap, bağımsız hesaptan daha gerçekçidir ve yanlış alarmın daha olası değerini gösterir.

    Ne alır:
        question_count: Soru sayısı. Örnek: 28
        baseline_only_rate: Bir soruda yalnız baseline'ın doğru bilme olasılığı. Örnek: 0.10
        adapter_only_rate: Bir soruda yalnız adaptörün doğru bilme olasılığı. Örnek: 0.10

    Ne döndürür:
        Her fark değeri için olasılık. Örnek (28 soru, ikisi de 0.10): {-1: 0.16, 0: 0.17, 1: 0.16, ...}

    Nasıl çalışır:
        Sıfır farkla başlanır. Her soru eklendiğinde, o ana kadarki her fark değeri
        üç olası sonuca göre bölünür ve olasılıklar yeni fark değerlerine dağıtılır.
        Bütün sorular eklenince son dağılım elde edilir.
    """
    same_result_rate = 1 - baseline_only_rate - adapter_only_rate
    distribution = {0: 1.0}
    # Her tur bir soruyu temsil eder.
    for _ in range(question_count):
        next_distribution: dict[int, float] = {}
        for difference, probability in distribution.items():
            for step, step_probability in ((-1, baseline_only_rate), (1, adapter_only_rate), (0, same_result_rate)):
                next_distribution[difference + step] = (
                    next_distribution.get(difference + step, 0.0) + probability * step_probability
                )
        distribution = next_distribution
    return distribution


def failure_probability(distribution: dict[int, float], tolerance: int) -> float:
    """
    Ne yapar:
        Bir fark dağılımında, adaptörün eşikten kalma olasılığını toplar.

    Neden var:
        Kural şudur: adaptör, baseline'dan en fazla "tolerans" kadar soru daha az doğru yapabilir.
        Farklı tolerans değerlerinin ne kadar sık "kaldı" dediğini görmek için bu fonksiyon gerekir.

    Ne alır:
        distribution: Fark değerleri ve olasılıkları. Örnek: {-3: 0.05, -2: 0.10, -1: 0.20, 0: 0.30, ...}
        tolerance: Kabul edilen en fazla geride kalma. Örnek: 2

    Ne döndürür:
        Kalma olasılığı. Örnek: tolerans 2 iken fark −3 veya daha kötü olmalı; yukarıdaki örnekte en az 0.05.
    """
    return sum(probability for difference, probability in distribution.items() if difference <= -(tolerance + 1))


def trap_threshold_analysis(degradation: int) -> dict:
    """
    Ne yapar:
        Tuzak soruları eşiği (4.1) için üç farklı varsayımla iki olasılık tablosu çıkarır:
        yanlış alarm (iki model eşitken "kaldı" demek) ve yakalama (model gerçekten kötüleşmişken "kaldı" demek).

    Neden var:
        Eşik belgesindeki "tolerans 2 soru" kararının sayısal gerekçesi bu tablolardır.
        Tolerans çok küçükse iyi modeller şans eseri kalır; çok büyükse gerçek kötüleşme gözden kaçar.

    Ne alır:
        degradation: Adaptörün baseline'dan kaç soru daha kötü olduğu varsayımı. Örnek: 3

    Ne döndürür:
        Üç tablo: "independent" (bağımsız varsayım), "paired" (soru soru eşleştirilmiş varsayım)
        ve "exact_degradation" (adaptör tam o kadar soruyu kesin kaybeder varsayımı).
        Örnek satır (kötüleşme 3 soru): {"success_rate": 0.8, "false_alarm_tolerance_2": 0.20, "detection_tolerance_2": 0.56, ...}
    """
    result: dict = {"independent": [], "paired": []}

    # Birinci varsayım, bağımsız modeller: her başarı oranı için önce iki model eşitken,
    # sonra adaptör gerçekten kötüleşmişken eşiğin ne sıklıkla "kaldı" dediği hesaplanır.
    for success_rate in SUCCESS_RATES:
        equal = difference_distribution_independent(TRAP_QUESTION_COUNT, success_rate, success_rate)
        worse = difference_distribution_independent(
            TRAP_QUESTION_COUNT, success_rate - degradation / TRAP_QUESTION_COUNT, success_rate)
        result["independent"].append({
            "success_rate": success_rate,
            **{f"false_alarm_tolerance_{t}": failure_probability(equal, t) for t in TOLERANCES},
            **{f"detection_tolerance_{t}": failure_probability(worse, t) for t in TOLERANCES},
        })

    # İkinci varsayım, soru soru eşleştirme: iki modelin farklı sonuç verdiği sorular
    # ikisi arasında eşit bölünür. Kötüleşme varsa, fazladan kayıplar baseline lehine eklenir.
    for disagreement_rate in DISAGREEMENT_RATES:
        half_rate = disagreement_rate / 2
        degradation_rate = degradation / TRAP_QUESTION_COUNT
        equal = difference_distribution_paired(TRAP_QUESTION_COUNT, half_rate, half_rate)
        worse = difference_distribution_paired(TRAP_QUESTION_COUNT, half_rate + degradation_rate, half_rate)
        result["paired"].append({
            "disagreement_rate": disagreement_rate,
            **{f"false_alarm_tolerance_{t}": failure_probability(equal, t) for t in TOLERANCES},
            **{f"detection_tolerance_{t}": failure_probability(worse, t) for t in TOLERANCES},
        })

    # Üçüncü varsayım: adaptör belirli sayıda soruyu kesin olarak kaybeder.
    # Kalan sorularda yine şansa bağlı küçük farklar olur. Burada yalnızca yakalama olasılığı hesaplanır.
    result["exact_degradation"] = []
    for disagreement_rate in DISAGREEMENT_RATES:
        half_rate = disagreement_rate / 2
        noise = difference_distribution_paired(TRAP_QUESTION_COUNT - degradation, half_rate, half_rate)
        worse = {difference - degradation: probability for difference, probability in noise.items()}
        result["exact_degradation"].append({
            "disagreement_rate": disagreement_rate,
            **{f"detection_tolerance_{t}": failure_probability(worse, t) for t in TOLERANCES},
        })
    return result


# ---------- 3. Yargıç modelin insanla uyumu ----------
def calibration_uncertainty(pair_count: int, agreement: float = 0.75, kappa_chance: float = 0.5) -> dict:
    """
    Ne yapar:
        Yargıç modelin insanla ne kadar aynı kararı verdiği ölçülürken, bu ölçümün ne kadar kesin olduğunu hesaplar.
        Yargıç model, iki cevaptan hangisinin daha iyi olduğuna karar veren ayrı bir yapay zekâ modelidir.

    Neden var:
        Yargıcı seçmeden önce insanla birlikte birkaç cevap çifti puanlanır.
        Az sayıda çiftle ölçülen uyum şansa çok bağlıdır.
        Bu fonksiyon, 40 çiftin yargıç seçimi için yeterince kesin bilgi verip vermediğini gösterir.

    Ne alır:
        pair_count: Puanlanan cevap çifti sayısı. Örnek: 40
        agreement: Beklenen uyum oranı. Varsayılan: 0.75 (yüzde 75).
        kappa_chance: İki puanlayıcının sırf şans eseri aynı karara varma olasılığı. Varsayılan: 0.5.

    Ne döndürür:
        Kesinlik ölçüleri; "yüzde puan" cinsinden. Örnek (40 çift):
        {"pairs": 40, "agreement_half_width_percentage_points": 13.4, "wilson_lower_percentage_points": 59.8,
         "wilson_upper_percentage_points": 85.8, ...}
        Yani yüzde 75 ölçülen uyumun gerçek değeri büyük olasılıkla yüzde 60 ile 86 arasındadır.

    Nasıl çalışır:
        Üç yöntem kullanılır.
        Basit yöntem: ölçülen oranın iki yanına eşit pay bırakır.
        Wilson yöntemi: az sayıda ölçümde daha güvenilir bir aralık verir.
        Kappa: şans eseri uyumu çıkardıktan sonra kalan gerçek uyumu ölçer; burada yalnızca kaba bir kesinlik hesaplanır.
    """
    # Basit yöntem: ölçülen oranın iki yanına bırakılan pay.
    half_width = Z_SCORE_95 * sqrt(agreement * (1 - agreement) / pair_count)
    # Wilson yöntemi: aralığın ortası ve genişliği ayrı hesaplanır.
    center = (agreement + Z_SCORE_95**2 / (2 * pair_count)) / (1 + Z_SCORE_95**2 / pair_count)
    wilson_half_width = Z_SCORE_95 * sqrt(
        agreement * (1 - agreement) / pair_count + Z_SCORE_95**2 / (4 * pair_count * pair_count)
    ) / (1 + Z_SCORE_95**2 / pair_count)
    # Kappa için kaba kesinlik: basit yöntemdeki pay, şans eseri uyum çıkarıldıktan sonra büyür.
    kappa_half_width = Z_SCORE_95 * sqrt(agreement * (1 - agreement) / pair_count) / (1 - kappa_chance)
    return {
        "pairs": pair_count,
        "agreement_half_width_percentage_points": 100 * half_width,
        "wilson_lower_percentage_points": 100 * (center - wilson_half_width),
        "wilson_upper_percentage_points": 100 * (center + wilson_half_width),
        "pairs_per_5_percentage_points": 0.05 * pair_count,
        "percentage_points_per_pair": 100 / pair_count,
        "kappa_half_width": kappa_half_width,
    }


# ---------- 4. Eski Holm hesabı ve işaret testi ----------
def holm_thresholds(test_count: int, alpha: float = 0.05) -> list[float]:
    """
    Ne yapar:
        Holm yöntemine göre, birden fazla test yapıldığında her testin geçmesi gereken sınırları hesaplar.

    Neden var:
        Bu yöntem artık kullanılmıyor; projede tek bir ikincil test kaldığı için gereksiz oldu.
        Yine de ilk sürümün sonuçlarıyla karşılaştırma yapılabilsin diye hesaplanmaya devam ediyor.

    Ne alır:
        test_count: Test sayısı. Örnek: 3
        alpha: Genel yanlış alarm sınırı. Varsayılan: 0.05.

    Ne döndürür:
        Sırayla sınırlar. Örnek (3 test): [0.0167, 0.025, 0.05]
    """
    return [alpha / (test_count - i) for i in range(test_count)]


def sign_test_p_value(wins: int, decision_count: int) -> float:
    """
    Ne yapar:
        İşaret testinin p değerini hesaplar.
        İşaret testi şunu sorar: iki model aslında eşit olsaydı, bu kadar çok galibiyet
        yalnızca şans eseri ne sıklıkla çıkardı? Bu sıklığa p değeri denir.

    Neden var:
        Eşik 1.1 ve 5.1, "adaptör baseline'dan anlamlı ölçüde daha iyi mi?" sorusunu bu testle cevaplar.
        p değeri 0,05'ten küçükse sonuç şansa bağlanamayacak kadar güçlü sayılır.

    Ne alır:
        wins: Adaptörün kazandığı karşılaştırma sayısı. Örnek: 45
        decision_count: Beraberlikler çıkarıldıktan sonra kalan karşılaştırma sayısı. Örnek: 70

    Ne döndürür:
        p değeri. Örnek: 45 galibiyet, 70 karar için yaklaşık 0.022.

    Nasıl çalışır:
        İki model eşit olsaydı her karşılaştırma yazı tura gibi olurdu.
        Bu en az bu kadar uç bir sonucun olasılığı hesaplanır; iki yön de sayılır
        (çok kazanmak da çok kaybetmek de uç sayılır), bu yüzden sonuç 2 ile çarpılır.
    """
    wins = max(wins, decision_count - wins)
    return min(1.0, 2 * sum(comb(decision_count, i) for i in range(wins, decision_count + 1)) / 2**decision_count)


def minimum_wins_required(decision_count: int, alpha: float) -> int | None:
    """
    Ne yapar:
        Belli sayıda karşılaştırmada, sonucun anlamlı sayılması için en az kaç galibiyet gerektiğini bulur.

    Neden var:
        "100 karşılaştırmanın kaçını kazanmak gerekir?" sorusu, sonuçlar görülmeden önce cevaplanmalı.
        Böylece kural sonuçlara göre esnetilemez.

    Ne alır:
        decision_count: Karşılaştırma sayısı (beraberlikler hariç). Örnek: 100
        alpha: Anlamlılık sınırı. Örnek: 0.05

    Ne döndürür:
        Gereken en az galibiyet. Örnek: 100 karşılaştırma için 61.
        Hiçbir galibiyet sayısı yetmiyorsa None (boş) döner; 5 veya daha az karşılaştırmada böyledir.
    """
    return next(
        (wins for wins in range(decision_count // 2, decision_count + 1)
         if sign_test_p_value(wins, decision_count) < alpha),
        None,
    )


def minimum_wins_table(largest_decision_count: int = 100) -> list[dict]:
    """
    Ne yapar:
        1'den verilen sayıya kadar her karşılaştırma sayısı için gereken en az galibiyeti ve p değerini tablolar.

    Neden var:
        Eşik belgesindeki 1.1 tablosu buradan gelir. Elle hesaplanırsa hata yapılabilir.

    Ne alır:
        largest_decision_count: Tablonun gideceği en büyük karşılaştırma sayısı. Varsayılan: 100.

    Ne döndürür:
        Her karşılaştırma sayısı için bir satır.
        Örnek satır: {"decision_count": 100, "alpha_0.05": 61, "alpha_0.05_p_value": 0.035, ...}
    """
    rows = []
    for decision_count in range(1, largest_decision_count + 1):
        row = {"decision_count": decision_count}
        for label, alpha in TABLE_ALPHAS:
            wins = minimum_wins_required(decision_count, alpha)
            row[f"alpha_{label}"] = wins
            row[f"alpha_{label}_p_value"] = sign_test_p_value(wins, decision_count) if wins is not None else None
        rows.append(row)
    return rows


def main() -> None:
    """
    Ne yapar:
        Terminalde yazılan komutu okur, bütün hesapları yapar, tek bir dosyaya yazar ve kısa bir özet basar.

    Neden var:
        Eşik belgelerindeki "ölçüldü" diye işaretli sayılar her zaman aynı komutla yeniden üretilebilsin.

    Ne alır:
        Doğrudan bir değer almaz. Bilgileri terminalde yazılan komuttan okur (--output ve --degradation).

    Ne döndürür:
        Bir değer döndürmez. Sonuç dosyasını yazar ve ekrana özet basar.
        Örnek ekran çıktısı: "Aile düzeyinde yanlış alarm: {'17_guard_thresholds': 0.582, ...}"
    """
    # Komuttaki seçenekleri tanımla. Her seçeneğin tek bir İngilizce adı vardır.
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", type=Path, required=True, help="Sonuçların yazılacağı JSON dosyası")
    parser.add_argument("--degradation", type=int, default=3,
                        help="Tuzak hesabında adaptörün kaç soru daha kötü varsayılacağı")
    arguments = parser.parse_args()

    # Bütün hesapları yap. Anahtarların sırası ilk sürümle aynıdır; iki dosya yan yana okunabilsin.
    result = {
        "family_wise_false_alarm_alpha_0_05": {
            "17_guard_thresholds": family_wise_error_rate(17),
            "21_guard_thresholds_s2_two_baselines": family_wise_error_rate(21),
            "4_critical_2.1x2_3.7_4.2": family_wise_error_rate(4),
            "3_critical_2.1x1_3.7_4.2": family_wise_error_rate(3),
        },
        "trap_4_1": trap_threshold_analysis(arguments.degradation),
        "calibration": [calibration_uncertainty(pair_count) for pair_count in CALIBRATION_PAIR_COUNTS],
        "holm_thresholds": {f"test_count={m}": holm_thresholds(m) for m in HOLM_TEST_COUNTS},
        "sign_test_minimum_wins": {
            f"alpha={alpha:.4f}": {
                f"decision_count={count}": minimum_wins_required(count, alpha) for count in SIGN_TEST_DECISION_COUNTS
            }
            for alpha in SIGN_TEST_ALPHAS
        },
        "sign_test_minimum_wins_table_1_to_100": minimum_wins_table(100),
    }

    # Sonuçları dosyaya yaz.
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # Ekrana kısa bir özet yaz. Bu yalnızca okumayı kolaylaştırır; resmî değerler dosyadadır.
    family_wise = result["family_wise_false_alarm_alpha_0_05"]
    print("Aile düzeyinde yanlış alarm:", {key: round(value, 3) for key, value in family_wise.items()})
    for model_name in ("independent", "paired"):
        print(f"4.1 {model_name}:")
        for row in result["trap_4_1"][model_name]:
            rate_key = "success_rate" if model_name == "independent" else "disagreement_rate"
            print(f"  {rate_key}={row[rate_key]:.2f}  "
                  + "  ".join(f"tolerans {t}: yanlış alarm={row[f'false_alarm_tolerance_{t}']:.3f}, "
                              f"yakalama={row[f'detection_tolerance_{t}']:.3f}" for t in TOLERANCES))
    print("4.1 kesin kötüleşme (tam N soruda kayıp + gürültü):")
    for row in result["trap_4_1"]["exact_degradation"]:
        print(f"  disagreement_rate={row['disagreement_rate']:.2f}  "
              + "  ".join(f"tolerans {t}: yakalama={row[f'detection_tolerance_{t}']:.3f}" for t in TOLERANCES))
    for row in result["calibration"]:
        print(f"Kalibrasyon, {row['pairs']} çift: ±{row['agreement_half_width_percentage_points']:.1f} yüzde puan "
              f"(Wilson {row['wilson_lower_percentage_points']:.1f}–{row['wilson_upper_percentage_points']:.1f}), "
              f"5 yüzde puan = {row['pairs_per_5_percentage_points']:.2f} çift, kappa ±{row['kappa_half_width']:.2f}")
    print("Holm (tarihî):", {key: [round(value, 4) for value in values] for key, values in result["holm_thresholds"].items()})
    print("İşaret testi, gereken en az galibiyet:", result["sign_test_minimum_wins"])


if __name__ == "__main__":
    main()
