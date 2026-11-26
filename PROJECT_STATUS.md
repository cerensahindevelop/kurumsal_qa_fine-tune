# PROJECT_STATUS

Son güncelleme: 2026-11-26 (bakım: tek güncel dosya düzeni, archive/ kaldırıldı; bakım: karar isteme kuralı; bakım: kilit manifesti değişiklik kaydı; bakım: onay yetkisi proje sahibine geçti; önceki: 2026-11-25, bakım: kanarya dosyaları kaldırıldı, erişim testi README'ye taşındı; bakım: eski kayıtlar archive/ altına taşındı; bakım: isimlendirme refactor'ı; önceki: 2026-11-24, 01: eşiklerin açıklamalı belgesi; eşik kararları: kritik/uyarı, tuzak −2, kalibrasyon 40, raporlama; açık kararlar 17–23 kapatıldı; proje sahibi onayı öncesi netleştirmeler; eşik paketi onaya hazır; `hazir_istemli` kapsamdan çıkarıldı) · Son tamamlanan aşama: **01**

---

> **Not (2026-11-26):** `archive/` klasörü kaldırıldı. Her kayıt türünün tek bir güncel dosyası var; eski hâller git geçmişinde. Aşağıdaki geçmiş kayıtlarda geçen `archive/…`, `lock_manifest_v<N>.json`, `env/<tarih>_…` ve `path_migration_*_2026-11-25.json` yolları o günün doğru kaydıdır ve değiştirilmedi (proje sahibi kararı 2A). Bu dosyaları görmek için: `git show 1919cce:<yol>`. Kilit manifesti sürümlerinin commit'leri: `evaluation/lock_manifest_changelog.md`.

## Bakım: tek güncel dosya düzeni, archive/ kaldırıldı (2026-11-26; aşama değil, 02'ye geçilmedi)

### Tamamlanan iş
- Kural (proje sahibi, 2026-11-26): her kayıt türünün tek bir güncel dosyası olur. Eski sürümler silinir ve git geçmişinde kalır.
- `archive/` tamamen kaldırıldı: `README.md`, kilit manifestleri v1–v5, `threshold_probabilities_v1.json`, girdi listeleri v1–v5, `2026-11-23_packages.txt`.
- Taşıma kayıtları silindi (karar 1B): `evaluation/path_migration_map_2026-11-25.json`, `evaluation/path_migration_manifest_2026-11-25.json`. Özetleri ve geri getiren commit'leri değişiklik kaydında.
- Tek dosyaya inenler:

  | Eski | Yeni | İçerik |
  |---|---|---|
  | `evaluation/lock_manifest_v6.json` | `evaluation/lock_manifest.json` | Başa `"version": 6` eklendi; başka fark yok |
  | `env/2026-11-25_input_sha256_v6.json` | `env/input_sha256.json` | Aynı |
  | `archive/env/2026-11-24_packages.txt` | `env/packages.txt` | Aynı |
  | `archive/env/2026-11-23_hardware.txt` | `env/hardware.txt` | Aynı |
  | `archive/degerlendirme/threshold_probabilities_v1.json` | `evaluation/threshold_probabilities.json` | Betikle yeniden üretildi; İngilizce anahtarlar, sayılar aynı |
- Kod:
  - `build_input_manifest`: tek dosyaya yazar. Kilitli dosyalar ya da kalıplar değişince `version` bir artar, değişmediyse kilit manifestine dokunulmaz. Git'e kaydedilmemiş bir dosyanın üzerine yazmaz (`ensure_committed`).
  - `compare_lock_manifests`: git'teki bir sürümü okur (`--old HEAD:evaluation/lock_manifest.json`). Arşiv yolu arama kodu kaldırıldı.
  - `build_path_migration_manifest`: yeni `--pair ESKİ YENİ` seçeneği; ayrı bir eşleme dosyası gerekmez. Çıktı tek dosya: `evaluation/path_migration.json`. Aynı üzerine yazma koruması var.
- CLAUDE.md: klasör ağacından `archive/` çıktı. "Her aşama sonunda" kuralı `env/packages.txt`, `env/input_sha256.json` ve `env/hardware.txt` olarak değişti.
- README: "Eski kayıtlar git geçmişinde" bölümü ve `git clone` uyarısı eklendi. 01 komutları tek dosyalara göre düzeltildi; yeni 1d (taşıma kaydı) komutu eklendi.
- Talimat niteliğindeki yerler güncellendi: 02 yapılacakları, 11. aşama kilit kontrolü, onaya hazır dosyalar, sonraki aşamanın ihtiyaç duyacağı bilgiler, planlar, öğrenme notları ve `inceleme/README.md`. Geçmiş kayıtlar olduğu gibi kaldı (karar 2A).

### Kararlar (proje sahibi, 2026-11-26; sohbette soruldu)
- **1B:** taşıma kayıtları silinir. Gerekçe: bir kerelik kanıttı ve işini yaptı; "tek güncel dosya" kuralına uyuyor; özet ve geri getiren commit değişiklik kaydında. 02 için tek `evaluation/path_migration.json`.
- **2A:** PROJECT_STATUS'taki geçmiş kayıtlar değiştirilmez; en üste not eklenir. Gerekçe: o gün doğru olan kayıt silinmez, yeni kayıt eklenir. Talimat niteliğindeki yerler güncellenir.
- **3A:** plan olduğu gibi uygulandı. Önkoşul kontrol edildi: `inceleme/` ve içindeki iki kilitli dosya silinecekler listesinde yoktu.

### Doğrulama sonuçları (ölçüldü)
- Değişiklik kaydı: v1–v6'nın altısı tabloda; altı commit kimliği git'teki ekleme commit'leriyle aynı. Arşivdeki v1–v5 o commit'lerdeki hâlleriyle bayt bayt aynı (5/5 SHA-256).
- Silmeden sonra `compare_lock_manifests` v1–v5'i git'ten okudu: beş çiftin sonuçları değişiklik kaydıyla aynı; test ve tuzak her çiftte 7/7 aynı.
- Taşınan env dosyaları kaynaklarıyla aynı SHA-256 (3/3). `lock_manifest.json` v6'dan yalnızca `version` satırıyla farklı.
- Eşik olasılıkları: yeni çıktı, v1 ile anahtar çevirisinden sonra birebir aynı.
- Sentetik git deposunda `build_input_manifest`: ilk çalıştırma sürüm 1; değişiklik yokken dosyaya dokunulmadı; veri değişince sürüm 2; kaydedilmemiş ya da değiştirilmiş dosyanın üzerine yazmayı reddetti (çıkış kodu 1).
- Kilitli dosyalar: sonuç aşağıdaki son doğrulamada.

### Değişen çalıştırılabilir kod veya komut yolları
- `python -m src.data.build_input_manifest … --output env/input_sha256.json --lock-manifest-output evaluation/lock_manifest.json`
- `python -m src.evaluation.compare_lock_manifests --old HEAD:evaluation/lock_manifest.json --new evaluation/lock_manifest.json [--path-migration evaluation/path_migration.json]`
- `python -m src.data.build_path_migration_manifest --pair <eski> <yeni> [--pair …] --base-ref HEAD --lock-manifest evaluation/lock_manifest.json --output evaluation/path_migration.json`
- `python -m src.evaluation.threshold_probabilities --output evaluation/threshold_probabilities.json`
- `pip freeze > env/packages.txt`; `nvidia-smi … > env/hardware.txt`

---

## Bakım: karar ve onay isteme kuralı (2026-11-26; aşama değil, 02'ye geçilmedi)

### Tamamlanan iş
- CLAUDE.md'ye "Karar ve onay isteme" bölümü eklendi. Karar gerektiğinde iş durur ve soru sohbette sabit düzenle sorulur (ne soruluyor, neden şimdi, seçenekler, öneri, etki). Bir mesajda en fazla üç karar sorulur. Cevap gelmeden o konuda bir şey uygulanmaz. Cevap ve gerekçesi PROJECT_STATUS'a kayıt olarak yazılır.
- Eski "kendi çözümünü uygula ve 'Varsayılan olarak uygulananlar' listesine yaz" kuralı kaldırıldı (aşağıda, "Çalışma kuralı: eşik paketindeki yeni belirsizlikler").
- Çelişki kalmasın diye CLAUDE.md'de iki satır uyarlandı: "Yalnızca şu durumlarda sor…" satırı yeni bölüme yönlendiriyor; PROJECT_STATUS şablonundaki "Açık kararlar" maddesi "Kararlar: cevaplananlar ve gerekçeleri; sorulmuş ama cevabı bekleyenler" oldu.
- V1–V6 "onay bekliyor" olarak işaretlendi. V1–V3 bu sohbette soruldu; V4–V6 bu üç soru cevaplanınca sorulacak (bir mesajda en fazla üç karar kuralı).
- Kilit manifesti değişiklik kaydı (aynı istekteki 1. madde) bir önceki bakımda yapılmıştı (`c5f4fe1`, `1f2cb74`); yeniden yapılmadı.

### Kararlar
- **V1, V2, V3: onaylandı (proje sahibi, 2026-11-26; üçünde de A, yani dosyalarda uygulanmış olan hâl).** Hiçbir dosya değişmedi; `thresholds_v1.md` §6.2 U.2 olduğu gibi kaldı.
  - V1 (3.1, TurkishMMLU): yalnızca iki sistemden birinin doğru bildiği sorular, iki yönde incelenir. Gerekçe: farkı yalnızca ayrışan sorular yaratır; doğru/yanlış sorularda "en olumsuz 20" sıralaması anlamsızdır.
  - V2 (3.8, harf çıkarılamayan oran): harf çıkarılamayan bütün cevaplar + harf çıkarılan cevaplardan seed 42 ile 20 rastgele cevap. Gerekçe: betik iki yönde yanılabilir; yalnızca tek yöne bakmak düzeltmeyi hep adaptör lehine işletir. Ek yük 20 kayıt.
  - V3 (2.2, 3.6, ikili karşılaştırma): yargıcın iki sırada tutarlı karar verdiği kayıplar ve kazançlar; beraberlikler incelenmez. Gerekçe: V1 ile aynı ilke (ayrışmayan kayıtlara bakılmaz); yalnızca kayıplar tek yönlü olur; beraberlikleri eklemek iş yükünü neredeyse ikiye katlar.
- **V4, V5, V6: onaylandı (proje sahibi, 2026-11-26; üçünde de A, yani dosyalarda uygulanmış olan hâl).** Hiçbir dosya değişmedi; `thresholds_v1.md` §6.2 U.2 ve U.5 olduğu gibi kaldı.
  - V4 (2.3, 3.9 ortalama koşulu): farkı en olumsuz 20 + en olumlu 20 + kalanlardan seed 42 ile 10 rastgele kayıt. Gerekçe: iki yönlü; rastgele 10 kayıt düşüşün birkaç uç kayıttan mı genelden mi geldiğini gösterir.
  - V5 (sınır ve körlük): her yönde en fazla 40 kayıt; CSV'de yön gösterilmez, kayıtlar seed 42 ile karışık sıralanır. Gerekçe: tek toplam sınır bir yönü kırpabilir; yönü görmek değerlendiriciyi farkında olmadan yanlı yapabilir.
  - V6 (kritik eşiklere taşıma): uyarı incelemesindeki düzeltmeler kritik eşiklere (2.1, 3.7, 4.2) taşınmaz. Gerekçe: kritik eşikler incelemeyle esnetilmez; taşıma bu kuralı dolaylı yoldan delerdi.
