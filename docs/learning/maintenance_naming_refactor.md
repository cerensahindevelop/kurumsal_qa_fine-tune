# Bakım: isimlendirme refactor'ı (2026-11-25)

Bu bakım bir aşama değildir. Amaç, projeyi ilk kez açan bir Python/ML geliştiricisinin dosya, fonksiyon ve alan
adlarından ne işe yaradıklarını anlayabilmesidir. Davranış değişmedi; yalnızca adlar değişti ve eski adlar
okunmaya devam ediyor. Tam eşleme tablosu `PROJECT_STATUS.md` → "Bakım: isimlendirme refactor'ı" bölümünde.

## Adlandırma kuralları

- Python modülü, fonksiyon, değişken ve projeye ait veri anahtarı: `snake_case` (`build_review_csv`, `expected_behavior`).
- Sabit: `UPPER_SNAKE_CASE` (`DEFAULT_LOCKED_PATTERNS`).
- CLI seçeneği: `kebab-case` (`--lock-manifest-output`).
- Ad, kodun gerçek işlevini söyler: `build_*` bir dosya üretir, `count_*` sayar, `compute_*` bir değer hesaplar.
- Terim ayrımları: `prompt` modelin aldığı girdidir, `system_prompt` sistem rolündeki prompt'tur. `baseline`
  değerlendirmedeki karşılaştırma sistemidir; `base_model` adaptörün bağlandığı temel modeldir.

## `src/data/build_review_csv.py`: dosya adı, CLI seçeneği ve JSONL alanı nasıl bağlanır

**Yol ve girdi:** `--input` bir taslak JSONL (her satır bir kayıt), `--output` insan onay CSV'si.

**Blok 1: dosya adı ve komut.**
- Aldığı veri: kabuktaki komut, ör. `python -m src.data.build_review_csv --input taslak.jsonl --output review/x.csv`.
- Dönüşüm: `-m src.data.build_review_csv` ifadesi `src/data/build_review_csv.py` dosyasını modül olarak çalıştırır.
  Noktalar klasör ayırıcıdır; `src/` ve `src/data/` altındaki boş `__init__.py` dosyaları bu klasörleri paket yapar.
- Neden: dosya adı komutun kendisidir. Ad değişince README komutu da değişir; bu yüzden ikisi birlikte güncellendi.
- Sonraki bloğa: çalışan `main()` fonksiyonu.

**Blok 2: CLI seçeneği → değişken.**
- Aldığı veri: komuttaki `--input` ve `--output` seçenekleri.
- Dönüşüm: `parser.add_argument("--input", ...)` seçeneği tanımlar. Python, seçenek adındaki tireleri atıp
  değeri `arguments.input` adıyla verir (`--lock-manifest-output` → `arguments.lock_manifest_output`).
- Neden: her seçeneğin tek bir İngilizce adı var. Eski Türkçe adlar (`--girdi`, `--cikti`) kafa karıştırmasın diye
  2026-11-25'te kaldırıldı; eski adla yazılan komut "unrecognized arguments" hatası verir.
- Sonraki bloğa: `arguments.input` (taslak yolu) ve `arguments.output` (CSV yolu).

**Blok 3: JSONL alanı ve eski ad.**
- Aldığı veri: her kayıt, ör. `{"id": "GK2-001", "grup": "a", "kategori": "...", "prompt": "..."}`.
- Dönüşüm: `get_field(record, "group")` önce `group` anahtarına bakar, yoksa `LEGACY_INPUT_FIELDS` sözlüğündeki
  eski adı (`grup`) okur. `prompt` ve `id` iki sürümde de aynıdır.
- Neden: kilitli `genel_kontrol_v2` taslağı Türkçe alanlarla yazıldı ve değiştirilemez. Okuyan kod iki adı da tanırsa
  hem eski hem yeni dosya çalışır.
- Sonraki bloğa: yeni adlı satır (`group`, `category`, `knowledge_items`).

**Blok 4: CSV başlığı ve insan onaylarının taşınması.**
- Aldığı veri: var olan CSV (eski veya yeni başlıklı).
- Dönüşüm: `read_existing_reviews` her başlığı `LEGACY_CSV_COLUMNS` ile yeni ada çevirir
  (`onay (evet/hayir/duzelt)` → `approval (evet/hayir/duzelt)`, `not` → `notes`) ve satırları `id`'ye göre tutar.
  Yeni CSV yazılırken her kayıt kendi `id`'sindeki eski hücreleri alır. Hücre değeri (`Düzelt`, `evet`) değiştirilmez;
  yalnızca sayım sırasında `normalize_label` ile sadeleştirilir.
- Neden: insan emeği kaybolmasın. Eşleme sıraya göre değil kimliğe göre yapıldığı için taslağa kayıt eklense de onaylar doğru satıra gider.
- Çıktı: yeni başlıklı CSV ve ekranda onay dağılımı.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):**
- Taslak satırı: `{"id": "GK-2", "grup": "b", "kategori": "k2", "prompt": "Soru?", "bilgi_ogeleri": ["öğe 1", "öğe 2"]}`
- Eski CSV satırı: `id=GK-2`, `onay (evet/hayir/duzelt)=evet`, `bilgi_ogeleri_dogru_mu (…)=duzelt `, `not=ikinci not`
- Yeni CSV satırı: `id=GK-2`, `group=b`, `knowledge_items=öğe 1 | öğe 2`, `approval (…)=evet`,
  `knowledge_items_correct (…)=duzelt ` (sondaki boşluk korunur), `notes=ikinci not`

