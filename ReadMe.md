# 🔍 YOLOv8 ile Nesne Tespiti: Kupa ve Kalem Projesi

Bu proje, **BLG-407 Makine Öğrenmesi** dersi Proje Ödevi kapsamında geliştirilmiştir.
Özgün bir veri seti kullanılarak **YOLOv8** modeli eğitilmiş ve tespit sonuçlarını gösteren modern bir masaüstü arayüzü tasarlanmıştır.

## 👨‍🎓 Öğrenci Bilgileri
* **Adı:** [Eftalya Beril]
* **Soyadı:** [ŞAHİN]
* **Okul No:** [2212721037]
* **Ders:** BLG-407 Makine Öğrenmesi

## 🚀 Proje Hakkında
* **Hedef:** "Kupa" ve "Kalem" nesnelerinin tespiti.
* **Özgünlük:** Kupa ve Kalem nesneleri farklı açılardan, farklı ışık koşullarında ve arka planlarda çekilerek etiketlenmiştir.
* **Veri Seti:** Proje için özgün olarak çekilmiş görseller kullanılmıştır.
* **Model:** YOLOv8n (Nano) modeli tercih edilmiştir.
* **Eğitim:** Model, 20 epoch boyunca eğitilmiş ve `best.pt` ağırlıkları elde edilmiştir.
* **Başarı Skoru:** Eğitim sonucunda model yüksek başarı göstermiştir.

### 📱Geliştirilen Arayüz (GUI)
Kullanıcı deneyimini artırmak amacıyla **PyQt5** kütüphanesi kullanılarak "Soft UI" (Pastel Tonlar) tasarım diline sahip bir masaüstü uygulaması geliştirilmiştir.

* **📂 Resim Yükleme:** Kullanıcı bilgisayarından seçtiği herhangi bir görsel üzerinde nesne tespiti yapabilir.
* **🎥 Canlı Kamera Modu (Opsiyonel Özellik):** Webcam entegrasyonu sayesinde gerçek zamanlı olarak nesne tespiti yapılabilir.
* **💾 Sonuç Kaydetme:** Tespit yapılan görseller, üzerine bounding box (sınırlayıcı kutu) çizilerek otomatik tarih/saat isimlendirmesiyle kaydedilir.
* **✨ Modern Tasarım:** Göz yormayan renk paleti ve kullanıcı dostu butonlar.

## 📂 Dosya Yapısı

📦 Yolo_Proje_Teslim
 ┣ 📂 train/                # Eğitim veri seti görselleri ve etiketleri
 ┣ 📂 val/                  # Doğrulama (Validation) veri seti
 ┣ 📜 gui_app.py            # PyQt5 tabanlı ana masaüstü uygulaması (Kodu buradan çalıştırın)
 ┣ 📜 best.pt               # Eğitilmiş YOLOv8 model dosyası (Weights)
 ┣ 📜 yolo_training.ipynb   # Eğitim sürecini, Loss ve mAP grafiklerini içeren rapor
 ┣ 📜 config.yaml           # Model eğitim konfigürasyon dosyası
 ┣ 📜 requirements.txt      # Gerekli Python kütüphaneleri listesi
 ┗ 📜 ReadMe.md             # Proje dokümantasyonu (Bu dosya)

## 🛠️ Kurulum ve Çalıştırma

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt

2.  Uygulamayı başlatın:
   ```bash
   python gui_app.py


📊 Eğitim Sonuçları ve Başarı

Modelin eğitim süreci boyunca elde edilen Kayıp (Loss) ve Doğruluk (mAP) grafikleri ile Karmaşıklık Matrisi (Confusion Matrix), proje dosyasındaki yolo_training.ipynb içerisinde detaylı olarak sunulmuştur.

mAP50 Skoru: %75 üzeri (Kupa ve Kalem tespiti için optimize edilmiştir).

Epoch Sayısı: 20