# 01: Proje iskeleti, cevap standardı ve ön kayıt

Bu aşamada model çalıştırılmadı ve eğitim yapılmadı. Amaç, daha hiçbir sonuç görülmeden "neyi, nasıl ölçeceğiz ve neye başarı diyeceğiz" sorusunu yazıya dökmek.

Yeni terimler:
- **Ön kayıt (pre-registration):** başarı ölçütlerini sonuçları görmeden yazıp kilitlemek. Neden: sonuç görüldükten sonra seçilen ölçüt, farkında olmadan "iyi görünen" ölçüte kayar.
- **Birincil uç nokta (primary endpoint):** başarının tek ana ölçüsü. Ne kadar çok ölçüt varsa, biri şans eseri iyi çıkabilir. Tek ana ölçü bunu önler.
- **İkili karşılaştırma (pairwise):** yargıç iki cevabı yan yana görür ve "hangisi daha iyi?" diye karar verir. Mutlak puan vermekten daha tutarlıdır.
- **SHA-256 özeti (hash):** bir dosyanın parmak izi. Dosyada tek bir karakter değişse bile özet tamamen değişir.

---

## 1. `src/veri/girdi_ozeti.py`

**Girdi:** bir veya daha fazla kök klasör (`--girdi`), çıktı yolu (`--cikti`), isteğe bağlı kilit manifesti yolu (`--kilit-cikti`).

**Blok 1: dosya gezme.**
- Aldığı veri: kök klasör yolu.
- Dönüşüm: `rglob("*")` ile bütün dosyalar sıralı biçimde listelenir.
- Neden: sıralama, iki çalıştırmanın aynı sırayla çıktı vermesini sağlar; böylece `diff` alınabilir.
- Sonraki bloğa verdiği: dosya yolları.

**Blok 2: parmak izi ve sayım.**
- Aldığı veri: her dosya.
- Dönüşüm: dosya 1 MB'lık parçalar hâlinde okunup SHA-256 hesaplanır, metin dosyalarında satır sayılır.
- Neden: parçalı okuma büyük PDF'lerde belleği korur. Satır sayımı içeriği göstermeden "dosya beklenen boyutta mı?" sorusunu cevaplar.
- Sonraki bloğa verdiği: her dosya için `{yol, bayt, satir, sha256}`.

**Blok 3: kilit işareti.**
- Aldığı veri: göreli yol.
- Dönüşüm: `fnmatch` ile kilitli desenlerle (test, tuzak, Türkçe değerlendirme) karşılaştırılır, `kilitli: true/false` eklenir.
- Neden: 11. aşamada test dosyası, bugünkü özetiyle aynı olmalıdır. Kilit manifesti bunu kanıtlar.
- Sonraki bloğa verdiği: iki JSON dosyası. Ekrana yalnızca toplam sayılar yazılır.

**Mini örnek (örnek, uydurma):**
```json
{"kok": "/veri", "yol": "degerlendirme/test.jsonl", "bayt": 51234, "satir": 100, "sha256": "9f2c…", "kilitli": true}
```

**Gerçek çalışma (ölçüldü):** 505 dosya tarandı, 25'i kilitli (Gruplu Veriler'de 2 + 8, ham veride 5 + 10).

**Üç cümlelik özet:** Bu betik girdi dosyalarının parmak izini çıkarır, içeriklerini açmaz. Kilitli setlerin parmak izleri ayrı bir manifeste yazılır. Böylece test setinin sonradan değişmediğini ve görülmediğini kanıtlayabiliriz.

**Kontrol sorusu:** Neden test dosyasının satır sayısını yazmak sorun değil, ama ilk satırını yazmak sorun?
*Cevap:* Satır sayısı içerik hakkında bilgi taşımaz. İlk satır ise bir test sorusudur; araç çıktısında görünürse o soru "görülmüş" sayılır ve test temizliği bozulur.

---

## 2. `istemler/sistem_v1.txt`

