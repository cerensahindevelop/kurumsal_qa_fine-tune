# Rapor planı v1

Durum: taslak (01, 2026-11-23), senior onayı: bekliyor
Bağlı dosyalar: `degerlendirme/deney_plani_v1.md`, `degerlendirme/esikler_v1.md`

Senior raporu 11. aşamadaki bütün puanlar üretilip commit edildikten sonra yazılır. Bu dosya raporun iskeletini ve önceden bilinen sınırlamaları sonuçlardan önce kayda geçirir; böylece sınırlamalar sonuca göre seçilmez.

## 1. Bölümler

1. **Özet:** birincil sonuç tek cümleyle (geçti / geçmedi), ardından koruma koşulları.
2. **Yöntem:**
   - sistemler, veri ve bölmeler (sayı ve SHA-256 ile);
   - eğitim tarifi;
   - üretim ayarları;
   - yargıç seçimi (kalibrasyon sonuçları);
   - insan formu.
3. **Birincil sonuç:** seçilen adaptör vs `hazir_istemli` (yargıç üslup+jargon; insan formu, 50 soru).
4. **Koruma koşulları:** bilgi doğruluğu, genel Türkçe (saklanan bölüm), tuzak (NN/28).
5. **İkincil sonuçlar:**
   - sentetik katkısı;
   - istem katkısı;
   - `hazir` ile fark;
   - üslup sızıntısı;
   - yargıç–insan uyumu;
   - varsa `genel_karisim_adaptor` ve tetikleyici sonucu (§3A).
6. **Eşik ve plan değişiklikleri:** v1'den sonraki her sürüm, tarihi ve gerekçesiyle.
7. **Sınırlamalar** (§4).
8. **Örnek cevaplar:** test cevapları yalnızca puanlar commit edildikten sonra okunur ve yalnızca açıklama amacıyla kullanılır.
9. **Kurum verisi turu için öneriler.**

## 2. Raporlama kuralları

- Her sayının yanında kaynağı yazılır: otomatik metrik, yerel yargıç ya da insan formu.
- Her farkın yanında güven aralığı veya p değeri verilir. Ham sayılar (ör. 31/50) da yazılır.
- "Katkı gösterilemedi" ile "katkı yok" ayrı ifadelerdir; ikisi karıştırılmaz.
- Önceden kayıtlı olmayan analizler "keşif" başlığı altında ve ayrı bir bölümde verilir.

## 3. Ölçülen / tahmin ayrımı

