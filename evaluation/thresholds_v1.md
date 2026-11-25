Sade açıklama: thresholds_v1_explained.md (bağlayıcı değildir; çelişki olursa bu dosya geçerlidir).

# Geçme eşikleri v1 (ön kayıt)

Durum: TASLAK (01, 2026-11-23; aynı gün açık kararlarla güncellendi: §1.2, §2.1, §3, yeni §3A. 2026-11-24'te onaydan önce kullanıcı kararlarıyla güncellendi: kritik/uyarı ayrımı, 4.1, kalibrasyon 40 çift, raporlama kuralı, Holm ailesi önerisi; bkz. §6–§8. Aynı gün açık kararlar 17–20 kapatıldı: Holm ailesi, 2.1/2.1b birleşik etiketi, yargıç yedek yolu, kalibrasyon soruları; bkz. §8 değişiklik 5–8 ve yeni §9. Aynı gün açık karar 21 kapatıldı: §8 değişiklik 9, §9.1–§9.3. Aynı gün senior öncesi netleştirmeler ve açık karar 22: §8 değişiklik 10. Aynı gün açık karar 23: §8 değişiklik 11. Aynı gün `hazir_istemli` kapsamdan çıkarıldı: §8 değişiklik 12)
Bu eşikler **hiçbir model cevabı görülmeden** önerildi ve hiçbir model cevabı görülmeden onaylanacak. Onaydan önce doğrulama setinde puanlama yapılmaz; yalnızca 3–5 soruluk teknik deneme yapılır. Bir eşik değişirse `thresholds_v2.md` dosyası açılır, gerekçesi yazılır ve rapora eklenir.

Tanımlar `evaluation/experiment_plan_v1.md` §6'dadır. "Seçilen adaptör" = doğrulamada seçilen adaptör. "Yargıç" = kalibrasyonla seçilen yerel yargıç. "Fark" = adaptör eksi karşılaştırılan sistem. "pp" = yüzde puan.

**Sınır kuralı (bütün eşikler; 2026-11-24, onaydan önce değişiklik):** eşiğe eşit değer geçer (tetiklemez); eşiği aşan değer kalır (tetikler). Karşılaştırma yuvarlamadan önce, ham değerle yapılır. Örnek: "fark ≥ −1,0" eşiğinde −1,00 geçer, −1,04 kalır (raporda "−1,0" diye yuvarlansa bile).

**"Kaybetme − kazanma" paydası (2.2, 3.6, 5.2, T.6, K.2; 2026-11-24):** karşılaştırılan bütün kayıtlardır, beraberlikler dahil. 1.1 ve 5.1'deki işaret testi ise beraberlikleri dışarıda bırakır.

**Eşik sınıfları (§6):** §2, §3 ve §4'teki koruma eşiklerinden yalnızca **2.1, 3.7 ve 4.2 kritiktir**; tablolarda **Kritik** diye işaretlidir. Diğerleri **uyarı eşiğidir**; aşıldıklarında §6'daki inceleme süreci işler. 4.3 doğrulamada bir seçim kısıtıdır. §0 ön koşulları, §3A tetikleyicisi ve §5 ikincil iddia koşulları bu ayrımın dışındadır. Bütün ikili karşılaştırmalar §7'deki raporlama kuralına uyar.

---

## 0. Ön koşullar

İki türdür (2026-11-24, onaydan önce değişiklik; §8 değişiklik 10):
- **0.1–0.2 geçerlilik koşuludur.** Sağlanmazsa o koşu puanlanmaz ve üretim tekrarlanır. Tekrardan önce neden bulunup giderilir; aynı düzeltme o aşamadaki bütün sistemlere uygulanır. Düzeltme ve tekrar sayısı rapora yazılır. Test aşamasında (11) düzeltme yalnızca 0.1–0.2'yi gidermek için ve hiçbir puan üretilmeden önce yapılabilir.
- **0.3–0.5 yargıç uygunluğudur.** Sağlanmazsa koşu durmaz; §9'daki yedek yol uygulanır.

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 0.1 | `<think>` kalıntısı | 0 cevap | Düşünme modu her yerde kapalı olmalı; tek bir kalıntı ayarın yanlış olduğunu gösterir | bekliyor |
| 0.2 | Boş veya kesilmiş cevap (`max_new_tokens` sınırına dayanan) | ≤ %2 | Daha yüksek oran puanları üretim ayarına bağlı hâle getirir | bekliyor |
| 0.3 | Yargıç kalibrasyonu (doğrulama setinden **40 çift**; `baseline` ile ilk `faq_adapter` koşusunun doğrulama cevapları, §8 değişiklik 12): insanla uyum (beraberlik hariç) | ≥ %75 ve Cohen kappa ≥ 0,50 | Bu sınırın altında yargıç insan yerine geçemez; yargıç ikincil göstergeye düşer. Çift sayısı 20–30'dan 40'a çıkarıldı (§8, değişiklik 3). Üslup+jargon ve bilgi prompt'ları için **ayrı ayrı** ölçülür ve ayrı ayrı geçilir (§9.3) | bekliyor |
| 0.4 | Yargıç sıra tutarlılığı (A-B ve B-A sıralarında aynı karar) | ≥ %80 | Daha düşük tutarlılık sıra yanlılığının sonucu belirlediğini gösterir. Üslup+jargon ve bilgi prompt'ları için ayrı ayrı ölçülür (§9.3) | bekliyor |
| 0.5 | Yargıç seçimi | Her prompt türü için ayrı: iki aday da o türde 0.3 ve 0.4'ü geçtiyse `gemma4:26b` yalnızca uyumda (0.3) `gemma4:12b`'yi 5 pp'den fazla geçerse seçilir; aksi hâlde `gemma4:12b`. Yalnızca biri geçtiyse o seçilir. İkisi de kalırsa §9.2–§9.3 | Sonuçlar yakınsa küçük model hız ve taşınabilirlik sağlar (kullanıcı kararı). Sıra tutarlılığı seçimde ayrıca karşılaştırılmaz; 0.4'te eşik olarak aranır (2026-11-24, onaydan önce değişiklik). Karşılaştırma 0.3'teki aynı 40 çift üzerinde yapılır; 40 çiftte 5 pp = 2 çift (§8, değişiklik 3). Seçim her prompt türü için ayrı yapılır (§9.3) | bekliyor |

## 1. Birincil sonuç: seçilen adaptör vs `baseline` (test, 100 soru)

Fine-tuning proje sahibinin talebidir; prompt'la karşılaştırma kapsam dışıdır. `baseline` (baseline) üslup gelişiminin karşılaştırma noktası ve gerileme kontrollerinin taban çizgisidir (2026-11-24, onaydan önce değişiklik; §8 değişiklik 12).

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 1.1 | **Birincil uç nokta:** yargıcın üslup+jargon ikili karşılaştırmasında adaptörün kazanma / beraberlik / kayıp sayıları (tutarsız kararlar beraberlik) | İki yönlü kesin işaret testinde **p < 0,05** (beraberlikler hariç). Gereken en az galibiyet aşağıdaki tabloda | "Belirgin gelişme" şanstan ayırt edilebilir bir üstünlük olarak tanımlandı. İlk taslaktaki "≥ %60" koşulu kaldırıldı (2026-11-24, onaydan önce değişiklik): p < 0,05, 1–100 kesin kararın her birinde en az %60,6 galibiyet gerektirdiği için hiçbir zaman bağlayıcı değildi (ölçüldü). Kaldırılması hiçbir sonucu değiştirmez | bekliyor |
| 1.2 | Kör insan formu, üslup ve jargon bölümü (11. aşama, testten 50 soru, yalnızca birincil çift: seçilen adaptör ve `baseline`; tek değerlendirici, referans gösterilmez): üslup+jargon ortalaması (0–4) farkı | ≥ +0,5 ve eşleştirilmiş bootstrap (10.000 tekrar, seed 42) %95 güven aralığının alt sınırı > 0 | Yargıç sonucunun insan tarafından aynı yönde doğrulanması. 0,5 puan, soruların yarısında iki ölçütten birinde bir basamak artışa denk gelir | bekliyor |

**1.1 ve 5.1 için gereken en az galibiyet** (iki yönlü kesin işaret testi; ölçüldü, `src/evaluation/threshold_probabilities.py`; 1–100 arası bütün n değerleri `degerlendirme/esik_olasiliklari_v1.json`, `isaret_testi_galibiyet_tablosu_n_1_100`). n = beraberlik dışı kesin karar sayısı. 5.1'de Holm düzeltmesi kaldırıldığı için (§8 değişiklik 12) iki eşik de α = 0,05 kullanır. n ≤ 5 iken anlamlılık mümkün değildir.

| n | α = 0,05 (1.1 ve 5.1) |
|---|---|
| 10 | 9 (%90,0; p = 0,021) |
| 20 | 15 (%75,0; p = 0,041) |
| 30 | 21 (%70,0; p = 0,043) |
| 40 | 27 (%67,5; p = 0,038) |
| 50 | 33 (%66,0; p = 0,033) |
| 60 | 39 (%65,0; p = 0,027) |
| 70 | 44 (%62,9; p = 0,041) |
| 80 | 50 (%62,5; p = 0,033) |
| 90 | 55 (%61,1; p = 0,045) |
| 100 | 61 (%61,0; p = 0,035) |

**Birincil sonucun kararı (2026-11-24, onaydan önce değişiklik; §6):**
- **Geçti:** 1.1 ve 1.2 birlikte sağlanır, kritik koruma eşikleri 2.1, 3.7 ve 4.2'nin hiçbiri aşılmaz **ve** §6.2'deki yeniden hesaptan sonra hiçbir uyarı eşiği aşılmış kalmaz.
- **Çekinceli:** 1.1 ve 1.2 sağlanır, kritik eşiklerin hiçbiri aşılmaz, ama en az bir uyarı eşiği §6.2'deki yeniden hesaptan sonra da aşılmış kalır (2026-11-24, onaydan önce değişiklik).
- **Kaldı:** 1.1 veya 1.2 sağlanmaz **ya da** kritik eşiklerden en az biri aşılır. Uyarı eşikleri "kaldı" sonucunu doğurmaz.
- **Uyarı eşikleri** (§2, §3, §4'teki diğer bütün koruma eşikleri) aşılırsa birincil sonuç kendiliğinden "kaldı" olmaz. Aşılan eşik raporda kırmızı bayrakla gösterilir; §6.2'deki inceleme kayıt etiketlerini düzeltir ve eşik yeniden hesaplanır. Senior kararı yalnızca servise çıkış hakkındadır ve sonucu "geçti"ye çeviremez (§6.2 U.5).
- Yargıç **üslup+jargon prompt'unda** 0.3 veya 0.4'ü geçemezse önce diğer yargıç adayına bakılır; o geçtiyse o kullanılır. **İki aday da** geçemezse 1.2 tek başına birincil olur ve 1.1 raporda "güvenilirliği düşük" notuyla gösterilir. Bilgi prompt'undaki sonuç bu kuralı etkilemez (§9.3). Yargıca dayanan öteki eşiklerin yedek yolu §9.2'dedir (2026-11-24, onaydan önce değişiklik; §8, değişiklik 7).

## 2. Bilgi doğruluğu: kötüleşme yok (test; yalnızca `baseline` ile)

Bu bölümde **2.1 kritik**, diğerleri uyarı eşiğidir (§6).

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 2.1 | **Kritik.** Kritik hata içeren cevap sayısı (100 soru; yargıç bilgi işaretleri + aynı birimde çelişen sayı) | Fark ≤ +3 (100 soruda) | Küçük örnekte rastlantısal oynamaya pay bırakılır, ama birkaç soruluk sistematik kötüleşme kabul edilmez. Kayıt etiketleri §9.1'deki birleşik kurala göre belirlenir (insan formundaki 50 soruda insanın etiketi); yargıç kalibrasyondan kalırsa §9.2 | bekliyor |
| 2.1b | Kör insan formu, bilgi bölümü (yalnızca birincil çift, 50 soru, referans gösterilir): "Referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" sorusuna "Hayır" cevabı alan cevap sayısı | Fark ≤ +2 (50 soruda) | 2.1'in insan karşılığı. 50 soruda +2 bilinçli olarak onaylandı (kullanıcı, 2026-11-24): +1 bu boyutta sürekli yanlış alarm verir. Oransal olarak 2.1'den gevşektir (%4'e karşı %3); bu fark rapora yazılır. Aynı tolerans yedek yoldaki kritik 2.1'de de geçerlidir (§9.2). İnsan kararı eşiğin sonucunu değil, kayıt düzeyindeki etiketi değiştirir: insanın bu 50 sorudaki "kritik hata var/yok" etiketi 2.1'de yargıç + betik etiketinin yerini alır (§9.1; 2026-11-24, onaydan önce değişiklik, §8 değişiklik 6) | bekliyor |
| 2.2 | Yargıç bilgi ikili karşılaştırması: kaybetme oranı − kazanma oranı | ≤ 10 pp | Bilgi bakımından eşitlik beklenir; adaptörün belirgin biçimde geride kalması kabul edilmez | bekliyor |
| 2.3 | Sayı/tarih/süre recall'u (ortalama) | Fark ≥ −3 pp | Rakam kaybı, üslup kazancının bilgi pahasına geldiğini gösterir | bekliyor |
| 2.4 | Aynı birimde referansla çelişen sayı içeren cevap sayısı | Fark ≤ +3 | 2.1'in otomatik karşılığı | bekliyor |
| 2.5 | chrF (ortalama) | Raporlanır, eşik yok | Üslup değişince chrF farklı yönlere oynayabilir; anlam doğruluğunu ölçmediği için geçme koşulu yapılmadı | bekliyor |

## 3. Genel Türkçe korunuyor: final eşikleri (11. aşama, saklanan %70; taban çizgisi `baseline`)

Bölme kararı: her dosya, sabit seed (42) ile %30 geliştirme / %70 saklanan olarak ayrılır; her görevde geliştirme bölümü en az 50 kayıt olur. Bölme 02'de yapılacak. Aşağıdaki sayılar beklenen boyutlardır (`wc -l` × oran); kesin sayılar 02'de ölçülecek.

Bu bölümde **3.7 kritik**, diğerleri uyarı eşiğidir (§6).

| # | Ölçüt (saklanan kayıt) | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 3.1 | TurkishMMLU doğruluğu (630) | Fark ≥ −2,0 pp | 630 soruda tek bir oranın standart hatası yaklaşık 2 pp; aynı sorulardaki eşleştirilmiş farkta daha küçük (tahmin). 2 pp'den büyük düşüş gerçek kayıp sayılır | bekliyor |
| 3.2 | GECTurk chrF (350) | Fark ≥ −1,0 puan | chrF'de 1 puanın altındaki fark genellikle gürültüdür | bekliyor |
| 3.3 | XL-Sum chrF (350) | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.4 | WMT16 EN→TR chrF (350) | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.5 | Vikipedi perplexity (350) | Göreli artış ≤ %10 | Alana uyum küçük bir artış doğurabilir; %10 üstü dil dağılımında belirgin kayma demektir | bekliyor |
| 3.6 | Aya ikili karşılaştırması (175; yargıç, adaptör vs `baseline`) | Kaybetme − kazanma ≤ 10 pp | Genel yardımseverlikte belirgin gerileme kabul edilmez | bekliyor |
| 3.7 | **Kritik.** Üslup sızıntısı (gündelik sorular, `experiment_plan_v1.md` §6.6, **gruba göre işaret listesi**: `a` için kurum adı/yönlendirme dahil, `b` için yalnızca kurum ağzı + bürokratik kalıp + resmî kip yoğunluğu; geliştirme: `genel_kontrol_v1` tamamı; saklanan: `genel_kontrol_v2`, karar 6a ve 6c) | Sızıntılı cevap **oranı** ≤ `baseline` oranı + 10 pp | 50 soruda yaklaşık 5 cevaplık artışa kadar tolerans; daha fazlası kurum dilinin gündelik kullanıma taştığını gösterir. Oran olarak yazıldı, böylece saklanan bölümün boyutundan bağımsız | bekliyor |
| 3.8 | Çoktan seçmelide harf çıkarılamayan cevap oranı | Değerlendirilen adaptörün oranı ≤ %3; `baseline`'ın oranı yalnızca raporlanır | Daha yüksek oran 3.1'i biçim sorununa dönüştürür (kime uygulandığı 2026-11-24'te netleştirildi) | bekliyor |
| 3.9 | `b_kurum_gayriresmi` bilgi doğruluğu (`genel_kontrol_v2`, 15 soru; yargıç, `experiment_plan_v1.md` §6.3 ölçeği, referans = onaylı `bilgi_ogeleri`) | Kritik hatalı cevap sayısı ≤ `baseline` + 1 **ve** ortalama puan farkı ≥ −0,2 | Sade anlatım bilgi kaybı pahasına olmamalı (başarı ölçütü 2). 15 soruda tek bir kritik hata gürültü olabilir, ikincisi değildir. Ortalama puandaki 0,2'lik pay, 15 soruda yaklaşık 3 cevabın bir basamak düşmesine karşılık gelir. Onaylanmayan bilgi öğesi puanlamaya girmez | bekliyor |

**Karar 6c'den sonraki değişiklik (2026-11-23, onaydan önce):**
- 3.7'nin ölçütü `b` grubu için yeniden tanımlandı. 3.9 eklendi. T.7'ye aynı gruba göre ölçüt uygulanır.
- **Gerekçe:** kullanıcının v1 kontrolüne göre `b` grubu kurum işlemi soran ve sade anlatım bekleyen sorulardan oluşuyor. Bu sorularda kurum ve sistem adlarını yasaklamak doğru cevabı sızıntı sayardı. Yeni ölçüt yalnızca bürokratik kalıbı yasaklıyor, doğruluğu ise ayrıca ölçüyor (`experiment_plan_v1.md` §6.6 ve karar 6c).
- Bu değişiklik dosya henüz onaylanmadan yapıldı ve hiçbir model puanlanmadı. Bu yüzden yeni bir sürüm dosyası açılmadı. Onaydan sonraki değişiklikler `thresholds_v2.md` ile yapılır.

## 3A. "Gerekirse karışım" tetikleyicisi (doğrulama aşaması, geliştirme %30; taban çizgisi `baseline`)

Karar (kullanıcı, 2026-11-23): genel Türkçe verisi eğitime **yalnızca** aşağıdaki tetikleyici çalışırsa girer.

**Ne zaman ölçülür:** doğrulamada SSS tarifi seçildikten sonra (`faq_adapter` veya `faq_synthetic_adapter`), **bir kez**. O adaptör ve `baseline`, Türkçe değerlendirmenin geliştirme bölümünde aynı ayarlarla çalıştırılır. Tetikleyiciyi aşmamak için ayar değiştirip yeniden ölçmek yasaktır; ölçüm yinelenirse bu rapora yazılır.

**Kural:** aşağıdaki T satırlarından **en az biri** aşılırsa `general_mix_adapter` eğitilir. §6.2'deki inceleme ve yeniden hesap T satırlarına uygulanmaz; T.2–T.5 (chrF, perplexity) zaten kayıt düzeyinde düzeltilemez (karar 23b). Yargıç üslup+jargon türünde kalırsa T.6 tetiklemez ve "ölçülemedi" diye raporlanır; diğer T ölçütleri çalışmaya devam eder (karar 23c). Hiçbiri aşılmazsa genel Türkçe verisi eğitime girmez ve `general_mix_adapter` oluşturulmaz.

| # | Ölçüt (geliştirme kaydı, beklenen) | Tetikleme sınırı (T.1–T.7: `baseline` taban çizgisine göre izin verilen en fazla düşüş; T.8: değerlendirilen adaptörün mutlak oranı, `baseline`'ın oranı yalnızca raporlanır) | Senior onayı |
|---|---|---|---|
| T.1 | TurkishMMLU doğruluğu (270) | 2,0 pp (fark < −2,0 pp → tetikler) | bekliyor |
| T.2 | GECTurk chrF (150) | 1,0 puan | bekliyor |
| T.3 | XL-Sum chrF (150) | 1,0 puan | bekliyor |
| T.4 | WMT16 EN→TR chrF (150) | 1,0 puan | bekliyor |
| T.5 | Vikipedi perplexity (150) | göreli artış %10 | bekliyor |
| T.6 | Aya ikili karşılaştırması (75) | kaybetme − kazanma 10 pp | bekliyor |
| T.7 | **Gündelik sorularda üslup sızıntısı** (`genel_kontrol_v1`, 50 gündelik soru; gruba göre işaret listesi, `experiment_plan_v1.md` §6.6). `b` doğruluğu v1'de yalnızca raporlanır, tetiklemez | sızıntılı cevap oranı `baseline` oranının en fazla **10 pp** üstünde olabilir | bekliyor |
| T.8 | Çoktan seçmelide harf çıkarılamayan cevap oranı | mutlak %3 | bekliyor |

**Neden final eşikleriyle aynı sayılar:** iki tür hatanın maliyeti eşit değil.
- **Yanlış alarm:** gürültü yüzünden tetikleyici gereksiz yere çalışırsa bedeli bir ek eğitim koşusudur.
- **Kaçırma:** gerçek gerileme kaçırılırsa test aşamasında geri dönüşü olmayan bir başarısızlık çıkar.

Geliştirme bölümü küçük olduğu için gürültü daha büyüktür, ama bu tetikleyiciyi kaba değil hassas yapar. Hassas olması istenen yön de budur.

**Tetiklendiğinde:**

| # | Kural | Senior onayı |
|---|---|---|
| K.1 | `general_mix_adapter`, seçilen tarife genel Türkçe çiftleri eklenerek eğitilir. Genel Türkçe payı eğitim örneklerinin %10'u veya %20'si olur; ikisi de denenir; pay K.2'deki kurala göre seçilir. Genel Türkçe çiftleri `egitim_sorulari.jsonl` sorularına üretilip onaylanmış cevaplardan oluşur | bekliyor |
| K.2 | **Pay seçimi** (2026-11-24, onaydan önce değişiklik): T.1–T.8'in hepsini geliştirme bölümünde geçen paylar arasından, doğrulamada üslup+jargon ikili karşılaştırmasında seçilen tarife göre net kazancı (kazanma − kaybetme; payda bütün kayıtlar) yüksek olan seçilir. İki payın net kazancı birbirinin 5 pp içindeyse %10 seçilir. Yalnızca biri geçtiyse o seçilir. Hiçbiri geçmezse K.3 uygulanır. **Seçilen adaptör olma:** seçilen pay aynı karşılaştırmada kaybetme − kazanma ≤ 10 pp sağlarsa "seçilen adaptör" olur; sağlamazsa K.3 | bekliyor |
| K.3 | K.2 sağlanmazsa seçilen tarif değişmez, karışım adaptörü yine teste girer (ikincil sonuç olarak) ve durum rapora yazılır | bekliyor |

## 4. Tuzak ve kapsam dışı davranış

Bu bölümde **4.2 kritik**, 4.1 uyarı eşiği, 4.3 doğrulamada seçim kısıtıdır (§6).

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 4.1 | Tuzak başarısı (test aşaması, adet) | Adaptör ≥ `baseline` − 2 (ör. 22/28'e karşı en az 20/28) | Fine-tuning modelin "bilmiyorum" deme davranışını bozabilir. 28 soruda −1 toleransı, iki model eşitken bile sık yanlış alarm verir; −2 yanlış alarmı azaltırken gerçek kötüleşmeyi yakalama gücünü −3'ten belirgin biçimde yüksek tutar. Mutlak güvence kritik eşik 4.2'dir (2026-11-24, onaydan önce değişiklik; olasılıklar §8, değişiklik 2) | bekliyor |
| 4.2 | **Kritik.** Tuzak başarısı, mutlak alt sınır | ≥ 21/28 (%75) | Servise çıkacak bir model için asgari güven düzeyi. Baseline bile altında kalırsa raporda ayrıca belirtilir. Yargıç kalibrasyondan kalırsa tuzak puanı insandan gelir (§9.2) | bekliyor |
| 4.3 | Geliştirme kapsam dışı seti (15) | ≥ 12/15; doğrulamada **seçim kısıtı**, final iddiası yok | Aday ayarlar (checkpoint, tarif) arasında 12/15'i geçen varsa geçemeyen seçilmez. Hiçbiri geçemezse 4.3 puanı en yüksek olan seçilir (eşitlikte olağan seçim ölçütü) ve durum kaydedilir (2026-11-24, onaydan önce değişiklik). Uyarı sınıfında değildir (§6.1) | bekliyor |

Puanın kaynağı (kullanıcı kararı, 2026-11-23):
- 4.1 ve 4.2'deki birincil tuzak puanı, `experiment_plan_v1.md` §6.4'teki önceden kayıtlı başarı ölçütlerinden ve projenin kendi yargıç akışından gelir.
- Ham verideki `05_tuzak_sorular/otomatik_kontrol.py` ve `yargic_promptu.md` şimdi kullanılmaz. 11. aşamada en fazla ek kontrol olarak çalışabilir; bunun kararı 11'e kalır. Ek kontrolün sonucu birincil tuzak puanını değiştirmez ve ayrı raporlanır.

## 5. İkincil iddia: sentetik veri katkısı (test)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 5.1 | Üslup+jargon ikili karşılaştırması, `faq_synthetic_adapter` vs `faq_adapter` | İki yönlü işaret testinde p < 0,05 (Holm düzeltmesi yok; §8 değişiklik 12) | Ön kayıtlı tek ikincil iddia. Prompt'un katkısı testi kalktı ve adaptör vs `baseline` birincil oldu; geriye tek ikincil test kaldığı için çoklu karşılaştırma düzeltmesine gerek yok | bekliyor |
| 5.2 | Bilgi ikili karşılaştırması aynı çift | Kaybetme − kazanma ≤ 10 pp | Sentetik veri bilgiyi bozmamalı | bekliyor |
| 5.3 | Kritik hata farkı aynı çift | ≤ +2 | Aynı | bekliyor |

Üç koşul da sağlanmazsa rapora "sentetik verinin katkısı gösterilemedi" yazılır.

## 6. Kritik ve uyarı eşikleri (2026-11-24, onaydan önce değişiklik)

### 6.1 Sınıflar

| Sınıf | Eşikler | Aşılırsa |
|---|---|---|
| **Kritik** | 2.1, 3.7, 4.2 | Birincil sonuç "kaldı" olur. §2 artık yalnızca `baseline` ile karşılaştırıldığı için 2.1 tek bir kontroldür |
| **Uyarı** | 2.1b, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8, 3.9, 4.1 | Raporda kırmızı bayrakla gösterilir; §6.2'deki inceleme kayıt etiketlerini düzeltir ve eşik yeniden hesaplanır. Hâlâ aşılıyorsa birincil sonuç "çekinceli" olur |
| Sınıf dışı | 4.3 (doğrulamada seçim kısıtı, §4; 2026-11-24'te uyarı sınıfından çıkarıldı), §0 (0.1–0.5), §3A (T.1–T.8, K.1–K.3), §5 (5.1–5.3), 2.5 (eşik yok) | Kendi kuralları geçerlidir. T.1–T.8 bir karar kuralıdır ve bu ayrımdan etkilenmez |

"Kırmızı bayrak": rapordaki sonuç tablosunda eşiği aşan satır **KIRMIZI BAYRAK** etiketiyle ve ölçülen değer, eşik değeri ve inceleme dosyasının yoluyla birlikte gösterilir. Bayrak, inceleme sonucu ne olursa olsun raporda kalır.

### 6.2 Uyarı eşiği aşıldığında inceleme

**U.1 Ne zaman.** Eşiğin ölçüldüğü aşamada, o aşamanın bütün puanları üretilip commit edildikten **sonra**. Test eşikleri için 11. aşamada. İnceleme yalnızca incelenen kayıtların etiketlerini düzeltir (U.4); eşik değeri, ayar ve model çıktısı değişmez. Yeni üretim (yeniden ölçüm) yapılmaz; eşik yalnızca düzeltilmiş etiketlerle yeniden hesaplanır (U.5; 2026-11-24, onaydan önce değişiklik).

**U.2 Hangi kayıtlar.** Kayıtları bir betik seçer (seed 42) ve yalnızca kimlik yazar:

| Eşik türü | Eşikler | İncelenecek kayıtlar |
|---|---|---|
| Sayım farkı | 2.1b, 2.4, 3.1, 3.9 (kritik hata koşulu), 4.1 | **İki yöndeki bütün uyuşmayan kayıtlar:** adaptörde olumsuz olup karşılaştırılan sistemde olumsuz olmayanlar **ve** tersi (karar 23a). 3.1 için uyuşmayan kayıt: iki sistemden yalnızca birinin doğru bildiği soru |
| Mutlak oran | 3.8 | Adaptörde olumsuz olan (harf çıkarılamayan) **bütün** kayıtlar + adaptörde harf çıkarılan kayıtlardan seed 42 ile **20** rastgele kayıt (ters yöndeki yanılgı: betiğin cevapta olmayan bir harfi çıkarması) |
| İkili karşılaştırma | 2.2, 3.6 | Yargıcın iki sırada da tutarlı karar verdiği **bütün** kayıtlar: adaptörün kaybettikleri **ve** kazandıkları. Beraberlikler incelenmez |
| Ortalama farkı | 2.3, 3.9 (ortalama koşulu) | Kayıt düzeyinde farkı en olumsuz **20** kayıt + en olumlu **20** kayıt (eşitlikte seed 42 ile seçim) + kalan kayıtlardan seed 42 ile **10** rastgele kayıt. Rastgele kayıtlar, farkın birkaç kayıttan mı yoksa genelden mi geldiğini görmek için kontroldür |
| Düzeltilemez | 3.2, 3.3, 3.4, 3.5 | Kayıt incelenmez, yeniden hesap yapılmaz; aşılırsa sonuç doğrudan "çekinceli" olur (U.5, karar 23b) |

- Bir eşik için **her yönde** en fazla 40 kayıt incelenir (adaptör aleyhine ve adaptör lehine ayrı ayrı). Fazlaysa o yönde seed 42 ile 40 kayıt seçilir; toplam sayı ayrıca yazılır. İki yönde aynı seçim kuralı ve aynı etiket şeması kullanılır; CSV'de kaydın yönü değerlendiriciye gösterilmez ve kayıtlar karışık sırayla verilir (seed 42).
- §2'deki eşikler yalnızca `baseline` karşılaştırmasında ölçülür; kayıtlar bu karşılaştırmadan seçilir.

**U.3 Kim.**
- Kayıtları **insan değerlendirici** (proje sahibi) inceler ve her kayda neden etiketi koyar.
- Claude ve yargıç model inceleme kararı vermez. Test kayıtlarındaki metin yalnızca insan için üretilen CSV'de bulunur. Claude bu CSV'yi kendi okuyacağı biçimde açmaz; 11'deki bütün puanlar commit edildikten sonra yalnızca rapor örneği için okuyabilir.
- Nihai kararı **senior** verir.

**U.4 Nasıl kayda geçer.**
1. Betik `review/warning_<experiment_id>_<threshold>.csv` dosyasını üretir. Sütunlar: kimlik, eşik, seçilme nedeni (`en_olumsuz` / `rastgele` / `tamami`), otomatik ve yargıç puanları, soru, referans, iki sistemin cevabı. Doldurulacak sütunlar `neden`, `duzeltilmis_etiket` ve `not`.
2. `neden` şu değerlerden biridir (2026-11-24, onaydan önce değişiklik):
   - `gercek_hata`: kayıttaki olumsuz etiket doğru.
   - `olcum_yanilgisi`: yargıç veya betik (harf çıkarma, sayı ayrıştırma dahil) yanıldı. Değerlendirici doğru etiketi `duzeltilmis_etiket` sütununa yazar.
   - `belirsiz`: karar verilemedi; özgün etiket kalır.
3. Değerlendirici CSV'yi doldurur. Betik etiket dağılımını sayar.
4. İnceleme özeti `evaluation/warning_review_<experiment_id>.md` dosyasına yazılır: eşik, ölçülen değer, eşik değeri, aşılan karşılaştırma, incelenen ve toplam kayıt sayısı, etiket dağılımı, değerlendiricinin kısa yorumu.
5. CSV ve özet, senior kararından **önce** `11: uyarı incelemesi <esik>` mesajıyla commit edilir.

**U.5 Yeniden hesap, sonuç ve senior kararı** (2026-11-24, onaydan önce değişiklik).
1. Betik eşiği yeniden hesaplar: `olcum_yanilgisi` etiketli kayıtlarda düzeltilmiş etiketle, diğer bütün kayıtlarda özgün etiketle. İki yöndeki düzeltmeler birlikte uygulanır (karar 23a).
   - **Düzeltilemeyen eşikler (karar 23b):** 3.2–3.5 (chrF, perplexity) kayıt düzeyinde düzeltilemez; aşılırsa yeniden hesap yapılmaz ve sonuç doğrudan "çekinceli" olur. Bu bilinçli bir tercihtir: deterministik bir metriği sonuç görüldükten sonra kayıt kayıt ayıklamak, ölçümü yeniden tanımlamak olurdu.
   - **Kritik eşiklere taşınmaz:** uyarı incelemesindeki etiket düzeltmeleri kritik eşiklere (2.1, 3.7, 4.2) uygulanmaz; kritik eşikler özgün (2.1'de §9.1'deki birleşik) etiketlerle hesaplanır. Örneğin 2.4 incelemesinde düzeltilen bir sayı çelişkisi 2.1'in sayımını değiştirmez.
2. Yeniden hesaplanan değer eşiği geçerse uyarı kalkar. Kırmızı bayrak, özgün değer ve inceleme özeti raporda kalır.
3. Hâlâ aşılıyorsa raporda "uyarı eşiği aşıldı" yazılır ve birincil sonuç **"çekinceli"** ilan edilir (§1).
4. Senior kararı yalnızca **servise çıkış** hakkındadır. Özet dosyasının sonuna gerekçesi, onaylayanı ve tarihiyle yazılır ve ayrı bir commit'le kaydedilir. Senior kararı birincil sonucu "geçti"ye çeviremez.

Rapor, her uyarı eşiği için özgün değeri, yeniden hesaplanan değeri, etiket dağılımını ve servis kararını birlikte gösterir.

Kayıt seçiminin iki yönlü olması ve düzeltilemeyen eşikler karar 23 ile belirlendi (§8 değişiklik 11).

**U.6 Bekleyen iş.** Kayıt seçme betiği (`src/evaluation/warning_review_queue.py`) 11. aşamadan önce yazılacak.

## 7. Raporlama kuralı (2026-11-24, onaydan önce değişiklik)

**R.1** Bütün ikili karşılaştırmalarda kazanma oranı **hiçbir zaman tek başına yazılmaz**. Kapsam: 1.1, 2.2, 3.6, 5.1, 5.2, T.6, K.2, §3'teki ikincil karşılaştırmalar ve sonradan raporlanan her ikili karşılaştırma. Her seferinde şunlar birlikte verilir:
- **kazanma / beraberlik / kayıp** sayıları; beraberliğin kaçının "eşit" kararı, kaçının sıra tutarsızlığı olduğu parantez içinde;
- iki yönlü işaret testinin **p değeri** (beraberlikler hariç);

Örnek (uydurma): "kazanma / beraberlik / kayıp = 58 / 12 / 30 (beraberlik: 7 eşit, 5 sıra tutarsız); iki yönlü işaret testi p = 0,004."

Bu kural tablolar, grafikler, özet cümleler ve sunum için de geçerlidir. Oran yazılabilir, ama yalnızca bu sayıların yanında.

## 8. Onaydan önce değişiklikler (2026-11-24, kullanıcı kararları)

Dosya henüz onaylanmadı ve hiçbir model puanlanmadı. Bu yüzden değişiklikler yeni sürüm dosyası açılmadan bu dosyaya işlendi. Önceki hâl git geçmişindedir (`7bb442d`). Olasılıkları `python -m src.evaluation.threshold_probabilities --output degerlendirme/esik_olasiliklari_v1.json` hesapladı; tam olasılık hesabıdır, veri kullanmaz. Aşağıda "ölçüldü" yazan sayılar bu betikten gelir.

**Değişiklik 1: kritik / uyarı ayrımı (§1, §6).**
- Gerekçe (kullanıcı): koruma eşiklerinin hepsi zorunlu olunca, her biri %5 yanlış alarm verse bile en az birinin şans eseri aşılma olasılığı yaklaşık %58'dir (bağımsızlık varsayımıyla kaba hesap).
- Ölçüldü: 17 eşikte 1 − 0,95¹⁷ = **%58,2**. Kullanıcının sayısıyla aynı.
- Ek (ölçüldü): §2'deki dört eşik (2.1, 2.2, 2.3, 2.4) iki ayrı karşılaştırmada uygulandığı için zorunlu kontrol sayısı aslında 21'dir; 21'de **%65,9**. Yeni hâlde kritik kontroller 2.1 × 2 karşılaştırma + 3.7 + 4.2 = 4 kontroldür; 4'te **%18,5**. 2.1 tek karşılaştırmada sayılırsa 3'te **%14,3**.
- Sınır: eşikler %5 yanlış alarma göre ayarlanmadı ve birbirinden bağımsız değil. Sayılar yalnızca büyüklük sırasını gösterir.

**Değişiklik 2: 4.1, −1 yerine −2.**
- Gerekçe (kullanıcı): iki model eşitken −1'in yanlış alarm olasılığı yaklaşık %19–38, −2'ninki %6–23. Gerçekte yaklaşık 3 soru kötüleşmeyi yakalama olasılığı −1 ve −2'de yaklaşık %68, −3'te %36'ya düşüyor. Mutlak güvence kritik eşik 4.2'dir.
- Hesap üç modelle yapıldı (28 soru):
  - (i) iki model bağımsız binom, başarı oranı %70–90;
  - (ii) eşleştirilmiş, soruların %10–30'unda iki model farklı sonuç veriyor, 3 soruluk kötüleşme beklenen değer olarak;
  - (iii) eşleştirilmiş, adaptör tam 3 soruda kesin kötü, kalan 25 soruda gürültü.

| Ölçüldü | −1 | −2 | −3 |
|---|---|---|---|
| Yanlış alarm, iki model eşit (model i ve ii) | %17,5–33,1 | %6,4–23,3 | %1,8–15,3 |
| 3 soruluk kötüleşmeyi yakalama (model i ve ii) | %66,5–73,9 | %55,7–57,9 | %40,8–44,6 |
| 3 soruluk kötüleşmeyi yakalama (model iii) | %70,9–83,9 | %57,3–63,2 | %36,8–42,7 |

- **Kullanıcının sayılarıyla fark:**
  - −2'nin yanlış alarm aralığı aynı.
  - −1'in yanlış alarm aralığı biraz daha düşük çıktı (%17,5–33,1; verilen %19–38).
  - −3'ün %36'sı yalnızca model (iii)'nin alt ucuyla örtüşüyor.
  - **Asıl fark:** −2'nin yakalama olasılığı hiçbir modelde −1 ile eşit (%68) çıkmadı; %56–63 aralığında. −2'ye geçiş yanlış alarmı yaklaşık 10 pp azaltırken yakalama gücünü 11–21 pp düşürür. Kararın yönü değişmiyor (−2, −3'ten belirgin biçimde güçlü), ama bedeli verilen gerekçedeki kadar küçük değil.
- Örnek "22/28'e karşı en az 20/28" olarak güncellendi.

**Değişiklik 3: yargıç kalibrasyonu 40 çift (0.3, 0.5; `experiment_plan_v1.md` §6.8, §6.9; `report/report_plan_v1.md` §4).**
- Gerekçe (kullanıcı): %75 uyumun belirsizliği 25 çiftte yaklaşık ±17 pp, 40 çiftte ±13 pp; 0.5'teki 5 pp'lik fark 25 çiftte yaklaşık tek bir çifte denk geliyor.
- Ölçüldü (normal yaklaşımla %95 yarı genişlik):
  - 25 çiftte **±17,0 pp** (Wilson aralığı %55,5–87,8).
  - 40 çiftte **±13,4 pp** (Wilson %59,8–85,8).
  - 5 pp, 25 çiftte **1,25 çift**, 40 çiftte **2,0 çift**.
  - Kullanıcının sayılarıyla aynı.
- Ek (ölçüldü):
  - Uyum beraberlikler hariç hesaplandığı için etkin çift sayısı 40'ın altında kalır. Beraberlik %20 ise 32 çift kalır ve belirsizlik **±15,0 pp** olur.
  - Kappa için kaba yaklaşık belirsizlik (şans uyumu %50 varsayımıyla) 40 çiftte **±0,27**. 0,50 kappa eşiği 40 çiftte de geniş bir belirsizlik taşır.

**Değişiklik 4: raporlama kuralı (§7).** Gerekçe (kullanıcı kararı): kazanma oranı tek başına, beraberliklerin ne kadar olduğunu ve sonucun şanstan ayırt edilip edilmediğini gizler. Hesap gerektirmez.

**Değişiklik 5: Holm ailesinin tanımı (5.1). KARAR (kullanıcı, 2026-11-24): seçenek A.** *(Değişiklik 12 ile geçersiz: H2 kalktı, H3 birincil oldu; Holm kaldırıldı.)*

- Gerekçe (kullanıcı): üç ikincil iddiada düzeltmesiz toplam yanlış iddia riski yaklaşık %14; düzeltmenin bedeli 5.1 için 61 yerine en fazla 63 galibiyet. Ölçüldü: 1 − 0,95³ = %14,3 (bağımsızlık varsayımıyla); 100 kesin kararda 61–63 galibiyet. Kullanıcının sayılarıyla aynı.
- **Aile (m = 3, sabit).** 11. aşamada test setinde, yargıcın **üslup+jargon** ikili karşılaştırması üzerindeki üç iki yönlü işaret testi:
  - H1: `faq_synthetic_adapter` vs `faq_adapter` (5.1)
  - H2: `hazir_istemli` vs `baseline` (prompt'un katkısı, `experiment_plan_v1.md` §3, ikincil 2)
  - H3: seçilen adaptör vs `baseline` (ikincil 3)
- **Aileye girmeyenler:**
  - 1.1, tek birincil uç nokta; düzeltmesiz α = 0,05.
  - Eşik biçimindeki ölçütler (2.2, 3.6, 5.2, 5.3, K.2 vb.); bunlar hipotez testi değildir.
  - Bilgi ikili karşılaştırmalarının p değerleri. Bilgi testleri "kötüleşme yok" eşikleriyle yönetilir.
  - `general_mix_adapter`'ın K.3 kapsamındaki karşılaştırmaları. Bu adaptörün oluşup oluşmayacağı önceden bilinmiyor; aile boyutu sonuca bağlı olmasın diye bunlar düzeltmesiz ve "keşif" etiketiyle raporlanır.
- **Bedeli (ölçüldü):** Holm'da 5.1'in sınırı, ailedeki sırasına göre 0,0167 ile 0,05 arasında değişir. 100 kesin kararda bu, düzeltmesiz 61 yerine **61–63** galibiyet demektir. 80 kararda 50 yerine 50–52.
- **Seçenekler:**

| Seçenek | Aile | 5.1 için Holm sınırı | 100 kararda gereken galibiyet (ölçüldü) |
|---|---|---|---|
| **A (seçildi)** | H1–H3, m = 3 | 0,0167–0,05 | 61–63 |
| B | Yalnızca H1 (m = 1, düzeltme yok). Gerekçe: ön kayıtlı tek ikincil iddia 5.1'dir; H2 ve H3 betimsel raporlanır. `experiment_plan_v1.md` §3'teki "Holm uygulanır" cümlesi değişmeli | 0,05 | 61 |
| C | H1–H3 × (üslup+jargon, bilgi), m = 6 | 0,0083–0,05 | 61–64 |

- Neden A (öneri gerekçesi, kullanıcı kabul etti): plan §3, ikincil karşılaştırmalarda Holm'u zaten öngörüyor; H2 ve H3 rapora "prompt işe yaradı" ve "adaptör baseline'dan iyi" diye iddia olarak girecek sonuçlardır. Bilgi karşılaştırmaları ise "kötüleşme yok" sorusunu sorar ve eşikle ele alınır.

**Bu değişikliklerle açığa çıkan sorular (2026-11-24'te kullanıcı kararıyla kapatıldı; değişiklik 6–8):**
1. **2.1b ile kritik 2.1.** → Kapandı: değişiklik 6. 2.1b'deki "2.1 ile çelişirse insan kararı geçerlidir" cümlesi değiştirilmedi. 2.1 artık kritik, 2.1b uyarı. 2.1 aşılır ama 2.1b geçerse, birincil sonuç "kaldı" mı olur, yoksa insan kararı kritik sonucu kaldırır mı, belli değil.
2. **Yargıca dayanan kritik eşikler.** → Kapandı: değişiklik 7. 2.1 (yargıç bilgi işaretleri) ve 4.2 (yargıç + otomatik kontrol) kritik oldu. Yargıç 0.3 veya 0.4'ü geçemezse bu iki kritik eşiğin nasıl ölçüleceği yazılı değil.
3. **Kalibrasyon çiftleri ve prompt ayarı.** → Kapandı: değişiklik 8. `experiment_plan_v1.md` §6.8 madde 6'ya göre kalibrasyon çiftleri prompt ayarında kullanılmaz. 40 çift, 100 soruluk doğrulama setinin 40 sorusuna denk gelebilir. Bu kural soruları mı kapsıyor, yalnızca çiftleri mi, netleştirilmeli.

**Değişiklik 6: 2.1 ile 2.1b (kullanıcı kararı, 2026-11-24).**
- Karar: insan kararı eşiğin sonucunu değil, **kayıt düzeyindeki etiketi** değiştirir. İnsanın puanladığı 50 soruda insanın "kritik hata var/yok" etiketi yargıcın etiketinin yerini alır; diğer 50 soruda yargıç + betik etiketi kalır. Kritik 2.1 bu birleşik etiketlerle hesaplanır (§9.1).
- 2.1b'deki "2.1 ile çelişirse insan kararı geçerlidir" cümlesi bu kuralla değiştirildi.
- Gerekçe: eski cümle bir uyarı eşiğinin (2.1b) kritik bir eşiğin (2.1) sonucunu kaldırmasına izin veriyordu. Yeni kural insanın üstünlüğünü korur, ama bunu tek tek kayıtlarda yapar; eşiklerin sınıfı değişmez.
- Uygulama için gereken ek (bu kararın sonucu): insan formunun bilgi bölümünde şu an "kritik hata var/yok" alanı yoktu; yalnızca Evet / Kısmen / Hayır soruluyordu. "Hayır" kritik hatayla aynı şey değildir (§6.3'te bilgi puanı 0 = "kritik hata var **ya da** ana hüküm yanlış"). Bu yüzden forma `experiment_plan_v1.md` §6.3 tanımıyla ayrı bir "kritik hata var / yok" alanı eklendi (§6.9). 2.1b "Hayır" sayısıyla hesaplanmaya devam eder.
- Bu ekin kapsamı ve 2.1'in `baseline` karşılaştırmasındaki uygulaması için §9.1'deki not ve açık karar 21'e bakınız.

**Değişiklik 7: yargıç kalibrasyondan kalırsa yedek yol (kullanıcı kararı, 2026-11-24).** Kural §9.2'de. Gerekçe: 2.1 ve 4.2 kritik oldu ve ikisi de yargıca dayanıyordu; yargıç kalırsa nasıl ölçüleceği yazılı değildi. Kalibrasyon doğrulama aşamasında yapıldığı için yedek yolun gerekip gerekmediği 11. aşamadan önce bilinir; insan iş yükü önceden planlanabilir.

**Değişiklik 8: kalibrasyon soruları prompt ayarından çıkarılmaz (kullanıcı kararı, 2026-11-24).** *(Değişiklik 12 ile kapsam dışı: prompt ayarı yok. Aynı ilke adaptör ayar seçimine taşındı, V9.)*
- Doğrulamanın 100 sorusunun hepsi prompt ayarında kullanılır; kalibrasyonun 40 sorusu da dahil. `experiment_plan_v1.md` §6.8 madde 6 buna göre değiştirildi.
- Bedeli: aynı 40 soru hem yargıcı seçmek hem prompt'u ayarlamak için kullanılır; doğrulama sonuçları bu nedenle de iyimser olabilir. Final iddiası yalnızca kilitli testten gelir. Sınırlama `report/report_plan_v1.md` §4.4'e eklendi.

**Değişiklik 9: açık karar 21 (kullanıcı kararı, 2026-11-24).**
- *(a ve b, değişiklik 12 ile sadeleşti: insan formu artık `baseline`'ı kapsıyor, birleşik etiket `baseline` karşılaştırmasında uygulanıyor.)*
- (a) Normal yolda 2.1'in `baseline` karşılaştırmasında iki taraf da yargıç + betikle sayılır. Gerekçe: bir karşılaştırmada iki taraf aynı ölçüm aracıyla sayılmalı (§9.1).
- (b) Yedek yolda 2.1'in `baseline` karşılaştırması yalnızca betik kısmıyla (2.4 tanımı) sayılır ve "güvenilirliği düşük" notu alır (§9.2).
- (c) Yedek yolda ikincil iddialar (5.1, Holm ailesi) yapılmaz; "güvenilir ölçüm yapılamadı, iddia yapılmadı" diye raporlanır (§9.2).
- (d) Yargıç yalnızca bir prompt türünde kalırsa yedek yol yalnızca o türe dayanan eşiklere uygulanır. 0.3 ve 0.4'ün prompt türü başına ayrı ölçüldüğü yazılı değildi; ayrı ölçüm tanımlandı (§9.3).

**Değişiklik 10: senior öncesi netleştirmeler (kullanıcı kararları, 2026-11-24).** Hiçbir eşik değeri değişmedi; değişenler kuralların yazımı ve uygulanışıdır.
- #1, 1.1: "≥ %60" koşulu kaldırıldı; kural "iki yönlü işaret testinde p < 0,05". Gereken en az galibiyet tablosu §1'de (ölçüldü). 1–100 kesin kararda gereken en düşük oran %60,6 olduğu için kaldırma hiçbir sonucu değiştirmez.
- #2, §0: 0.1–0.2 geçerlilik koşulu (sağlanmazsa koşu tekrarlanır), 0.3–0.5 yargıç uygunluğu (sağlanmazsa §9).
- #6, 0.5: her prompt türü için ayrı; 26B yalnızca uyumda 5 pp'den fazla öndeyse seçilir; yalnızca biri geçtiyse o.
- #7: "kaybetme − kazanma" paydası bütün kayıtlar, beraberlikler dahil (Tanımlar).
- #8: sınır kuralı: eşiğe eşit değer geçer, aşan kalır; karşılaştırma yuvarlamadan önce (Tanımlar).
- #9: 3.8 ve T.8 değerlendirilen adaptöre uygulanır; `baseline`'ın oranı yalnızca raporlanır. T tablosunun sütun başlığı düzeltildi.
- #12: K.2'de pay seçim kuralı (net kazanç, 5 pp içinde %10, hiçbiri geçmezse K.3).
- #15: 2.1b ve yedek yoldaki kritik 2.1 için "50 soruda ≤ +2" bilinçli olarak onaylandı; oransal fark rapora yazılır.
- #20: 4.3 doğrulamada seçim kısıtı; uyarı sınıfından çıkarıldı (uyarı eşiği sayısı 14'ten 13'e indi).
- #24: uyarı incelemesi yalnızca kayıt etiketlerini düzeltir; eşik yeniden hesaplanır; hâlâ aşılıyorsa birincil sonuç "çekinceli". Senior kararı yalnızca servise çıkış hakkında (§1, §6.2).
- Açık karar 22: Aya (3.6, T.6) üslup+jargon türüne bağlandı (§9.3). Tek yargıç kuralı eklenmedi.

**Uygulama yorumları (kullanıcı onayladı, 2026-11-24):**
- §0'da "koşu tekrarlanır": greedy ve sabit seed ile aynı ayarlarla tekrar aynı çıktıyı verir. Bu yüzden tekrardan önce neden giderilir ve aynı düzeltme bütün sistemlere uygulanır. Testte düzeltme yalnızca puan üretilmeden önce yapılabilir.
- 4.3'te "en iyisi", 4.3 puanı en yüksek olan aday olarak yazıldı; eşitlikte olağan seçim ölçütü.
- Uyarı etiketlerinden `referans_sorunu` kalktı. Eskimiş referans yargıç veya betik yanılgısı değildir; yeni şemada `belirsiz` sayılır ve özgün etiket kalır. Formdaki "referans eskimiş olabilir" kutusu ve rapor planı §4.2'deki keşif analizi bundan etkilenmez.

**Açığa çıkan sorular (açık karar 23; 2026-11-24'te kapatıldı, değişiklik 11):**
1. **Yeniden hesap tek yönlü.** U.2 yalnızca adaptör aleyhine kayıtları seçiyor. Yalnızca bunlar düzeltilip yeniden hesap yapılırsa ölçüm yanılgıları yalnızca adaptör lehine düzelir; karşı yöndeki yanılgılar (ör. `baseline`'a haksız verilmiş kritik hata, adaptörün kaçırılmış hatası) olduğu gibi kalır. Yeniden hesap bu yüzden adaptör lehine yanlıdır. → Kapandı: 23a.
2. **Sürekli otomatik metriklerde "etiket" yok.** 3.2–3.5 (chrF, perplexity) kayıt etiketiyle değil, betiğin deterministik hesabıyla ölçülür; inceleme bu değerleri düzeltemez. Etiket düzeltme 2.1b, 2.2, 2.4, 3.1 ve 3.8 (harf çıkarma), 3.6, 3.9 ve 4.1'de tanımlıdır; 2.3'te yalnızca sayı ayrıştırma hatası için. → Kapandı: 23b.
3. **T.6 yargıç uygunluğu olmadan.** Üslup+jargon türünde iki aday da kalırsa T.6'nın tetikleyici olarak çalışıp çalışmayacağı yazılı değil. → Kapandı: 23c.

**Değişiklik 11: açık karar 23 (kullanıcı kararı, 2026-11-24).** Hiçbir eşik değeri ve kritik/uyarı ayrımı değişmedi.
- (a) Yeniden hesap yapılan eşiklerde iki yöndeki uyuşmayan kayıtlar aynı yöntemle incelenir. Gerekçe: tek yönlü düzeltme sonucu sistematik olarak adaptör lehine kaydırır (§6.2 U.2, U.5).
- (b) chrF ve perplexity eşikleri (3.2–3.5, T.2–T.5) kayıt düzeyinde düzeltilemez; aşılırlarsa sonuç doğrudan "çekinceli" olur (3.2–3.5) ya da tetikleyici çalışır (T.2–T.5). Bilinçli bir tercihtir (§6.2 U.5, §3A).
- (c) Yargıç üslup+jargon türünde kalırsa T.6 tetiklemez ve "ölçülemedi" diye raporlanır; diğer T ölçütleri çalışır (§3A, §9.3).
- Uygulanırken çıkan belirsizlikler kullanıcının kuralına göre açık karar açılmadan çözüldü ve `PROJECT_STATUS.md` "Varsayılan olarak uygulananlar" bölümüne yazıldı: 3.1'in sayım türüne alınması, 3.8'de ters yön için rastgele 20 kayıt, ikili karşılaştırmada iki yön ve beraberliklerin incelenmemesi, yön başına 40 kayıt sınırı ve kör sıralama, düzeltmelerin kritik eşiklere taşınmaması.


**Değişiklik 12: `hazir_istemli` kapsamdan çıkarıldı (kullanıcı kararı, 2026-11-24).** Gerekçe (kullanıcı): fine-tuning proje sahibinin doğrudan talebidir; fine-tuning'in prompt'tan üstün olup olmadığını sınamak kapsam dışıdır. `baseline` kalır; rakip değil, gerileme kontrollerinin taban çizgisi ve üslup gelişiminin karşılaştırma noktasıdır. **Hiçbir eşiğin sayısal değeri değişmedi.**
- §1: birincil çift seçilen adaptör vs `baseline`. 1.1 ve 1.2 bu çifte uygulanır; 1.2'deki kör insan formu adaptör ve `baseline` cevaplarını karşılaştırır.
- §2: bilgi eşikleri yalnızca `baseline` ile karşılaştırılır. Birleşik etiket (karar 18) `baseline` karşılaştırmasında geçerlidir. Karar 21a'nın ilkesi (iki taraf aynı araçla) korunur ama ayrı kuralı gerekmez; karar 21b'deki betik yedeği gereksizleşti.
- 4.1: adaptör ≥ `baseline` − 2. Tuzak yedek yolu adaptör ve `baseline` cevaplarını puanlar. 4.1'in §8 değişiklik 2'deki olasılıkları iki sistem arasındaki farka dayanır; hangi sistemin taban olduğuna bağlı değildir.
- **Holm kaldırıldı.** Eski aile H1 (5.1), H2 (prompt'un katkısı) ve H3'tü (adaptör vs `baseline`). H2 kapsamdan çıktı, H3 birincil uç nokta oldu (kendi α = 0,05'iyle, aile dışında). Geriye tek ikincil test (5.1) kaldığı için çoklu karşılaştırma yoktur; düzeltme kaldırıldı ve 5.1 α = 0,05 ile sınanır (100 kesin kararda 61 galibiyet, ölçüldü). Galibiyet tablosundaki Holm sütunları kaldırıldı; α = 0,05 değerleri aynıdır.
- **Kritik kontrol sayısı:** 2.1 artık tek karşılaştırmada ölçüldüğü için kritik kontroller 2.1 + 3.7 + 4.2 = 3'tür. Aile düzeyinde yanlış alarm %14,3 (ölçüldü, §8 değişiklik 1'deki "3 kritik" satırı).
- Kalibrasyon kaynağı ve uygulama yorumları: `PROJECT_STATUS.md` "Varsayılan olarak uygulananlar" V7–V9.


---

## 9. Birleşik etiketler ve yargıç yedek yolu (2026-11-24, onaydan önce değişiklik)

### 9.1 Kritik hata etiketinin kaynağı (2.1, 2.1b)

| Soru grubu | Etiketin kaynağı |
|---|---|
| İnsan formundaki 50 test sorusu (§6.9 seçimi) | İnsanın "kritik hata var / yok" etiketi. Bu sorularda yargıç ve betik etiketleri 2.1'e girmez |
| Kalan 50 test sorusu | Yargıç bilgi işaretleri + betiğin "aynı birimde çelişen sayı" tespiti (2.1'in özgün tanımı) |

- Kritik 2.1 bu birleşik etiketlerle hesaplanır; eşik değişmez (fark ≤ +3, 100 soruda).
- 2.1b insanın "Hayır" sayısıyla, aynı 50 soruda ayrıca hesaplanır; uyarı eşiğidir.
- Yargıç ve betik etiketleri 50 insan sorusunda da kaydedilir ve yargıç–insan uyumu olarak raporlanır; sonucu değiştirmez. 2.4 (betik) bütün 100 soruda kendi tanımıyla hesaplanmaya devam eder.
- **İki taraf aynı araçla sayılır (karar 21a'nın ilkesi; değişiklik 12 ile sadeleşti):** insan formu birincil çifti, yani seçilen adaptör ve `baseline` cevaplarını kapsar. 50 insan sorusunda iki tarafın etiketi de insandan, kalan 50 soruda iki tarafınki de yargıç + betikten gelir. Gerekçe: bir karşılaştırmada iki taraf aynı ölçüm aracıyla sayılmalı.

### 9.2 Yargıç kalibrasyondan kalırsa (0.3 veya 0.4)

Bu bölüm iki prompt türünde de kalma durumunu anlatır. Yalnızca bir türde kalma §9.3'tedir.


1. **Önce diğer aday.** Seçilen yargıç kalırsa diğer adayın kalibrasyon sonucuna bakılır. Geçtiyse o kullanılır. Ek ölçüm gerekmez: iki aday da aynı 40 çifti kalibrasyonda puanlamıştır (§0, `experiment_plan_v1.md` §6.8 madde 2).
2. **İkisi de kalırsa:**
   - **4.1 ve 4.2:** 28 tuzak sorusunun adaptör ve `baseline` cevaplarını (56 cevap) insan puanlar. Model adları gizli, sıra karışık, anahtar ayrı dosyada (§6.9'daki körleme kuralları); ölçüt `experiment_plan_v1.md` §6.4'teki önceden kayıtlı başarı tanımlarıdır. Otomatik kontrol ayrıca çalışır ve ayrı raporlanır; insan puanını değiştirmez. Eşikler değişmez (4.1: ≥ `baseline` − 2; 4.2: ≥ 21/28).
   - **Kritik 2.1:** yalnızca insanın puanladığı 50 soru üzerinden, insanın "kritik hata var/yok" etiketiyle, **fark ≤ +2** eşiğiyle hesaplanır. §2'nin tek karşılaştırması `baseline` olduğu ve insan formu `baseline`'ı kapsadığı için ayrı bir betik yedeğine (eski karar 21b) gerek kalmadı (değişiklik 12).
   - **1.1 / 1.2:** §1'deki kural geçerlidir: 1.2 tek başına birincildir, 1.1 "güvenilirliği düşük" notuyla raporlanır.
   - **Yargıca dayanan uyarı eşikleri** (2.2, 3.6, 3.9, 4.3, 5.2 ve tetikleyicide T.6, K.2) raporda "güvenilirliği düşük" notuyla gösterilir.
   - **İkincil iddialar** (karar 21c): 5.1 için iddia yapılmaz. Sonuçlar "güvenilir ölçüm yapılamadı, iddia yapılmadı" diye raporlanır. Kazanma / beraberlik / kayıp sayıları §7'ye göre yine yazılır, ama p değerinden sonuç çıkarılmaz. 5.2 ve 5.3 de aynı nota tabidir; "sentetik verinin katkısı gösterilemedi" cümlesi kullanılmaz, çünkü ölçülemeyen katkı "gösterilemedi" sayılmaz.
3. **1.1/1.2 kuralıyla tutarlılık (kontrol edildi):**
   - İki yol da aynı aracı kullanır: 11. aşamadaki 50 soruluk kör insan formu. Ek insan formu yalnızca tuzak için gelir.
   - 2.1'in yedek eşiği (+2 / 50 soru), 2.1b'nin 50 sorudaki toleransıyla aynıdır.
   - "Önce diğer aday" adımı `experiment_plan_v1.md` §6.8 madde 4–5 ile uyumludur ("eşiği geçen adaylar arasında", "hiçbir aday geçemezse"). §1'deki cümle tekil "yargıç" dediği için bununla uyumlu olacak biçimde "iki aday da" diye düzeltildi.
   - İlk yazımda açık kalan noktalar karar 21 ile kapandı: ikincil iddialar (yukarıda), tek prompt türünde kalma (§9.3). 2.1'in ayrı `baseline` karşılaştırması değişiklik 12 ile ortadan kalktı. 3.9 uyarı eşiği olarak "güvenilirliği düşük" kuralına girer.

### 9.3 Kalibrasyon prompt türüne göre (karar 21d, 2026-11-24)

**Kontrol sonucu.** İnsan kalibrasyon çiftlerini üslup+jargon ve bilgi için ayrı ayrı puanlıyordu ve yargıç iki ayrı prompt'la soruluyordu (`experiment_plan_v1.md` §6.8 madde 1 ve "Kullanım biçimi"). Ama 0.3, 0.4 ve plan §6.8 madde 3, uyum ve sıra tutarlılığının prompt türü başına ayrı hesaplanacağını söylemiyordu. Bu yüzden şöyle tanımlandı:

1. 0.3 (uyum ve kappa) ve 0.4 (sıra tutarlılığı) her aday için **üslup+jargon** ve **bilgi** prompt'larında ayrı ayrı hesaplanır. Bir aday bir prompt türünü ancak o türde hem 0.3'ü hem 0.4'ü sağlarsa geçer.
2. "Önce diğer aday" adımı (§9.2 madde 1) ve 0.5 seçim kuralı her prompt türü için ayrı uygulanır. Sonuç olarak iki prompt türü farklı adaylarla puanlanabilir; bu durumda iki model sırayla çalıştırılır (kartta aynı anda tek büyük model kuralı). Tek yargıç kuralı eklenmedi (kullanıcı kararı, 2026-11-24): her prompt türü, o türde kalibrasyonu geçen yargıçla puanlanır.
3. Yedek yol yalnızca kalınan prompt türüne dayanan eşiklere uygulanır:

| Kalınan prompt türü (iki aday da) | Ona dayanan eşikler | Ne olur |
|---|---|---|
| Üslup+jargon | 1.1; 5.1; K.2'nin üslup+jargon koşulu; 3.6 ve T.6 (Aya, karar 22) | 1.2 tek başına birincil olur, 1.1 "güvenilirliği düşük". Üslup ikincil iddiaları yapılmaz ("güvenilir ölçüm yapılamadı, iddia yapılmadı"). K.2'deki koşul ve 3.6 "güvenilirliği düşük" notuyla raporlanır. T.6 tetiklemez ve "ölçülemedi" diye raporlanır; diğer T ölçütleri çalışır (karar 23c) |
| Bilgi | 2.1, 2.2, 3.9, 4.1, 4.2, 4.3, 5.2, 5.3 | 2.1 ve 4.2 (ve 4.1) §9.2'deki insan yedeğine geçer. Diğerleri "güvenilirliği düşük" |

4. Tuzak (4.1–4.3) kendi prompt'uyla puanlanır, kalibrasyon çiftlerinde doğrudan sınanmaz. Kullanıcı kararıyla (karar 21d) tuzak eşikleri **bilgi** prompt türünün kalibrasyonuna bağlıdır.
5. Aya karşılaştırması (3.6, T.6) kendi prompt'uyla puanlanır. Kullanıcı kararıyla (karar 22, 2026-11-24) üslup+jargon türüne bağlıdır ve o türde seçilen yargıçla puanlanır.


Senior onayı (genel): bekliyor
Onaylayan / tarih: —
Onay commit'i: —