**Gerçek çalışma (ölçüldü, sentetik dosyalarla):** eski ve yeni betik aynı taslak ve aynı eski CSV'den başlık
eşlemesiyle hücre hücre aynı CSV'yi üretti; onay dağılımı aynıydı. Yeni CSV'de ikinci çalıştırma bayt bayt aynıydı.

**Üç cümlelik özet:** Komuttaki modül adı dosya yolunu, CLI seçeneği `arguments` değişkenini, `get_field` de JSONL anahtarını
belirler. JSONL alanları ve CSV başlıkları eski Türkçe adları da tanır; CLI seçeneklerinin ise yalnızca İngilizce adı vardır. Onaylar satır sırasına göre değil kayıt kimliğine göre taşınır. Bu yüzden ad
değişikliği hem eski dosyaları hem insan emeğini korur.

**Kontrol sorusu:** Eski CSV başlıklarını yeni adlara çevirmeseydik ne olurdu?
*Cevap:* `old.get("approval (evet/hayir/duzelt)")` boş dönerdi, çünkü eski dosyada o başlık yok. Betik bütün
onayları boş yazardı ve kullanıcının işaretlediği değerler sessizce kaybolurdu.

## `src/data/build_input_manifest.py` ve `src/evaluation/threshold_probabilities.py`

- **Ne değişti:** fonksiyon adları (`compute_sha256`, `count_lines`, `scan_root`, yeni ortak yardımcı `build_file_record`;
  `sign_test_p_value`, `minimum_wins_required`, `trap_threshold_analysis` ve diğerleri) ve çıktı JSON anahtarları.
- **Ne değişmedi:** hesap. Gerçek girdilerde yeni manifest v5 ile 27/27 kilitli ve 506/506 dosyada aynı özet verdi;
  eşik olasılıkları v1 JSON'uyla anahtar eşlemesinden sonra aynı çıktı (ölçüldü).
- **Neden tarihî dosyalar yerinde:** manifest bir kanıttır; içeriği ya da yolu değişirse "kilitli set değişmedi" iddiası
  eski commit'lerle karşılaştırılamaz. Bu yüzden v1–v5 Türkçe anahtarlarıyla saklandı (2026-11-25'te `archive/degerlendirme/` altına taşındı; 2026-11-26'dan beri yalnızca git geçmişinde, commit'leri `evaluation/lock_manifest_changelog.md` tablosunda); okuyacak
  betikler `LEGACY_FIELD_NAMES` sözlüğünü kullanır.

**Kontrol sorusu:** `compute_sha256` adı `sha256_hesapla`'dan neden daha iyi?
*Cevap:* Ekip ve kaynaklar "compute/hash" fiilini kullanır; adı okuyan, belgeye bakmadan bir değer hesapladığını ve dosyayı değiştirmediğini anlar.

## `src/data/build_path_migration_manifest.py`: taşınan dosyaların kanıtı

**Yol ve girdi:** `--mapping` ([eski_yol, yeni_yol] listesi), `--base-ref` (eski içeriğin okunacağı git sürümü),
`--lock-manifest` (hangi dosyaların kilitli olduğu), `--output`.

**Blok 1: eşleme.** Eski ve yeni yol çiftleri elle yazılmış bir JSON'dan okunur. Neden: git'in otomatik ad değişikliği
tahmini (rename detection) boş `__init__.py` ve `.gitkeep` dosyalarını rastgele eşleyebiliyor; elle yazılan eşleme
gerçek anlamı taşır.

**Blok 2: iki özet.** Eski yolun SHA-256'sı `git show <sürüm>:<yol>` ile git'ten, yeni yolunki diskten hesaplanır.
Neden: taşınan dosyanın eski yolu diskte artık yok. İçerik yalnızca özet için belleğe alınır, hiçbir yere yazılmaz.

**Blok 3: kilit ve sonuç.** Her kayda `content_unchanged` (içerik aynı mı) ve `locked` (kilitli mi) eklenir; ekrana
yalnızca sayılar basılır. Kilitli bir dosyanın içeriği değişmişse `locked_changed` sıfırdan büyük çıkar.

**Gerçek çalışma (ölçüldü):** 24 dosya; 7'si içerikçe aynı (system prompt ve `.gitkeep`'ler), 17'si bilerek
değişti; kilitli dosya 0.

**Üç cümlelik özet:** Ad değişikliğinden sonra hangi dosyanın yalnızca yer değiştirdiğini, hangisinin içeriğinin de
değiştiğini SHA-256 ile kanıtlar. Eski içerik git'ten okunur, yeni içerik diskten. Kilitli bir dosya değişirse sayı
olarak hemen görünür.

**Kontrol sorusu:** System prompt dosyası taşındı; içeriğinin değişmediğini nasıl biliyoruz?
*Cevap:* Manifestte `prompts/system_prompt_v1.txt` için `old_sha256` (HEAD'deki `istemler/sistem_v1.txt`) ile
`new_sha256` aynı ve `content_unchanged: true`.

## Kod yazım kuralları neden eklendi

Kodu okuyan biri her fonksiyonun ne yaptığını ve neden var olduğunu docstring'den öğrenebilmeli. Bu yüzden bütün
betiklerde fonksiyon başına "ne alır, ne döndürür, neden var" yazıldı; `ap`, `args`, `n`, `tol`, `pp` gibi kısaltmalar
`parser`, `arguments`, `decision_count`, `tolerance`, `percentage_points` oldu. Davranışın değişmediği, eski ve yeni
betikler aynı girdide çalıştırılarak doğrulandı (13/13 kontrol). Kurallar CLAUDE.md'de "Kod yazım kuralları" başlığında.
