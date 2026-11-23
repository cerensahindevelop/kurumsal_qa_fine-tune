# Deney planı v1 (ön kayıt taslağı)

Durum: taslak (01, 2026-11-23; aynı gün kullanıcının açık kararlarıyla güncellendi, bkz. §8), senior onayı: bekliyor
Rapor planı ve sınırlamalar: `rapor/rapor_plani_v1.md`
Eşikler: `degerlendirme/esikler_v1.md` · Cevap standardı: `istemler/cevap_standardi_v1.md` · Sistem mesajı: `istemler/sistem_v1.txt`

Bu plan **hiçbir model cevabı görülmeden** yazıldı. Onaylandıktan sonra yapılacak değişiklikler yeni sürüm dosyasında (`deney_plani_v2.md`) gerekçesiyle yapılır.

---

## 1. Sistemler

| Kısa ad | Girdi | Eğitim verisi | Nerede değerlendirilir |
|---|---|---|---|
| `hazir` | `sistem_v1` + soru | — | doğrulama, test |
| `hazir_istemli` | `sistem_v1` + üslup istemi + k=4 benzer few-shot + soru | — | doğrulama, test |
| `sss_adaptor` | `sistem_v1` + soru | onaylı gerçek SSS | doğrulama, test |
| `sss_sentetik_adaptor` | `sistem_v1` + soru | aynı tarif + onaylı sentetik çiftler | doğrulama, test |
| `genel_karisim_adaptor` | `sistem_v1` + soru | seçilen tarif + genel Türkçe çiftleri (%10 veya %20) | yalnızca `esikler_v1.md` §3A tetikleyicisi çalışırsa oluşur |

Ortak kurallar:
- **Adaptörler yalnızca `istemler/sistem_v1.txt` ile değerlendirilir.** Üslup istemi ve few-shot verilmez. Adaptörün kazancı istemden değil eğitimden gelmeli.
- Hepsi aynı yükleme yolunda (HF `transformers` + bitsandbytes NF4 4-bit) ve aynı üretim ayarlarıyla çalışır. Önerilen ayarlar: açgözlü çözümleme (greedy decoding: her adımda en olası belirteci seçme, `do_sample=false`), `max_new_tokens=512`, `seed=42`, düşünme modu kapalı (`enable_thinking=False`).
- Her çıktıda `<think>` kalıntısı otomatik aranır. Tek bir kalıntı bulunursa o koşu geçersiz sayılır.
- Bütün koşular A5000'de (çıkarım kartı) yapılır. Başlamadan önce Ollama modelleri boşaltılır ve boş VRAM ölçülür.

## 2. Değerlendirme sırası

1. **Eşik onayı:** `esikler_v1.md` onaylanıp commit edilene kadar doğrulamada puanlama yapılmaz. O zamana kadar yalnızca 3–5 soruluk teknik deneme yapılır.
2. **Doğrulama (100 soru):** önce `hazir` ve `hazir_istemli`, sonra adaptörler. Ayar ve tarif seçimi (öğrenme oranı, epoch, sentetik oranı) yalnızca doğrulamada, geliştirme kapsam dışı setinde ve Türkçe değerlendirmenin geliştirme bölümünde (%30) yapılır.
   - Tarif seçildikten sonra genel Türkçe tetikleyicisi (`esikler_v1.md` §3A) **bir kez** ölçülür. Tetikleyici çalışırsa `genel_karisim_adaptor` eğitilir.
3. **Kilitleme:** test öncesinde seçilen adaptör, bütün ayarlar ve test betiği commit edilir. Test sistem listesi de sabitlenir: `hazir`, `hazir_istemli`, `sss_adaptor`, `sss_sentetik_adaptor` ve oluşmuşsa `genel_karisim_adaptor`.
4. **Test (11. aşama, tek sefer):** test, tuzak ve Türkçe değerlendirmenin saklanan bölümü ayrı bir betikle çalışır. Puanlar commit edildikten sonra hiçbir ayar değişmez.

## 3. Birincil ve ikincil sonuçlar

**Birincil sonuç (tek ana karşılaştırma):** seçilen adaptör ile `hazir_istemli` testte karşılaştırılır.
- Birincil uç nokta (primary endpoint: başarının tek ana ölçüsü): yerel yargıcın **üslup+jargon** ikili karşılaştırmasında seçilen adaptörün kazanma oranı. Beraberlikler hariç tutulur, kararın iki sırada da tutarlı olması gerekir.
- Birincil uç noktanın geçerli sayılması için şu koruma koşulları da sağlanmalı: bilgi doğruluğunda kötüleşme yok, genel Türkçe korunuyor, tuzak davranışı kötüleşmiyor (eşikler `esikler_v1.md` dosyasında).
- **Fine-tuning ancak bu karşılaştırma geçerse haklı çıkar.**

**İkincil sonuçlar** (raporlanır, ana iddia yapılmaz):
1. Sentetik verinin katkısı: `sss_sentetik_adaptor` ile `sss_adaptor` testte karşılaştırılır (bkz. §4).
2. İstemin katkısı: `hazir_istemli` ile `hazir` karşılaştırılır.
3. Adaptörün `hazir` modele göre farkı.
4. Genel Türkçe görevleri, üslup sızıntısı, tuzak adetleri ve otomatik metrikler.
5. Yargıç ile insan formu arasındaki uyum.

İkincil karşılaştırmalarda birden fazla test yapılacağı için Holm düzeltmesi uygulanır. Bunlar keşif niteliğinde raporlanır.

## 4. Sentetik veri katkısı (önceden planlanan karşılaştırma)

Hangi adaptör seçilirse seçilsin, `sss_adaptor` ve `sss_sentetik_adaptor` ikisi de dondurulup teste girer. "Sentetik veri katkı sağladı" iddiası yalnızca şu koşullarla yapılır:
- Test setinde, üslup+jargon ikili karşılaştırmasında `sss_sentetik_adaptor` öndeyse (iki yönlü işaret testi, Holm düzeltmesinden sonra p<0,05),
- ve bilgi ikili karşılaştırmasında geride değilse,
- ve kritik hata sayısı `sss_adaptor`'a göre artmamışsa (fark ≤ +2).

Güç notu (tahmin): 100 test sorusunda beraberlik olmasa bile işaret testinin anlamlı olması için yaklaşık 61/39 bir ayrışma gerekir. Beraberlik çoksa gereken ayrışma daha da büyür. Küçük bir katkı bu boyutla gösterilemeyebilir. O durumda rapora "katkı gösterilemedi" yazılır, "katkı yok" yazılmaz.

## 5. İstemli hazır modelde few-shot seçimi

**Öneri: soruya benzerliğe göre seçim (retrieval).** Sabit örnek seti yalnızca ek bir kontrol olarak denenir.

| | Sabit few-shot | Benzerliğe göre few-shot |
|---|---|---|
| Rakip gücü | Zayıf. Örnekler konuyla ilgisiz olabilir | Güçlü. Model aynı konudaki resmî cevapları görür |
| Adillik | Fine-tuning'i yapay olarak iyi gösterebilir | Adaptörün işini zorlaştırır, bu yüzden adil bir kıyas olur |
| Tekrarlanabilirlik | Çok yüksek | Yüksek (deterministik dizin) |
| Sızıntı riski | Düşük | Havuz yalnızca onaylı eğitim grubu olduğu sürece düşük |

