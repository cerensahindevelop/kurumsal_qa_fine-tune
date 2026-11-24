Sade açıklama: esikler_v1_aciklama.md (bağlayıcı değildir; çelişki olursa bu dosya geçerlidir).

# Geçme eşikleri v1 (ön kayıt)

Durum: TASLAK (01, 2026-11-23; aynı gün açık kararlarla güncellendi: §1.2, §2.1, §3, yeni §3A. 2026-11-24'te onaydan önce kullanıcı kararlarıyla güncellendi: kritik/uyarı ayrımı, 4.1, kalibrasyon 40 çift, raporlama kuralı, Holm ailesi önerisi; bkz. §6–§8. Aynı gün açık kararlar 17–20 kapatıldı: Holm ailesi, 2.1/2.1b birleşik etiketi, yargıç yedek yolu, kalibrasyon soruları; bkz. §8 değişiklik 5–8 ve yeni §9)
Bu eşikler **hiçbir model cevabı görülmeden** önerildi ve hiçbir model cevabı görülmeden onaylanacak. Onaydan önce doğrulama setinde puanlama yapılmaz; yalnızca 3–5 soruluk teknik deneme yapılır. Bir eşik değişirse `esikler_v2.md` dosyası açılır, gerekçesi yazılır ve rapora eklenir.

Tanımlar `degerlendirme/deney_plani_v1.md` §6'dadır. "Seçilen adaptör" = doğrulamada seçilen adaptör. "Yargıç" = kalibrasyonla seçilen yerel yargıç. "Fark" = adaptör eksi karşılaştırılan sistem. "pp" = yüzde puan.

**Eşik sınıfları (§6):** §2, §3 ve §4'teki koruma eşiklerinden yalnızca **2.1, 3.7 ve 4.2 kritiktir**; tablolarda **Kritik** diye işaretlidir. Diğerleri **uyarı eşiğidir**; aşıldıklarında §6'daki inceleme süreci işler. §0 geçerlilik ön koşulları, §3A tetikleyicisi ve §5 ikincil iddia koşulları bu ayrımın dışındadır. Bütün ikili karşılaştırmalar §7'deki raporlama kuralına uyar.

---

## 0. Geçerlilik ön koşulları (bunlar sağlanmazsa koşu puanlanmaz)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 0.1 | `<think>` kalıntısı | 0 cevap | Düşünme modu her yerde kapalı olmalı; tek bir kalıntı ayarın yanlış olduğunu gösterir | bekliyor |
| 0.2 | Boş veya kesilmiş cevap (`max_new_tokens` sınırına dayanan) | ≤ %2 | Daha yüksek oran puanları üretim ayarına bağlı hâle getirir | bekliyor |
| 0.3 | Yargıç kalibrasyonu (doğrulama setinden **40 çift**): insanla uyum (beraberlik hariç) | ≥ %75 ve Cohen kappa ≥ 0,50 | Bu sınırın altında yargıç insan yerine geçemez; yargıç ikincil göstergeye düşer. Çift sayısı 20–30'dan 40'a çıkarıldı (§8, değişiklik 3) | bekliyor |
| 0.4 | Yargıç sıra tutarlılığı (A-B ve B-A sıralarında aynı karar) | ≥ %80 | Daha düşük tutarlılık sıra yanlılığının sonucu belirlediğini gösterir | bekliyor |
| 0.5 | Yargıç seçimi | `gemma4:26b`, `gemma4:12b`'yi hem uyumda hem sıra tutarlılığında 5 pp'den fazla geçmiyorsa `gemma4:12b` seçilir | Sonuçlar yakınsa küçük model hız ve taşınabilirlik sağlar (kullanıcı kararı). Karşılaştırma 0.3'teki aynı 40 çift üzerinde yapılır; 40 çiftte 5 pp = 2 çift (§8, değişiklik 3) | bekliyor |

## 1. Birincil sonuç: seçilen adaptör vs `hazir_istemli` (test, 100 soru)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 1.1 | **Birincil uç nokta:** yargıcın üslup+jargon ikili karşılaştırmasında adaptörün kazanma oranı (tutarsız kararlar beraberlik, beraberlikler hariç) | ≥ %60 **ve** iki yönlü işaret testinde p < 0,05 | "Belirgin gelişme" için %50'den açıkça yüksek bir oran gerekli. Tek başına %60 küçük örnekte şansla çıkabileceği için anlamlılık koşulu da eklendi | bekliyor |
| 1.2 | Kör insan formu, üslup ve jargon bölümü (11. aşama, testten 50 soru, yalnızca birincil çift, tek değerlendirici, referans gösterilmez): üslup+jargon ortalaması (0–4) farkı | ≥ +0,5 ve eşleştirilmiş bootstrap (10.000 tekrar, seed 42) %95 güven aralığının alt sınırı > 0 | Yargıç sonucunun insan tarafından aynı yönde doğrulanması. 0,5 puan, soruların yarısında iki ölçütten birinde bir basamak artışa denk gelir | bekliyor |

**Birincil sonucun kararı (2026-11-24, onaydan önce değişiklik; §6):**
- **Geçti:** 1.1 ve 1.2 birlikte sağlanır **ve** kritik koruma eşikleri 2.1, 3.7 ve 4.2'nin hiçbiri aşılmaz.
- **Kaldı:** 1.1 veya 1.2 sağlanmaz **ya da** kritik eşiklerden en az biri aşılır. Uyarı eşiklerinin durumu bu kararı değiştirmez.
- **Uyarı eşikleri** (§2, §3, §4'teki diğer bütün koruma eşikleri) aşılırsa birincil sonuç kendiliğinden "kaldı" olmaz. Aşılan eşik raporda kırmızı bayrakla gösterilir, §6.2'deki inceleme yapılır ve birincil sonucun geçerli kalıp kalmayacağına senior ile birlikte karar verilir.
- Yargıç 0.3 veya 0.4'ü geçemezse önce diğer yargıç adayına bakılır; o geçtiyse o kullanılır. **İki aday da** geçemezse 1.2 tek başına birincil olur ve 1.1 raporda "güvenilirliği düşük" notuyla gösterilir. Yargıca dayanan öteki eşiklerin yedek yolu §9.2'dedir (2026-11-24, onaydan önce değişiklik; §8, değişiklik 7).

## 2. Bilgi doğruluğu: kötüleşme yok (test; hem `hazir` hem `hazir_istemli` ile ayrı ayrı)

Bu bölümde **2.1 kritik**, diğerleri uyarı eşiğidir (§6).

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 2.1 | **Kritik.** Kritik hata içeren cevap sayısı (100 soru; yargıç bilgi işaretleri + aynı birimde çelişen sayı) | Fark ≤ +3 (100 soruda) | Küçük örnekte rastlantısal oynamaya pay bırakılır, ama birkaç soruluk sistematik kötüleşme kabul edilmez. Kayıt etiketleri §9.1'deki birleşik kurala göre belirlenir (insan formundaki 50 soruda insanın etiketi); yargıç kalibrasyondan kalırsa §9.2 | bekliyor |
| 2.1b | Kör insan formu, bilgi bölümü (yalnızca birincil çift, 50 soru, referans gösterilir): "Referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" sorusuna "Hayır" cevabı alan cevap sayısı | Fark ≤ +2 (50 soruda) | 2.1'in insan karşılığı; örneklem yarı büyüklükte olduğu için tolerans da orantılı küçültüldü. İnsan kararı eşiğin sonucunu değil, kayıt düzeyindeki etiketi değiştirir: insanın bu 50 sorudaki "kritik hata var/yok" etiketi 2.1'de yargıç + betik etiketinin yerini alır (§9.1; 2026-11-24, onaydan önce değişiklik, §8 değişiklik 6) | bekliyor |
| 2.2 | Yargıç bilgi ikili karşılaştırması: kaybetme oranı − kazanma oranı | ≤ 10 pp | Bilgi bakımından eşitlik beklenir; adaptörün belirgin biçimde geride kalması kabul edilmez | bekliyor |
| 2.3 | Sayı/tarih/süre recall'u (ortalama) | Fark ≥ −3 pp | Rakam kaybı, üslup kazancının bilgi pahasına geldiğini gösterir | bekliyor |
| 2.4 | Aynı birimde referansla çelişen sayı içeren cevap sayısı | Fark ≤ +3 | 2.1'in otomatik karşılığı | bekliyor |
| 2.5 | chrF (ortalama) | Raporlanır, eşik yok | Üslup değişince chrF farklı yönlere oynayabilir; anlam doğruluğunu ölçmediği için geçme koşulu yapılmadı | bekliyor |

## 3. Genel Türkçe korunuyor: final eşikleri (11. aşama, saklanan %70; taban çizgisi `hazir`)

Bölme kararı: her dosya, sabit seed (42) ile %30 geliştirme / %70 saklanan olarak ayrılır; her görevde geliştirme bölümü en az 50 kayıt olur. Bölme 02'de yapılacak. Aşağıdaki sayılar beklenen boyutlardır (`wc -l` × oran); kesin sayılar 02'de ölçülecek.

Bu bölümde **3.7 kritik**, diğerleri uyarı eşiğidir (§6).

| # | Ölçüt (saklanan kayıt) | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 3.1 | TurkishMMLU doğruluğu (630) | Fark ≥ −2,0 pp | 630 soruda tek bir oranın standart hatası yaklaşık 2 pp; aynı sorulardaki eşleştirilmiş farkta daha küçük (tahmin). 2 pp'den büyük düşüş gerçek kayıp sayılır | bekliyor |
| 3.2 | GECTurk chrF (350) | Fark ≥ −1,0 puan | chrF'de 1 puanın altındaki fark genellikle gürültüdür | bekliyor |
| 3.3 | XL-Sum chrF (350) | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.4 | WMT16 EN→TR chrF (350) | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.5 | Vikipedi perplexity (350) | Göreli artış ≤ %10 | Alana uyum küçük bir artış doğurabilir; %10 üstü dil dağılımında belirgin kayma demektir | bekliyor |
| 3.6 | Aya ikili karşılaştırması (175; yargıç, adaptör vs `hazir`) | Kaybetme − kazanma ≤ 10 pp | Genel yardımseverlikte belirgin gerileme kabul edilmez | bekliyor |
| 3.7 | **Kritik.** Üslup sızıntısı (gündelik sorular, `deney_plani_v1.md` §6.6, **gruba göre işaret listesi**: `a` için kurum adı/yönlendirme dahil, `b` için yalnızca kurum ağzı + bürokratik kalıp + resmî kip yoğunluğu; geliştirme: `genel_kontrol_v1` tamamı; saklanan: `genel_kontrol_v2`, karar 6a ve 6c) | Sızıntılı cevap **oranı** ≤ `hazir` oranı + 10 pp | 50 soruda yaklaşık 5 cevaplık artışa kadar tolerans; daha fazlası kurum dilinin gündelik kullanıma taştığını gösterir. Oran olarak yazıldı, böylece saklanan bölümün boyutundan bağımsız | bekliyor |
| 3.8 | Çoktan seçmelide harf çıkarılamayan cevap oranı | ≤ %3 | Daha yüksek oran 3.1'i biçim sorununa dönüştürür | bekliyor |
| 3.9 | `b_kurum_gayriresmi` bilgi doğruluğu (`genel_kontrol_v2`, 15 soru; yargıç, `deney_plani_v1.md` §6.3 ölçeği, referans = onaylı `bilgi_ogeleri`) | Kritik hatalı cevap sayısı ≤ `hazir` + 1 **ve** ortalama puan farkı ≥ −0,2 | Sade anlatım bilgi kaybı pahasına olmamalı (başarı ölçütü 2). 15 soruda tek bir kritik hata gürültü olabilir, ikincisi değildir. Ortalama puandaki 0,2'lik pay, 15 soruda yaklaşık 3 cevabın bir basamak düşmesine karşılık gelir. Onaylanmayan bilgi öğesi puanlamaya girmez | bekliyor |

**Karar 6c'den sonraki değişiklik (2026-11-23, onaydan önce):**
- 3.7'nin ölçütü `b` grubu için yeniden tanımlandı. 3.9 eklendi. T.7'ye aynı gruba göre ölçüt uygulanır.
- **Gerekçe:** kullanıcının v1 kontrolüne göre `b` grubu kurum işlemi soran ve sade anlatım bekleyen sorulardan oluşuyor. Bu sorularda kurum ve sistem adlarını yasaklamak doğru cevabı sızıntı sayardı. Yeni ölçüt yalnızca bürokratik kalıbı yasaklıyor, doğruluğu ise ayrıca ölçüyor (`deney_plani_v1.md` §6.6 ve karar 6c).
- Bu değişiklik dosya henüz onaylanmadan yapıldı ve hiçbir model puanlanmadı. Bu yüzden yeni bir sürüm dosyası açılmadı. Onaydan sonraki değişiklikler `esikler_v2.md` ile yapılır.

## 3A. "Gerekirse karışım" tetikleyicisi (doğrulama aşaması, geliştirme %30; taban çizgisi `hazir`)

Karar (kullanıcı, 2026-11-23): genel Türkçe verisi eğitime **yalnızca** aşağıdaki tetikleyici çalışırsa girer.

**Ne zaman ölçülür:** doğrulamada SSS tarifi seçildikten sonra (`sss_adaptor` veya `sss_sentetik_adaptor`), **bir kez**. O adaptör ve `hazir`, Türkçe değerlendirmenin geliştirme bölümünde aynı ayarlarla çalıştırılır. Tetikleyiciyi aşmamak için ayar değiştirip yeniden ölçmek yasaktır; ölçüm yinelenirse bu rapora yazılır.

**Kural:** aşağıdaki T satırlarından **en az biri** aşılırsa `genel_karisim_adaptor` eğitilir. Hiçbiri aşılmazsa genel Türkçe verisi eğitime girmez ve `genel_karisim_adaptor` oluşturulmaz.

| # | Ölçüt (geliştirme kaydı, beklenen) | İzin verilen en fazla düşüş (`hazir` taban çizgisine göre) | Senior onayı |
|---|---|---|---|
| T.1 | TurkishMMLU doğruluğu (270) | 2,0 pp (fark < −2,0 pp → tetikler) | bekliyor |
| T.2 | GECTurk chrF (150) | 1,0 puan | bekliyor |
| T.3 | XL-Sum chrF (150) | 1,0 puan | bekliyor |
| T.4 | WMT16 EN→TR chrF (150) | 1,0 puan | bekliyor |
| T.5 | Vikipedi perplexity (150) | göreli artış %10 | bekliyor |
| T.6 | Aya ikili karşılaştırması (75) | kaybetme − kazanma 10 pp | bekliyor |
| T.7 | **Gündelik sorularda üslup sızıntısı** (`genel_kontrol_v1`, 50 gündelik soru; gruba göre işaret listesi, `deney_plani_v1.md` §6.6). `b` doğruluğu v1'de yalnızca raporlanır, tetiklemez | sızıntılı cevap oranı `hazir` oranının en fazla **10 pp** üstünde olabilir | bekliyor |
| T.8 | Çoktan seçmelide harf çıkarılamayan cevap oranı | mutlak %3 | bekliyor |

**Neden final eşikleriyle aynı sayılar:** iki tür hatanın maliyeti eşit değil.
- **Yanlış alarm:** gürültü yüzünden tetikleyici gereksiz yere çalışırsa bedeli bir ek eğitim koşusudur.
- **Kaçırma:** gerçek gerileme kaçırılırsa test aşamasında geri dönüşü olmayan bir başarısızlık çıkar.

Geliştirme bölümü küçük olduğu için gürültü daha büyüktür, ama bu tetikleyiciyi kaba değil hassas yapar. Hassas olması istenen yön de budur.

**Tetiklendiğinde:**

| # | Kural | Senior onayı |
|---|---|---|
| K.1 | `genel_karisim_adaptor`, seçilen tarife genel Türkçe çiftleri eklenerek eğitilir. Genel Türkçe payı eğitim örneklerinin %10'u veya %20'si olur; ikisi de denenir ve seçim doğrulamada yapılır. Genel Türkçe çiftleri `egitim_sorulari.jsonl` sorularına üretilip onaylanmış cevaplardan oluşur | bekliyor |
| K.2 | Karışım adaptörü T.1–T.8'in hepsini geliştirme bölümünde geçerse **ve** doğrulamada üslup+jargon ikili karşılaştırmasında seçilen tarife göre kaybetme − kazanma ≤ 10 pp ise "seçilen adaptör" olur | bekliyor |
| K.3 | K.2 sağlanmazsa seçilen tarif değişmez, karışım adaptörü yine teste girer (ikincil sonuç olarak) ve durum rapora yazılır | bekliyor |

## 4. Tuzak ve kapsam dışı davranış

Bu bölümde **4.2 kritik**, diğerleri uyarı eşiğidir (§6).

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 4.1 | Tuzak başarısı (test aşaması, adet) | Adaptör ≥ `hazir_istemli` − 2 (ör. 22/28'e karşı en az 20/28) | Fine-tuning modelin "bilmiyorum" deme davranışını bozabilir. 28 soruda −1 toleransı, iki model eşitken bile sık yanlış alarm verir; −2 yanlış alarmı azaltırken gerçek kötüleşmeyi yakalama gücünü −3'ten belirgin biçimde yüksek tutar. Mutlak güvence kritik eşik 4.2'dir (2026-11-24, onaydan önce değişiklik; olasılıklar §8, değişiklik 2) | bekliyor |
| 4.2 | **Kritik.** Tuzak başarısı, mutlak alt sınır | ≥ 21/28 (%75) | Servise çıkacak bir model için asgari güven düzeyi. Hazır model bile altında kalırsa raporda ayrıca belirtilir. Yargıç kalibrasyondan kalırsa tuzak puanı insandan gelir (§9.2) | bekliyor |
| 4.3 | Geliştirme kapsam dışı seti (15) | ≥ 12/15; yalnızca geliştirme ölçüsü, final iddiası yok | Ayar seçerken erken uyarı vermesi için | bekliyor |

Puanın kaynağı (kullanıcı kararı, 2026-11-23):
- 4.1 ve 4.2'deki birincil tuzak puanı, `deney_plani_v1.md` §6.4'teki önceden kayıtlı başarı ölçütlerinden ve projenin kendi yargıç akışından gelir.
- Ham verideki `05_tuzak_sorular/otomatik_kontrol.py` ve `yargic_promptu.md` şimdi kullanılmaz. 11. aşamada en fazla ek kontrol olarak çalışabilir; bunun kararı 11'e kalır. Ek kontrolün sonucu birincil tuzak puanını değiştirmez ve ayrı raporlanır.

## 5. İkincil iddia: sentetik veri katkısı (test)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 5.1 | Üslup+jargon ikili karşılaştırması, `sss_sentetik_adaptor` vs `sss_adaptor` | Holm düzeltmesinden sonra iki yönlü işaret testinde p < 0,05. Test ailesi m = 3, §8 değişiklik 5 (kullanıcı kararı: seçenek A) | Ön kayıtlı ikincil iddia; birden fazla karşılaştırma yapıldığı için düzeltme gerekli | bekliyor |
| 5.2 | Bilgi ikili karşılaştırması aynı çift | Kaybetme − kazanma ≤ 10 pp | Sentetik veri bilgiyi bozmamalı | bekliyor |
| 5.3 | Kritik hata farkı aynı çift | ≤ +2 | Aynı | bekliyor |

Üç koşul da sağlanmazsa rapora "sentetik verinin katkısı gösterilemedi" yazılır.

## 6. Kritik ve uyarı eşikleri (2026-11-24, onaydan önce değişiklik)

### 6.1 Sınıflar

| Sınıf | Eşikler | Aşılırsa |
|---|---|---|
| **Kritik** | 2.1, 3.7, 4.2 | Birincil sonuç "kaldı" olur. 2.1 §2'deki iki karşılaştırmanın (`hazir` ve `hazir_istemli`) ikisinde de kritiktir |
| **Uyarı** | 2.1b, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8, 3.9, 4.1, 4.3 | Raporda kırmızı bayrakla gösterilir, §6.2'deki inceleme yapılır, nihai karar senior ile verilir |
| Sınıf dışı | §0 (0.1–0.5), §3A (T.1–T.8, K.1–K.3), §5 (5.1–5.3), 2.5 (eşik yok) | Kendi kuralları geçerlidir. T.1–T.8 bir karar kuralıdır ve bu ayrımdan etkilenmez |

"Kırmızı bayrak": rapordaki sonuç tablosunda eşiği aşan satır **KIRMIZI BAYRAK** etiketiyle ve ölçülen değer, eşik değeri ve inceleme dosyasının yoluyla birlikte gösterilir. Bayrak, inceleme sonucu ne olursa olsun raporda kalır.

### 6.2 Uyarı eşiği aşıldığında inceleme

**U.1 Ne zaman.** Eşiğin ölçüldüğü aşamada, o aşamanın bütün puanları üretilip commit edildikten **sonra**. Test eşikleri için 11. aşamada; 4.3 için doğrulama aşamasında ve test kilidinden önce. İnceleme hiçbir puanı, eşiği veya ayarı değiştirmez. İnceleme sonrasında yeniden ölçüm yapılmaz.

**U.2 Hangi kayıtlar.** Kayıtları bir betik seçer (seed 42) ve yalnızca kimlik yazar:

| Eşik türü | Eşikler | İncelenecek kayıtlar |
|---|---|---|
| Sayım farkı | 2.1b, 2.4, 3.9 (kritik hata koşulu), 4.1 | Adaptörde olumsuz olup karşılaştırılan sistemde olumsuz olmayan **bütün** kayıtlar. Ters yöndekilerin (adaptör lehine olanların) yalnızca sayısı yazılır |
| Mutlak oran | 3.8, 4.3 | Adaptörde olumsuz olan **bütün** kayıtlar |
| İkili karşılaştırma | 2.2, 3.6 | Adaptörün iki sırada da kaybettiği **bütün** kayıtlar |
| Ortalama farkı | 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.9 (ortalama koşulu) | Kayıt düzeyinde farkı en olumsuz **20** kayıt (eşitlikte seed 42 ile seçim) + kalan kayıtlardan seed 42 ile **10** rastgele kayıt. Rastgele kayıtlar, düşüşün birkaç kayıttan mı yoksa genelden mi geldiğini görmek için kontroldür |

- Bir eşik için en fazla 40 kayıt incelenir. Fazlaysa seed 42 ile 40 kayıt seçilir; toplam sayı ayrıca yazılır.
- §2'deki eşik hangi karşılaştırmada (`hazir` veya `hazir_istemli`) aşıldıysa o karşılaştırmanın kayıtları seçilir. İkisinde de aşıldıysa ikisi ayrı ayrı incelenir.

**U.3 Kim.**
- Kayıtları **insan değerlendirici** (proje sahibi) inceler ve her kayda neden etiketi koyar.
- Claude ve yargıç model inceleme kararı vermez. Test kayıtlarındaki metin yalnızca insan için üretilen CSV'de bulunur. Claude bu CSV'yi kendi okuyacağı biçimde açmaz; 11'deki bütün puanlar commit edildikten sonra yalnızca rapor örneği için okuyabilir.
- Nihai kararı **senior** verir.

**U.4 Nasıl kayda geçer.**
1. Betik `inceleme/uyari_<deney_id>_<esik>.csv` dosyasını üretir. Sütunlar: kimlik, eşik, seçilme nedeni (`en_olumsuz` / `rastgele` / `tamami`), otomatik ve yargıç puanları, soru, referans, iki sistemin cevabı. Doldurulacak sütunlar `neden` ve `not`.
2. `neden` şu değerlerden biridir:
   - `gercek_kotulesme`: adaptörün cevabı gerçekten daha kötü.
   - `olcum_hatasi`: betik, yargıç veya harf çıkarma hatası; cevap aslında kötü değil.
   - `referans_sorunu`: referans eskimiş veya hatalı.
   - `belirsiz`.
3. Değerlendirici CSV'yi doldurur. Betik etiket dağılımını sayar.
4. İnceleme özeti `degerlendirme/uyari_inceleme_<deney_id>.md` dosyasına yazılır: eşik, ölçülen değer, eşik değeri, aşılan karşılaştırma, incelenen ve toplam kayıt sayısı, etiket dağılımı, değerlendiricinin kısa yorumu.
5. CSV ve özet, senior kararından **önce** `11: uyarı incelemesi <esik>` mesajıyla commit edilir. 4.3 için aynı adımlar doğrulama aşamasında yapılır.

**U.5 Senior kararı.** Özet dosyasının sonuna yazılır ve ayrı bir commit'le kaydedilir. İçeriği:
- Karar:
  - **(a) Birincil sonuç geçerli.** Uyarı rapora sınırlama olarak yazılır.
  - **(b) Birincil sonuç "kaldı".**
- Gerekçe (en az bir paragraf; etiket dağılımına atıfla).
- Onaylayan ve tarih.

Rapor, her uyarı eşiği için ölçülen değeri, inceleme özetini ve senior kararını birlikte gösterir.

**U.6 Bekleyen iş.** Kayıt seçme betiği (`src/degerlendirme/uyari_kuyrugu.py`) 11. aşamadan önce yazılacak. 4.3 kullanılacaksa doğrulama aşamasından önce yazılmalı.

## 7. Raporlama kuralı (2026-11-24, onaydan önce değişiklik)

**R.1** Bütün ikili karşılaştırmalarda kazanma oranı **hiçbir zaman tek başına yazılmaz**. Kapsam: 1.1, 2.2, 3.6, 5.1, 5.2, T.6, K.2, §3'teki ikincil karşılaştırmalar ve sonradan raporlanan her ikili karşılaştırma. Her seferinde şunlar birlikte verilir:
- **kazanma / beraberlik / kayıp** sayıları; beraberliğin kaçının "eşit" kararı, kaçının sıra tutarsızlığı olduğu parantez içinde;
- iki yönlü işaret testinin **p değeri** (beraberlikler hariç);
- Holm ailesindeki testlerde ayrıca düzeltilmiş p değeri.

Örnek (uydurma): "kazanma / beraberlik / kayıp = 58 / 12 / 30 (beraberlik: 7 eşit, 5 sıra tutarsız); iki yönlü işaret testi p = 0,004."

Bu kural tablolar, grafikler, özet cümleler ve sunum için de geçerlidir. Oran yazılabilir, ama yalnızca bu sayıların yanında.

## 8. Onaydan önce değişiklikler (2026-11-24, kullanıcı kararları)

Dosya henüz onaylanmadı ve hiçbir model puanlanmadı. Bu yüzden değişiklikler yeni sürüm dosyası açılmadan bu dosyaya işlendi. Önceki hâl git geçmişindedir (`7bb442d`). Olasılıkları `python -m src.degerlendirme.esik_olasiliklari --cikti degerlendirme/esik_olasiliklari_v1.json` hesapladı; tam olasılık hesabıdır, veri kullanmaz. Aşağıda "ölçüldü" yazan sayılar bu betikten gelir.

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

**Değişiklik 3: yargıç kalibrasyonu 40 çift (0.3, 0.5; `deney_plani_v1.md` §6.8, §6.9; `rapor/rapor_plani_v1.md` §4).**
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

**Değişiklik 5: Holm ailesinin tanımı (5.1). KARAR (kullanıcı, 2026-11-24): seçenek A.**

- Gerekçe (kullanıcı): üç ikincil iddiada düzeltmesiz toplam yanlış iddia riski yaklaşık %14; düzeltmenin bedeli 5.1 için 61 yerine en fazla 63 galibiyet. Ölçüldü: 1 − 0,95³ = %14,3 (bağımsızlık varsayımıyla); 100 kesin kararda 61–63 galibiyet. Kullanıcının sayılarıyla aynı.
- **Aile (m = 3, sabit).** 11. aşamada test setinde, yargıcın **üslup+jargon** ikili karşılaştırması üzerindeki üç iki yönlü işaret testi:
  - H1: `sss_sentetik_adaptor` vs `sss_adaptor` (5.1)
  - H2: `hazir_istemli` vs `hazir` (istemin katkısı, `deney_plani_v1.md` §3, ikincil 2)
  - H3: seçilen adaptör vs `hazir` (ikincil 3)
- **Aileye girmeyenler:**
  - 1.1, tek birincil uç nokta; düzeltmesiz α = 0,05.
  - Eşik biçimindeki ölçütler (2.2, 3.6, 5.2, 5.3, K.2 vb.); bunlar hipotez testi değildir.
  - Bilgi ikili karşılaştırmalarının p değerleri. Bilgi testleri "kötüleşme yok" eşikleriyle yönetilir.
  - `genel_karisim_adaptor`'ün K.3 kapsamındaki karşılaştırmaları. Bu adaptörün oluşup oluşmayacağı önceden bilinmiyor; aile boyutu sonuca bağlı olmasın diye bunlar düzeltmesiz ve "keşif" etiketiyle raporlanır.
- **Bedeli (ölçüldü):** Holm'da 5.1'in sınırı, ailedeki sırasına göre 0,0167 ile 0,05 arasında değişir. 100 kesin kararda bu, düzeltmesiz 61 yerine **61–63** galibiyet demektir. 80 kararda 50 yerine 50–52.
- **Seçenekler:**

| Seçenek | Aile | 5.1 için Holm sınırı | 100 kararda gereken galibiyet (ölçüldü) |
|---|---|---|---|
| **A (seçildi)** | H1–H3, m = 3 | 0,0167–0,05 | 61–63 |
| B | Yalnızca H1 (m = 1, düzeltme yok). Gerekçe: ön kayıtlı tek ikincil iddia 5.1'dir; H2 ve H3 betimsel raporlanır. `deney_plani_v1.md` §3'teki "Holm uygulanır" cümlesi değişmeli | 0,05 | 61 |
| C | H1–H3 × (üslup+jargon, bilgi), m = 6 | 0,0083–0,05 | 61–64 |

- Neden A (öneri gerekçesi, kullanıcı kabul etti): plan §3, ikincil karşılaştırmalarda Holm'u zaten öngörüyor; H2 ve H3 rapora "istem işe yaradı" ve "adaptör hazır modelden iyi" diye iddia olarak girecek sonuçlardır. Bilgi karşılaştırmaları ise "kötüleşme yok" sorusunu sorar ve eşikle ele alınır.

**Bu değişikliklerle açığa çıkan sorular (2026-11-24'te kullanıcı kararıyla kapatıldı; değişiklik 6–8):**
1. **2.1b ile kritik 2.1.** → Kapandı: değişiklik 6. 2.1b'deki "2.1 ile çelişirse insan kararı geçerlidir" cümlesi değiştirilmedi. 2.1 artık kritik, 2.1b uyarı. 2.1 aşılır ama 2.1b geçerse, birincil sonuç "kaldı" mı olur, yoksa insan kararı kritik sonucu kaldırır mı, belli değil.
2. **Yargıca dayanan kritik eşikler.** → Kapandı: değişiklik 7. 2.1 (yargıç bilgi işaretleri) ve 4.2 (yargıç + otomatik kontrol) kritik oldu. Yargıç 0.3 veya 0.4'ü geçemezse bu iki kritik eşiğin nasıl ölçüleceği yazılı değil.
3. **Kalibrasyon çiftleri ve istem ayarı.** → Kapandı: değişiklik 8. `deney_plani_v1.md` §6.8 madde 6'ya göre kalibrasyon çiftleri istem ayarında kullanılmaz. 40 çift, 100 soruluk doğrulama setinin 40 sorusuna denk gelebilir. Bu kural soruları mı kapsıyor, yalnızca çiftleri mi, netleştirilmeli.

**Değişiklik 6: 2.1 ile 2.1b (kullanıcı kararı, 2026-11-24).**
- Karar: insan kararı eşiğin sonucunu değil, **kayıt düzeyindeki etiketi** değiştirir. İnsanın puanladığı 50 soruda insanın "kritik hata var/yok" etiketi yargıcın etiketinin yerini alır; diğer 50 soruda yargıç + betik etiketi kalır. Kritik 2.1 bu birleşik etiketlerle hesaplanır (§9.1).
- 2.1b'deki "2.1 ile çelişirse insan kararı geçerlidir" cümlesi bu kuralla değiştirildi.
- Gerekçe: eski cümle bir uyarı eşiğinin (2.1b) kritik bir eşiğin (2.1) sonucunu kaldırmasına izin veriyordu. Yeni kural insanın üstünlüğünü korur, ama bunu tek tek kayıtlarda yapar; eşiklerin sınıfı değişmez.
- Uygulama için gereken ek (bu kararın sonucu): insan formunun bilgi bölümünde şu an "kritik hata var/yok" alanı yoktu; yalnızca Evet / Kısmen / Hayır soruluyordu. "Hayır" kritik hatayla aynı şey değildir (§6.3'te bilgi puanı 0 = "kritik hata var **ya da** ana hüküm yanlış"). Bu yüzden forma `deney_plani_v1.md` §6.3 tanımıyla ayrı bir "kritik hata var / yok" alanı eklendi (§6.9). 2.1b "Hayır" sayısıyla hesaplanmaya devam eder.
- Bu ekin kapsamı ve 2.1'in `hazir` karşılaştırmasındaki uygulaması için §9.1'deki not ve açık karar 21'e bakınız.

**Değişiklik 7: yargıç kalibrasyondan kalırsa yedek yol (kullanıcı kararı, 2026-11-24).** Kural §9.2'de. Gerekçe: 2.1 ve 4.2 kritik oldu ve ikisi de yargıca dayanıyordu; yargıç kalırsa nasıl ölçüleceği yazılı değildi. Kalibrasyon doğrulama aşamasında yapıldığı için yedek yolun gerekip gerekmediği 11. aşamadan önce bilinir; insan iş yükü önceden planlanabilir.

**Değişiklik 8: kalibrasyon soruları istem ayarından çıkarılmaz (kullanıcı kararı, 2026-11-24).**
- Doğrulamanın 100 sorusunun hepsi istem ayarında kullanılır; kalibrasyonun 40 sorusu da dahil. `deney_plani_v1.md` §6.8 madde 6 buna göre değiştirildi.
- Bedeli: aynı 40 soru hem yargıcı seçmek hem istemi ayarlamak için kullanılır; doğrulama sonuçları bu nedenle de iyimser olabilir. Final iddiası yalnızca kilitli testten gelir. Sınırlama `rapor/rapor_plani_v1.md` §4.4'e eklendi.

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
- **Not (uygulama yorumu, kullanıcı onayı bekliyor; açık karar 21):** insan formu yalnızca birincil çifti (seçilen adaptör, `hazir_istemli`) kapsar; `hazir` cevapları insanca etiketlenmez. 2.1'in `hazir` karşılaştırmasında adaptörün etiketleri insandan, `hazir`'ınkiler yargıçtan gelirse iki taraf farklı ölçüm aracıyla sayılmış olur. Bu yüzden şimdilik birleşik etiket yalnızca `hazir_istemli` karşılaştırmasında uygulanır; `hazir` karşılaştırmasında iki taraf da yargıç + betik etiketiyle sayılır.

### 9.2 Yargıç kalibrasyondan kalırsa (0.3 veya 0.4)

1. **Önce diğer aday.** Seçilen yargıç kalırsa diğer adayın kalibrasyon sonucuna bakılır. Geçtiyse o kullanılır. Ek ölçüm gerekmez: iki aday da aynı 40 çifti kalibrasyonda puanlamıştır (§0, `deney_plani_v1.md` §6.8 madde 2).
2. **İkisi de kalırsa:**
   - **4.1 ve 4.2:** 28 tuzak sorusunun adaptör ve `hazir_istemli` cevaplarını (56 cevap) insan puanlar. Model adları gizli, sıra karışık, anahtar ayrı dosyada (§6.9'daki körleme kuralları); ölçüt `deney_plani_v1.md` §6.4'teki önceden kayıtlı başarı tanımlarıdır. Otomatik kontrol ayrıca çalışır ve ayrı raporlanır; insan puanını değiştirmez. Eşikler değişmez (4.1: ≥ `hazir_istemli` − 2; 4.2: ≥ 21/28).
   - **Kritik 2.1:** yalnızca insanın puanladığı 50 soru üzerinden, insanın "kritik hata var/yok" etiketiyle, **fark ≤ +2** eşiğiyle hesaplanır.
   - **1.1 / 1.2:** §1'deki kural geçerlidir: 1.2 tek başına birincildir, 1.1 "güvenilirliği düşük" notuyla raporlanır.
   - **Yargıca dayanan uyarı eşikleri** (2.2, 3.6, 3.9, 4.3, 5.2 ve tetikleyicide T.6, K.2) raporda "güvenilirliği düşük" notuyla gösterilir.
3. **1.1/1.2 kuralıyla tutarlılık (kontrol edildi):**
   - İki yol da aynı aracı kullanır: 11. aşamadaki 50 soruluk kör insan formu. Ek insan formu yalnızca tuzak için gelir.
   - 2.1'in yedek eşiği (+2 / 50 soru), 2.1b'nin 50 sorudaki toleransıyla aynıdır.
   - "Önce diğer aday" adımı `deney_plani_v1.md` §6.8 madde 4–5 ile uyumludur ("eşiği geçen adaylar arasında", "hiçbir aday geçemezse"). §1'deki cümle tekil "yargıç" dediği için bununla uyumlu olacak biçimde "iki aday da" diye düzeltildi.
   - Yedek yol kapsamadığı üç nokta bırakıyor (açık karar 21): 2.1'in `hazir` karşılaştırması insanla ölçülemez (form `hazir`'ı kapsamaz); 5.1 ve Holm ailesi tamamen yargıca dayanır; 3.9 (`b` grubu bilgi doğruluğu) yargıca dayanır ve kritik değildir.


Senior onayı (genel): bekliyor
Onaylayan / tarih: —
Onay commit'i: —
