# Geçme eşikleri v1: sade açıklama

**Bu belge bağlayıcı değildir.** Bağlayıcı metin `degerlendirme/esikler_v1.md`'dir. İki belge çelişirse `esikler_v1.md` geçerlidir. Buradaki eşik değerleri o dosyadan aynen alındı; hiçbiri değiştirilmedi.

**Okuyucu:** ML'de yeni bir yazılımcı ve onun senior'ı.
**Amaç:** her eşiğin arkasındaki sebep zincirini göstermek; hiçbir şey ezbere kalmasın.
**Örnekler hakkında:** bütün örnek sayılar ve sorular **uydurmadır**. Test, tuzak, doğrulama, `genel_kontrol` ve Türkçe değerlendirme setlerinden hiçbir soru veya sonuç kullanılmadı. Henüz hiçbir model puanlanmadı. Örneklerdeki p değerleri ve kappa değerleri, uydurma sayılar üzerinde formülle hesaplandı.

Kısaltmalar: **pp** = yüzde puan. **Fark** = adaptör eksi karşılaştırılan sistem. **Yargıç** = kalibrasyonla seçilen yerel yargıç model. Sistem adları için `CLAUDE.md`'deki tabloya bakın (`hazir`, `hazir_istemli`, `sss_adaptor`, `sss_sentetik_adaptor`, `genel_karisim_adaptor`).

---

## 1. Giriş

### Eşik nedir, neden önceden yazılır?

**Eşik** (threshold), bir sonucun "geçti" mi "kaldı" mı sayılacağını belirleyen sınırdır. Okuldaki geçme notu gibidir: "50 ve üstü geçer".

Bu notun sınavdan **önce** ilan edilmesi gerekir. Öğretmen kâğıtları okuduktan sonra geçme notunu belirlerse, bilerek ya da bilmeyerek sevdiği öğrenciyi geçirecek sınırı seçebilir. Bizde de aynı tehlike var. Sonuçları gördükten sonra eşik koyarsak, fine-tuning'in "başarılı" çıkacağı sınırı seçmeye kayarız. Buna **ön kayıt** (pre-registration) denir: ne ölçüleceği, nasıl ölçüleceği ve hangi sonucun başarı sayılacağı, hiçbir model cevabı görülmeden yazılır ve commit edilir. Git geçmişi, eşiğin sonuçlardan önce yazıldığının kanıtıdır.

Eşik sonradan değişebilir, ama gizlice değişemez. Yeni bir dosya (`esikler_v2.md`) açılır, gerekçe yazılır ve değişiklik raporda gösterilir.

### "Fine-tuning başarılı sayılması için ne olmalı?"

1. Ölçüm geçerli olmalı: düşünme kalıntısı yok, kesik cevap çok az, yargıç insana yeterince benziyor (§0).
2. Seçilen adaptör, üslup ve jargonda **istemli hazır modeli** (`hazir_istemli`) açıkça ve istatistiksel olarak anlamlı biçimde yenmeli (1.1).
3. Kör insan formu da aynı yönde bir gelişme görmeli (1.2).
4. Üç **kritik** koruma eşiğinin hiçbiri aşılmamalı: kritik hata sayısı (2.1), gündelik sorularda üslup sızıntısı (3.7), tuzak başarısının mutlak alt sınırı (4.2).
5. Diğer koruma eşikleri (bilgi, genel Türkçe, tuzak) **uyarı** eşiğidir. Biri aşılırsa sonuç kendiliğinden düşmez: aşan kayıtlar bir insan tarafından incelenir ve karar senior ile yazılı olarak verilir (§6).
6. İkili karşılaştırmaların hepsi "kazanma / beraberlik / kayıp" sayıları ve p değeriyle birlikte raporlanmalı; kazanma oranı tek başına yazılmaz (§7).

### Eşik türleri

| Tür | Hangi soruyu cevaplar? | Bölüm |
|---|---|---|
| Geçerlilik ön koşulu | Ölçüm aracımız sağlam mı, sonuçlara güvenebilir miyiz? | §0 |
| Birincil | Fine-tuning asıl amacına ulaştı mı (üslup ve jargonda belirgin gelişme)? | §1 |
| Koruma, kritik | Kazanç, kabul edilemeyecek bir zarar pahasına mı geldi? Aşılırsa birincil sonuç "kaldı" olur | 2.1, 3.7, 4.2 |
| Koruma, uyarı | Kazancın yanında incelenmesi gereken bir gerileme var mı? Aşılırsa insan incelemesi ve senior kararı | §2, §3, §4'teki diğerleri |
| Tetikleyici | Eğitime genel Türkçe verisi eklememiz gerekiyor mu? | §3A |
| İkincil | Sentetik veri ek bir katkı sağladı mı? (ana iddia değil) | §5 |

---

## 2. §0 Geçerlilik ön koşulları

**Bu bölüm neden var?** Bir termometre bozuksa, ölçtüğü ateşe bakarak hasta hakkında karar veremezsiniz. §0 termometreyi kontrol eder. Modelin iyi ya da kötü olduğuna dair hiçbir şey söylemez. Yalnızca "bu ölçüm sonuç olarak okunabilir mi?" sorusunu cevaplar. 0.1 ve 0.2 cevap üretim ayarını, 0.3–0.5 yargıcı denetler. Bu yüzden diğer bütün eşiklerden önce gelir.

### 0.1 `<think>` kalıntısı: 0 cevap

**Arka plan.** Qwen3 ailesi modeller iki biçimde çalışabilir. **Düşünme modu** (thinking mode) açıkken model, cevabı yazmadan önce `<think>` ve `</think>` etiketleri arasında kendi kendine bir ara metin üretir: "Önce şunu hesaplayayım, sonra şuna bakayım…". Düşünme modu kapalıyken doğrudan cevabı yazar. Bu mod sohbet şablonundaki (chat template: soruyu modelin beklediği biçime sokan kalıp) bir bayrakla seçilir: HF tarafında `enable_thinking=False`, Ollama tarafında `think=false`. Projede bu mod her yerde kapalıdır (ayrıntı hemen aşağıdaki ek bölümde).

**Ne yapılıyor.** Her koşunun bütün cevaplarında `<think>` veya `</think>` metni otomatik olarak aranır. Eşik: **0 cevap**. Tek bir cevapta bile bulunursa o koşu geçersiz sayılır ve puanlanmaz.

**Neden.**
1. Düşünme modunu kapatma kararı verdik (aşağıdaki ek bölüm).
2. Bayrak bir yerde unutulursa (ör. yeni bir betikte, yeni bir şablonda), model düşünme metni üretmeye başlar.
3. Bu sessiz bir hatadır: kod çökmez, yalnızca cevaplar uzar ve biçimi değişir.
4. Kalıntı rastgele bir olay değil, ayarın yanlış olduğunun işaretidir. Bir cevapta varsa, ayar bütün koşuda yanlıştır.
5. Bu yüzden eşik "az olsun" değil "hiç olmasın"dır: 0.

**Olmasaydı ne olurdu.** `sss_adaptor_v1` değerlendirilirken betikte şablon bayrağı unutulur. Adaptörün cevaplarının bir kısmı düşünme metniyle başlar. Yargıç bu cevapları "daha ayrıntılı" bulup kayırır, adaptör üslupta %70 kazanır. Biz bunu fine-tuning'in başarısı sanarız. Gerçekte fark eğitimden değil, iki sistemin farklı modda çalışmasından gelir.

**İşimize ne yarıyor.** Hazır model ile adaptörlerin aynı koşulda ölçüldüğünü garanti eder. İntranette betik Claude olmadan çalışacak; kontrol otomatik olduğu için orada da aynı hata yakalanır. Senior'a "bütün koşularda düşünme kalıntısı 0" diye tek satırlık bir geçerlilik kanıtı sunulur.

**Örnek (uydurma).**
- Geçti: 100 cevabın hiçbirinde `<think>` yok → koşu puanlanır.
- Kaldı: 100 cevabın 1'inde `</think>` var → koşu geçersiz. Ayar düzeltilir, koşu yeni sürüm numarasıyla (ör. `_v2`) baştan yapılır.

#### Ek: Düşünme modunu neden kapattık?

**Düşünme modu nedir, nerede işe yarar?** Model cevaptan önce bir "karalama kâğıdı" kullanır. Ara adımları yazmak, birbirine bağlı adımlardan oluşan işlerde doğruluğu artırabilir: çok adımlı hesap ("önce brüt, sonra kesinti, sonra net"), mantık bulmacaları, kod yazma ve hata ayıklama. Matematik sınavında işlem kâğıdı kullanmak gibidir.

**Bizim işimiz ne tür?** Kurum çalışanının sorusuna mevzuattaki bilgiyi doğru **hatırlamak** ve bunu kurumun resmî **üslubuyla** yazmak. Bu işlerin çoğu tek adımlıdır: "İhbar süresi ne kadar?" sorusunun cevabı bir hesap zinciri değil, bilinen bir kuraldır. Fine-tuning'den beklediğimiz kazanç da üslup ve jargondadır, akıl yürütmede değil.

**Kapatma nedenleri:**
1. **Eğitim verisinde düşünme metni yok.** SSS çiftleri yalnızca soru ve cevaptan oluşur. Düşünme açık bir şablonla eğitseydik, modele "düşünme bölümü boş" örnekleri ya da hiç olmayan bir bölüm öğretmiş olurduk. Eğitim biçimi ile kullanım biçimi ayrışırdı.
2. **Eğitim ve kullanım biçimi aynı olmalı.** Model hangi kalıpta eğitildiyse o kalıpta kullanılınca en iyi sonucu verir. Eğitim, değerlendirme, öğretmen üretimi ve servis aynı şablonu kullanırsa, ölçtüğümüz şey servisteki davranışın kendisi olur.
3. **Hız ve maliyet.** Düşünme metni cevaptan birkaç kat uzun olabilir. Bunun üç sonucu var:
   - Değerlendirmede beş sistem, birkaç set ve iki sıralı yargıç çalışacak; süre katlanır.
   - Servis tek bir A5000'de çalışacak; uzun üretim, aynı anda cevap verilebilecek kullanıcı sayısını düşürür.
   - İntranetteki donanım bizimkinden daha güçlü olmayabilir.
4. **Ölçümü kirletir.**
   - Sayı/tarih/süre karşılaştırması (2.3, 2.4) cevaptaki bütün sayıları tarar. Düşünme metnindeki ara sayılar ("belki 30 gündür… hayır, 60") yanlışlıkla "çelişen sayı" olarak sayılır.
   - Yargıç, uzun düşünme metnini görürse onu cevabın parçası sanabilir ve uzunluğu kayırabilir.
   - `max_new_tokens` sınırı (0.2) düşünme metniyle dolup asıl cevabı kesebilir.
5. **Kullanıcıya yanlış ara bilgi gösterme riski.** Düşünme metninde model yanlış bir ara hüküm yazıp sonra düzeltebilir. Servis bu metni gösterirse, çalışan yanlış ara bilgiyi doğru sanabilir. Kurum içi bir araçta bu kabul edilemez.

**Bedeli.** Birden fazla kuralı birleştirmeyi gerektiren sorularda doğruluk kaybı olabilir. Örnek tür (uydurma): "8 yıllık çalışanın hem kıdem tazminatı hesabı hem ihbar süresi ne olur?" Burada iki ayrı kural uygulanıp birleştirilmelidir. Düşünme modu bu tür sorularda yardımcı olabilirdi. **Bu kayıp ölçülmedi**; büyüklüğü bilinmiyor.

**İsteğe bağlı yan deney.** Kaybın büyüklüğünü ölçmek için şu deney yapılabilir: `hazir` model doğrulama setinde iki kez çalıştırılır, bir kez düşünme açık, bir kez kapalı. Doğruluk (bilgi puanı, kritik hata sayısı) ve süre karşılaştırılır. Bu deney **ana planda yok** ve sonucu hiçbir eşiği etkilemez. Yapılıp yapılmayacağına 06. aşamada karar verilecek. `PROJE_DURUMU.md`'de açık karar olarak kayıtlıdır. Not: düşünme açık koşu 0.1'i bilerek ihlal eder; bu yüzden ana sonuçlara karışmaması için ayrı bir deney kimliğiyle yürütülmesi gerekir.

### 0.2 Boş veya kesilmiş cevap: ≤ %2

**Arka plan.**
- **Token** (belirteç): modelin metni işlediği küçük parçalar. Bir kelime bir ya da birkaç token olabilir ("tazminatı" → "tazmin" + "atı" gibi). Türkçe eklemeli olduğu için kelime başına token sayısı İngilizceden yüksektir.
- **`max_new_tokens`**: modelin bir cevapta en fazla kaç yeni token üretebileceği. Projede önerilen değer 512. Model bu sınıra gelince cümlenin ortasında da olsa durur. Cevap "kesilmiş" olur.
- **Boş cevap**: modelin hiçbir şey ya da yalnızca boşluk üretmesi.

**Ne yapılıyor.** Bir koşudaki cevaplardan kaçının boş olduğu ve kaçının `max_new_tokens` sınırına dayandığı (üretilen token sayısı = 512) betikle sayılır. Eşik: oran **≤ %2**.

**Neden.**
1. Kesilmiş bir cevabın sonunda genellikle önemli bilgi vardır (istisna, koşul, başvuru yeri).
2. Kesik cevap düşük puan alır. Ama bu düşük puan modelin bilgisinden değil, bizim seçtiğimiz 512 sınırından gelir.
3. Kesik cevap çoksa, puanlar "model ne biliyor" değil "512 yeterli mi" sorusunu ölçmeye başlar. `esikler_v1.md` bunu "puanlar üretim ayarına bağlı hâle gelir" diye ifade ediyor.
4. Neden %2? 100 soruluk bir sette en fazla 2 cevap. Bu kadarı tek tük aşırı uzun cevaplara pay bırakır ve sonucu belirleyemez. Eğitim SSS cevaplarının 90. yüzdeliği 89 kelime (ölçüldü, 01); 512 token bunun birkaç katıdır. Normal bir cevabın sınıra dayanması beklenmez. Sınıra dayanmak çoğunlukla bir döngü (aynı cümleyi tekrar etme) belirtisidir.

**Olmasaydı ne olurdu.** Fine-tuning sonrası adaptör bazı sorularda aynı paragrafı tekrar etmeye başlar ve %9 cevabı kesilir. Bilgi puanı düşer, biz "fine-tuning bilgiyi bozdu" sonucuna varırız. Gerçek sorun ise bir tekrar döngüsüdür; ayrı teşhis edilip çözülmesi gerekir.

**İşimize ne yarıyor.** Kalite sorununu üretim ayarı sorunundan ayırır. İntranette farklı bir donanımda aynı ayar kullanıldığında da sonuçların karşılaştırılabilir kaldığını gösterir. Senior'a "puanlar kesilmeden etkilenmedi" diye sunulabilir.

**Örnek (uydurma).**
- Geçti: 100 cevaptan 1'i sınıra dayanmış (%1) → koşu puanlanır.
- Kaldı: 100 cevaptan 5'i sınıra dayanmış (%5) → koşu puanlanmaz. Önce nedeni (döngü mü, gerçekten uzun soru mu) incelenir.

### 0.3 Yargıç kalibrasyonu: insanla uyum ≥ %75 ve Cohen kappa ≥ 0,50

**Arka plan.**
- **Yargıç model** (LLM-as-a-judge): cevapları puanlamak için kullanılan ayrı bir dil modeli. Yüzlerce cevabı insanın tek tek okuması pahalıdır; yargıç bunu dakikalar içinde yapar. Projede yargıç Ollama üzerinde, **farklı bir aileden** (Gemma 4) seçilir. Neden farklı aile: değerlendirilen bütün sistemler Qwen; aynı aileden bir yargıç kendi üslubuna benzeyen cevapları kayırabilir.
- **İkili karşılaştırma** (pairwise comparison): yargıca aynı soruya verilmiş iki cevap gösterilir ve "hangisi daha iyi?" diye sorulur. Cevap: "A daha iyi / B daha iyi / eşit".
- **Kalibrasyon** (calibration): bir ölçüm aracının doğru sonuç verdiğini, bilinen bir ölçüyle karşılaştırarak sınamak. Bizde "bilinen ölçü" insanın kararıdır. Doğrulama setinden 40 cevap çifti hem insan (kör olarak) hem yargıç tarafından puanlanır. (İlk taslakta 20–30 çiftti; 2026-11-24'te kullanıcı kararıyla 40'a çıkarıldı.)
- **Uyum yüzdesi**: insanla yargıcın aynı kararı verdiği çiftlerin oranı. Beraberlikler hariç tutulur.
- **Cohen kappa** (κ): şansla oluşacak uyumu çıkardıktan sonra kalan uyumu ölçen katsayı. Formül: κ = (gözlenen uyum − şans uyumu) / (1 − şans uyumu). 1 tam uyum, 0 yazı-tura kadar uyum demektir.

