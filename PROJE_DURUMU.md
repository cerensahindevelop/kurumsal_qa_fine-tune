# PROJE_DURUMU

Son güncelleme: 2026-11-24 (01: eşiklerin açıklamalı belgesi eklendi) · Son tamamlanan aşama: **01**

---

## 01: Proje iskeleti, cevap standardı, deney planı, eşik taslağı (2026-11-23)

### Tamamlanan iş
- Proje kökü belirlendi: `/home/aipc/Desktop/Projeler/kurum-qa-finetune`. Git deposu başlatıldı (`main`).
- CLAUDE.md'deki klasör yapısı kuruldu. `src/` alt paketlerine `__init__.py` eklendi.
- Cevap standardı ve tek sistem mesajı (`sistem_v1.txt`) yazıldı.
- Deney planı (ön kayıt taslağı) hazırlandı: sistemler, doğrulama ve test sırası, birincil/ikincil sonuç ayrımı, sentetik katkısının test karşılaştırması, few-shot önerisi, puanlama tanımları, metrik sınırları, yargıç adayları ve kalibrasyon kuralı, beş açık karar ve mini puanlama gösterimi.
- Eşik taslağı (`esikler_v1.md`) yazıldı. Bütün satırlarda "senior onayı: bekliyor" yazıyor.
- Geliştirme kapsam dışı seti için 15 soruluk taslak yazıldı (tuzak setine bakılmadan).
- Girdi SHA-256 özeti ve kilit manifesti üretildi. Paket ve donanım kaydı alındı.
- Eğitim başlatılmadı. Hiçbir model çalıştırılmadı.

### Üretilen dosyalar
| Dosya | Amaç |
|---|---|
| `README.md`, `.gitignore`, `experiments.csv` (yalnızca başlık satırı) | İskelet |
| `istemler/sistem_v1.txt` | Tek sistem mesajı (eğitim, değerlendirme, servis) |
| `istemler/cevap_standardi_v1.md` | Üslup, jargon, bilgi yokken ve alan dışında davranış |
| `degerlendirme/deney_plani_v1.md` | Ön kayıt taslağı |
| `degerlendirme/esikler_v1.md` | Eşik taslağı (onay bekliyor) |
| `degerlendirme/gelistirme_kapsam_disi.jsonl` | 15 soru, `onay: onaylandı (kullanıcı)`; GKD-008 ve GKD-012 düzeltildi; 02'deki çakışma denetimi bekliyor |
| `degerlendirme/kilit_manifesti_v1.json` | 25 kilitli dosyanın SHA-256 özeti |
| `src/veri/girdi_ozeti.py` | Girdi özeti ve kilit manifesti betiği (içerik basmaz) |
| `env/2026-11-23_girdi_sha256.json` | 505 girdi dosyasının özeti |
| `env/2026-11-23_paketler.txt`, `env/2026-11-23_donanim.txt` | Ortam kaydı |
| `docs/ogrenme/01_iskelet_ve_plan.md` | Öğrenme açıklaması |
| `rapor/rapor_plani_v1.md` | Rapor iskeleti ve önceden bilinen sınırlamalar (açık kararlar güncellemesinde eklendi) |
| `inceleme/genel_kontrol_v2_taslak.jsonl`, `inceleme/genel_kontrol_v2_onay.csv` | Saklanan üslup sızıntısı seti taslağı (60) ve onay kuyruğu (karar 6a) |
| `degerlendirme/kilit_manifesti_v2.json`, `env/2026-11-23_girdi_sha256_v2.json` | 27 kilitli dosya: v1'deki 25 + ham `01_sss` + v2 taslağı (ilk `b` yorumu) |
| `degerlendirme/kilit_manifesti_v3.json`, `env/2026-11-23_girdi_sha256_v3.json` | 27 kilitli dosya; v2'den farkı yalnızca yeniden yazılmış `b` grubuyla taslağın özeti (karar 6c) |
| `degerlendirme/kilit_manifesti_v4.json`, `env/2026-11-23_girdi_sha256_v4.json` | 27 kilitli dosya; v3'ten farkı yalnızca GK2-050 düzeltmesiyle taslağın özeti |
| `degerlendirme/kilit_manifesti_v5.json`, `env/2026-11-23_girdi_sha256_v5.json` | **Geçerli manifest.** 27 kilitli dosya; v4'ten farkı yalnızca kullanıcı onaylı, GK2-044 düzeltilmiş taslağın özeti |
| `src/veri/onay_csv.py` | JSONL taslağından onay CSV'si üretir; dolu hücreleri kimliğe göre korur (karar 6c) |
| `degerlendirme/esikler_v1_aciklama.md` | Eşiklerin sade açıklaması (bağlayıcı değil): her eşik için arka plan, ne, neden, olmasaydı, katkı, uydurma örnek; düşünme modu ek bölümü; terim sözlüğü; "Açıklarken fark ettiklerim" (22 madde). `esikler_v1.md`'ye yalnızca en üste atıf satırı eklendi (2026-11-24) |

