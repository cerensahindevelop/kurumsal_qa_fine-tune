"""
Ne yapar:
    Veri klasörlerindeki her dosyanın "parmak izini" çıkarır ve bir listeye yazar.
    Bu parmak izine SHA-256 özeti denir. 64 karakterlik bir harf ve rakam dizisidir.
    Dosyada tek bir harf değişse bile parmak izi tamamen değişir.

Neden var:
    Bazı veri dosyaları kilitlidir: test soruları, tuzak sorular ve Türkçe değerlendirme soruları.
    Bu dosyalar proje sonuna kadar hiç değişmemeli ve kimse içlerini okumamalı.
    Bu betik, kilitli dosyaların bugünkü parmak izlerini ayrı bir dosyaya yazar.
    Bu dosyaya kilit manifesti denir. Manifest, "içinde ne olduğunu gösteren liste" demektir.
    Proje sonunda parmak izleri yeniden çıkarılır ve bu listeyle karşılaştırılır.
    Aynıysa dosyalara kimsenin dokunmadığı kanıtlanmış olur.

Neden güvenli:
    Betik dosyaların içeriğini hiçbir zaman ekrana yazmaz.
    Yalnızca dosyanın yerini, boyutunu, satır sayısını ve parmak izini yazar.
    Bu yüzden kilitli dosyalara dokunmasına izin verilen az sayıdaki betikten biridir.

Nasıl çalıştırılır (terminalde, proje klasöründeyken):
    python -m src.data.build_input_manifest \\
        --input "/home/aipc/Desktop/Gruplu Veriler" /home/aipc/Desktop/fine_tuneVeriler \\
        --extra-locked inceleme/genel_kontrol_v2_taslak.jsonl \\
        --output env/input_sha256.json \\
        --lock-manifest-output evaluation/lock_manifest.json

    --input: taranacak veri klasörleri.
    --extra-locked: bu klasörlerin dışında olup yine de kilitlenecek dosyalar.
    --output: bütün dosyaların listesinin yazılacağı yer.
    --lock-manifest-output: yalnızca kilitli dosyaların listesinin yazılacağı yer.

Tek dosya, sürüm numarası içeride:
    Her iki liste de tek bir güncel dosyadır; her çalıştırmada üzerine yazılır.
    Eski hâller git geçmişinde saklanır. Bu yüzden betik, git'e kaydedilmemiş bir dosyanın üzerine yazmaz.
    Kilit manifestinin sürüm numarası dosyanın içindeki "version" alanındadır.
    Numara yalnızca kilitli bir dosya ya da kilit kalıbı değişince bir artar.
    Hiçbir şey değişmediyse kilit manifesti olduğu gibi bırakılır.
    Numara artınca evaluation/lock_manifest_changelog.md tablosuna yeni bir satır eklenir.

Eski listeler:
    Eski sürümler (kilit manifesti v1–v5 ve girdi listeleri) git geçmişindedir. Hangi commit'te
    ve hangi yolda oldukları evaluation/lock_manifest_changelog.md tablosunda yazar.
    Örnek: git show 35f1a69:degerlendirme/kilit_manifesti_v5.json
    O sürümlerde alan adları Türkçedir. Örneğin "yol" bugün "path" olarak yazılıyor.
    Eski ve yeni adların karşılığı aşağıdaki LEGACY_FIELD_NAMES listesindedir.
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import hashlib
import json
import subprocess
from pathlib import Path

# Kilitli sayılan dosyaların yer kalıpları.
# Yıldız (*) "bu klasördeki bütün dosyalar" anlamına gelir.
# Kalıplar, veri klasörünün içindeki yere göre yazılır.
# Bu adlar proje dışındaki gerçek veri klasörlerine aittir; projenin kendi klasörleriyle karıştırılmamalı.
DEFAULT_LOCKED_PATTERNS = [
    "degerlendirme/test.jsonl",
    "degerlendirme/tuzak_sorular.jsonl",
    "degerlendirme/Türkçe Değerlendirme/*",
    "05_tuzak_sorular/*",
    "06_genel_turkce/degerlendirme/*",
    "01_sss/*",  # Ham sıkça sorulan sorular. Test soruları buradan seçildiği için bunlar da kilitli.
]

# Satırları sayılacak dosya türleri.
# Yalnızca metin dosyalarında satır saymak anlamlıdır.
# PDF gibi dosyalar satırlardan oluşmadığı için sayılmaz.
LINE_COUNTED_SUFFIXES = {".jsonl", ".csv", ".txt", ".md", ".py"}

# Eski listelerdeki (git geçmişindeki kilit manifesti v1–v5 ve girdi listeleri) Türkçe alan adlarının bugünkü karşılıkları.
# Eski bir listeyi okuyacak bir betik, adları bu tabloyla çevirir.
LEGACY_FIELD_NAMES = {
    "olusturma": "created_at",
    "desenler": "patterns",
    "dosyalar": "files",
    "kok": "root",
    "yol": "path",
    "bayt": "bytes",
    "satir": "lines",
    "sha256": "sha256",
    "kilitli": "locked",
}


def compute_sha256(path: Path, chunk_size: int = 1 << 20) -> str:
    """
    Ne yapar:
        Bir dosyanın parmak izini (SHA-256 özetini) çıkarır.

    Neden var:
        Dosyada tek bir harf bile değişse parmak izi tamamen değişir.
        Böylece kilitli dosyalara kimsenin dokunmadığını, içlerini açmadan kanıtlayabiliriz.

    Ne alır:
        path: Parmak izi çıkarılacak dosyanın yeri.
              Örnek: "evaluation/dev_out_of_scope_v1.jsonl"
        chunk_size: Dosyadan her seferinde okunacak parçanın büyüklüğü.
                    Varsayılan değer 1 megabayttır; çoğu zaman değiştirmeye gerek yoktur.

    Ne döndürür:
        Parmak izi metni. Örnek: "3a7bd3e2360a3d29eea436fcfb7e44c7..."

    Nasıl çalışır:
        Dosyayı tek seferde değil, 1 megabaytlık parçalar hâlinde okur.
        Her parça okundukça parmak izi hesabına eklenir.
        Böylece çok büyük dosyalarda bile bilgisayarın belleği dolmaz.
    """
    hasher = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def count_lines(path: Path) -> int:
    """
    Ne yapar:
        Bir dosyada kaç satır olduğunu sayar.

    Neden var:
        Veri dosyalarımızın çoğu JSONL biçimindedir.
        JSONL'de her satır bir kayıttır; örneğin bir soru ve cevabı.
        Satır sayısı, dosyada beklenen sayıda kayıt olup olmadığını gösterir.
        Bunu yaparken satırların içeriğine bakmaz; yalnızca sayar.

    Ne alır:
        path: Satırları sayılacak dosyanın yeri.
              Örnek: "evaluation/dev_out_of_scope_v1.jsonl"

    Ne döndürür:
        Satır sayısı. Örnek: 15
    """
    with path.open("rb") as file:
        return sum(1 for _ in file)


def build_file_record(path: Path, root: Path, relative_path: str, locked: bool) -> dict:
    """
    Ne yapar:
        Tek bir dosya için listeye yazılacak bilgi satırını hazırlar.
        Bu satırda dosyanın yeri, boyutu, satır sayısı, parmak izi ve kilitli olup olmadığı bulunur.

    Neden var:
        Listeye dosyalar iki yoldan girer: veri klasörü taranarak ya da tek tek eklenerek.
        İki yoldan gelen dosyaların bilgisi tam olarak aynı biçimde yazılmalı.
        Bu fonksiyon olmasaydı aynı bilgiyi iki ayrı yerde hazırlamak gerekirdi ve ikisi zamanla farklılaşabilirdi.

    Ne alır:
        path: Dosyanın tam yeri. Örnek: "/home/aipc/Desktop/Gruplu Veriler/degerlendirme/test.jsonl"
        root: Dosyanın bağlı olduğu veri klasörü. Örnek: "/home/aipc/Desktop/Gruplu Veriler"
        relative_path: Dosyanın bu klasörün içindeki yeri. Örnek: "degerlendirme/test.jsonl"
        locked: Dosya kilitli mi? Örnek: True

    Ne döndürür:
        Bilgi satırı. Örnek:
        {"root": "/home/aipc/Desktop/Gruplu Veriler", "path": "degerlendirme/test.jsonl",
         "bytes": 51234, "lines": 100, "sha256": "9f2c...", "locked": True}
        "bytes" dosyanın büyüklüğüdür. Metin dosyası değilse "lines" boş (None) kalır.
    """
    return {
        "root": str(root),
        "path": relative_path,
        "bytes": path.stat().st_size,
        "lines": count_lines(path) if path.suffix.lower() in LINE_COUNTED_SUFFIXES else None,
        "sha256": compute_sha256(path),
        "locked": locked,
    }


def scan_root(root: Path, locked_patterns: list[str]) -> list[dict]:
    """
    Ne yapar:
        Bir veri klasöründeki bütün dosyaları, alt klasörler dahil, tek tek gezer.
        Her dosya için bir bilgi satırı hazırlar.

    Neden var:
        Veri klasörlerinde yüzlerce dosya var. Bunları elle listelemek hem yavaş hem de hataya açık olurdu.

    Ne alır:
        root: Taranacak veri klasörü. Örnek: "/home/aipc/Desktop/Gruplu Veriler"
        locked_patterns: Kilitli dosyaların yer kalıpları. Örnek: ["degerlendirme/test.jsonl", "01_sss/*"]

    Ne döndürür:
        Bilgi satırlarının listesi. Her dosya için bir satır.
        Örnek: [{"path": "degerlendirme/test.jsonl", "locked": True, ...}, {"path": "gercek_sss/egitim_adayi.jsonl", "locked": False, ...}]

    Nasıl çalışır:
        Dosyaları her seferinde alfabetik sırayla gezer.
        Böylece iki ayrı çalıştırmanın listesi aynı sırada çıkar ve satır satır karşılaştırılabilir.
        Bir dosyanın yeri kilitli kalıplardan birine uyuyorsa dosya kilitli sayılır.
    """
    records = []
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        relative_path = path.relative_to(root).as_posix()
        locked = any(fnmatch.fnmatch(relative_path, pattern) for pattern in locked_patterns)
        records.append(build_file_record(path, root, relative_path, locked))
    return records


def ensure_committed(path: Path) -> None:
    """
    Ne yapar:
        Bir dosyanın üzerine yazılmadan önce, şu anki hâlinin git'e kaydedilmiş (commit edilmiş) olduğunu kontrol eder.
        Kaydedilmemişse betiği durdurur.

    Neden var:
        Projede her kayıt türünün tek bir güncel dosyası vardır. Eski hâller ayrı dosyalarda değil,
        yalnızca git geçmişinde saklanır. Kaydedilmemiş bir hâlin üzerine yazılırsa o hâl hiçbir yerde kalmaz.
        Kilit manifesti için bu, bir sürümün kanıtının kaybolması demektir.

    Ne alır:
        path: Üzerine yazılacak dosya. Örnek: Path("evaluation/lock_manifest.json")

    Ne döndürür:
        Bir değer döndürmez. Sorun yoksa sessizce biter; sorun varsa açıklamayla betiği durdurur.

    Nasıl çalışır:
        Dosya hiç yoksa kaybolacak bir şey de yoktur; kontrol geçer.
        Varsa git'e iki soru sorulur: "bu dosya izleniyor mu?" ve "son commit'ten beri değişti mi?".
        Dosyanın bulunduğu klasörde git yoksa (örneğin geçici bir deneme klasörü) kontrol yapılamaz ve betik durur.
    """
    if not path.exists():
        return
    folder = path.resolve().parent
    tracked = subprocess.run(["git", "-C", str(folder), "ls-files", "--error-unmatch", path.resolve().name],
                             capture_output=True)
    if tracked.returncode != 0:
        raise SystemExit(f"{path} git'e kaydedilmemiş. Önceki hâli kaybolmasın diye üzerine yazılmadı. "
                         "Önce commit edin.")
    changed = subprocess.run(["git", "-C", str(folder), "diff", "--quiet", "HEAD", "--", path.resolve().name])
    if changed.returncode != 0:
        raise SystemExit(f"{path} son commit'ten sonra değişmiş. Önceki hâli kaybolmasın diye üzerine yazılmadı. "
                         "Önce commit edin.")


def fingerprint_set(records: list[dict]) -> set[tuple[str, str, str]]:
    """
    Ne yapar:
        Manifestteki dosya kayıtlarını "kök klasör, yol, parmak izi" üçlülerinden oluşan bir kümeye çevirir.

    Neden var:
        İki manifestin aynı dosyaları aynı parmak izleriyle tutup tutmadığını tek bir karşılaştırmayla görmek için.
        Boyut, satır sayısı ya da kayıtların sırası bu karşılaştırmaya karışmamalı.

    Ne alır:
        records: Dosya kayıtları. Eski Türkçe alan adlı kayıtlar da olabilir.
                 Örnek: [{"kok": "/veri", "yol": "test.jsonl", "sha256": "3a7b...", "kilitli": True}]

    Ne döndürür:
        Üçlülerden oluşan küme. Örnek: {("/veri", "test.jsonl", "3a7b...")}
    """
    converted = [{LEGACY_FIELD_NAMES.get(key, key): value for key, value in record.items()} for record in records]
    return {(record["root"], record["path"], record["sha256"]) for record in converted}


def next_version(previous: dict | None, locked_records: list[dict], patterns: list[str]) -> int:
    """
    Ne yapar:
        Kilit manifestinin yeni sürüm numarasını belirler.

    Neden var:
        Kilit manifesti tek bir dosyadır; sürüm numarası dosyanın içinde "version" alanında durur.
        Numara yalnızca kilitli bir dosya ya da kilit kalıbı değiştiğinde artmalıdır.
        Yalnızca tarih değişti diye artarsa, değişiklik kaydında boş satırlar birikir.

    Ne alır:
        previous: Diskteki önceki manifest. Dosya yoksa None.
                  Örnek: {"version": 6, "created_at": "...", "patterns": [...], "files": [...]}
        locked_records: Bu çalıştırmada bulunan kilitli dosya kayıtları.
                        Örnek: [{"root": "/veri", "path": "test.jsonl", "sha256": "3a7b...", "locked": True}]
        patterns: Bu çalıştırmada kullanılan kilit kalıpları. Örnek: ["degerlendirme/test.jsonl"]

    Ne döndürür:
        Sürüm numarası. Örnek: değişiklik yoksa 6, değişiklik varsa 7, ilk manifestse 1.

    Nasıl çalışır:
        Her dosya "kök klasör, yol ve parmak izi" üçlüsüyle temsil edilir. Önceki ve yeni manifestin üçlüleri
        ile kalıpları aynıysa numara korunur, farklıysa bir artırılır.
        Eski Türkçe alan adlı bir manifest gelirse adlar önce LEGACY_FIELD_NAMES ile çevrilir.
        Önceki manifestte sürüm alanı yoksa numara tahmin edilmez; betik durur.
    """
    if previous is None:
        return 1
    previous = {LEGACY_FIELD_NAMES.get(key, key): value for key, value in previous.items()}
    if "version" not in previous:
        raise SystemExit("Önceki kilit manifestinde 'version' alanı yok; sürüm numarası tahmin edilemez.")

    unchanged = (fingerprint_set(previous["files"]) == fingerprint_set(locked_records)
                 and previous.get("patterns") == patterns)
    return previous["version"] if unchanged else previous["version"] + 1


def main() -> None:
    """
    Ne yapar:
        Terminalde yazılan komutu okur, veri klasörlerini tarar ve iki liste dosyası yazar:
        bütün dosyaların listesi ve yalnızca kilitli dosyaların listesi (kilit manifesti).

    Neden var:
        Aynı işlem ileride internetsiz kurum ağında, yardımcı olmadan, tek bir komutla tekrarlanabilmeli.

    Ne alır:
        Doğrudan bir değer almaz. Bilgileri terminalde yazılan komuttan okur
        (--input, --output ve diğerleri; dosyanın başındaki açıklamaya bakın).

    Ne döndürür:
        Bir değer döndürmez. Dosyaları diske yazar ve ekrana kısa bir sayım basar.
        Örnek ekran çıktısı: "files=506 locked=27 output=env/input_sha256.json lock_manifest=değişmedi version=6"
    """
    # Komuttaki seçenekleri tanımla. Her seçeneğin tek bir İngilizce adı vardır.
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1].strip())
    parser.add_argument("--input", nargs="+", required=True, type=Path,
                        help="Taranacak veri klasörleri")
    parser.add_argument("--output", required=True, type=Path,
                        help="Bütün dosyaların listesinin yazılacağı yer")
    parser.add_argument("--lock-manifest-output", type=Path,
                        help="Yalnızca kilitli dosyaların listesinin (kilit manifestinin) yazılacağı yer")
    parser.add_argument("--locked-patterns", nargs="*",
                        default=DEFAULT_LOCKED_PATTERNS, help="Kilitli dosyaların yer kalıpları")
    parser.add_argument("--extra-locked", nargs="*", default=[], type=Path,
                        help="Veri klasörlerinin dışında olup yine de kilitlenecek dosyalar")
    arguments = parser.parse_args()

    # Listeye oluşturulma zamanını yaz. Böylece listenin ne zaman çıkarıldığı sonradan bilinir.
    created_at = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

    # Önce veri klasörlerini tara.
    # Klasör yoksa hemen dur; eksik bir liste, hiç liste olmamasından daha tehlikelidir.
    records = []
    for root in arguments.input:
        if not root.is_dir():
            raise SystemExit(f"Girdi klasörü yok: {root}")
        records.extend(scan_root(root, arguments.locked_patterns))

    # Sonra tek tek eklenen dosyaları listeye kat. Bunlar her zaman kilitli sayılır.
    # Bu dosyaların bağlı olduğu klasör, dosyanın kendi bulunduğu klasördür.
    for path in arguments.extra_locked:
        if not path.is_file():
            raise SystemExit(f"Ek kilitli dosya yok: {path}")
        path = path.resolve()
        records.append(build_file_record(path, path.parent, path.name, locked=True))

    # Üzerine yazmadan önce iki dosyanın da şu anki hâlinin git'e kaydedilmiş olduğunu kontrol et.
    # Eski sürümler ayrı dosyalarda değil, yalnızca git geçmişinde saklanır.
    # Kaydedilmemiş bir hâlin üzerine yazılırsa o hâl kalıcı olarak kaybolur.
    ensure_committed(arguments.output)
    if arguments.lock_manifest_output:
        ensure_committed(arguments.lock_manifest_output)

    # Bütün dosyaların listesini yaz.
    # ensure_ascii=False ayarı, Türkçe karakterli dosya adlarının (ç, ş, ğ) dosyada okunabilir kalmasını sağlar.
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps({"created_at": created_at, "files": records}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )

    # İstenmişse yalnızca kilitli dosyaların listesini (kilit manifestini) ayrıca yaz.
    # Hangi kalıplarla kilitlendiği de yazılır; böylece liste tek başına anlaşılır.
    locked_records = [record for record in records if record["locked"]]
    lock_message = ""
    if arguments.lock_manifest_output:
        previous = None
        if arguments.lock_manifest_output.exists():
            previous = json.loads(arguments.lock_manifest_output.read_text(encoding="utf-8"))
        version = next_version(previous, locked_records, arguments.locked_patterns)
        if previous is not None and version == previous.get("version"):
            # Kilitli dosyalar ve kalıplar aynı: dosyaya dokunma.
            # Yalnızca tarih değişsin diye yeni bir sürüm üretmek, değişiklik kaydını anlamsız satırlarla doldururdu.
            lock_message = f" lock_manifest=değişmedi version={version}"
        else:
            arguments.lock_manifest_output.parent.mkdir(parents=True, exist_ok=True)
            arguments.lock_manifest_output.write_text(
                json.dumps(
                    {"version": version, "created_at": created_at,
                     "patterns": arguments.locked_patterns, "files": locked_records},
                    ensure_ascii=False,
                    indent=1,
                ),
                encoding="utf-8",
            )
            lock_message = (f" lock_manifest=yeni_sürüm version={version}"
                            " (sıradaki iş: compare_lock_manifests ile karşılaştır ve"
                            " evaluation/lock_manifest_changelog.md tablosuna satır ekle)")

    # Ekrana yalnızca sayıları yaz.
    # Dosya içeriği hiçbir zaman ekrana yazılmaz; kilitli soruların görülmemesi için bu şarttır.
    print(f"files={len(records)} locked={len(locked_records)} output={arguments.output}{lock_message}")


if __name__ == "__main__":
    main()
