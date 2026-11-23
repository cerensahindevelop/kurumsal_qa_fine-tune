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
- **Kapsam:** pilot açık verilerle yapıldı. Sonuçlar kurum verisine doğrudan genellenemez; aynı akış orijinal modelden yeniden çalıştırılacak.
