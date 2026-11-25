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
| `prompts/` | System prompt (`system_prompt_v1.txt`) ve cevap standardı |
| `review/` | İnsanın dolduracağı CSV kuyrukları |
| `evaluation/` | Deney planı, eşikler, geliştirme kapsam dışı seti, yeni kilit manifestleri, puanlama çıktıları |
| `experiments/` | Deney çıktıları (`<experiment_id>/`, asla yeniden kullanılmaz) |
| `report/` | Senior raporu |
| `docs/learning/` | Aşama aşama öğrenme açıklamaları |
| `env/` | Paket, donanım ve girdi özeti kayıtları |

## Tarihî kayıtlar

2026-11-25 isimlendirme bakımından önce üretilmiş kayıtlar `archive/` klasöründe saklanır. Bu dosyalar değiştirilmez;
yeni çıktılar oraya yazılmaz. Ayrıntı: `archive/README.md`.

| Yer | İçerik | Not |
|---|---|---|
| `archive/degerlendirme/` | Kilit manifestleri v1–v5 (`lock_manifest_v1.json` … `v5`), `threshold_probabilities_v1.json` | Türkçe alan adlarıyla. Karşılıklar `LEGACY_FIELD_NAMES` ve `LEGACY_OUTPUT_KEYS` sözlüklerinde. |
| `archive/env/` | Girdi parmak izi listeleri v1–v5, paket ve donanım kayıtları (2026-11-23/24) | Eski adları `girdi_sha256`, `paketler`, `donanim` idi. |
| `inceleme/` | Kilitli `genel_kontrol_v2_taslak.jsonl` ve onay CSV'si | Arşivde değil; kilitli olduğu için yerinde duruyor. 02'de `evaluation/held_out/` altına taşınacak. |

Taşınan 38 dosyanın "eski yol → yeni yol → SHA-256" listesi: `evaluation/path_migration_manifest_2026-11-25.json`
(24'ü ad değişikliği, 14'ü arşive taşıma; arşivdekilerin hepsi içerikçe aynı).

## Girdiler (salt okunur)

- Ham veri: `/home/aipc/Desktop/fine_tuneVeriler`
- Hazırlanmış veri: `/home/aipc/Desktop/Gruplu Veriler`

Test, tuzak ve Türkçe değerlendirme setleri kilitlidir. Bu setlere yalnızca sayı, kimlik ve SHA-256 özeti yazan betikler dokunur. Kilitli dosyaların listesi ve özetleri: `evaluation/lock_manifest_v6.json` (geçerli sürüm, 2026-11-25; v5 ile aynı 27 dosya ve aynı SHA-256 özetleri, yeni alan adlarıyla). v1–v5 `archive/degerlendirme/` altında tarihî kayıt olarak durur.

**11. aşamadaki kilit kontrolü** o gün geçerli olan en yüksek numaralı `evaluation/lock_manifest_v<N>.json` dosyasını kullanır. 02'de `genel_kontrol_v2` `evaluation/held_out/` altına taşınınca `lock_manifest_v7.json` üretilir; 11'de beklenen manifest v7'dir. Kontrol yalnızca SHA-256 ve sayı karşılaştırır, içerik basmaz.

## Çalıştırma sırası

Her komut proje kökünden çalıştırılır. Yollarda boşluk olduğu için tırnak kullanılır.

### 01: İskelet ve ön kayıt