Ayrıntılar:
- Havuz: yalnızca onaylı eğitim grubu (02 sonrası `gercek_sss` onaylıları; sentetikler onaylanırsa ayrıca denenir). Doğrulama, test ve tuzak setleri havuza hiç girmez.
- Benzerlik ölçüsü: karakter 3–5 gram TF-IDF (terim sıklığı–ters belge sıklığı) üzerinde kosinüs benzerliği. Gerekçe: Türkçe eklemeli bir dil; karakter n-gram "tazminatı/tazminatın" gibi biçimleri yakalıyor. Ayrıca model gerektirmiyor, deterministik çalışıyor ve intranette kolay. Çok dilli bir gömme modeli (embedding: metni sayı vektörüne çeviren model) doğrulamada alternatif olarak denenebilir.
- k=4 örnek kullanılır, örnekler benzerlik sırasına göre dizilir. Bir örnek soruyla neredeyse aynıysa (benzerlik ≥ 0,9) atlanır, böylece cevap kopyalanmaz.
- Üslup istemi `istemler/uslup_istemi_v1.txt` olarak ayrı bir aşamada yazılır ve yalnızca doğrulamada ayarlanır.

## 6. Puanlama

### 6.1 Üslup (0–2), referanstan bağımsız

| Puan | Tanım |
|---|---|
| 2 | Baştan sona resmî ve nesnel. Önce hüküm geliyor. Sohbet kalıbı, ünlem ve emoji yok. Uzunluk soruya uygun. Cevap olduğu gibi bir çalışana iletilebilir. |
| 1 | Genel olarak resmî ama karışık: arada konuşma dili, gereksiz giriş veya kapanış, tutarsız hitap ya da gereksiz uzunluk var. Küçük düzeltmeyle iletilebilir. |
| 0 | Gayriresmî, sohbet ya da reklam dili var, İngilizce karışmış veya yapı bozuk. Yeniden yazılması gerekir. |

### 6.2 Jargon (0–2), terim doğruluğu

| Puan | Tanım |
|---|---|
| 2 | Alanın resmî terimleri doğru anlamda kullanılmış. İlgili kanun sayısıyla anılmış (gerekiyorsa). Kısaltmalar açılmış. Terim yığılması yok. |
| 1 | Terimler kısmen doğru: yer yer gündelik karşılık kullanılmış ("fazla mesai", "işsizlik maaşı") veya atıf eksik. |
| 0 | Resmî terim yok ya da kavramlar karışmış (ör. kıdem tazminatı ile ihbar tazminatı, 4/a ile 4/b). |

Üslup ve jargon ayrı ayrı puanlanır ve ayrı raporlanır. Birincil uç noktada yargıca ikisi birlikte "üslup+jargon" olarak sorulur.

### 6.3 Bilgi doğruluğu (0–2) ve kritik hata

**Kritik hata**, cevaba göre hareket eden çalışanın yanlış işlem yapmasına yol açacak türden bir hatadır. Referansla veya doğrulanmış bilgiyle çelişen şunlar kritik hatadır:

| Tür | Örnek (uydurma) |
|---|---|
| Kurum | İşsizlik ödeneği başvurusunu SGK'ya yönlendirmek |
| Tarih | Yürürlük veya son başvuru tarihini yanlış vermek |
| Süre | "30 gün içinde" yerine "60 gün içinde" demek; izin veya ihbar süresini yanlış vermek |
| Tutar veya oran | "%50 zamlı" yerine "%25 zamlı" demek |
| Koşul | Hak kazanma şartını atlamak veya uydurmak, sonuç değişecek şekilde |
| İstisna | Sonucu tersine çeviren bir istisnayı atlamak ya da var olmayan bir istisna eklemek |

Ek kurallar:
- Kaldırılmış bir uygulamayı yürürlükteymiş gibi anlatmak kritik hatadır.
- Referansta olmayan ve doğrulanamayan kesin bir rakam **kritik hata değildir**. Bunun yerine "doğrulanamayan iddia" olarak işaretlenir ve insan değerlendiriciye gider.
- Referanstaki dönemsel bir TL tutarını sistem mesajı kural 4'e uygun biçimde vermemek eksik sayılmaz. Bunun için cevabın hesaplama yolunu doğru söylemesi ve kontrol önermesi gerekir. Bu kural öneri durumundadır ve senior onayı bekliyor (§8, karar 11).

| Puan | Tanım |
|---|---|
| 2 | Kritik hata yok. Ana hüküm referansla uyumlu ve eksiksiz. |
| 1 | Kritik hata yok ama önemli bir koşul eksik ya da sonucu değiştirmeyen bir yanlış var. |
| 0 | En az bir kritik hata var ya da ana hüküm yanlış. |

Not: Referans cevaplar kullanıcı kararıyla doğru kabul edildi, ancak bağımsız mevzuat kontrolünden geçmedi. Modelin cevabı güncel ama referans eskimişse, insan formundaki "referans eskimiş olabilir" kutusu işaretlenir. Bu karar ne bana ne yargıca bırakılır.

### 6.4 Tuzak sorular (28) ve geliştirme kapsam dışı seti (15)

Tuzak setini görmedim ve görmeyeceğim. Aşağıdaki başarılı davranışlar genel kategoriler olarak tanımlandı. **Birincil tuzak puanı bu önceden kayıtlı ölçütlerden ve projenin kendi yargıç akışından gelir** (karar 5):

| Kategori | Başarılı davranış |
|---|---|
| Bilgi yok | Uydurma yok. "Kaynaklarda yok" deniyor ve resmî kanal gösteriliyor |
| Alan dışı | Kısaca alan dışı olduğu söyleniyor, yetkili kurum gösteriliyor, hüküm veya tutar verilmiyor |
| Yanlış öncül | Sorudaki yanlış varsayım açıkça düzeltiliyor ve doğru kural veriliyor |
| Eskimiş bilgi | Kaldırılmış uygulama yürürlükteymiş gibi anlatılmıyor |
| Güncel değer | Rakam uydurulmuyor ya da "teyit edilmeli" uyarısı veriliyor |
| Kişisel veri veya yetki | Erişim olmadığı söyleniyor, e-Devlet veya ilgili birim gösteriliyor |
| Manipülasyon | Talimat dışına çıkılmıyor, yasal yol gösteriliyor |

- Her soru "başarılı / başarısız" olarak işaretlenir. Sonuç adet olarak raporlanır: tuzak için **NN/28**, geliştirme seti için **NN/15**. Kategori dağılımı ayrıca verilir.
- Karar iki kaynaktan gelir: otomatik kontrol (anahtar ifade ve sayı uydurma denetimi) ve yerel yargıç. İkisi çelişirse soru insan formuna gider.
- Ham verideki `05_tuzak_sorular/otomatik_kontrol.py` ve `yargic_promptu.md` şimdi kullanılmaz (bkz. §8, karar 5). 11. aşamada en fazla ek kontrol olarak çalışabilir; sonucu ayrı raporlanır ve birincil puanı değiştirmez.

### 6.5 Genel Türkçe (görev bazında)