**Girdi:** yok (sabit metin). Eğitim, değerlendirme ve servis bu dosyayı **aynen** kullanır.

**Blok 1: rol ve alan.** Asistanın kime hizmet ettiğini (kurum çalışanı) ve alanını (ÇSGB, SGK, İŞKUR mevzuatı) tanımlar. Neden: alan tanımı olmadan "alan dışı" kavramı da olmaz.

**Blok 2: alan içi kurallar (1–8).**
- Önce hüküm, sonra koşul ve dayanak gelir. Resmî dil kullanılır.
- Rakamlar yalnızca emin olunduğunda verilir. Bilgi yoksa uydurulmaz, resmî kanal gösterilir.
- Kişisel veri istenmez. Bağlayıcı hukuki görüş verilmez.
- Neden: kurum çalışanı cevabı başkasına aktaracak; yanlış rakam, uzun bir cevaptan daha zararlıdır.

**Blok 3: alan dışı ve genel dil görevleri.**
- Başka kurumun konusu sorulursa (vergi, tapu…) model alan dışı olduğunu söyler ve yetkili kurumu gösterir.
- Genel dil görevlerinde (yazım, özet, çeviri) yardım eder ve kurum dilini dayatmaz.
- Neden: bu ayrım olmasaydı model genel Türkçe sorularını da reddederdi. Bu hem genel Türkçe ölçümlerini bozardı hem de üslup sızıntısını artırırdı.

**Mini örnek (örnek, uydurma):** "Bu paragrafı özetler misin?" → doğal bir özet. "Emlak vergisi ne kadar?" → "Bu konu Gelir İdaresi Başkanlığı ve belediyelerin görev alanındadır…"

**Üç cümlelik özet:** Sistem mesajı modelin rolünü, alanını ve bilgi yokken nasıl davranacağını tanımlar. Aynı metin eğitimde, değerlendirmede ve serviste kullanılır; böylece model eğitimde ne gördüyse kullanımda da onu görür. Alan dışı soruları genel dil görevlerinden ayırmak, genel Türkçe becerisini korumak için şarttır.

**Kontrol sorusu:** Adaptörü değerlendirirken neden üslup istemi ve few-shot örnekleri vermiyoruz?
*Cevap:* Adaptörün kazancının eğitimden mi yoksa istemden mi geldiğini ayırmak için. İstem kazancı zaten `hazir_istemli` sistemde ölçülüyor.

---

## 3. `degerlendirme/deney_plani_v1.md` ve `degerlendirme/esikler_v1.md`

**Girdi:** CLAUDE.md'deki hedefler ve sistem listesi. Model cevabı yok.

**Blok 1: sistemler ve sıra.** Beş sistem tanımlanır. Önce doğrulamada ayar seçilir, sonra testte tek bir kez ölçülür. Neden: test yalnızca bir kez kullanılırsa, üzerinde ayar yapılmamış olur.

**Blok 2: birincil ve ikincil sonuç.**
- Tek ana karşılaştırma: seçilen adaptör ile `hazir_istemli`.
- Sentetik katkısı ön kayıtlı bir ikincil iddiadır.
- Neden: çok sayıda karşılaştırma şans eseri bir "kazanç" üretebilir. Ana iddiayı tek bir karşılaştırmaya bağlamak bunu önler.

**Blok 3: puanlama.**
- Üslup, jargon ve bilgi ayrı ayrı 0–2 puanlanır. Kritik hata bilgi puanını sıfırlar.
- Her otomatik metriğin neyi ölçmediği yazılıdır.
- Neden: tek bir metrik (ör. chrF) doğruluğu ve üslubu aynı anda ölçemez.