**Ne yapılıyor.** Her yargıç adayı kalibrasyon çiftlerini puanlar. Beraberlik dışı çiftlerde insanla uyum yüzdesi ve kappa hesaplanır. Eşik: **uyum ≥ %75 ve kappa ≥ 0,50**. İkisi birden sağlanmalı. Ölçüm üslup+jargon ve bilgi istemleri için **ayrı ayrı** yapılır; bir aday bir istem türünde geçip ötekinde kalabilir (2026-11-24 tanımlandı; §9). Sağlanmazsa önce diğer adayın sonucuna bakılır; o geçtiyse o kullanılır. İki aday da kalırsa yargıç insan yerine geçemez, **ikincil göstergeye düşer** ve kritik eşikler için yedek yol işler (§9'daki "Yargıç kalibrasyondan kalırsa" bölümü).

**Neden.**
1. Sonuçların çoğu yargıçtan geliyor (1.1, 2.1, 2.2, 3.6, 3.9, 5.x).
2. Yargıç insandan farklı düşünüyorsa, ölçtüğümüz şey "insanın tercihi" değil "yargıcın tercihi" olur. Hedef kullanıcı insan olduğu için insanın tercihine yakın olmalıyız.
3. Uyum yüzdesi tek başına yanıltabilir. Örneğin insan çiftlerin çoğunda A'yı seçmişse, her zaman "A" diyen bir yargıç düşünmeden yüksek uyum alır. Kappa bu şans payını çıkarır.
4. Bu yüzden iki koşul birlikte: %75 "çoğunlukla aynı kararı veriyor", 0,50 "bu uyum şanstan değil".
5. Neden bu sayılar? %75, her dört karardan üçünde insanla aynı demektir; ikili seçimde şans düzeyi %50'dir. Kappa'da 0,41–0,60 aralığı yaygın olarak "orta düzey uyum" diye anılır (Landis ve Koch ölçeği). 0,50 bu aralığın ortasıdır ve "insan yerine kullanılabilir" için asgari bir düzey olarak seçildi.
6. Neden 40 çift? Az çiftle ölçülen bir uyum yüzdesi çok oynar. %75 uyumun %95 belirsizliği 25 çiftte yaklaşık ±17 pp, 40 çiftte ±13 pp (ölçüldü, `src/degerlendirme/esik_olasiliklari.py`). Yani 25 çiftte %75 ölçülen bir yargıcın gerçek uyumu %58 de olabilir, %92 de. 40 çift bu aralığı daraltır ama yok etmez. Uyum beraberlikler hariç hesaplandığı için etkin çift sayısı 40'tan azdır; %20 beraberlikte ±15 pp. Kappa için belirsizlik 40 çiftte de yaklaşık ±0,27'dir (kaba hesap).

**Olmasaydı ne olurdu.** Yargıç her zaman daha uzun cevabı seçiyor. Kalibrasyon yapmadan kullanırız. Adaptör daha uzun cevap verdiği için %68 kazanır. Raporda "üslup belirgin gelişti" yazarız. İnsanlar ise uzun cevapları "gereksiz uzun" bulup tercih etmiyor.

**İşimize ne yarıyor.** Yargıcın sözünü neden dinlediğimizi sayıyla gösterir. İntranette aynı kalibrasyon kurum verisiyle tekrarlanabilir. Senior'un ilk soracağı "yargıca neden güveniyoruz?" sorusunun cevabıdır.

**Örnek (uydurma).** 40 çiftin 8'i beraberlik; 32 beraberliksiz çift kalıyor:
- Geçti: insan 16 A / 16 B diyor. Yargıç 13 A'yı ve 13 B'yi doğru buluyor, 3'er yerde ters diyor. Uyum 26/32 = %81,3. Şans uyumu %50, kappa 0,63. İki koşul da sağlandı.
- Kaldı: insan 24 A / 8 B diyor. Yargıç 30 kez A diyor. 24 çiftte aynı karar → uyum tam %75 (koşul sağlanıyor). Ama yargıç neredeyse hep A dediği için şans uyumu %71,9. Kappa yalnızca 0,11. Kappa koşulu kaldı; yargıç ikincil göstergeye düşer.

### 0.4 Yargıç sıra tutarlılığı: ≥ %80

**Arka plan.** **Sıra yanlılığı** (position bias): yargıç modellerin cevabın içeriğinden bağımsız olarak ilk (ya da ikinci) gösterilen cevabı kayırma eğilimi. Bunu yakalamak için her çift iki kez sorulur: bir kez A-B sırasıyla, bir kez B-A sırasıyla. **Sıra tutarlılığı**, iki sırada da aynı cevabın kazandığı çiftlerin oranıdır.

**Ne yapılıyor.** Kalibrasyon çiftleri iki sırada yargıca verilir. İki sırada aynı kararın çıktığı çiftler sayılır. Eşik: **≥ %80**. Ayrıca bütün asıl ölçümlerde kural şudur: iki sırada karar değişirse o çift **beraberlik** sayılır.

**Neden.**
1. Yargıç gerçekten içeriğe bakıyorsa, cevapların yerini değiştirmek kararını değiştirmemelidir.
2. Karar sırayla değişiyorsa, o kararı içerik değil konum belirlemiştir.
3. Tutarsız çiftler beraberlik sayıldığı için, tutarlılık düşükse beraberlik sayısı şişer. Kesin karar sayısı azalır ve 1.1'deki anlamlılık testi gücünü kaybeder.
4. Neden %80? Her beş çiftten en fazla birinde sıranın kararı değiştirmesine izin verilir. Daha düşük tutarlılıkta, kesin kararların önemli bir bölümü şansa bağlı olur.

**Olmasaydı ne olurdu.** Değerlendirme betiği adaptörün cevabını hep A konumuna koyuyor ve yargıç ilk cevabı kayırıyor. Tek sırada sorarsak adaptör %65 kazanır. İki sırada sorsaydık kararların yarısı değişecek ve kazanma oranı %52'ye inecekti.

**İşimize ne yarıyor.** Kararın içerikten geldiğini kanıtlar. Sıra yanlılığı oranı raporlanır; senior bunu yargıcın kalite göstergesi olarak görür. İntranette farklı bir yargıç seçilirse aynı kontrol tekrarlanır.

**Örnek (uydurma).**
- Geçti: 30 çiftin 26'sında iki sırada aynı karar → %86,7.
- Kaldı: 30 çiftin 21'inde aynı karar → %70. Yargıç ikincil göstergeye düşer.

### 0.5 Yargıç seçimi: büyük model belirgin biçimde iyi değilse küçük model

**Arka plan.** İki aday var: `gemma4:12b` (12 milyar parametre, yaklaşık 8–10 GB VRAM, tahmin) ve `gemma4:26b` (uzmanlar karışımı, MoE: her token için parametrelerin yalnızca bir bölümü çalışır; yaklaşık 16–19 GB, tahmin). Büyük model genellikle daha iyi karar verir ama daha yavaştır, daha çok bellek ister ve intranete taşınması daha zordur.

**Ne yapılıyor.** İki aday da 0.3 ve 0.4 ölçümlerinden geçer. Eşik metni: "`gemma4:26b`, `gemma4:12b`'yi hem uyumda hem sıra tutarlılığında 5 pp'den fazla geçmiyorsa `gemma4:12b` seçilir". `deney_plani_v1.md` §6.8'deki açık hâli şudur: 26b uyumda 5 pp'den fazla önde değilse **ve** sıra tutarlılığında da 5 pp'den fazla önde değilse 12b seçilir.

**Neden.**
1. 40 çiftlik kalibrasyon setinde tek bir çift uyum yüzdesini 2,5 pp oynatır; beraberlikler çıkınca daha fazla.
2. Bu yüzden birkaç puanlık fark gerçek bir üstünlük olmayabilir.
3. Fark küçükse büyük modelin bedeli (hız, VRAM, taşıma) kazancından fazladır.
4. 5 pp, 40 çiftte 2 çifte denk gelir (ölçüldü). İlk taslaktaki 25 çiftte bu yalnızca 1,25 çiftti; yani tek bir çift seçimi belirleyebilirdi. Kalibrasyonun 40 çifte çıkarılmasının bir nedeni budur. 2 çift de küçük bir farktır; kural bilerek "belirgin fark yoksa küçük model" yönünde kurulmuştur.
5. Bu bir kullanıcı kararıdır; belirsizlik durumunda pratik tarafı seçer.

**Olmasaydı ne olurdu.** 26b uyumda 2 pp önde diye seçilir. İntranette aynı karta sığmadığı ortaya çıkar, değerlendirme saatlerce sürer ya da yargıç değişmek zorunda kalır. Pilot ile kurum turu farklı yargıçlarla ölçülmüş olur.

**İşimize ne yarıyor.** Seçimi önceden kurala bağlar; sonuçlara bakıp "işimize gelen yargıcı" seçme riskini kaldırır. Küçük model seçilirse servis ve değerlendirme aynı A5000'de daha rahat çalışır.

**Örnek (uydurma).**
- 12b seçilir: 26b uyum %82, 12b %79 (fark 3 pp). Sıra tutarlılığı 26b %88, 12b %85 (fark 3 pp). İkisi de 5 pp'nin altında.
- 26b seçilir: 26b uyum %86, 12b %77 (fark 9 pp). Sıra tutarlılığı 26b %92, 12b %84 (fark 8 pp).

---

## 3. §1 Birincil sonuç: seçilen adaptör vs `hazir_istemli` (test, 100 soru)

**Bu bölüm neden var?** Projenin ana sorusu şu: "Fine-tuning, iyi yazılmış bir istem ve birkaç örnekle elde edilemeyecek bir üslup ve jargon kazancı sağlıyor mu?" Karşılaştırma `hazir` ile değil, `hazir_istemli` ile yapılır. Çünkü fine-tuning pahalı bir yoldur. Aynı kazanç istemle ucuza elde edilebiliyorsa fine-tuning haklı çıkmaz. Tek bir ana karşılaştırma seçmek de bilinçli bir karardır: çok sayıda karşılaştırma yapılırsa biri şansla "başarılı" çıkar. Bölümde iki eşik var: yargıç ölçüsü (1.1) ve onu doğrulayan insan ölçüsü (1.2).

Birincil sonuç şöyle karara bağlanır (2026-11-24 güncellemesi):
- **Geçti:** 1.1 ve 1.2 birlikte sağlanır ve üç kritik koruma eşiğinin (2.1, 3.7, 4.2) hiçbiri aşılmaz.
- **Kaldı:** 1.1 veya 1.2 sağlanmaz ya da kritik eşiklerden biri aşılır.
- Uyarı eşikleri aşılırsa sonuç kendiliğinden düşmez. İnceleme yapılır ve karar senior ile verilir (§6 açıklaması aşağıda).
- Yargıç **üslup+jargon isteminde** 0.3 veya 0.4'ü geçemezse önce diğer aday denenir. **İki aday da** geçemezse 1.2 tek başına birincil olur, 1.1 "güvenilirliği düşük" notuyla raporlanır (2026-11-24 güncellemesi; ayrıntı §9).

### 1.1 Birincil uç nokta: üslup+jargon kazanma oranı ≥ %60 ve işaret testi p < 0,05

**Arka plan.**
- **Birincil uç nokta** (primary endpoint): başarının tek ana ölçüsü. Ön kayıtta tek bir tane seçilir.
- **Kazanma oranı** (win rate): yargıcın adaptörü seçtiği çiftlerin, kesin karar verilen çiftlere oranı.
- **Beraberlik** (tie): yargıcın "eşit" dediği ya da iki sırada farklı karar verdiği çiftler. Kazanma oranının paydasına girmez.
- **İşaret testi** (sign test): "İki sistem aslında eşitse, bu kadar dengesiz bir galibiyet dağılımını şansla görme olasılığı nedir?" sorusunu cevaplayan test. Mantık yazı-turadır: eşit iki sistem için her kesin karar yazı-tura gibidir; 100 atışta 70 yazı gelmesi şüphelidir.
- **p değeri** (p-value): sistemler gerçekten eşit olsaydı, gördüğümüz kadar (veya daha) uç bir sonucu görme olasılığı. Küçükse "bu şans olamaz" deriz. 0,05 geleneksel sınırdır: yirmide bir.
- **İki yönlü** (two-sided): hem "adaptör çok kazandı" hem "adaptör çok kaybetti" uçları hesaba katılır. Sonucu görmeden yön seçmemek için kullanılır.

**Ne yapılıyor.** Test setinin 100 sorusunda seçilen adaptör ile `hazir_istemli` cevapları yargıca iki sırada verilir. Soru: "Hangisi üslup ve jargon bakımından daha iyi?" Referans cevap gösterilmez. Tutarsız kararlar ve "eşit" kararları beraberlik sayılır, beraberlikler çıkarılır. Eşik: kazanma oranı **≥ %60 ve iki yönlü işaret testinde p < 0,05**.

**Neden.**
1. Başarı ölçütü "belirgin gelişme". %50 eşitlik demektir; %52 gibi bir oran belirgin değildir.
2. %60, "her beş karşılaştırmanın üçünde adaptör daha iyi" demektir. Bir kullanıcının fark edeceği düzeyde bir üstünlük olarak seçildi.
3. Ama küçük örnekte %60 şansla da çıkabilir. Örneğin 20 kesin kararda 12–8 sonucu yazı-turayla kolayca oluşur.
4. Bu yüzden anlamlılık koşulu eklendi: oran hem büyük hem şanstan ayırt edilebilir olmalı.
5. Hesap (ölçüldü, formülle): 100 kesin kararda p < 0,05 için en az 61 galibiyet gerekir; 60/100 ise p = 0,057 verir. Kesin karar sayısı azaldıkça gereken oran yükselir: 80 kararda 50 (%62,5), 50 kararda 33 (%66).

**Olmasaydı ne olurdu.** Beraberlikler yüzünden yalnızca 25 kesin karar kalır. Adaptör 15'ini kazanır: %60. Anlamlılık koşulu olmasaydı "belirgin gelişme" deriz. Oysa 15–10 sonucu (p ≈ 0,42) eşit iki sistemden de kolayca çıkar. Kurum verisiyle tekrarlandığında sonuç %48'e döner.

**İşimize ne yarıyor.** Projenin "evet/hayır" cevabını tek bir satıra bağlar. Sonucu görmeden yazıldığı için senior'a "başarı ölçütünü biz sonradan seçmedik" denebilir. İntranette aynı betik aynı testi yapar.

**Örnek (uydurma).** Raporlama kuralına (§7) uygun yazımla:
- Geçti: kazanma / beraberlik / kayıp = 58 / 12 / 30; p = 0,004. Kazanma oranı %65,9.
- Kaldı (oran düşük): 52 / 13 / 35; p = 0,086. Oran %59,8.
- Kaldı (oran yüksek ama anlamsız): 39 / 37 / 24; p = 0,077. Oran %61,9.

Son örnek, kazanma oranının neden tek başına yazılmadığını gösteriyor. "%61,9" etkileyici görünür, ama 100 sorunun 37'si beraberliktir ve sonuç şanstan ayırt edilemez.

### 1.2 Kör insan formu, üslup ve jargon: fark ≥ +0,5 ve bootstrap %95 güven aralığının alt sınırı > 0

**Arka plan.**
- **Kör değerlendirme** (blind evaluation): değerlendirici hangi cevabın hangi sistemden geldiğini bilmez. Model adları gizli, sıra karışık, eşleştirme anahtarı ayrı bir dosyadadır.
- **Puanlar**: üslup 0–2 ve jargon 0–2 (`deney_plani_v1.md` §6.1, §6.2). Toplamları 0–4 arasıdır. Bu bölümde referans cevap gösterilmez.
- **Eşleştirilmiş fark** (paired difference): aynı soruda adaptörün puanı eksi `hazir_istemli` puanı. Aynı soru iki sistemde de ölçüldüğü için sorunun kolaylığı farkta birbirini götürür.
- **Bootstrap** (yeniden örnekleme): elimizdeki 50 soruluk farkları torbaya koyup, yerine koyarak 50 tane çekme ve ortalamayı hesaplama işini çok kez (burada 10.000) tekrarlamak. Bu 10.000 ortalamanın yayılması, "başka 50 soru seçseydik sonuç ne kadar oynardı?" sorusunu cevaplar.
- **%95 güven aralığı** (confidence interval): bu yayılmanın ortadaki %95'lik bölümü. Alt sınır 0'ın üstündeyse, gelişmenin 0'dan büyük olduğuna makul ölçüde güvenebiliriz.

**Ne yapılıyor.** 11. aşamada testten 50 soru (cevaplar üretilmeden önce kimlikle seçilir) için seçilen adaptör ile `hazir_istemli` cevapları tek bir değerlendirici tarafından kör olarak puanlanır. Soru başına üslup+jargon toplamının farkı alınır, ortalaması hesaplanır. Eşik: **ortalama fark ≥ +0,5 ve eşleştirilmiş bootstrap (10.000 tekrar, seed 42) %95 güven aralığının alt sınırı > 0**.

**Neden.**
1. Yargıç ne kadar kalibre olursa olsun bir modeldir. Ana iddia bir insan tarafından da doğrulanmalı.
2. Hedef kullanıcı insandır; asıl ölçü insanın algısıdır.
3. Neden +0,5? Soruların yarısında iki ölçütten birinde bir basamak artış (ör. jargon 1'den 2'ye) ortalamada +0,5 eder. Bu, bir okuyucunun fark edeceği en küçük anlamlı değişiklik olarak seçildi.
4. Neden güven aralığı? 50 soruda ortalama birkaç iyi soruyla şişebilir. Alt sınırın 0'ın üstünde olması, gelişmenin birkaç sorudan değil genelden geldiğini gösterir.
5. Neden bootstrap? Puanlar 0–4 arasında kaba basamaklı; normal dağılım varsayımı zayıf kalır. Bootstrap böyle bir varsayım gerektirmez.

**Olmasaydı ne olurdu.** Yargıç adaptörü kayırıyor ama kalibrasyon setinde bu görünmemiş. 1.1 geçer, "fine-tuning başarılı" deriz. İnsan formu olsaydı, insanın iki sistem arasında fark görmediği (fark +0,1) ortaya çıkacaktı.

**İşimize ne yarıyor.** Yargıç ile insanı birbirine karşı denetler. Yargıç kalibrasyondan geçemezse projenin ana kararı yine verilebilir: 1.2 tek başına birincil olur. Senior'a "bir insan da kör olarak aynı şeyi gördü" denebilir.

**Örnek (uydurma).**
- Geçti: ortalama fark +0,72; %95 güven aralığı [+0,38, +1,06]. İki koşul da sağlandı.
- Kaldı: ortalama fark +0,60; güven aralığı [−0,04, +1,22]. Ortalama yeterli ama alt sınır 0'ın altında; fark birkaç sorudan geliyor olabilir.

---

## 4. §2 Bilgi doğruluğu: kötüleşme yok

**Bu bölüm neden var?** Fine-tuning üslubu değiştirirken bilgiyi de bozabilir. Model resmî bir dille ama yanlış süreyle cevap verirse, bu daha tehlikelidir: resmî üslup yanlış bilgiye güven kazandırır. Başarı ölçütü 2 ("bilgi doğruluğunda kötüleşme yok") burada ölçülür. Bu bölüm bir **koruma** bölümüdür: adaptörün bilgide daha iyi olmasını beklemez, yalnızca belirgin biçimde kötüleşmemesini ister. Karşılaştırma hem `hazir` hem `hazir_istemli` ile ayrı ayrı yapılır; ikisinde de geçmelidir. Aynı şey hem yargıçla, hem otomatik metrikle, hem insanla ölçülür. Çünkü her yöntemin kör noktası farklıdır. Bu bölümde yalnızca **2.1 kritiktir**; 2.1b–2.4 uyarı eşiğidir (bkz. §6 açıklaması). Neden 2.1: çalışanı yanlış işleme yönlendiren hata en pahalı hatadır. Diğer ölçüler aynı riskin daha ince ya da daha gürültülü göstergeleridir.

### 2.1 Kritik hata içeren cevap sayısı: fark ≤ +3 (100 soruda)

**Arka plan.** **Kritik hata**: cevaba göre hareket eden bir çalışanın yanlış işlem yapmasına yol açacak hata. Tanım `deney_plani_v1.md` §6.3'te: yanlış kurum, tarih, süre, tutar/oran, atlanan veya uydurulan koşul ya da istisna, kaldırılmış bir uygulamayı yürürlükte gibi anlatmak. Referansta olmayan ama doğrulanamayan bir rakam kritik hata değildir; ayrı işaretlenir ve insana gider.

**Ne yapılıyor.** Test setinin 100 sorusunda her sistemin her cevabı için iki kaynaktan kritik hata işareti toplanır: yargıcın bilgi işaretleri ve otomatik betiğin "aynı birimde referansla çelişen sayı" tespiti. Kritik hatalı cevaplar sayılır. İnsan formundaki 50 soruda ise etiket insandan gelir: insanın "kritik hata var/yok" kararı yargıç ve betik işaretinin yerini alır (**birleşik etiket**, 2026-11-24; §9). Eşik: **adaptörün sayısı − karşılaştırılan sistemin sayısı ≤ +3**. Bu bir **kritik eşiktir**: iki karşılaştırmadan birinde bile aşılırsa birincil sonuç "kaldı" olur.

**Neden.**
1. Kritik hata, bu projedeki en pahalı hatadır; çalışanı yanlış işleme yönlendirir.
2. "Hiç artmasın" (fark ≤ 0) koşulu küçük örnekte haksız olur. İki sistem aynı derecede iyi olsa bile, hangi soruların hatalı çıkacağı rastlantıyla birkaç adet oynayabilir.
3. +3, bu rastlantısal oynamaya pay bırakır.
4. Ama 4 ve üstü artış, birkaç soruluk sistematik bir kötüleşme sayılır ve kabul edilmez.

**Olmasaydı ne olurdu.** Adaptör üslupta açıkça kazanır ama yeni öğrendiği resmî kalıplarda sürelerini karıştırır: 6 kritik hatadan 13'e çıkar. Yalnızca 1.1'e bakarsak, çalışanları yanlış sürelerle yönlendiren bir modeli "başarılı" diye servise çıkarırız.

**İşimize ne yarıyor.** Üslup kazancının bilgi pahasına gelmediğini kanıtlar. Kurum verisi turunda en çok sorulacak soru budur: "Model yanlış bilgi veriyor mu?"

**Örnek (uydurma).**
- Geçti: `hazir_istemli` 7, adaptör 9 kritik hata → fark +2.
- Kaldı: `hazir` 5, adaptör 10 → fark +5.

### 2.1b Kör insan formu, bilgi bölümü: "Hayır" cevabı farkı ≤ +2 (50 soruda)

**Arka plan.** İnsan formunun ikinci bölümünde değerlendirici soruyu, **referans cevabı** ve modelin cevabını görür. Soru: "Referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" Seçenekler: Evet / Kısmen / Hayır. Bu bölüm üslup bölümü bittikten sonra doldurulur; referansı gördükten sonra üslup puanının referansa benzerliğe kaymasını önlemek için.

**Ne yapılıyor.** Yalnızca birincil çift (seçilen adaptör ve `hazir_istemli`) için, 1.2 ile aynı 50 soruda "Hayır" cevabı alan cevaplar sayılır. Eşik: **fark ≤ +2**. Formda ayrıca "Kritik hata var mı? Var / Yok" alanı bulunur (2026-11-24 eklendi). Bu alan 2.1'e girer: insanın kararı eşiğin sonucunu değil, **o kaydın etiketini** değiştirir (§9, birleşik etiket). İlk taslaktaki "2.1 ile çelişirse insan kararı geçerlidir" cümlesi bu kuralla değiştirildi.

**Neden.**
1. 2.1 yargıca ve betiğe dayanır. İnsan, yargıcın kaçırdığı ince koşul hatalarını görebilir.
2. "Hayır", 2.1'deki kritik hatanın insan karşılığıdır.
3. Örneklem 50 soru, yani 2.1'in yarısı. 2.1'deki +3'ün yarısı 1,5'tir; tam sayı olması için +2'ye yuvarlandı.
4. İnsan bir değerlendirme aracı olarak yargıçtan daha güvenilir kabul edildiği için çelişkide insan kazanır. Ama bu üstünlük tek tek kayıtlarda kullanılır: 2.1b bir uyarı eşiği olarak kritik 2.1'in sonucunu kaldıramaz.
5. Neden "Hayır" ile ayrı bir kritik hata alanı? "Hayır" kritik hatayla aynı şey değildir. Ana hükmü yanlış ama kimseyi yanlış işleme yönlendirmeyecek bir cevap da "Hayır" alabilir.

**Olmasaydı ne olurdu.** Yargıç, resmî dille yazılmış ama bir istisnayı atlayan cevapları "doğru" sayıyor. 2.1 geçiyor. İnsan formu olmasaydı bu sistematik kör nokta raporda hiç görünmezdi.

**İşimize ne yarıyor.** Bilgi doğruluğunu bir insan gözüyle de bağlar. Senior'a "bilgiyi bir insan referansla karşılaştırdı" denebilir.

**Örnek (uydurma).**
- Geçti: `hazir_istemli` 4, adaptör 5 "Hayır" → fark +1.
- Aşıldı (uyarı): `hazir_istemli` 3, adaptör 7 → fark +4.

### 2.2 Yargıç bilgi ikili karşılaştırması: kaybetme − kazanma ≤ 10 pp

**Arka plan.** 1.1'deki ikili karşılaştırma ve iki sıralı sorma burada da geçerlidir. Fark: soru "hangisi bilgi bakımından daha doğru?" ve yargıca referans cevap da verilir.

**Ne yapılıyor.** Adaptörün kaybetme oranından kazanma oranı çıkarılır. Eşik: **≤ 10 pp**.

**Neden.**
1. Bilgide eşitlik beklenir; fine-tuning bilgi kazandırmak için değil üslup için yapıldı.
2. Eşitlikte kaybetme ile kazanma birbirine yakın çıkar; fark 0 civarında oynar.
3. 10 pp, küçük bir rastlantısal dengesizliğe izin verir. Daha fazlası, adaptörün bilgide belirgin biçimde geride kaldığını gösterir.
4. 2.1 yalnızca ağır hataları sayar. 2.2 daha ince farkları da yakalar: eksik koşul, daha az eksiksiz cevap.

**Olmasaydı ne olurdu.** Adaptörün hiç kritik hatası artmıyor ama cevapları kısalıyor ve önemli koşulları atlıyor. 2.1 geçer. 2.2 olmasaydı, "bilgi korundu" deriz; oysa yargıç çiftlerin %35'inde hazır modeli, %15'inde adaptörü daha doğru buluyordu.

**İşimize ne yarıyor.** Kritik olmayan ama birikince kullanıcıyı yanıltan bilgi kaybını yakalar.

**Örnek (uydurma).**
Bu örnekte oranlar 100 sorunun hepsi üzerinden hesaplandı; payda henüz kesinleşmedi ("Açıklarken fark ettiklerim", madde 7).
- Geçti: kazanma / beraberlik / kayıp = 18 / 60 / 22; p = 0,64. Kaybetme − kazanma = 4 pp.
- Aşıldı (uyarı): 14 / 55 / 31; p = 0,016. Kaybetme − kazanma = 17 pp. Adaptörün iki sırada da kaybettiği 31 kayıt incelenir.

### 2.3 Sayı/tarih/süre recall'u: fark ≥ −3 pp

**Arka plan.** **Recall** (yakalama oranı): referansta geçen sayıların kaçının cevapta da geçtiği. Referans "30 gün içinde, %50 zamlı" diyorsa iki sayı vardır; cevapta yalnızca 30 geçiyorsa recall 1/2 = %50 olur. Bu ölçüm betikle, yargıç olmadan yapılır.

**Ne yapılıyor.** Her cevap için recall hesaplanır, sistem başına ortalama alınır. Eşik: **adaptörün ortalaması − karşılaştırılan sistemin ortalaması ≥ −3 pp**.

**Neden.**
1. Kurum sorularının bilgi çekirdeği çoğunlukla sayılardır: süre, gün, oran.
2. Üslup değişirken model sayıları atlamaya başlarsa ("makul bir süre içinde"), cevap kulağa resmî gelir ama işe yaramaz.
3. Bu ölçüm otomatik olduğu için yargıçtan bağımsız bir kontroldür.
4. 3 pp küçük bir pay bırakır: yazıyla yazılmış sayılar ya da farklı biçimler ("bir ay" ↔ "30 gün") birkaç puan oynatabilir.

**Olmasaydı ne olurdu.** Adaptör "Kanunda belirlenen süre içinde başvurunuz gerekmektedir" gibi resmî ama sayısız cümleler kurmayı öğrenir. Yargıç üslubu beğenir. Recall %78'den %61'e düşmüştür ama kimse fark etmez.

**İşimize ne yarıyor.** Yargıç ve insandan bağımsız, intranette aynen tekrarlanabilen ucuz bir alarm.

**Örnek (uydurma).**
- Geçti: `hazir` %74, adaptör %72 → fark −2 pp.
- Aşıldı (uyarı): `hazir_istemli` %80, adaptör %71 → fark −9 pp.

### 2.4 Aynı birimde referansla çelişen sayı içeren cevap sayısı: fark ≤ +3

**Arka plan.** Betik, cevaptaki sayıları birimiyle birlikte (gün, ay, yüzde vb.) çıkarır ve referanstakilerle karşılaştırır. Referans "%50" dediği yerde cevap "%25" diyorsa bu **aynı birimde çelişen sayı**dır. Bu, yanlış bilginin en ölçülebilir biçimidir.

**Ne yapılıyor.** En az bir çelişen sayı içeren cevaplar sayılır. Eşik: **fark ≤ +3**.

**Neden.**
1. 2.1'in tamamen otomatik karşılığıdır: yargıç yanılsa bile bu sayım yanılmaz (kendi sınırları içinde).
2. 2.3 "sayıyı söylemedi" durumunu, 2.4 "sayıyı yanlış söyledi" durumunu yakalar. İkincisi daha tehlikelidir.
3. Tolerans 2.1 ile aynı mantıkla +3 seçildi.

**Olmasaydı ne olurdu.** Yargıç, iki cevaptaki "%25" ve "%50" farkını gözden kaçırır. 2.1 geçer. Otomatik sayım olmasaydı, adaptörün 6 cevapta oran karıştırdığını bilmezdik.

**İşimize ne yarıyor.** Yargıcın kontrolü. İntranette yargıç değişse bile bu ölçüm aynı kalır.

**Örnek (uydurma).**
- Geçti: `hazir` 3, adaptör 4 → fark +1.
- Aşıldı (uyarı): `hazir` 2, adaptör 8 → fark +6.

### 2.5 chrF: raporlanır, eşik yok

**Arka plan.** **chrF** (karakter n-gram F-skoru): cevap ile referans arasında ortak karakter dizilerinin oranına dayanan benzerlik puanı (0–100). "tazminatı" ile "tazminatın" büyük ölçüde örtüşür; bu yüzden Türkçe gibi eklemeli dillerde kelime tabanlı ölçülerden daha adil sonuç verir. `sacrebleu` kütüphanesiyle hesaplanır.

**Ne yapılıyor.** Her sistemin ortalama chrF'si hesaplanır ve raporlanır. **Eşik yok**; geçme koşulu değildir.

**Neden.**
1. chrF anlamı değil yüzey benzerliğini ölçer.
2. Adaptör tam da üslubu değiştirmek için eğitildi. Üslup değişince cümleler referanstan farklılaşabilir ve chrF düşebilir; ya da referansın üslubuna yaklaşıp yükselebilir. İki yön de bilgi doğruluğu hakkında bir şey söylemez.
3. Tek bir kritik rakam hatası ("30" → "60") chrF'yi neredeyse değiştirmez.
4. Böyle bir ölçüyü geçme koşulu yapmak, ya iyi bir modeli haksız yere düşürür ya da kötüsünü geçirir.
5. Yine de raporlanır, çünkü alanda yaygın kullanılan bir ölçüdür ve büyük bir değişim incelemeye değer bir işarettir.

**Olmasaydı ne olurdu.** chrF'ye eşik koysaydık: adaptör referanstan farklı ama doğru ve daha resmî cümleler kurduğu için chrF 6 puan düşer. "Bilgi kötüleşti" deriz; oysa 2.1–2.4 bilginin korunduğunu gösteriyordur.

**İşimize ne yarıyor.** Yaygın bir metriği neden bağlayıcı yapmadığımızı önceden açıklar. Senior "chrF neden düştü?" diye sorarsa cevap hazırdır.

**Örnek (uydurma).** Eşik olmadığı için geçti/kaldı yoktur. Raporlama örneği: `hazir_istemli` 41,2; adaptör 38,7 (fark −2,5). Rapora "chrF düştü; anlam doğruluğu ölçülerinde (2.1–2.4) kötüleşme yok" diye yazılır.

---

## 5. §3 Genel Türkçe korunuyor: final eşikleri (11. aşama, saklanan %70)

**Bu bölüm neden var?** Model kurum SSS'leriyle eğitilirken başka becerilerini unutabilir. Buna **unutma** (catastrophic forgetting) denir. Kurumda çalışan biri modele yalnızca mevzuat değil, metin özetleme, düzeltme, çeviri veya gündelik bir soru da sorabilir. Başarı ölçütü 3 ("genel Türkçe becerileri korunuyor") burada ölçülür. Taban çizgisi `hazir`'dır, çünkü korumak istediğimiz şey orijinal modelin becerisidir. Ölçüm Türkçe değerlendirme setlerinin **saklanan %70** bölümünde, yalnızca 11. aşamada bir kez yapılır. Geliştirme %30 bölümü ise ayar seçiminde ve §3A tetikleyicisinde kullanılır. Aynı veriyle hem ayar seçip hem sonuç bildirmek, sonucu iyimser yapar; ayrım bunun içindir. Bu bölümde yalnızca **3.7 (üslup sızıntısı) kritiktir**; diğerleri uyarı eşiğidir. Neden 3.7: kurum dilinin gündelik kullanıma taşması fine-tuning'in en doğrudan ve kullanıcının hemen fark edeceği yan etkisidir. Ölçümü de yargıca değil sabit bir işaret listesine dayanır.

### 3.1 TurkishMMLU doğruluğu (630): fark ≥ −2,0 pp

**Arka plan.**
- **TurkishMMLU**: çeşitli derslerden Türkçe çoktan seçmeli sorular. Modelin genel bilgi ve akıl yürütmesini ölçer. Soruların önüne aynı 5 örnek soru-cevap konur (5-shot), model yalnızca harfi seçer.
- **Doğruluk** (accuracy): doğru cevaplanan soruların oranı.
- **Standart hata** (standard error): bir oranın, örneklem rastlantısı yüzünden ne kadar oynayabileceğinin ölçüsü. Formül √(p(1−p)/n). 630 soruda ve %50–60 doğrulukta yaklaşık 2 pp'dir (ölçüldü, formülle).

**Ne yapılıyor.** Saklanan 630 soruda adaptör ile `hazir`'ın doğruluğu ölçülür. Eşik: **fark ≥ −2,0 pp**.

**Neden.**
1. Genel bilgi, fine-tuning'in en çok bozabileceği beceridir.
2. Eşik standart hata düzeyinde seçildi. Tek bir oranın gürültüsü yaklaşık 2 pp. Aynı sorularda eşleştirilmiş fark daha az gürültülüdür (tahmin; iki model çoğu soruda aynı cevabı verir).
3. Dolayısıyla 2 pp'den büyük bir düşüş gürültüyle açıklanması zor, gerçek bir kayıp sayılır.

**Olmasaydı ne olurdu.** Adaptör kurum dilini öğrenirken tarih ve coğrafya bilgisinde 6 pp kaybeder. Yalnızca kurum sorularına bakarsak bunu görmeyiz. Kullanıcılar modeli genel işlerde kullanmaya başlayınca sorun ortaya çıkar.

**İşimize ne yarıyor.** Standart, dışarıda da bilinen bir ölçüyle "model genel olarak aptallaşmadı" kanıtı. İntranette aynı dosya ve aynı betikle tekrarlanır.

**Örnek (uydurma).**
- Geçti: `hazir` %58,4, adaptör %57,1 → fark −1,3 pp.
- Aşıldı (uyarı): `hazir` %58,4, adaptör %55,6 → fark −2,8 pp.

### 3.2 GECTurk chrF (350): fark ≥ −1,0 puan

**Arka plan.** **GECTurk**: Türkçe dilbilgisi hatası düzeltme görevi. Modele hatalı bir cümle verilir, düzeltilmiş hâlini yazması istenir. chrF (2.5) burada uygun bir ölçüdür, çünkü doğru düzeltme referansa karakter düzeyinde çok yakın olmalıdır.

**Ne yapılıyor.** Saklanan 350 kayıtta adaptör ve `hazir`'ın ortalama chrF'si karşılaştırılır. Eşik: **fark ≥ −1,0 puan**.

**Neden.**
1. Kurum çalışanı modele resmî yazışma düzelttirebilir; bu beceri korunmalı.
2. 2.5'te chrF'ye eşik koymadık, çünkü orada üslup değişikliği bekleniyordu. Burada beklenmiyor: görevin tek bir doğru biçimi var, chrF anlamlı bir ölçü olur.
3. `esikler_v1.md` gerekçesi: chrF'de 1 puanın altındaki fark genellikle gürültüdür. Daha büyük düşüş gerçek kayıp sayılır.

**Olmasaydı ne olurdu.** Adaptör düzeltme yerine cümleyi resmî üsluba "çevirmeye" başlar. Cümleler referanstan uzaklaşır, chrF 4 puan düşer. Fark etmezsek kullanıcının metnini istemediği biçimde değiştiren bir model çıkarırız.

**İşimize ne yarıyor.** Üslup sızıntısının bir başka biçimini, düzeltme görevine taşmasını yakalar.

**Örnek (uydurma).**
- Geçti: `hazir` 71,3, adaptör 70,8 → fark −0,5.
- Aşıldı (uyarı): `hazir` 71,3, adaptör 68,9 → fark −2,4.

### 3.3 XL-Sum chrF (350): fark ≥ −1,0 puan

**Arka plan.** **XL-Sum**: haber metinlerini özetleme görevi. chrF, model özeti ile referans özet arasındaki benzerliği ölçer. Özetlemede birçok doğru cevap olduğu için chrF burada kaba bir ölçüdür ama iki modeli karşılaştırmak için kullanılabilir.

**Ne yapılıyor.** Saklanan 350 kayıtta ortalama chrF karşılaştırılır. Eşik: **fark ≥ −1,0 puan**.

**Neden.**
1. Özetleme, kurum içinde de istenecek genel bir iştir (rapor, toplantı notu).
2. Fine-tuning modelin uzun girdi okuma ve kısaltma becerisini bozabilir: model örneğin her özete resmî bir giriş cümlesi eklemeye başlayabilir.
3. Eşik 3.2 ile aynı mantıkla 1 puan seçildi.

**Olmasaydı ne olurdu.** Adaptör her özeti "İlgili haberde belirtildiği üzere…" diye başlatmaya başlar. Özetler uzar, chrF düşer. Ölçmeseydik bu alışkanlık kullanıcıya kadar giderdi.

**İşimize ne yarıyor.** Kurum dilinin özetleme gibi tarafsız bir göreve taşmadığını gösterir.

**Örnek (uydurma).**
- Geçti: `hazir` 33,0, adaptör 33,4 → fark +0,4.
- Aşıldı (uyarı): `hazir` 33,0, adaptör 31,6 → fark −1,4.

### 3.4 WMT16 EN→TR chrF (350): fark ≥ −1,0 puan

**Arka plan.** **WMT16 EN→TR**: İngilizceden Türkçeye çeviri görevi. chrF, çeviri değerlendirmesinde yaygın kullanılır.

**Ne yapılıyor.** Saklanan 350 kayıtta ortalama chrF karşılaştırılır. Eşik: **fark ≥ −1,0 puan**.

**Neden.**
1. Çeviri, iki dili birlikte kullanma becerisini ölçer. Yalnızca Türkçe SSS ile eğitilmek bu beceriyi zayıflatabilir.
2. Kurumda yabancı dildeki bir yönetmeliği veya e-postayı çevirtmek gerçekçi bir kullanımdır.
3. Eşik 3.2 ile aynı mantıkla 1 puan.

**Olmasaydı ne olurdu.** Adaptör İngilizce cümleleri çevirmek yerine Türkçe olarak "cevaplamaya" başlar (SSS alışkanlığı). chrF 5 puan düşer. Fark etmezsek çeviri isteyen kullanıcı ilgisiz bir cevap alır.

**İşimize ne yarıyor.** Talimat izleme becerisinin (soru-cevap değil çeviri istendiğini anlama) korunduğunu gösterir.

**Örnek (uydurma).**
- Geçti: `hazir` 52,6, adaptör 52,0 → fark −0,6.
- Aşıldı (uyarı): `hazir` 52,6, adaptör 49,8 → fark −2,8.

### 3.5 Vikipedi perplexity (350): göreli artış ≤ %10

**Arka plan.** **Perplexity** (şaşkınlık): modelin bir metni ne kadar "beklenmedik" bulduğunun ölçüsü. Model metni token token okurken her seferinde bir sonraki token'ı tahmin eder. Doğru token'a yüksek olasılık verirse şaşırmaz, perplexity düşük olur. Kabaca, "model her adımda ortalama kaç seçenek arasında kararsız kaldı" diye düşünülebilir. Burada sohbet şablonu ve sistem mesajı olmadan, ham Vikipedi metninde ölçülür. Yalnızca aynı tokenizer'ı kullanan modeller arasında karşılaştırılabilir; bizde hepsi aynı tabandan gelir.

**Ne yapılıyor.** Saklanan 350 metinde adaptör ve `hazir`'ın perplexity'si ölçülür. Göreli artış = (adaptör − hazır) / hazır. Eşik: **≤ %10**.

**Neden.**
1. Üretim görevleri (3.1–3.4) belirli becerileri ölçer. Perplexity daha temel bir şeyi ölçer: modelin genel Türkçe dağılımı hâlâ yerinde mi?
2. Resmî metne uyum sağlamış bir modelin genel metinde biraz daha şaşırması doğaldır. Bu cevapların kötü olduğu anlamına gelmez.
3. Bu yüzden eşik sıfır değil, %10'luk bir pay.
4. Perplexity'nin mutlak değeri modele ve metne göre çok değiştiği için fark yerine göreli artış kullanılır.
5. %10'un üstü, dil dağılımında belirgin bir kayma olarak yorumlanır. Bu sayı bir ölçümden değil, makul bir pay olarak seçildi.

**Olmasaydı ne olurdu.** Adaptör aşırı eğitilmiş ve genel Türkçeyi "unutmaya" başlamış. Üretim görevlerinde küçük bozulmalar var ama eşiklerin hemen altında kalıyor. Perplexity %35 artmıştır; ölçmeseydik bu erken uyarıyı kaçırırdık.

**İşimize ne yarıyor.** Üretim gerektirmediği için hızlıdır ve yargıç ya da referans cevap istemez. Kurum turunda aynı metinle hızlı bir "sağlık kontrolü" olarak kullanılabilir.

**Örnek (uydurma).**
- Geçti: `hazir` 8,40, adaptör 8,95 → göreli artış %6,5.
- Aşıldı (uyarı): `hazir` 8,40, adaptör 9,62 → göreli artış %14,5.

### 3.6 Aya ikili karşılaştırması (175): kaybetme − kazanma ≤ 10 pp

**Arka plan.** **Aya**: çeşitli konularda açık uçlu Türkçe yardım istekleri (ör. "Bir doğum günü mesajı yazar mısın?"). Tek bir doğru cevap olmadığı için chrF kullanılamaz. Bunun yerine yargıç ikili karşılaştırması (0.3, 1.1) kullanılır: adaptör vs `hazir`.

**Ne yapılıyor.** Saklanan 175 kayıtta yargıç iki sırada karar verir. Eşik: **kaybetme − kazanma ≤ 10 pp**.

**Neden.**
1. Genel yardımseverlik, sabit cevaplı görevlerle ölçülemez.
2. Adaptörün genel isteklerde hazır modele eşit olması beklenir; daha iyi olması beklenmez.
3. 10 pp, 2.2 ile aynı mantıkla küçük bir dengesizliğe izin verir; daha fazlası belirgin gerileme sayılır.

**Olmasaydı ne olurdu.** Adaptör her isteğe kısa ve resmî cevap vermeye başlar ("Talebiniz doğrultusunda…"). Sabit cevaplı görevler geçer. Yargıç ise genel isteklerde hazır modeli %40, adaptörü %20 tercih ediyordur.

**İşimize ne yarıyor.** Kullanıcının günlük deneyimine en yakın genel ölçüdür.

**Örnek (uydurma).**
175 kaydın hepsi üzerinden:
- Geçti: kazanma / beraberlik / kayıp = 42 / 84 / 49; p = 0,53. Fark 4,0 pp.
- Aşıldı (uyarı): 33 / 79 / 63; p = 0,003. Fark 17,1 pp. 63 kayıt 40'tan fazla olduğu için seed 42 ile 40'ı incelenir.

### 3.7 Üslup sızıntısı: sızıntılı cevap oranı ≤ `hazir` oranı + 10 pp

**Arka plan.** **Üslup sızıntısı**: kurum dilinin gereksiz yere gündelik sorulara taşması. Örnek (uydurma): "Akşam yemeği için hızlı bir tarif önerir misin?" sorusuna "İlgili mevzuat çerçevesinde…" diye başlayan bir cevap. Ölçüm `genel_kontrol` setlerindeki 50 gündelik soruda yapılır ve iki grup için iki ayrı işaret listesi kullanılır (`deney_plani_v1.md` §6.6):
- **`a` grubu** (kurumla ilgisiz gündelik sorular): kurum ağzı, mevzuat atfı, gereksiz kurum yönlendirmesi, resmî kip yoğunluğu.
- **`b` grubu** (kurum işlemini gündelik dille soran ve sade anlatım bekleyen sorular): kurum ve sistem adları serbesttir, çünkü doğru yönlendirme cevabın kendisidir. İşaretler: kurum ağzı, bürokratik kalıp, resmî kip yoğunluğu.

İki grupta da cevapta **en az 2 farklı işaret** varsa cevap sızıntılı sayılır. Listeler eşik onayıyla dondurulur.

**Ne yapılıyor.** Final ölçümü saklanan set `genel_kontrol_v2` üzerinde yapılır. Sızıntılı cevap oranı = sızıntılı cevap / gündelik soru. Eşik: **adaptörün oranı ≤ `hazir`'ın oranı + 10 pp**. Bu bir **kritik eşiktir**.

**Neden.**
1. Fine-tuning modele resmî üslup öğretir. Model bu üslubu "her zaman" kullanmayı öğrenirse amacından sapmış olur. Hedef "doğru yerde resmî üslup"tur.
2. Hazır model de bazen resmî konuşur; bu yüzden mutlak sınır yerine `hazir`'a göre bir artış sınırı konur.
3. 50 soruda 10 pp yaklaşık 5 cevaba denk gelir. Bu kadar artışa tolerans var; daha fazlası kurum dilinin gündelik kullanıma taştığını gösterir.
4. Eşik oran olarak yazıldı; saklanan bölümün boyutu değişse de anlamı değişmez.
5. Neden iki işaret? Tek bir "Sayın" kelimesi kaza olabilir. İki farklı işaret, cevabın bütün olarak kurum diline kaydığını gösterir.
6. Neden `b` için farklı liste? Bu sorularda "e-Devlet'ten başvurun" demek doğru cevaptır. Kurum adlarını yasaklamak doğru cevabı cezalandırırdı (karar 6c).

**Olmasaydı ne olurdu.** Adaptör kurum sorularında mükemmel ama "Arkadaşıma doğum günü mesajı yazar mısın?" sorusuna "Sayın arkadaşım, doğum gününüz münasebetiyle…" diye cevap veriyor. Kurum çalışanları modeli genel işlerde kullanmayı bırakır ve "garip bir araç" der.

**İşimize ne yarıyor.** Fine-tuning'in en olası yan etkisini doğrudan ölçer. Senior'a "model resmî üslubu ne zaman kullanacağını biliyor" kanıtı.

**Örnek (uydurma).**
- Geçti: `hazir` %6, adaptör %14 → artış 8 pp.
- Kaldı: `hazir` %6, adaptör %22 → artış 16 pp.

### 3.8 Çoktan seçmelide harf çıkarılamayan cevap oranı: ≤ %3

**Arka plan.** TurkishMMLU'da (3.1) cevap bir harftir (A, B, C…). Betik modelin cevabından harfi otomatik çıkarır. Model "Cevap B'dir" yerine uzun bir açıklama yazarsa veya hiç harf vermezse harf çıkarılamaz; o soru yanlış sayılır ve ayrıca raporlanır.

**Ne yapılıyor.** Harf çıkarılamayan cevapların oranı hesaplanır. Eşik: **≤ %3** (mutlak).

**Neden.**
1. Harf çıkarılamayan cevap yanlış sayılır. Bu oran yüksekse 3.1 bilgi değil biçim ölçmeye başlar.
2. Fine-tuning modele uzun, açıklamalı cevap yazmayı öğretebilir; bu da harf vermemeye yol açar.
3. %3 küçük bir pay bırakır: 630 soruda yaklaşık 19 cevap.
4. Bu eşik 3.1'in geçerlilik koşuludur; 0.2'nin çoktan seçmeli karşılığı gibi düşünülebilir.

**Olmasaydı ne olurdu.** Adaptörün doğruluğu 5 pp düşer, "genel bilgi kayboldu" deriz. Oysa düşüşün nedeni modelin her soruya resmî bir paragrafla cevap verip harf yazmamasıdır. Bilgi kaybı yoktur, biçim sorunu vardır; ve bu ikisi farklı çözüm ister.

**İşimize ne yarıyor.** 3.1 kaldığında nedenin bilgi mi biçim mi olduğunu ayırt eder.

**Örnek (uydurma).**
- Geçti: 630 cevabın 9'unda harf yok → %1,4.
- Aşıldı (uyarı): 630 cevabın 41'inde harf yok → %6,5.

### 3.9 `b_kurum_gayriresmi` bilgi doğruluğu (15 soru): kritik hatalı cevap ≤ `hazir` + 1 ve ortalama puan farkı ≥ −0,2

**Arka plan.** `b` grubu soruları kurum işlemi sorar ama sade anlatım ister (3.7). Sade bir cevap sızıntı ölçütünü geçer. Ama sade ve **yanlış** bir cevap da geçer. Bu yüzden `b` grubunda doğruluk ayrıca ölçülür. Yargıç her cevabı tek başına (ikili değil) `deney_plani_v1.md` §6.3'teki 0–2 ölçeğiyle puanlar. Referans olarak kaydın kullanıcı onaylı `bilgi_ogeleri` alanı kullanılır.

**Ne yapılıyor.** Saklanan `genel_kontrol_v2`'nin 15 `b` sorusunda iki şey ölçülür. Eşik: **adaptörün kritik hatalı cevap sayısı ≤ `hazir` + 1 ve ortalama puan farkı ≥ −0,2**.

**Neden.**
1. Sadeleşme bilgi kaybı pahasına olmamalı (başarı ölçütü 2).
2. 15 soruda tek bir kritik hata gürültü olabilir; ikincisi değildir. Bu yüzden +1'e izin var.
3. Ortalama puanda 0,2'lik pay, 15 soruda yaklaşık 3 cevabın bir basamak düşmesine karşılık gelir (3 × 1 / 15 = 0,2).
4. İki koşul farklı şeyleri yakalar: ilki ağır hataları, ikincisi yaygın küçük eksikleri.
5. Onaylanmayan bilgi öğesi puanlamaya girmez; referansın kendisi doğrulanmış olmalı.

**Olmasaydı ne olurdu.** Adaptör sade cevap vermeyi öğrenir ama sadeleştirirken başvuru süresini atlar. Sızıntı oranı mükemmel çıkar. Doğruluk ölçülmeseydi "sade anlatım başarılı" derdik.

**İşimize ne yarıyor.** Sistem mesajındaki sade anlatım kuralının (kural 9) bilgiyi feda etmeden uygulandığını gösterir.

**Örnek (uydurma).**
- Geçti: `hazir` 1, adaptör 2 kritik hata. Ortalama puan `hazir` 1,60, adaptör 1,47 → fark −0,13.
- Aşıldı (uyarı) (kritik hata): `hazir` 1, adaptör 3 kritik hata.
- Aşıldı (uyarı) (ortalama): kritik hata eşit ama ortalama fark −0,33.

---

## 6. §3A "Gerekirse karışım" tetikleyicisi (doğrulama aşaması, geliştirme %30)

**Bu bölüm neden var?** Unutmaya (§3) karşı yaygın bir çare, eğitim verisine bir miktar genel Türkçe soru-cevap karıştırmaktır. Ama bu çarenin bedeli var: ek veri üretimi, ek eğitim koşusu ve üslup kazancının bir kısmının sulanması. Kullanıcı kararıyla (2026-11-23) genel Türkçe verisi eğitime **yalnızca bir sorun görülürse** girer. §3A, "sorun görüldü mü?" sorusunu önceden sayıya bağlar. Böylece karışım kararı sezgiyle değil kuralla verilir.

Ölçüm doğrulama aşamasında, SSS tarifi seçildikten sonra **bir kez** yapılır. Seçilen adaptör ve `hazir`, Türkçe değerlendirmenin **geliştirme** bölümünde aynı ayarlarla çalıştırılır. Tetikleyiciyi aşmamak için ayar değiştirip yeniden ölçmek yasaktır; yinelenirse rapora yazılır. **T.1–T.8'den en az biri aşılırsa** `genel_karisim_adaptor` eğitilir.

**Neden final eşikleriyle aynı sayılar?** İki hatanın bedeli eşit değil:
- **Yanlış alarm**: tetikleyici gereksiz çalışır → bir ek eğitim koşusu.
- **Kaçırma**: gerçek gerileme görülmez → 11. aşamada geri dönüşü olmayan bir başarısızlık.

Kaçırma çok daha pahalı olduğu için, tetikleyici final eşiklerinden daha gevşek olmamalıdır. Aynı sayılar kullanılınca, geliştirme bölümünde kıl payı geçen bir model en azından "uyarı" almış olur.

### T.1 TurkishMMLU doğruluğu (270): fark < −2,0 pp → tetikler

**Arka plan.** Bkz. 3.1. Fark: 270 geliştirme sorusu kullanılır. Daha az soru olduğu için standart hata daha büyüktür: yaklaşık 3 pp (ölçüldü, formülle).

**Ne yapılıyor.** Seçilen SSS adaptörü ile `hazir` geliştirme bölümünde karşılaştırılır. **Fark −2,0 pp'nin altındaysa** tetikler.

**Neden.** 3.1'deki eşikle aynıdır. Geliştirmede kıl payı geçen bir model testte de kıl payı kalabilir. Bunu önceden yakalayıp önlem almak, 11. aşamada sürprizle karşılaşmaktan ucuzdur.

**Olmasaydı ne olurdu.** Geliştirmede −3 pp'lik düşüş görülür ama "gürültüdür" diye geçilir. 11. aşamada saklanan bölümde −3,5 pp çıkar ve 3.1 kalır. Ayar değiştirmek artık yasaktır; proje "genel bilgi korunmadı" sonucuyla biter.

**İşimize ne yarıyor.** 3.1'in erken uyarısı. Karışım kararını önceden kayıtlı bir sayıya bağlar.

**Örnek (uydurma).**
- Tetiklemez: fark −1,1 pp.
- Tetikler: fark −2,6 pp.

### T.2 GECTurk chrF (150): izin verilen en fazla düşüş 1,0 puan

**Arka plan.** Bkz. 3.2. 150 geliştirme kaydı.

**Ne yapılıyor.** Adaptörün chrF'si `hazir`'dan 1,0 puandan fazla düşükse tetikler.

**Neden.** 3.2 ile aynı eşik; gerekçe T.1 ile aynı: kaçırma, yanlış alarmdan pahalıdır.

**Olmasaydı ne olurdu.** Düzeltme görevine üslup sızıntısı geliştirmede görünür ama önlem alınmaz; test aşamasında 3.2 kalır.

**İşimize ne yarıyor.** 3.2'nin erken uyarısı.

**Örnek (uydurma).** Tetiklemez: −0,4. Tetikler: −1,8.

### T.3 XL-Sum chrF (150): izin verilen en fazla düşüş 1,0 puan

**Arka plan.** Bkz. 3.3. 150 geliştirme kaydı.

**Ne yapılıyor.** chrF düşüşü 1,0 puandan fazlaysa tetikler.

**Neden.** 3.3 ile aynı eşik, aynı mantık.

**Olmasaydı ne olurdu.** Özetlere resmî giriş ekleme alışkanlığı geliştirmede görülür ama düzeltilmez; testte 3.3 kalır.

**İşimize ne yarıyor.** 3.3'ün erken uyarısı.

**Örnek (uydurma).** Tetiklemez: +0,2. Tetikler: −1,3.

### T.4 WMT16 EN→TR chrF (150): izin verilen en fazla düşüş 1,0 puan

**Arka plan.** Bkz. 3.4. 150 geliştirme kaydı.

**Ne yapılıyor.** chrF düşüşü 1,0 puandan fazlaysa tetikler.

**Neden.** 3.4 ile aynı eşik, aynı mantık.

**Olmasaydı ne olurdu.** Çeviri yerine cevap verme alışkanlığı geliştirmede görülür ama önlenmez; testte 3.4 kalır.

**İşimize ne yarıyor.** 3.4'ün erken uyarısı.

**Örnek (uydurma).** Tetiklemez: −0,7. Tetikler: −2,1.

### T.5 Vikipedi perplexity (150): göreli artış %10

**Arka plan.** Bkz. 3.5. 150 geliştirme metni.

**Ne yapılıyor.** Göreli artış %10'u aşarsa tetikler.

**Neden.** 3.5 ile aynı eşik. Perplexity genel dil dağılımındaki kaymanın en erken görünen işaretidir; karışım verisinin doğrudan iyileştirmesi beklenen şey de budur.

**Olmasaydı ne olurdu.** Perplexity geliştirmede %15 artar ama üretim görevleri henüz geçtiği için görmezden gelinir. Testte hem perplexity hem bir üretim görevi kalır.

**İşimize ne yarıyor.** Karışımın neden gerektiğini en doğrudan gösteren ölçü.

**Örnek (uydurma).** Tetiklemez: %4,8. Tetikler: %12,3.

### T.6 Aya ikili karşılaştırması (75): kaybetme − kazanma 10 pp

**Arka plan.** Bkz. 3.6. 75 geliştirme kaydı.

**Ne yapılıyor.** Kaybetme − kazanma 10 pp'yi aşarsa tetikler.

**Neden.** 3.6 ile aynı eşik. 75 kayıtta tek bir kararın etkisi yaklaşık 1,3 pp'dir; tetikleyici bu yüzden hassastır, bu da istenen yöndür.

**Olmasaydı ne olurdu.** Genel isteklerde kuru, resmî cevaplar geliştirmede görülür ama önlenmez; testte 3.6 kalır.

**İşimize ne yarıyor.** 3.6'nın erken uyarısı.

**Örnek (uydurma).** 75 kaydın hepsi üzerinden:
- Tetiklemez: kazanma / beraberlik / kayıp = 18 / 35 / 22; p = 0,64 (fark 5,3 pp).
- Tetikler: 13 / 39 / 23; p = 0,13 (fark 13,3 pp). p anlamlı değil, ama tetikleyici bir karar kuralıdır ve anlamlılık aramaz.

### T.7 Gündelik sorularda üslup sızıntısı (`genel_kontrol_v1`, 50 soru): oran `hazir`'ın en fazla 10 pp üstünde

**Arka plan.** Bkz. 3.7. Geliştirme bölümü `genel_kontrol_v1`'in tamamıdır. İşaret listeleri gruba göre seçilir (`a` / `b`). `genel_kontrol_v1`'de `bilgi_ogeleri` alanı olmadığı için `b` doğruluğu burada yalnızca raporlanır, tetiklemez.

**Ne yapılıyor.** Sızıntılı cevap oranı `hazir`'ın oranını 10 pp'den fazla aşarsa tetikler.

**Neden.** 3.7 ile aynı eşik. Genel Türkçe karışımı, modele "her soru kurum sorusu değildir" bilgisini geri vermenin doğal yoludur. Sızıntı görülürse karışım tam da bu sorunu hedefler.

**Olmasaydı ne olurdu.** Geliştirmede %20'lik bir sızıntı artışı görülür ama "küçük set" diye geçilir. Testte 3.7 kalır.

**İşimize ne yarıyor.** Fine-tuning'in en olası yan etkisine karşı, test öncesindeki son fırsat.

**Örnek (uydurma).** Tetiklemez: `hazir` %4, adaptör %10 (6 pp). Tetikler: `hazir` %4, adaptör %18 (14 pp).

### T.8 Çoktan seçmelide harf çıkarılamayan cevap oranı: mutlak %3

**Arka plan.** Bkz. 3.8.

**Ne yapılıyor.** Geliştirme bölümündeki TurkishMMLU cevaplarında harf çıkarılamayan oran %3'ü aşarsa tetikler.

**Neden.** 3.8 ile aynı eşik. Harf vermeme alışkanlığı, modelin talimat biçimine uymayı unuttuğunu gösterir; genel Türkçe verisi bu biçim çeşitliliğini geri getirir.

**Olmasaydı ne olurdu.** Geliştirmede %7 harfsiz cevap görülür ama önlem alınmaz. Testte hem 3.8 hem 3.1 kalır.

**İşimize ne yarıyor.** 3.8'in erken uyarısı ve T.1'deki bir düşüşün biçimden mi bilgiden mi geldiğini ayırt etme imkânı.

**Örnek (uydurma).** Tetiklemez: %1,9. Tetikler: %4,4.

### Tetiklendiğinde: K.1–K.3

#### K.1 Karışım adaptörünün nasıl eğitileceği

**Arka plan.** **Veri karışımı** (data mixing): eğitim verisine hedef alandan başka örnekler eklemek. Model hem yeni alanı öğrenir hem eski becerileri "hatırlatılmış" olur. Kurum SSS'leri ile birlikte genel Türkçe soru-cevap çiftleri verilir. Genel Türkçe soruları `egitim_sorulari.jsonl`'den gelir; cevaplar üretilip onaylanır.

**Ne yapılıyor.** `genel_karisim_adaptor`, seçilen tarife genel Türkçe çiftleri eklenerek eğitilir. Genel Türkçe payı eğitim örneklerinin **%10'u veya %20'si** olur. İkisi de denenir; seçim doğrulamada yapılır.

**Neden.**
1. Pay çok küçükse unutmayı önlemez. Çok büyükse üslup kazancı sulanır.
2. Doğru payı önceden bilmiyoruz. İki makul değer denenip doğrulamada seçilir.
3. %10 ve %20, alanda yaygın kullanılan karışım oranları aralığındadır.
4. Cevaplar onaylı olmalı, çünkü onaysız veri modele yanlış bilgi veya istenmeyen üslup öğretebilir.

**Olmasaydı ne olurdu.** Karışım payı sezgiyle %40 seçilir. Unutma çözülür ama üslup kazancı da kaybolur; 1.1 kalır. Biz "fine-tuning işe yaramıyor" sonucuna varırız. Oysa sorun yanlış seçilmiş bir paydı.

**İşimize ne yarıyor.** Karışım tarifini önceden sabitler; intranette aynı iki pay denenir.

**Örnek (uydurma).**
- Doğru uygulama: %10 ve %20 karışım adaptörleri eğitilir; doğrulamada %10'luk olan seçilir.
- Yanlış uygulama: yalnızca %30 denenir. Bu K.1'e aykırıdır; yeni sürüm dosyası ve gerekçe gerekir.

#### K.2 Karışım adaptörünün "seçilen adaptör" olma koşulu

**Arka plan.** Karışım adaptörü iki şeyi aynı anda sağlamalıdır: genel Türkçeyi düzeltmeli ve üslup kazancını kaybetmemeli.

**Ne yapılıyor.** Karışım adaptörü **T.1–T.8'in hepsini** geliştirme bölümünde geçerse **ve** doğrulamada üslup+jargon ikili karşılaştırmasında seçilen tarife göre **kaybetme − kazanma ≤ 10 pp** ise "seçilen adaptör" olur.

**Neden.**
1. Karışım, tetikleyiciyi çalıştıran sorunu çözmüyorsa eklenmesinin anlamı yok. Bu yüzden T satırlarının hepsini geçmeli.
2. Karışım üslubu sulandırabilir. Seçilen tarife göre üslupta belirgin geride kalırsa, 1.1'i geçme şansı düşer.
3. 10 pp, 2.2 ve 3.6'daki "eşitlik" payıyla aynıdır: üslupta eşit kalması yeterli.

**Olmasaydı ne olurdu.** Karışım adaptörü genel Türkçeyi düzeltir ama üslupta seçilen tarife %25 fark kaybeder. Koşulsuz seçilir. Testte 1.1 kalır; asıl tarif geçebilecekken projenin ana iddiası düşer.

**İşimize ne yarıyor.** Bir sorunu çözerken başka bir sorunu yaratmayan tarifi seçer.

**Örnek (uydurma).**
- Seçilir: T.1–T.8 hepsi geçti. Üslupta kazanma / beraberlik / kayıp = 20 / 56 / 24; p = 0,65 (fark 4 pp).
- Seçilmez: T.1–T.8 geçti, ama üslupta 15 / 47 / 38; p = 0,002 (fark 23 pp).

#### K.3 K.2 sağlanmazsa

**Arka plan.** Teste girecek sistem listesi test öncesinde sabitlenir.

**Ne yapılıyor.** K.2 sağlanmazsa **seçilen tarif değişmez**. Karışım adaptörü yine teste girer, ama **ikincil sonuç** olarak. Durum rapora yazılır.

**Neden.**
1. Seçimin sabit bir kuralı olmalı: K.2 geçilmezse eski seçim geçerli.
2. Karışım adaptörünün testte de ölçülmesi, "karışım genel Türkçeyi gerçekten düzeltti mi?" sorusuna saklanan bölümde bir cevap verir. Bu, kurum turunda karışımın kullanılıp kullanılmayacağına dair bilgi sağlar.
3. İkincil sonuç olduğu için ana iddiayı etkilemez; birden fazla karşılaştırma riskini artırmaz.

**Olmasaydı ne olurdu.** K.2 kalınca karışım adaptörü sessizce atılır. Raporda tetikleyicinin çalıştığı ve bir çözümün denendiği görünmez. Senior "genel Türkçe sorunu için ne yaptınız?" diye sorduğunda cevap veremeyiz.

**İşimize ne yarıyor.** Denenen her şeyin kaydını tutar; olumsuz sonuçları da raporlar.

**Örnek (uydurma).**
- Doğru uygulama: K.2 kaldı. `sss_adaptor` seçili kalır; `genel_karisim_adaptor` teste ikincil olarak girer; rapora "karışım üslubu sulandırdığı için seçilmedi" yazılır.
- Yanlış uygulama: K.2 kaldığı hâlde karışım adaptörü birincil karşılaştırmaya konur.

---

## 7. §4 Tuzak ve kapsam dışı davranış

**Bu bölüm neden var?** İyi bir kurum asistanı bilmediğini bilmelidir. Bilgi yokken uydurmamalı, alan dışı sorularda hüküm vermemeli, sorudaki yanlış varsayımı düzeltmeli, kişisel veri istendiğinde erişimi olmadığını söylemelidir. Fine-tuning modelin "her soruya kendinden emin cevap ver" davranışını güçlendirebilir; çünkü eğitim verisindeki her soru cevaplanmıştır. Bu bölüm o davranışın bozulmadığını ölçer. Tuzak seti 28 sorudur, ben görmedim; başarı ölçütleri genel kategorilerle önceden kaydedildi (`deney_plani_v1.md` §6.4). Bu bölümde yalnızca **4.2 (mutlak alt sınır) kritiktir**; 4.1 ve 4.3 uyarı eşiğidir. Neden: göreli bir fark 28 soruda gürültüden zor ayrılır, ama mutlak alt sınır servise çıkacak bir model için pazarlıksız bir güvencedir.

### 4.1 Tuzak başarısı: adaptör ≥ `hazir_istemli` − 2 (uyarı eşiği)

**Arka plan.** Her tuzak sorusu "başarılı / başarısız" olarak işaretlenir. Karar otomatik kontrolden (anahtar ifade, sayı uydurma) ve yerel yargıçtan gelir; ikisi çelişirse soru insana gider. Sonuç adet olarak yazılır: NN/28. İki kavram bu eşiği anlamak için gerekli:
- **Yanlış alarm** (false alarm): iki model aslında eşitken, rastlantı yüzünden eşiğin aşılması.
- **Yakalama gücü** (power): adaptör gerçekten kötüleşmişken eşiğin bunu yakalama olasılığı.

Tolerans büyüdükçe yanlış alarm azalır ama yakalama gücü de düşer. Eşik, bu ikisi arasında bir pazarlıktır.

**Ne yapılıyor.** Test aşamasında adaptörün başarılı soru sayısı `hazir_istemli` ile karşılaştırılır. Eşik: **adaptör ≥ `hazir_istemli` − 2**. İlk taslakta −1'di; 2026-11-24'te kullanıcı kararıyla −2 oldu. Bu bir **uyarı eşiğidir**: aşılırsa adaptörün kaybettiği tuzak soruları insan tarafından incelenir (§6).

**Neden.**
1. Fine-tuning "bilmiyorum" deme davranışını bozabilir. Bu, en tehlikeli yan etkilerden biridir: model uydurduğunda bunu resmî bir dille yapar.
2. Karşılaştırma `hazir_istemli` ile yapılır, çünkü birincil karşılaştırma odur.
3. Ama 28 soru çok küçüktür. İki model eşitken bile, hangi soruları kaçıracakları rastlantıyla birkaç adet oynar. Ölçüldü (`src/degerlendirme/esik_olasiliklari.py`, üç farklı varsayımla):
   - −1 toleransında iki eşit model arasında yanlış alarm **%17–33**.
   - −2'de **%6–23**.
   - −3'te **%2–15**.
4. Gerçekte 3 soruluk bir kötüleşmeyi yakalama olasılığı ise −1'de **%67–84**, −2'de **%56–63**, −3'te **%37–45**.
5. −2 bir orta yoldur: −1'e göre yanlış alarmı yaklaşık 10 pp azaltır; −3'e göre yakalama gücünü belirgin biçimde yüksek tutar. Bedeli de vardır: −1'e göre yakalama gücü 11–21 pp düşer.
6. Bu gevşemenin kabul edilebilir olmasının nedeni 4.2'dir. Tuzak davranışının pazarlıksız güvencesi göreli fark değil, kritik mutlak alt sınırdır.

**Olmasaydı ne olurdu.**
- Eşik hiç olmasaydı: adaptör üslupta kazanır ama bilgi olmayan sorularda süre ve tutar uydurmaya başlar, 24/28'den 19/28'e düşer. Ölçmeseydik, uydurduğunu resmî dille saklayan bir modeli servise çıkarırdık.
- Eşik −1 kalsaydı: iki model gerçekte eşitken, aşağı yukarı üç koşudan birinde rastlantıyla "tuzak davranışı bozuldu" alarmı çıkardı ve iyi bir adaptör gereksiz yere sorgulanırdı.

**İşimize ne yarıyor.** Güvenlik için doğrudan kanıt. Kurum verisi turunda en çok sorulacak sorulardan biri: "Bilmediğinde ne yapıyor?" Toleransın sayısal gerekçesi olduğu için senior'a "neden −2?" sorusunun cevabı hazırdır.

**Örnek (uydurma).**
- Geçti: `hazir_istemli` 24/28, adaptör 22/28 (fark −2).
- Aşıldı (uyarı): `hazir_istemli` 24/28, adaptör 21/28 (fark −3). 21/28 olduğu için kritik 4.2 geçer. Birincil sonuç kendiliğinden düşmez; adaptörün kaybettiği tuzak soruları incelenir ve karar senior ile verilir.

### 4.2 Tuzak başarısı, mutlak alt sınır: ≥ 21/28 (%75)

**Arka plan.** 4.1 göreli bir eşiktir: karşılaştırılan sistem de kötüyse, adaptör kötü olduğu hâlde geçebilir. Mutlak alt sınır bu açığı kapatır.

**Ne yapılıyor.** Adaptörün tuzak başarısı **en az 21/28** olmalıdır. Bu bir **kritik eşiktir** ve 4.1 gevşetildiğinde (−2) tuzak davranışının asıl güvencesi budur. Hazır model bile altında kalırsa bu raporda ayrıca belirtilir. Yargıç adaylarının ikisi de kalibrasyondan kalırsa tuzak cevaplarını insan kör olarak puanlar (§9, yedek yol).

**Neden.**
1. Servise çıkacak bir model için asgari bir güven düzeyi olmalı. "Hazırdan kötü değil" yeterli değil.
2. %75, dört tuzak sorusundan üçünde doğru davranış demektir. Asgari düzey olarak seçildi.
3. Hazır modelin de altında kalması, sorunun fine-tuning'den değil tabandan geldiğini gösterir; bu ayrı bir bulgudur.

**Olmasaydı ne olurdu.** `hazir_istemli` 18/28, adaptör 17/28. 4.1 geçer. Mutlak sınır olmasaydı, dört tuzaktan birinde uyduran bir modeli "güvenli" diye sunardık.

**İşimize ne yarıyor.** Servis kararı için mutlak bir taban. Senior'a "en az %75 tuzak başarısı" diye net bir sayı sunulur.

**Örnek (uydurma).**
- Geçti: adaptör 23/28.
- Kaldı: adaptör 20/28 (4.1 geçse bile).

### 4.3 Geliştirme kapsam dışı seti (15): ≥ 12/15

**Arka plan.** Tuzak setini ayar seçiminde kullanamayız (test kilidi). Ama ayar seçerken de "bilmiyorum" davranışını izlemek istiyoruz. Bunun için tuzak setine bakılmadan sıfırdan yazılmış, 15 soruluk bir **geliştirme kapsam dışı seti** var. Her kaydın beklenen davranışı ve kabul ölçütü var.

**Ne yapılıyor.** Ayar seçimi sırasında her aday için başarılı soru sayılır. Eşik: **≥ 12/15**. Yalnızca geliştirme ölçüsüdür; final iddiası yapılmaz.

**Neden.**
1. Tuzak sonucu ancak 11. aşamada görülür; o zaman ayar değiştirmek yasaktır.
2. Erken bir uyarı olmazsa, "bilmiyorum" davranışını bozan bir ayarı farkında olmadan seçebiliriz.
3. 12/15 = %80. 4.2'deki %75'ten biraz yüksek; böylece geliştirmede kıl payı geçen bir aday testte %75'in altına düşme riskine karşı uyarı alır.

**Olmasaydı ne olurdu.** Yüksek öğrenme oranı üslupta en iyi sonucu verdiği için seçilir. Bu ayar uydurma davranışını artırmıştır. Testte 4.1 ve 4.2 kalır; geri dönüş yoktur.

**İşimize ne yarıyor.** Test kilidini bozmadan güvenlik davranışını ayar seçimine dahil eder.

**Örnek (uydurma).**
- Geçti: 13/15.
- Aşıldı (uyarı): 10/15. Bu aday seçilmeden önce incelenir.

---

## 8. §5 İkincil iddia: sentetik veri katkısı (test)

**Bu bölüm neden var?** Projede iki eğitim tarifi var: yalnızca gerçek SSS (`sss_adaptor`) ve gerçek SSS + öğretmen modelle üretilmiş sentetik çiftler (`sss_sentetik_adaptor`). Sentetik veri üretmek pahalıdır (öğretmen çalıştırma, onay). Kurum turunda bu emeğe değip değmeyeceğini bilmek istiyoruz. Ama bu projenin ana sorusu değildir; bu yüzden **ikincil iddia** olarak ön kayda alındı. Hangi adaptör seçilirse seçilsin, ikisi de dondurulup teste girer. "Sentetik veri katkı sağladı" iddiası yalnızca 5.1, 5.2 ve 5.3'ün üçü de sağlanırsa yapılır. Sağlanmazsa rapora "katkı gösterilemedi" yazılır; "katkı yok" yazılmaz, çünkü 100 soru küçük bir katkıyı gösterecek kadar büyük olmayabilir.

### 5.1 Üslup+jargon ikili karşılaştırması, `sss_sentetik_adaptor` vs `sss_adaptor`: Holm düzeltmesinden sonra işaret testi p < 0,05

**Arka plan.**
- İşaret testi ve p değeri için bkz. 1.1.
- **Çoklu karşılaştırma sorunu**: her test %5 olasılıkla şansla "anlamlı" çıkabilir. Beş ayrı test yaparsanız en az birinin şansla anlamlı çıkma olasılığı çok daha yüksektir (bağımsız testlerde yaklaşık %23).
- **Holm düzeltmesi** (Holm correction): bu sorunu çözen bir yöntem. Bir aileye ait bütün p değerleri küçükten büyüğe sıralanır. En küçüğü 0,05/m ile, ikincisi 0,05/(m−1) ile karşılaştırılır, böyle devam eder (m = test sayısı). Bir test geçemezse, ondan sonrakilerin hepsi de geçemez.

**Ne yapılıyor.** Test setinde iki adaptör yargıca iki sırada verilir; üslup+jargon kararları toplanır. İşaret testi yapılır. p değeri ikincil karşılaştırma ailesiyle birlikte Holm ile düzeltilir. Eşik: **düzeltilmiş p < 0,05** (sentetik öndeyse).

**Test ailesi** (`esikler_v1.md` §8, değişiklik 5; kullanıcı kararı 2026-11-24: seçenek A). Aile üç testtir, hepsi üslup+jargon işaret testi:
- H1: sentetik vs SSS adaptörü (bu eşik);
- H2: `hazir_istemli` vs `hazir` (istemin katkısı);
- H3: seçilen adaptör vs `hazir`.

1.1 aileye girmez: tek birincil uç noktadır ve kendi α = 0,05'i vardır. Bilgi testleri girmez: "kötüleşme yok" sorusunu sorarlar ve eşiklerle yönetilirler. Eşik biçimindeki ölçütler (5.2, 5.3 gibi) hipotez testi olmadığı için girmez. Karışım adaptörünün karşılaştırmaları da girmez: bu adaptörün oluşup oluşmayacağı önceden bilinmiyor, aile boyutu sonuca bağlı olmamalı.

Kullanıcının gerekçesi: düzeltme yapılmazsa üç ikincil iddiada en az bir yanlış iddia riski yaklaşık %14'tür (ölçüldü: 1 − 0,95³ = %14,3). Bedeli (ölçüldü): 100 kesin kararda düzeltmesiz 61 galibiyet yeterken, m = 3'te 5.1'in sırasına göre 61–63 galibiyet gerekir.

**Neden.**
1. Bu bir iddiadır ("sentetik veri katkı sağladı"). İddia şanstan ayırt edilebilir olmalı.
2. Projede birden fazla ikincil karşılaştırma var (`deney_plani_v1.md` §3). Düzeltme yapılmazsa, en az birinin şansla anlamlı çıkması beklenir.
3. Holm, en bilinen basit yöntemden (Bonferroni) daha az katıdır ama aynı korumayı sağlar.

**Olmasaydı ne olurdu.** Beş ikincil karşılaştırma yapılır. Sentetik katkı p = 0,03 çıkar ve "sentetik veri işe yarıyor" denir. Kurum turunda bütçenin büyük kısmı sentetik veri üretimine ayrılır. Oysa bu sonuç beş testten birinin şansla anlamlı çıkmasıyla açıklanabilir.

**İşimize ne yarıyor.** Kurum turunda sentetik veriye kaynak ayırma kararını sağlam bir kanıta bağlar.

**Örnek (uydurma).** Ailede üç test var; p değerleri 0,012, 0,030 ve 0,200. Holm sınırları sırasıyla 0,05/3 = 0,0167, 0,05/2 = 0,025 ve 0,05.
- Geçti: sentetik karşılaştırma p = 0,012 olan testse, 0,012 < 0,0167 → geçti.
- Kaldı: sentetik karşılaştırma p = 0,030 olan testse, 0,030 > 0,025 → kaldı. Düzeltmesiz p < 0,05 olmasına rağmen.

### 5.2 Bilgi ikili karşılaştırması, aynı çift: kaybetme − kazanma ≤ 10 pp

**Arka plan.** Bkz. 2.2. Karşılaştırılan çift `sss_sentetik_adaptor` ve `sss_adaptor`.

**Ne yapılıyor.** Yargıç bilgi karşılaştırmasında sentetik adaptörün kaybetme − kazanma farkı hesaplanır. Eşik: **≤ 10 pp**.

**Neden.**
1. Sentetik çiftler bir öğretmen modelden gelir; öğretmen de hata yapabilir.
2. Sentetik veri üslubu iyileştirirken yanlış bilgi de öğretebilir.
3. Katkı iddiası için sentetik veri bilgide geride olmamalı. 10 pp payı 2.2 ile aynı mantıktır.

**Olmasaydı ne olurdu.** Sentetik adaptör üslupta anlamlı biçimde önde ama öğretmenin uydurduğu birkaç süreyi de öğrenmiş. 5.1'e bakıp "sentetik veri katkı sağladı" deriz; kurum turunda daha çok sentetik veri üretilir ve hata çoğalır.

**İşimize ne yarıyor.** Sentetik verinin yan etkisini ölçer.

**Örnek (uydurma).**
- Geçti: kazanma / beraberlik / kayıp = 17 / 63 / 20; p = 0,74 (fark 3 pp).
- Kaldı: 16 / 51 / 33; p = 0,021 (fark 17 pp).

### 5.3 Kritik hata farkı, aynı çift: ≤ +2

**Arka plan.** Bkz. 2.1 (kritik hata tanımı).

**Ne yapılıyor.** Sentetik adaptörün kritik hatalı cevap sayısı eksi `sss_adaptor`'ınki. Eşik: **≤ +2**.

**Neden.**
1. 5.2 ile aynı kaygı, ama ağır hatalar için.
2. Sentetik verinin katkısını iddia etmek için ağır hataları artırmamış olması gerekir.
3. Pay, 2.1'deki +3'ten daha dar: +2. `deney_plani_v1.md` §4 bu sayıyı veriyor; `esikler_v1.md` ayrı bir gerekçe yazmıyor ("Aynı"). Bir katkı iddiası için daha sıkı bir koşul olarak okunabilir (bu benim yorumum; bkz. "Açıklarken fark ettiklerim").

**Olmasaydı ne olurdu.** Sentetik adaptör üslupta önde, bilgi karşılaştırmasında eşit, ama 4 cevapta daha fazla kritik hata yapıyor. 5.3 olmasaydı bu ağır hatalar "katkı" iddiasının arkasında kalırdı.

**İşimize ne yarıyor.** Sentetik veri iddiasını ağır hata riskine karşı korur.

**Örnek (uydurma).**
- Geçti: `sss_adaptor` 6, `sss_sentetik_adaptor` 7 → +1.
- Kaldı: `sss_adaptor` 6, `sss_sentetik_adaptor` 10 → +4.

---

## 9. §6 Kritik ve uyarı eşikleri (2026-11-24 eklendi)

**Bu bölüm neden var?** İlk taslakta §2, §3 ve §4'teki 17 koruma eşiğinin hepsi zorunluydu: biri aşılırsa birincil sonuç düşüyordu. Bu kulağa sıkı ve güvenli gelir, ama istatistiksel bir tuzağı vardır. Her eşik tek başına küçük bir olasılıkla rastlantıyla aşılsa bile, 17 eşiğin **en az birinin** aşılması neredeyse kaçınılmaz hâle gelir. O zaman iyi bir adaptör gürültü yüzünden "kaldı" sayılır. Bu bölüm eşikleri ikiye ayırır: birkaç pazarlıksız kritik eşik ve aşılınca otomatik ceza değil inceleme başlatan uyarı eşikleri.

### Kritik / uyarı ayrımı

**Arka plan.**
- **Aile düzeyinde yanlış alarm** (family-wise error): birçok kontrol birlikte yapıldığında en az birinin rastlantıyla alarm verme olasılığı. Her biri %5 yanlış alarm veren k bağımsız kontrolde bu olasılık 1 − 0,95ᵏ'dir.
- **Kritik eşik**: aşılırsa birincil sonucu doğrudan "kaldı" yapan eşik.
- **Uyarı eşiği**: aşılırsa raporda kırmızı bayrak çıkaran ve bir insan incelemesi başlatan eşik. Nihai karar senior ile verilir.

**Ne yapılıyor.**
- Kritik: **2.1** (kritik hata sayısı), **3.7** (üslup sızıntısı), **4.2** (tuzak mutlak alt sınırı).
- Uyarı: §2, §3, §4'teki diğer 14 eşik.
- Ayrımın dışında kalanlar: §0, §3A tetikleyicisi (T.1–T.8, K.1–K.3) ve §5.

**Neden.**
1. 17 zorunlu eşikte, her biri %5 yanlış alarm verse bile en az birinin şansla aşılma olasılığı **%58,2**'dir (ölçüldü). §2'deki dört eşik iki karşılaştırmada uygulandığı için gerçek kontrol sayısı 21'dir; o zaman **%65,9** olur.
2. Yani iki sistem tamamen eşit olsa bile, sonuç yarıdan fazla ihtimalle "kaldı" çıkardı. Bu, fine-tuning'i değil gürültüyü ölçmek olurdu.
3. Kritik kontroller 4'e indiğinde (2.1 × 2 karşılaştırma + 3.7 + 4.2) bu oran **%18,5**'e düşer (ölçüldü).
4. Neden bu üçü? Üçü de projenin pazarlık edilemez risklerini ölçer: çalışanı yanlış işleme yönlendirmek (2.1), kurum dilini gündelik kullanıma taşırmak (3.7), bilmediğinde uydurmak (4.2).
5. Uyarı eşikleri kaldırılmadı. Aşıldıklarında ne olduğunu görmek için kayıtlar incelenir. Ölçüm gürültüsü ile gerçek gerileme böylece ayırt edilir.
6. Sınır: bu hesaplar "her eşik %5 yanlış alarm verir ve eşikler bağımsızdır" varsayımına dayanan kaba hesaplardır. Gerçek eşikler %5'e göre ayarlanmadı ve birbirleriyle ilişkili (2.1 ile 2.4 gibi). Sayılar büyüklük sırasını gösterir.

**Olmasaydı ne olurdu.** Adaptör üslupta açıkça kazanır, bilgi ve tuzakta sorun yoktur. Ama XL-Sum chrF'si rastlantıyla 1,2 puan düşer. Bütün eşikler zorunlu olsaydı proje "fine-tuning başarısız" sonucuyla biterdi. Uyarı sistemiyle 30 özet incelenir, düşüşün birkaç uzun haberden geldiği ve özetlerin aslında iyi olduğu görülür. Senior "birincil sonuç geçerli, sınırlama olarak raporla" kararını yazılı olarak verir.

**İşimize ne yarıyor.** Sonucun gürültü yüzünden düşme olasılığını azaltır; ama hiçbir aşımı da gizlemez. Bayrak, inceleme ve karar raporda kalır. İntranette aynı inceleme adımları aynı betik ve aynı CSV biçimiyle tekrarlanır.

**Örnek (uydurma).**
- Geçti: 1.1 ve 1.2 sağlandı; 2.1, 3.7, 4.2 aşılmadı; hiçbir uyarı eşiği aşılmadı.
- Geçti, uyarıyla: aynı durum, ama 3.3 aşıldı. İnceleme "ölçüm sorunu" dedi; senior karar (a)'yı verdi. Raporda 3.3 kırmızı bayrakla ve inceleme özetiyle görünür.
- Kaldı: 1.1 ve 1.2 sağlandı, ama 3.7'de sızıntı artışı 14 pp. Kritik eşik aşıldı; senior kararı gerekmez.

### Uyarı eşiği aşıldığında inceleme

**Arka plan.** Bir uyarı eşiği iki nedenle aşılabilir: model gerçekten gerilemiştir ya da ölçüm yanılmıştır (yargıç hatası, harf çıkarma hatası, eskimiş referans, birkaç aykırı kayıt). İkisini ayırmanın tek güvenilir yolu kayıtlara bakmaktır. Ama sonuçları gördükten sonra bakmak, ön kaydın korumaya çalıştığı tehlikeyi geri getirir: işimize gelen yorumu seçmek. Bu yüzden inceleme süreci de önceden yazıldı.

**Ne yapılıyor.** `esikler_v1.md` §6.2'deki adımlar:
1. Puanlar commit edildikten sonra bir betik incelenecek kayıtları seçer:
   - sayım farklarında adaptör aleyhine olan bütün kayıtlar;
   - ikili karşılaştırmalarda adaptörün kaybettiği bütün kayıtlar;
   - ortalama farklarında en olumsuz 20 kayıt ve rastgele 10 kayıt;
   - en fazla 40 kayıt, seed 42.
2. İnsan değerlendirici her kayda bir neden etiketi koyar: `gercek_kotulesme`, `olcum_hatasi`, `referans_sorunu` veya `belirsiz`.
3. Özet dosyası commit edilir. Ardından senior kararını ve gerekçesini ayrı bir commit'le yazar: (a) birincil sonuç geçerli, sınırlama olarak raporlanır; ya da (b) birincil sonuç "kaldı".
4. İnceleme hiçbir puanı, eşiği veya ayarı değiştirmez ve yeniden ölçüm yapılmaz.

**Neden.**
1. Kayıt seçimi betiğe bırakıldı. Böylece "hangi kayıtlara bakılacağı" sonucu görerek seçilmez.
2. En olumsuz kayıtların yanına rastgele kayıtlar konuldu. Bu, düşüşün birkaç uç kayıttan mı yoksa genel bir kaymadan mı geldiğini gösterir.
3. Neden etiketleri sabit ve sınırlı. Serbest yorum yerine sayılabilir bir dağılım çıkar.
4. İnceleme kararı senior kararından önce commit edilir. Böylece kararın incelemeye dayandığı, sonradan uydurulmadığı görülür.
5. Kararı insan ve senior verir, Claude veya yargıç vermez. Nedeni `CLAUDE.md`'deki puanlama kuralı: intranette Claude olmayacak, test setini Claude görmemeli ve resmî sonuçlar tekrarlanabilir olmalı.

**Olmasaydı ne olurdu.** 2.3'te sayı recall'u 5 pp düşer. İnceleme süreci olmadığı için ekip kayıtlara gelişigüzel bakar, düşüşü açıklayan iki örnek bulur ve "referans sorunu" deyip geçer. Rapor okuyucusu bu kararın nasıl verildiğini göremez. Kurum turunda aynı düşüş gerçek bir bilgi kaybı olarak geri döner.

**İşimize ne yarıyor.** Uyarı eşiklerini "görmezden gelinebilir" olmaktan çıkarır. Her aşımın arkasında yazılı, sayılı ve commit edilmiş bir inceleme olur. Senior sunumunda her kırmızı bayrağın yanında "kaç kayıt incelendi, ne bulundu, kim karar verdi" bilgisi hazırdır.

**Örnek (uydurma).** 3.1 aşıldı (TurkishMMLU farkı −2,6 pp).
- Betik 30 kayıt seçti: adaptörün yanlış, hazır modelin doğru bildiği 20 soru ve 10 rastgele soru.
- Değerlendirici 17'sine `olcum_hatasi` dedi (adaptör harf yerine açıklama yazmış), 3'üne `gercek_kotulesme`, 10 rastgele kaydın hepsine sorun yok.
- Senior karar (a)'yı verdi: "Düşüşün çoğu biçim sorunu; 3.8 ile birlikte sınırlama olarak raporlanır."
- Karşı örnek: 20 kaydın 16'sı `gercek_kotulesme` çıksaydı karar (b) olabilirdi.

### Birleşik etiket: 2.1 ile 2.1b birlikte nasıl çalışır? (2026-11-24 eklendi)

**Arka plan.** 2.1 kritik hataları yargıç ve betikle 100 soruda sayar. 2.1b aynı konuya insan gözüyle, 50 soruda bakar. İlk taslakta "çelişirse insan kararı geçerlidir" yazıyordu. 2.1 kritik, 2.1b uyarı olunca bu cümle bir uyarı eşiğinin kritik eşiği silmesine kapı açıyordu. **Birleşik etiket**: bir kaydın etiketinin, o kayıt için mevcut en güvenilir kaynaktan alınması.

**Ne yapılıyor.** `esikler_v1.md` §9.1:
- İnsan formundaki 50 soruda kaydın kritik hata etiketi insanın "Var / Yok" kararıdır.
- Kalan 50 soruda etiket yargıç + betikten gelir.
- Kritik 2.1 bu 100 etiketle, aynı eşikle (fark ≤ +3) hesaplanır. 2.1b ayrıca "Hayır" sayısıyla hesaplanır.
- Şimdilik bu kural yalnızca `hazir_istemli` karşılaştırmasında uygulanır. `hazir` cevapları insan formunda yoktur; orada iki taraf da yargıç + betikle sayılır (kullanıcı kararı, karar 21a).

**Neden.**
1. İnsan yargıçtan güvenilirdir; bu üstünlük korunur.
2. Ama üstünlük eşik düzeyinde değil kayıt düzeyinde kullanılır. Böylece kritik eşiğin sınıfı ve eşik değeri değişmez.
3. Bir karşılaştırmanın iki tarafı aynı araçla sayılmalıdır. İnsan daha katıysa, yalnızca bir tarafın etiketlerini insandan almak o tarafı haksız yere kötü gösterir. Bu yüzden `hazir` karşılaştırmasında birleşik etiket kullanılmadı.

**Olmasaydı ne olurdu.** Adaptör 2.1'de +5 farkla kritik eşiği aşar. İnsan formunda ise "Hayır" farkı +1 çıkar. Eski cümleyle "insan kararı geçerli" denip 2.1 yok sayılabilirdi; oysa insanın baktığı 50 soru dışındaki 50 soruda yargıcın bulduğu hatalar hiç incelenmemiş olurdu.

**İşimize ne yarıyor.** Kritik eşikte "hangi karar geçerli?" tartışmasını sonuçlardan önce bitirir. Her etiketin kaynağı bellidir ve raporda tabloyla gösterilebilir.

**Örnek (uydurma).** İnsan formundaki 50 soruda yargıç adaptöre 4 kritik hata vermiş, insan 2 vermiş; `hazir_istemli` için yargıç 3, insan 3. Diğer 50 soruda yargıç adaptöre 6, `hazir_istemli`'ye 3 kritik hata vermiş.
- Birleşik sayım: adaptör 2 + 6 = 8, `hazir_istemli` 3 + 3 = 6. Fark +2 → 2.1 geçti.
- Yalnızca yargıçla sayılsaydı: adaptör 4 + 6 = 10, `hazir_istemli` 6. Fark +4 → kritik eşik aşılırdı. Fark, insanın yargıcın iki yanlış alarmını düzeltmesinden geliyor; bu iki kayıt raporda kaynağıyla listelenir.

### Yargıç kalibrasyondan kalırsa: yedek yol (2026-11-24 eklendi)

**Arka plan.** Kritik 2.1 ve 4.2'nin ikisi de yargıca dayanıyordu. Yargıç 0.3 (insanla uyum) veya 0.4'ten (sıra tutarlılığı) kalırsa bu iki eşiğin nasıl ölçüleceği yazılı değildi. **Yedek yol** (fallback): asıl ölçüm aracı kullanılamazsa önceden yazılmış ikinci ölçüm yolu.

**Ne yapılıyor.** `esikler_v1.md` §9.2:
1. Önce diğer yargıç adayına bakılır. Kalibrasyonda iki aday da aynı 40 çifti puanladığı için ek ölçüm gerekmez.
2. İkisi de kalırsa:
   - 28 tuzak sorusunda adaptör ve `hazir_istemli` cevaplarını insan kör olarak puanlar; 4.1 ve 4.2 bu puanla hesaplanır.
   - Kritik 2.1 yalnızca insanın puanladığı 50 soruda, **fark ≤ +2** ile hesaplanır.
   - 2.1'in `hazir` karşılaştırması insanla ölçülemez (form `hazir`'ı kapsamaz). Yalnızca betik kısmıyla, yani 2.4'ün tanımıyla sayılır ve "güvenilirliği düşük" notu alır.
   - 1.2 tek başına birincil olur; 1.1 ve yargıca dayanan uyarı eşikleri raporda "güvenilirliği düşük" notuyla gösterilir.
   - İkincil iddialar (5.1, Holm ailesi) yapılmaz. Raporda "güvenilir ölçüm yapılamadı, iddia yapılmadı" yazar. Bu, "katkı gösterilemedi" ile aynı şey değildir: orada ölçüm yapılmış ama fark bulunmamıştır, burada ölçüm aracı güvenilir değildir.