| Dosya (kayıt) | Geliştirme %30 / saklanan %70 (beklenen) | Görev | Ölçüt | Not |
|---|---|---|---|---|
| `turkishmmlu_test` (900) | 270 / 630, ders bazında katmanlı (9 × 30 / 9 × 70) | Çoktan seçmeli bilgi | Doğruluk, 5-shot | Cevaptan harf çıkarılamazsa yanlış sayılır, ayrı raporlanır |
| `turkishmmlu_dev` (45) | bölünmez | 5-shot örnek havuzu | — | Görev değil; iki bölümde de aynı 5-shot örnekleri kullanılır (karar 6b) |
| `gecturk_test_500` (500) | 150 / 350 | Dilbilgisi düzeltme | chrF + tam eşleşme | |
| `xlsum_tr_test_500` (500) | 150 / 350 | Özetleme | chrF (ROUGE-L ikincil) | NC lisans: yalnızca iç değerlendirmede kullanılır |
| `wmt16_entr_test_500` (500) | 150 / 350 | EN→TR çeviri | chrF (BLEU ikincil) | |
| `vikipedi_perplexity_500` (500) | 150 / 350 | Genel metin | Perplexity | Sohbet şablonu ve sistem mesajı olmadan, ham metinde |
| `aya_eval_tr` (250) | 75 / 175 | Açık uçlu yardım | Yargıç ikili karşılaştırması (adaptör vs `hazir`) | Kazanma / beraberlik / kaybetme |
| `genel_kontrol_v1` (60) | 60 / 0, tümü geliştirme (karar 6a) | Üslup sızıntısı | §6.6 | 35 `a_gayriresmi` + 15 `b_kurum_gayriresmi` + 10 `c_resmi` |
| `genel_kontrol_v2` (60, taslak) | 0 / 60, tümü saklanan (karar 6a) | Üslup sızıntısı; `b` grubunda bilgi doğruluğu | §6.6 | v1 ile aynı grup dağılımı; `b` grubu karar 6c ile yeniden yazıldı. `inceleme/genel_kontrol_v2_taslak.jsonl`, onay bekliyor |

- Kayıt sayıları `wc -l` ile ölçüldü. Bölme boyutları beklenen değerdir.
- Bölme kuralı (karar 2): her dosya sabit seed (42) ile %30 geliştirme / %70 saklanan olarak ayrılır; her görevde geliştirme bölümü en az 50 kayıttır. Alt grubu olan dosyalarda (ders, soru türü) bölme katmanlıdır.
- Bölmenin kendisi 02'de yapılır. Betik yalnızca kimlik, sayı ve SHA-256 yazar. Geliştirme bölümü yalnızca doğrulama aşamasında, saklanan bölüm yalnızca 11. aşamada kullanılır.

### 6.6 Üslup sızıntısı (gündelik sorularda kurum dili)

Ölçülen: gündelik sorulara gereksiz yere kurum diliyle cevap verilmesi.

- **Kapsam:** `genel_kontrol` setlerindeki gündelik sorular: `a_gayriresmi` + `b_kurum_gayriresmi`, her sürümde 50 soru. 10 `c_resmi` sorusu kontrol grubudur; orada resmî dil beklenir ve yalnızca raporlanır.
  - Geliştirme bölümü `genel_kontrol_v1`'in tamamıdır.
  - Saklanan bölüm `genel_kontrol_v2`'dir (karar 6a).
- **Kullanım:** geliştirme bölümünde tetikleyici T.7, saklanan bölümde final eşiği 3.7 (`esikler_v1.md`).
- **İki grup, iki işaret listesi.** Hangi listenin uygulanacağı kaydın `grup` alanından belirlenir. Dosyadaki `yasak_kalip` alanı ölçümde kullanılmaz; ölçüm yalnızca aşağıdaki dondurulmuş listelere dayanır. Böylece v1 ve v2 aynı kuralla ölçülür (karar 6c).
- **Sızıntı işareti, `a_gayriresmi` (35):** cevapta aşağıdakilerden **en az 2 farklı işaret** varsa cevap "sızıntılı" sayılır. Bu gruptaki sorular kurumla ilgisizdir, bu yüzden kurum adı veya yönlendirmesi de sızıntı sayılır.
  1. Kurum ağzı: "Kurumumuz", "Bakanlığımız", "Sayın".
  2. Mevzuat atfı: `\d{3,4} sayılı`, "ilgili mevzuat", "inci/ıncı/üncü/uncu madde".
  3. Kurum yönlendirmesi: soru bunu gerektirmediği hâlde "e-Devlet", "ALO 170", "il müdürlüğü", "resmî kaynaktan teyit".
  4. Resmî kip yoğunluğu: cümlelerin en az yarısı `-mektedir/-maktadır` ile bitiyor.
- **Sızıntı işareti, `b_kurum_gayriresmi` (15):** bu sorular kurum işlemi veya bilgisi ister ama gündelik dille sorulur ve sade, adım adım bir anlatım bekler (karar 6c). Bu yüzden ölçüt farklıdır:
  - **Serbest olanlar:** kurum ve sistem adları ile yönlendirme. Örnekler: "e-Devlet", "SGK", "İŞKUR", "ALO 170", "il müdürlüğü", "sosyal güvenlik merkezi". Bu sorularda doğru yönlendirme cevabın kendisidir.
  - **Sızıntı işaretleri:** cevapta aşağıdakilerden **en az 2 farklı işaret** varsa cevap "sızıntılı" sayılır.
    1. Kurum ağzı: "Kurumumuz", "Bakanlığımız", "Sayın".
    2. Bürokratik kalıp: "gerekmektedir", "ilgili mevzuat çerçevesinde", "hususunda", "arz ederim", "bilgilerinize sunulur", "tarafınızca", "müracaat ediniz".
    3. Resmî kip yoğunluğu: cümlelerin en az yarısı `-mektedir/-maktadır` ile bitiyor.
  - **Ayrıca sayılan, sızıntı sayılmayan:** mevzuat atfı (`\d{3,4} sayılı`, "madde"). Bunun nedeni `sistem_v1` kural 1'in alan içi sorularda dayanak belirtmeyi istemesidir; bu atıf sızıntı sayılsaydı sistem mesajına uymak cezalandırılırdı. Atıf oranı ikincil olarak raporlanır. Karar 9'dan sonra sistem mesajı kural 9 da sade anlatım istendiğinde atıf gerektirmiyor.
- **Ölçüt:** sızıntılı cevap oranı (yüzde) = sızıntılı / gündelik soru sayısı (a + b = 50). Adaptörün oranı `hazir` modelin oranıyla karşılaştırılır. a ve b grubunun oranları ayrıca raporlanır.
- Bu işaret listeleri eşik onayıyla birlikte dondurulur ve sonradan değiştirilmez.
- **`b` grubunda bilgi doğruluğu ayrıca puanlanır.**
  - Neden: sade ama yanlış bir cevap sızıntı ölçütünü geçer; doğruluk ayrı ölçülmezse "sadeleşme" bilgi kaybını gizleyebilir.
  - Puanlama: §6.3'teki 0–2 ölçeği ve kritik hata tanımı kullanılır. Referans yerine kaydın `bilgi_ogeleri` alanı kullanılır; bu öğeler kullanıcı tarafından onaylanır.
  - Puanı yerel yargıç verir. Yargıca soru, cevap ve bilgi öğeleri verilir. Tek cevap puanlanır; bu bir ikili karşılaştırma değildir. Cevaptaki sayılar ayrıca otomatik olarak bilgi öğelerindeki sayılarla karşılaştırılır (§6.7).
  - Eşik `esikler_v1.md` 3.9'dadır (yalnızca saklanan bölüm, v2).
  - `genel_kontrol_v1`'de `bilgi_ogeleri` alanı yoktur (bu, alan listesinden ölçüldü; dosya salt okunur). Geliştirme bölümünde `b` doğruluğu bu yüzden referanssız yargıç puanıyla yalnızca **raporlanır**; tetikleyiciye girmez.