**Blok 4: eşikler.** Her ölçüt için bir sayı, gerekçesi ve "senior onayı: bekliyor" satırı vardır. Neden: eşik sonuçtan önce sabitlenirse "başarı" tanımı sonuca göre esnetilemez.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):** yargıç 100 sorunun 50'sinde adaptörü, 30'unda istemli modeli seçiyor, 20'si beraberlik. Kazanma oranı 50/80 = %62,5 ≥ %60 ✓. İşaret testi (50'ye karşı 30) için p ≈ 0,03 < 0,05 ✓. Kritik hata farkı +1 ≤ +3 ✓. Bu durumda birincil uç nokta geçilmiş olur, ama genel Türkçe ve tuzak eşikleri de ayrıca kontrol edilir.

**Gerçek çalışma:** yok. Hiçbir model puanlanmadı.

**Üç cümlelik özet:** Deney planı neyin ölçüleceğini, eşik dosyası ise neye başarı denileceğini sonuçlar görülmeden kayda geçirir. Ana iddia tek bir karşılaştırmaya bağlıdır: fine-tune edilmiş model, istemle güçlendirilmiş hazır modeli geçmeli. Bilgi doğruluğu, genel Türkçe ve tuzak davranışı "kötüleşmeme" koşulları olarak bu iddiayı korur.

**Kontrol sorusu:** Yargıç iki sırada (A-B ve B-A) farklı karar verirse neden beraberlik sayıyoruz?
*Cevap:* Karar cevabın kendisine değil, cevabın hangi sırada gösterildiğine bağlı demektir; buna sıra yanlılığı denir. Böyle bir karar güvenilir olmadığı için iki sisteme de puan verilmez.

---

## 4. `degerlendirme/gelistirme_kapsam_disi.jsonl`

**Girdi:** yok. 15 soru tuzak setine bakılmadan sıfırdan yazıldı. Alanlar: `id, kategori, soru, beklenen_davranis, kabul_olcutu, kaynak, onay`.

**Blok 1: kategoriler.** Alan dışı, sınır vakası, kişisel veri, yetki dışı istek, güncel değer, bilgi yok, yanlış öncül, hukuki tahmin, ticari tavsiye ve manipülasyon. Neden: tuzak seti 11. aşamaya kadar kilitli; geliştirme sırasında "bilmiyorum deme" davranışını ölçebilmek için ayrı bir set gerekiyor.

**Blok 2: onay ve çakışma.** Taslakta her kayıtta `onay: bekliyor` yazıyordu. Kullanıcı seti onayladı; artık her kayıtta `onay: onaylandı (kullanıcı)` yazıyor. İki düzeltme yapıldı. GKD-012'nin kabul ölçütü, doğru bir "bir yılı doldurunca kullanabilirsiniz" cevabını haksız yere başarısız saymasın diye daraltıldı. GKD-008'in beklenen davranışına Asgari Ücret Tespit Komisyonu'nu anma izni eklendi. Ders: kabul ölçütü yanlış cevabı yakalarken doğru cevabı cezalandırmamalı; bir kelimeyi yasaklamak ("kullanabilirsiniz") çoğu zaman fazla geniş kalır. Set 02'de tuzak ve test setiyle yakın eşleşme denetiminden geçer. Eşleşme çıkarsa kararı kullanıcı verir.

**Mini örnek (gerçek kayıt, bu set test değildir):** `GKD-011` "İstifa ettim; işsizlik ödeneğim ne zaman hesabıma yatar?" → beklenen: öncülü düzeltmek (kendi isteğiyle ayrılmada kural olarak hak yok) ve İŞKUR'a yönlendirmek.

**Üç cümlelik özet:** Bu küçük set, modelin bilmediği ya da alanı dışında kalan sorularda uydurmadığını geliştirme sırasında kontrol eder. Gerçek tuzak setinin yerini tutmaz; yalnızca erken uyarı verir. Tuzak setinden bağımsız yazıldığı için onu kullanmak test kilidini bozmaz.

