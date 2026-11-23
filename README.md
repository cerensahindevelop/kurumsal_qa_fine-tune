# kurum-qa-finetune

Kurum çalışanları için resmî üsluplu soru-cevap modeli: resmî `Qwen/Qwen3.8-27B` üzerine LLaMA-Factory ile 4-bit QLoRA.
İlk tur açık verilerle (ÇSGB, SGK, İŞKUR) yapılan bir pilottur. Kurum verisi geldiğinde aynı akış orijinal modelden yeniden çalıştırılır.

Proje kuralları: `CLAUDE.md` · Güncel durum: `PROJE_DURUMU.md`

## Klasörler

| Klasör | İçerik |
|---|---|
| `configs/` | Deney YAML'ları (`<deney_id>.yaml`) |
| `data/` | Üretilen eğitim/doğrulama dosyaları + `dataset_info.json` (JSONL'ler git'e girmez) |
| `src/` | Betikler: `veri/`, `egitim/`, `degerlendirme/`, `uretim/`, `servis/` |
| `istemler/` | Sistem mesajı (`sistem_v1.txt`) ve cevap standardı |
| `inceleme/` | İnsanın dolduracağı CSV kuyrukları |
| `degerlendirme/` | Deney planı, eşikler, kilit manifesti, geliştirme kapsam dışı seti, puanlama çıktıları |
| `experiments/` | Deney çıktıları (`<deney_id>/`, asla yeniden kullanılmaz) |
| `rapor/` | Senior raporu |
| `docs/ogrenme/` | Aşama aşama öğrenme açıklamaları |
| `env/` | Paket, donanım ve girdi özeti kayıtları |

## Girdiler (salt okunur)

- Ham veri: `/home/aipc/Desktop/fine_tuneVeriler`
- Hazırlanmış veri: `/home/aipc/Desktop/Gruplu Veriler`

Test, tuzak ve Türkçe değerlendirme setleri kilitlidir. Bu setlere yalnızca sayı, kimlik ve SHA-256 özeti yazan betikler dokunur. Kilitli dosyaların listesi ve özetleri: `degerlendirme/kilit_manifesti_v3.json` (geçerli sürüm).

## Çalıştırma sırası

Her komut proje kökünden çalıştırılır. Yollarda boşluk olduğu için tırnak kullanılır.

### 01: İskelet ve ön kayıt

```bash
# 1) Girdilerin SHA-256 özeti ve kilit manifesti (içerik basmaz)
python -m src.veri.girdi_ozeti \
  --girdi "/home/aipc/Desktop/Gruplu Veriler" /home/aipc/Desktop/fine_tuneVeriler \
  --ek-kilitli inceleme/genel_kontrol_v2_taslak.jsonl \
  --cikti env/$(date +%F)_girdi_sha256_v3.json \
  --kilit-cikti degerlendirme/kilit_manifesti_v3.json
# (v1 manifesti --ek-kilitli olmadan ve 01_sss deseni eklenmeden üretilmişti; v2, b grubu yeniden yazılmadan önceki taslağı kilitler.)
# genel_kontrol_v2 onaylanıp degerlendirme/saklanan/ altına taşınınca --ek-kilitli o yolu gösterir
# ve çıktı kilit_manifesti_v4.json olur.

# 1b) Asistanın yazdığı taslaklar için insan onay kuyruğu (dolu hücreler kimliğe göre korunur)
python -m src.veri.onay_csv \
  --girdi inceleme/genel_kontrol_v2_taslak.jsonl \
  --cikti inceleme/genel_kontrol_v2_onay.csv

# 2) Paket ve donanım kaydı
pip freeze > env/$(date +%F)_paketler.txt
nvidia-smi --query-gpu=index,name,pci.bus_id,memory.total,memory.used,driver_version --format=csv > env/$(date +%F)_donanim.txt
ollama --version >> env/$(date +%F)_donanim.txt
```

Sonraki aşamaların komutları her aşama sonunda bu bölüme eklenir.

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
