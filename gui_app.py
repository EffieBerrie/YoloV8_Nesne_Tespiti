import sys
import cv2
import os
from datetime import datetime # Tarih saat için eklendi
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPixmap, QImage, QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO

# OMP Hatasını önlemek için
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# --- AYARLAR ---
# Model Yolun (Train4 klasörün)
MODEL_PATH = r"C:\Users\Owner\runs\detect\train4\weights\best.pt"

class NesneTespitUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 Nesne Tespiti - Soft UI")
        self.setGeometry(100, 100, 1200, 750)
        
        # Değişkenler
        self.model = None
        self.image_path = None
        self.processed_image = None
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_open = False

        self.init_styles() # Tasarım Ayarları
        self.load_model()
        self.initUI()

    def init_styles(self):
        # PASTEL RENK PALETİ VE CSS STİLLERİ
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FDFBF7; /* Çok açık krem */
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                color: #555555;
            }
            /* GÖRSEL PANELLERİ */
            QLabel#ImagePanel {
                background-color: #F0F4F8; /* Pastel Grimsi Mavi */
                border-radius: 15px;
                border: 2px dashed #D1D9E6;
            }
            /* BUTON GENEL STİLİ */
            QPushButton {
                border-radius: 12px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
                color: white;
                border: none;
            }
            /* MAVİ BUTON (Resim Seç) */
            QPushButton#BtnBlue {
                background-color: #8EACCD; /* Pastel Mavi */
            }
            QPushButton#BtnBlue:hover { background-color: #7B9BBF; }

            /* YEŞİL BUTON (Test Et) */
            QPushButton#BtnGreen {
                background-color: #95D2B3; /* Pastel Yeşil */
            }
            QPushButton#BtnGreen:hover { background-color: #7FC0A0; }

            /* KIRMIZI/PEMBE BUTON (Kamera) */
            QPushButton#BtnRed {
                background-color: #E78F81; /* Pastel Kiremit/Pembe */
            }
            QPushButton#BtnRed:hover { background-color: #D67565; }

            /* TURUNCU BUTON (Kaydet) */
            QPushButton#BtnOrange {
                background-color: #F1C376; /* Pastel Turuncu/Hardal */
            }
            QPushButton#BtnOrange:hover { background-color: #DEAF60; }
        """)

    def load_model(self):
        try:
            self.model = YOLO(MODEL_PATH)
            print(f"Model Yüklendi: {MODEL_PATH}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Model yüklenemedi!\n{e}")

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40) # Kenar boşlukları

        # --- BAŞLIK ---
        lbl_title = QLabel("YOLOv8 Nesne Tespiti Projesi")
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        lbl_title.setStyleSheet("color: #607D8B; margin-bottom: 10px;")
        main_layout.addWidget(lbl_title)

        # --- GÖRSEL ALANI ---
        image_layout = QHBoxLayout()
        image_layout.setSpacing(30)

        # Sol Panel
        self.lbl_original = QLabel("Resim Seçin veya Kamerayı Açın")
        self.lbl_original.setObjectName("ImagePanel") # CSS için ID
        self.lbl_original.setAlignment(Qt.AlignCenter)
        self.lbl_original.setFixedSize(530, 430)
        self.lbl_original.setFont(QFont("Segoe UI", 12))

        # Sağ Panel
        self.lbl_result = QLabel("Sonuç Ekranı")
        self.lbl_result.setObjectName("ImagePanel") # CSS için ID
        self.lbl_result.setAlignment(Qt.AlignCenter)
        self.lbl_result.setFixedSize(530, 430)
        self.lbl_result.setFont(QFont("Segoe UI", 12))

        image_layout.addWidget(self.lbl_original)
        image_layout.addWidget(self.lbl_result)
        
        # --- BİLGİ ALANI ---
        self.lbl_info = QLabel("Hazır.")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setFont(QFont("Segoe UI", 14))
        self.lbl_info.setStyleSheet("color: #888; font-style: italic;")

        # --- BUTONLAR ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.btn_load = QPushButton("📂 Resim Seç")
        self.btn_load.setObjectName("BtnBlue")
        self.btn_load.setCursor(Qt.PointingHandCursor)
        self.btn_load.clicked.connect(self.select_image)

        self.btn_detect = QPushButton("✨ Analiz Et")
        self.btn_detect.setObjectName("BtnGreen")
        self.btn_detect.setCursor(Qt.PointingHandCursor)
        self.btn_detect.clicked.connect(self.detect_image)

        self.btn_camera = QPushButton("🎥 Kamera Modu")
        self.btn_camera.setObjectName("BtnRed")
        self.btn_camera.setCursor(Qt.PointingHandCursor)
        self.btn_camera.clicked.connect(self.toggle_camera)

        self.btn_save = QPushButton("💾 Sonucu Kaydet")
        self.btn_save.setObjectName("BtnOrange")
        self.btn_save.setCursor(Qt.PointingHandCursor)
        self.btn_save.clicked.connect(self.save_image)

        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_detect)
        btn_layout.addWidget(self.btn_camera)
        btn_layout.addWidget(self.btn_save)

        # Düzenleri Birleştir
        main_layout.addLayout(image_layout)
        main_layout.addWidget(self.lbl_info)
        main_layout.addLayout(btn_layout)
        main_widget.setLayout(main_layout)

    # --- FONKSİYONLAR ---
    def select_image(self):
        if self.is_camera_open: self.toggle_camera()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Görsel (*.jpg *.png *.jpeg)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.lbl_original.setPixmap(pixmap.scaled(self.lbl_original.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.lbl_result.clear()
            self.lbl_result.setText("Analiz Bekleniyor...")
            self.lbl_info.setText(f"Seçilen Dosya: {os.path.basename(file_path)}")
            self.processed_image = None

    def detect_image(self):
        if not self.image_path: return
        self.lbl_info.setText("Yapay zeka analiz ediyor...")
        QApplication.processEvents()
        
        results = self.model(self.image_path)
        self.display_result(results[0])

    def toggle_camera(self):
        if not self.is_camera_open:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                QMessageBox.warning(self, "Hata", "Kamera bulunamadı!")
                return
            self.timer.start(30)
            self.is_camera_open = True
            self.lbl_original.setText("")
            self.lbl_info.setText("Canlı Kamera Modu Aktif")
            self.btn_camera.setText("Kamerayı Durdur")
        else:
            self.timer.stop()
            if self.cap: self.cap.release()
            self.lbl_original.clear()
            self.lbl_result.clear()
            self.lbl_original.setText("Kamera Kapalı")
            self.is_camera_open = False
            self.lbl_info.setText("Kamera durduruldu.")
            self.btn_camera.setText("🎥 Kamera Modu")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_on_label(frame_rgb, self.lbl_original)
            
            results = self.model(frame, verbose=False)
            res_plotted = results[0].plot()
            
            res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
            self.display_on_label(res_rgb, self.lbl_result)
            self.processed_image = res_plotted

    def display_on_label(self, img_rgb, label):
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def display_result(self, result):
        res_plotted = result.plot()
        res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
        self.display_on_label(res_rgb, self.lbl_result)
        self.processed_image = res_plotted
        
        count_kupa = sum(1 for box in result.boxes if int(box.cls[0]) == 0)
        count_kalem = sum(1 for box in result.boxes if int(box.cls[0]) == 1)
        self.lbl_info.setText(f"Sonuç: {count_kupa} Kupa, {count_kalem} Kalem bulundu.")

    def save_image(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek görüntü yok.")
            return
        
        # --- YENİ EKLENEN KISIM: OTOMATİK İSİMLENDİRME ---
        simdi = datetime.now().strftime("%Y%m%d_%H%M%S") # Örnek: 20251216_143005
        varsayilan_isim = f"sonuc_{simdi}.jpg"
        
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Görüntüyü Kaydet", varsayilan_isim, "Resim (*.jpg *.png)", options=options)
        
        if save_path:
            cv2.imwrite(save_path, self.processed_image)
            QMessageBox.information(self, "Başarılı", f"Görüntü kaydedildi:\n{os.path.basename(save_path)}")

    def closeEvent(self, event):
        if self.is_camera_open: self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NesneTespitUygulamasi()
    window.show()
    sys.exit(app.exec_())