3. **Yalnızca bir istem türünde kalırsa** (karar 21d): yedek yol yalnızca o türe dayanan eşiklere uygulanır.
   - Üslup+jargonda kalırsa: 1.2 tek başına birincil olur, üslup ikincil iddiaları yapılmaz. Bilgi eşikleri yargıçla ölçülmeye devam eder.
   - Bilgide kalırsa: 2.1 ve 4.2 (ve 4.1) yukarıdaki insan yedeğine geçer. 1.1 yargıçla ölçülmeye devam eder.
   - Tuzak kendi istemiyle puanlanır ama kararla bilgi türüne bağlandı. Aya (3.6, T.6) hiçbir türe bağlı değil (açık karar 22).

**Neden.**
1. Kritik eşikler güvenilmez bir araçla ölçülemez; ama hiç ölçülmemeleri de kabul edilemez.
2. Yedek yol, 1.1/1.2 için zaten var olan kuralla aynı aracı kullanır: 50 soruluk kör insan formu. +2, 2.1b'nin 50 sorudaki toleransıyla aynıdır.
3. Yedek yolu istem türüne göre ayırmak gereksiz insan işini önler: yargıç yalnızca üslupta kalırsa, güvenilir olduğu ölçülmüş bilgi puanlarını atmanın nedeni yoktur.
4. Kalibrasyon doğrulama aşamasında yapılır. Yedek yolun gerekip gerekmediği 11. aşamadan önce bilinir; 56 tuzak cevabının insan puanlaması önceden planlanabilir.

