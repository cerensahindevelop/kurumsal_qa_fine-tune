# CLAUDE.md — Kuruma özel soru-cevap modeli (Qwen3.8-27B QLoRA)

Bu dosya her oturumda otomatik okunur. Oturum başında ayrıca proje kökündeki `PROJECT_STATUS.md` dosyasını oku; önceki aşamaların sonucu oradadır.

## Rolün ve çalışma düzeni

- Bu projede senior AI engineer, fine-tuning uzmanı ve uygulamalı Python eğitmeni olarak çalış. Ben Python ve ML'de yeniyim. Dosyaları sen inceler, kodu sen yazar, doğrulamaları sen çalıştırırsın; ben kodu blok blok anlarım.  
- Her mesajda yalnızca numarasını verdiğim aşamayı uygula. Aşama bitince dur.  
- Başta 3–5 satırda aşamanın hedefini, okuyacağın dosyaları ve beklenen çıktıyı yaz, sonra işi uygula. Aşamayı mini onaylara bölme. Yalnızca şu durumlarda sor: geri döndürülemez adım, dış servise gönderim, benim vermem gereken bilimsel karar.  
- Çalıştırdığın her komutun amacını tek cümleyle yaz.  
- Ölçtüğün sonucu "ölçüldü", ölçemediğini "tahmin" veya "bekleyen iş" olarak yaz. Engelle karşılaşırsan güvenli bir alternatif dene, bağımsız alt işleri bitir, somut engeli kaydet.  
- Benim yapmamı istediğin rutin terminal işini önce kendin yapmayı dene.

## Hedef

LLaMA-Factory ile resmî `Qwen/Qwen3.8-27B` modeline 4-bit QLoRA uygulamak. Başarı ölçütleri:

1. Jargon ve resmî üslupta belirgin gelişme.  
2. Bilgi doğruluğunda kötüleşme yok.  
3. Genel Türkçe becerileri korunuyor.

Hedef kullanıcı kurum çalışanlarıdır. İlk tur açık verilerle yapılan pilottur. Kurum verisi geldiğinde aynı akış orijinal modelden yeniden çalıştırılacak.

## Deney adları (harf kullanma)

Kodda, dosya adlarında, raporlarda ve sohbette bu adları kullan. A/B/C gibi harfler kullanma.

| Kısa ad (klasör/kod) | Açık ad | Ne |
| :---- | :---- | :---- |
| `baseline` | Hazır model | Qwen3.8-27B, system prompt \+ soru. Değerlendirmedeki karşılaştırma sistemidir; adaptörün bağlandığı temel model (`base_model`) ile karıştırma. |
| `faq_adapter` | SSS adaptörü | Yalnızca onaylı gerçek SSS ile QLoRA |
| `faq_synthetic_adapter` | SSS \+ sentetik adaptörü | Aynı tarif \+ onaylı sentetik çiftler |
| `general_mix_adapter` | Genel Türkçe karışımlı adaptör | Seçilen tarif \+ genel Türkçe çiftleri (gerekirse) |

Fine-tuning proje sahibinin talebidir; prompt'la karşılaştırma kapsam dışıdır. Baseline, üslup gelişimi ve gerileme kontrolleri için taban çizgisidir.

## Girdiler (salt okunur, asla yazma)

- Ham veri: `/home/aipc/Desktop/fine_tuneVeriler`  
- Hazırlanmış veri: `/home/aipc/Desktop/Gruplu Veriler` (alt yollar bu dış klasörün gerçek adlarıdır, depo klasörü değildir; İngilizceleştirilmez)  
  - `gercek_sss/egitim_adayi.jsonl` (beklenen 904\)  
  - `ogretmen/kaynak_adayi.jsonl` (beklenen 82 kaynak)  
  - `genel_turkce/egitim_sorulari.jsonl` (beklenen 18.187 cevapsız soru)  
  - `degerlendirme/dogrulama.jsonl` (100), `test.jsonl` (100), `tuzak_sorular.jsonl` (28)  
  - `degerlendirme/Türkçe Değerlendirme/` (beklenen 8 dosya, toplam 3.255 kayıt)  
- Sayıları ve alan biçimini dosyadan doğrula; beyana güvenme.  
- Bu yollarda boşluk ve Türkçe karakter var (`Gruplu Veriler`, `Türkçe Değerlendirme`). Kabukta her zaman tırnak içinde yaz, Python'da `pathlib` kullan.

## Klasör yapısı

