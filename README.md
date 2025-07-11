# PixelSink - Gelişmiş Görsel Analiz Aracı

PixelSink, yüklenen görsellerin içeriğinde potansiyel bilgi sızıntılarını tespit etmek için tasarlanmış bir web uygulamasıdır. Görselleri üç farklı katmanda analiz ederek gizli verileri, metadata izlerini ve dosya bütünlüğünü kontrol eder.

## 🎯 Temel Özellikler

1.  **EXIF Metadata Analizi**: GPS konumu, çekim tarihi, cihaz modeli gibi bir görselin içinde saklanan tüm metadata bilgilerini listeler.
2.  **LSB Steganografi Tespiti**: Görselin en anlamsız bit (Least Significant Bit) katmanlarını analiz ederek, piksellerin içine gizlenmiş potansiyel mesaj veya veri izlerini arar.
3.  **Görsel Hash Üretimi**:
    *   **SHA256**: Dosyanın bütünlüğünü doğrulamak ve tam kopyaları tespit etmek için kullanılır.
    *   **Perceptual Hash (pHash)**: Görsel olarak birbirine benzeyen ancak farklı dosya yapılarına sahip resimleri karşılaştırmak için kullanılır.
4.  **Şüpheli Skor**: Analiz sonuçlarına göre (örneğin GPS verisi varlığı, LSB anormallikleri) bir risk skoru hesaplar.

## 🛠️ Kullanılan Teknolojiler

*   **Backend**: Flask
*   **Görsel İşleme ve Analiz**:
    *   `Pillow`: Görsel manipülasyonu ve LSB analizi.
    *   `exifread`: EXIF metadata çıkarımı.
    *   `imagehash`: Perceptual hash (pHash) üretimi.
    *   `hashlib`: SHA256 hash üretimi.
*   **Frontend**: HTML, CSS, JavaScript (Vanilla)

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Gerekli Kütüphaneleri Yükleyin**:

    Proje dizininde bir terminal açın ve `requirements.txt` dosyasındaki bağımlılıkları yükleyin.

    ```bash
    pip install -r requirements.txt
    ```

2.  **Uygulamayı Başlatın**:

    Aşağıdaki komut ile Flask geliştirme sunucusunu başlatın.

    ```bash
    python3 app.py
    ```

3.  **Uygulamaya Erişin**:

    Sunucu başarıyla başladıktan sonra, web tarayıcınızdan `http://127.0.0.1:5002` adresini ziyaret edin.

## 📁 Klasör Yapısı

```
pixelsink/
├── app.py              # Ana Flask uygulaması
├── requirements.txt      # Gerekli Python kütüphaneleri
├── README.md             # Proje açıklaması
├── analyzer/             # Analiz modülleri
│   ├── exif_reader.py
│   ├── hash_generator.py
│   └── lsb_detector.py
├── static/               # CSS ve JS dosyaları
│   └── style.css
├── templates/            # HTML şablonları
│   ├── index.html
│   └── report.html
└── uploads/              # Kullanıcı tarafından yüklenen görseller
```