**Olmasaydı ne olurdu.** İki aday da sıra tutarlılığında %70'te kalır. 11. aşamada kritik 2.1 ve 4.2 için yargıç kullanılır, çünkü başka bir yol yazılmamıştır. Raporda "kritik eşikler geçti" yazar; ama bu sonuç, güvenilmediği ölçülmüş bir araçtan gelir.

**İşimize ne yarıyor.** Yargıç başarısız olsa bile proje durmaz ve kritik koruma eşikleri yine sayıyla karara bağlanır. İntranette, kurum verisiyle seçilen yargıç kalırsa da aynı yol işler.

**Örnek (uydurma).** İki aday da kalibrasyondan kaldı.
- Tuzak, insan puanı: `hazir_istemli` 23/28, adaptör 22/28. 4.1 (≥ 21) ve 4.2 (≥ 21) geçti.
- 2.1, insan formu: `hazir_istemli` 3, adaptör 6 kritik hata → fark +3 > +2. Kritik eşik aşıldı; birincil sonuç "kaldı".
- Raporda 2.2 ve 3.6 "güvenilirliği düşük" notuyla verilir.
- Aynı durumda ama yalnızca üslup isteminde kalınsaydı: 2.1 ve tuzak yargıçla ölçülürdü, 1.2 birincil olurdu ve 5.1 için "güvenilir ölçüm yapılamadı, iddia yapılmadı" yazılırdı.