`.claude/settings.json` ve `kanarya.txt` kullanıcı isteğiyle git'e eklendi. `kanarya.txt` deny kuralı gereği okunmadı.

### Doğrulama sonuçları
**Ölçüldü:**
- Satır sayıları (`wc -l`) beyanla uyumlu: `egitim_adayi` 904, `kaynak_adayi` 82, `egitim_sorulari` 18.187, `dogrulama` 100, `test` 100, `tuzak_sorular` 28. Türkçe Değerlendirme'de 8 dosya, toplam 3.255 satır (aya 250, gecturk 500, genel_kontrol 60, mmlu_dev 45, mmlu_test 900, vikipedi 500, wmt16 500, xlsum 500).
- Alan adları:
  - SSS ve doğrulama: `id, kaynak, soru, cevap_metin`.
  - Öğretmen: `belge_konumu, kaynak, baslik, tarih_bilgisi, metin`.
  - Genel Türkçe: `id, soru`.
- Eğitim SSS kaynak dağılımı: SGK 428, ÇSGB 336, İŞKUR 140. Cevap uzunluğu medyanı 40 kelime (10. yüzdelik 19, 90. yüzdelik 89).
- GPU'lar: nvidia-smi 0 = RTX A5000 (2D:00.0, 884 MiB dolu); nvidia-smi 1 = RTX 4500 Ada (99:00.0, 15 MiB dolu). Sürücü 615.71.09.
- Ollama 0.35.1 kurulu (≥ 0.32.12 gerekli). Kurulu modeller: `qwen3.6:35b`, `qwen2.5:*`, `nomic-embed-text`. `qwen3.8` ve `gemma4` henüz indirilmedi.
- Gösterim metrikleri (geçici el yazımı chrF): Cevap 1 chrF 62,1 ve sayı recall 5/5; Cevap 2 chrF 27,4 ve sayı recall 1/5.
- İşaret testi kontrolü: 100 soruda anlamlılık için ≥ 61/39 gerekiyor.
- Eşik açıklaması (2026-11-24):
  - `esikler_v1.md` farkı yalnızca en üstteki atıf satırı (+2 satır, git diff).
  - Kilitli 27 dosyanın 27'si `kilit_manifesti_v5.json` ile aynı SHA-256 (yalnızca sayı basan kontrol). Girdi değişmedi; yeni manifest üretilmedi.
  - Açıklamadaki p değerleri, kappa ve standart hatalar uydurma sayılar üzerinde formülle hesaplandı; veri kullanılmadı.
  - Paket kaydı: `env/2026-11-24_paketler.txt` (temel miniconda ortamı).