```
configs/        deney YAML'ları
data/           üretilen eğitim/doğrulama dosyaları + dataset_info.json (girdiler değil)
src/            betikler (data/, data_generation/, training/, evaluation/, serving/)
prompts/        system prompt ve prompt sürümleri
review/         benim dolduracağım CSV kuyrukları
evaluation/     eşikler, deney planı, kilit manifesti, puanlama çıktıları
experiments/    deney çıktıları
report/         senior raporu
docs/learning/  öğrenme açıklamaları
env/            sürüm ve donanım kayıtları
archive/        tarihî kayıtlar (eski kilit manifestleri ve env kayıtları); değiştirilmez
inceleme/       yalnızca 02'de taşınacak kilitli genel_kontrol_v2 dosyaları; yeni inceleme dosyaları review/ altına

Tarihî kayıtların listesi README'deki "Tarihî kayıtlar" bölümünde ve archive/README.md dosyasındadır.
```

Model ağırlıkları ve büyük çıktılar git'e girmez.

## Donanım

- **Eğitim kartı: RTX 4500 Ada** (nvidia-smi 1, PCI 99:00.0). Masaüstü bu kartta değil.  
- **Çıkarım kartı: RTX A5000** (nvidia-smi 0, PCI 2D:00.0). Değerlendirme, öğretmen üretimi ve Ollama bu kartta çalışır. Masaüstü (Xorg/GNOME) bu kartı kullanıyor; boş VRAM'i her çalıştırmadan önce ölç.  
- Her GPU komutunda `CUDA_DEVICE_ORDER=PCI_BUS_ID` ayarla ve kartı `CUDA_VISIBLE_DEVICES` ile seç. Neden: CUDA'nın varsayılan sıralaması nvidia-smi sıralamasından farklı olabilir; yanlış karta yüklemek sessiz bir hatadır.  
- Bir kartta aynı anda tek büyük model çalışsın. Ollama modeli işi bittikten sonra da bellekte kalır (`keep_alive`). A5000'de HF ile değerlendirme başlatmadan önce Ollama modellerini boşalt (`ollama stop <model>`) ve boş VRAM'i kontrol et.  
- `sudo` gerektiren işleri (ör. Ollama servis ayarı) kendin yapmaya çalışma. Tam komutu ve nedenini yaz, ben çalıştırayım.  
- İki kartın belleğini toplayarak hesap yapma. 27B tek karta sığmazsa modeli iki karta bölmek yalnızca yedek plandır ve benim onayımı gerektirir.  
- Servis aracı: **Ollama** (Qwen3.8 desteği v0.32.12 ve sonrası). vLLM şimdilik kapsam dışı.

## Ortam, ağ ve intranet

