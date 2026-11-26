# Bakım: tek güncel dosya düzeni (2026-11-26)

Bu bakım bir aşama değildir. Kural: her kayıt türünün tek bir güncel dosyası olur. Eski sürümler ayrı dosyalarda değil, git geçmişinde durur.

## Fikir: git zaten bir arşivdir

Git, her commit'te bütün dosyaların o anki hâlini saklar. `lock_manifest_v5.json`, `lock_manifest_v6.json` gibi kopyalar tutmak, aynı bilgiyi iki yerde tutmak demektir.
İki yerde tutulan bilgi zamanla birbirinden ayrılır ve hangisinin doğru olduğu karışır.

- Eski bir sürümü görmek için: `git show <commit>:<yol>`. Örnek: `git show 35f1a69:degerlendirme/kilit_manifesti_v5.json`.
- Kilit manifestinin hangi sürümünün hangi commit'te olduğu `evaluation/lock_manifest_changelog.md` tablosunda yazar.
- **Dikkat:** Bu düzen `.git` klasörüne dayanır. Proje başka bir makineye `git clone` ile taşınmalıdır. Yalnızca dosyaları kopyalamak, geçmişi ve dolayısıyla bütün eski sürümleri kaybettirir.

## `src/data/build_input_manifest.py`: iki yeni koruma

**Blok 1: üzerine yazmadan önce kontrol (`ensure_committed`).**
- Aldığı veri: yazılacak dosyanın yolu, örneğin `evaluation/lock_manifest.json`.
- Dönüşüm: git'e iki soru sorulur: "bu dosya izleniyor mu?" ve "son commit'ten beri değişti mi?".
- Neden: tek dosya düzeninde önceki hâl yalnızca git'tedir. Kaydedilmemiş bir hâlin üzerine yazılırsa o hâl hiçbir yerde kalmaz.
- Sonraki bloğa: sorun yoksa yazmaya izin; sorun varsa betik açıklamayla durur.

**Blok 2: sürüm numarası (`next_version`, `fingerprint_set`).**
- Aldığı veri: diskteki önceki manifest ve bu çalıştırmada bulunan kilitli dosyalar.
- Dönüşüm: her dosya "kök klasör, yol, parmak izi" üçlüsüne indirilir. Üçlüler ve kilit kalıpları aynıysa numara korunur ve dosyaya dokunulmaz. Farklıysa numara bir artar.
- Neden: numara yalnızca kilitli içerik değişince artmalı. Yalnızca tarih değişti diye artsaydı, değişiklik kaydı boş satırlarla dolardı.
- Çıktı: ekranda `lock_manifest=değişmedi version=6` ya da `lock_manifest=yeni_sürüm version=7`.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):**
- Diskte `{"version": 6, "files": [("/veri", "test.jsonl", "aaaa…")]}` var.
- Yeni taramada aynı üçlü çıktı: sürüm 6 kalır, dosyaya dokunulmaz.
- Yeni taramada `test.jsonl`'in parmak izi `bbbb…` çıktı: dosya yeniden yazılır, `version` 7 olur. Sıradaki iş: karşılaştırma betiği ve değişiklik kaydına satır.

**Gerçek çalışma (ölçüldü, geçici bir git deposunda sahte veriyle):** ilk çalıştırma sürüm 1 verdi. Değişiklik yokken dosyaya dokunulmadı. Veri değişince sürüm 2 oldu. Değiştirilmiş ya da git'e hiç kaydedilmemiş bir dosyanın üzerine yazma denemesi reddedildi.

## `src/evaluation/compare_lock_manifests.py`: git'ten okuma

`--old HEAD:evaluation/lock_manifest.json`, manifestin son commit'teki hâlini okur. `HEAD`, "son commit" demektir.
Böylece yeni sürüm diske yazıldıktan sonra, eskisiyle karşılaştırmak için ayrı bir kopya gerekmez.
v1–v5 de aynı yolla okunur: `--old 518aa58:degerlendirme/kilit_manifesti_v4.json`.

**Üç cümlelik özet:** Projede her kaydın tek bir güncel dosyası var; eski hâller git'te. Betikler kaydedilmemiş bir dosyanın üzerine yazmayı reddeder; kilit manifestinin sürümü de yalnızca kilitli içerik değişince artar. Eski bir sürümü görmek için `git show <commit>:<yol>` yeter, ama bunun için proje `.git` klasörüyle birlikte taşınmalıdır.

**Kontrol sorusu:** Manifesti yeniden ürettin ama commit etmeden betiği bir kez daha çalıştırdın. Ne olur, neden?
*Cevap:* Betik durur: "son commit'ten sonra değişmiş … önce commit edin". İlk çalıştırmanın ürettiği sürüm henüz git'te değildir. Üzerine yazılsaydı o sürüm hiçbir yerde kalmazdı.
