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

**Blok 2: onay ve çakışma.** Her kayıtta `onay: bekliyor` yazar. Set 02'de tuzak ve test setiyle yakın eşleşme denetiminden geçer. Eşleşme çıkarsa kararı kullanıcı verir.

**Mini örnek (gerçek kayıt, bu set test değildir):** `GKD-011` "İstifa ettim; işsizlik ödeneğim ne zaman hesabıma yatar?" → beklenen: öncülü düzeltmek (kendi isteğiyle ayrılmada kural olarak hak yok) ve İŞKUR'a yönlendirmek.

**Üç cümlelik özet:** Bu küçük set, modelin bilmediği ya da alanı dışında kalan sorularda uydurmadığını geliştirme sırasında kontrol eder. Gerçek tuzak setinin yerini tutmaz; yalnızca erken uyarı verir. Tuzak setinden bağımsız yazıldığı için onu kullanmak test kilidini bozmaz.

**Kontrol sorusu:** Bu sette 15/15 başarı alan bir model tuzak setinde de başarılı sayılır mı?
*Cevap:* Hayır. Bu set küçüktür ve aynı kişi tarafından yazılmıştır; tuzak setindeki farklı tuzak türlerini kapsamayabilir. Final iddiası yalnızca 11. aşamadaki tuzak sonucuyla yapılır.

---

## 5. Gösterim: mini puanlama

Uydurma soru ve iki cevapla yapılan gösterim `degerlendirme/deney_plani_v1.md` §9'dadır. Oradan çıkan ders: chrF iki cevabı birbirinden ayırıyor (62,1'e karşı 27,4, ölçüldü), ama Cevap 2'deki "%25" ve "300 saat" kritik hatalarını tek başına göstermiyor. Bu hataları sayı karşılaştırması yakalıyor (recall 5/5'e karşı 1/5, ölçüldü).