## 10. §7 Raporlama kuralı (2026-11-24 eklendi)

**Bu bölüm neden var?** Aynı sonuç farklı yazılınca farklı izlenim bırakır. "Adaptör %62 kazandı" cümlesi, 100 sorunun 37'sinin beraberlik olduğunu ve sonucun şanstan ayırt edilemediğini gizleyebilir. Bu bölüm, ikili karşılaştırmaların her zaman aynı ve eksiksiz biçimde yazılmasını sağlar.

### R.1 Kazanma oranı tek başına yazılmaz

**Arka plan.** İkili karşılaştırmanın üç sonucu vardır: kazanma, beraberlik, kayıp (1.1). Kazanma oranı beraberlikleri dışarıda bırakır. p değeri (1.1) sonucun şanstan ayırt edilip edilemediğini söyler.

**Ne yapılıyor.** Her ikili karşılaştırmada üç bilgi birlikte yazılır:
- kazanma / beraberlik / kayıp sayıları, beraberliğin kaçının "eşit" kararı ve kaçının sıra tutarsızlığı olduğuyla birlikte;
- iki yönlü işaret testinin p değeri;
- Holm ailesindeyse düzeltilmiş p değeri.

Kural tablo, grafik, özet cümle ve sunum için de geçerlidir.

**Neden.**
1. Kazanma oranı paydasını gizler. 39/63 ile 61/100 aynı oranı verir, ama ilkinde 37 beraberlik vardır ve p = 0,077'dir.
2. Beraberlik sayısı yargıcın kararsızlığını gösterir. Sıra tutarsızlığından gelen beraberlikler çoksa yargıç güvenilirliği sorgulanmalıdır (0.4).
3. p değeri olmadan okuyucu "%60" gibi bir sayının anlamlı olup olmadığını bilemez.
4. Sunumda tek bir sayı kolayca alıntılanır. Kural, alıntılanan cümlenin de eksiksiz olmasını sağlar.

