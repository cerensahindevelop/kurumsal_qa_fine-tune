# kurum-qa-finetune

Kurum çalışanları için resmî üsluplu soru-cevap modeli: resmî `Qwen/Qwen3.8-27B` üzerine LLaMA-Factory ile 4-bit QLoRA.
Fine-tuning proje sahibinin talebidir; prompt'la karşılaştırma kapsam dışıdır. Baseline (`baseline`: hazır Qwen3.8-27B, aynı system prompt'la), üslup gelişimi ve gerileme kontrolleri için taban çizgisidir.
İlk tur açık verilerle (ÇSGB, SGK, İŞKUR) yapılan bir pilottur. Kurum verisi geldiğinde aynı akış orijinal modelden yeniden çalıştırılır.

Proje kuralları: `CLAUDE.md` · Güncel durum: `PROJECT_STATUS.md`

## Klasörler

| Klasör | İçerik |
|---|---|
| `configs/` | Deney YAML'ları (`<experiment_id>.yaml`) |
| `data/` | Üretilen eğitim/doğrulama dosyaları + `dataset_info.json` (JSONL'ler git'e girmez) |
| `src/` | Betikler: `data/` (veri hazırlama, manifest, review CSV), `data_generation/` (öğretmen modelle eğitim verisi üretimi), `training/`, `evaluation/`, `serving/` |
| `prompts/` | System prompt (`system_prompt.txt`), onun sürüm kaydı (`system_prompt_changelog.md`) ve cevap standardı |
| `review/` | İnsanın dolduracağı CSV kuyrukları |
| `evaluation/` | Deney planı, eşikler, geliştirme kapsam dışı seti, kilit manifesti (`lock_manifest.json`) ve değişiklik kaydı, eşik olasılıkları, puanlama çıktıları |
| `experiments/` | Deney çıktıları (`<experiment_id>/`, asla yeniden kullanılmaz) |
| `report/` | Senior raporu |
| `docs/learning/` | Aşama aşama öğrenme açıklamaları |
| `env/` | `input_sha256.json` (girdi parmak izleri), `packages.txt` (paket sürümleri), `hardware.txt` (donanım) |
| `inceleme/` | Yalnızca 02'de taşınacak kilitli `genel_kontrol_v2` dosyaları; 02'den sonra silinir |

## Eski kayıtlar git geçmişinde