**Kontrol sorusu:** Bu sette 15/15 başarı alan bir model tuzak setinde de başarılı sayılır mı?
*Cevap:* Hayır. Bu set küçüktür ve aynı kişi tarafından yazılmıştır; tuzak setindeki farklı tuzak türlerini kapsamayabilir. Final iddiası yalnızca 11. aşamadaki tuzak sonucuyla yapılır.

---

## 5. Gösterim: mini puanlama

Uydurma soru ve iki cevapla yapılan gösterim `degerlendirme/deney_plani_v1.md` §9'dadır. Oradan çıkan ders: chrF iki cevabı birbirinden ayırıyor (62,1'e karşı 27,4, ölçüldü), ama Cevap 2'deki "%25" ve "300 saat" kritik hatalarını tek başına göstermiyor. Bu hataları sayı karşılaştırması yakalıyor (recall 5/5'e karşı 1/5, ölçüldü).

---

## 6. Açık kararların işlenmesi (01 güncellemesi)

**Tetikleyici kural (`esikler_v1.md` §3A):** "Gerekirse yap" türü bir karar ancak "ne zaman gerekir?" sorusu sonuç görülmeden sayıyla yazılırsa güvenilirdir. Burada tetikleyici, seçilen adaptörün Türkçe değerlendirmenin geliştirme bölümünde hazır modele göre ne kadar gerileyebileceğini görev görev söyler. Sınırlardan biri aşılırsa genel Türkçe karışımlı adaptör eğitilir.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):**
- TurkishMMLU geliştirme bölümünde hazır model %61,0, adaptör %58,5 → fark −2,5 pp. T.1 sınırı −2,0 pp, yani tetikleyici **çalışır**.
- Aynı koşuda sızıntı oranları %8'e karşı %14 → fark +6 pp ≤ +10 pp, T.7 aşılmaz.

Tek bir satırın aşılması yeterlidir; karışım koşusu yapılır.

**İnsan formunun iki bölümü:** üslup bölümünde referans gösterilmez. Neden: referansı gören değerlendirici farkında olmadan "referansa benzeyen" cevaba yüksek üslup puanı verebilir. Bilgi bölümünde ise referans gösterilir, çünkü bilgi ancak bir ölçüye göre kontrol edilebilir.

**Üç cümlelik özet:** Genel Türkçe verisi artık yalnızca sayısal bir tetikleyici aşılırsa eğitime giriyor. Tetikleyici, final eşikleriyle aynı sayıları geliştirme bölümünde kullanıyor; böylece gerileme testten önce yakalanıyor. İnsan değerlendirmesi 50 soruda, tek kişi tarafından, üslup ve bilgi ayrı bölümlerde ve kör olarak yapılacak.

**Kontrol sorusu:** Tetikleyiciyi geçemeyen bir adaptörün öğrenme oranını değiştirip tekrar ölçmek neden yasak?
*Cevap:* Çünkü o zaman geliştirme bölümü bir ayar hedefine dönüşür. Aynı bölüm üzerinde defalarca deneme yapıp eşiği "geçen" ayarı seçmek, gerilemeyi gizleyen şanslı bir sonuç üretebilir. Tetikleyici bu yüzden bir kez ölçülür.

## 7. Karar 6c: `b` grubunun yeniden yazılması ve gruba göre sızıntı ölçütü

**Dosyalar ve girdileri:**
- `inceleme/genel_kontrol_v2_taslak.jsonl`: GK2-036..050 yeniden yazıldı.
- `src/veri/onay_csv.py`: girdi taslak JSONL, çıktı onay CSV'si.
- `degerlendirme/deney_plani_v1.md` §6.6 ve `esikler_v1.md` 3.7, 3.9 ve T.7.

**Blok 1, neden ölçüt değişti.** Sızıntı ölçütünün amacı, "soru bunu gerektirmediği hâlde kurum diline kaymak" durumunu yakalamaktır. `b` soruları ise kurum işlemini sorar: "e-Devlet'ten nasıl bakarım?" sorusunun doğru cevabı "e-Devlet" kelimesini içermek zorundadır. Eski liste bu cevabı sızıntılı sayardı; buna yanlış alarm (false positive) denir. Yeni kuralda kurum adları serbest, yasak olan yalnızca bürokratik kalıptır ("Sayın", "gerekmektedir", "ilgili mevzuat çerçevesinde").