- V1–V6 tamamlandı. V7–V10 ve isimlendirme bakımındaki numarasız varsayılanlar bu turda sorulmadı (kapsam dışı).

---

## Bakım: kilit manifesti değişiklik kaydı (2026-11-26; aşama değil, 02'ye geçilmedi)

### Tamamlanan iş
- Yeni betik `src/evaluation/compare_lock_manifests.py`: iki manifesti karşılaştırır; eklenen, çıkarılan, parmak izi değişen ve aynı kalan dosyaları yalnızca yol ve 12 karakterlik kısa parmak iziyle yazar. Kilitli dosyaları açmaz, yalnızca manifestleri okur.
  - Eski Türkçe alanlı (v1–v5) ve İngilizce alanlı (v6) manifestleri okur (`LEGACY_FIELD_NAMES`).
  - `--path-migration` ile verilen taşıma listesine göre taşınan dosyayı "taşındı" olarak eşler. Manifestin kendisi taşındıysa eski yolundan yeni yerini bulur.
  - Test ve tuzak dosyaları için ayrı bir özet satırı yazar (`--focus-patterns`).
- Yeni dosya `evaluation/lock_manifest_changelog.md`: v1–v6 için sürüm, tarih, ne değişti, hangi dosya, neden ve commit.
- README'ye "1a" kuralı ve komutu eklendi.

### Doğrulama sonuçları (ölçüldü)
- Beş ardışık çift: v1→v2 2 dosya eklendi (ham `01_sss`, `genel_kontrol_v2` taslağı) ve `01_sss/*` kalıbı eklendi; v2→v3, v3→v4 ve v4→v5 yalnızca taslağın parmak izi değişti; v5→v6 27/27 aynı.
- Test ve tuzak dosyaları (7 dosya) her çiftte ve v1→v6 doğrudan karşılaştırmada 7/7 aynı. v1'in 25 dosyasının 25'i v6'da aynı.
- Sentetik manifestlerle test: taşıma listesiyle taşınan dosya "aynı kaldı (taşındı)" çıktı; liste olmadan "çıkarıldı + eklendi". Eklenen, çıkarılan ve değişen dosya ile yeni kalıp doğru yakalandı. Eski manifest yolu (`degerlendirme/kilit_manifesti_v4.json`) taşıma eşlemesiyle arşivdeki dosyaya çözüldü. Olmayan manifestte betik hatayla durdu.
- v1–v5 commit'leri eski yollarla bulundu (`0820870`, `b4ebb4e`, `518aa58`, `35f1a69`; v1 `914c1e8`). Arşive taşınan yolda `git log --follow` beşi için de yanlışlıkla `914c1e8` gösterdi; kayıtta bu not var.

### Değişen çalıştırılabilir kod veya komut yolları
- Yeni: `python -m src.evaluation.compare_lock_manifests --old … --new … [--path-migration …] [--focus-patterns …] [--output …]`.

---

## Bakım: onay yetkisi proje sahibine geçti (2026-11-26; aşama değil, 02'ye geçilmedi)

### Tamamlanan iş
- Bu projede onayları proje sahibi (kullanıcı) verir; başka bir onaylayıcı yoktur (kullanıcı kararı, 2026-11-26).
- Eski onaylayıcı adıyla yazılmış bütün onay ve karar ifadeleri ("… onayı: bekliyor", "… onayıyla commit edilir", "nihai kararı … verir", "… kararı yalnızca servise çıkış hakkındadır") "proje sahibi" olarak değişti. Kapsam: CLAUDE.md (yazma izni verildi), PROJECT_STATUS.md, `evaluation/thresholds_v1.md`, `evaluation/thresholds_v1_explained.md`, `evaluation/experiment_plan_v1.md`, `report/report_plan_v1.md`, `prompts/response_standard_v1.md`, `docs/learning/01_skeleton_and_plan.md`. README'de onay ifadesi yoktu.
- Eşik tablolarındaki 8 onay sütununun başlığı "Onay (proje sahibi)" oldu. Genel onay satırı "Proje sahibi onayı (genel): bekliyor".
- Uyarı eşiği kuralının (§1, §6.2 U.3–U.5) anlamı değişmedi: proje sahibinin kararı yalnızca servise çıkış hakkındadır ve birincil sonucu "geçti"ye çeviremez.
- Onay durumları "bekliyor" olarak kaldı. Henüz hiçbir şey onaylanmadı. Proje sahibi 01'i öğrendikten sonra onay verecek; onay tarihi ve commit kimliği dosyalara ayrı bir commit'le yazılacak.
- Rapor ve sunum ifadeleri bilerek değişmedi: o kişi raporun okuyucusudur, onaylayıcı değil.

### Doğrulama sonuçları (ölçüldü)
- 60 değişiklik, 8 dosya; betik her değişikliğin beklenen sayıda yapıldığını saydı.
- Git farkı: değişen 8 dosyanın hepsinde sayı dizisi önceki commit'le aynı, satır sayıları aynı. Hiçbir eşik değeri değişmedi.
- Metin araması (archive/ hariç; arşiv değiştirilmez): eşleşme 78'den 18'e indi. Kalanlar:
  - 1 rol tanımı: CLAUDE.md'deki "… AI engineer" satırı (Claude'un rolü, onayla ilgisi yok).
  - 3 rapor adı: CLAUDE.md klasör ağacı, README klasör tablosu, `report/report_plan_v1.md`.
  - 14 okuyucu ve sunum anlamı, hepsi `thresholds_v1_explained.md`'de ("Okuyucu: …", "… denebilir/sunulur", "… diye sorarsa", "… sunumunda").

---

## Bakım: kanarya dosyaları kaldırıldı, erişim testi README'ye taşındı (2026-11-25; aşama değil)

### Tamamlanan iş
- `kanarya.txt` ve `kanarya_klasor/` silindi. `.claude/settings.json`'daki iki kanarya kuralı kaldırıldı; yerine kalıcı `Read(//home/aipc/Desktop/Projeler/kurum-qa-finetune/security_check/**)` kuralı eklendi. `security_check/` projede bulunmaz; yalnızca test sırasında geçici oluşturulur ve `.gitignore`'dadır.
- README'ye "Erişim engeli testi" bölümü yazıldı (ne zaman, neden gerçek test dosyasıyla değil, adımlar, reddedilmezse ne yapılır).
- Kullanıcı kararları (2026-11-25): `archive/degerlendirme/` adı olduğu gibi kalır (dosyaların o zamanki yerini gösterir). Kilitli dosyaların İngilizce adları 02'deki taşımada uygulanır (aşağıda).

### Doğrulama sonuçları (ölçüldü)
- `settings.json` geçerli JSON; deny kuralı 10 → 9. Kaldırılan 2 (kanarya), eklenen 1 (`security_check/**`). Test, tuzak ve girdi klasörlerini koruyan 8 kural aynen duruyor (8/8).
- `git check-ignore`: `security_check/` ve `security_check/canary.txt` `.gitignore:48` ile dışarıda.
- Yeni kural bu oturumda etkin: `security_check/canary.txt` okuma denemesi "izin ayarlarınca reddedildi" cevabı aldı. Dosya oluşturma komutu bu oturumda reddedildiği için deneme dosyasız yapıldı; içerikli tam test README adımlarıyla yeni bir oturumda kullanıcı tarafından yapıldı.
- Erişim engeli testi (kullanıcı, 2026-11-25; ölçüldü): Reload Window sonrası yeni sohbette `security_check/canary.txt` okuma denemesi reddedildi. Deny kuralları çalışıyor.

### 02'nin yapılacakları (bu bakımdan)
- Çakışma denetiminden sonra kilitli dosyalar İngilizce adlarıyla taşınır:
  - `inceleme/genel_kontrol_v2_taslak.jsonl` → `evaluation/held_out/general_control_v2.jsonl`
  - `inceleme/genel_kontrol_v2_onay.csv` → `review/general_control_v2_review.csv`