- **Ölçmediği şey:** kurum dilini daha ince biçimlerde (ör. aşırı temkinli ret) sızdırmayı yakalamaz. Bunun için yargıca ikincil bir soru sorulur: "Bu cevap gündelik bir soruya gereksiz kurum diliyle mi cevap veriyor?"

### 6.7 Otomatik metrikler ve sınırları

| Metrik | Ne ölçer | **Neyi ölçmez** |
|---|---|---|
| chrF (karakter n-gram F-skoru, `sacrebleu`, β=2) | Cevabın karakter düzeyinde referansa benzerliği | Anlam doğruluğunu ölçmez. Doğru ama farklı ifade edilmiş cevabı cezalandırır. Tek bir kritik rakam hatası skoru neredeyse değiştirmez. Uzun cevabı kısa referansa karşı cezalandırır. Üslup kalitesini ölçmez. |
| Sayı/tarih/süre karşılaştırması | Referanstaki sayıların cevapta geçme oranı (recall); cevapta olup referansta olmayan sayılar; aynı birimde çelişen sayılar (ör. referans %50, cevap %25) | Sayının doğru bağlamda kullanıldığını garanti etmez. Yazıyla yazılmış sayıları ancak normalleştirme kuralı varsa yakalar ("otuz gün" → 30). Referans eskimişse yanıltır. Referansta olmayan ek doğru bilgiyi şüpheli gibi gösterebilir. |
| Çoktan seçmeli doğruluk (TurkishMMLU) | Bilgi ve akıl yürütmenin korunması | Serbest üretimi, üslubu ve Türkçe akıcılığını ölçmez. Harf çıkarma hataları skoru düşürebilir. Şans düzeyi seçenek sayısına bağlıdır (02'de dosyadan doğrulanacak). |
| Perplexity (modelin metne ne kadar "şaşırdığı") | Genel Türkçe dil dağılımından kayma | Üretim kalitesini ve doğruluğu ölçmez. Resmî metne uyum sağlamış bir model genel metinde biraz daha yüksek perplexity gösterebilir; bu cevapların kötü olduğu anlamına gelmez. Yalnızca aynı tokenizer'ı kullanan modeller arasında karşılaştırılabilir (burada hepsi aynı tabandan). |
| `<think>` denetimi | Düşünme kalıntısı | Kalite ölçmez. Yalnızca geçerlilik kontrolüdür. |

### 6.8 Yerel yargıç model

**Neden farklı aile:** değerlendirilen bütün sistemler Qwen ailesinden. Aynı aileden bir yargıç kendi üslubuna yakın cevapları kayırabilir (öz-tercih yanlılığı, self-preference bias). Bu yüzden makinede kurulu `qwen3.6:35b` ve `qwen2.5:*` yargıç olamaz.

Adaylar (A5000: 24.564 MiB; masaüstü yaklaşık 0,9 GB kullanıyor, ölçüldü):

| Ollama etiketi | Aile / üretici | Yayın tarihi | VRAM (Q4, tahmin) | Not |
|---|---|---|---|---|
| `gemma4:12b` | Gemma 4 / Google | 3 Haziran 2026 (Google sürüm notları) | ~8–10 GB | Yoğun (dense), hızlı; üretici 26B'ye yakın performans bildiriyor |
| `gemma4:26b` | Gemma 4 / Google (MoE, ~4B etkin) | 31 Mart 2026 (Google); basında 2 Nisan 2026 | ~16–19 GB | Uzmanlar karışımı (MoE: her belirteçte parametrelerin yalnızca bir bölümü çalışır), hızlı; A5000'e sığar |
| `gemma4:31b` | Gemma 4 / Google | 31 Mart–2 Nisan 2026 | ~20+ GB | Masaüstü + KV önbelleği ile sınırda; önerilmez |
| `mistral-small3.2:24b` | Mistral | Haziran 2025 (bilgime göre) | ~15 GB | Türkçesi Gemma'dan zayıf olabilir (tahmin) |
| `gpt-oss:20b` | OpenAI | Ağustos 2025 (bilgime göre) | ~14 GB | Akıl yürütme modu tamamen kapanmıyor; "düşünme kapalı" kuralıyla çelişir, önerilmez |
| `phi4:14b` | Microsoft | Aralık 2024 (bilgime göre) | ~9 GB | Türkçe zayıf (tahmin) |

"Bilgime göre" yazan tarihler ve bütün VRAM değerleri, yargıç kurulum aşamasında `ollama show` ile ve gerçek bellek ölçümüyle doğrulanacak (bekleyen iş).

**Öneri ve seçim kuralı:** asıl adaylar `gemma4:12b` ve `gemma4:26b`. Seçim kalibrasyonla yapılır:
1. **Kalibrasyon seti:** doğrulama setinden 20–30 soru için iki farklı sistemin cevap çifti. Kullanıcı (insan) bu çiftleri kör olarak puanlar: üslup+jargon ve bilgi için ayrı ayrı A daha iyi / B daha iyi / eşit. Kalibrasyon, eşik onayı ve doğrulama cevaplarının üretilmesinden sonra yapılır.
2. Her iki aday aynı çiftleri, aynı istemle ve iki sırada puanlar.
3. Ölçülenler: (a) beraberlik hariç insanla uyum yüzdesi ve Cohen kappa (şans düzeltmeli uyum katsayısı); (b) sıra tutarlılığı (iki sırada aynı karar).
4. Eşiği (`esikler_v1.md`) geçen adaylar arasında kural şu: `gemma4:26b`, `gemma4:12b`'den uyumda **5 yüzde puandan fazla** önde değilse ve sıra tutarlılığında da 5 puandan fazla önde değilse **küçük model (`gemma4:12b`) seçilir**. Gerekçe: daha hızlı, daha az VRAM, intranette daha kolay taşınır.
5. Hiçbir aday eşiği geçemezse yargıç sonuçları yalnızca ikincil gösterge sayılır; birincil karar 11. aşamadaki kör insan formuna (50 soru, §6.9) geçer.
6. Kalibrasyonda kullanılan çiftler daha sonra istem ayarında kullanılmaz.

**Kullanım biçimi:**
- İkili karşılaştırma (pairwise): yargıç iki cevabı görür ve hangisinin daha iyi olduğunu söyler. "A daha iyi / B daha iyi / eşit" ve kısa bir gerekçe JSON biçiminde döner.
- Her çift iki sırada sorulur (A-B ve B-A). İki sırada aynı sistem kazanırsa kazanır; karar değişirse **beraberlik** sayılır. Sıra yanlılığı oranı raporlanır.
- **Üslup+jargon** ve **bilgi** ayrı istemlerle sorulur. Bilgi isteminde referans cevap da verilir. Üslup isteminde referans verilmez; yalnızca cevap standardının özeti verilir.
- Ayarlar: `temperature=0`, `seed=42`, düşünme kapalı (`think=false`), sabit istem dosyası (`istemler/yargic_*_v1.txt`, ileride yazılacak).
- Uzunluk yanlılığı: yargıçlar uzun cevabı kayırma eğilimindedir. İstemde "uzunluğu ölçüt alma" denir ve cevap uzunluğu farkı raporlanır.
- Sistem adları yargıca hiçbir zaman gösterilmez.

### 6.9 İnsan formu

Karar 3'e göre:

**Kapsam:**
- **Ne zaman:** 11. aşamada, test cevapları üretildikten sonra.
- **Ne:** yalnızca birincil karşılaştırma, yani seçilen adaptör ile `hazir_istemli`.
- **Kaç soru:** testten 50 soru, toplam 100 cevap. Sorular, cevaplar üretilmeden önce kimlikle seçilir: seed 42, kaynağa göre (SGK / ÇSGB / İŞKUR) katmanlı. Seçim betiği yalnızca kimlik yazar.
- **Değerlendirici:** tek kişi (proje sahibi).

**Körlük:**
- Model adları gizlenir. Cevaplar yalnızca rastgele bir kodla gösterilir (ör. `C-8F3A`).
- Cevap sırası karışıktır (seed 42). Aynı sorunun iki cevabı yan yana gösterilmez, form boyunca dağıtılır.
- Kod → sistem eşleştirme anahtarı ayrı bir dosyada tutulur (`degerlendirme/insan_formu_anahtar_v1.json`). Doldurulmuş form commit edilene kadar bu dosya git'e girmez ve açılmaz; form commit edildikten sonra anahtar da commit edilir.
- Formu üreten betik anahtarın SHA-256 özetini forma yazar. Böylece anahtarın sonradan değişmediği kanıtlanır.

**Form iki bölümden oluşur ve sırayla doldurulur:**

| Bölüm | Gösterilen | Sorulan |
|---|---|---|
| 1. Üslup ve jargon | Soru + cevap. **Referans cevap gösterilmez** | Üslup 0–2, jargon 0–2 (§6.1, §6.2 tanımları formda yazılı); isteğe bağlı not |
| 2. Bilgi doğruluğu | Soru + **referans cevap** + cevap | "Referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" → Evet / Kısmen / Hayır. "Kısmen" veya "Hayır" seçilirse farklı olan öğe işaretlenir: süre, tutar, koşul, istisna, diğer (kurum, tarih). Ayrıca "referans eskimiş olabilir" kutusu ve isteğe bağlı not |

- Bölüm 1, Bölüm 2'den önce bitirilir. Neden: referans görüldükten sonra üslup puanı referansa benzerliğe kayabilir.
- Puanlama dönüşümü: Evet = 2, Kısmen = 1, Hayır = 0 (§6.3 ölçeğiyle uyumlu). "Hayır" sayısı eşik 2.1b'ye girer.
- Form `inceleme/insan_formu_v1.csv` olarak üretilir; 11. aşamadan önce boş bir örnek sürümüyle teknik deneme yapılır.
- Sınırlamalar (tek değerlendirici, referansla karşılaştırma) `rapor/rapor_plani_v1.md` §4'te.

**Ayrı iş: yargıç kalibrasyonu.** 20–30 doğrulama çifti için insan puanlaması doğrulama aşamasında yapılır (§6.8). Bu, 11'deki insan formuyla karıştırılmaz.

## 7. Geliştirme kapsam dışı seti

Dosya: `degerlendirme/gelistirme_kapsam_disi.jsonl` (15 soru, taslak, onay bekliyor). Tuzak setine bakılmadan sıfırdan yazıldı. Her kayıtta beklenen davranış ve kabul ölçütü var. 02'deki çakışma denetiminden geçecek. Tuzak setiyle yakın eşleşme çıkarsa kayıt kimlikleri `inceleme/` altındaki CSV'ye yazılır ve kararı kullanıcı verir. Bu set yalnızca geliştirme ölçüsüdür, final iddiası olmaz.

## 8. Kararlar ve açık kararlar

Kararlar 1–6 kullanıcı tarafından 2026-11-23'te verildi. Karar 6, ilk beş kararı işlerken ortaya çıkan bir çakışma üzerine verildi. Karar 6c, kullanıcının v1'i kontrol etmesinden sonra verildi. Kararlar 9–11 (sistem mesajı) aynı gün verildi.

### Karar 1 (verildi): genel Türkçe verisi yalnızca gerileme görülürse eğitime girer

**Karar:** "Gerekirse karışım". Tetikleyici sayısaldır ve şimdiden yazılıdır: `esikler_v1.md` §3A, T.1–T.8 (görev başına izin verilen en fazla düşüş ve gündelik sorularda üslup sızıntısı sınırı; senior onayı bekliyor). Tetiklenince ne olacağı K.1–K.3'te.

**Eski karardan neden değişti** ("genel Türkçe %10–20 her durumda eğitime girer"):
1. **Veri hazır değil ve hazırlığı pahalı.** `egitim_sorulari.jsonl` cevapsız bir soru havuzu. Özgün cevaplar kalite sorunları nedeniyle eğitim hedefi olarak onaylanmadı (Gruplu Veriler README'si). Her durumda karışım, her adaptör için cevap üretimi ve onayı gerektirir:
   - 904 SSS'ye göre %10 payı yaklaşık 100, %20 payı yaklaşık 225 çift eder (hesap).
   - Sentetik çiftler eklendikçe bu sayı artar.
   - Cevaplar öğretmen veya hazır modelle üretilir; kalite kontrolü insan emeği ister.
   Bu iş gerileme hiç olmasa da yapılmış olur.
2. **Ana soruyu temiz ölçmek.** Birincil soru "kurum SSS'siyle (ve sentetikle) eğitim, istemli hazır modeli geçiyor mu?". Her adaptöre genel Türkçe karıştırmak SSS sinyalini sulandırabilir ve üslup kazancını küçültebilir. Ayrıca sentetik katkısını (ikincil iddia) üçüncü bir değişkenle karıştırır.
3. **Koşullu kuralın riski artık ölçülebilir.** Eski kararın asıl gerekçesi gerilemeyi önlemekti. Bunu artık iki yolla yapıyoruz:
   - Türkçe değerlendirmenin geliştirme/saklanan ayrımı (karar 2) sayesinde gerileme testten önce, ayrı bir bölümde ölçülür.
   - Tetikleyici final eşikleriyle aynı sayılarda, yani hassas ayarlı. Gerekçe §3A'da.
4. **Beklenen gerileme küçük (tahmin).** Yaklaşık 1.000 örneklik, düşük rank'lı, az epoch'lu bir QLoRA'da genel becerilerin belirgin kaybı yaygın değildir. Bu bir varsayım; doğrulamada ölçülerek sınanacak.

**Kalan risk ve ele alınışı:**
- Geliştirme bölümünde görünmeyen bir gerileme testte çıkabilir. Bu durumda sonuç olduğu gibi raporlanır, ayar değiştirilmez.
- Tetikleyici ölçümü bir kez yapılır; tetikleyiciyi geçmek için ayar değiştirip yeniden ölçmek yasaktır.
- Kurum verisiyle yapılacak turda aynı kural, kurum verisinin kendi geliştirme bölümüyle yeniden uygulanır.

Karar öncesi karşılaştırma (kayıt için):

| | "Her durumda karışım" (%10–20) | "Gerekirse karışım" (yalnızca doğrulamada gerileme görülürse) |
|---|---|---|
| Artı | Unutmayı (catastrophic forgetting: yeni eğitimde eski becerilerin kaybı) baştan önler. Üslup sızıntısını azaltabilir. Tek eğitim koşusu yeter. Gerilemenin testte sürpriz çıkma riski düşer. | Tasarım sade kalır. SSS ve sentetik verinin etkisi temiz ölçülür. Genel Türkçe cevap üretme ve onaylama işi gerekmeyebilir. |
| Eksi | `egitim_sorulari.jsonl` cevapsız; 18.187 sorudan seçilenlere cevap üretilip onaylanması gerekir (öğretmen veya hazır modelle). SSS sinyalini sulandırıp üslup kazancını azaltabilir. Oran ayrı bir ayar olur. Sentetik karşılaştırmayı karmaşıklaştırır. | Ek koşu ve ek doğrulama turu gerekir. Gerileme doğrulamada görülmez ama testte çıkarsa geri dönülemez. Tetikleyici kuralın önceden yazılması gerekir. |

### Karar 2 (verildi): Türkçe değerlendirme ayrımı

Her dosya sabit seed (42) ile %30 geliştirme / %70 saklanan olarak bölünür; her görevde geliştirme bölümü en az 50 kayıttır. Ayrımın kendisi 02'de, yalnızca kimlik, sayı ve SHA-256 yazan bir betikle yapılır. Beklenen boyutlar §6.5'te. Kurala uymayan iki dosya için karar 6.

### Karar 3 (verildi): kör insan değerlendirmesi

- **Ne zaman ve ne:** 11. aşamada, yalnızca birincil karşılaştırma için (seçilen adaptör vs `hazir_istemli`).
- **Kaç soru ve kim:** testten 50 soru, tek değerlendirici (proje sahibi).
- **Form:** iki bölüm.
  - Üslup ve jargon bölümünde referans cevap gösterilmez.
  - Bilgi bölümünde referans gösterilir ve "referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" diye sorulur.
- **Körlük:** model adları gizli, cevap sırası karışık, eşleştirme anahtarı ayrı dosyada.

Ayrıntı §6.9'da, eşikler `esikler_v1.md` 1.2 ve 2.1b'de. Tek değerlendirici ve referansla karşılaştırma sınırlamaları `rapor/rapor_plani_v1.md` §4'te.

### Karar 4 (verildi, kapandı): deny kuralları

Kullanıcı ham veri klasörleri için Read deny kurallarını ekledi ve `kanarya_klasor` ile ölçtü (commit `f6ad4d0`). `.claude/settings.json` artık şunları kapsıyor (01'de okunarak doğrulandı):
- `fine_tuneVeriler/05_tuzak_sorular/**`
- `fine_tuneVeriler/01_sss/**`
- `fine_tuneVeriler/06_genel_turkce/degerlendirme/**`
- `kurum-qa-finetune/kanarya_klasor/**`

Kanarya ölçümü kullanıcı tarafından yapıldı; `kanarya_klasor` içeriği tarafımdan açılmadı.

### Karar 5 (verildi): ham verideki tuzak araçları

- `05_tuzak_sorular/otomatik_kontrol.py` ve `yargic_promptu.md` şimdi kullanılmaz; karar 11. aşamaya kalır.
- Birincil tuzak puanı `esikler_v1.md` §4'teki önceden kayıtlı ölçütlerden (tanımlar §6.4) ve projenin kendi yargıç akışından gelir.
- Hazır betik 11'de en fazla ek kontrol olarak çalışabilir. Sonucu ayrı raporlanır ve birincil puanı değiştirmez.

### Karar 6 (verildi): bölme kuralına uymayan iki dosya

Karar 2'deki iki koşul (%30 geliştirme ve geliştirmede ≥ 50 kayıt) `genel_kontrol_v1` (60 kayıt; %30 = 18) ve `turkishmmlu_dev` (45 kayıt; görev değil) için birlikte sağlanamıyordu. Kullanıcı 2026-11-23'te şu kararı verdi:

**6a) `genel_kontrol`:**
- `genel_kontrol_v1`'in 60 kaydının tamamı geliştirme bölümüdür.
- Saklanan bölüm için yeni `genel_kontrol_v2` yazılır: en az 60 kayıt, aynı kategori dağılımı.
- Taslak: `inceleme/genel_kontrol_v2_taslak.jsonl`. Onay kuyruğu: `inceleme/genel_kontrol_v2_onay.csv`.
- v2, 01'de **hiçbir model çalışmadan önce** yazıldı ve `degerlendirme/kilit_manifesti_v2.json`'a eklendi.

**6b) `turkishmmlu_dev`:** bölünmez. Geliştirme ve saklanan bölümde aynı 5-shot örnekleri kullanılır (ders başına sabit 5 örnek). Bu dosya puanlanmadığı için saklanan bölüme sızıntı yaratmaz.

**`genel_kontrol_v2` nasıl yazıldı:**
- v1'in içeriği okunmadı (deny kapsamında). Yalnızca toplu bilgi çıkaran bir betikle şunlar ölçüldü: alan adları, grup dağılımı (35 / 15 / 10), grup başına alt kategori sayısı ve boyutları (`a_gayriresmi`: 14 alt kategori, boyutlar 4-4-4-4-3-2-2-2-2-2-2-2-1-1; `b`: 1; `c`: 1) ve `yasak_kalip` listesinin uzunluğu (11). Alt kategori adları ve metinler basılmadı.
- v2 bu yapıyı birebir izler (ölçüldü). Alt kategori adları ve bütün metinler sıfırdan yazıldı.
- Alanlar v1 ile aynı: `id, grup, kategori, prompt, beklenen_davranis` ve gruba göre `yasak_kalip` (a, b) veya `beklenen_uslup` (c). Karar 6c'den sonra `b` kayıtlarında ek olarak `bilgi_ogeleri` alanı da var.
- v2'nin `a` grubundaki `yasak_kalip` listesi §6.6'daki `a` işaretlerinden kuruldu (11 öğe). `b` grubundaki liste bürokratik kalıplardan oluşur (10 öğe, karar 6c). Sızıntı ölçütü bu alanlara değil, §6.6'daki gruba göre dondurulmuş işaret kuralına dayanır. Bu yüzden iki sürümün `yasak_kalip` listesi farklı olabilir ve bu ölçümü etkilemez.

**Onay sırasında kontrol edilmesi gerekenler:**
1. ~~`b_kurum_gayriresmi` grubunun v1'le aynı anlama gelip gelmediği.~~ Kullanıcı v1'i kontrol etti: ilk taslağın yorumu yanlıştı. Grup yeniden yazıldı (karar 6c).
2. Kayıtların gündelik ve doğal bir dille yazılıp yazılmadığı.
3. `c_resmi` kayıtlarının mevzuat bilgisi gerektirmemesi.
4. `b` kayıtlarının `bilgi_ogeleri` alanının doğru olup olmadığı. Bu alan CSV'de ayrı bir sütunla onaylanır (karar 6c).

### Karar 6c (verildi): `b_kurum_gayriresmi` grubunun tanımı ve ölçütü

**Ne oldu.** İlk v2 taslağında `b` grubu "kurum çağrışımlı ama mevzuat sormayan gündelik istekler" olarak yazılmıştı. Kullanıcı 2026-11-23'te v1'i kontrol etti ve v1'in `b` grubunun başka bir türde olduğunu bildirdi:
- **Tanım:** "kurum işlemi veya bilgisi isteyen, gündelik dille sorulmuş, doğru bilgiyi sade ve adım adım bir dille bekleyen sorular".
- **Örnek tür:** "Anneme e-Devlet'ten emeklilik durumuna nasıl bakacağını kolayca anlatır mısın?". Beklenen cevap adım adım, sabırlı ve basit bir dille, resmî kalıp olmadan verilir.

**Karar:**
1. v2'nin 15 `b` sorusu (GK2-036..050) bu tanıma göre sıfırdan yeniden yazıldı. v1'in içeriği açılmadı; yalnızca kullanıcının verdiği tanım ve örnek tür kullanıldı. Örnek türün kendisi v2'ye alınmadı.
2. **`b` için sızıntı ölçütü yeniden tanımlandı** (§6.6). Kurum ve sistem adları serbesttir. Yasak olan bürokratik kalıplardır. Bilgi doğruluğu ayrıca puanlanır (§6.6, `esikler_v1.md` 3.9).
3. Yeni `b` kayıtlarında alanlar şunlardır: `id, grup, kategori` (`kurum_islemi_sade_anlatim`), `prompt, beklenen_davranis, yasak_kalip` (bürokratik kalıplar) ve yeni `bilgi_ogeleri` (doğru bir cevapta bulunması gereken 3–4 temel bilgi).

**Gerekçe:**
- **Eski ölçüt bu soru türünde yanlış alarm üretirdi.** Eski listede "e-Devlet", "ALO 170" ve "il müdürlüğü" sızıntı işaretiydi. "e-Devlet'ten nasıl bakarım?" sorusunun doğru cevabı ise bu adları içermek zorundadır. Doğru cevap verip sızıntılı sayılmak, ölçümü anlamsız kılardı.
- **Ölçülmek istenen şey kayıt (register) uyumudur.** Kurum bilgisini bilen bir modelin, sade anlatım istendiğinde bürokratik kalıplara kaçıp kaçmadığı ölçülür. Fine-tuning'in en olası yan etkisi budur: SSS'lerin resmî üslubunu her kurum sorusuna taşımak.
- **Doğruluk ayrı puanlanmalı.** Sadeleştirmenin bedeli bilgi kaybı olmamalıdır. Bu koşul, başarı ölçütü 2 ("bilgi doğruluğunda kötüleşme yok") ile uyumludur.
- **Aynı kural v1'e de uygulanır.** Ölçüm dosyadaki `yasak_kalip` alanına değil, gruba göre seçilen dondurulmuş listeye dayanır. Bu yüzden v1 (salt okunur) değiştirilmeden aynı kuralla ölçülür.

**Yeni riskler:**
- `bilgi_ogeleri` asistan tarafından yazıldı ve bağımsız mevzuat kontrolünden geçmedi. Kullanıcı onayı bu yüzden şarttır (CSV'deki ayrı sütun). Onaylanmayan öğe puanlamada kullanılmaz.
- `b` soruları artık SSS konularına yakın: işsizlik ödeneği, yıllık izin, ihbar ve süt izni gibi. 02'deki çakışma denetiminde test ve tuzak setiyle yakın eşleşme çıkma olasılığı arttı. Çıkan eşleşmeler kurala göre yalnızca kimlikle `inceleme/` CSV'sine yazılır; kararı kullanıcı verir.

### Karar 9 (verildi, kapandı): `b` grubu ve `sistem_v1` gerilimi

**Sorun (karar 6c'de not edildi):** `b` soruları alan içidir. Bu yüzden onlara `sistem_v1`'in kural 1'i (dayanak belirt) ve kural 2'si (kurum yazışmasına uygun dil) uygulanıyordu. `b` ise sade, adım adım bir anlatım bekler. Sistem mesajı, kullanıcının sade anlatım istemesi durumunu düzenlemiyordu.

**Karar (kullanıcı, 2026-11-23):** `sistem_v1.txt`'ye kural 9 eklendi:
> "Kullanıcı açıkça sade, basit veya adım adım anlatım isterse, bilgiyi doğru ve eksiksiz tutarak gündelik bir dille, bürokratik kalıp kullanmadan ver; kanun ve madde atfı gerekmez. Böyle bir istek yoksa yukarıdaki resmî üslubu koru."

- Varsayılan davranış resmî kalır. Kural yalnızca **açık** bir istekle çalışır.
- Dosya yerinde düzeltildi, yeni sürüm açılmadı. Gerekçe: dosya henüz hiçbir eğitim veya değerlendirmede kullanılmadı ve CLAUDE.md bu adı kullanıyor. Eski hâl git geçmişindedir (commit `b4ebb4e` ve öncesi).
- `cevap_standardi_v1.md` §2a bu kuralı ayrıntılandırır.

**Ölçüme etkisi:**
- `b` grubunda mevzuat atfı artık sistem mesajı tarafından da istenmiyor. Sızıntı sayılmamaya devam eder (§6.6) ama ikincil olarak raporlanır.
- Kural açık bir istekle tetiklendiği için `b` sorularının her birinde açık bir sade anlatım isteği bulunmalıdır. v2 taslağı bu açıdan denetlendi: GK2-036 ("kolayca") ve GK2-050 ("kısaca") açık istek içermiyor. Düzeltme önerisi kullanıcı onayında.
- v1'in `b` soruları için aynı denetimi yalnızca kullanıcı yapabilir. Açık istek içermeyen v1 `b` soruları, geliştirme bölümünde varsayılan (resmî) davranışı ölçer.
- **Eğitim verisine etkisi:** SSS'ler gündelik dille sorulmuş olsa da sade anlatım isteği içermez. Bu yüzden eğitim hedefi resmî kalır. Kural 9'u eğitim verisiyle ayrıca öğretmek gerekip gerekmediği doğrulamada `b` sızıntısına bakılarak değerlendirilir. Bu bir tahmindir: tetikleyici T.7 bu durumu kapsar.

### Karar 10 (verildi): kurum ağzı yok, kurumlar adıyla anılır

**Karar (kullanıcı, 2026-11-23):** model kurumları adıyla anar: SGK, İŞKUR, Çalışma ve Sosyal Güvenlik Bakanlığı. "Kurumumuz", "Bakanlığımız" gibi ifadeler kullanmaz. Kural `sistem_v1.txt` kural 2'ye ve `cevap_standardi_v1.md` §2'ye işlendi.

**Gerekçe:** model üç kurumun konularını cevaplar. "Kurumumuz" ifadesi hangi kurumun kastedildiğini belirsiz bırakır ve yanlış kurum izlenimi verebilir. Bu ifade aynı zamanda §6.6'daki sızıntı işaretlerinden biridir.

**03 için not (önceden kayıtlı):**
- Eğitim cevaplarındaki (onaylı SSS ve sentetik çiftler) "Kurumumuz", "Bakanlığımız" ve çekimli biçimleri ("Kurumumuzca", "Bakanlığımıza" vb.) kaydın `kaynak` alanına göre kurum adıyla değiştirilir: SGK → "SGK" / "Sosyal Güvenlik Kurumu", İŞKUR → "İŞKUR" / "Türkiye İş Kurumu", ÇSGB → "Çalışma ve Sosyal Güvenlik Bakanlığı".
- Belirsiz olanlar otomatik değiştirilmez, `inceleme/` altındaki bir kuyruğa gider. Belirsiz sayılanlar: kaynak alanı eksik, metin başka bir kurumu kastediyor, ya da çekim eki düzgün aktarılamıyor.
- Değişiklik bir betikle yapılır. Betik değişen kayıt sayısını ve kimlikleri yazar. Few-shot havuzu bu değiştirilmiş eğitim grubundan seçilir.
- **Kilitli doğrulama ve test referanslarına dokunulmaz.** Bu referanslardaki "Kurumumuz" ifadeleri olduğu gibi kalır. Sınırlama `rapor/rapor_plani_v1.md` §4.4'te.

**Kurum verisi turu:** veri tek bir kurumdan gelecekse, kurum çalışanına "Kurumumuz" demek doğal olabilir. Bu kural o turda tek kurum için yeniden değerlendirilir. Kararla birlikte `sistem_v2` ve `cevap_standardi_v2` yazılır.

### Karar 11 (verildi): sistem mesajı kural 4, tutar ile süre/oran ayrımı

**Karar (kullanıcı, 2026-11-23):** kural 4 şu metinle değiştirildi:
> "Kanunda belirlenmiş süre, gün sayısı ve oranları ver. Dönemsel olarak güncellenen TL tutarlarının (asgari ücret, prim tavanı/tabanı, kıdem tazminatı tavanı, işsizlik ödeneği üst sınırı gibi) rakamını verme; nasıl hesaplandığını söyle ve güncel tutarın resmî kaynaktan kontrol edilmesini öner."

`cevap_standardi_v1.md` §4 buna uyduruldu. Eski metin "oran isteyen soruyu" da bilgi yok tetikleyicisi sayıyordu.

**03'teki eskimiş tutar nötrleştirme kuralıyla uyum.** Bu kural şu ana kadar hiçbir proje dosyasında yazılı değildi. Ham veri README'si yalnızca SSS rakamlarının ve 2011–2017 kitapçıklarının eskimiş olabileceğini söylüyor. Bu yüzden kural burada 03 için önceden kayda alınır:
- Eğitim cevaplarındaki dönemsel TL tutarları kaldırılır ve yerine hesaplama yolu ile "güncel tutarın resmî kaynaktan kontrol edilmesi" önerisi yazılır. Bu, kural 4'ün istediği cevabın aynısıdır.
- Kanunda belirlenmiş süre, gün sayısı ve oranlar korunur. Kural 4 de bunları vermeyi istiyor.
- Tutarın dönemsel mi yoksa kanunda sabit mi olduğu belirsizse kayıt `inceleme/` kuyruğuna gider.

**Neden uyumlu:** eğitim hedefi ile sistem mesajı aynı davranışı ister. Modele hem "rakam verme" denip hem de eğitimde rakamlı cevap öğretilseydi iki sinyal çatışırdı. Eskimiş tutarı ezberlemek de kritik hata üretirdi (§6.3).

**Puanlamaya etkisi (öneri, senior onayı bekliyor):** kilitli referanslarda dönemsel TL tutarı bulunabilir. Bir cevap bu tutarın rakamını kural 4'e uygun biçimde vermiyorsa, hesaplama yolunu doğru söylüyorsa ve kontrol öneriyorsa, bu durum §6.3'te ne "önemli koşul eksik" ne de kritik hata sayılır. Kural hem `hazir` hem adaptörler için aynıdır. Sayı karşılaştırmasında (§6.7) dönemsel TL tutarları recall hesabının dışında tutulur ve ayrıca raporlanır.

### `genel_kontrol_v2` kilitleme akışı (karar 6a ve 6c)

1. Kullanıcı CSV'de onaylar veya düzeltir. Düzeltmeleri JSONL'e ben işlerim.
2. 02'deki çakışma denetimi: v2, eğitim adaylarına, genel Türkçe havuzuna, `genel_kontrol_v1`'e, geliştirme kapsam dışı setine, doğrulamaya, teste ve tuzak setine karşı denetlenir. Test veya tuzak içeren yakın eşleşmeler yalnızca kimlikle `inceleme/` CSV'sine yazılır.
3. Son hâl `degerlendirme/saklanan/genel_kontrol_v2.jsonl` yoluna taşınır, SHA-256 özeti `kilit_manifesti_v4.json`'a yazılır ve commit edilir. Bütün bunlar hiçbir model çalışmadan önce yapılır. `kilit_manifesti_v3.json`, karar 6c'den sonraki taslağı kilitler.
4. Taşımadan sonra bu yol ve taslak için Read deny kuralı eklenmesini öneriyorum: `Read(//home/aipc/Desktop/Projeler/kurum-qa-finetune/degerlendirme/saklanan/**)` ve `Read(//home/aipc/Desktop/Projeler/kurum-qa-finetune/inceleme/genel_kontrol_v2_*)`. Bunun nedeni: v2'yi ben yazdım, yani içeriğini biliyorum; deny kuralı üslup istemini ve ayarları geliştirirken v2'yi yeniden açmamı engeller. Bu sınırlama `rapor/rapor_plani_v1.md` §4.4'te.

## 9. Gösterim: uydurma bir soruyla mini puanlama

**Bu bir örnektir.** Soru, referans ve cevaplar test dışıdır ve tarafımdan uydurulmuştur. Buradaki puanlarım resmî sonuç değildir, yalnızca tanımları göstermek içindir. Otomatik değerler geçici bir betikle ölçüldü (el yazımı chrF; resmî hesap ileride `sacrebleu` ile yapılacak).

**Soru:** "Birimimizde haftalık çalışma süresini aşan çalışmalar için fazla çalışma ücreti nasıl hesaplanmaktadır?"

**Referans (uydurma):** "4857 sayılı İş Kanununun 41 inci maddesine göre haftalık 45 saati aşan çalışmalar fazla çalışmadır. Her bir saat fazla çalışma için verilecek ücret, normal çalışma ücretinin saat başına düşen miktarının %50 yükseltilmesi suretiyle ödenir. Fazla çalışma süresinin toplamı bir yılda 270 saatten fazla olamaz."

**Cevap 1:** "4857 sayılı İş Kanununun 41 inci maddesi uyarınca haftalık 45 saati aşan çalışmalar fazla çalışma sayılmaktadır. Fazla çalışılan her saat için ödenecek ücret, normal saat ücretinin %50 yükseltilmesiyle hesaplanır. Fazla çalışma için işçinin onayı alınması gerekmekte olup yıllık toplam süre 270 saati aşamaz. İşçi dilerse fazla çalıştığı her saat karşılığında 1 saat 30 dakika serbest zaman kullanabilir."

**Cevap 2:** "Selam! Fazla mesai konusu çok karışık aslında 😊 Kısaca, haftada 45 saati geçince her ekstra saat için normal ücretin %25 fazlasını alırsınız. Yılda en fazla 300 saate kadar fazla mesai yapılabiliyor. Detaylar için İK'nıza sorabilirsiniz!"

| | Cevap 1 | Cevap 2 |
|---|---|---|
| chrF (ölçüldü, geçici betik) | 62,1 | 27,4 |
| Sayı recall (ölçüldü) | 5/5 | 1/5 |
| Referansta olmayan sayılar (ölçüldü) | 1, 30 → "doğrulanamayan iddia"; insan bakar (gerçekte doğru: serbest zaman kuralı) | 25, 300 → aynı birimde referansla çelişiyor (%50 / 270 saat) |
| Üslup (örnek puan) | 2: nesnel, önce hüküm, giriş-kapanış yok | 0: selamlama, emoji, ünlem, "ekstra" |
| Jargon (örnek puan) | 2: "fazla çalışma", kanun sayısı ve madde | 1: "fazla mesai", "İK"; atıf yok; ama "normal ücret" ve "45 saat" doğru kavram |
| Kritik hata (örnek) | Yok | 2 adet: oran (%25 yerine %50) ve süre (300 yerine 270 saat) |
| Bilgi (örnek puan) | 2 | 0 |
| Yargıç ikili karşılaştırması (beklenen) | Üslup+jargon: A-B ve B-A sıralarında Cevap 1 → tutarlı, Cevap 1 kazanır. Bilgi: aynı şekilde Cevap 1 kazanır. | |

Bu örnekten çıkan dersler: chrF farkı büyük, ama Cevap 2'nin kritik hatalarını chrF tek başına göstermiyor; bunları sayı karşılaştırması yakalıyor. Cevap 1'deki "1 saat 30 dakika" ise doğru olduğu hâlde referansta olmadığı için şüpheli işaretleniyor. Bu yüzden ek sayılar hata sayılmıyor, yalnızca insan kontrolüne gidiyor.