**Tahmin / bekleyen iş:**
- Kayıt düzeyinde JSON doğrulaması, kimlik benzersizliği ve çakışma denetimi (02).
- Yargıç VRAM değerleri ve bazı yayın tarihleri (`mistral-small3.2`, `gpt-oss`, `phi4`) bilgime dayanıyor; yargıç kurulumunda doğrulanacak.
- TurkishMMLU seçenek sayısı (02'de dosyadan).
- `sacrebleu` kurulu değil; resmî chrF metrik betiğinden önce sabit sürümle kurulacak.

### Kararlar (kullanıcı, 2026-11-23) — "01: açık kararlar kaydedildi" commit'iyle işlendi
1. **Genel Türkçe verisi** yalnızca gerileme görülürse eğitime girer.
   - Sayısal tetikleyici `esikler_v1.md` §3A'da: T.1–T.8 (görev başına izin verilen en fazla düşüş ve sızıntı sınırı) ve K.1–K.3 (tetiklenince yapılacaklar). Senior onayı bekliyor.
   - Eski "her durumda %10–20" kararından neden değişildiği `deney_plani_v1.md` §8, karar 1'de.
2. **Türkçe değerlendirme ayrımı:** her dosyada %30 geliştirme / %70 saklanan, seed 42; her görevde geliştirme bölümü en az 50 kayıt. Bölme 02'de yapılacak.
3. **Kör insan değerlendirmesi:**
   - 11. aşamada, yalnızca birincil çift için, testten 50 soru, tek değerlendirici (proje sahibi).
   - Form iki bölüm: üslup ve jargon referanssız; bilgi bölümünde referans gösterilir.
   - Model adları gizli, sıra karışık, anahtar ayrı dosyada.
   - Ayrıntı `deney_plani_v1.md` §6.9'da, eşikler 1.2 ve 2.1b'de, sınırlamalar `rapor/rapor_plani_v1.md` §4'te.
4. **Deny kuralları:** kapandı. Commit `f6ad4d0`; ham `05_tuzak_sorular`, `01_sss`, `06_genel_turkce/degerlendirme` ve `kanarya_klasor` için Read deny var (settings.json okunarak doğrulandı; kanarya ölçümünü kullanıcı yaptı).
5. **Ham tuzak araçları:** şimdi kullanılmayacak, karar 11'e kaldı. Birincil tuzak puanı önceden kayıtlı ölçütlerden ve projenin kendi yargıç akışından gelir; hazır betik 11'de en fazla ek kontrol olabilir.

6. **Bölme kuralına uymayan iki dosya** (kullanıcı kararı, 2026-11-23; `deney_plani_v1.md` §8, karar 6):
   - **6a:** `genel_kontrol_v1`'in tamamı (60) geliştirme bölümü olur. Saklanan karşılığı yeni `genel_kontrol_v2`: 60 kayıt, aynı dağılım. Taslak `inceleme/` altında yazıldı ve `kilit_manifesti_v2.json`'a eklendi.
   - **6b:** `turkishmmlu_dev` bölünmez; iki bölümde de aynı 5-shot örnekleri kullanılır.
   - **6c** (kullanıcı v1'i kontrol ettikten sonra): v2'nin `b` grubu yanlış yorumlanmıştı.
     - GK2-036..050 sıfırdan yeniden yazıldı. Yeni tanım: "kurum işlemi veya bilgisi isteyen, gündelik dille sorulmuş, sade ve adım adım anlatım bekleyen sorular". Kategori `kurum_islemi_sade_anlatim`, yeni alan `bilgi_ogeleri`.
     - `b` için sızıntı ölçütü yeniden tanımlandı (`deney_plani_v1.md` §6.6): kurum ve sistem adları serbest, bürokratik kalıplar yasak. Mevzuat atfı ayrıca sayılır, sızıntı sayılmaz.
     - `b` doğruluğu için `esikler_v1.md` 3.9 eklendi. 3.7 ve T.7 gruba göre ölçüte bağlandı; gerekçe `esikler_v1.md` §3 sonunda ve plan karar 6c'de.

### Sistem mesajı kararları (kullanıcı, 2026-11-23) — "01: sistem mesajı kararları" commit'iyle işlendi
`sistem_v1.txt` yerinde düzeltildi, yeni sürüm açılmadı. Dosya henüz hiçbir eğitim veya değerlendirmede kullanılmamıştı; eski hâl git geçmişinde (`b4ebb4e`). Ayrıntılar `deney_plani_v1.md` §8'de.
- **Karar 9, sade anlatım:** yeni kural 9 eklendi. Kullanıcı sade, basit, kolay anlaşılır veya adım adım anlatım istediğini belirtirse model doğru ve eksiksiz bilgiyi gündelik dille, bürokratik kalıpsız ve atıfsız verir. Varsayılan üslup resmî kalır. `cevap_standardi_v1.md` §2a. Açık karar 9 kapandı.
  - Kullanıcı incelemesinden sonra ("01: kural 9 tetikleyicisi ve GK2-050"): tetikleyici kelime eşleşmesi değil anlamdır. Kuralın başı şu oldu: "Kullanıcı sade, basit, kolay anlaşılır veya adım adım bir anlatım istediğini belirtirse (ör. "kolayca anlatır mısın", "teknolojiden anlamayan birine anlatacağım")…". Tek başına "kısaca" sade anlatım isteği sayılmaz.
  - **Ton istekleriyle genişleme** ("01: kural 9 ton istekleriyle genişletildi"): kullanıcı v1 `b` sorularında ton istekleri de gördü ("samimi", "sohbet eder gibi", "mesaj atar gibi", "eğlenceli"). Kural 9 artık "samimi, gündelik veya eğlenceli bir tonda" anlatım isteğini de kapsıyor. Örnekler "sohbet eder gibi anlat" ve "esprili bir dille yaz" eklendi. "Kısaca" istisnası kuralın metnine yazıldı. `sistem_v1.txt` yerinde düzeltildi; `cevap_standardi_v1.md` §2a (ton isteği örneği dahil) ve plan karar 9 güncellendi.
  - Ölçüldü: v2'nin 15 `b` sorusunun 15'i sadelik isteği içeriyor, ton isteği içeren yok (kendi taslağım üzerinde sınıflama). v2 değiştirilmedi; dağılım farkı rapor planı §4.4'te sınırlama.
- **Karar 10, kurum ağzı:** kural 2'ye eklendi. Model kurumları adıyla anar, "Kurumumuz" / "Bakanlığımız" demez. `cevap_standardi_v1.md` §2. 03 notu aşağıda. Kurum verisi turunda bu kural tek kurum için yeniden değerlendirilecek.
- **Karar 11, tutar ile süre/oran ayrımı:** kural 4 değiştirildi. Kanunda belirlenmiş süre, gün sayısı ve oranlar verilir. Dönemsel TL tutarlarının rakamı verilmez; hesaplama yolu söylenir ve resmî kaynaktan kontrol önerilir. `cevap_standardi_v1.md` §4 uyduruldu.
  - 03'teki eskimiş tutar nötrleştirme kuralı plan karar 11'de önceden kayda alındı ve **kullanıcı tarafından onaylandı**.
  - §6.3'teki puanlama kuralı **kullanıcı tarafından kabul edildi**: kural 4'e uygun biçimde verilmeyen dönemsel TL tutarı eksik sayılmaz. Kesin onayı eşiklerle birlikte senior verecek.

### Açık kararlar (kullanıcı)
7. **`genel_kontrol_v2`:** onay kapandı ("01: genel_kontrol_v2 onaylandı"); taşıma ve deny kuralı açık.
   - Ölçüldü: 60/60 kayıt "evet". `b` bilgi öğeleri: 14 "evet", GK2-044 "düzelt". CSV'deki tek içerik farkı GK2-044'ün 4. öğesiydi.
   - GK2-044'ün 4. öğesi kullanıcının metniyle aynen taslağa işlendi. Gerekçe: 1475 md. 14'e göre kıdem tazminatını yalnızca 4857 md. 25/II kaldırır; işçinin haklı nedenle feshi (md. 24) de tazminat doğurur.
   - Bilgi öğesi kontrolünün kapsamı (ikincil kaynaklar, birincil metinle tek tek karşılaştırma yok) rapor planı §4.4'e sınırlama olarak yazıldı.
   - Taslak yeniden üretilen CSV ile bayt bayt aynı (ölçüldü). Onaylı taslak `kilit_manifesti_v5.json` ile kilitlendi.
   - **Açık:** taşıma 02'deki çakışma denetiminden sonra yapılacak (kullanıcı kararı). Taşımadan sonra önerilen Read deny kuralı eklenmeli: `degerlendirme/saklanan/**`, `inceleme/genel_kontrol_v2_*`.
- ~~9. `b` grubu ile `sistem_v1` gerilimi~~: karar 9 ile kapandı (aşağıda).
- ~~`genel_kontrol_v2` sade anlatım isteği denetimi~~ kapandı.
  - GK2-036 kullanıcı kararıyla değişmedi; "kolayca anlatır mısın, bilgisayardan pek anlamaz" açık bir istektir.
  - GK2-050 "Kısaca ve sade bir dille anlatır mısın?" olarak düzeltildi.
  - 15 `b` sorusunun hepsi istek içeriyor. CSV ve `kilit_manifesti_v4.json` yeniden üretildi.
  - v1 `b` sorularında aynı denetimi yalnızca kullanıcı yapabilir.
- ~~12. Ton isteklerinde ünlem/emoji~~ kapandı ("01: karar 12-13 kapatıldı"): emoji her durumda yasak; ünlem yalnızca kural 9'daki isteklerde ölçülü olarak serbest. Kural 9'un sonuna "Bu durumda ünlem ölçülü kullanılabilir; emoji hiçbir durumda kullanılmaz." eklendi. Kural 2'deki yasak resmî üslup için geçerli (`cevap_standardi_v1.md` §2a). Cümlenin yeri ve kapsamı karar 14 ile düzeltildi.
- ~~13. "kolayca anlatır mısın" örneği~~ kapandı: örnek "anlaşılır bir dille anlatır mısın" ile değiştirildi. Ölçüldü: yeni ifade ve çekirdeği "anlaşılır bir dille" v1'de 0/60, v2'de 0/60. v1 yalnızca sayı basan `src/veri/ifade_say.py` ile denetlendi. Betiğin doğruluğu v2'de bilinen iki eşleşmeyle sınandı (1/1).
- ~~14. Kural 9'daki "Bu durumda" göndermesi~~ kapandı ("01: karar 14 kapatıldı"): kullanıcı iki seçeneği birlikte seçti. Ünlem/emoji cümlesi kuralın sonundan kaldırıldı. Yerine "kanun ve madde atfı gerekmez." ifadesinin hemen ardına "Ton isteği varsa ünlem ölçülü kullanılabilir; emoji hiçbir durumda kullanılmaz." eklendi. Kural 9 "Böyle bir istek yoksa yukarıdaki resmî üslubu koru." cümlesiyle bitiyor. Sonuç: ünlem yalnızca ton isteğinde serbest; sadelik isteğinde ve resmî üslupta yok. Standart §2a, plan karar 9/12/14 ve öğrenme dosyası güncellendi.
- ~~Geliştirme kapsam dışı seti kullanıcı onayı~~ kapandı ("01: geliştirme kapsam dışı seti onaylandı").
  - GKD-012'nin kabul ölçütü "Bir yıl şartı belirtilmiş; iznin ilk ay içinde kullanılabileceği söylenmemiş." oldu. Gerekçe: doğru bir cevap "bir yılı doldurduktan sonra kullanabilirsiniz" diyebilir; eski ölçüt bu cevabı haksız yere başarısız sayardı.
  - GKD-008'in beklenen davranışına "Asgari ücretin Asgari Ücret Tespit Komisyonu tarafından belirlendiğini söyleyebilir." eklendi.
  - Diğer 13 kayıt olduğu gibi onaylandı. 15 kaydın hepsinde `onay: "onaylandı (kullanıcı)"`. Ölçüldü: yalnızca bu üç alan değişti, başka alan değişmedi.
  - Set kilit manifestinde değil (geliştirme seti); yeni manifest üretilmedi. 02'deki çakışma denetiminden geçecek.
8. **Senior onayları:** `esikler_v1.md` (bütün satırlar, §3A ve yeni 3.9 dahil), `deney_plani_v1.md`, `rapor/rapor_plani_v1.md`, `cevap_standardi_v1.md`, `sistem_v1.txt`, `gelistirme_kapsam_disi.jsonl` (15 soru). Kullanıcı `cevap_standardi_v1.md` ve `sistem_v1.txt` için kararlarını verdi (karar 9–14). `gelistirme_kapsam_disi.jsonl` kullanıcı tarafından onaylandı (aşağıda); senior onayı yine bekliyor.
15. **Düşünme modu yan deneyi** (açık, karar 06'da verilecek): `hazir` model doğrulama setinde düşünme açık ve kapalı çalıştırılıp bilgi doğruluğu (bilgi puanı, kritik hata) ve süre karşılaştırılsın mı? Ana planda yok, hiçbir eşiği etkilemez. Yapılırsa 0.1'i bilerek ihlal ettiği için ayrı bir deney kimliğiyle yürütülmeli. Gerekçe: düşünme kapalılığının çok adımlı sorulardaki (ör. kıdem + ihbar birlikte) bedeli ölçülmedi. Ayrıntı `esikler_v1_aciklama.md`, 0.1 ek bölümü.
16. **Eşik açıklamasında listelenen zayıf noktalar** (açık, senior kararı): `esikler_v1_aciklama.md` §10'da 22 madde var. Hiçbiri düzeltilmedi. Öne çıkanlar:
    - 1.1'deki %60 koşulu hiç bağlayıcı değil (100 kararda p < 0,05 için %61 gerekir; ölçüldü, formülle).
    - §0 başlığı ile 0.3/0.4'ün sonucu çelişiyor.
    - Yargıç kalibrasyondan kalırsa yargıca dayalı koruma eşiklerinin durumu yazılmamış.
    - "Kaybetme − kazanma" eşiklerinde payda belirsiz.
    - §3A'daki sekiz ölçütlü tetikleyicinin neredeyse her zaman çalışması olası (tahmin).
    - Ele alınacaksa eşik onayından **önce** yapılmalı; onaydan sonra `esikler_v2.md` gerekir.

### Sonraki aşamanın ihtiyaç duyacağı bilgiler
- Kilitli desenler `src/veri/girdi_ozeti.py` içindeki `VARSAYILAN_KILITLI` listesinde. 02 ve sonrası bu listeye uymalı.
  - `01_sss/*` deseni listeye eklendi. Yeni `--ek-kilitli` seçeneği proje içindeki tek dosyaları kilitler. Geçerli manifest: `kilit_manifesti_v5.json`.
- **02'de Türkçe değerlendirme bölmesi:**
  - Dosya başına %30 / %70, seed 42, geliştirmede ≥ 50 kayıt.
  - Alt grubu olan dosyalarda (TurkishMMLU ders, `genel_kontrol` soru türü) katmanlı.
  - Betik yalnızca kimlik, sayı ve SHA-256 yazar.
  - Beklenen boyutlar `deney_plani_v1.md` §6.5'te.
  - `genel_kontrol_v1` ve `turkishmmlu_dev` bölünmez (karar 6). `genel_kontrol_v2` saklanan bölümdür.
- 02'deki çakışma denetimine `inceleme/genel_kontrol_v2_taslak.jsonl` (onaylı hâli) de girer. Karşılaştırılacak setler: eğitim adayları, genel Türkçe havuzu, `genel_kontrol_v1`, geliştirme kapsam dışı seti, doğrulama, test ve tuzak.
- v2 onaylandı ama henüz taşınmadı. 02'deki çakışma denetiminden sonra `degerlendirme/saklanan/genel_kontrol_v2.jsonl` yoluna taşınır, `kilit_manifesti_v6.json` üretilir ve hiçbir model çalışmadan önce commit edilir. Denetimde değişiklik gerekirse yeniden kullanıcı onayı alınır.
- v2'nin `b` soruları SSS konularına yakın (işsizlik ödeneği, yıllık izin, ihbar, süt izni vb.). 02'deki çakışma denetiminde test ve tuzakla yakın eşleşme çıkabilir; çıkarsa yalnızca kimlikle CSV'ye yazılır.
- **03 için önceden kayıtlı veri dönüşümleri** (`deney_plani_v1.md` karar 10 ve 11). İkisi de betikle yapılır, değişen kimlikleri yazar ve belirsiz kayıtları `inceleme/` kuyruğuna gönderir. Kilitli doğrulama ve test referanslarına dokunulmaz.
  1. **Kurum ağzı:** eğitim cevaplarındaki "Kurumumuz", "Bakanlığımız" ve çekimli biçimleri `kaynak` alanına göre kurum adıyla değiştirilir.
  2. **Eskimiş tutar** (kullanıcı onaylı): dönemsel TL tutarları kaldırılır, yerine hesaplama yolu ve kontrol önerisi yazılır. Kanunda belirlenmiş süre, gün ve oranlar korunur. Tutarın dönemsel mi yoksa kanunda sabit mi olduğu belirsizse kayıt inceleme kuyruğuna gider.
- 02'deki toplu sayımlarda doğrulama ve test referanslarında "Kurumumuz/Bakanlığımız" ve TL tutarı içeren kayıtların **yalnızca sayısı** çıkarılmalı; içerik basılmamalı. Bu sayılar rapor sınırlaması için gerekiyor.
- Sızıntı puanlama betiği işaret listesini kaydın `grup` alanına göre seçmeli (`a` / `b`), dosyadaki `yasak_kalip` alanını kullanmamalı (§6.6).
- 11'deki insan formu için 50 test sorusu, cevaplar üretilmeden önce kimlikle seçilir (seed 42, kaynağa göre katmanlı). Bu seçim 11'in ilk adımıdır, 02'de yapılmaz.
- Kilitli setler yalnızca toplu sayı, kimlik ve SHA-256 yazan betiklerle açılır. Çakışma denetiminde test ve tuzak içeren çiftler yalnızca kimlikle `inceleme/` CSV'sine yazılır.
- `gelistirme_kapsam_disi.jsonl` 02'deki çakışma denetimine dahil edilmeli.
- Few-shot havuzu yalnızca onaylı eğitim grubundan oluşur (karakter 3–5 gram TF-IDF, k=4).
- Yargıç adayları: `gemma4:12b` ve `gemma4:26b`. Kalibrasyon ancak eşik onayından ve doğrulama cevapları üretildikten sonra yapılır. Seçim kuralı `esikler_v1.md` 0.5'te.
- Üretim ayarı önerisi: greedy, `max_new_tokens=512`, `seed=42`, düşünme kapalı. Yükleme: HF + bitsandbytes NF4.
- Proje Python ortamı henüz kurulmadı. `pip freeze` şimdilik temel miniconda ortamından (Python 3.13.13).
- Qwen3.8 için LLaMA-Factory şablon adı (düşünme kapalı) doğrulanmadı (bekleyen iş).

### Değişen çalıştırılabilir kod veya komut yolları
- Yeni: `python -m src.veri.girdi_ozeti --girdi ... --cikti ... --kilit-cikti ...` (README "01" bölümü).
- Değişti: `src/veri/girdi_ozeti.py` artık `--ek-kilitli` seçeneğini kabul ediyor ve `01_sss/*` desenini varsayılan olarak kilitli sayıyor.
- Yeni: `python -m src.veri.ifade_say --girdi <jsonl ...> --ifade "<ifade>"`. Bir ifadenin kaç kayıtta geçtiğini sayar, içerik ve kimlik basmaz; kilitli setlerde de kullanılabilir (karar 13).
- Yeni: `python -m src.veri.onay_csv --girdi inceleme/genel_kontrol_v2_taslak.jsonl --cikti inceleme/genel_kontrol_v2_onay.csv` (karar 6c).
- Değişti: girdi özeti komutunun çıktıları artık `env/<tarih>_girdi_sha256_v5.json` ve `degerlendirme/kilit_manifesti_v5.json`.
- Değişti: `src/veri/onay_csv.py` sonunda onay dağılımını yazıyor. "düzelt"/"duzelt", "hayır"/"hayir" ve büyük/küçük harf aynı sayılıyor (`normal_onay`); hücredeki yazım değişmiyor. evet/hayir/duzelt dışındaki değerler kimlikle listeleniyor.
- Düzeltildi: `src/veri/onay_csv.py` artık betiğin kendi "-" yer tutucusunu "dolu satır" saymıyor. Önceki sürüm 45 yanlış "korunan" satır bildiriyordu; içerik farkı yoktu.
