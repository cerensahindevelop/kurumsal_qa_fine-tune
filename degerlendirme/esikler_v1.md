# Geçme eşikleri v1 (ön kayıt)

Durum: TASLAK (01, 2026-11-23)
Bu eşikler **hiçbir model cevabı görülmeden** önerildi ve hiçbir model cevabı görülmeden onaylanacak. Onaydan önce doğrulama setinde puanlama yapılmaz; yalnızca 3–5 soruluk teknik deneme yapılır. Bir eşik değişirse `esikler_v2.md` dosyası açılır, gerekçesi yazılır ve rapora eklenir.

Tanımlar `degerlendirme/deney_plani_v1.md` §6'dadır. "Seçilen adaptör" = doğrulamada seçilen adaptör. "Yargıç" = kalibrasyonla seçilen yerel yargıç. "Fark" = adaptör eksi karşılaştırılan sistem. "pp" = yüzde puan.

---

## 0. Geçerlilik ön koşulları (bunlar sağlanmazsa koşu puanlanmaz)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 0.1 | `<think>` kalıntısı | 0 cevap | Düşünme modu her yerde kapalı olmalı; tek bir kalıntı ayarın yanlış olduğunu gösterir | bekliyor |
| 0.2 | Boş veya kesilmiş cevap (`max_new_tokens` sınırına dayanan) | ≤ %2 | Daha yüksek oran puanları üretim ayarına bağlı hâle getirir | bekliyor |
| 0.3 | Yargıç kalibrasyonu: insanla uyum (beraberlik hariç) | ≥ %75 ve Cohen kappa ≥ 0,50 | Bu sınırın altında yargıç insan yerine geçemez; yargıç ikincil göstergeye düşer | bekliyor |
| 0.4 | Yargıç sıra tutarlılığı (A-B ve B-A sıralarında aynı karar) | ≥ %80 | Daha düşük tutarlılık sıra yanlılığının sonucu belirlediğini gösterir | bekliyor |
| 0.5 | Yargıç seçimi | `gemma4:26b`, `gemma4:12b`'yi hem uyumda hem sıra tutarlılığında 5 pp'den fazla geçmiyorsa `gemma4:12b` seçilir | Sonuçlar yakınsa küçük model hız ve taşınabilirlik sağlar (kullanıcı kararı) | bekliyor |

