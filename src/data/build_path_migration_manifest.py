"""
Ne yapar:
    Yeri veya adı değiştirilen dosyalar için bir liste yazar: eski yer, yeni yer ve iki yerdeki parmak izi.
    Parmak izi, dosyanın SHA-256 özetidir: 64 karakterlik bir harf ve rakam dizisi.
    Dosyada tek bir harf değişse parmak izi tamamen değişir.

Neden var:
    Bir dosya taşındığında içeriğinin bozulmadığı kanıtlanmalı.
    Bu özellikle kilitli dosyalar ve onay bekleyen belgeler için önemlidir.
    Bu liste, hangi dosyanın yalnızca yer değiştirdiğini, hangisinin içeriğinin de değiştiğini gösterir.

Nasıl çalıştırılır (terminalde, proje klasöründeyken):
    python -m src.data.build_path_migration_manifest \\
        --pair inceleme/genel_kontrol_v2_taslak.jsonl evaluation/held_out/general_control_v2.jsonl \\
        --pair inceleme/genel_kontrol_v2_onay.csv review/general_control_v2_review.csv \\
        --base-ref HEAD \\
        --lock-manifest evaluation/lock_manifest.json \\
        --output evaluation/path_migration.json

    --pair: bir eski yer ve bir yeni yer. Her taşınan dosya için bir kez yazılır.
    --mapping: çift çok olduğunda, çiftlerin yazıldığı bir JSON dosyası ([["eski", "yeni"], ...]).
               --pair ile birlikte de kullanılabilir; en az biri gerekir.
    --base-ref: eski içeriğin okunacağı git kaydı. Git, projenin geçmiş sürümlerini saklayan araçtır;
                her kaydın kısa bir kimliği vardır (örnek: 59aa89e). Bu, taşımadan önceki son kayıt olmalıdır.
    --lock-manifest: hangi dosyaların kilitli olduğunu söyleyen liste (kilit manifesti).
    --output: sonucun yazılacağı dosya.

Tek dosya:
    Sonuç her zaman evaluation/path_migration.json dosyasına yazılır ve yalnızca son taşımayı anlatır.
    Önceki taşımaların kaydı git geçmişindedir. Örnek: 2026-11-25'teki ad değişikliğinin kaydı
    git show 1919cce:evaluation/path_migration_manifest_2026-11-25.json komutuyla görülür.
    Betik, git'e kaydedilmemiş bir çıktının üzerine yazmaz; önceki kayıt kaybolmasın.

Eşleme neden elle yazılır:
    Git dosyaların nereye taşındığını kendisi tahmin edebilir. Ama boş dosyaları ve çok değişmiş
    dosyaları yanlış eşleyebilir. Elle yazılan eşleme, gerçekte neyin nereye gittiğini gösterir.

Neden güvenli:
    Dosyaların içeriği yalnızca parmak izi hesaplamak için okunur; hiçbir yere yazılmaz ve ekrana basılmaz.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from src.data.build_input_manifest import LEGACY_FIELD_NAMES, compute_sha256, ensure_committed


def sha256_at_git_ref(git_ref: str, path: str) -> str | None:
    """
    Ne yapar:
        Bir dosyanın, git geçmişindeki belli bir kayıttaki hâlinin parmak izini çıkarır.

    Neden var:
        Taşınan bir dosyanın eski yeri diskte artık yoktur.
        Eski içerik yalnızca git geçmişinden okunabilir.

    Ne alır:
        git_ref: Git kaydının kimliği. Örnek: "59aa89e"
        path: Dosyanın o kayıttaki yeri. Örnek: "istemler/sistem_v1.txt"

    Ne döndürür:
        Parmak izi metni. Örnek: "0ecd66614c7f4b7d..."
        Dosya o kayıtta yoksa None (boş) döner.
    """
    completed = subprocess.run(["git", "show", f"{git_ref}:{path}"], capture_output=True)
    if completed.returncode != 0:
        return None
    return hashlib.sha256(completed.stdout).hexdigest()


def locked_project_paths(lock_manifest_path: Path) -> set[str]:
    """
    Ne yapar:
        Kilit manifestinden, proje klasörünün içinde duran kilitli dosyaların yerlerini çıkarır.

    Neden var:
        Taşınan bir dosyanın kilitli olup olmadığını bilmemiz gerekir.
        Kilitli bir dosyanın içeriği hiçbir zaman değişmemelidir; liste bunu ayrıca işaretler.

    Ne alır:
        lock_manifest_path: Kilit manifestinin yeri. Örnek: "evaluation/lock_manifest.json"

    Ne döndürür:
        Proje klasörüne göre yerlerin kümesi. Örnek: {"inceleme/genel_kontrol_v2_taslak.jsonl"}

    Nasıl çalışır:
        Hem eski Türkçe alan adlı listeleri (v1'den v5'e) hem yeni İngilizce alan adlı listeleri (v6 ve sonrası) okur.
        Eski adlar önce yeni adlara çevrilir.
        Proje klasörünün dışındaki dosyalar (dış veri klasörleri) atlanır.
    """
    manifest = json.loads(lock_manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files", manifest.get("dosyalar", []))
    project_root = Path.cwd().resolve()
    paths = set()
    for record in files:
        # Eski alan adlarını yeni adlara çevir. Yeni listede bu çeviri hiçbir şeyi değiştirmez.
        record = {LEGACY_FIELD_NAMES.get(key, key): value for key, value in record.items()}
        full_path = Path(record["root"]) / record["path"]
        if full_path.is_relative_to(project_root):
            paths.add(full_path.relative_to(project_root).as_posix())
    return paths


def main() -> None:
    """
    Ne yapar:
        Terminalde yazılan komutu okur. Eşlemedeki her dosya için eski ve yeni parmak izini çıkarır.
        Sonucu dosyaya yazar ve ekrana kısa bir sayım basar.

    Neden var:
        Taşıma işinin kanıtı her zaman aynı komutla yeniden üretilebilsin.

    Ne alır:
        Doğrudan bir değer almaz. Bilgileri terminalde yazılan komuttan okur
        (--pair, --mapping, --base-ref, --lock-manifest, --output).

    Ne döndürür:
        Bir değer döndürmez. Dosyaya her taşınan dosya için bir satır yazar.
        Örnek satır: {"old_path": "istemler/sistem_v1.txt", "new_path": "prompts/system_prompt_v1.txt",
                      "old_sha256": "0ecd...", "new_sha256": "0ecd...", "content_unchanged": true, "locked": false}
        Örnek ekran çıktısı: "files=24 content_unchanged=7 content_changed=17 missing=0 locked=0 locked_changed=0 ..."
    """
    # Komuttaki seçenekleri tanımla. Her seçeneğin tek bir İngilizce adı vardır.
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1].strip())
    parser.add_argument("--pair", nargs=2, action="append", default=[], metavar=("OLD", "NEW"),
                        help="Bir taşınan dosyanın eski ve yeni yeri; her dosya için bir kez yazılır")
    parser.add_argument("--mapping", type=Path, help="Çok sayıda çift için JSON dosyası ([[eski, yeni], ...])")
    parser.add_argument("--base-ref", default="HEAD", help="Eski içeriğin okunacağı git kaydı")
    parser.add_argument("--lock-manifest", type=Path, required=True, help="Kilitli dosyaları gösteren liste")
    parser.add_argument("--output", type=Path, required=True, help="Sonucun yazılacağı dosya (JSON)")
    arguments = parser.parse_args()

    # Eşlemeyi topla: komutta yazılan çiftler ve varsa eşleme dosyasındakiler.
    # Hiç çift yoksa yazılacak bir kanıt da yoktur; boş bir dosya yanlış güven verirdi.
    pairs = [tuple(pair) for pair in arguments.pair]
    if arguments.mapping:
        pairs += [tuple(pair) for pair in json.loads(arguments.mapping.read_text(encoding="utf-8"))]
    if not pairs:
        raise SystemExit("En az bir --pair ya da --mapping verin.")
    ensure_committed(arguments.output)

    # Kilitli dosyaların listesini oku.
    locked_paths = locked_project_paths(arguments.lock_manifest)

    # Her çift için iki parmak izi çıkar: eskisi git geçmişinden, yenisi diskteki dosyadan.
    # İkisi aynıysa dosyanın içeriği taşıma sırasında değişmemiştir.
    records = []
    for old_path, new_path in pairs:
        new_file = Path(new_path)
        old_sha256 = sha256_at_git_ref(arguments.base_ref, old_path)
        new_sha256 = compute_sha256(new_file) if new_file.is_file() else None
        records.append({
            "old_path": old_path,
            "new_path": new_path,
            "old_sha256": old_sha256,
            "new_sha256": new_sha256,
            "content_unchanged": old_sha256 is not None and old_sha256 == new_sha256,
            "locked": old_path in locked_paths or new_path in locked_paths,
        })

    # Sonucu dosyaya yaz.
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps({"base_ref": arguments.base_ref, "lock_manifest": str(arguments.lock_manifest), "files": records},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    # Ekrana yalnızca sayıları yaz.
    # "missing": eski veya yeni yerinde bulunamayan dosya sayısı; sıfır olmalı.
    # "locked_changed": içeriği değişmiş kilitli dosya sayısı; sıfır olmalı.
    missing_count = sum(1 for record in records if record["old_sha256"] is None or record["new_sha256"] is None)
    unchanged_count = sum(record["content_unchanged"] for record in records)
    locked_changed_count = sum(1 for record in records if record["locked"] and not record["content_unchanged"])
    print(f"files={len(records)} content_unchanged={unchanged_count} content_changed={len(records) - unchanged_count - missing_count} "
          f"missing={missing_count} locked={sum(record['locked'] for record in records)} "
          f"locked_changed={locked_changed_count} output={arguments.output}")


if __name__ == "__main__":
    main()