- Taşımadan önce ve sonra SHA-256 aynı olmalı. Kanıt `python -m src.data.build_path_migration_manifest --pair <eski> <yeni> … --base-ref HEAD --lock-manifest evaluation/lock_manifest.json --output evaluation/path_migration.json` ile tek dosyaya yazılır (README 1d). Ardından `build_input_manifest` yeniden çalıştırılır; `evaluation/lock_manifest.json` güncellenir, `version` 7 olur ve hiçbir model çalışmadan önce commit edilir. *(2026-11-26'da tek dosya düzenine göre güncellendi.)*
- Sürüm 7 üretilince, commit etmeden önce `python -m src.evaluation.compare_lock_manifests --old HEAD:evaluation/lock_manifest.json --new evaluation/lock_manifest.json --path-migration evaluation/path_migration.json` çalıştırılır. `evaluation/lock_manifest_changelog.md` tablosuna v7 satırı eklenir. Beklenen: taslak "aynı kaldı (taşındı)", test ve tuzak 7/7 aynı. Bu kural bundan sonraki her manifest sürümü için geçerlidir (README "1a").
- Taşımadan sonra `inceleme/` boşalırsa silinir. `evaluation/held_out/**` için Read deny kuralı eklenir (settings.json değişeceği için README'deki erişim engeli testi yapılır).
- Belgelerdeki `genel_kontrol_v2` veri seti adı ve dosyadaki Türkçe alan adları (`grup`, `beklenen_davranis` gibi) kilit gereği değişmez; okuyan kod `LEGACY_*` eşlemelerini kullanır.

---

## Bakım: eski kayıtlar archive/ altına taşındı (2026-11-25; aşama değil, 02'ye geçilmedi)

### Tamamlanan iş
- 14 tarihî dosya `archive/` altına taşındı; klasör yapısı korundu, dosya adları İngilizceye çevrildi:
  - `degerlendirme/kilit_manifesti_v1–v5.json` → `archive/degerlendirme/lock_manifest_v1–v5.json`
  - `degerlendirme/esik_olasiliklari_v1.json` → `archive/degerlendirme/threshold_probabilities_v1.json`
  - `env/2026-11-23_girdi_sha256(_v2–v5).json` → `archive/env/2026-11-23_input_sha256_v1–v5.json`
  - `env/2026-11-23_donanim.txt`, `env/2026-11-2[34]_paketler.txt` → `archive/env/…_hardware.txt`, `…_packages.txt`
- Boşalan `degerlendirme/` silindi. `env/` altında yalnızca güncel `2026-11-25_input_sha256_v6.json` kaldı.
- `archive/README.md` (ne olduğu, neden saklandığı) ve yeni `inceleme/README.md` yazıldı. `inceleme/` altındaki kilitli `genel_kontrol_v2` dosyalarına dokunulmadı.
- 14 çift `evaluation/path_migration_map_2026-11-25.json` eşlemesine eklendi; `evaluation/path_migration_manifest_2026-11-25.json` 38 kayıtla yeniden üretildi (`--base-ref 59aa89e`).
- README, PROJECT_STATUS, planlar, öğrenme notları, CLAUDE.md ve kod docstring'lerindeki atıflar yeni yollara güncellendi. Tarihî notlardaki atıflar da arşivdeki yeni yolu gösterir.

### Doğrulama sonuçları (ölçüldü)
- Taşımadan önce diskte ve sonra yeni yerde: 14/14 aynı SHA-256. Migration manifesti: arşiv çiftleri 14/14 `content_unchanged`; toplam 38 kayıt, kayıp 0, içeriği değişen kilitli dosya 0.
- Aşağıdaki "Kilit kontrolü" ve "--help" sonuçları bu bakımın son durumu içindir (özet bölümüne bakın).

### 11. aşamadaki kilit kontrolü
- *(2026-11-26'da güncellendi.)* Kontrol tek dosyayı kullanır: `evaluation/lock_manifest.json`. Sürüm dosyanın içindeki `version` alanındadır; şu an 6. 02'de `genel_kontrol_v2` taşınınca 7 olur; 11'de beklenen sürüm 7.

---

## Bakım: isimlendirme refactor'ı (2026-11-25; aşama değil, 02'ye geçilmedi)

### Tamamlanan iş
- Dosya, modül, fonksiyon, CLI ve proje veri alanı adları yerleşik İngilizce teknik terimlere çevrildi; README ve öğrenme notları Türkçe kaldı. Dokümanlarda "istem" → "prompt", "sistem mesajı" → "system prompt", deney etiketi `hazir` → `baseline` (karşılaştırma sistemi; `base_model` ile karıştırılmaz).
- CLI seçeneklerinin yalnızca İngilizce adı var (kullanıcı kararı, 2026-11-25: kafa karışmasın). Eski Türkçe adlar (`--girdi`, `--cikti`, `--kilit-cikti`, `--kilitli`, `--ek-kilitli`, `--ifade`, `--kotulesme`) kaldırıldı; eski adla yazılan komut hata verir. JSONL alanları ve CSV başlıkları için eski adları okuma desteği (`LEGACY_*`) duruyor.
- Bütün `.py` dosyalarının docstring ve yorumları CLAUDE.md'deki yeni şablona göre (Ne yapar / Neden var / Ne alır / Ne döndürür / Nasıl çalışır) Python bilmeyen bir okur için yeniden yazıldı. Docstring'lerdeki örnek sayılar betikle doğrulandı.
- Deney kısa adları: `hazir` → `baseline`, `sss_adaptor` → `faq_adapter`, `sss_sentetik_adaptor` → `faq_synthetic_adapter`, `genel_karisim_adaptor` → `general_mix_adapter` (bütün aktif belgelerde; CLAUDE.md tablosunda açık adlar Türkçe kaldı). Henüz deney koşulmadığı için eski adlı deney çıktısı yok.
- CLAUDE.md'ye "Kod yazım kuralları" bölümü eklendi (Türkçe docstring ve blok yorumları, kısaltmasız adlar, adlandırma). Bütün `.py` dosyaları bu kurallara göre yeniden yazıldı; `__init__.py` dosyalarına paketi tanıtan birer docstring eklendi. Davranış değişmedi (aşağıda ölçüm).
- Yeni betik `src/data/build_path_migration_manifest.py`: taşınan dosyaların eski/yeni yolunu ve SHA-256 özetini yazar. Çıktı `evaluation/path_migration_manifest_2026-11-25.json` (eşleme: `evaluation/path_migration_map_2026-11-25.json`).
- Yeni kilit manifesti `evaluation/lock_manifest_v6.json` ve `env/2026-11-25_input_sha256_v6.json` (yeni alan adlarıyla; içerik v5 ile aynı).
- Eşik değerleri, değerlendirme mantığı, veri bölmeleri, system prompt metni ve kilitli dosyalar değişmedi. `hazir_istemli` yalnızca tarihî ad olarak geçiyor.

### Eski ad → yeni ad
| Eski | Yeni |
|---|---|
| `istemler/`, `sistem_v1.txt`, `cevap_standardi_v1.md` | `prompts/`, `system_prompt_v1.txt`, `response_standard_v1.md` |
| `src/veri/` (`girdi_ozeti`, `onay_csv`, `ifade_say`) | `src/data/` (`build_input_manifest`, `build_review_csv`, `count_phrase_matches`) |
| `src/degerlendirme/esik_olasiliklari.py` | `src/evaluation/threshold_probabilities.py` |
| `src/egitim/`, `src/uretim/`, `src/servis/` | `src/training/`, `src/data_generation/` (öğretmen modelle eğitim verisi üretimi; model cevapları `evaluation/` tarafında), `src/serving/` |
| `degerlendirme/esikler_v1.md`, `esikler_v1_aciklama.md`, `deney_plani_v1.md`, `gelistirme_kapsam_disi.jsonl` | `evaluation/thresholds_v1.md`, `thresholds_v1_explained.md`, `experiment_plan_v1.md`, `dev_out_of_scope_v1.jsonl` |
| `rapor/rapor_plani_v1.md`, `docs/ogrenme/01_iskelet_ve_plan.md`, `PROJE_DURUMU.md` | `report/report_plan_v1.md`, `docs/learning/01_skeleton_and_plan.md`, `PROJECT_STATUS.md` |
| `inceleme/` (yeni kuyruklar) | `review/` |
| Deney adları `hazir`, `sss_adaptor`, `sss_sentetik_adaptor`, `genel_karisim_adaptor` | `baseline`, `faq_adapter`, `faq_synthetic_adapter`, `general_mix_adapter` |
| Eşik olasılıkları çıktı anahtarları (`yanlis_alarm_tol1`, `uyum_yari_genislik_pp`, `n`…) | `false_alarm_tolerance_1`, `agreement_half_width_percentage_points`, `decision_count`… (tam eşleme `LEGACY_OUTPUT_KEYS`) |
| `experiments.csv`: `deney_id, kisa_ad, …, taban_model, yukleme, …, sistem_istemi, …, kart, durum, …, cikti_klasoru, not` | `experiment_id, short_name, …, base_model, quantization, …, system_prompt, …, gpu, status, …, output_dir, notes` |
| Geliştirme seti alanları `kategori, soru, beklenen_davranis, kabul_olcutu, kaynak, onay` | `category, question, expected_behavior, acceptance_criteria, source, approval` (değerler aynı) |
| Manifest alanları `olusturma, dosyalar, desenler, kok, yol, bayt, satir, kilitli` | `created_at, files, patterns, root, path, bytes, lines, locked` (v6'dan itibaren) |
| Onay CSV başlıkları `grup, kategori, bilgi_ogeleri, onay (…), bilgi_ogeleri_dogru_mu (…), not` | `group, category, knowledge_items, approval (…), knowledge_items_correct (…), notes` |

### Yerinde korunanlar (taşınmadı, değişmedi)
- Eski kilit manifestleri v1–v5 ve eşik olasılıkları v1: tarihî çıktılar, Türkçe alan adlarıyla. Bu refactor'da yerinde kaldılar; aynı gün sonraki bakımda içerikleri değişmeden `archive/degerlendirme/` altına taşındılar. Karşılıklar `LEGACY_FIELD_NAMES` ve `LEGACY_OUTPUT_KEYS` sözlüklerinde.
- `inceleme/genel_kontrol_v2_taslak.jsonl` (kilitli; v2–v5 manifestleri bu yolu kaydetti) ve `inceleme/genel_kontrol_v2_onay.csv` (kilitli prompt'lar ve kullanıcı onayları). Taslağın alan adları (`grup`, `kategori`, `beklenen_davranis`, `bilgi_ogeleri`, `yasak_kalip`…) değiştirilemez; `build_review_csv` bunları okur.
- `env/2026-11-2*` kayıtları, `kanarya*` (deny kuralı sınama dosyaları; sonraki bakımda kaldırıldı), `.claude/settings.json`, dış girdi yolları (`/home/aipc/Desktop/...`) ve `DEFAULT_LOCKED_PATTERNS` içindeki dış göreli yollar (`degerlendirme/test.jsonl` vb.).

### Doğrulama sonuçları (hepsi ölçüldü; eğitim, çıkarım ve kilitli test çalıştırılmadı)
- Docstring şablonuna göre yeniden yazım ve takma adların kaldırılmasından sonra test yeniden çalıştırıldı: 11/11 geçti (aynı kontroller; takma ad kontrolü yerine "eski Türkçe seçenekler reddediliyor" kontrolü).
- İlk kod yazım kuralları turundan sonra eşdeğerlik testi yeniden çalıştırıldı: 13/13 kontrol geçti (manifest, o tarihte duran takma adlar, ifade sayımı, CSV başlık eşlemesi ve onay taşıma, onay dağılımı, ikinci çalıştırmanın bayt bayt aynılığı, eşik olasılıkları; v1 JSON ile karşılaştırma artık yalnızca `LEGACY_OUTPUT_KEYS` sözlüğüyle yapılıyor, ek kural gerekmiyor).
- Taşınan 24 izlenen dosya: eşleme, HEAD'de olup diskte olmayan 24 yolla birebir aynı. Hiçbiri kilitli değil. 7'sinin içeriği aynı (system prompt ve 6 `.gitkeep`); 17'si bilerek değişti (belgelerde yol ve terim, kod yeniden yazımı, `__init__.py` docstring'leri, geliştirme setinde alan adları).
- `lock_manifest_v6.json`: v5 ile 27/27 aynı yol ve SHA-256, desenler aynı; girdi özeti v6, v5 ile 506/506 aynı.
- Kanarya testleri: `kanarya.txt` ve `kanarya_klasor/ic.txt` okuma denemesi deny kuralıyla reddedildi. Proje içinde taşınan kilitli yol olmadığı için `.claude/settings.json` bu bakımda değiştirilmedi (kanaryalar sonraki bakımda kaldırıldı).
- Dört modül yeni yoluyla `--help` veriyor; beş `src` alt paketi import ediliyor.
- Sentetik girdilerde eski (HEAD) ve yeni betik: manifest kayıtları, SHA-256, bayt ve satır sayıları, anahtar eşlemesinden sonra eşdeğer (takma adlı çağrıda da). İfade sayımı aynı (3 ve 1). Eşik olasılıkları eski betik çıktısıyla ve depodaki `archive/degerlendirme/threshold_probabilities_v1.json` ile eşdeğer.
- `build_review_csv`: eski Türkçe başlıklı, dolu CSV'den onay, bilgi onayı ve not hücreleri `id`'ye göre aynen taşındı ("Düzelt", sondaki boşluklu "duzelt " dahil); onay dağılımı ve tanımsız değer listesi eskisiyle aynı. Yeni başlıklı CSV'de ikinci çalıştırma bayt bayt aynı. İngilizce alan adlı girdi de çalışıyor.
- Gerçek girdiler (yalnızca sayı basıldı): yeni manifest betiği 27/27 kilitli dosyada `archive/degerlendirme/lock_manifest_v5.json` ile, 506/506 dosyada `archive/env/2026-11-23_input_sha256_v5.json` ile aynı SHA-256/bayt/satır; desen listesi aynı. Çıktılar geçici klasöre yazıldı ve silindi, yeni manifest üretilmedi.
- `thresholds_v1.md` ve `thresholds_v1_explained.md`'de sayı dizisi önce/sonra birebir aynı (1232 ve 1943 sayı); satır sayıları ve satır numaralı atıflar değişmedi. `experiment_plan_v1.md`'deki tek sayı farkı dosya adındaki `_v1`.
- `git check-ignore`: `evaluation/responses/`, `*_responses.jsonl`, eski `*_cevaplar.jsonl` desenleri, `data/**/*.jsonl`, checkpoint/adaptör/pid, `.env`, `settings.local.json` dışarıda; eşik belgeleri, geliştirme seti, `review/*.csv`, `run.log` izleniyor.
- System prompt, kilitli taslak ve onay CSV'si HEAD ile bayt bayt aynı (SHA-256).

### Varsayılan olarak uygulananlar (kullanıcının gözden geçirmesini bekliyor)
- "Tarihî manifestleri yerinde koru" ve "kilitli içeriği taşıma" kuralları nedeniyle eski `degerlendirme/` ve `inceleme/` klasörleri başta yalnızca tarihî dosyalarla kaldı. Sonraki bakımda (yukarıda) tarihî kayıtlar `archive/` altına toplandı; `inceleme/` yalnızca kilitli dosyalarla duruyor.
- Onaya hazır dosyaların yolu ve terimleri değişti; içerik ve eşik değerleri aynı. Proje sahibi onay için commit kimliği yazarken `--follow` kullanılmalı.
- v6 numarası bu bakımda kullanıldı; `genel_kontrol_v2` 02'de taşınınca üretilecek manifest v7 olur (belgeler buna göre güncellendi). **11. aşamadaki kilit kontrolü o gün geçerli en yüksek numaralı `evaluation/lock_manifest_v<N>.json`'u kullanır; beklenen v7.**
- Geliştirme setinde örnek doğru cevabı tutan ayrı bir alan yok (`acceptance_criteria` bir ölçüttür, cevap değildir); bu yüzden `reference_answer` adı kullanılmadı. Kilitli setlerdeki alanlar değiştirilemez.
- Henüz yazılmamış betiklerin planlanan sütun ve etiket adları (ör. `neden`, `duzeltilmis_etiket`, `gercek_hata`) belgede olduğu gibi bırakıldı; betik yazılırken İngilizce adlandırılacak. Yalnızca planlanan yollar çevrildi (`src/evaluation/warning_review_queue.py`, `review/human_form_v1.csv`, `evaluation/held_out/`, `evaluation/responses/`).

### Değişen çalıştırılabilir kod veya komut yolları
- `python -m src.data.build_input_manifest --input … --output … --lock-manifest-output … [--extra-locked …] [--locked-patterns …]`
- `python -m src.data.build_review_csv --input … --output …`
- `python -m src.data.count_phrase_matches --input … --phrase …`
- `python -m src.evaluation.threshold_probabilities --output evaluation/threshold_probabilities_v2.json [--degradation 3]`
- Yeni: `python -m src.data.build_path_migration_manifest --mapping … --base-ref … --lock-manifest … --output …`
- Ortam kayıtları: `env/<date>_packages.txt`, `env/<date>_hardware.txt`. Aşağıdaki 01 bölümündeki komut adları bu bakımda yeni adlarla güncellendi.

---

## 01: Proje iskeleti, cevap standardı, deney planı, eşik taslağı (2026-11-23)

### Tamamlanan iş
- Proje kökü belirlendi: `/home/aipc/Desktop/Projeler/kurum-qa-finetune`. Git deposu başlatıldı (`main`).
- CLAUDE.md'deki klasör yapısı kuruldu. `src/` alt paketlerine `__init__.py` eklendi.
- Cevap standardı ve tek system prompt (`system_prompt_v1.txt`) yazıldı.
- Deney planı (ön kayıt taslağı) hazırlandı: sistemler, doğrulama ve test sırası, birincil/ikincil sonuç ayrımı, sentetik katkısının test karşılaştırması, few-shot önerisi, puanlama tanımları, metrik sınırları, yargıç adayları ve kalibrasyon kuralı, beş açık karar ve mini puanlama gösterimi.
- Eşik taslağı (`thresholds_v1.md`) yazıldı. Bütün satırlarda "Onay (proje sahibi): bekliyor" yazıyor.
- Geliştirme kapsam dışı seti için 15 soruluk taslak yazıldı (tuzak setine bakılmadan).
- Girdi SHA-256 özeti ve kilit manifesti üretildi. Paket ve donanım kaydı alındı.
- Eğitim başlatılmadı. Hiçbir model çalıştırılmadı.
- **Eşik kararları (kullanıcı, 2026-11-24; onaydan önce, aynı dosyaya işlendi):**
  - Yalnızca 2.1, 3.7 ve 4.2 kritik; §2–§4'teki diğer 14 eşik uyarı. Uyarı aşılırsa kırmızı bayrak, betikle seçilen kayıtların insan incelemesi ve proje sahibinin kararı gelir. Süreç `thresholds_v1.md` §6.2'de tanımlı.
  - §1'deki birincil sonuç cümlesi bu ayrıma göre yeniden yazıldı. §3A tetikleyicisi bu ayrımdan etkilenmiyor.
  - 4.1 "adaptör ≥ `hazir_istemli` − 2" oldu (2026-11-24'te `hazir_istemli` kapsamdan çıkınca "adaptör ≥ `baseline` − 2").
  - Yargıç kalibrasyonu 40 çifte çıktı (`thresholds_v1.md` 0.3 ve 0.5, `experiment_plan_v1.md` §6.8 ve §6.9, `report_plan_v1.md` §4).
  - Raporlama kuralı (`thresholds_v1.md` §7): kazanma oranı tek başına yazılmaz; kazanma / beraberlik / kayıp sayıları ve p değeri birlikte verilir.
  - Holm ailesi önerildi; karar kullanıcıda (açık karar 17).
  - Gerekçelerdeki olasılıklar betikle yeniden hesaplandı (`thresholds_v1.md` §8).
  - `thresholds_v1_explained.md` güncellendi: yeni §9 (kritik/uyarı) ve §10 (raporlama), 4.1 yeniden yazıldı, örnekler yeni raporlama biçimine çevrildi, sözlüğe 5 terim eklendi, "fark ettiklerim" 27 maddeye çıktı.
  - `docs/learning/01_skeleton_and_plan.md` §10 eklendi.
- **Açık kararlar 17–20 kapatıldı (kullanıcı, 2026-11-24; onaydan önce, `thresholds_v1.md` §8 değişiklik 5–8 ve yeni §9):**
  - 17: Holm ailesi seçenek A, m = 3 (H1 5.1, H2 prompt'un katkısı, H3 adaptör vs `baseline`).
  - 18: 2.1b'deki "çelişirse insan kararı geçerlidir" cümlesi kaldırıldı. İnsanın 50 sorudaki "kritik hata var/yok" etiketi 2.1'de yargıç + betik etiketinin yerini alır (birleşik etiket, §9.1). Bunun için insan formunun bilgi bölümüne ayrı bir "Kritik hata var mı?" alanı eklendi (`experiment_plan_v1.md` §6.9); "Hayır" kritik hatayla aynı şey değildi.
  - 19: yargıç yedek yolu (§9.2). Önce diğer aday; ikisi de kalırsa tuzak insan puanıyla, kritik 2.1 50 insan sorusunda fark ≤ +2 ile, yargıca dayanan uyarılar "güvenilirliği düşük" notuyla. 1.1/1.2 kuralıyla tutarlılığı kontrol edildi; §1'deki tekil "yargıç" ifadesi "iki aday da" diye düzeltildi.
  - 20: kalibrasyon soruları prompt ayarından çıkarılmaz (`experiment_plan_v1.md` §6.8 madde 6); sınırlama `report_plan_v1.md` §4.4'e eklendi.
- **Açık karar 21 kapatıldı (kullanıcı, 2026-11-24; `thresholds_v1.md` §8 değişiklik 9, §9.1–§9.3):**
  - (a) Normal yolda 2.1'in `baseline` karşılaştırması iki tarafta da yargıç + betikle.
  - (b) Yedek yolda 2.1'in `baseline` karşılaştırması betik kısmıyla (2.4 tanımı), "güvenilirliği düşük".
  - (c) Yedek yolda ikincil iddia yok: "güvenilir ölçüm yapılamadı, iddia yapılmadı".
  - (d) 0.3/0.4'ün prompt türü başına ayrı ölçüldüğü yazılı değildi (insan etiketi ve yargıç prompt'u ayrıydı, eşik hesabı tanımsızdı); ayrı ölçüm tanımlandı (§9.3). Yedek yol yalnızca kalınan türe dayanan eşiklere uygulanır. Sonuç: iki prompt türü farklı adaylarla puanlanabilir.
  - "Fark ettiklerim" 30 maddesi üç gruba ayrıldı (açık karar 16'da); hiçbiri düzeltilmedi.
- **Proje sahibi onayı öncesi netleştirmeler ve açık karar 22 (kullanıcı, 2026-11-24; `thresholds_v1.md` §8 değişiklik 10).** Hiçbir eşik değeri değişmedi:
  - #1: 1.1'den "≥ %60" kaldırıldı; kural "işaret testi p < 0,05". Gereken en az galibiyet tablosu §1'de (betikle, ölçüldü).
  - #2: §0 ikiye ayrıldı: 0.1–0.2 geçerlilik koşulu (koşu tekrarlanır), 0.3–0.5 yargıç uygunluğu (yedek yol).
  - #6: 0.5 prompt türü başına; 26B yalnızca uyumda 5 pp'den fazla öndeyse; yalnızca biri geçerse o.
  - #7: "kaybetme − kazanma" paydası bütün kayıtlar, beraberlikler dahil.
  - #8: sınır kuralı: eşiğe eşit değer geçer, aşan kalır; karşılaştırma yuvarlamadan önce.
  - #9: 3.8 ve T.8 değerlendirilen adaptöre uygulanır; T tablosunun başlığı düzeltildi.
  - #12: K.2 pay seçimi (net kazanç; 5 pp içinde %10; hiçbiri geçmezse K.3).
  - #15: 50 soruda +2 bilinçli onaylandı; oransal fark rapor planına yazıldı.
  - #20: 4.3 doğrulamada seçim kısıtı; uyarı sınıfından çıktı (uyarı eşikleri 14 → 13).
  - #24: uyarı incelemesi yalnızca kayıt etiketlerini düzeltir, eşik yeniden hesaplanır, hâlâ aşılıyorsa birincil sonuç "çekinceli". Sonuç artık üç değerli: geçti / çekinceli / kaldı. Proje sahibinin kararı yalnızca servise çıkış hakkında.
  - Karar 22: Aya (3.6, T.6) üslup+jargon türüne bağlandı. Tek yargıç kuralı eklenmedi.
  - Rapor planı: özet üç değerli; 2.1b'nin oransal toleransı sınırlamaya yazıldı.
  - `thresholds_v1_explained.md`: ilgili bölümler, 4 sözlük terimi; "fark ettiklerim" 33 madde (31–33 yeni).
- **Açık karar 23 kapatıldı ve eşik paketi onaya hazır (kullanıcı, 2026-11-24; `thresholds_v1.md` §8 değişiklik 11):**
  - (a) Yeniden hesap yapılan uyarı eşiklerinde iki yöndeki uyuşmayan kayıtlar aynı yöntemle incelenir (§6.2 U.2, U.5).
  - (b) 3.2–3.5 ve T.2–T.5 kayıt düzeyinde düzeltilemez; aşılırsa doğrudan "çekinceli" (T.2–T.5'te tetikleme). Bilinçli tercih olarak yazıldı.
  - (c) Yargıç üslup türünde kalırsa T.6 tetiklemez, "ölçülemedi" diye raporlanır; diğer T'ler çalışır (§3A, §9.3).
  - Üç uygulama yorumu (#2 tekrar, #20 "en iyisi", #24 `referans_sorunu`) kullanıcı tarafından onaylandı.
  - Yeni çalışma kuralı ve "Varsayılan olarak uygulananlar" bölümü eklendi (aşağıda). Bu turda 6 varsayılan uygulandı.
- **`hazir_istemli` kapsamdan çıkarıldı (kullanıcı kararı, 2026-11-24; `thresholds_v1.md` §8 değişiklik 12).** Fine-tuning proje sahibinin talebidir; prompt'la karşılaştırma kapsam dışıdır. `baseline` üslup gelişiminin ve gerileme kontrollerinin taban çizgisidir. Hiçbir eşiğin sayısal değeri değişmedi:
  - `CLAUDE.md` (kullanıcı izniyle): deney tablosundan `hazir_istemli` satırı kaldırıldı; "haklı çıkar" cümlesi değiştirildi. Masaüstündeki üst dizin kopyası (`/home/aipc/Desktop/CLAUDE.md`) değiştirilmedi.
  - §1 birincil çift adaptör vs `baseline`; insan formu adaptör ve `baseline`'ı karşılaştırır. §2 yalnızca `baseline`. 4.1 "≥ `baseline` − 2". Birleşik etiket `baseline` karşılaştırmasında; karar 21a/21b sadeleşti.
  - Holm kaldırıldı: H2 kalktı, H3 birincil oldu; tek ikincil test (5.1) α = 0,05. Galibiyet tablosunda yalnızca α = 0,05 sütunu kaldı.
  - Kritik kontrol 3'e indi (aile düzeyinde yanlış alarm %14,3, ölçüldü).
  - Deney planı §5 (few-shot, üslup prompt'u) "kapsam dışı"; rapor planına kullanıcının sınırlama cümlesi eklendi.
  - Varsayılanlar V7–V10 (kalibrasyon kaynağı ve 06/07 sırası dahil).
  - `thresholds_v1_explained.md`: §9'a "birleşik etiket" ve "yedek yol" alt bölümleri, sözlüğe 2 terim; "fark ettiklerim" 30 madde (3, 4, 6, 21, 23, 26 güncellendi; 28–30 yeni).

### Üretilen dosyalar
| Dosya | Amaç |
|---|---|
| `README.md`, `.gitignore`, `experiments.csv` (yalnızca başlık satırı) | İskelet |
| `prompts/system_prompt_v1.txt` | Tek system prompt (eğitim, değerlendirme, servis) |
| `prompts/response_standard_v1.md` | Üslup, jargon, bilgi yokken ve alan dışında davranış |
| `evaluation/experiment_plan_v1.md` | Ön kayıt taslağı |
| `evaluation/thresholds_v1.md` | Eşik taslağı (onay bekliyor) |
| `evaluation/dev_out_of_scope_v1.jsonl` | 15 soru, `approval: onaylandı (kullanıcı)`; GKD-008 ve GKD-012 düzeltildi; 02'deki çakışma denetimi bekliyor |
| `archive/degerlendirme/lock_manifest_v1.json` | 25 kilitli dosyanın SHA-256 özeti |
| `src/data/build_input_manifest.py` | Girdi özeti ve kilit manifesti betiği (içerik basmaz) |
| `archive/env/2026-11-23_input_sha256_v1.json` | 505 girdi dosyasının özeti |
| `archive/env/2026-11-23_packages.txt`, `archive/env/2026-11-23_hardware.txt` | Ortam kaydı |
| `docs/learning/01_skeleton_and_plan.md` | Öğrenme açıklaması |
| `report/report_plan_v1.md` | Rapor iskeleti ve önceden bilinen sınırlamalar (açık kararlar güncellemesinde eklendi) |
| `inceleme/genel_kontrol_v2_taslak.jsonl`, `inceleme/genel_kontrol_v2_onay.csv` | Saklanan üslup sızıntısı seti taslağı (60) ve onay kuyruğu (karar 6a) |
| `archive/degerlendirme/lock_manifest_v2.json`, `archive/env/2026-11-23_input_sha256_v2.json` | 27 kilitli dosya: v1'deki 25 + ham `01_sss` + v2 taslağı (ilk `b` yorumu) |
| `archive/degerlendirme/lock_manifest_v3.json`, `archive/env/2026-11-23_input_sha256_v3.json` | 27 kilitli dosya; v2'den farkı yalnızca yeniden yazılmış `b` grubuyla taslağın özeti (karar 6c) |
| `archive/degerlendirme/lock_manifest_v4.json`, `archive/env/2026-11-23_input_sha256_v4.json` | 27 kilitli dosya; v3'ten farkı yalnızca GK2-050 düzeltmesiyle taslağın özeti |
| `archive/degerlendirme/lock_manifest_v5.json`, `archive/env/2026-11-23_input_sha256_v5.json` | **Geçerli manifest.** 27 kilitli dosya; v4'ten farkı yalnızca kullanıcı onaylı, GK2-044 düzeltilmiş taslağın özeti |
| `src/data/build_review_csv.py` | JSONL taslağından onay CSV'si üretir; dolu hücreleri kimliğe göre korur (karar 6c) |
| `evaluation/thresholds_v1_explained.md` | Eşiklerin sade açıklaması (bağlayıcı değil): her eşik için arka plan, ne, neden, olmasaydı, katkı, uydurma örnek; düşünme modu ek bölümü; terim sözlüğü; "Açıklarken fark ettiklerim" (22 madde). `thresholds_v1.md`'ye yalnızca en üste atıf satırı eklendi (2026-11-24). Aynı gün eşik kararlarına göre güncellendi; "fark ettiklerim" 27 madde |
| `src/evaluation/threshold_probabilities.py` | Eşik gerekçelerindeki olasılıkları tam hesapla yeniden üretir (veri okumaz) |
| `archive/degerlendirme/threshold_probabilities_v1.json` | Betiğin çıktısı; `thresholds_v1.md` §8'deki "ölçüldü" sayılarının kaynağı |

`.claude/settings.json` ve `kanarya.txt` kullanıcı isteğiyle git'e eklendi. `kanarya.txt` deny kuralı gereği okunmadı. (2026-11-25'te kanarya dosyaları kaldırıldı; erişim testi README "Erişim engeli testi" bölümünde.)

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
  - `thresholds_v1.md` farkı yalnızca en üstteki atıf satırı (+2 satır, git diff).
  - Kilitli 27 dosyanın 27'si `archive/degerlendirme/lock_manifest_v5.json` ile aynı SHA-256 (yalnızca sayı basan kontrol). Girdi değişmedi; yeni manifest üretilmedi.
  - Açıklamadaki p değerleri, kappa ve standart hatalar uydurma sayılar üzerinde formülle hesaplandı; veri kullanılmadı.
  - Paket kaydı: `archive/env/2026-11-24_packages.txt` (temel miniconda ortamı).
- Eşik kararlarının gerekçeleri (2026-11-24, `src/evaluation/threshold_probabilities.py`, tam olasılık hesabı):
  - 17 zorunlu eşikte en az birinin şansla aşılması %58,2 (kullanıcının sayısıyla aynı). §2'nin iki karşılaştırması sayılırsa 21 eşikte %65,9. Yeni hâlde 4 kritik kontrolde %18,5.
  - 4.1, iki eşit modelde yanlış alarm: −1'de %17,5–33,1 (verilen %19–38), −2'de %6,4–23,3 (verilen %6–23, aynı).
  - 4.1, 3 soruluk kötüleşmeyi yakalama: −1'de %66,5–83,9, −2'de %55,7–63,2, −3'te %36,8–44,6.
  - **Fark:** kullanıcı −2'de yakalamayı yaklaşık %68 verdi; hiçbir modelde bu çıkmadı. −2, −1'e göre yakalama gücünden 11–21 pp kaybettiriyor. −3 için verilen %36, "kesin kötüleşme" modelinin alt ucuyla örtüşüyor.
  - Kalibrasyon, %75 uyumda %95 yarı genişlik: 25 çiftte ±17,0 pp, 40 çiftte ±13,4 pp (verilenle aynı). 5 pp, 25 çiftte 1,25, 40 çiftte 2,0 çift. Kappa belirsizliği 40 çiftte yaklaşık ±0,27 (kaba).
  - Açıklama örneklerindeki p değerleri ve kappa aynı betiğin `isaret_p` (yeni adı `sign_test_p_value`) işleviyle hesaplandı.
  - `thresholds_v1.md` git farkında silinen satırlar yalnızca kararlarda adı geçen satırlar: durum satırı, 0.3, 0.5, §1 cümlesi, 2.1, 3.7, 4.1, 4.2, 5.1.
- Açık kararlar 17–20 (2026-11-24):
  - 17'nin gerekçesi: 1 − 0,95³ = %14,3 (ölçüldü, bağımsızlık varsayımıyla); 100 kesin kararda 61–63 galibiyet (önceki betik çıktısı). Kullanıcının sayılarıyla aynı.
  - `thresholds_v1.md` git farkında değişen satırlar: durum satırı, §1 yargıç cümlesi, 2.1, 2.1b, 4.2, 5.1, §8 değişiklik 5 ve açık sorular; eklenenler §8 değişiklik 6–8 ve §9.
  - Kilitli 27 dosyanın 27'si `archive/degerlendirme/lock_manifest_v5.json` ile aynı SHA-256 (yalnızca sayı basan kontrol). Girdi değişmedi.
  - Paket kaydı: `archive/env/2026-11-24_packages.txt` yeniden yazıldı.

**Tahmin / bekleyen iş:**
- Kayıt düzeyinde JSON doğrulaması, kimlik benzersizliği ve çakışma denetimi (02).
- Yargıç VRAM değerleri ve bazı yayın tarihleri (`mistral-small3.2`, `gpt-oss`, `phi4`) bilgime dayanıyor; yargıç kurulumunda doğrulanacak.
- TurkishMMLU seçenek sayısı (02'de dosyadan).
- `sacrebleu` kurulu değil; resmî chrF metrik betiğinden önce sabit sürümle kurulacak.

### Kararlar (kullanıcı, 2026-11-23) — "01: açık kararlar kaydedildi" commit'iyle işlendi
1. **Genel Türkçe verisi** yalnızca gerileme görülürse eğitime girer.
   - Sayısal tetikleyici `thresholds_v1.md` §3A'da: T.1–T.8 (görev başına izin verilen en fazla düşüş ve sızıntı sınırı) ve K.1–K.3 (tetiklenince yapılacaklar). Proje sahibi onayı bekliyor.
   - Eski "her durumda %10–20" kararından neden değişildiği `experiment_plan_v1.md` §8, karar 1'de.
2. **Türkçe değerlendirme ayrımı:** her dosyada %30 geliştirme / %70 saklanan, seed 42; her görevde geliştirme bölümü en az 50 kayıt. Bölme 02'de yapılacak.
3. **Kör insan değerlendirmesi:**
   - 11. aşamada, yalnızca birincil çift için, testten 50 soru, tek değerlendirici (proje sahibi).
   - Form iki bölüm: üslup ve jargon referanssız; bilgi bölümünde referans gösterilir.
   - Model adları gizli, sıra karışık, anahtar ayrı dosyada.
   - Ayrıntı `experiment_plan_v1.md` §6.9'da, eşikler 1.2 ve 2.1b'de, sınırlamalar `report/report_plan_v1.md` §4'te.
4. **Deny kuralları:** kapandı. Commit `f6ad4d0`; ham `05_tuzak_sorular`, `01_sss`, `06_genel_turkce/degerlendirme` ve `kanarya_klasor` için Read deny var (settings.json okunarak doğrulandı; kanarya ölçümünü kullanıcı yaptı). 2026-11-25: kanarya kuralları yerine kalıcı `security_check/**` kuralı geldi.
5. **Ham tuzak araçları:** şimdi kullanılmayacak, karar 11'e kaldı. Birincil tuzak puanı önceden kayıtlı ölçütlerden ve projenin kendi yargıç akışından gelir; hazır betik 11'de en fazla ek kontrol olabilir.

6. **Bölme kuralına uymayan iki dosya** (kullanıcı kararı, 2026-11-23; `experiment_plan_v1.md` §8, karar 6):
   - **6a:** `genel_kontrol_v1`'in tamamı (60) geliştirme bölümü olur. Saklanan karşılığı yeni `genel_kontrol_v2`: 60 kayıt, aynı dağılım. Taslak `inceleme/` altında yazıldı ve `archive/degerlendirme/lock_manifest_v2.json`'a eklendi.
   - **6b:** `turkishmmlu_dev` bölünmez; iki bölümde de aynı 5-shot örnekleri kullanılır.
   - **6c** (kullanıcı v1'i kontrol ettikten sonra): v2'nin `b` grubu yanlış yorumlanmıştı.
     - GK2-036..050 sıfırdan yeniden yazıldı. Yeni tanım: "kurum işlemi veya bilgisi isteyen, gündelik dille sorulmuş, sade ve adım adım anlatım bekleyen sorular". Kategori `kurum_islemi_sade_anlatim`, yeni alan `bilgi_ogeleri`.
     - `b` için sızıntı ölçütü yeniden tanımlandı (`experiment_plan_v1.md` §6.6): kurum ve sistem adları serbest, bürokratik kalıplar yasak. Mevzuat atfı ayrıca sayılır, sızıntı sayılmaz.
     - `b` doğruluğu için `thresholds_v1.md` 3.9 eklendi. 3.7 ve T.7 gruba göre ölçüte bağlandı; gerekçe `thresholds_v1.md` §3 sonunda ve plan karar 6c'de.

### System prompt kararları (kullanıcı, 2026-11-23) — "01: system prompt kararları" commit'iyle işlendi
`system_prompt_v1.txt` yerinde düzeltildi, yeni sürüm açılmadı. Dosya henüz hiçbir eğitim veya değerlendirmede kullanılmamıştı; eski hâl git geçmişinde (`b4ebb4e`). Ayrıntılar `experiment_plan_v1.md` §8'de.
- **Karar 9, sade anlatım:** yeni kural 9 eklendi. Kullanıcı sade, basit, kolay anlaşılır veya adım adım anlatım istediğini belirtirse model doğru ve eksiksiz bilgiyi gündelik dille, bürokratik kalıpsız ve atıfsız verir. Varsayılan üslup resmî kalır. `response_standard_v1.md` §2a. Açık karar 9 kapandı.
  - Kullanıcı incelemesinden sonra ("01: kural 9 tetikleyicisi ve GK2-050"): tetikleyici kelime eşleşmesi değil anlamdır. Kuralın başı şu oldu: "Kullanıcı sade, basit, kolay anlaşılır veya adım adım bir anlatım istediğini belirtirse (ör. "kolayca anlatır mısın", "teknolojiden anlamayan birine anlatacağım")…". Tek başına "kısaca" sade anlatım isteği sayılmaz.
  - **Ton istekleriyle genişleme** ("01: kural 9 ton istekleriyle genişletildi"): kullanıcı v1 `b` sorularında ton istekleri de gördü ("samimi", "sohbet eder gibi", "mesaj atar gibi", "eğlenceli"). Kural 9 artık "samimi, gündelik veya eğlenceli bir tonda" anlatım isteğini de kapsıyor. Örnekler "sohbet eder gibi anlat" ve "esprili bir dille yaz" eklendi. "Kısaca" istisnası kuralın metnine yazıldı. `system_prompt_v1.txt` yerinde düzeltildi; `response_standard_v1.md` §2a (ton isteği örneği dahil) ve plan karar 9 güncellendi.
  - Ölçüldü: v2'nin 15 `b` sorusunun 15'i sadelik isteği içeriyor, ton isteği içeren yok (kendi taslağım üzerinde sınıflama). v2 değiştirilmedi; dağılım farkı rapor planı §4.4'te sınırlama.
- **Karar 10, kurum ağzı:** kural 2'ye eklendi. Model kurumları adıyla anar, "Kurumumuz" / "Bakanlığımız" demez. `response_standard_v1.md` §2. 03 notu aşağıda. Kurum verisi turunda bu kural tek kurum için yeniden değerlendirilecek.
- **Karar 11, tutar ile süre/oran ayrımı:** kural 4 değiştirildi. Kanunda belirlenmiş süre, gün sayısı ve oranlar verilir. Dönemsel TL tutarlarının rakamı verilmez; hesaplama yolu söylenir ve resmî kaynaktan kontrol önerilir. `response_standard_v1.md` §4 uyduruldu.
  - 03'teki eskimiş tutar nötrleştirme kuralı plan karar 11'de önceden kayda alındı ve **kullanıcı tarafından onaylandı**.
  - §6.3'teki puanlama kuralı **kullanıcı tarafından kabul edildi**: kural 4'e uygun biçimde verilmeyen dönemsel TL tutarı eksik sayılmaz. Kesin onayı eşiklerle birlikte proje sahibi verecek.

### Açık kararlar (kullanıcı)
7. **`genel_kontrol_v2`:** onay kapandı ("01: genel_kontrol_v2 onaylandı"); taşıma ve deny kuralı açık.
   - Ölçüldü: 60/60 kayıt "evet". `b` bilgi öğeleri: 14 "evet", GK2-044 "düzelt". CSV'deki tek içerik farkı GK2-044'ün 4. öğesiydi.
   - GK2-044'ün 4. öğesi kullanıcının metniyle aynen taslağa işlendi. Gerekçe: 1475 md. 14'e göre kıdem tazminatını yalnızca 4857 md. 25/II kaldırır; işçinin haklı nedenle feshi (md. 24) de tazminat doğurur.
   - Bilgi öğesi kontrolünün kapsamı (ikincil kaynaklar, birincil metinle tek tek karşılaştırma yok) rapor planı §4.4'e sınırlama olarak yazıldı.
   - Taslak yeniden üretilen CSV ile bayt bayt aynı (ölçüldü). Onaylı taslak `archive/degerlendirme/lock_manifest_v5.json` ile kilitlendi.
   - **Açık:** taşıma 02'deki çakışma denetiminden sonra yapılacak (kullanıcı kararı). Taşımadan sonra önerilen Read deny kuralı eklenmeli: `evaluation/held_out/**` (dosya İngilizce adıyla `general_control_v2.jsonl` olarak taşınacak; yukarıdaki "02'nin yapılacakları").
- ~~9. `b` grubu ile `system_prompt_v1` gerilimi~~: karar 9 ile kapandı (aşağıda).
- ~~`genel_kontrol_v2` sade anlatım isteği denetimi~~ kapandı.
  - GK2-036 kullanıcı kararıyla değişmedi; "kolayca anlatır mısın, bilgisayardan pek anlamaz" açık bir istektir.
  - GK2-050 "Kısaca ve sade bir dille anlatır mısın?" olarak düzeltildi.
  - 15 `b` sorusunun hepsi istek içeriyor. CSV ve `archive/degerlendirme/lock_manifest_v4.json` yeniden üretildi.
  - v1 `b` sorularında aynı denetimi yalnızca kullanıcı yapabilir.
- ~~12. Ton isteklerinde ünlem/emoji~~ kapandı ("01: karar 12-13 kapatıldı"): emoji her durumda yasak; ünlem yalnızca kural 9'daki isteklerde ölçülü olarak serbest. Kural 9'un sonuna "Bu durumda ünlem ölçülü kullanılabilir; emoji hiçbir durumda kullanılmaz." eklendi. Kural 2'deki yasak resmî üslup için geçerli (`response_standard_v1.md` §2a). Cümlenin yeri ve kapsamı karar 14 ile düzeltildi.
- ~~13. "kolayca anlatır mısın" örneği~~ kapandı: örnek "anlaşılır bir dille anlatır mısın" ile değiştirildi. Ölçüldü: yeni ifade ve çekirdeği "anlaşılır bir dille" v1'de 0/60, v2'de 0/60. v1 yalnızca sayı basan `src/data/count_phrase_matches.py` ile denetlendi. Betiğin doğruluğu v2'de bilinen iki eşleşmeyle sınandı (1/1).
- ~~14. Kural 9'daki "Bu durumda" göndermesi~~ kapandı ("01: karar 14 kapatıldı"): kullanıcı iki seçeneği birlikte seçti. Ünlem/emoji cümlesi kuralın sonundan kaldırıldı. Yerine "kanun ve madde atfı gerekmez." ifadesinin hemen ardına "Ton isteği varsa ünlem ölçülü kullanılabilir; emoji hiçbir durumda kullanılmaz." eklendi. Kural 9 "Böyle bir istek yoksa yukarıdaki resmî üslubu koru." cümlesiyle bitiyor. Sonuç: ünlem yalnızca ton isteğinde serbest; sadelik isteğinde ve resmî üslupta yok. Standart §2a, plan karar 9/12/14 ve öğrenme dosyası güncellendi.
- ~~Geliştirme kapsam dışı seti kullanıcı onayı~~ kapandı ("01: geliştirme kapsam dışı seti onaylandı").
  - GKD-012'nin kabul ölçütü "Bir yıl şartı belirtilmiş; iznin ilk ay içinde kullanılabileceği söylenmemiş." oldu. Gerekçe: doğru bir cevap "bir yılı doldurduktan sonra kullanabilirsiniz" diyebilir; eski ölçüt bu cevabı haksız yere başarısız sayardı.
  - GKD-008'in beklenen davranışına "Asgari ücretin Asgari Ücret Tespit Komisyonu tarafından belirlendiğini söyleyebilir." eklendi.
  - Diğer 13 kayıt olduğu gibi onaylandı. 15 kaydın hepsinde `onay: "onaylandı (kullanıcı)"`. Ölçüldü: yalnızca bu üç alan değişti, başka alan değişmedi.
  - Set kilit manifestinde değil (geliştirme seti); yeni manifest üretilmedi. 02'deki çakışma denetiminden geçecek.
8. **Proje sahibi onayları:** `thresholds_v1.md` (bütün satırlar, §3A ve yeni 3.9 dahil), `experiment_plan_v1.md`, `report/report_plan_v1.md`, `response_standard_v1.md`, `system_prompt_v1.txt`, `dev_out_of_scope_v1.jsonl` (15 soru). Kullanıcı `response_standard_v1.md` ve `system_prompt_v1.txt` için kararlarını verdi (karar 9–14). `dev_out_of_scope_v1.jsonl` kullanıcı tarafından onaylandı (aşağıda); proje sahibi onayı yine bekliyor.
15. **Düşünme modu yan deneyi** (açık, karar 06'da verilecek): `baseline` model doğrulama setinde düşünme açık ve kapalı çalıştırılıp bilgi doğruluğu (bilgi puanı, kritik hata) ve süre karşılaştırılsın mı? Ana planda yok, hiçbir eşiği etkilemez. Yapılırsa 0.1'i bilerek ihlal ettiği için ayrı bir deney kimliğiyle yürütülmeli. Gerekçe: düşünme kapalılığının çok adımlı sorulardaki (ör. kıdem + ihbar birlikte) bedeli ölçülmedi. Ayrıntı `thresholds_v1_explained.md`, 0.1 ek bölümü.
16. **Eşik açıklamasında listelenen zayıf noktalar** (`thresholds_v1_explained.md` §12, 33 madde). Gruplama 2026-11-24'te yapıldı:
    - **Proje sahibi onayından önce (10): hepsi kapandı** (1, 2, 6, 7, 8, 9, 12, 15, 20, 24; `thresholds_v1.md` §8 değişiklik 10).
    - **İlgili aşamada (5):** 13, 14, 17, 22, 25. Aşağıda "Sonraki aşamanın ihtiyaç duyacağı bilgiler"de aşamalarına not olarak yazıldı.
    - **Yalnızca not (15):** 3, 4, 5, 10, 11, 16, 18, 19, 21, 23, 26, 27, 28, 29, 30.
    - **Yeni (31–33):** açık karar 23'e bağlı.
17. **Holm ailesi** (**kapandı**, kullanıcı kararı 2026-11-24): seçenek A, m = 3. `thresholds_v1.md` 5.1 ve §8 değişiklik 5; `experiment_plan_v1.md` §3.
18. **2.1b ile kritik 2.1** (**kapandı**, kullanıcı kararı 2026-11-24): insan kararı kayıt etiketini değiştirir, eşik sonucunu değil. `thresholds_v1.md` 2.1b, §8 değişiklik 6, §9.1; `experiment_plan_v1.md` §6.9 (yeni "kritik hata var/yok" alanı).
19. **Yargıç kalırsa kritik 2.1 ve 4.2** (**kapandı**, kullanıcı kararı 2026-11-24): `thresholds_v1.md` §1, §8 değişiklik 7, §9.2; `experiment_plan_v1.md` §6.4 ve §6.8 madde 5; `report_plan_v1.md` §4.4.
20. **Kalibrasyon soruları ve prompt ayarı** (**kapandı**, kullanıcı kararı 2026-11-24): çıkarılmaz, 100 soru prompt ayarında. `experiment_plan_v1.md` §6.8 madde 6; `report_plan_v1.md` §4.4.
21. **Birleşik etiket ve yedek yolun `baseline` ve ikincil iddialardaki uygulaması** (**kapandı**, kullanıcı kararı 2026-11-24): (a) iki taraf yargıç + betik; (b) yedekte betik kısmı + "güvenilirliği düşük"; (c) yedekte ikincil iddia yok; (d) kalibrasyon prompt türü başına, yedek yol yalnızca kalınan türe. `thresholds_v1.md` §8 değişiklik 9, §9.1–§9.3; `experiment_plan_v1.md` §6.8 madde 3 ve 5; `report_plan_v1.md` §4.4.
22. **Aya karşılaştırması yargıç kalırsa** (**kapandı**, kullanıcı kararı 2026-11-24): üslup+jargon türüne bağlandı. Tek yargıç kuralı eklenmedi. `thresholds_v1.md` §9.3; `experiment_plan_v1.md` §6.5 ve §6.8 madde 4.
23. **Uyarı incelemesinin yeniden hesabı** (**kapandı**, kullanıcı kararı 2026-11-24): (a) iki yönlü inceleme; (b) chrF ve perplexity düzeltilemez, bilinçli tercih; (c) yargıç üslupta kalırsa T.6 "ölçülemedi". Uygulama yorumları onaylandı. `thresholds_v1.md` §3A, §6.2, §8 değişiklik 11, §9.3.

Açık karar kalmadı. 2026-11-26'dan itibaren yeni kararlar listeye yazılmaz; sohbette doğrudan sorulur (CLAUDE.md "Karar ve onay isteme").

### Çalışma kuralı: eşik paketindeki yeni belirsizlikler (kullanıcı, 2026-11-24; **2026-11-26'da kaldırıldı**)
- Eski kural "kendi çözümünü uygula ve listeye yaz" idi. Yerine CLAUDE.md "Karar ve onay isteme" kuralı geldi: karar gerektiğinde iş durur ve soru sohbette doğrudan sorulur.
- Bu kuralla daha önce uygulanmış maddeler (aşağıdaki V1–V6) sohbette tek tek proje sahibinin onayına sunuldu; cevap gelene kadar "onay bekliyor".

### Çalışma kuralı: GitHub'a gönderim (kullanıcı, 2026-11-24)
- Uzak depo: `origin` = https://github.com/cerensahindevelop/kurumsal_qa_fine-tune (`main`, ilk gönderim `38dcb32`).
- Aşama sonlarında yalnızca yerel commit yapılır. `git push` her seferinde **kullanıcıya sorulur** ve yalnızca onay gelirse yapılır.

### Varsayılan olarak uygulananlar (V1–V6 proje sahibince onaylandı, 2026-11-26; V7–V10 sorulmadı)
Satır numaraları 2026-11-24 commit'indeki `evaluation/thresholds_v1.md` içindir. Hiçbiri bir eşik değerini veya kritik/uyarı ayrımını değiştirmiyor.

| # | Sorun (tek cümle) | Uygulanan çözüm | Dosya / satır |
|---|---|---|---|
| V1 (**onaylandı**, 2026-11-26, A) | 3.1 (TurkishMMLU doğruluğu) "ortalama farkı" türündeydi; doğru/yanlış bir sayım olduğu için "iki yöndeki uyuşmayan kayıt" orada tanımsızdı. | 3.1 "sayım farkı" türüne alındı: uyuşmayan kayıt = iki sistemden yalnızca birinin doğru bildiği soru, iki yönde de. | `thresholds_v1.md`:174 (§6.2 U.2) |
| V2 (**onaylandı**, 2026-11-26, A) | 3.8 mutlak bir orandır, karşılaştırılan sistem yoktur; "iki yön" tanımsızdı ve yalnızca olumsuz kayıtlara bakmak düzeltmeyi tek yönlü bırakıyordu. | Harf çıkarılamayan bütün kayıtlara ek olarak, harf çıkarılan kayıtlardan seed 42 ile 20 rastgele kayıt incelenir (betiğin cevapta olmayan harfi çıkarması). | `thresholds_v1.md`:175 |
| V3 (**onaylandı**, 2026-11-26, A) | İkili karşılaştırmada (2.2, 3.6) "uyuşmayan kayıt" tanımsızdı. | Yargıcın iki sırada tutarlı karar verdiği bütün kayıtlar (adaptörün kayıpları ve kazançları) incelenir; beraberlikler iki yönde de incelenmez. | `thresholds_v1.md`:176 |
| V4 (**onaylandı**, 2026-11-26, A) | Ortalama farkı eşiklerinde (2.3, 3.9 ortalama) yalnızca "en olumsuz 20" vardı. | En olumsuz 20 + en olumlu 20 + rastgele 10. | `thresholds_v1.md`:177 |
| V5 (**onaylandı**, 2026-11-26, A) | "En fazla 40 kayıt" sınırı tek yön için yazılmıştı; iki yönde tek sınır bir yönü kırpabilirdi. Ayrıca yön görünürse değerlendirici yanlı olabilirdi. | Her yönde en fazla 40 kayıt; aynı seçim kuralı ve etiket şeması; CSV'de yön gösterilmez, kayıtlar seed 42 ile karışık sıralanır. | `thresholds_v1.md`:180 |
| V6 (**onaylandı**, 2026-11-26, A) | Uyarı incelemesindeki düzeltmelerin kritik eşiklere taşınıp taşınmadığı yazılı değildi (2.4, 2.1'in alt kümesi); taşınırsa bir uyarı incelemesi kritik sonucu dolaylı olarak kaldırabilirdi. | Taşınmaz: kritik eşikler (2.1, 3.7, 4.2) özgün etiketlerle, 2.1'de §9.1'deki birleşik etiketlerle hesaplanır. Kritik/uyarı ayrımını korur, değiştirmez. | `thresholds_v1.md`:201 (§6.2 U.5) |
| V7 | `hazir_istemli` çıkınca yargıç kalibrasyonunun çift kaynağı (`baseline` vs `hazir_istemli`) ortadan kalktı. | Kaynak: `baseline` ile ilk `faq_adapter` koşusunun (`faq_adapter_v1`, son checkpoint) doğrulama cevapları; 40 soru seed 42 ile kaynağa göre katmanlı. **Sıraya etkisi:** 06'da yalnızca `baseline`'ın doğrulama cevapları üretilir ve otomatik metrikler hesaplanır; yargıçla puanlama yapılamaz. Kalibrasyon ve yargıç seçimi 07'de, ilk adaptörün doğrulama cevaplarından sonra yapılır. Yargıca dayanan bütün doğrulama puanlamaları (checkpoint/tarif seçimi, `faq_synthetic_adapter`, K.2) kalibrasyondan sonra gelir. 06 ve 07'nin içeriği depoda tanımlı değil; bu sıra, aşamaların senin numaralandırmana göre bir tahminidir. | `thresholds_v1.md`:28 (0.3); `experiment_plan_v1.md` §2 madde 2, §6.8 madde 1 |
| V8 | 4.3'teki "aday ayarlar (prompt, checkpoint)" ifadesinde prompt artık aday değil. | "(checkpoint, tarif)" olarak düzeltildi. | `thresholds_v1.md`:140; `thresholds_v1_explained.md` 4.3 |
| V9 | Karar 20'nin konusu olan prompt ayarı kalktı; ama kalibrasyonun 40 sorusu artık adaptör seçiminde aynı iyimserlik sorununu taşıyor. | Karar 20'nin ilkesi adaptör ayar/tarif seçimine taşındı: kalibrasyon soruları seçimden çıkarılmaz. Rapor sınırlaması buna göre yeniden yazıldı; ayrıca yargıcın yalnızca `faq_adapter` üslubuyla sınandığı eklendi. | `experiment_plan_v1.md` §6.8 madde 6; `report_plan_v1.md` §4.4 |
| V10 | `genel_kontrol_v2` sınırlaması artık var olmayan "prompt geliştirme"den söz ediyordu. | "System prompt ve seçilen ayarlar" olarak düzeltildi; risk aynı kaldı. | `report_plan_v1.md` §4.4 (`genel_kontrol_v2` maddesi) |

### Onaya hazır dosyalar (proje sahibi onayı bekliyor)
- **Onaylanacaklar:** `evaluation/thresholds_v1.md`, `evaluation/experiment_plan_v1.md`, `report/report_plan_v1.md`, `prompts/response_standard_v1.md`, `prompts/system_prompt_v1.txt`, `evaluation/dev_out_of_scope_v1.jsonl` (15 soru).
- **Destekleyici, bağlayıcı değil:** `evaluation/thresholds_v1_explained.md`, `src/evaluation/threshold_probabilities.py`, `evaluation/threshold_probabilities.json` (2026-11-26'da arşivdeki v1'in yerine üretildi; sayılar aynı).
- Her dosyanın son commit'i `git log -1 --follow --format=%h -- <dosya>` ile görülür (`--follow`, 2026-11-25 ad değişikliğinden önceki geçmişi de izler). Onay, eşik dosyasının sonundaki "Proje sahibi onayı (genel)" satırına ve "Onay (proje sahibi)" sütunundaki "bekliyor" hücrelerine ayrı bir commit'le yazılır.

### Sonraki aşamanın ihtiyaç duyacağı bilgiler
- Kilitli desenler `src/data/build_input_manifest.py` içindeki `DEFAULT_LOCKED_PATTERNS` listesinde. 02 ve sonrası bu listeye uymalı.
  - `01_sss/*` deseni listeye eklendi. Yeni `--extra-locked` seçeneği proje içindeki tek dosyaları kilitler. Geçerli manifest: `evaluation/lock_manifest.json` (sürüm 6).
- **02'de Türkçe değerlendirme bölmesi:**
  - Dosya başına %30 / %70, seed 42, geliştirmede ≥ 50 kayıt.
  - Alt grubu olan dosyalarda (TurkishMMLU ders, `genel_kontrol` soru türü) katmanlı.
  - Betik yalnızca kimlik, sayı ve SHA-256 yazar.
  - Beklenen boyutlar `experiment_plan_v1.md` §6.5'te.
  - `genel_kontrol_v1` ve `turkishmmlu_dev` bölünmez (karar 6). `genel_kontrol_v2` saklanan bölümdür.
- 02'deki çakışma denetimine `inceleme/genel_kontrol_v2_taslak.jsonl` (onaylı hâli) de girer. Karşılaştırılacak setler: eğitim adayları, genel Türkçe havuzu, `genel_kontrol_v1`, geliştirme kapsam dışı seti, doğrulama, test ve tuzak.
- v2 onaylandı ama henüz taşınmadı. 02'deki çakışma denetiminden sonra `evaluation/held_out/general_control_v2.jsonl` yoluna taşınır (İngilizce ad, kullanıcı kararı 2026-11-25), `evaluation/lock_manifest.json` güncellenir (sürüm 6 → 7) ve hiçbir model çalışmadan önce commit edilir. Denetimde değişiklik gerekirse yeniden kullanıcı onayı alınır.
- v2'nin `b` soruları SSS konularına yakın (işsizlik ödeneği, yıllık izin, ihbar, süt izni vb.). 02'deki çakışma denetiminde test ve tuzakla yakın eşleşme çıkabilir; çıkarsa yalnızca kimlikle CSV'ye yazılır.
- **03 için önceden kayıtlı veri dönüşümleri** (`experiment_plan_v1.md` karar 10 ve 11). İkisi de betikle yapılır, değişen kimlikleri yazar ve belirsiz kayıtları `review/` kuyruğuna gönderir. Kilitli doğrulama ve test referanslarına dokunulmaz.
  1. **Kurum ağzı:** eğitim cevaplarındaki "Kurumumuz", "Bakanlığımız" ve çekimli biçimleri `kaynak` alanına göre kurum adıyla değiştirilir.
  2. **Eskimiş tutar** (kullanıcı onaylı): dönemsel TL tutarları kaldırılır, yerine hesaplama yolu ve kontrol önerisi yazılır. Kanunda belirlenmiş süre, gün ve oranlar korunur. Tutarın dönemsel mi yoksa kanunda sabit mi olduğu belirsizse kayıt inceleme kuyruğuna gider.
- 02'deki toplu sayımlarda doğrulama ve test referanslarında "Kurumumuz/Bakanlığımız" ve TL tutarı içeren kayıtların **yalnızca sayısı** çıkarılmalı; içerik basılmamalı. Bu sayılar rapor sınırlaması için gerekiyor.
- Sızıntı puanlama betiği işaret listesini kaydın `grup` alanına göre seçmeli (`a` / `b`), dosyadaki `yasak_kalip` alanını kullanmamalı (§6.6).
- 11'deki insan formu için 50 test sorusu, cevaplar üretilmeden önce kimlikle seçilir (seed 42, kaynağa göre katmanlı). Bu seçim 11'in ilk adımıdır, 02'de yapılmaz.
- Kilitli setler yalnızca toplu sayı, kimlik ve SHA-256 yazan betiklerle açılır. Çakışma denetiminde test ve tuzak içeren çiftler yalnızca kimlikle `review/` CSV'sine yazılır.
- `dev_out_of_scope_v1.jsonl` 02'deki çakışma denetimine dahil edilmeli.
- Few-shot havuzu, üslup prompt'u ve prompt ayarı **kapsam dışı** (2026-11-24, `hazir_istemli` çıkarıldı; `experiment_plan_v1.md` §5). Bütün sistemler yalnızca `system_prompt_v1` ile çalışır.
- Yargıç adayları: `gemma4:12b` ve `gemma4:26b`. Kalibrasyon ancak eşik onayından ve doğrulama cevapları üretildikten sonra yapılır. Seçim kuralı `thresholds_v1.md` 0.5'te.
- Üretim ayarı önerisi: greedy, `max_new_tokens=512`, `seed=42`, düşünme kapalı. Yükleme: HF + bitsandbytes NF4.
- Proje Python ortamı henüz kurulmadı. `pip freeze` şimdilik temel miniconda ortamından (Python 3.13.13).
- Qwen3.8 için LLaMA-Factory şablon adı (düşünme kapalı) doğrulanmadı (bekleyen iş).

- **Eşik kararlarından doğan işler (2026-11-24):**
  - Uyarı incelemesi için kayıt seçme betiği `src/evaluation/warning_review_queue.py` yazılacak (bekleyen iş): 11'den önce, 4.3 kullanılacaksa doğrulama aşamasından önce. Kurallar `thresholds_v1.md` §6.2'de: seed 42, eşik başına en fazla 40 kayıt, yalnızca kimlik basar, çıktısı `review/warning_<experiment_id>_<threshold>.csv`.
  - Bütün puanlama ve rapor betikleri ikili karşılaştırmaları §7 biçiminde yazmalı: kazanma / beraberlik / kayıp, beraberliğin eşit ve sıra tutarsız ayrımı, p değeri.
  - Yargıç kalibrasyon seti doğrulamadan 40 çift olacak: `baseline` ile ilk `faq_adapter` koşusunun (`faq_adapter_v1`, son checkpoint) doğrulama cevapları (V7). Kalibrasyon soruları adaptör ayar ve tarif seçiminden çıkarılmaz (V9).
- **Açık kararlar 17–20'den doğan işler (2026-11-24):**
  - İnsan formu betiği (11) bilgi bölümüne "Kritik hata var mı? Var / Yok" alanını koymalı; §6.3 tanımı formda yazılı olmalı.
  - 2.1 puanlama betiği etiket kaynağını kayıt başına yazmalı (`insan` / `yargic_betik`) ve §9.1'e göre birleştirmeli. §2 yalnızca `baseline` ile karşılaştırılır; 50 insan sorusunda iki tarafın (adaptör, `baseline`) etiketi de insandan gelir.
  - Kalibrasyon betiği uyumu, kappayı ve sıra tutarlılığını her aday × prompt türü (üslup+jargon, bilgi) için ayrı yazmalı ve seçimi tür başına yapmalı (§9.3). 0.5'te yalnızca uyum karşılaştırılır. Aya, üslup türünün yargıcıyla puanlanır.
- **Proje sahibi onayı öncesi netleştirmelerden doğan işler (2026-11-24):**
  - Bütün eşik betikleri sınır kuralını uygulamalı: ham değerle karşılaştırma, eşiğe eşit değer geçer. "Kaybetme − kazanma" paydası bütün kayıtlar.
  - Uyarı kuyruğu betiği (`src/evaluation/warning_review_queue.py`) `neden` (`gercek_hata` / `olcum_yanilgisi` / `belirsiz`) ve `duzeltilmis_etiket` sütunlarını üretmeli ve eşiği yeniden hesaplayan bir adım içermeli. Kayıt seçimi iki yönlü (yön başına en fazla 40, yön CSV'de gizli, karışık sıra; V1–V5). 3.2–3.5 için kuyruk üretilmez. Düzeltmeler kritik eşik hesabına girmez (V6).
  - Rapor betiği birincil sonucu üç değerle yazmalı: geçti / çekinceli / kaldı.
  - Doğrulama seçim betiği 4.3'ü seçim kısıtı olarak uygulamalı; K.2'nin pay seçimi kuralını içermeli.
- **"Fark ettiklerim" 2. grup: ilgili aşamada çözülecekler (düzeltilmedi):**
  - Madde 22 (0.2'nin birimi: sistem başına mı, set başına mı, Türkçe değerlendirme görevlerinde de geçerli mi): üretim betiği yazılırken, hiçbir puanlamadan önce sabitlenecek.
  - Madde 17 (2.3'te sayı içermeyen referanslar): sayı metriği betiği yazılırken tanımlanacak. 02'de doğrulama ve test referanslarında sayı içermeyenlerin yalnızca sayısı çıkarılabilir.
  - Madde 14 (2.4, 2.1'in alt kümesi): 2.1/2.4 puanlama betiği ve rapor bunu açıkça yazacak. Yedek yolda 2.4 kullanıldığı için önemli.
  - Madde 25 (uyarı incelemesi kör değil): uyarı kuyruğu betiği (11'den önce) körleme ekleyebilir. §6.2'nin metnine dokunacağı için `thresholds_v2` gerektirebilir.
  - Madde 13 (K.3 sonrası bilinen sorunla teste girme): tetikleyici çalışırsa rapor taslağında bu senaryo önceden hazırlanacak.
  - Yedek yol gerekirse (kalibrasyonda iki aday da kalırsa) 11'de tuzak için ayrı kör insan formu gerekir: `review/trap_human_form_v1.csv`, ayrı anahtar dosyası, 56 cevap. Kalibrasyon sonucu doğrulama aşamasında bilineceği için ihtiyaç 11'den önce belli olur.

### Değişen çalıştırılabilir kod veya komut yolları
- Yeni: `python -m src.data.build_input_manifest --input ... --output ... --lock-manifest-output ...` (README "01" bölümü).
- Değişti: `src/data/build_input_manifest.py` artık `--extra-locked` seçeneğini kabul ediyor ve `01_sss/*` desenini varsayılan olarak kilitli sayıyor.
- Yeni: `python -m src.data.count_phrase_matches --input <jsonl ...> --phrase "<ifade>"`. Bir ifadenin kaç kayıtta geçtiğini sayar, içerik ve kimlik basmaz; kilitli setlerde de kullanılabilir (karar 13).
- Yeni: `python -m src.data.build_review_csv --input inceleme/genel_kontrol_v2_taslak.jsonl --output inceleme/genel_kontrol_v2_onay.csv` (karar 6c).
- Değişti: girdi özeti komutunun çıktıları artık `archive/env/<tarih>_input_sha256_v5.json` ve `archive/degerlendirme/lock_manifest_v5.json`.
- Değişti: `src/data/build_review_csv.py` sonunda onay dağılımını yazıyor. "düzelt"/"duzelt", "hayır"/"hayir" ve büyük/küçük harf aynı sayılıyor (`normalize_label`, eski adı `normal_onay`); hücredeki yazım değişmiyor. evet/hayir/duzelt dışındaki değerler kimlikle listeleniyor.
- Düzeltildi: `src/data/build_review_csv.py` artık betiğin kendi "-" yer tutucusunu "dolu satır" saymıyor. Önceki sürüm 45 yanlış "korunan" satır bildiriyordu; içerik farkı yoktu.
- Yeni: `python -m src.evaluation.threshold_probabilities --output archive/degerlendirme/threshold_probabilities_v1.json [--degradation 3]`. Eşik gerekçelerindeki olasılıkları hesaplar, veri okumaz (README 01, adım 1c).
- Değişti (2026-11-24): aynı betik artık `isaret_testi_galibiyet_tablosu_n_1_100` çıktısını da yazıyor (1.1 ve 5.1 için 1–100 kesin kararda gereken en az galibiyet). `gereken_galibiyet` (yeni adı `minimum_wins_required`) hiçbir k yetmediğinde `None` döndürüyor. Önceki çıktı anahtarları birebir aynı (ölçüldü).