**Blok 2, kayıt (register) ve doğruluk ayrı ölçülür.** Kayıt, aynı bilginin hangi resmiyet düzeyinde söylendiğidir. Bir cevap çok sade olup yanlış da olabilir. Bu yüzden `b` kayıtlarına `bilgi_ogeleri` eklendi: doğru bir cevapta bulunması gereken 3–4 temel bilgi. Yargıç cevabı bu öğelere göre 0–2 puanlar (3.9). Öğeleri asistan yazdığı için önce kullanıcı onayından geçerler.

**Blok 3, ölçüm dosyadaki listeye değil, gruba bağlı.** v1 salt okunur bir girdidir; içindeki `yasak_kalip` değiştirilemez. Bu yüzden puanlama betiği listeyi kaydın `grup` alanına göre plandan seçer. Böylece v1 (geliştirme) ve v2 (saklanan) aynı kuralla ölçülür.

**Blok 4, onay CSV'si betikle üretilir.** `onay_csv.py` taslağı CSV'ye döker ve `b` satırlarına ikinci bir onay sütunu ("bilgi öğeleri doğru mu?") açar. Zaten doldurulmuş hücreler kimliğe göre korunur. Bu sayede taslak değişince CSV yeniden üretilse de onaylarınız kaybolmaz.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):** soru: "İşten çıkarıldım, işsizlik maaşına nasıl başvururum, sade anlatır mısın?"
- Cevap X: "İŞKUR'a 30 gün içinde başvurman gerekiyor. 1) e-Devlet'e gir…" Kurum adı var ama bürokratik kalıp yok, bu yüzden sızıntılı değil. Bilgi öğeleri tam, puan 2.
- Cevap Y: "Sayın vatandaşımız, başvurunun ilgili mevzuat çerçevesinde İŞKUR'a yapılması gerekmektedir." 3 farklı işaret var, bu yüzden sızıntılı.
- Cevap Z: "SGK'ya git, 60 gün süren var." Sızıntılı değil, ama iki kritik hata var: kurum ve süre. Puan 0. Sızıntı ölçütünü geçmek doğru olmak demek değildir.

**Üç cümlelik özet:** `b` grubu artık kurum işlemini gündelik dille soran ve sade anlatım bekleyen sorulardan oluşuyor. Bu grupta kurum adları serbest, yasak olan bürokratik kalıplar. Sadeleşmenin bilgi kaybına yol açmadığını görmek için doğruluk, kullanıcının onayladığı bilgi öğelerine göre ayrıca puanlanıyor.

**Kontrol sorusu:** Neden `b` grubunda mevzuat atfı ("4447 sayılı Kanun") sızıntı sayılmadı, ama ayrıca sayılıyor?
*Cevap:* Çünkü `sistem_v1` kural 1 alan içi sorularda dayanak belirtmeyi istiyor. Bu atıf sızıntı sayılsaydı, sistem mesajına uyan model cezalandırılırdı. Atıf yine de sade anlatımı ağırlaştırabilir. Bu gerilim karar 9 ile çözüldü: sistem mesajı kural 9, sade anlatım istendiğinde atıf gerektirmiyor.

## 8. Sistem mesajı kararları 9–11 (`istemler/sistem_v1.txt`, `istemler/cevap_standardi_v1.md`)

