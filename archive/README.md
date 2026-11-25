# archive/

Bu klasörde projenin eski kayıtları saklanır. Buradaki dosyalar tarihî kayıttır; **değiştirilmez ve silinmez**.
Yeni çıktılar buraya yazılmaz.

## Neden saklanıyor

Kilit manifesti, kilitli test dosyalarının belli bir gündeki "parmak izlerini" (SHA-256 özetlerini) tutan listedir.
Bu listeler, test dosyalarına kimsenin dokunmadığının kanıtıdır. Kanıtın değeri, sonradan değişmemesindedir.
Bu yüzden eski sürümler silinmez, yalnızca bu klasöre toplanır.

## İçindekiler

| Dosya | Ne |
|---|---|
| `degerlendirme/lock_manifest_v1.json` … `lock_manifest_v5.json` | Kilit manifestinin ilk beş sürümü (2026-11-23/24). Geçerli sürüm `evaluation/lock_manifest_v6.json`; v5 ile aynı dosyaları ve aynı parmak izlerini taşır. |
| `degerlendirme/threshold_probabilities_v1.json` | Eşik olasılıklarının ilk hesabı. Yeni hesap aynı sayıları verir. |
| `env/2026-11-23_input_sha256_v1.json` … `_v5.json` | Bütün girdi dosyalarının parmak izi listeleri. |
| `env/2026-11-23_packages.txt`, `env/2026-11-24_packages.txt` | O günlerde kurulu Python paketlerinin listesi. |
| `env/2026-11-23_hardware.txt` | Ekran kartları ve sürücü bilgisi. |

## Dikkat

- Bu dosyaların içinde alan adları Türkçedir (örneğin `yol`, `kilitli`). Yeni adlarla karşılıkları
  `src/data/build_input_manifest.py` içindeki `LEGACY_FIELD_NAMES` ve `src/evaluation/threshold_probabilities.py`
  içindeki `LEGACY_OUTPUT_KEYS` listelerindedir.
- Dosyalar 2026-11-25'te eski yerlerinden (`degerlendirme/`, `env/`) buraya taşındı ve adları İngilizceye çevrildi.
  Taşımadan önce ve sonra parmak izleri aynıdır. Eski yer → yeni yer listesi:
  `evaluation/path_migration_manifest_2026-11-25.json`.
- `degerlendirme/` alt klasörünün adı, dosyaların geldiği yeri göstermek için korunmuştur.