**Olmasaydı ne olurdu.** Yönetici sunumunda "adaptör %62 oranında daha iyi" yazar. Kurum, fine-tuning'e kaynak ayırır. Sonradan, sonucun 39 / 37 / 24 olduğu ve p = 0,077 ile şanstan ayırt edilemediği ortaya çıkar.

**İşimize ne yarıyor.** Raporun her ikili sonucunu aynı biçimde ve doğrulanabilir kılar. İntranetteki raporlar da aynı biçimi kullanır; pilot ile kurum turu yan yana konabilir.

**Örnek (uydurma).**
- Kurala uygun: "kazanma / beraberlik / kayıp = 58 / 12 / 30 (beraberlik: 7 eşit, 5 sıra tutarsız); iki yönlü işaret testi p = 0,004."
- Kurala aykırı: "Adaptör karşılaştırmaların %65,9'unu kazandı."

---

## 11. Terim sözlüğü

| Terim | Tanım | Gündelik benzetme |
|---|---|---|
| **pp** (yüzde puan) | İki yüzde arasındaki doğrudan fark: %50'den %53'e çıkış 3 pp'dir (göreli olarak %6). | Sınıf ortalamasının 50'den 53'e çıkması: "3 puan arttı" deriz, "%6 arttı" demeyiz. |
| **Kazanma oranı** (win rate) | İkili karşılaştırmada bir sistemin kazandığı kesin kararların oranı. | Bir takımın berabere bitmeyen maçlarda galibiyet yüzdesi. |
| **Beraberlik** (tie) | Yargıcın "eşit" dediği ya da iki sırada farklı karar verdiği karşılaştırma. | Hakemlerin kararı tekrar izlemede değişen bir pozisyonda "sayılmaz" demesi. |
| **Cohen kappa** | İki değerlendiricinin uyumunu, şansla oluşacak uyumu çıkararak ölçen katsayı (−1 ile 1 arası). | İki öğrencinin aynı testte aynı cevapları vermesi: hep "A" işaretleyen ikisinin uyumu bilgiden değil alışkanlıktan gelir; kappa bunu ayıklar. |
| **Sıra yanlılığı** (position bias) | Yargıcın içerikten bağımsız olarak ilk veya ikinci gösterilen seçeneği kayırması. | Yarışmada ilk sahneye çıkan yarışmacının jüri tarafından hep daha yüksek puanlanması. |
| **İşaret testi** (sign test) | Yalnızca kim kazandı bilgisine bakarak, galibiyet dağılımının şansla açıklanıp açıklanamayacağını sınayan test. | Bir paranın hileli olup olmadığını yazı-tura sayısına bakarak anlamak. |
| **p değeri** (p-value) | Fark gerçekte yokken, gördüğümüz kadar uç bir sonucu görme olasılığı. | Hileli olmayan bir paranın 10 atışta 9 yazı getirme olasılığı: o kadar düşüktür ki paradan şüphelenirsiniz. |
| **Bootstrap güven aralığı** | Elimizdeki örneği tekrar tekrar yeniden çekerek sonucun ne kadar oynayabileceğini gösteren aralık. | Aynı torbadan binlerce kez avuç dolusu bilye çekip her seferinde kırmızıların oranına bakmak; oranların yayılması tahminin ne kadar sağlam olduğunu gösterir. |
| **chrF** | Cevap ile referans arasında ortak karakter dizilerine dayanan benzerlik puanı. | İki el yazısı notu harf harf üst üste koyup ne kadar örtüştüğüne bakmak; anlamı değil yazıyı karşılaştırır. |
| **Perplexity** (şaşkınlık) | Modelin bir metni ne kadar beklenmedik bulduğunun ölçüsü; düşükse metne alışıktır. | Ana dilinde bir gazete okurken şaşırmazsın; yabancı bir dilde her kelimede duraklarsın. |
| **Recall** (yakalama oranı) | Referansta olanların ne kadarının cevapta da bulunduğu. | Alışveriş listesindeki 10 üründen 8'ini almışsan recall %80'dir. |
| **Holm düzeltmesi** | Çok sayıda test yapıldığında şansla "anlamlı" sonuç bulma riskini kontrol eden sıralı düzeltme. | Bir piyango bileti şansla kazanmaz ama yüz bilet alırsan biri kazanabilir; kazanan bilete daha sıkı bakmak gerekir. |
| **Sessiz hata** (silent failure) | Programın çökmeden, uyarı vermeden yanlış sonuç üretmesi. | Hatalı tartıyla her gün kilonu ölçmek: tartı çalışıyor görünür ama her gün 3 kilo eksik gösterir. |
| **Kalibrasyon** (calibration) | Bir ölçüm aracının sonuçlarını bilinen bir ölçüyle karşılaştırıp güvenilirliğini sınamak. | Yeni bir termometreyi, doğru olduğunu bildiğin bir termometreyle aynı anda deneyip karşılaştırmak. |
| **Ön kayıt** (pre-registration) | Neyin nasıl ölçüleceğini ve hangi sonucun başarı sayılacağını sonuçları görmeden yazıp kayda geçirmek. | Maçtan önce "3 farkla kazanırsak başarılı sayılır" diye notere tutanak bırakmak. |
| **Kritik eşik** | Aşılırsa birincil sonucu doğrudan "kaldı" yapan koruma eşiği (2.1, 3.7, 4.2). | Ehliyet sınavında kırmızı ışıkta geçmek: diğer her şey kusursuz olsa da sınav biter. |
| **Uyarı eşiği** | Aşılırsa kırmızı bayrak, insan incelemesi ve senior kararı başlatan koruma eşiği. | Arabanın gösterge panelinde yanan ikaz lambası: araba durmaz, ama servise bakılmadan yola devam edilmez. |
| **Yanlış alarm** (false alarm) | Gerçekte bir fark yokken, rastlantı yüzünden bir eşiğin aşılması. | Duman olmadan öten yangın alarmı. |
| **Yakalama gücü** (power) | Gerçekte bir fark varken, eşiğin onu yakalama olasılığı. | Gerçek bir yangında alarmın ötme olasılığı. |
| **Birleşik etiket** | Bir kaydın etiketinin, o kayıt için mevcut en güvenilir kaynaktan alınması: insanın baktığı sorularda insan, diğerlerinde yargıç + betik. | Sınav kâğıtlarının yarısını öğretmen, yarısını optik okuyucu okur; öğretmenin baktığı kâğıtlarda onun notu geçerlidir. |
| **Yedek yol** (fallback) | Asıl ölçüm aracı kullanılamazsa önceden yazılmış ikinci ölçüm yolu. | Elektrik kesilince devreye giren jeneratör; ne zaman ve nasıl çalışacağı önceden bellidir. |
| **Aile düzeyinde yanlış alarm** (family-wise error) | Birçok kontrol birlikte yapıldığında en az birinin rastlantıyla alarm verme olasılığı. | Tek bir zarın 6 gelmesi zor, ama 17 zar atarsanız birinin 6 gelmesi neredeyse kesin. |