## 1. Birincil sonuç: seçilen adaptör vs `hazir_istemli` (test, 100 soru)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 1.1 | **Birincil uç nokta:** yargıcın üslup+jargon ikili karşılaştırmasında adaptörün kazanma oranı (tutarsız kararlar beraberlik, beraberlikler hariç) | ≥ %60 **ve** iki yönlü işaret testinde p < 0,05 | "Belirgin gelişme" için %50'den açıkça yüksek bir oran gerekli. Tek başına %60 küçük örnekte şansla çıkabileceği için anlamlılık koşulu da eklendi | bekliyor |
| 1.2 | İnsan formu (açık karar 3'teki örneklem): üslup+jargon ortalaması (0–4) farkı | ≥ +0,5 ve eşleştirilmiş bootstrap (10.000 tekrar, seed 42) %95 güven aralığının alt sınırı > 0 | Yargıç sonucunun insan tarafından aynı yönde doğrulanması. 0,5 puan, iki ölçütten birinde her iki cevaptan birinde bir basamak artışa denk gelir | bekliyor |

Birincil sonuç = 1.1 ve 1.2 birlikte, **ayrıca** §2, §3 ve §4'teki koruma eşiklerinin hepsi. Yargıç 0.3 veya 0.4'ü geçemezse 1.2 tek başına birincil olur.

## 2. Bilgi doğruluğu: kötüleşme yok (test; hem `hazir` hem `hazir_istemli` ile ayrı ayrı)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 2.1 | Kritik hata içeren cevap sayısı (insan formu + yargıç işaretleri; çelişki insanla çözülür) | Fark ≤ +3 (100 soruda) | Küçük örnekte rastlantısal oynamaya pay bırakılır, ama birkaç soruluk sistematik kötüleşme kabul edilmez | bekliyor |
| 2.2 | Yargıç bilgi ikili karşılaştırması: kaybetme oranı − kazanma oranı | ≤ 10 pp | Bilgi bakımından eşitlik beklenir; adaptörün belirgin biçimde geride kalması kabul edilmez | bekliyor |
| 2.3 | Sayı/tarih/süre recall'u (ortalama) | Fark ≥ −3 pp | Rakam kaybı, üslup kazancının bilgi pahasına geldiğini gösterir | bekliyor |
| 2.4 | Aynı birimde referansla çelişen sayı içeren cevap sayısı | Fark ≤ +3 | 2.1'in otomatik karşılığı | bekliyor |
| 2.5 | chrF (ortalama) | Raporlanır, eşik yok | Üslup değişince chrF farklı yönlere oynayabilir; anlam doğruluğunu ölçmediği için geçme koşulu yapılmadı | bekliyor |

## 3. Genel Türkçe korunuyor (saklanan bölüm; karşılaştırma `hazir` ile)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 3.1 | TurkishMMLU doğruluğu | Fark ≥ −2,0 pp | 900 soruda (saklanan bölüm küçülürse oransal) yaklaşık 1,5 pp standart hata (tahmin); 2 pp'den büyük düşüş gerçek kayıp sayılır | bekliyor |
| 3.2 | GECTurk chrF | Fark ≥ −1,0 puan | chrF'de 1 puanın altındaki fark genellikle gürültüdür | bekliyor |
| 3.3 | XL-Sum chrF | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.4 | WMT16 EN→TR chrF | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.5 | Vikipedi perplexity | Göreli artış ≤ %10 | Alana uyum küçük bir artış doğurabilir; %10 üstü dil dağılımında belirgin kayma demektir | bekliyor |
| 3.6 | Aya ikili karşılaştırması (yargıç, adaptör vs `hazir`) | Kaybetme − kazanma ≤ 10 pp | Genel yardımseverlikte belirgin gerileme kabul edilmez | bekliyor |
| 3.7 | Üslup sızıntısı (50 gündelik soru, `deney_plani_v1.md` §6.6 işaret listesi) | Sızıntılı cevap oranı farkı ≤ +10 pp | 50 soruda 5 cevaplık artışa kadar tolerans; daha fazlası kurum dilinin gündelik kullanıma taştığını gösterir | bekliyor |
| 3.8 | Çoktan seçmelide harf çıkarılamayan cevap oranı | ≤ %3 | Daha yüksek oran 3.1'i biçim sorununa dönüştürür | bekliyor |

Bu eşikler doğrulamada da (Türkçe değerlendirmenin geliştirme bölümünde, açık karar 2) "gerekirse karışım" tetikleyicisi olarak kullanılır: 3.1–3.7'den biri aşılırsa `genel_karisim_adaptor` koşusu yapılır (açık karar 1'e bağlı).

## 4. Tuzak ve kapsam dışı davranış

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 4.1 | Tuzak başarısı (test aşaması, adet) | Adaptör ≥ `hazir_istemli` − 1 (ör. 22/28'e karşı en az 21/28) | Fine-tuning modelin "bilmiyorum" deme davranışını bozabilir; bir sorudan fazla kayıp kabul edilmez | bekliyor |
| 4.2 | Tuzak başarısı, mutlak alt sınır | ≥ 21/28 (%75) | Servise çıkacak bir model için asgari güven düzeyi. Hazır model bile altında kalırsa raporda ayrıca belirtilir | bekliyor |
| 4.3 | Geliştirme kapsam dışı seti (15) | ≥ 12/15; yalnızca geliştirme ölçüsü, final iddiası yok | Ayar seçerken erken uyarı vermesi için | bekliyor |

## 5. İkincil iddia: sentetik veri katkısı (test)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 5.1 | Üslup+jargon ikili karşılaştırması, `sss_sentetik_adaptor` vs `sss_adaptor` | Holm düzeltmesinden sonra iki yönlü işaret testinde p < 0,05 | Ön kayıtlı ikincil iddia; birden fazla karşılaştırma yapıldığı için düzeltme gerekli | bekliyor |
| 5.2 | Bilgi ikili karşılaştırması aynı çift | Kaybetme − kazanma ≤ 10 pp | Sentetik veri bilgiyi bozmamalı | bekliyor |
| 5.3 | Kritik hata farkı aynı çift | ≤ +2 | Aynı | bekliyor |

Üç koşul da sağlanmazsa rapora "sentetik verinin katkısı gösterilemedi" yazılır.

---

Senior onayı (genel): bekliyor
Onaylayan / tarih: —
Onay commit'i: —
