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
| `turkishmmlu_dev` (45) | bölünmez | 5-shot örnek havuzu | — | Görev değil; iki bölümde de aynı 5-shot örnekleri kullanılır (açık karar 6) |
| `gecturk_test_500` (500) | 150 / 350 | Dilbilgisi düzeltme | chrF + tam eşleşme | |
| `xlsum_tr_test_500` (500) | 150 / 350 | Özetleme | chrF (ROUGE-L ikincil) | NC lisans: yalnızca iç değerlendirmede kullanılır |
| `wmt16_entr_test_500` (500) | 150 / 350 | EN→TR çeviri | chrF (BLEU ikincil) | |
| `vikipedi_perplexity_500` (500) | 150 / 350 | Genel metin | Perplexity | Sohbet şablonu ve sistem mesajı olmadan, ham metinde |
| `aya_eval_tr` (250) | 75 / 175 | Açık uçlu yardım | Yargıç ikili karşılaştırması (adaptör vs `hazir`) | Kazanma / beraberlik / kaybetme |
| `genel_kontrol_v1` (60) | **çakışma: %30 = 18 < 50** (açık karar 6) | Üslup sızıntısı | §6.6 | 35 gayriresmî + 15 kurum-samimi + 10 resmî |

- Kayıt sayıları `wc -l` ile ölçüldü. Bölme boyutları beklenen değerdir.
- Bölme kuralı (karar 2): her dosya sabit seed (42) ile %30 geliştirme / %70 saklanan olarak ayrılır; her görevde geliştirme bölümü en az 50 kayıttır. Alt grubu olan dosyalarda (ders, soru türü) bölme katmanlıdır.
- Bölmenin kendisi 02'de yapılır. Betik yalnızca kimlik, sayı ve SHA-256 yazar. Geliştirme bölümü yalnızca doğrulama aşamasında, saklanan bölüm yalnızca 11. aşamada kullanılır.

### 6.6 Üslup sızıntısı (gündelik sorularda kurum dili)

Ölçülen: gündelik sorulara gereksiz yere kurum diliyle cevap verilmesi.

- **Kapsam:** `genel_kontrol` setindeki gündelik sorular (v1'de 50: 35 gayriresmî + 15 kurum-samimi). 10 resmî soru kontrol grubudur; orada resmî dil beklenir ve yalnızca raporlanır. Geliştirme ve saklanan bölümler açık karar 6'ya bağlı.
- **Kullanım:** geliştirme bölümünde tetikleyici T.7, saklanan bölümde final eşiği 3.7 (`esikler_v1.md`).
- **Sızıntı işareti (otomatik):** bir cevapta aşağıdaki işaret listesinden **en az 2 farklı işaret** varsa o cevap "sızıntılı" sayılır:
  1. Kurum ağzı: "Kurumumuz", "Bakanlığımız", "Sayın".
  2. Mevzuat atfı: `\d{3,4} sayılı`, "ilgili mevzuat", "inci/ıncı/üncü/uncu madde".
  3. Kurum yönlendirmesi: soru bunu gerektirmediği hâlde "e-Devlet", "ALO 170", "il müdürlüğü", "resmî kaynaktan teyit".
  4. Resmî kip yoğunluğu: cümlelerin en az yarısı `-mektedir/-maktadır` ile bitiyor.
- **Ölçüt:** sızıntılı cevap oranı (yüzde) = sızıntılı / gündelik soru sayısı. Adaptörün oranı `hazir` modelin oranıyla karşılaştırılır.
- Bu işaret listesi eşik onayıyla birlikte dondurulur ve sonradan değiştirilmez.
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

Kararlar 1–5 kullanıcı tarafından 2026-11-23'te verildi. Açık karar 6 bu kararları işlerken ortaya çıktı.

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

Her dosya sabit seed (42) ile %30 geliştirme / %70 saklanan olarak bölünür; her görevde geliştirme bölümü en az 50 kayıttır. Ayrımın kendisi 02'de, yalnızca kimlik, sayı ve SHA-256 yazan bir betikle yapılır. Beklenen boyutlar §6.5'te. Kurala uymayan iki dosya için açık karar 6.

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

### Açık karar 6 (yeni): bölme kuralına uymayan iki dosya

Karar 2'deki iki koşul (%30 geliştirme ve geliştirmede ≥ 50 kayıt) iki dosyada birlikte sağlanamıyor:

| Dosya | Kayıt | Sorun |
|---|---|---|
| `genel_kontrol_v1` | 60 (35 gayriresmî + 15 kurum-samimi + 10 resmî) | %30 = 18 kayıt; 50 alt sınırının altında |
| `turkishmmlu_dev` | 45 | Görev değil, 5-shot örnek havuzu; bölünürse iki bölümde 5-shot örnekleri farklılaşır |

`genel_kontrol_v1` için seçenekler:

| Seçenek | Geliştirme / saklanan | Artı | Eksi |
|---|---|---|---|
| **Tümü geliştirme + yeni saklanan set (öneri)** | 60 / 0, saklanan karşılık: yeni `genel_kontrol_v2` (≥ 50 gündelik + 10 resmî) | İki bölüm de yeterince büyük; T.7 ve 3.7 anlamlı ölçülür | v2'nin yazılması gerekir. Önerim: v2'yi siz yazın ya da 02'de yazılıp hiçbir model cevabı görülmeden SHA-256 ile kilitlensin |
| 50 alt sınırı öncelikli | 50 / 10 (katmanlı) | Yeni veri gerekmez | Saklanan 10 soruda sızıntı oranı tek cevapla 10 pp oynar; 3.7 fiilen ölçülemez |
| %30 öncelikli | 18 / 42 | Oran kuralına uyar | 18 soruda T.7 tek cevapla 5,6 pp oynar; tetikleyici güvenilmez olur |

`turkishmmlu_dev` için önerim: bölünmesin. Yalnızca 5-shot örnek havuzu olarak iki bölümde de aynı biçimde kullanılsın (sabit 5 örnek, ders başına seed 42). Bu dosya puanlanmadığı için saklanan bölüme sızıntı yaratmaz.

Bu kararlar 02'deki bölme betiğinden önce verilmeli.

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