**Girdi:** kullanıcının kararları. **Çıktı:** sistem mesajındaki üç değişiklik.
- **Kural 2'ye ek, kurum ağzı yok.** Model üç kurumun konularını cevapladığı için "Kurumumuz" belirsizdir. Kurumlar adıyla anılır. Eğitim verisi 03'te buna uydurulur; kilitli referanslar değişmez.
- **Kural 4, tutar ile süre/oran ayrımı.** Kanundaki süreler ve oranlar sabittir, verilir. TL tutarları dönemseldir ve eğitim verisinde eskimiş olabilir. Bu yüzden rakam yerine hesaplama yolu verilir.
- **Kural 9, sade anlatım.** Varsayılan resmî üsluptur. Kullanıcı sade anlatım istediğini belirtirse aynı bilgi gündelik dille verilir. Tetikleyici kelime değil anlamdır: "kolayca anlatır mısın" sayılır, tek başına "kısaca" sayılmaz, çünkü o yalnızca kısalık ister.
  - Sonradan genişletildi: kullanıcı samimi, gündelik veya eğlenceli bir ton istediğini belirtirse de ("sohbet eder gibi anlat", "esprili bir dille yaz") aynı kural çalışır. Bilgi yine eksiksiz kalır; değişen yalnızca dildir.
  - Kuraldaki örnekler bilerek değerlendirme sorularından farklı seçilir. Sistem mesajı her soruda modele verildiği için, değerlendirme sorusuna benzeyen bir örnek o soruyu kısmen önceden cevaplamış olur. Bu yüzden "kolayca anlatır mısın" (v2'de geçiyordu) "anlaşılır bir dille anlatır mısın" ile değiştirildi (karar 13).
  - Emoji her durumda yasak; ünlem yalnızca ton isteklerinde ölçülü olarak serbest (karar 12). Cümle, "Bu durumda" göndermesi yanlış duruma bağlanmasın diye kuralın sonundan izin cümlesinin yanına taşındı ve "Ton isteği varsa…" diye açık yazıldı (karar 14). Ders: sistem mesajında zamir ve gönderme ("bu durumda") en yakın cümleye bağlanarak okunur; koşulu her cümlede açıkça yazmak daha güvenlidir. Emojiye izin vermemenin nedeni sızıntı riski: model emojiyi bir kez öğrenirse resmî cevaplara da taşıyabilir.
  - **`src/veri/ifade_say.py` (girdi: JSONL dosyaları ve ifadeler).** Blok 1: her kaydın bütün metin alanlarını toplar. Blok 2: Türkçeye uygun küçük harfe çevirir ("İ"→"i", "I"→"ı"); Python'un `lower()` işlevi "I"yı "i" yaptığı için bu adım ayrıca yazıldı. Blok 3: yalnızca dosya adı, kayıt sayısı ve eşleşme sayısını basar. Böylece kilitli bir sette bir ifadenin geçip geçmediği, içerik görülmeden öğrenilir. *Gerçek çalışma:* "anlaşılır bir dille anlatır mısın" v1'de 0/60, v2'de 0/60. Doğruluk sınaması: "KOLAYCA ANLATIR MISIN" v2'de 1 (büyük harf ve I/ı dönüşümü çalışıyor).
  - *Kontrol sorusu:* Sayım betiğini neden önce bilinen bir eşleşmeyle sınadık? *Cevap:* 0 sonucu iki şey demek olabilir: ifade gerçekten yok ya da betik hiçbir şey bulamıyor. Bilinen bir eşleşmenin 1 çıkması, sıfırın gerçek bir sıfır olduğunu gösterir.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):** "İşsizlik maaşı ne kadar?"
- Kural 4'e uygun: "Günlük ödenek, son dört aylık prime esas kazançların günlük ortalamasının %40'ıdır; aylık tutar asgari ücretin brüt tutarının %80'ini geçemez. Güncel tutarı İŞKUR'dan kontrol etmeniz önerilir."
- Uygun değil: "Aylık 12.345 TL." Bu rakam uydurma; doğru olsa bile kısa sürede eskir.

