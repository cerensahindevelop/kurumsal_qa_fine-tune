"""
Ne yapar:
    Asistanın yazdığı taslak soruları, insanın tek tek onaylayacağı bir tabloya (CSV dosyasına) döker.
    CSV, Excel'de açılabilen, virgülle ayrılmış basit bir tablo dosyasıdır.

Neden var:
    Asistanın yazdığı her soru kullanılmadan önce insan tarafından onaylanmalı.
    Taslak değiştiğinde tablo yeniden üretilir.
    Bu sırada insanın daha önce doldurduğu onaylar ve notlar kaybolmamalı.
    Bu betik, eski onayları her kaydın kimliğine bakarak yeni tabloya taşır.

Nasıl çalıştırılır (terminalde, proje klasöründeyken):
    python -m src.data.build_review_csv --input taslak.jsonl --output review/taslak_review.csv

    --input: taslak soruların bulunduğu JSONL dosyası. JSONL'de her satır bir kayıttır.
    --output: yazılacak onay tablosu. Dosya zaten varsa içindeki onaylar korunur.

Ne zaman kullanılmaz:
    Test ve tuzak soruları için kullanılmaz. Bu betik tablonun içine soruların metnini yazar;
    kilitli soruların metni görülmemelidir.

Eski dosyalarla uyum:
    2026-11-25'ten önce tablo başlıkları Türkçeydi (örneğin "onay", "not").
    Betik bu eski başlıkları okuyup yeni İngilizce başlıklara çevirir (LEGACY_CSV_COLUMNS).
    Taslaklardaki eski Türkçe alan adları da okunur (örneğin "grup"; LEGACY_INPUT_FIELDS).

Onay değerleri:
    İnsan onay hücresine "evet", "hayir" veya "duzelt" yazar.
    Sayım yapılırken yazım farkları yok sayılır: "Düzelt", "düzelt" ve "duzelt" aynı sayılır.
    Hücredeki yazım ise hiç değiştirilmez.
    Bu üç değerden biri olmayan bir yazım varsa, o kaydın kimliği ekranda gösterilir.
"""
import argparse
import csv
import json
from pathlib import Path

# İnsanın dolduracağı sütunların başlıkları.
# Parantez içindeki kelimeler, hücreye yazılabilecek değerleri hatırlatır.
APPROVAL = "approval (evet/hayir/duzelt)"
KNOWLEDGE_APPROVAL = "knowledge_items_correct (evet/hayir/duzelt)"
NOTES = "notes"
REVIEWER_COLUMNS = [APPROVAL, KNOWLEDGE_APPROVAL, NOTES]
VALID_LABELS = {"evet", "hayir", "duzelt"}

# Bilgi öğesi olmayan satırlarda bilgi onayı hücresine betik "-" yazar.
# Bu, "burada onaylanacak bir şey yok" demektir. İnsanın doldurduğu bir değer sayılmaz.
NOT_APPLICABLE = "-"

# Eski tablo başlıklarının yeni karşılıkları. Eski tablolardaki onaylar bu eşlemeyle taşınır.
LEGACY_CSV_COLUMNS = {
    "onay (evet/hayir/duzelt)": APPROVAL,
    "bilgi_ogeleri_dogru_mu (evet/hayir/duzelt)": KNOWLEDGE_APPROVAL,
    "not": NOTES,
    "grup": "group",
    "kategori": "category",
    "bilgi_ogeleri": "knowledge_items",
}

# Taslaklardaki yeni alan adlarının eski Türkçe karşılıkları.
# Kilitli taslaklar eski adlarla yazıldı ve değiştirilemez; betik onları da okuyabilmeli.
LEGACY_INPUT_FIELDS = {"group": "grup", "category": "kategori", "knowledge_items": "bilgi_ogeleri"}

# Türkçe harflerin Latin karşılıkları. Onay sayımında "düzelt" ile "duzelt" aynı sayılsın diye kullanılır.
TURKISH_TO_ASCII = str.maketrans({"ı": "i", "İ": "i", "ü": "u", "Ü": "u", "ö": "o", "Ö": "o",
                                  "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g", "ç": "c", "Ç": "c"})


def normalize_label(value: str) -> str:
    """
    Ne yapar:
        Bir onay hücresindeki yazıyı sayım için sadeleştirir.
        Baştaki ve sondaki boşlukları siler, Türkçe harfleri Latin harflerine çevirir, küçük harf yapar.

    Neden var:
        İnsanlar aynı şeyi farklı yazabilir: "Düzelt", "düzelt ", "duzelt".
        Bu fonksiyon olmasaydı bunlar üç ayrı değer sayılır ve onay sayımı bölünürdü.
        Hücredeki asıl yazı değiştirilmez; bu sadeleştirme yalnızca sayarken kullanılır.

    Ne alır:
        value: Hücredeki yazı. Örnek: "Düzelt "

    Ne döndürür:
        Sadeleştirilmiş yazı. Örnek: "duzelt"
    """
    return value.strip().translate(TURKISH_TO_ASCII).lower()


def get_field(record: dict, name: str, default=None):
    """
    Ne yapar:
        Bir kayıttan istenen alanı okur. Alan yeni adıyla yoksa eski Türkçe adıyla arar.

    Neden var:
        Eski taslaklarda alanlar Türkçe adlıdır ("grup"), yenilerde İngilizce ("group").
        Bu fonksiyon sayesinde betik iki tür dosyayı da aynı şekilde okur.

    Ne alır:
        record: Bir taslak kaydı. Örnek: {"id": "GK-1", "grup": "a", "prompt": "Soru?"}
        name: İstenen alanın yeni adı. Örnek: "group"
        default: Alan hiç yoksa döndürülecek değer. Varsayılan: None (boş).

    Ne döndürür:
        Alanın değeri. Örnek: "a"
    """
    if name in record:
        return record[name]
    return record.get(LEGACY_INPUT_FIELDS.get(name, name), default)


