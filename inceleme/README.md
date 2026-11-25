# inceleme/ (tarihî, taşınmaz)

Yeni insan inceleme kuyrukları `review/` altına yazılır. Bu klasörde yalnızca kilitli `genel_kontrol_v2` taslağı
ve onun onay CSV'si kalır. Kilit manifestleri v2–v5 taslağı bu yolla kaydettiği için dosya taşınmaz.
02'deki çakışma denetiminden sonra taslak `evaluation/held_out/genel_kontrol_v2.jsonl` yoluna taşınır ve
`evaluation/lock_manifest_v7.json` üretilir.

`genel_kontrol_v2_onay.csv` eski Türkçe başlıklarla yazıldı. `python -m src.data.build_review_csv` bu başlıkları
okur ve onayları kayıt `id`'sine göre taşır.