```bash
# 1) Girdilerin SHA-256 özeti ve kilit manifesti (içerik basmaz)
#    N = son sürüm + 1 (şu an 7). v1–v6 üretildi; var olan sürümün üzerine yazılmaz.
python -m src.data.build_input_manifest \
  --input "/home/aipc/Desktop/Gruplu Veriler" /home/aipc/Desktop/fine_tuneVeriler \
  --extra-locked inceleme/genel_kontrol_v2_taslak.jsonl \
  --output env/$(date +%F)_input_sha256_vN.json \
  --lock-manifest-output evaluation/lock_manifest_vN.json
# v1–v5 eski adla üretildi: src.veri.girdi_ozeti --girdi/--cikti/--kilit-cikti/--ek-kilitli,
# çıktılar archive/env/2026-11-23_input_sha256_v5.json ve archive/degerlendirme/lock_manifest_v5.json.
# Eski Türkçe seçenek adları 2026-11-25'te kaldırıldı; yalnızca İngilizce adlar çalışır. Alan adları v6'dan itibaren İngilizce
# (kok→root, yol→path, bayt→bytes, satir→lines, kilitli→locked; tam liste LEGACY_FIELD_NAMES).
# (v1 manifesti --extra-locked olmadan ve 01_sss deseni eklenmeden üretilmişti; v2, b grubu yeniden yazılmadan önceki taslağı; v3, GK2-050 düzeltmesinden önceki taslağı; v4, kullanıcı onayından ve GK2-044 düzeltmesinden önceki taslağı kilitler.)
# genel_kontrol_v2 onaylanıp evaluation/held_out/ altına taşınınca --extra-locked o yolu gösterir
# ve çıktı lock_manifest_v7.json olur.

# 1b) Asistanın yazdığı taslaklar için insan onay kuyruğu (dolu hücreler kimliğe göre korunur;
#     sonunda onay dağılımını yazar, "düzelt"/"duzelt" aynı sayılır)
#     Eski Türkçe başlıklı CSV'ler de okunur; yeniden çalıştırılırsa başlıklar İngilizce yazılır,
#     onay/not hücreleri kimliğe göre taşınır. Yeni kuyruklar review/ altına yazılır.
python -m src.data.build_review_csv \
  --input inceleme/genel_kontrol_v2_taslak.jsonl \
  --output inceleme/genel_kontrol_v2_onay.csv

# 1c) Eşik gerekçelerindeki olasılıklar (veri okumaz; tam olasılık hesabı)
#     Aile düzeyinde yanlış alarm, 4.1 tuzak toleransı, kalibrasyon belirsizliği, işaret testi tablosu
#     v1 (archive/degerlendirme/threshold_probabilities_v1.json) Türkçe anahtarlarla yazıldı ve arşivde durur;
#     v2 aynı sayıları İngilizce anahtarlarla yazar (karşılıklar: LEGACY_OUTPUT_KEYS).
python -m src.evaluation.threshold_probabilities \
  --output evaluation/threshold_probabilities_v2.json

# 2) Paket ve donanım kaydı
#    (2026-11-23/24 kayıtları archive/env/ altında)
pip freeze > env/$(date +%F)_packages.txt
nvidia-smi --query-gpu=index,name,pci.bus_id,memory.total,memory.used,driver_version --format=csv > env/$(date +%F)_hardware.txt
ollama --version >> env/$(date +%F)_hardware.txt
```

### Bakım (2026-11-25): isimlendirme ve arşiv

```bash
# Taşınan dosyaların eski/yeni yolu ve SHA-256 özeti (eşleme elle yazıldı; içerik basmaz).
# Eşleme hem ad değişikliğini hem archive/ taşımasını içerir.
# --base-ref, bakımdan önceki son commit'tir (59aa89e); eski içerik oradan okunur.
python -m src.data.build_path_migration_manifest \
  --mapping evaluation/path_migration_map_2026-11-25.json \
  --base-ref 59aa89e \
  --lock-manifest evaluation/lock_manifest_v6.json \
  --output evaluation/path_migration_manifest_2026-11-25.json

# Yeni alan adlarıyla güncel kilit manifesti (v6; v5 ile aynı 27 dosya ve özet)
python -m src.data.build_input_manifest \
  --input "/home/aipc/Desktop/Gruplu Veriler" /home/aipc/Desktop/fine_tuneVeriler \
  --extra-locked inceleme/genel_kontrol_v2_taslak.jsonl \
  --output env/2026-11-25_input_sha256_v6.json \
  --lock-manifest-output evaluation/lock_manifest_v6.json
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
