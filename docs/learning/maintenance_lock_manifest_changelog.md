# Bakım: kilit manifesti karşılaştırma ve değişiklik kaydı (2026-11-26)

Bu bakım bir aşama değildir. Amaç: manifestin bir sürümünden ötekine neyin, neden değiştiğini okunur kılmak.

## `src/evaluation/compare_lock_manifests.py`

**Yol ve girdi:** `--old` ve `--new` iki kilit manifesti. `--path-migration` taşınan dosyaların "eski yol → yeni yol" listesi (isteğe bağlı). Betik kilitli dosyaları değil, yalnızca bu listeleri okur.

**Blok 1: aynı dile çevirme.**
- Aldığı veri: manifest JSON'u. Eski sürümde `{"yol": ..., "kilitli": ...}`, yenisinde `{"path": ..., "locked": ...}`.
- Dönüşüm: `rename_legacy_keys`, `LEGACY_FIELD_NAMES` sözlüğüyle eski adları yenilere çevirir.
- Neden: iki manifest aynı adları kullanmazsa hiçbir kayıt eşleşmez.
- Sonraki bloğa: aynı biçimde iki manifest.

**Blok 2: her dosyaya kalıcı bir kimlik verme.**
- Aldığı veri: kaydın kök klasörü (`root`) ve kökün içindeki yeri (`path`).
- Dönüşüm: `file_key` ikisini tek yola birleştirir. Dosya projenin içindeyse yolu proje köküne göre yazar ve taşıma listesini uygular (`follow_migrations`).
- Neden: 02'de taslak `inceleme/` altından `evaluation/held_out/` altına taşınacak. Taşıma listesi olmadan bu dosya "çıkarıldı" ve "eklendi" diye iki kez yanlış görünürdü.
- Sonraki bloğa: kimlik → kayıt tabloları.

**Blok 3: gruplama ve özet.**
- Dönüşüm: `compare_manifests` kimlikleri karşılaştırır. Yalnızca yeni manifestte olan "eklendi", yalnızca eskide olan "çıkarıldı" grubuna girer. İkisinde de olan, parmak izi farklıysa "değişti", aynıysa "aynı kaldı" grubuna girer. Kilit kalıplarındaki fark ve test/tuzak dosyalarının özeti ayrıca yazılır.
- Neden: değişiklik kaydındaki her satırın dayanağı bu dört gruptur.
- Çıktı: ekranda kısa liste, istenirse JSON dosyası.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):**
- Eski: `inceleme/taslak.jsonl` (parmak izi `aaaa…`), `veri/test.jsonl` (`bbbb…`).
- Yeni: `evaluation/held_out/general.jsonl` (`aaaa…`), `veri/test.jsonl` (`dddd…`). Taşıma listesi: `inceleme/taslak.jsonl → evaluation/held_out/general.jsonl`.
- Sonuç: `general.jsonl` "aynı kaldı (taşındı)", `test.jsonl` "parmak izi değişti" ve test özeti "0/1 aynı (hepsi aynı: hayır)".

**Gerçek çalışma (ölçüldü):** v1→v6 arasındaki beş ardışık çiftte değişen tek dosya `genel_kontrol_v2` taslağı. v2'de iki dosya eklendi. Test ve tuzak dosyaları her çiftte 7/7 aynı. Ayrıntı: `evaluation/lock_manifest_changelog.md`.

**Üç cümlelik özet:** Parmak izi yalnızca "değişti mi?" sorusunu cevaplar. Bu betik iki manifesti karşılaştırıp neyin eklendiğini, çıkarıldığını, değiştiğini ve aynı kaldığını yazar. "Neden değişti?" sorusunu da değişiklik kaydı tablosu cevaplar.

**Kontrol sorusu:** 02'de taslak taşındıktan sonra betiği `--path-migration` vermeden çalıştırırsak ne görürüz?
*Cevap:* Taslak "çıkarıldı" ve yeni yolu "eklendi" diye iki ayrı satırda görünür. İçerik aynı olsa bile betik bunun aynı dosya olduğunu bilemez. Taşıma listesi verilince tek satırda "aynı kaldı (taşındı)" olur.
