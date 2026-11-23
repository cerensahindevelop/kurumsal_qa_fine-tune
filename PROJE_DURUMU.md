# PROJE_DURUMU

Son güncelleme: 2026-11-23 (01 açık kararları ve karar 6 işlendi) · Son tamamlanan aşama: **01**

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
| `degerlendirme/gelistirme_kapsam_disi.jsonl` | 15 soru, `onay: bekliyor` |
| `degerlendirme/kilit_manifesti_v1.json` | 25 kilitli dosyanın SHA-256 özeti |
| `src/veri/girdi_ozeti.py` | Girdi özeti ve kilit manifesti betiği (içerik basmaz) |
| `env/2026-11-23_girdi_sha256.json` | 505 girdi dosyasının özeti |
| `env/2026-11-23_paketler.txt`, `env/2026-11-23_donanim.txt` | Ortam kaydı |
| `docs/ogrenme/01_iskelet_ve_plan.md` | Öğrenme açıklaması |
| `rapor/rapor_plani_v1.md` | Rapor iskeleti ve önceden bilinen sınırlamalar (açık kararlar güncellemesinde eklendi) |
| `inceleme/genel_kontrol_v2_taslak.jsonl`, `inceleme/genel_kontrol_v2_onay.csv` | Saklanan üslup sızıntısı seti taslağı (60) ve onay kuyruğu (karar 6a) |
| `degerlendirme/kilit_manifesti_v2.json`, `env/2026-11-23_girdi_sha256_v2.json` | 27 kilitli dosya: v1'deki 25 + ham `01_sss` + v2 taslağı |

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

### Açık kararlar (kullanıcı)
7. **`genel_kontrol_v2` onayı:** `inceleme/genel_kontrol_v2_onay.csv` doldurulacak. Kontrol edilmesi gerekenler `deney_plani_v1.md` karar 6'da; en önemlisi, `b_kurum_gayriresmi` grubunun v1'le aynı anlama gelip gelmediği. Onaydan sonra ayrıca önerilen Read deny kuralı (`degerlendirme/saklanan/**`, `inceleme/genel_kontrol_v2_*`) eklenmeli.
8. **Senior onayları:** `esikler_v1.md` (bütün satırlar, §3A dahil), `deney_plani_v1.md`, `rapor/rapor_plani_v1.md`, `cevap_standardi_v1.md`, `sistem_v1.txt`, `gelistirme_kapsam_disi.jsonl` (15 soru). Son üçünü kullanıcı ayrıca inceleyecek; bu adımda dokunulmadı.

### Sonraki aşamanın ihtiyaç duyacağı bilgiler
- Kilitli desenler `src/veri/girdi_ozeti.py` içindeki `VARSAYILAN_KILITLI` listesinde. 02 ve sonrası bu listeye uymalı.
  - `01_sss/*` deseni listeye eklendi. Yeni `--ek-kilitli` seçeneği proje içindeki tek dosyaları kilitler. Geçerli manifest: `kilit_manifesti_v2.json`.
- **02'de Türkçe değerlendirme bölmesi:**
  - Dosya başına %30 / %70, seed 42, geliştirmede ≥ 50 kayıt.
  - Alt grubu olan dosyalarda (TurkishMMLU ders, `genel_kontrol` soru türü) katmanlı.
  - Betik yalnızca kimlik, sayı ve SHA-256 yazar.
  - Beklenen boyutlar `deney_plani_v1.md` §6.5'te.
  - `genel_kontrol_v1` ve `turkishmmlu_dev` bölünmez (karar 6). `genel_kontrol_v2` saklanan bölümdür.
- 02'deki çakışma denetimine `inceleme/genel_kontrol_v2_taslak.jsonl` (onaylı hâli) de girer. Karşılaştırılacak setler: eğitim adayları, genel Türkçe havuzu, `genel_kontrol_v1`, geliştirme kapsam dışı seti, doğrulama, test ve tuzak.
- v2 onaylanınca: `degerlendirme/saklanan/genel_kontrol_v2.jsonl` yoluna taşınır, `kilit_manifesti_v3.json` üretilir ve hiçbir model çalışmadan önce commit edilir.
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