Ölçülmeyen her şey (ör. yargıç VRAM'i, beklenen gerileme) "tahmin" olarak işaretlenir. Kurum verisi turunda tekrarlanması gereken her adım, betik adıyla birlikte yazılır.

## 4. Önceden bilinen sınırlamalar

### 4.1 Tek insan değerlendirici

- **Değerlendiriciler arası uyum ölçülemez.** Tek kişi olduğu için insan puanlarının ne kadar tekrarlanabilir olduğu bilinmez. Kappa raporlanamaz.
- **Kişisel ölçek ve beklenti yanlılığı.** Değerlendirici projeyi tasarlayan kişidir. Model adları gizli ve cevap sırası karışık olsa da (körleme) şu sızıntılar mümkündür:
  - Değerlendirici eğitim verisinin üslubunu tanıdığı için adaptör cevaplarını tahmin edebilir.
  - Puanlama ölçeği kişiye özgüdür (ör. "resmî" eşiği).
- **Azaltıcı önlemler:**
  - Puan tanımları forma yazılır.
  - Üslup bölümü referanssız ve bilgi bölümünden önce doldurulur.
  - Yargıç–insan uyumu raporlanır.
  - Kurum verisi turunda en az iki değerlendirici önerilir.
- **Kapsam sınırı.** İnsan formu yalnızca birincil karşılaştırmayı ve 50 soruyu kapsar. İkincil karşılaştırmalar yalnızca yargıç ve otomatik metriklere dayanır.

### 4.2 Referansla karşılaştırma

- **Ölçülen şey "referansa uygunluk"tur, "mevzuata doğruluk" değildir.**
  - Referans cevaplar kullanıcı kararıyla doğru kabul edildi, ama bağımsız mevzuat kontrolünden geçmedi.
  - SSS'lerde soru bazında tarih yoktur; bazı rakamlar eskimiş olabilir.
- **Doğru ek bilgi ödüllendirilmez.** Form "referansla aynı süre, tutar, koşul ve istisnayı söylüyor mu?" diye sorar. Referansta olmayan doğru bilgi ne ödüllendirilir ne cezalandırılır. Referanstan daha güncel ve doğru bir cevap "Hayır" alabilir.
- **Azaltıcı önlem.** Formdaki "referans eskimiş olabilir" kutusu. İşaretlenen sorular ayrıca listelenir; bu sorular çıkarıldığında sonucun değişip değişmediği keşif analizi olarak raporlanır.
- **Yargıç da aynı sınırı taşır:** yargıcın bilgi istemi de referansa dayanır.

### 4.3 Örneklem büyüklüğü

- **Test:** 100 soruluk testte işaret testinin anlamlı olması için beraberlik hariç yaklaşık 61/39 bir ayrışma gerekir (hesaplandı). Küçük etkiler gösterilemeyebilir.
- **İnsan formu:** 50 soruluk formda güven aralıkları geniş olacaktır.
- **Tuzak ve geliştirme setleri:** tuzak (28) ve geliştirme kapsam dışı (15) setlerinde tek bir soru 3,6 ve 6,7 yüzde puan değiştirir.

### 4.4 Diğer

- **Yargıç:** tek bir model ailesidir (Gemma). Aileye özgü tercihleri tamamen dışlanamaz; kalibrasyon bunu yalnızca 20–30 çiftle sınar.
- **Üslup sızıntısı ölçütü:** önceden belirlenmiş bir işaret listesine dayanır. Listedeki ifadeleri kullanmadan gerçekleşen sızıntıyı kaçırabilir.
- **Saklanan `genel_kontrol_v2` asistan tarafından yazıldı.**
  - Sorunu: istemi ve ayarları geliştiren asistan bu setin içeriğini biliyor.
  - Önlemler:
    - v2, hiçbir model cevabı görülmeden yazılıp SHA-256 ile kilitlendi.
    - Taşındıktan sonra Read deny kapsamına alınması önerildi.
    - İstem ve ayar seçiminde kullanılmaz.
  - Kalan risk: geliştirilen istemlerin v2'deki soru türlerine bilinçsizce uyması tamamen dışlanamaz.
- **Geliştirme ve saklanan sızıntı setleri arasında yorum farkı olabilir.** v1 ve v2 farklı zamanlarda yazıldı ve v1'in içeriği v2 yazılırken görülmedi. Bu yüzden iki set arasında konu ve zorluk farkı olabilir.
  - İlk taslakta `b_kurum_gayriresmi` grubu yanlış yorumlanmıştı. Kullanıcının v1 kontrolünden sonra grup, kullanıcının verdiği tanıma göre yeniden yazıldı (karar 6c).
  - Geliştirme ile saklanan bölüm arasındaki sızıntı oranı farkı bu nedenle yalnızca dikkatle yorumlanır.
- **`b` grubunun bilgi öğeleri asistan tarafından yazıldı.** v2'deki `bilgi_ogeleri` kullanıcı onayından geçti (14 "evet", 1 "düzelt"). 15 b kaydının bilgi öğeleri, farklı bir asistan oturumunda 2026 tarihli ikincil kaynaklarla (işsizlik ödeneği, rapor parası, yıllık izin, süt izni) ve mevzuat bilgisiyle kontrol edildi; GK2-044 düzeltildi; birincil mevzuat metniyle tek tek karşılaştırma yapılmadı. 3.9'daki doğruluk ölçümü bu yüzden "onaylı öğelere uygunluk"tur, "mevzuata doğruluk" değildir. v1'de bu alan olmadığı için geliştirme bölümünde `b` doğruluğu yalnızca referanssız yargıç puanıyla raporlanır.
- **Sade anlatım kuralı, kullanıcının sade anlatım veya gündelik bir ton istediğini belirtmesiyle tetiklenir** (karar 9, `sistem_v1` kural 9). Tetikleyici kelime değil anlamdır. Bu yüzden isteğin bulunup bulunmadığını otomatik olarak değil, kullanıcı kararıyla belirliyoruz.
  - Açık istek içermeyen `b` sorularında model varsayılan resmî üsluba döner.
  - v2'deki `b` soruları bu açıdan denetlendi; v1'deki `b` sorularını yalnızca kullanıcı denetleyebilir.
  - Eğitim verisinde sade anlatım örneği yoktur. Adaptörün bu kuralı korumayı unutması mümkündür ve `b` sızıntısı bunu ölçer.
- **`b` grubunda istek türü dağılımı v1 ile v2 arasında farklı** (karar 9, ton istekleriyle genişleme).
  - v2'nin 15 `b` sorusunun hepsi sadelik isteği içerir ("sade", "basit", "adım adım", "kolay"); ton isteği içeren soru yoktur (asistanın kendi taslağı üzerindeki sınıflaması).
  - Kullanıcının gözlemine göre v1'de "samimi", "sohbet eder gibi", "mesaj atar gibi", "eğlenceli, gençlere hitap eden" gibi ton istekleri de vardır.
  - Sonuç: saklanan bölüm, ton isteğine uyumu ve ton isteği altında bilgi doğruluğunu ölçmez. Bu davranış yalnızca geliştirme bölümünde (v1) görülür; v1 istem ve ayar geliştirmede kullanıldığı için oradaki sonuç iyimser olabilir.
  - v2 bu yüzden değiştirilmedi (kullanıcı kararı): kilitli bir set sonuçlar görülmeden belirlendiği için ölçüdür; sonradan ona soru eklemek ölçüyü yeniden tasarlamak olurdu.
  - Geliştirme ile saklanan bölüm arasındaki `b` sızıntı farkı yorumlanırken istek türü dağılımı da birlikte verilir.
- **Kurum ağzı yalnızca eğitim tarafında düzeltildi** (karar 10).
  - Eğitim cevaplarındaki "Kurumumuz", "Bakanlığımız" ifadeleri 03'te kurum adıyla değiştirilir. Kilitli doğrulama ve test referanslarına ise dokunulmaz; bu ifadeler orada kalır.
  - Sistem mesajı iki modele de kurum adı kullanmasını söylediği için, bu ifadeleri içeren referanslarda chrF hem `hazir`/`hazir_istemli` hem adaptör için hafifçe düşebilir.
  - Etki iki tarafa da uygulandığı için farkı büyük ölçüde götürmesi beklenir (tahmin). Raporda bu ifadeleri içeren referans sayısı verilir. Bu sayı 02'deki toplu sayımla, içerik basılmadan ölçülür.
  - Yargıç ve insan bilgi puanı kurum adının yazılış biçiminden etkilenmez.
- **Dönemsel TL tutarları** (karar 11). Model dönemsel tutarın rakamını vermez. Referansta bu rakam varsa:
  - sayı recall'u düşer;
  - chrF hafifçe düşer;
  - bilgi puanı için §6.3'teki ek kural önerisi (senior onayı bekliyor) uygulanır.
  Tutar içeren referansların sayısı ayrıca raporlanır.
- **Kapsam:** pilot açık verilerle yapıldı. Sonuçlar kurum verisine doğrudan genellenemez; aynı akış orijinal modelden yeniden çalıştırılacak.
