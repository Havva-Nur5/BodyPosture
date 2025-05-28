# BodyPosture
Postür Takip ve Duruş Uyarı Sistemi
Bu proje, gerçek zamanlı olarak kullanıcının duruşunu analiz eden ve kötü duruş tespit edildiğinde hem görsel hem de sesli uyarı veren bir postür takip uygulamasıdır. Özellikle masa başında uzun süre çalışanlar için ergonomik farkındalık yaratmayı hedefler.

Özellikler
Gerçek zamanlı kamera görüntüsü: Bilgisayar kamerasından alınan görüntü anlık olarak analiz edilir.

MediaPipe Pose ile vücut analizi: Sol kulak, omuz ve kalça noktaları üzerinden duruş değerlendirilir.

Duruş çizgileri: Kulak-omuz ve omuz-kalça arası çizgilerle hizalanma görselleştirilir.

Görsel uyarılar: Ekranda duruş bozuklukları ile ilgili uyarı metinleri gösterilir.

Sesli uyarı: Yanlış duruş devam ederse sistem belirli aralıklarla sesli uyarı verir.

Qt arayüzü: Kullanıcı dostu arayüzde canlı kamera görüntüsü gösterilir.

Nasıl Çalışır?
Sistem, kameradan alınan görüntüdeki vücut noktalarını (kulak, omuz, kalça) tespit eder.

Bu üç noktanın yatay eksendeki hizasına bakarak duruşun doğru olup olmadığı değerlendirilir.

Duruş bozulmuşsa ekranda uyarı metinleri gösterilir ve belli aralıklarla bip sesi çalınır.

Duruş düzeltilirse ekranda "perfect ✔" mesajı görünür.

Gereksinimler
Aşağıdaki kütüphaneler sistemde kurulu olmalıdır:

Python 3.x

OpenCV (opencv-python)

MediaPipe (mediapipe)

PySide6 (pyside6)

Kurulum için:

bash
Kopyala
Düzenle
pip install opencv-python mediapipe pyside6
Kullanım
ui_form.py dosyasının bulunduğundan emin olun (Qt Designer ile oluşturulmuş arayüz).

main.py dosyasını çalıştırın:

bash
Kopyala
Düzenle
python main.py
Kamera açılacak, arayüz üzerinden canlı görüntü ve duruş değerlendirmesi başlayacaktır.

Notlar
Kod Windows sistemler için yazılmıştır. winsound modülü Windows'a özeldir. Eğer başka bir işletim sistemi kullanıyorsanız sesli uyarı kısmını alternatif bir yöntemle değiştirmeniz gerekir.

Uygulama, sadece sol vücut noktalarını baz alarak değerlendirme yapar. Daha gelişmiş bir sistem için sağ taraf ve simetri kontrolleri de eklenebilir.