def read_existing_reviews(path: Path) -> dict[str, dict]:
    """
    Ne yapar:
        Daha önce doldurulmuş onay tablosunu okur.
        Eski Türkçe başlıkları yeni İngilizce başlıklara çevirir.

    Neden var:
        Tablo yeniden üretildiğinde insanın doldurduğu onaylar kaybolmamalı.
        Onaylar satır sırasına göre değil, kaydın kimliğine göre bulunur.
        Böylece taslağa yeni kayıt eklense bile her onay doğru soruya gider.

    Ne alır:
        path: Onay tablosunun yeri. Örnek: "review/taslak_review.csv"

    Ne döndürür:
        Her kayıt kimliği için o satırın bilgileri. Dosya yoksa boş bir sonuç döner.
        Örnek: {"GK-1": {"id": "GK-1", "approval (evet/hayir/duzelt)": "evet", "notes": "", ...}}
    """
    if not path.exists():
        return {}
    # Excel tabloları kaydederken dosyanın başına görünmez bir işaret ekleyebilir.
    # "utf-8-sig" okuma biçimi bu işareti atar; yoksa ilk başlığın adı bozulurdu.
    with path.open(encoding="utf-8-sig", newline="") as file:
        return {
            row["id"]: {LEGACY_CSV_COLUMNS.get(column, column): value for column, value in row.items()}
            for row in csv.DictReader(file)
        }


def main() -> None:
    """
    Ne yapar:
        Terminalde yazılan komutu okur, taslaktan onay tablosunu yazar.
        Sonra ekrana kaç satırın korunduğunu ve onayların dağılımını yazar.

    Neden var:
        Asistanın yazdığı taslakların insan onayı tek bir tabloda ve her seferinde aynı yolla toplansın.

    Ne alır:
        Doğrudan bir değer almaz. Bilgileri terminalde yazılan komuttan okur (--input ve --output).

    Ne döndürür:
        Bir değer döndürmez. Tabloyu diske yazar ve ekrana kısa bir özet basar.
        Örnek ekran çıktısı:
            "60 satır yazıldı -> review/taslak_review.csv (korunan dolu satır: 60)"
            "approval (evet/hayir/duzelt): {'evet': 59, 'duzelt': 1}"
    """
    # Komuttaki seçenekleri tanımla. Her seçeneğin tek bir İngilizce adı vardır.
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1].strip())
    parser.add_argument("--input", type=Path, required=True, help="Taslak soruların JSONL dosyası")
    parser.add_argument("--output", type=Path, required=True, help="Yazılacak onay tablosu (CSV)")
    arguments = parser.parse_args()

    # Taslak kayıtlarını ve (varsa) eski tablodaki insan onaylarını oku.
    records = [json.loads(line) for line in arguments.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    previous_rows = read_existing_reviews(arguments.output)

    # Tabloyu yaz. Her kayıt bir satırdır.
    # İnsanın doldurduğu sütunlar, eski tablodan kaydın kimliğine göre aynen alınır.
    # "utf-8-sig" yazma biçimi, Excel'in Türkçe karakterleri doğru göstermesini sağlar.
    columns = ["id", "group", "category", "prompt", "knowledge_items"] + REVIEWER_COLUMNS
    with arguments.output.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for record in records:
            knowledge_items = get_field(record, "knowledge_items")
            row = {
                "id": record["id"],
                "group": get_field(record, "group"),
                "category": get_field(record, "category"),
                "prompt": record["prompt"],
                # Bilgi öğeleri tek hücreye " | " işaretiyle ayrılarak yazılır.
                "knowledge_items": " | ".join(knowledge_items or []),
            }
            previous_row = previous_rows.get(record["id"], {})
            for column in REVIEWER_COLUMNS:
                row[column] = previous_row.get(column, "")
            # Bu kayıtta bilgi öğesi yoksa onaylanacak bir şey de yoktur; hücreye "-" yazılır.
            if knowledge_items is None:
                row[KNOWLEDGE_APPROVAL] = NOT_APPLICABLE
            writer.writerow(row)

    # İnsanın en az bir hücresini doldurduğu satırları say.
    # Betiğin kendi yazdığı "-" işareti insan doldurması sayılmaz.
    kept_row_count = sum(
        1 for record in records
        if any(previous_rows.get(record["id"], {}).get(column, "").strip() not in ("", NOT_APPLICABLE)
               for column in REVIEWER_COLUMNS)
    )
    print(f"{len(records)} satır yazıldı -> {arguments.output} (korunan dolu satır: {kept_row_count})")

    # Her onay sütunu için hangi değerden kaç tane olduğunu say ve yaz.
    # Yazım farkları yok sayılır. Tanınmayan bir değer varsa o kaydın kimliği gösterilir;
    # böylece yanlış yazılmış bir onay sessizce kaybolmaz.
    for column in (APPROVAL, KNOWLEDGE_APPROVAL):
        label_counts: dict[str, int] = {}
        undefined_ids = []
        for record in records:
            # Bilgi öğesi olmayan satırlar bilgi onayı sayımına girmez.
            if column == KNOWLEDGE_APPROVAL and get_field(record, "knowledge_items") is None:
                continue
            label = normalize_label(previous_rows.get(record["id"], {}).get(column, "")) or "(boş)"
            label_counts[label] = label_counts.get(label, 0) + 1
            if label not in VALID_LABELS and label != "(boş)":
                undefined_ids.append(record["id"])
        print(f"{column}: {dict(sorted(label_counts.items()))}"
              + (f" | tanımsız değer: {undefined_ids}" if undefined_ids else ""))


if __name__ == "__main__":
    main()