**Üç cümlelik özet:** Sistem mesajı artık kurumları adıyla anıyor ve "Kurumumuz" demiyor. Kanundaki süre ve oranları veriyor, dönemsel TL tutarları yerine hesaplama yolunu söylüyor. Kullanıcı sade anlatım istediğini belirtirse aynı bilgiyi bürokratik kalıp ve atıf olmadan veriyor.

**Kontrol sorusu:** Eğitim cevaplarındaki "Kurumumuz" ifadesini değiştirip test referanslarındakini neden değiştirmiyoruz?
*Cevap:* Test referansları kilitlidir ve sonuçlar görülmeden belirlenmiş ölçüdür. Onları değiştirmek, ölçüyü sonuca göre ayarlamak olurdu. Bunun bedeli, iki modelde de chrF'in hafifçe düşmesidir; bu bedel rapora sınırlama olarak yazıldı.

## 9. `genel_kontrol_v2` onayının işlenmesi (`src/veri/onay_csv.py`)

**Girdi:** kullanıcının doldurduğu `inceleme/genel_kontrol_v2_onay.csv` ve taslak `inceleme/genel_kontrol_v2_taslak.jsonl`. **Çıktı:** onaylı taslak, onay dağılımı ve yeni kilit manifesti (`kilit_manifesti_v5.json`).

- **Blok 1, farkı bulmak.** CSV ile JSONL alan alan karşılaştırıldı. Tek içerik farkı GK2-044'ün 4. bilgi öğesiydi. Düzeltme JSONL'de yalnızca o dizge değiştirilerek işlendi, böylece başka satır değişmedi.
- **Blok 2, yazım normalleştirmesi (normalization).** İnsanlar aynı değeri farklı yazabilir: "düzelt", "Düzelt", "duzelt". `normal_onay` Türkçe harfleri ASCII karşılığına çevirir ve küçük harfe indirir. Bu yalnızca sayımda kullanılır; hücredeki yazım korunur. evet/hayir/duzelt dışında kalan bir değer çıkarsa betik o kaydın kimliğini listeler. Böylece yanlış yazım sessizce kaybolmaz.
- **Blok 3, gidiş-dönüş kontrolü (round-trip).** Düzeltilmiş JSONL'den CSV yeniden üretildi. Sonuç kullanıcının dosyasıyla bayt bayt aynı çıktı. Bu, iki dosyanın birbirine tam uyduğunu ve hiçbir onay hücresinin kaybolmadığını gösterir.
- **Blok 4, kilit.** Onaylı taslağın özeti yeni manifest sürümüne yazıldı. Eski manifestlerin üzerine yazılmaz; her sürüm o anki hâlin kanıtıdır.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):**
- Hücreler: `düzelt`, `Duzelt `, `evet`, `tamam`.
- Sayım: `duzelt` 2, `evet` 1, tanımsız `tamam` 1. "tamam" yazan kaydın kimliği ekrana basılır.

**Gerçek çalışma:** `onay` sütununda 60 "evet"; bilgi öğesi sütununda 14 "evet" ve 1 "duzelt" (ölçüldü).

**Üç cümlelik özet:** Kullanıcının onay tablosundaki tek düzeltme taslağa aynen işlendi ve başka hiçbir satır değişmedi. Betik artık "düzelt" ile "duzelt"i aynı sayıyor ve tanımadığı değerleri kimlikleriyle gösteriyor. Onaylı taslak yeni bir manifest sürümüyle kilitlendi; saklanan klasörüne taşıma 02'deki çakışma denetiminden sonra yapılacak.

**Kontrol sorusu:** Normalleştirmeyi neden yalnızca sayımda yapıp hücredeki "düzelt" yazımını değiştirmiyoruz?
*Cevap:* CSV insanın kaydıdır. Betik onu kendi biçimine çevirseydi kullanıcının yazdığı değişmiş olurdu ve gidiş-dönüş kontrolü (dosyanın bayt bayt aynı kalması) anlamını yitirirdi. Karşılaştırma için sadeleştirmek yeterli.
