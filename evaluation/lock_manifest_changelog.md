# Kilit manifesti değişiklik kaydı

SHA-256 bir dosyanın parmak izidir; yalnızca değişip değişmediğini gösterir. Neyin neden değiştiğini bu tablo anlatır.

Kilit manifesti tek bir dosyadır: `evaluation/lock_manifest.json`. Sürüm numarası dosyanın içindeki `version` alanındadır.
Eski sürümler git geçmişindedir. Bir sürümü görmek için tablodaki commit ile yolu birleştirin. Örnek (sürüm 5):

```bash
git show 35f1a69:degerlendirme/kilit_manifesti_v5.json
```

Tablodaki "değişti / eklendi / aynı" bilgileri `src/evaluation/compare_lock_manifests.py` betiğinin çıktısından alındı (ölçüldü).
Parmak izleri ilk 12 karakteriyle yazıldı. Betik yalnızca manifestleri okur; kilitli dosyaların içeriği açılmadı.
"Neden" sütunu `PROJECT_STATUS.md` ve `evaluation/experiment_plan_v1.md` içindeki kararlardan kısaltıldı.

## Sürümler

| Sürüm | Tarih | Ne değişti | Hangi dosya | Neden | Commit |
|---|---|---|---|---|---|
| v1 | 2026-11-23 | İlk kilit: 25 dosya kilitlendi. | Test seti (1), tuzak seti (1), Türkçe değerlendirme (8), ham tuzak klasörü `05_tuzak_sorular` (5), ham genel Türkçe değerlendirme klasörü (10) | Test ve değerlendirme setlerinin, hiçbir iş başlamadan önceki parmak izini kaydetmek. | `914c1e8` |
| v2 | 2026-11-23 | 2 dosya eklendi; yeni kilit kalıbı `01_sss/*`. Diğer 25 dosya aynı. | `fine_tuneVeriler/01_sss/sss_birlesik.jsonl` (`830d67600620`), `inceleme/genel_kontrol_v2_taslak.jsonl` (`edf68c2c4bed`) | Test soruları ham sıkça sorulan sorulardan seçildiği için ham dosya da kilitlendi. `genel_kontrol_v1`'in tamamı geliştirme bölümü oldu; saklanan karşılığı olarak 60 soruluk `genel_kontrol_v2` taslağı yazıldı ve kilitlendi (karar 6a). | `0820870` |
| v3 | 2026-11-23 | 15 soru yeniden yazıldı (`b` grubu, GK2-036…050). Diğer 26 dosya aynı. | `inceleme/genel_kontrol_v2_taslak.jsonl` (`edf68c2c4bed` → `34abf2f80a7e`) | `b` grubu yanlış yorumlanmıştı. Yeni tanım: kurum işlemi soran, gündelik dille sorulmuş, sade ve adım adım anlatım bekleyen sorular (karar 6c). | `b4ebb4e` |
| v4 | 2026-11-23 | 1 soru düzeltildi (GK2-050). Diğer 26 dosya aynı. | `inceleme/genel_kontrol_v2_taslak.jsonl` (`34abf2f80a7e` → `93459a5c8b90`) | "Kısaca anlatır mısın?" yalnızca kısalık istiyordu, sade anlatım isteği değildi. Kullanıcı onayıyla "Kısaca ve sade bir dille anlatır mısın?" oldu. | `518aa58` |
| v5 | 2026-11-23 | 1 sorunun bir bilgi öğesi düzeltildi (GK2-044, 4. öğe); taslak kullanıcı tarafından onaylandı (60/60 "evet"). Diğer 26 dosya aynı. | `inceleme/genel_kontrol_v2_taslak.jsonl` (`93459a5c8b90` → `3b8d3aa1dab9`) | Kullanıcı incelemesi: kıdem tazminatıyla ilgili öğe eksikti; işçinin haklı nedenle feshi de tazminat doğurur. | `35f1a69` |
| v6 | 2026-11-25 | Hiçbir dosya değişmedi (27/27 aynı, kilit kalıpları aynı). Yalnızca manifestin alan adları İngilizce oldu (`yol` → `path` gibi). 2026-11-26'da dosya `evaluation/lock_manifest.json` adını aldı ve içine `"version": 6` eklendi; kilitli dosyalar ve parmak izleri aynı kaldı. | — | İsimlendirme bakımı. Eski manifestler `archive/degerlendirme/` altına taşındı. | `6f55863` |

**Test ve tuzak dosyaları bütün sürümlerde aynı kaldı (ölçüldü).** Test seti, tuzak seti ve ham tuzak klasöründeki 5 dosya (toplam 7) her ardışık çiftte (v1→v2, v2→v3, v3→v4, v4→v5, v5→v6) 7/7 aynı. v1→v6 doğrudan karşılaştırmasında da 7/7 aynı. v1'deki 25 dosyanın 25'i v6'da aynı parmak iziyle duruyor; bütün sürümlerde değişen tek dosya `genel_kontrol_v2` taslağı.

**Sürümlerin yolları (git'te):**

| Sürüm | Commit | Yol |
|---|---|---|
| v1–v5 | tablodaki commit | `degerlendirme/kilit_manifesti_v<N>.json` |
| v6 | `6f55863` (son hâli `1919cce`) | `evaluation/lock_manifest_v6.json` |
| 6 ve sonrası (tek dosya) | her sürümün commit'i | `evaluation/lock_manifest.json` |

Not: v1–v5 2026-11-25'te `archive/degerlendirme/` altına taşındı, 2026-11-26'da arşiv kaldırıldı. Bu yüzden `git log --follow` bu dosyalarda yanlış commit gösterebilir. Commit'ler eski yollarla bulundu: `git log --diff-filter=A -- degerlendirme/kilit_manifesti_v<N>.json`.

## Taşıma kayıtlarının özeti

2026-11-25 isimlendirme ve arşiv bakımında 38 dosya taşındı: 24'ü ad değişikliği, 14'ü arşive taşıma. 21'inin içeriği aynı kaldı; 17'si bilerek değiştirilen belge ve koddu. Kilitli dosya 0. Kayıtlar 2026-11-26'da silindi (proje sahibi kararı 1B). Geri getirmek için:

```bash
git show 1919cce:evaluation/path_migration_manifest_2026-11-25.json
git show 1919cce:evaluation/path_migration_map_2026-11-25.json
```

2026-11-26'da arşiv kaldırılırken dört dosya taşındı: kilit manifesti (yalnızca `version` satırı eklendi), girdi listesi, paket ve donanım kaydı. Üçünün içeriği aynı. Kilitli dosya 0. Bundan sonraki taşımaların kaydı tek dosyadır: `evaluation/path_migration.json` (yalnızca son taşıma; öncekiler git'te).

## Yeni sürüm eklenirken

`build_input_manifest` sürüm numarasını artırdığında (ekranda `lock_manifest=yeni_sürüm`), commit etmeden önce yeni dosya git'teki son sürümle karşılaştırılır ve bu tabloya yeni bir satır eklenir:

```bash
python -m src.evaluation.compare_lock_manifests \
  --old HEAD:evaluation/lock_manifest.json \
  --new evaluation/lock_manifest.json
```

Kilitli bir dosya taşındıysa, taşıma kaydı da verilir: `--path-migration evaluation/path_migration.json`. Böylece taşınan dosya "çıkarıldı + eklendi" diye değil, "taşındı" diye görünür. Satırdaki "test ve tuzak" sonucu betiğin son satırlarından alınır.