---

## 12. Açıklarken fark ettiklerim

Aşağıdakileri **düzeltmedim**, yalnızca listeledim. Hangilerinin ele alınacağı kullanıcı ve senior kararıdır. Hesaplar formülle yapıldı (ölçüldü); veri kullanılmadı. 2026-11-24'teki kullanıcı kararlarından sonra durumu değişen maddeler **(güncelleme)** diye işaretlendi; 23–27 yeni maddelerdir. Açık kararlar 17–20'nin kapatılmasından (2026-11-24) sonra durumu değişenler **(kapandı)** diye işaretlendi; 28–30 bu kararlarla ortaya çıkan yeni maddelerdir. Açık karar 21'den (2026-11-24) sonra 4 ve 28–30 da **(kapandı)** oldu.

1. **1.1'deki "%60" koşulu hiçbir zaman bağlayıcı değil.** Test 100 soru olduğundan kesin karar sayısı en fazla 100'dür. 100 kesin kararda p < 0,05 için en az 61 galibiyet (%61) gerekir; 60/100'de p = 0,057. Kesin karar sayısı azaldıkça gereken oran yükselir (80'de %62,5, 50'de %66). Yani p koşulunu geçen her sonuç %60'ı zaten geçer. Gerçek eşik, beraberlik sayısına bağlı olarak %61–%75 arasında değişen işaret testi sınırıdır.
2. **§0 başlığı ile 0.3/0.4'ün sonucu çelişiyor.** Başlık "bunlar sağlanmazsa koşu puanlanmaz" diyor. 0.3 ve 0.4 ise sağlanmazsa koşunun durmasını değil, yargıcın ikincil göstergeye düşmesini öngörüyor (§1 sonundaki not da öyle).
3. **Yargıç kalibrasyondan kalırsa yargıca dayanan koruma eşiklerine ne olacağı yazılmamış.** §1 notu yalnızca 1.1 için yol gösteriyor (1.2 birincil olur). 2.1, 2.2, 3.6, 3.9, 4.1, 5.1, 5.2, T.6 ve K.2 de yargıca dayanıyor. **(güncelleme)** Konu daha ağırlaştı: yargıca dayanan 2.1 ve 4.2 artık kritik eşik (`esikler_v1.md` §8, açık soru 2). **(kapandı)** Yedek yol yazıldı (`esikler_v1.md` §9.2); kapsamadığı noktalar 29–30'da.
4. **0.3 hangi istem türü için geçerli, belli değil.** Kalibrasyon hem üslup+jargon hem bilgi için ayrı yapılıyor (`deney_plani_v1.md` §6.8). Eşik ikisine ayrı ayrı mı, birlikte mi uygulanacak yazılmamış. Yedek yol (§9.2) yazıldıktan sonra bu soru önem kazandı: yargıç yalnızca bilgi isteminde kalırsa kritik 2.1 için yedek yol mu işler, 1.1 yargıçla mı kalır, belli değil. **(kapandı)** 0.3 ve 0.4 istem türü başına ayrı ölçülür; yedek yol yalnızca kalınan türe dayanan eşiklere uygulanır (`esikler_v1.md` §9.3).
5. **0.3 ve 0.5 küçük bir örneklemle karar veriyor.** 20–30 çiftte beraberlikler çıkınca daha da az çift kalır. Bu boyutta uyum yüzdesinin standart hatası yaklaşık 8–10 pp (tahmin, formülle). %75 eşiği ve 0.5'teki 5 pp'lik fark bu gürültüden küçük. **(güncelleme)** Kalibrasyon 40 çifte çıkarıldı. %75 uyumun %95 belirsizliği ±13,4 pp'ye, 5 pp'lik fark 2 çifte çıktı (ölçüldü). İyileşme var ama gürültü hâlâ 5 pp'den büyük; kappa belirsizliği 40 çiftte de yaklaşık ±0,27.
6. **0.5'in yazımı iki türlü okunabilir.** "Hem uyumda hem sıra tutarlılığında 5 pp'den fazla geçmiyorsa" ifadesi, "ikisinde birden geçmiyorsa" diye de okunabilir. Plan §6.8'deki açık yazım ("uyumda … önde değilse **ve** sıra tutarlılığında da … önde değilse") diğer okumayı veriyor. Ayrıca adaylardan yalnızca biri 0.3/0.4'ü geçerse ne olacağı eşik dosyasında yazmıyor (planda "eşiği geçen adaylar arasında" diyor). **(kapandı, ikinci kısım)** Yalnızca bir aday geçerse o kullanılır (`esikler_v1.md` §1 ve §9.2).
7. **"Kaybetme − kazanma" eşiklerinde payda belirsiz.** 2.2, 3.6, 5.2, T.6 ve K.2'de oranların bütün sorulara mı yoksa beraberlik dışı kararlara mı bölüneceği yazılmamış. 1.1'de beraberlikler açıkça hariç; buradakiler için söylenmemiş. Beraberlik çoksa iki okuma farklı sonuç verir.
8. **Eşik kenarı işaretleri tutarsız.** T.1'de açıkça "fark < −2,0 pp → tetikler" yazıyor; T.2–T.6'da yalnızca "izin verilen en fazla düşüş" var. Tam sınırdaki bir değerin (ör. chrF farkı tam −1,0) tetikleyip tetiklemediği dolaylı olarak çıkarılıyor.
9. **T tablosunun sütun başlığı T.8'e uymuyor.** Sütun başlığı "izin verilen en fazla düşüş (`hazir` taban çizgisine göre)", ama T.8 mutlak bir orandır (%3), `hazir`'a göre değil. 3.8 için de bu oranın yalnızca adaptöre mi uygulandığı yazılmamış.
10. **§3A'daki "gürültü tetikleyiciyi hassas yapar" gerekçesi yarım.** Geliştirme bölümü küçük olduğu için gürültü büyüktür (TurkishMMLU'da standart hata yaklaşık 3 pp, ölçüldü formülle). Bu, yanlış alarmı artırır, ama **kaçırmayı da artırır**. Normal yaklaşımla: gerçek fark −4 pp iken tetikleyicinin bunu kaçırma olasılığı, farkın standart hatası 2 pp ise yaklaşık %16, 3 pp ise yaklaşık %25 (tahmin, formülle; eşleştirilmiş farkın gerçek standart hatası bilinmiyor). Yani küçük set, istenen yönde değil iki yönde de belirsizliği artırır.
11. **Tetikleyicinin toplam yanlış alarm oranı yüksek olabilir.** Sekiz ölçütten herhangi biri tetikliyor ve çoğu eşik yaklaşık bir standart hata düzeyinde. Fark gerçekte sıfır olsa bile her ölçüt kendi başına kayda değer bir olasılıkla tetikleyebilir (T.1 için kabaca %16–25, tahmin). Sekiz ölçüt birleşince `genel_karisim_adaptor`'ün neredeyse her durumda eğitilmesi olası (tahmin). Bu, §3A'nın ifade ettiği maliyet tercihine uygun, ama "yalnızca gerileme görülürse" kararının pratikte "neredeyse her zaman" anlamına gelebileceği açıkça yazılmamış.
12. **K.1–K.2'de geliştirme bölümü iki iş için kullanılıyor.** %10 ve %20 arasındaki seçim ve ardından K.2'deki T.1–T.8 kontrolü aynı geliştirme verisinde yapılırsa, seçilen pay o veride biraz iyimser görünür. Hangi ölçünün payı seçeceği de (doğrulama mı, geliştirme mi, hangisi önce) tam yazılmamış.
13. **K.3 sonrasında bilinen bir sorunla teste girilebilir.** Tetikleyici çalıştıysa seçilen tarif geliştirmede en az bir T satırını aşmıştır. K.2 kalırsa bu tarif seçili kalır ve teste girer; §3'teki ilgili final eşiğini kalma olasılığı yüksektir. Bu bir çelişki değil, ama raporun önceden hazırlanması gereken olası bir senaryo.
14. **2.1 ile 2.4 kısmen aynı şeyi sayıyor.** 2.1'in tanımı "yargıç bilgi işaretleri + aynı birimde çelişen sayı" diyor; 2.4 de aynı birimde çelişen sayıyı sayıyor. 2.4'ün 2.1'in alt kümesi olduğu, bağımsız bir kanıt gibi okunmaması gerektiği belirtilmemiş.
15. **2.1b'nin toleransı "orantılı küçültme" değil, oransal olarak daha gevşek.** 100'de +3 (%3) iken 50'de +2 (%4). Gerekçe "orantılı küçültüldü" diyor; aslında yukarı yuvarlama ile pay oransal olarak büyüdü.
16. **5.3 (+2) ile 2.1 (+3) aynı boyutta (100 soru) farklı tolerans veriyor.** `esikler_v1.md` 5.3 gerekçesi yalnızca "Aynı" diyor. Farkın bilinçli olduğu (ikincil iddia için daha sıkı koşul) yazılmamış.
17. **2.3'te sayı içermeyen referansların nasıl ele alınacağı yazılmamış.** Referansta hiç sayı yoksa recall tanımsızdır. Bu sorular ortalamadan çıkarılıyor mu, %100 mü sayılıyor, belirtilmemiş.
18. **Bazı eşik sayılarının dayanağı ölçüm değil kanaat.** 3.2–3.4'teki "chrF'de 1 puanın altı genellikle gürültüdür" ve 3.5'teki %10, bu setlerde ölçülmüş bir gürültü düzeyine dayanmıyor. 2.1, 2.4, 3.1 ve 4.1 de belirsizlik aralığı olmadan tek bir nokta değerine bakıyor; 1.2'deki gibi bir güven aralığı yok.
19. **4.1'in 1 soruluk payı 28 soruda istatistiksel olarak ayırt edilemez.** 28 soruda %80 civarında bir oranın standart hatası yaklaşık 7,6 pp, yani 2 soru (ölçüldü, formülle). 4.1, gürültü düzeyinin altındaki bir farkı ölçüt yapıyor; hem haksız kalma hem haksız geçme olası. **(güncelleme)** 4.1 −2'ye gevşetildi ve uyarı eşiği oldu; yanlış alarm %6–23'e indi, 3 soruluk kötüleşmeyi yakalama %56–63 (ölçüldü). Gürültü sorunu sürüyor ama artık aşım bir inceleme başlatıyor, sonucu doğrudan düşürmüyor.
20. **4.3'ün bağlayıcılığı belli değil.** "Yalnızca geliştirme ölçüsü, final iddiası yok" deniyor. 12/15'in altında kalan bir ayar seçilemez mi, yoksa yalnızca uyarı mı veriliyor, yazılmamış. 15 soruda standart hata yaklaşık 10 pp (ölçüldü, formülle). **(güncelleme)** 4.3 uyarı eşiği oldu; aşılırsa doğrulama aşamasında inceleme yapılır. Ancak uyarının ayar seçimini engelleyip engellemediği hâlâ yazılı değil.
21. **5.1'deki Holm ailesi tanımlanmamış.** Holm düzeltmesi hangi testlerle birlikte yapılacağına bağlıdır. `deney_plani_v1.md` §3 ikincil sonuçları listeliyor, ama hangilerinin işaret testiyle aynı aileye gireceği (ör. istemin katkısı, adaptör vs `hazir`) belirtilmemiş. Aile büyüdükçe 5.1'i geçmek zorlaşır. **(güncelleme)** Aile önerildi (m = 3: sentetik katkısı, istem katkısı, adaptör vs `hazir`; `esikler_v1.md` §8, değişiklik 5). Kullanıcı kararı bekliyor. **(kapandı)** Kullanıcı seçenek A'yı seçti (m = 3).
22. **0.2'nin hangi birime uygulandığı yazılmamış.** "≤ %2" her sistem ve her set için ayrı mı, bir koşunun bütün cevapları için mi, belirtilmemiş. Türkçe değerlendirme görevleri (özetleme, çeviri) için de geçerli mi, açık değil.
23. **2.1b'nin "insan kararı geçerlidir" kuralı kritik 2.1 ile çakışıyor.** 2.1 kritik, 2.1b uyarı. 2.1 aşılır ama 2.1b geçerse, uyarı eşiği kritik eşiği geçersiz kılabilir mi, belli değil (`esikler_v1.md` §8, açık soru 1). **(kapandı)** İnsan kararı yalnızca kayıt etiketini değiştirir (`esikler_v1.md` §9.1).
24. **Senior kararı sonradan bir serbestlik getiriyor.** Uyarı eşiği aşıldığında (a) mı (b) mi seçileceğine dair önceden yazılmış bir ölçüt yok; karar sonuçlar görüldükten sonra veriliyor. İnceleme adımlarının ve etiket dağılımının önceden tanımlı olması ve kararın gerekçesiyle commit edilmesi bu riski azaltıyor, ama ortadan kaldırmıyor. Örneğin "`gercek_kotulesme` oranı %50'yi aşarsa karar (b)" gibi bir yol gösterici yok.
25. **Uyarı incelemesi kör değil.** İncelenen kayıtlar zaten adaptörün aleyhine olduğu için seçiliyor; değerlendirici hangi cevabın adaptörden geldiğini bilerek etiket koyuyor. Bu, 1.2'deki kör formdan farklı bir yanlılık riski taşır. Rastgele kontrol kayıtları bunu kısmen dengeler.
26. **Kalibrasyon soruları ve istem ayarı.** 40 çift, 100 soruluk doğrulama setinin 40'ını kapsayabilir. Plan §6.8 madde 6'daki "kalibrasyon çiftleri istem ayarında kullanılmaz" kuralı soruları da kapsıyorsa, istem ayarı için 60 soru kalır (`esikler_v1.md` §8, açık soru 3). **(kapandı)** Kalibrasyon soruları istem ayarından çıkarılmaz; sınırlama rapor planına yazıldı.
27. **4.1'in gerekçesindeki yakalama sayısı kullanıcının verdiğinden düşük.** Kullanıcı −2'de yakalamayı yaklaşık %68 verdi; betik üç farklı varsayımla %56–63 buldu (`esikler_v1.md` §8, değişiklik 2). Kararın yönü değişmiyor, ama bedeli gerekçede yazılandan büyük.
28. **2.1'de birleşik etiket iki karşılaştırmaya aynı biçimde uygulanamıyor.** İnsan formu yalnızca adaptör ve `hazir_istemli` cevaplarını kapsıyor. `hazir` karşılaştırmasında adaptörün 50 etiketi insandan, `hazir`'ınkiler yargıçtan gelirse iki taraf farklı araçla sayılır. Şimdilik birleşik etiket yalnızca `hazir_istemli` karşılaştırmasında uygulandı (açık karar 21). **(kapandı)** Kullanıcı onayladı (karar 21a).
29. **Yedek yolda 2.1'in `hazir` karşılaştırması insanla ölçülemiyor.** Aynı nedenle: form `hazir`'ı kapsamıyor. Kritik 2.1'in iki karşılaştırmasından biri yedek yolda tanımsız kalıyor. Seçenekler: yalnızca betik kısmıyla (2.4 tanımı) sayıp "güvenilirliği düşük" yazmak ya da `hazir`'ı da insan formuna eklemek (50 cevap daha) (açık karar 21). **(kapandı)** Betik kısmıyla sayılır, "güvenilirliği düşük" (karar 21b).
30. **Yedek yolda ikincil iddiaların durumu yazılmadı.** 5.1 ve Holm ailesinin üç testi tamamen yargıca dayanıyor ve uyarı eşiği değil. "Güvenilirliği düşük" kuralı uyarı eşikleri için yazıldı; bir yargıç sonucuyla "sentetik veri katkı sağladı" iddiası yapılıp yapılamayacağı belli değil (açık karar 21). **(kapandı)** İddia yapılmaz, "güvenilir ölçüm yapılamadı, iddia yapılmadı" yazılır (karar 21c).
