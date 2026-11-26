"""
Ne yapar:
    Bir veya daha fazla veri dosyasında, verilen bir ifadenin kaç kayıtta geçtiğini sayar.
    Örneğin "anlaşılır bir dille anlatır mısın" cümlesinin 60 sorunun kaçında geçtiğini bulur.

Neden var:
    Bazen kilitli bir dosyada belli bir ifadenin olup olmadığını bilmemiz gerekir.
    Ama kilitli dosyaların içini okumamalıyız.
    Bu betik içeriği hiç göstermeden yalnızca sayıyı söyler.

Neden güvenli:
    Ekrana yalnızca dosya adı, kayıt sayısı ve eşleşme sayısı yazılır.
    Kaydın metni, kimliği veya eşleşen bölüm hiçbir zaman yazılmaz.
    Bu yüzden kilitli dosyalarda da kullanılabilir.

Nasıl çalıştırılır (terminalde, proje klasöründeyken):
    python -m src.data.count_phrase_matches --input evaluation/dev_out_of_scope.jsonl \\
        --phrase "anlaşılır bir dille anlatır mısın" --phrase "kısaca"

    --input: aranacak veri dosyaları. Birden fazla dosya yazılabilir.
    --phrase: aranacak ifade. Birden fazla ifade için seçenek tekrar yazılır.

Dosya biçimi:
    Dosyalar JSONL biçiminde olmalıdır. JSONL'de her satır bir kayıttır;
    örneğin bir soru, cevabı ve kategorisi tek bir satırda durur.

Arama kuralları:
    Kaydın bütün metinlerinde aranır; hangi alanda olduğu önemli değildir.
    Büyük ve küçük harf farkı yok sayılır. Türkçedeki İ/i ve I/ı farkı da doğru işlenir.
"""
import argparse
import json
from pathlib import Path


def turkish_lower(text: str) -> str:
    """
    Ne yapar:
        Metni Türkçe kurallarına uygun biçimde küçük harfe çevirir.

    Neden var:
        Python'un kendi küçük harf çevirisi İngilizce kuralını kullanır: "I" harfini "i" yapar.
        Türkçede ise "I" harfinin küçüğü "ı", "İ" harfinin küçüğü "i"dir.
        Bu fonksiyon olmasaydı "ISPARTA" ile "ısparta" aynı kelime sayılmazdı.

    Ne alır:
        text: Küçük harfe çevrilecek metin. Örnek: "KOLAYCA ANLATIR MISIN"

    Ne döndürür:
        Küçük harfli metin. Örnek: "kolayca anlatır mısın"
    """
    return text.replace("İ", "i").replace("I", "ı").lower()


def collect_strings(value) -> list[str]:
    """
    Ne yapar:
        Bir kaydın içindeki bütün metinleri toplayıp bir liste yapar.

    Neden var:
        Farklı dosyalarda metinler farklı adlı alanlarda durur: "prompt", "question", "messages" gibi.
        Bazı alanların içinde de başka alanlar vardır.
        Bu fonksiyon, alan adlarını bilmeden bütün metinlerde arama yapmamızı sağlar.

    Ne alır:
        value: Bir kayıt ya da kaydın bir parçası.
               Örnek: {"id": "1", "question": "İzin hakkım nedir?", "tags": ["izin", "süre"]}

    Ne döndürür:
        İçindeki bütün metinlerin listesi. Örnek: ["1", "İzin hakkım nedir?", "izin", "süre"]

    Nasıl çalışır:
        Değer bir metinse onu listeye koyar.
        Değer bir alan grubu ya da listeyse, içindeki her parça için kendini yeniden çağırır.
        Böylece ne kadar iç içe olursa olsun bütün metinlere ulaşır.
        Sayı gibi metin olmayan değerler atlanır.
    """
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [text for item in value.values() for text in collect_strings(item)]
    if isinstance(value, list):
        return [text for item in value for text in collect_strings(item)]
    return []


def main() -> None:
    """
    Ne yapar:
        Terminalde yazılan komutu okur ve her dosya için her ifadenin kaç kayıtta geçtiğini ekrana yazar.

    Neden var:
        Sayımın her zaman aynı kurallarla ve tek bir komutla yapılabilmesi için.

    Ne alır:
        Doğrudan bir değer almaz. Bilgileri terminalde yazılan komuttan okur (--input ve --phrase).

    Ne döndürür:
        Bir değer döndürmez. Ekrana her dosya için bir satır yazar.
        Örnek ekran çıktısı: "dev_out_of_scope.jsonl: records=15 ['kısaca']=2"
    """
    # Komuttaki seçenekleri tanımla. Her seçeneğin tek bir İngilizce adı vardır.
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1].strip())
    parser.add_argument("--input", type=Path, nargs="+", required=True, help="Aranacak veri dosyaları")
    parser.add_argument("--phrase", action="append", required=True, help="Aranacak ifade (tekrar yazılabilir)")
    arguments = parser.parse_args()

    # Aranacak ifadeleri bir kez küçük harfe çevir; her kayıtta yeniden çevirmeye gerek kalmasın.
    normalized_phrases = [turkish_lower(phrase) for phrase in arguments.phrase]

    for path in arguments.input:
        # Dosyadaki boş olmayan her satırı bir kayıt olarak oku.
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

        # Her kaydın bütün metinlerini tek bir küçük harfli metinde birleştir; ifadeyi bu metinde ara.
        record_texts = [turkish_lower(" ".join(collect_strings(record))) for record in records]
        match_counts = {
            original: sum(normalized in text for text in record_texts)
            for original, normalized in zip(arguments.phrase, normalized_phrases)
        }

        # Ekrana yalnızca sayıları yaz; kayıtların içeriği görünmesin.
        print(f"{path.name}: records={len(records)} "
              + " ".join(f"[{phrase!r}]={count}" for phrase, count in match_counts.items()))


if __name__ == "__main__":
    main()
