# System prompt değişiklik kaydı

Sürüm: 1

Onaylanan commit: (onay verilince yazılacak)

Bu dosya `prompts/system_prompt.txt` dosyasının sürüm kaydıdır. Eğitim, değerlendirme ve servis aynı dosyayı kullanır.

Sürüm satırları prompt dosyasının içine değil, buraya yazılır (proje sahibi kararı 2A, 2026-11-26). Neden: model `system_prompt.txt` dosyasını olduğu gibi okur. Dosyaya "Sürüm: 1" yazılsaydı model de bu satırı görürdü. Dosya saf kaldığı için, aşağıdaki parmak izi tam olarak modelin gördüğü metnin izidir.

SHA-256, bir dosyanın parmak izidir: dosyada tek bir harf değişse bile tamamen değişir. `experiments.csv` dosyasının `system_prompt_sha256` sütununa her deneyde bu parmak izi yazılır. Böylece her deneyin hangi system prompt ile yapıldığı kesin olarak kanıtlanır.

## Güncel hâl

| Alan | Değer |
|---|---|
| Dosya | `prompts/system_prompt.txt` |
| Sürüm | 1 |
| Boyut | 2.977 bayt (ölçüldü, 2026-11-26) |
| SHA-256 | `0ecd66614c7f4b7db1aab3d671e90125517c83453bd38bc78f34019bdd048cf0` (ölçüldü, 2026-11-26) |
| Durum | taslak; proje sahibi onayı bekliyor |

Parmak izini yeniden ölçmek için:

```bash
sha256sum prompts/system_prompt.txt
```

## Değişiklik geçmişi

Onaydan sonraki her değişiklikte "Sürüm" numarası bir artar, yeni parmak izi yukarıdaki tabloya yazılır ve buraya bir satır eklenir. Eski hâller git geçmişindedir: `git log --follow -- prompts/system_prompt.txt`.

| Tarih | Ne değişti | Neden |
|---|---|---|
| 2026-11-23 | İlk taslak (`istemler/sistem_v1.txt`); aynı gün kararlar 9–14 ile yerinde düzeltildi, sürüm numarası artırılmadı. | Dosya henüz hiçbir eğitimde veya değerlendirmede kullanılmamıştı. Ayrıntı: `PROJECT_STATUS.md`, "System prompt kararları". |
| 2026-11-25 | Ad `prompts/system_prompt_v1.txt` oldu; içerik aynı. | İsimlendirme bakımı (İngilizce klasör ve dosya adları). |
| 2026-11-26 | Ad `prompts/system_prompt.txt` oldu; içerik aynı (SHA-256 yukarıdaki değer). | Dosya adlarında sürüm eki kullanılmaz; sürüm bu dosyada ve git geçmişinde durur (proje sahibi kararı). |
