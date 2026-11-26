# Bakım: dosya adlarında sürüm eki yok (2026-11-26)

Bu bakım bir aşama değildir. Kural: dosyanın adı ne olduğunu anlatır (`thresholds.md`), kaçıncı sürüm olduğunu anlatmaz (`thresholds_v1.md` değil). Sürüm dosyanın içinde ve git geçmişinde durur.

## Fikir: ad sabit kalınca atıflar kırılmaz

Eski düzende eşik dosyası değişince `thresholds_v2.md` açılacaktı. O zaman bu dosyayı anan her belge, betik ve kural da güncellenmek zorunda kalırdı. Biri unutulursa, o yer sessizce eski sürümü göstermeye devam ederdi.
Yeni düzende ad hiç değişmez. Değişen tek şey dosyanın içindeki "Sürüm" numarası ve "Değişiklik geçmişi" tablosudur.
Onaylanan sürümü kanıtlayan, onay commit'inin kimliğidir. Commit kimliği, git'in o anki hâle verdiği değişmez bir etikettir. O kimlikle `git show <commit>:evaluation/thresholds.md` yazıldığında, onaylanan metnin birebir aynısı görülür.

## Belgelerin yeni başı ve sonu

**Blok 1: en üstte iki satır.**
- Aldığı veri: belge.
- Dönüşüm: başlığın altına "Sürüm: 1" ve "Onaylanan commit: (onay verilince yazılacak)" eklenir.
- Neden: belgeyi açan kişi hangi sürümü okuduğunu ve bu sürümün onaylanıp onaylanmadığını hemen görür.

**Blok 2: en altta "Değişiklik geçmişi".**
- Dönüşüm: tarih, ne değiştiği ve neden değiştiği bir tabloya yazılır.
- Kural: onaydan sonraki her değişiklikte sürüm numarası bir artar ve tabloya bir satır eklenir. Değişiklik raporda da gösterilir.
- Onaydan önceki değişikliklerde sürüm numarası artmadı. Çünkü o zaman hiçbir model puanlanmamıştı. Bu değişikliklerin ayrıntısı `thresholds.md` §8'de durur.

## İki istisna: modelin okuduğu dosya ve veri dosyası

`prompts/system_prompt.txt` modele olduğu gibi verilir. Başına "Sürüm: 1" yazılsaydı model de bu satırı okurdu.
Bu yüzden dosya saf kaldı (proje sahibi kararı 2A). Sürümü ve parmak izi ayrı bir dosyada durur: `prompts/system_prompt_changelog.md`.
Aynı neden `evaluation/dev_out_of_scope.jsonl` için de geçerli: JSONL dosyasında her satır bir kayıttır. Fazladan bir satır dosyayı bozardı. Bu dosyanın sürüm kaydı `experiment_plan.md` Değişiklik geçmişi'ndedir.

## `experiments.csv`: `system_prompt_sha256`

Eski sütun "system_prompt" adını taşıyordu ve oraya bir sürüm adı yazılacaktı. Ama ad, içeriği kanıtlamaz; dosya adı aynı kalıp içerik değişebilir.
Yeni sütuna dosyanın SHA-256 parmak izi yazılır. Parmak izi tek bir harf değişse bile tamamen değişir. Böylece her deneyin hangi metinle yapıldığı kesin olarak kanıtlanır.

**Mini örnek (örnek, uydurma; gerçek çalışma değil):**
- `faq_adapter_run1` satırında `system_prompt_sha256 = aaaa…`.
- Biri prompt'a bir virgül ekledi ve `faq_adapter_run2` koştu: satırda `bbbb…` yazar.
- İki koşu karşılaştırılırken bu fark hemen görülür. Değişiklik kayıttaki tabloyla eşleşmiyorsa, onaysız bir değişiklik yapılmış demektir.

**Gerçek çalışma (ölçüldü, 2026-11-26):** `prompts/system_prompt.txt` 2.977 bayt, SHA-256 `0ecd66614c7f…`. Yeniden adlandırmadan önceki hâliyle aynı (`evaluation/path_migration.json`: 7 taşımanın 2'si içerik aynı; bunlar prompt ve geliştirme seti. Kalan 5'i, başlık ve sürüm satırı eklenen belgeler).

## Deney koşularının adı: `_run<N>`

Aynı deneyin ikinci koşusu ilkinin klasörünün üzerine yazmasın diye adın sonuna bir koşu numarası gelir: `faq_adapter_run1`, `faq_adapter_run2` (proje sahibi kararı 1A).
`v` harfi kullanılmaz, çünkü belge sürümüyle karışırdı. Koşuda neyin değiştiği config dosyasında ve `experiments.csv` notunda yazar.

**Üç cümlelik özet:** Dosya adları artık sürüm taşımıyor; sürüm dosyanın en üstünde, değişiklikler en altta, eski hâller git'te duruyor. Modelin olduğu gibi okuduğu system prompt'a satır eklenmedi; onun sürümü ve parmak izi ayrı bir kayıt dosyasında. Her deney satırı, kullandığı system prompt'u parmak iziyle kanıtlıyor ve koşular `_run1`, `_run2` diye numaralanıyor.

**Kontrol sorusu:** Onaydan sonra 2.1 eşiği değişirse ne yapılır?
*Cevap:* Yeni dosya açılmaz. `evaluation/thresholds.md` içinde "Sürüm: 1" "Sürüm: 2" olur ve Değişiklik geçmişi tablosuna tarih, değişiklik ve gerekçe yazılır. Değişiklik raporda gösterilir. Onaylanmış 1. sürüm, onay commit'inin kimliğiyle git'ten her zaman okunabilir.