Her kayıt türünün tek bir güncel dosyası vardır. Örnekler: kilit manifesti `evaluation/lock_manifest.json`, paket listesi `env/packages.txt`.
Dosya güncellenince eski hâl silinmez; git onu geçmişinde saklar. Bu yüzden ayrı bir arşiv klasörü yoktur (`archive/` 2026-11-26'da kaldırıldı).

**Uyarı:** Projenin eski kayıtları git geçmişinde tutulur. Projeyi başka bir makineye (örneğin intranete) taşırken `git clone` ile, `.git` klasörüyle birlikte taşıyın; yalnızca dosyaları kopyalamak geçmişi kaybettirir.

Eski bir sürümü görmek için `git show <commit>:<yol>` kullanılır. Örnek, kilit manifestinin 5. sürümü:

```bash
git show 35f1a69:degerlendirme/kilit_manifesti_v5.json
```

- Kilit manifestinin her sürümünün commit'i, yolu ve "neyin neden değiştiği": `evaluation/lock_manifest_changelog.md`.
- Bir dosyanın bütün geçmişi: `git log --oneline -- <yol>`. Yolu değişmiş dosyalarda `--follow` bazen yanlış eşler; değişiklik kaydı bunun için doğrulanmış commit'leri verir.
- Dosya adlarında sürüm eki (`_v1` gibi) yoktur. Bir belgenin sürümü en üstteki "Sürüm" satırında, değişiklikleri en alttaki "Değişiklik geçmişi" bölümündedir. Onaylanan sürüm, onay commit'inin kimliğiyle kayıtlıdır. System prompt dosyasına satır eklenmez, çünkü model dosyayı olduğu gibi okur; sürümü ve parmak izi `prompts/system_prompt_changelog.md` içindedir.
- `experiments.csv` dosyasının `system_prompt_sha256` sütununa, deneyde kullanılan `prompts/system_prompt.txt` dosyasının SHA-256 parmak izi yazılır (`sha256sum prompts/system_prompt.txt`).
- Deney kimliği `<short_name>_run<N>` biçimindedir (örneğin `faq_adapter_run1`); aynı deneyin yeni koşusu bir sonraki numarayı alır.
- 2026-11-26'dan önceki yollar (örneğin `evaluation/thresholds_v1.md`) git geçmişindedir: `git log --follow -- evaluation/thresholds.md`.
- v1–v5 ve eski girdi listeleri Türkçe alan adlıdır. Betikler bunları `LEGACY_FIELD_NAMES` ve `LEGACY_OUTPUT_KEYS` sözlükleriyle okur.

## Girdiler (salt okunur)

- Ham veri: `/home/aipc/Desktop/fine_tuneVeriler`
- Hazırlanmış veri: `/home/aipc/Desktop/Gruplu Veriler`

Test, tuzak ve Türkçe değerlendirme setleri kilitlidir. Bu setlere yalnızca sayı, kimlik ve SHA-256 özeti yazan betikler dokunur. Kilitli dosyaların listesi ve özetleri: `evaluation/lock_manifest.json`. Sürüm numarası dosyanın içindeki `version` alanındadır; şu an **6** (27 dosya).

**11. aşamadaki kilit kontrolü** `evaluation/lock_manifest.json` dosyasını kullanır. 02'de `genel_kontrol_v2` `evaluation/held_out/` altına taşınınca bu dosya güncellenir ve sürüm 7 olur; 11'de beklenen sürüm 7'dir. Kontrol yalnızca SHA-256 ve sayı karşılaştırır, içerik basmaz.

## Çalıştırma sırası

Her komut proje kökünden çalıştırılır. Yollarda boşluk olduğu için tırnak kullanılır.

### 01: İskelet ve ön kayıt

```bash
# 1) Girdilerin SHA-256 özeti ve kilit manifesti (içerik basmaz)
#    İki dosya da tek güncel dosyadır; her çalıştırmada üzerine yazılır, eski hâl git geçmişinde kalır.
#    Betik, git'e kaydedilmemiş bir dosyanın üzerine yazmaz: önce commit edin.
#    Kilit manifestinin version alanı yalnızca kilitli dosyalar ya da kalıplar değişince bir artar;
#    değişmediyse dosyaya dokunulmaz ve ekrana "lock_manifest=değişmedi" yazılır.
python -m src.data.build_input_manifest \
  --input "/home/aipc/Desktop/Gruplu Veriler" /home/aipc/Desktop/fine_tuneVeriler \
  --extra-locked inceleme/genel_kontrol_v2_taslak.jsonl \
  --output env/input_sha256.json \
  --lock-manifest-output evaluation/lock_manifest.json
# Alan adları sürüm 6'dan itibaren İngilizce (kok→root, yol→path, bayt→bytes, satir→lines, kilitli→locked;
# tam liste LEGACY_FIELD_NAMES). Sürümlerin hikâyesi: evaluation/lock_manifest_changelog.md.
# genel_kontrol_v2 evaluation/held_out/ altına taşınınca --extra-locked o yolu gösterir ve sürüm 7 olur.

# 1a) KURAL: kilit manifestinin sürümü her arttığında son commit'teki hâliyle karşılaştır ve
#     evaluation/lock_manifest_changelog.md tablosuna yeni satır ekle (ne değişti, hangi dosya, neden, commit).
#     --old HEAD:... git'teki son kaydedilmiş sürümü okur. Betik yalnızca manifestleri okur; kilitli dosyaları açmaz.
#     Kilitli bir dosya taşındıysa sona --path-migration evaluation/path_migration.json ekle (aşağıdaki 1d).
python -m src.evaluation.compare_lock_manifests \
  --old HEAD:evaluation/lock_manifest.json \
  --new evaluation/lock_manifest.json

# 1b) Asistanın yazdığı taslaklar için insan onay kuyruğu (dolu hücreler kimliğe göre korunur;
#     sonunda onay dağılımını yazar, "düzelt"/"duzelt" aynı sayılır)
#     Eski Türkçe başlıklı CSV'ler de okunur; yeniden çalıştırılırsa başlıklar İngilizce yazılır,
#     onay/not hücreleri kimliğe göre taşınır. Yeni kuyruklar review/ altına yazılır.
python -m src.data.build_review_csv \
  --input inceleme/genel_kontrol_v2_taslak.jsonl \
  --output inceleme/genel_kontrol_v2_onay.csv

# 1c) Eşik gerekçelerindeki olasılıklar (veri okumaz; tam olasılık hesabı)
#     Aile düzeyinde yanlış alarm, 4.1 tuzak toleransı, kalibrasyon belirsizliği, işaret testi tablosu.
#     İlk çıktı Türkçe anahtarlıydı ve git geçmişindedir; sayılar aynı (karşılıklar: LEGACY_OUTPUT_KEYS).
python -m src.evaluation.threshold_probabilities \
  --output evaluation/threshold_probabilities.json

# 1d) Dosya taşındığında taşıma kaydı (eski yol → yeni yol → SHA-256; içerik basmaz).
#     Tek güncel dosya evaluation/path_migration.json; yalnızca son taşımayı anlatır.
#     2026-11-25 ad değişikliğinin kaydı: git show 1919cce:evaluation/path_migration_manifest_2026-11-25.json
python -m src.data.build_path_migration_manifest \
  --pair <eski_yol> <yeni_yol> \
  --base-ref HEAD \
  --lock-manifest evaluation/lock_manifest.json \
  --output evaluation/path_migration.json

# 2) Paket ve donanım kaydı (tek dosyalar; tarihli kopya üretilmez)
pip freeze > env/packages.txt
nvidia-smi --query-gpu=index,name,pci.bus_id,memory.total,memory.used,driver_version --format=csv > env/hardware.txt
ollama --version >> env/hardware.txt
```

Sonraki aşamaların komutları her aşama sonunda bu bölüme eklenir.

## Erişim engeli testi

Test ve tuzak dosyalarını Claude Code'un okuması `.claude/settings.json` içindeki engel kurallarıyla (deny kuralları) yasaklanır.
Bu test, engellerin gerçekten çalıştığını zararsız bir dosyayla gösterir.

**a) Ne zaman yapılır**
- Claude Code güncellendiğinde.
- `.claude/settings.json` değiştiğinde.
- Proje başka bir makineye taşındığında (örneğin kurumun internetsiz ağına).

