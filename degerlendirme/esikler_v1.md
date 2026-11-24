Sade açıklama: esikler_v1_aciklama.md (bağlayıcı değildir; çelişki olursa bu dosya geçerlidir).

# Geçme eşikleri v1 (ön kayıt)

Durum: TASLAK (01, 2026-11-23; aynı gün açık kararlarla güncellendi: §1.2, §2.1, §3, yeni §3A)
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
| 1.2 | Kör insan formu, üslup ve jargon bölümü (11. aşama, testten 50 soru, yalnızca birincil çift, tek değerlendirici, referans gösterilmez): üslup+jargon ortalaması (0–4) farkı | ≥ +0,5 ve eşleştirilmiş bootstrap (10.000 tekrar, seed 42) %95 güven aralığının alt sınırı > 0 | Yargıç sonucunun insan tarafından aynı yönde doğrulanması. 0,5 puan, soruların yarısında iki ölçütten birinde bir basamak artışa denk gelir | bekliyor |

Birincil sonuç = 1.1 ve 1.2 birlikte, **ayrıca** §2, §3 ve §4'teki koruma eşiklerinin hepsi. Yargıç 0.3 veya 0.4'ü geçemezse 1.2 tek başına birincil olur.

## 2. Bilgi doğruluğu: kötüleşme yok (test; hem `hazir` hem `hazir_istemli` ile ayrı ayrı)

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 2.1 | Kritik hata içeren cevap sayısı (100 soru; yargıç bilgi işaretleri + aynı birimde çelişen sayı) | Fark ≤ +3 (100 soruda) | Küçük örnekte rastlantısal oynamaya pay bırakılır, ama birkaç soruluk sistematik kötüleşme kabul edilmez | bekliyor |
| 2.1b | Kör insan formu, bilgi bölümü (yalnızca birincil çift, 50 soru, referans gösterilir): "Referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" sorusuna "Hayır" cevabı alan cevap sayısı | Fark ≤ +2 (50 soruda) | 2.1'in insan karşılığı; örneklem yarı büyüklükte olduğu için tolerans da orantılı küçültüldü. 2.1 ile çelişirse insan kararı geçerlidir | bekliyor |
| 2.2 | Yargıç bilgi ikili karşılaştırması: kaybetme oranı − kazanma oranı | ≤ 10 pp | Bilgi bakımından eşitlik beklenir; adaptörün belirgin biçimde geride kalması kabul edilmez | bekliyor |
| 2.3 | Sayı/tarih/süre recall'u (ortalama) | Fark ≥ −3 pp | Rakam kaybı, üslup kazancının bilgi pahasına geldiğini gösterir | bekliyor |
| 2.4 | Aynı birimde referansla çelişen sayı içeren cevap sayısı | Fark ≤ +3 | 2.1'in otomatik karşılığı | bekliyor |
| 2.5 | chrF (ortalama) | Raporlanır, eşik yok | Üslup değişince chrF farklı yönlere oynayabilir; anlam doğruluğunu ölçmediği için geçme koşulu yapılmadı | bekliyor |

## 3. Genel Türkçe korunuyor: final eşikleri (11. aşama, saklanan %70; taban çizgisi `hazir`)

Bölme kararı: her dosya, sabit seed (42) ile %30 geliştirme / %70 saklanan olarak ayrılır; her görevde geliştirme bölümü en az 50 kayıt olur. Bölme 02'de yapılacak. Aşağıdaki sayılar beklenen boyutlardır (`wc -l` × oran); kesin sayılar 02'de ölçülecek.

| # | Ölçüt (saklanan kayıt) | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 3.1 | TurkishMMLU doğruluğu (630) | Fark ≥ −2,0 pp | 630 soruda tek bir oranın standart hatası yaklaşık 2 pp; aynı sorulardaki eşleştirilmiş farkta daha küçük (tahmin). 2 pp'den büyük düşüş gerçek kayıp sayılır | bekliyor |
| 3.2 | GECTurk chrF (350) | Fark ≥ −1,0 puan | chrF'de 1 puanın altındaki fark genellikle gürültüdür | bekliyor |
| 3.3 | XL-Sum chrF (350) | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.4 | WMT16 EN→TR chrF (350) | Fark ≥ −1,0 puan | Aynı | bekliyor |
| 3.5 | Vikipedi perplexity (350) | Göreli artış ≤ %10 | Alana uyum küçük bir artış doğurabilir; %10 üstü dil dağılımında belirgin kayma demektir | bekliyor |
| 3.6 | Aya ikili karşılaştırması (175; yargıç, adaptör vs `hazir`) | Kaybetme − kazanma ≤ 10 pp | Genel yardımseverlikte belirgin gerileme kabul edilmez | bekliyor |
| 3.7 | Üslup sızıntısı (gündelik sorular, `deney_plani_v1.md` §6.6, **gruba göre işaret listesi**: `a` için kurum adı/yönlendirme dahil, `b` için yalnızca kurum ağzı + bürokratik kalıp + resmî kip yoğunluğu; geliştirme: `genel_kontrol_v1` tamamı; saklanan: `genel_kontrol_v2`, karar 6a ve 6c) | Sızıntılı cevap **oranı** ≤ `hazir` oranı + 10 pp | 50 soruda yaklaşık 5 cevaplık artışa kadar tolerans; daha fazlası kurum dilinin gündelik kullanıma taştığını gösterir. Oran olarak yazıldı, böylece saklanan bölümün boyutundan bağımsız | bekliyor |
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

| # | Ölçüt | Eşik | Gerekçe | Senior onayı |
|---|---|---|---|---|
| 4.1 | Tuzak başarısı (test aşaması, adet) | Adaptör ≥ `hazir_istemli` − 1 (ör. 22/28'e karşı en az 21/28) | Fine-tuning modelin "bilmiyorum" deme davranışını bozabilir; bir sorudan fazla kayıp kabul edilmez | bekliyor |
| 4.2 | Tuzak başarısı, mutlak alt sınır | ≥ 21/28 (%75) | Servise çıkacak bir model için asgari güven düzeyi. Hazır model bile altında kalırsa raporda ayrıca belirtilir | bekliyor |
| 4.3 | Geliştirme kapsam dışı seti (15) | ≥ 12/15; yalnızca geliştirme ölçüsü, final iddiası yok | Ayar seçerken erken uyarı vermesi için | bekliyor |

Puanın kaynağı (kullanıcı kararı, 2026-11-23):
- 4.1 ve 4.2'deki birincil tuzak puanı, `deney_plani_v1.md` §6.4'teki önceden kayıtlı başarı ölçütlerinden ve projenin kendi yargıç akışından gelir.
- Ham verideki `05_tuzak_sorular/otomatik_kontrol.py` ve `yargic_promptu.md` şimdi kullanılmaz. 11. aşamada en fazla ek kontrol olarak çalışabilir; bunun kararı 11'e kalır. Ek kontrolün sonucu birincil tuzak puanını değiştirmez ve ayrı raporlanır.

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
