# Page Replacement Simulation

Doğuş Üniversitesi Yazılım Mühendisliği — İşletim Sistemleri dersi kapsamında geliştirilen sayfa değiştirme simülasyonu.

## Projenin Amacı

İşletim sistemlerinde fiziksel bellekte boş çerçeve kalmadığında hangi sayfanın bellekten çıkarılacağını farklı sayfa değiştirme algoritmalarıyla simüle etmek ve sonuçları karşılaştırmak.

## Özellikler

- FIFO (First-In, First-Out)
- LRU (Least Recently Used)
- Optimal Page Replacement
- Second Chance (Clock)
- Page hit ve page fault hesaplama
- Adım adım simülasyon geçmişi
- CustomTkinter kullanıcı arayüzü
- Otomatik testler ve girdi doğrulama

## Teknolojiler

- Python 3
- CustomTkinter
- pytest (test ortamında kullanılıyorsa)

## Kurulum

Depoyu klonlayın:

```bash
git clone https://github.com/beysatavli/page-replacement-simulation.git
cd page-replacement-simulation
```

Sanal ortam oluşturun ve etkinleştirin:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Bağımlılıkları yükleyin:

```bash
python3 -m pip install -r requirements.txt
```

## Çalıştırma

Proje ana dizinindeyken:

```bash
python3 main.py
```

## Testleri Çalıştırma

Test bağımlılıkları kuruluysa:

```bash
python3 -m pytest -v
```

## Proje Yapısı

- `main.py`: Uygulamanın başlangıç noktası
- `ui.py`: Kullanıcı arayüzü
- `simulator_bridge.py`: Arayüz ile simülasyon arasındaki bağlantı
- `page_replacemet/`: Sayfa değiştirme algoritmalarının bulunduğu modül
- `tests/`: Otomatik testler
- `requirements.txt`: Python bağımlılıkları

## Ekip Çalışması

Kod geliştirme çalışmaları ayrı Git branch'lerinde yürütülür. Değişiklikler Pull Request üzerinden incelenir ve uygun olduğunda ana dala birleştirilir.


## Proje Durumu

Proje kapsamında FIFO, LRU, Optimal ve Second Chance sayfa değiştirme algoritmalarının simülasyonu geliştirilmiştir. Kullanıcı arayüzü üzerinden girdi dizisi ve bellek çerçevesi sayısı belirlenerek simülasyon sonuçları incelenebilir.

Uygulamanın doğruluğu otomatik testlerle kontrol edilmektedir. Test sonuçları, doğrulama sırasında elde edilen gerçek çıktılara göre raporlanır.