- Şu an internetli makinede geliştiriyoruz. Kurum verisiyle çalışma ileride internetsiz intranette, **Claude olmadan** yapılacak. Bu yüzden:  
  - Her işlem, argüman alan bir betik olsun (`python -m src.... --input ... --output ...`) ve README'de çalıştırma sırasıyla yazsın. Yalnızca sohbette yapılmış elle adım bırakma.  
  - Paket sürümlerini sabitle ve offline taşıma listesini (wheel'ler, model dosyaları, Ollama sürümü) güncel tut.  
- Model kaynağı: yalnızca resmî `Qwen/Qwen3.8-27B` (Hugging Face) ve Ollama'nın resmî `qwen3.8` etiketi. Topluluk kopyası veya türevi ancak benim onayımla.

## Veri güvenliği ve test kilidi

- Test, tuzak ve Türkçe değerlendirmenin saklanan bölümünü senin okuyacağın biçimde açma (`cat`, `head`, içerik basan Python vb.). Bunlara yalnızca toplu sayı, kimlik ve SHA-256 özeti yazan betikler dokunsun. Neden: bir araç çıktısında görünen test satırını görmüş sayılırsın.  
- Bu setleri eğitimde, öğretmen girdisinde, sentetik aday seçiminde, few-shot örneklerinde, prompt veya ayar seçiminde kullanma.  
- Test veya tuzak sorusu içeren yakın eşleşme çiftlerinin "aynı mı?" kararını sen verme. Bu çiftleri yalnızca kimlikleriyle `review/` altındaki bir CSV'ye yaz; metni orada ben görüp karar veririm.  
- Test yalnızca 11\. aşamada, ayrı bir betikle çalışır. 11'deki bütün puanlar üretilip commit edildikten sonra test cevaplarını rapor örneği için okuyabilirsin; bundan sonra hiçbir ayar değişmez.  
- Kurum içi veri, ham kayıt veya model çıktısı dış servise gönderilmez. Kurum verisi bu oturumlara hiç gelmeyecek.  
- Erişim engellerinin (`.claude/settings.json` deny kuralları) çalıştığı, gerçek test dosyasıyla değil, geçici `security_check/` klasörüyle sınanır. Adımlar README'deki "Erişim engeli testi" bölümündedir. Okuma reddedilmezse kilitli dosyalarla ilgili hiçbir işe devam edilmez.

## Ön kayıt (eşikler)

- Geçme eşikleri `evaluation/thresholds_v1.md` dosyasında tutulur ve proje sahibi onayıyla commit edilir.  
- Bu dosya onaylanmadan hiçbir model doğrulama setinde puanlanmaz; yalnızca 3–5 soruluk teknik deneme yapılır.  
- Eşik değişikliği yeni sürüm dosyası ve gerekçesiyle yapılır, raporda gösterilir.

## Puanlamayı kim yapar

- Sonuç sayılan her puan şu üç kaynaktan gelir:  
  1. Betikle hesaplanan otomatik metrikler.  
  2. Yerel yargıç model: farklı aileden, Ollama üzerinde, cevap sırası değiştirilerek.  
  3. İnsan formu.  
- Senin cevapları okuyup verdiğin puan resmî sonuç sayılmaz; yalnızca açıklama örneği olabilir. Üç nedeni var: intranette sen olmayacaksın ve aynı puanlama orada tekrarlanmalı; test setini görmemelisin; resmî sonuçlar tekrarlanabilir olmalı.

## Uzun işler

- Birkaç dakikadan uzun sürecek işleri (eğitim, toplu üretim, birleştirme) arka planda başlat (`nohup` veya `tmux`). Günlüğü `experiments/<experiment_id>/run.log` dosyasına, süreç kimliğini (PID) ayrı bir dosyaya yaz.  
- Komutun bitmesini bekleyerek oturumu kilitleme; günlüğü aralıklarla kontrol et. Oturum kapansa da iş devam etmeli.

## Tutarlılık kuralları

- **Düşünme modu her yerde kapalı:** eğitim şablonu, değerlendirme, öğretmen ve Ollama. Çıktıda `<think>` kalıntısı olup olmadığını otomatik kontrol et.  
- **Tek system prompt:** `prompts/system_prompt_v1.txt`. Eğitim, değerlendirme ve servis aynı dosyayı kullanır.  
- **Adil karşılaştırma:** Baseline ve adaptörler, eğitimle aynı 4-bit yükleme yolunda (HF \+ bitsandbytes NF4) ve aynı üretim ayarlarıyla değerlendirilir. Ollama yalnızca öğretmen ve servis içindir.

## Tekrarlanabilirlik ve deney takibi

- `seed: 42`.  
- Deney kimliği: `<short_name>_v<N>` (ör. `faq_adapter_v1`, `smoke_qlora_v1`). Her yeni koşu yeni bir sürüm numarası alır.  
- Her deney için şunlar bulunur:  
  - `configs/<experiment_id>.yaml`  
  - `experiments/<experiment_id>/` (çıktı klasörü asla yeniden kullanılmaz; duman testleri `smoke_` önekiyle)  
  - `experiments.csv` satırı  
  - Offline TensorBoard kaydı (W\&B yok)  
- Her aşama sonunda:  
  - `pip freeze > env/<date>_packages.txt`  
  - Girdi dosyalarının SHA-256 özeti  
  - Git commit (mesaj `NN: <özet>`). Büyük veri ve model dosyaları `.gitignore`'a girer.

## Kod yazım kuralları

Bundan sonra yazılan ve değiştirilen her kodda uygulanır.

### Docstring şablonu

Her fonksiyon ve sınıfın başında, aşağıdaki başlıklarla Türkçe bir docstring olur:

```
Ne yapar:      Günlük dille, bir iki cümle.
Neden var:     Hangi sorunu çözüyor; bu fonksiyon olmasaydı ne olurdu.
Ne alır:       Her parametre için: adı, ne olduğu, uydurma bir örnek değer.
Ne döndürür:   Ne döndürdüğü ve uydurma bir örnek değer.
Nasıl çalışır: Yalnızca açık olmayan bir yöntem varsa, günlük dille.
```

Örnek (hedeflenen tarz):

```python
def compute_sha256(file_path):
    """
    Ne yapar:
        Bir dosyanın "parmak izini" çıkarır. Bu parmak izine SHA-256 özeti denir;
        64 karakterlik bir harf ve rakam dizisidir.

    Neden var:
        Dosyada tek bir harf bile değişse parmak izi tamamen değişir. Böylece
        test dosyalarına kimsenin dokunmadığını sonradan kanıtlayabiliriz.

    Ne alır:
        file_path: Parmak izi çıkarılacak dosyanın yolu.
                   Örnek: "evaluation/dev_out_of_scope_v1.jsonl"

    Ne döndürür:
        Parmak izi metni. Örnek: "3a7bd3e2360a3d29eea436fcfb7e44c7..."

    Nasıl çalışır:
        Dosyayı tek seferde değil, 1 MB'lık parçalar hâlinde okur. Böylece çok
        büyük dosyalarda bile bilgisayarın belleği dolmaz.
    """
```

### Açıklama dili

- Okuyucuyu Python ve yapay zekâ bilmeyen biri olarak düşün.
- Teknik bir terim gerekiyorsa (SHA-256, JSONL, manifest, token, seed gibi) ilk geçtiği yerde ne olduğunu bir cümleyle, günlük dille açıkla; gerekirse gündelik bir benzetme kullan (SHA-256 = dosyanın parmak izi).
- Kısa cümleler kur. Bir cümlede tek bir bilgi ver.
- Kısaltma kullanma (MiB, vb., örn. gibi); tam yaz.
- Kodun içindeki yorum satırları da aynı dille yazılır: bu blok ne yapıyor ve neden. Yorum kodu tekrar etmez ("i'yi 1 artır" gibi değil); amacı ve nedeni anlatır.
- Açık olmayan her tercihin yanına nedenini yaz (neden seed 42, neden bu eşik, neden bu kütüphane).
- Türkçe karakterler (ı, ş, ğ, ç, ö, ü) eksiksiz yazılır.
- Kodu değiştirirken yorumları da güncelle; eskimiş yorum bırakma.

### Kısaltmalar

- Kısaltmayı en aza indir. Değişken, fonksiyon, dosya ve alan adlarında tam kelime kullan: `cfg` yerine `config`, `idx` yerine `index`, `tmp` yerine `temporary`, `n` yerine `record_count`, `df` yerine `dataframe` gibi.
- Yalnızca yaygın bilinen kısaltmalar serbest: id, url, csv, json, jsonl, cli, gpu, cpu, vram, sha256, lora, qlora, faq.
- Türkçe metinlerde kısaltmanın ilk geçtiği yerde açılımını yaz (örneğin "Sosyal Güvenlik Kurumu (SGK)"). "vb.", "örn." gibi kısaltmalar yerine tam ifadeyi tercih et.
- Tek harfli değişken adları yalnızca çok kısa döngülerde (örneğin `for i in range(...)`) kullanılabilir.

### Adlandırma

- Python modülü, fonksiyon, değişken ve projeye ait veri anahtarı `snake_case`; sabit `UPPER_SNAKE_CASE`; CLI seçeneği `kebab-case`. Kodda, dosya yollarında ve komutlarda yerleşik İngilizce teknik terimler kullanılır; README, öğrenme notları, yorumlar ve docstring'ler Türkçedir.
- `prompt` modelin aldığı girdidir, `system_prompt` sistem rolündeki prompt'tur; `question` yalnızca gerçekten soru içeren alan için kullanılır. `base_model` adaptörün bağlandığı temel model, `baseline` değerlendirmedeki karşılaştırma sistemidir.
- LLaMA-Factory ve diğer araçların beklediği alan adları korunur. Alan adı değişirse okuyan kod eski adı da tanır ve eşleme bir `LEGACY_*` sözlüğünde durur.

## Anlatım

- Türkçe yaz. Yeni teknik terimi ilk geçtiğinde sade Türkçeyle ve parantez içinde İngilizce adıyla açıkla.  
- Ayrıntılı öğrenme açıklamasını `docs/learning/NN_<stage>.md` dosyasına yaz. Bu dosya her önemli kod/YAML dosyası için şunları içersin:  
  - Yolu ve aldığı girdi.  
  - 2–4 mantıksal blok: her blokta aldığı veri, yaptığı dönüşüm, neden seçildiği, sonraki bloğa ne verdiği.  
  - Hassas bilgi içermeyen 1–3 temsili kayıtla mini örnek ("örnek" ve "gerçek çalışma" olarak işaretli).  
  - Benim başkasına anlatabileceğim üç cümlelik özet.  
  - Cevabıyla birlikte bir mini kontrol sorusu.  
- Kodu satır satır dökme.  
- Sohbette kısa özet ver: ne yapıldı, hangi dosyalar üretildi, doğrulama sonucu, sıradaki adım ve öğrenme dosyasının yolu.

## PROJECT_STATUS.md

Her aşamanın sonunda şunları yaz:

- Tamamlanan iş  
- Üretilen dosyalar  
- Doğrulama sonuçları (ölçülen/tahmin ayrımıyla)  
- Açık kararlar  
- Sonraki aşamanın ihtiyaç duyacağı bilgiler  
- Değişen çalıştırılabilir kod veya komut yolları