"""
Ne yapar:
    İki kilit manifestini karşılaştırır ve aralarında neyin değiştiğini yazar.
    Kilit manifesti, kilitli dosyaların "parmak izlerini" (SHA-256 özetlerini) tutan listedir.
    Her dosya dört gruptan birine girer: eklendi, çıkarıldı, parmak izi değişti, aynı kaldı.

Neden var:
    Manifestin yeni bir sürümü çıktığında, iki dosyaya bakarak neyin değiştiğini anlamak zordur.
    İçlerinde yalnızca 64 karakterlik özetler vardır. Bu betik farkı tek bakışta okunur hâle getirir.
    Sonuç, evaluation/lock_manifest_changelog.md dosyasındaki değişiklik kaydına yazılır.

Neden güvenli:
    Betik yalnızca manifest dosyalarını okur. Kilitli dosyaların kendisini hiç açmaz.
    Ekrana yalnızca dosyanın yerini ve parmak izinin ilk 12 karakterini yazar.
    12 karakter, iki parmak izinin aynı mı farklı mı olduğunu görmeye yeter.

Nasıl çalıştırılır (terminalde, proje klasöründeyken):
    python -m src.evaluation.compare_lock_manifests \\
        --old HEAD:evaluation/lock_manifest.json \\
        --new evaluation/lock_manifest.json \\
        --path-migration evaluation/path_migration.json

    --old: eski manifest. Bir dosya yolu ya da git'teki bir sürüm olabilir.
           Git sürümü "<commit>:<yol>" biçiminde yazılır. Örnek: HEAD:evaluation/lock_manifest.json
           (HEAD, son commit demektir.) Kilit manifesti tek bir dosya olduğu için eski sürümü yalnızca git'tedir.
    --new: yeni manifest. Aynı biçimde; çoğunlukla diskteki güncel dosya.
    --path-migration: taşınan dosyaların "eski yol → yeni yol" listeleri (bir veya birkaç dosya).
    --focus-patterns: ayrıca özetlenecek dosyaların yer kalıpları. Varsayılan: test ve tuzak dosyaları.
    --output: sonucun ayrıca JSON olarak yazılacağı yer (isteğe bağlı).

Eski ve yeni manifestler:
    v1 ile v5 arasındaki manifestlerde alan adları Türkçedir ("yol", "kilitli" gibi).
    v6'dan itibaren İngilizcedir ("path", "locked" gibi). Betik ikisini de okur.
    Çeviri tablosu src/data/build_input_manifest.py içindeki LEGACY_FIELD_NAMES sözlüğüdür.

Taşınan dosyalar:
    Bir dosya iki sürüm arasında başka bir yere taşınmış olabilir.
    Örneğin 02. aşamada inceleme/genel_kontrol_v2_taslak.jsonl, evaluation/held_out/ altına taşınacak.
    Betik, yol taşıma listesine bakarak eski ve yeni yerin aynı dosya olduğunu anlar.
    Böylece taşınan dosya "çıkarıldı ve eklendi" diye değil, "taşındı" diye yazılır.

Eski sürümleri karşılaştırmak:
    v1–v5 yalnızca git geçmişindedir; commit'leri ve yolları evaluation/lock_manifest_changelog.md tablosundadır.
    Örnek: --old 518aa58:degerlendirme/kilit_manifesti_v4.json --new 35f1a69:degerlendirme/kilit_manifesti_v5.json
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path

from src.data.build_input_manifest import LEGACY_FIELD_NAMES

# Proje klasörü. Bu dosya src/evaluation/ içinde olduğu için iki üst klasör yukarıdadır.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Ekrana yazılan parmak izi uzunluğu.
# 12 karakterde iki farklı dosyanın şans eseri aynı görünmesi pratikte imkânsızdır.
SHORT_SHA256_LENGTH = 12

# Varsayılan olarak ayrıca özetlenen dosyalar: test ve tuzak soruları.
# Kalıplar, veri klasörünün içindeki yere göre yazılır. Yıldız (*) "bu klasördeki bütün dosyalar" demektir.
DEFAULT_FOCUS_PATTERNS = [
    "degerlendirme/test.jsonl",
    "degerlendirme/tuzak_sorular.jsonl",
    "05_tuzak_sorular/*",
]


def rename_legacy_keys(value):
    """
    Ne yapar:
        Eski manifestteki Türkçe alan adlarını bugünkü İngilizce adlara çevirir.

    Neden var:
        v1–v5 manifestleri "yol", "kilitli" gibi Türkçe adlar kullanır; v6 "path", "locked" kullanır.
        Karşılaştırmadan önce iki manifest aynı dili konuşmalı. Yoksa hiçbir dosya eşleşmez.

    Ne alır:
        value: Manifestten okunmuş bir değer (sözlük, liste ya da düz değer).
               Örnek: {"yol": "test.jsonl", "kilitli": True}

    Ne döndürür:
        Adları çevrilmiş aynı yapı. Örnek: {"path": "test.jsonl", "locked": True}

    Nasıl çalışır:
        İç içe sözlük ve listelerde kendini tekrar çağırarak her katmandaki adı çevirir.
        Tabloda olmayan adlar olduğu gibi kalır.
    """
    if isinstance(value, dict):
        return {LEGACY_FIELD_NAMES.get(key, key): rename_legacy_keys(item) for key, item in value.items()}
    if isinstance(value, list):
        return [rename_legacy_keys(item) for item in value]
    return value


def load_path_migrations(migration_paths: list[Path]) -> dict[str, str]:
    """
    Ne yapar:
        Taşınan dosyaların "eski yol → yeni yol" listelerini okur ve tek bir tabloda birleştirir.

    Neden var:
        Bir dosya taşındığında eski ve yeni yolunun aynı dosya olduğunu betiğin bilmesi gerekir.
        Bu tablo olmasaydı taşınan her dosya "çıkarıldı" ve "eklendi" diye iki kez yanlış yazılırdı.

    Ne alır:
        migration_paths: Taşıma listelerinin yolları. İki biçim okunur:
                         taşıma manifesti ({"files": [{"old_path": ..., "new_path": ...}]})
                         ve elle yazılmış eşleme ([["eski", "yeni"], ...]).
                         Örnek: [Path("evaluation/path_migration.json")]

    Ne döndürür:
        Proje köküne göre yazılmış yollarla bir tablo.
        Örnek: {"inceleme/genel_kontrol_v2_taslak.jsonl": "evaluation/held_out/general_control_v2.jsonl"}
    """
    migrations: dict[str, str] = {}
    for migration_path in migration_paths:
        data = json.loads(migration_path.read_text(encoding="utf-8"))
        # Taşıma manifesti bir sözlüktür ve kayıtlar "files" altındadır.
        # Elle yazılan eşleme ise doğrudan [eski, yeni] çiftlerinden oluşan bir listedir.
        if isinstance(data, dict):
            pairs = [(record["old_path"], record["new_path"]) for record in data["files"]]
        else:
            pairs = [(pair[0], pair[1]) for pair in data]
        for old_path, new_path in pairs:
            migrations[old_path] = new_path
    return migrations


def follow_migrations(path: str, migrations: dict[str, str]) -> str:
    """
    Ne yapar:
        Bir yolu, taşıma tablosuna göre bugünkü yerine kadar izler.

    Neden var:
        Bir dosya birden fazla kez taşınmış olabilir (örneğin önce adı değişir, sonra başka klasöre gider).
        Tek adım bakmak, dosyayı ara bir yerde bırakır ve eşleşme kaçar.

    Ne alır:
        path: Proje köküne göre yol. Örnek: "inceleme/genel_kontrol_v2_taslak.jsonl"
        migrations: load_path_migrations'ın döndürdüğü tablo.

    Ne döndürür:
        En son yol. Örnek: "evaluation/held_out/general_control_v2.jsonl"
        Yol tabloda yoksa aynen döner.

    Nasıl çalışır:
        Tabloda karşılığı kalmayana kadar "eski → yeni" adımlarını arka arkaya uygular.
        Yanlış yazılmış bir tablo döngüye girerse (a → b → a) bir kez görülen yolda durur.
    """
    seen = {path}
    while path in migrations and migrations[path] not in seen:
        path = migrations[path]
        seen.add(path)
    return path


def read_manifest_text(source: str) -> str:
    """
    Ne yapar:
        Bir manifestin metnini, diskteki bir dosyadan ya da git geçmişindeki bir sürümden okur.

    Neden var:
        Kilit manifesti tek bir dosyadır; her yeni sürüm eskisinin üzerine yazılır.
        Eski sürüm diskte artık yoktur, yalnızca git'te durur. Karşılaştırma için onu git'ten okumak gerekir.

    Ne alır:
        source: Dosya yolu ya da "<commit>:<yol>" biçiminde bir git sürümü.
                Örnek: "evaluation/lock_manifest.json" ya da "HEAD:evaluation/lock_manifest.json"

    Ne döndürür:
        Manifestin JSON metni. Örnek: '{"version": 6, "created_at": "...", ...}'

    Nasıl çalışır:
        Önce diskte böyle bir dosya var mı diye bakılır. Yoksa ve yazı ":" içeriyorsa, git'e "git show" ile sorulur.
        Komut proje klasöründe çalışır; böylece yollar proje köküne göre yazılabilir.
        İkisi de olmazsa betik açıklamayla durur.
    """
    path = Path(source)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    if ":" in source:
        shown = subprocess.run(["git", "-C", str(PROJECT_ROOT), "show", source], capture_output=True)
        if shown.returncode == 0:
            return shown.stdout.decode("utf-8")
    raise SystemExit(f"Manifest bulunamadı (ne diskte ne git'te): {source}")


def load_manifest(source: str) -> dict:
    """
    Ne yapar:
        Bir kilit manifestini okur ve alan adlarını İngilizceye çevirir.

    Neden var:
        Eski ve yeni manifestler aynı biçime getirilmeden karşılaştırılamaz.

    Ne alır:
        source: Dosya yolu ya da git sürümü. Örnek: "HEAD:evaluation/lock_manifest.json"

    Ne döndürür:
        Manifest sözlüğü. Örnek: {"version": 6, "created_at": "2026-11-25T15:09:17+03:00", "patterns": [...], "files": [...]}
        v1–v5 gibi sürüm alanı olmayan eski manifestlerde "version" anahtarı bulunmaz.
    """
    return rename_legacy_keys(json.loads(read_manifest_text(source)))


def file_key(record: dict, migrations: dict[str, str]) -> str:
    """
    Ne yapar:
        Bir manifest kaydı için, iki sürümde de aynı kalan bir "kimlik" yolu üretir.

    Neden var:
        Manifest yolu iki parçada tutar: kök klasör ("root") ve kökün içindeki yer ("path").
        Proje içindeki bir dosya taşındığında kök değişebilir. Karşılaştırma tek bir tam yol üzerinden yapılmalı.

    Ne alır:
        record: Manifestteki bir dosya kaydı.
                Örnek: {"root": "/home/aipc/Desktop/Projeler/kurum-qa-finetune/inceleme",
                        "path": "genel_kontrol_v2_taslak.jsonl", "sha256": "..."}
        migrations: load_path_migrations'ın döndürdüğü tablo.

    Ne döndürür:
        Proje içindeki dosyalar için proje köküne göre bugünkü yol, ötekiler için tam yol.
        Örnek: "inceleme/genel_kontrol_v2_taslak.jsonl" ya da
               "/home/aipc/Desktop/Gruplu Veriler/degerlendirme/test.jsonl"

    Nasıl çalışır:
        Kök ile yer birleştirilir. Dosya proje klasörünün içindeyse proje köküne göre yazılır
        ve taşıma tablosu uygulanır. Taşıma tablosu proje içindeki yollarla yazıldığı için
        dış veri klasörlerine uygulanmaz; zaten onlar salt okunurdur ve taşınmaz.
    """
    full_path = Path(record["root"]) / record["path"]
    if full_path.is_relative_to(PROJECT_ROOT):
        return follow_migrations(full_path.relative_to(PROJECT_ROOT).as_posix(), migrations)
    return full_path.as_posix()


def display_path(record: dict) -> str:
    """
    Ne yapar:
        Bir dosyanın ekranda gösterilecek kısa yolunu üretir.

    Neden var:
        Tam yollar uzundur ve okumayı zorlaştırır. Kök klasörün yalnızca son adı yeterlidir.

    Ne alır:
        record: Manifestteki bir dosya kaydı.
                Örnek: {"root": "/home/aipc/Desktop/Gruplu Veriler", "path": "degerlendirme/test.jsonl"}

    Ne döndürür:
        Kısa yol. Örnek: "Gruplu Veriler/degerlendirme/test.jsonl"
    """
    full_path = Path(record["root"]) / record["path"]
    if full_path.is_relative_to(PROJECT_ROOT):
        return full_path.relative_to(PROJECT_ROOT).as_posix()
    return f"{Path(record['root']).name}/{record['path']}"


def short(sha256: str) -> str:
    """
    Ne yapar:
        Bir parmak izinin yalnızca ilk 12 karakterini alır.

    Neden var:
        64 karakterlik tam parmak izi ekranda okunmaz. İki parmak izinin aynı mı farklı mı
        olduğunu görmek için baştaki 12 karakter yeter.

    Ne alır:
        sha256: Tam parmak izi. Örnek: "3a7bd3e2360a3d29eea436fcfb7e44c7..."

    Ne döndürür:
        Kısa parmak izi. Örnek: "3a7bd3e2360a"
    """
    return sha256[:SHORT_SHA256_LENGTH]


def compare_manifests(old_manifest: dict, new_manifest: dict, migrations: dict[str, str],
                      focus_patterns: list[str]) -> dict:
    """
    Ne yapar:
        İki manifestteki kilitli dosyaları eşleştirir ve her birini dört gruptan birine koyar.

    Neden var:
        Bu, betiğin asıl işidir. Diğer fonksiyonlar bu karşılaştırmayı mümkün kılmak için var.

    Ne alır:
        old_manifest: load_manifest ile okunmuş eski manifest.
        new_manifest: load_manifest ile okunmuş yeni manifest.
        migrations: Taşıma tablosu. Örnek: {"inceleme/a.jsonl": "evaluation/held_out/a.jsonl"}
        focus_patterns: Ayrıca özetlenecek dosyaların kalıpları. Örnek: ["degerlendirme/test.jsonl"]

    Ne döndürür:
        Sonuç sözlüğü. Örnek (kısaltılmış):
        {"added": [{"path": "fine_tuneVeriler/01_sss/a.jsonl", "new_sha256": "3a7bd3e2360a"}],
         "removed": [], "changed": [...], "unchanged": [...],
         "patterns_added": ["01_sss/*"], "patterns_removed": [],
         "focus": {"file_count": 4, "unchanged_count": 4, "all_unchanged": true}}

    Nasıl çalışır:
        Her kaydın kimlik yolu file_key ile çıkarılır. İki manifestte de bulunan kimlikler
        parmak izine göre "değişti" ya da "aynı kaldı" olur; yalnızca birinde bulunanlar
        "eklendi" ya da "çıkarıldı" olur. Eski ve yeni yer farklıysa kayda "old_path" de eklenir.
    """
    old_files = {file_key(record, migrations): record for record in old_manifest["files"]}
    new_files = {file_key(record, migrations): record for record in new_manifest["files"]}

    result = {"added": [], "removed": [], "changed": [], "unchanged": []}
    for key in sorted(old_files.keys() | new_files.keys()):
        old_record = old_files.get(key)
        new_record = new_files.get(key)
        if old_record is None:
            result["added"].append({"path": display_path(new_record), "new_sha256": short(new_record["sha256"])})
            continue
        if new_record is None:
            result["removed"].append({"path": display_path(old_record), "old_sha256": short(old_record["sha256"])})
            continue
        entry = {"path": display_path(new_record),
                 "old_sha256": short(old_record["sha256"]),
                 "new_sha256": short(new_record["sha256"])}
        # Dosya taşınmışsa eski yerini de yaz; okuyan kişi taşımayı görebilsin.
        if display_path(old_record) != display_path(new_record):
            entry["old_path"] = display_path(old_record)
        group = "unchanged" if old_record["sha256"] == new_record["sha256"] else "changed"
        result[group].append(entry)

    # Kilitleme kalıplarındaki farkı da yaz. Yeni bir kalıp, yeni bir dosya grubunun kilitlendiği anlamına gelir.
    old_patterns = old_manifest.get("patterns", [])
    new_patterns = new_manifest.get("patterns", [])
    result["patterns_added"] = [pattern for pattern in new_patterns if pattern not in old_patterns]
    result["patterns_removed"] = [pattern for pattern in old_patterns if pattern not in new_patterns]

    # Test ve tuzak dosyaları için ayrı bir özet çıkar.
    # Bu dosyalar bütün proje boyunca hiç değişmemeli; özet bunu tek satırda gösterir.
    focus_records = [record for record in old_manifest["files"] + new_manifest["files"]
                     if any(fnmatch.fnmatch(record["path"], pattern) for pattern in focus_patterns)]
    focus_keys = {file_key(record, migrations) for record in focus_records}
    unchanged_keys = {key for key in focus_keys
                      if key in old_files and key in new_files
                      and old_files[key]["sha256"] == new_files[key]["sha256"]}
    result["focus"] = {"patterns": focus_patterns,
                       "file_count": len(focus_keys),
                       "unchanged_count": len(unchanged_keys),
                       "all_unchanged": len(focus_keys) > 0 and focus_keys == unchanged_keys}
    return result


def format_header(label: str, source: str, manifest: dict) -> str:
    """
    Ne yapar:
        Raporun başındaki "eski" ya da "yeni" satırını yazar: kaynak, sürüm numarası, tarih ve dosya sayısı.

    Neden var:
        Okuyan kişi neyin neyle karşılaştırıldığını ilk iki satırda görmeli.

    Ne alır:
        label: Satırın etiketi. Örnek: "eski"
        source: Manifestin dosya yolu ya da git sürümü. Örnek: "HEAD:evaluation/lock_manifest.json"
        manifest: Okunmuş manifest. Örnek: {"version": 6, "created_at": "2026-11-25T15:09:17+03:00", "files": [...]}

    Ne döndürür:
        Tek satırlık metin.
        Örnek: "eski: HEAD:evaluation/lock_manifest.json (sürüm 6, 2026-11-25T15:09:17+03:00, 27 dosya)"

    Nasıl çalışır:
        v1–v5'te sürüm alanı yoktur. Onlar için "sürüm ?" yazılır; numara değişiklik kaydından okunur.
    """
    return (f"{label}: {source} (sürüm {manifest.get('version', '?')}, "
            f"{manifest.get('created_at', '?')}, {len(manifest['files'])} dosya)")


def format_report(old_source: str, new_source: str, old_manifest: dict, new_manifest: dict, result: dict) -> str:
    """
    Ne yapar:
        Karşılaştırma sonucunu insanın okuyacağı düz metne çevirir.

    Neden var:
        JSON çıktısı betikler için uygundur; terminalde bakan kişi için sade bir liste gerekir.

    Ne alır:
        old_source, new_source: Karşılaştırılan manifestlerin dosya yolu ya da git sürümü.
                                Örnek: "HEAD:evaluation/lock_manifest.json"
        old_manifest, new_manifest: Okunmuş manifestler (sürüm numarasını ve oluşturulma tarihini göstermek için).
        result: compare_manifests'ın döndürdüğü sözlük.

    Ne döndürür:
        Çok satırlı metin. Örnek:
        "eski: HEAD:evaluation/lock_manifest.json (sürüm 6, 2026-11-25T15:09:17+03:00, 27 dosya)
         ...
         özet: eklendi=0 çıkarıldı=0 değişti=0 aynı=27"
    """
    lines = [format_header("eski", old_source, old_manifest), format_header("yeni", new_source, new_manifest)]
    titles = {"added": "eklendi", "removed": "çıkarıldı", "changed": "parmak izi değişti", "unchanged": "aynı kaldı"}
    for group, title in titles.items():
        lines.append(f"{title} ({len(result[group])}):")
        for entry in result[group]:
            moved = f"  (taşındı; eski yer: {entry['old_path']})" if "old_path" in entry else ""
            fingerprints = " → ".join(entry[name] for name in ("old_sha256", "new_sha256") if name in entry)
            lines.append(f"  {entry['path']}  {fingerprints}{moved}")
    if result["patterns_added"] or result["patterns_removed"]:
        lines.append(f"kilit kalıbı eklendi: {result['patterns_added']}  çıkarıldı: {result['patterns_removed']}")
    focus = result["focus"]
    lines.append(f"test ve tuzak dosyaları: {focus['unchanged_count']}/{focus['file_count']} aynı"
                 f" (hepsi aynı: {'evet' if focus['all_unchanged'] else 'hayır'})")
    lines.append(f"özet: eklendi={len(result['added'])} çıkarıldı={len(result['removed'])}"
                 f" değişti={len(result['changed'])} aynı={len(result['unchanged'])}")
    return "\n".join(lines)


def main() -> None:
    """
    Ne yapar:
        Terminalde yazılan komutu okur, iki manifesti karşılaştırır ve sonucu ekrana yazar.
        İstenirse sonucu bir JSON dosyasına da yazar.

    Neden var:
        Her yeni manifest sürümünde aynı karşılaştırma, kurum ağında da tek bir komutla tekrarlanabilmeli.

    Ne alır:
        Doğrudan bir değer almaz. Bilgileri terminalde yazılan komuttan okur
        (--old, --new ve diğerleri; dosyanın başındaki açıklamaya bakın).

    Ne döndürür:
        Bir değer döndürmez. Ekrana karşılaştırma listesini basar.
        Örnek son satır: "özet: eklendi=2 çıkarıldı=0 değişti=0 aynı=25"
    """
    # Komuttaki seçenekleri tanımla. Her seçeneğin tek bir İngilizce adı vardır.
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1].strip())
    parser.add_argument("--old", required=True,
                        help="Eski kilit manifesti: dosya yolu ya da <commit>:<yol> (örnek: HEAD:evaluation/lock_manifest.json)")
    parser.add_argument("--new", required=True, help="Yeni kilit manifesti: dosya yolu ya da <commit>:<yol>")
    parser.add_argument("--path-migration", nargs="*", default=[], type=Path,
                        help="Taşınan dosyaların eski yol → yeni yol listeleri")
    parser.add_argument("--focus-patterns", nargs="*", default=DEFAULT_FOCUS_PATTERNS,
                        help="Ayrıca özetlenecek dosyaların yer kalıpları (varsayılan: test ve tuzak)")
    parser.add_argument("--output", type=Path, help="Sonucun ayrıca yazılacağı JSON dosyası")
    arguments = parser.parse_args()

    migrations = load_path_migrations(arguments.path_migration)
    old_manifest = load_manifest(arguments.old)
    new_manifest = load_manifest(arguments.new)

    result = compare_manifests(old_manifest, new_manifest, migrations, arguments.focus_patterns)
    print(format_report(arguments.old, arguments.new, old_manifest, new_manifest, result))

    if arguments.output:
        # Hangi dosyaların karşılaştırıldığını da yaz; JSON tek başına okunduğunda anlaşılsın.
        payload = {"old_manifest": arguments.old, "new_manifest": arguments.new, **result}
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
