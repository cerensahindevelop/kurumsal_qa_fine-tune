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
        --output env/2026-11-25_input_sha256_v6.json \\
        --lock-manifest-output evaluation/lock_manifest_v6.json

    --input: taranacak veri klasörleri.
    --extra-locked: bu klasörlerin dışında olup yine de kilitlenecek dosyalar.
    --output: bütün dosyaların listesinin yazılacağı yer.
    --lock-manifest-output: yalnızca kilitli dosyaların listesinin yazılacağı yer.

Eski listeler:
    2026-11-25'ten önce üretilen listeler (v1'den v5'e kadar) archive/degerlendirme/ klasöründedir.
    Onlarda alan adları Türkçedir. Örneğin "yol" bugün "path" olarak yazılıyor.
    Eski ve yeni adların karşılığı aşağıdaki LEGACY_FIELD_NAMES listesindedir.
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import hashlib
import json
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

# Eski listelerdeki (archive/degerlendirme/lock_manifest_v1 ile v5 arası) Türkçe alan adlarının bugünkü karşılıkları.
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
        Örnek ekran çıktısı: "files=506 locked=27 output=env/2026-11-25_input_sha256_v6.json"
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
    if arguments.lock_manifest_output:
        arguments.lock_manifest_output.parent.mkdir(parents=True, exist_ok=True)
        arguments.lock_manifest_output.write_text(
            json.dumps(
                {"created_at": created_at, "patterns": arguments.locked_patterns, "files": locked_records},
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )

    # Ekrana yalnızca sayıları yaz.
    # Dosya içeriği hiçbir zaman ekrana yazılmaz; kilitli soruların görülmemesi için bu şarttır.
    print(f"files={len(records)} locked={len(locked_records)} output={arguments.output}")


if __name__ == "__main__":
    main()