**b) Neden gerçek test dosyasıyla denenmez**
Kural çalışmıyorsa, deneme sırasında test sorularının içeriği görülmüş olur. Görülen bir soru "görülmemiş" hâle getirilemez; bu geri alınamaz.
Bu yüzden deneme, içinde önemli hiçbir şey olmayan geçici bir dosyayla yapılır. `security_check/` klasörü için kalıcı bir engel kuralı vardır.

**c) Adımlar**
1. Terminalde, proje klasöründeyken deneme dosyasını oluştur:
   ```bash
   mkdir -p security_check && echo "zararsiz deneme" > security_check/canary.txt
   ```
2. VS Code'da komut paletini aç ve **Reload Window** çalıştır. Böylece Claude Code ayarları yeniden okur.
3. Claude Code'da yeni bir sohbet aç ve şunu yaz: `security_check/canary.txt dosyasını Read aracıyla okumayı dene ve sonucu söyle`
4. Beklenen sonuç: okuma **reddedilir** ("denied by your permission settings" gibi bir mesaj).
5. Klasörü sil:
   ```bash
   rm -r security_check
   ```
   Klasör `.gitignore`'da olduğu için unutulsa bile git'e girmez; yine de her testten sonra silinir.

**d) Okuma reddedilmezse ne yapılır**
- Çalışmayı hemen durdur.
- `.claude/settings.json` dosyasını kontrol et: dosya bozuk mu, kurallar yerinde mi, yollar bu makineye uyuyor mu?
- Kurallar düzelip test yeniden yapılıp okuma reddedilene kadar kilitli dosyalarla ilgili hiçbir işe devam etme.

## GPU kuralı

Her GPU komutundan önce `CUDA_DEVICE_ORDER=PCI_BUS_ID` ayarlanır ve kart `CUDA_VISIBLE_DEVICES` ile seçilir. Eğitim RTX 4500 Ada'da (`CUDA_VISIBLE_DEVICES=1`), değerlendirme ve Ollama RTX A5000'de (`CUDA_VISIBLE_DEVICES=0`) çalışır.

## Offline taşıma listesi (intranet)

| Öğe | Durum |
|---|---|
| Python ortamı ve sabit sürümlü wheel'ler (`wheels/`) | bekleyen iş: proje ortamı kurulumu |
| `Qwen/Qwen3.8-27B` HF ağırlıkları (resmî) | bekleyen iş |
| Ollama ikilisi | 0.35.1 kurulu (gerekli ≥ 0.32.12) |
| Ollama modelleri: `qwen3.8` (resmî etiket), yargıç (`gemma4:12b` veya `gemma4:26b`, kalibrasyona göre) | bekleyen iş |
| Bu depo (`git bundle`) | her aşama sonunda güncel |
