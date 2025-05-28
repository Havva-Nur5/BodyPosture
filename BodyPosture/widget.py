# Gerekli kütüphaneleri içe aktarıyoruz
import cv2
import mediapipe as mp
import sys
import time
import winsound  # ses uyarısı için

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from ui_form import Ui_Widget  # tasarım dosyamız buradan geliyor

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # Kamerayı başlatıyoruz
        self.cap = cv2.VideoCapture(0)

        # Timer kurduk ki sürekli kamera görüntüsünü alabilelim
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_frame)
        self.timer.start(30)  # 30 milisaniyede bir frame alıyoruz

        # Pose tespiti için mediapipe'ı hazırlıyoruz
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Beep sesi sürekli çalmasın diye zaman tutmak için değişken
        self.last_beep_time = 0
        self.beep_interval = 3  # saniyede birden sık beep olmasın diye

    def show_frame(self):
        # Kameradan bir kare (frame) alıyoruz
        ret, frame = self.cap.read()
        if not ret:
            return  # Kamera açılmadıysa devam etmiyoruz

        # Renkleri mediapipe için RGB'ye çeviriyoruz
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        durus_iyi = True  # varsayılan olarak duruş iyi kabul ettik

        # Eğer vücut pozisyonu tespit edildiyse
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Kulağı, omzu ve kalçayı alıyoruz
            left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR]
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP]

            h, w, _ = frame.shape
            ear_px = int(left_ear.x * w), int(left_ear.y * h)
            shoulder_px = int(left_shoulder.x * w), int(left_shoulder.y * h)
            hip_px = int(left_hip.x * w), int(left_hip.y * h)

            # Noktaları daire ile işaretliyoruz
            cv2.circle(frame, ear_px, 6, (0, 255, 255), -1)
            cv2.circle(frame, shoulder_px, 8, (0, 255, 0), -1)
            cv2.circle(frame, hip_px, 8, (255, 0, 0), -1)

            # X eksenindeki farkları kontrol ediyoruz
            ear_shoulder_diff = abs(ear_px[0] - shoulder_px[0])
            shoulder_hip_diff = abs(shoulder_px[0] - hip_px[0])

            # Duruş doğru mu diye bakıyoruz (kulak omuzdan fazla önde mi gibi)
            kulak_omuz_dogru = ear_shoulder_diff < 40
            omuz_kalca_dogru = shoulder_hip_diff < 40

            durus_iyi = kulak_omuz_dogru and omuz_kalca_dogru

            # Çizgi rengini duruşa göre ayarlıyoruz
            line_color = (0, 255, 0) if durus_iyi else (0, 0, 255)

            # Kulak-omuz ve omuz-kalça arası çizgiler
            cv2.line(frame, ear_px, shoulder_px, line_color, 2)
            cv2.line(frame, shoulder_px, hip_px, line_color, 2)

            # Uyarı mesajlarını hazırlıyoruz
            uyarilar = []
            if not kulak_omuz_dogru:
                uyarilar.append("don't let your head down")  # başın öne düşmesin
            if not omuz_kalca_dogru:
                uyarilar.append("shoulders and bel are not on the same line ")  # omuz ve bel hizalanmamış
            if durus_iyi:
                uyarilar.append("perfect ✔️")  # her şey yolunda

            # Ekrana yazıları yazdırıyoruz
            y = 50
            for uyari in uyarilar:
                cv2.putText(frame, uyari, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, line_color, 2)
                y += 40

            # Beep sesi ne zaman çalacak onu kontrol ediyoruz
            current_time = time.time()
            if not durus_iyi and (current_time - self.last_beep_time) > self.beep_interval:
                winsound.Beep(1000, 500)  # 1000 Hz ses 0.5 saniye
                self.last_beep_time = current_time

        # Kameradan gelen görüntüyü PySide6 arayüzüne yerleştiriyoruz
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled_qimg = q_img.scaled(
            self.ui.label_camera.width(),
            self.ui.label_camera.height(),
            Qt.KeepAspectRatioByExpanding
        )
        pixmap = QPixmap.fromImage(scaled_qimg)
        self.ui.label_camera.setPixmap(pixmap)

    # Pencere kapanınca kamera kapansın diye
    def closeEvent(self, event):
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    # Uygulama başlatılıyor
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
