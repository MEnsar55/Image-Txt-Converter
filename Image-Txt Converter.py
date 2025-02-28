import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QLineEdit,
    QMessageBox, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QPixmap, QFont, QImage, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

# ----- ImageProcessor (Görüntüyü Yazıya Çevirici) -----
class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "English"  # varsayılan dil
        self.metot = 1
        self.image_path = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 700, 400)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 1px solid #333333;")

        self.txt_filename_label = QLabel(self)
        self.txt_filename_label.setGeometry(50, 470, 200, 30)
        self.txt_filename_label.setFont(QFont('Segoe UI', 10, QFont.Bold))

        self.txt_filename_input = QLineEdit(self)
        self.txt_filename_input.setGeometry(200, 470, 200, 30)
        self.txt_filename_input.setFont(QFont('Segoe UI', 10, QFont.Bold))

        self.btn_select_image = QPushButton(self)
        self.btn_select_image.setGeometry(50, 520, 150, 50)
        self.btn_select_image.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.btn_select_image.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px;")
        self.btn_select_image.clicked.connect(self.open_image)

        self.btn_change_metot = QPushButton(self)
        # Genişliği artırıldı
        self.btn_change_metot.setGeometry(250, 520, 300, 50)
        self.btn_change_metot.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.btn_change_metot.setStyleSheet("background-color: #FFC107; color: white; border-radius: 5px;")
        self.btn_change_metot.clicked.connect(self.change_metot)

        self.btn_save_pixels = QPushButton(self)
        self.btn_save_pixels.setGeometry(570, 520, 200, 50)
        self.btn_save_pixels.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.btn_save_pixels.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.btn_save_pixels.clicked.connect(self.save_pixels)

        self.status_label = QLabel(self)
        self.status_label.setGeometry(600, 580, 250, 30)
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.status_label.setStyleSheet("color: green;")

        self.updateLanguage(self.language)

    def updateLanguage(self, lang):
        self.language = lang
        if lang == "English":
            self.setWindowTitle("Image to Text Converter")
            self.txt_filename_label.setText("Enter txt file name:")
            self.txt_filename_input.setPlaceholderText("file name")
            self.btn_select_image.setText("Select Image")
            if self.metot == 1:
                self.btn_change_metot.setText("Change Method (Method 1)")
            else:
                self.btn_change_metot.setText("Change Method (Method 2)")
            self.btn_save_pixels.setText("Save Pixels")
        else:
            self.setWindowTitle("Görüntüyü Yazıya Çevirici")
            self.txt_filename_label.setText("Txt dosya adı girin:")
            self.txt_filename_input.setPlaceholderText("dosya adı")
            self.btn_select_image.setText("Resim Seç")
            if self.metot == 1:
                self.btn_change_metot.setText("Metot Değiştir (Metot 1)")
            else:
                self.btn_change_metot.setText("Metot Değiştir (Metot 2)")
            self.btn_save_pixels.setText("Pikselleri Kaydet")

    def open_image(self):
        options = QFileDialog.Options()
        fileTitle = "Select Image" if self.language=="English" else "Resim Seç"
        fileName, _ = QFileDialog.getOpenFileName(self, fileTitle, "", 
                                                  "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)", options=options)
        if fileName:
            self.image_path = fileName
            pixmap = QPixmap(fileName)
            self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))

    def change_metot(self):
        if self.metot == 1:
            self.metot = 2
            if self.language == "English":
                self.btn_change_metot.setText("Change Method (Method 2)")
            else:
                self.btn_change_metot.setText("Metot Değiştir (Metot 2)")
        else:
            self.metot = 1
            if self.language == "English":
                self.btn_change_metot.setText("Change Method (Method 1)")
            else:
                self.btn_change_metot.setText("Metot Değiştir (Metot 1)")

    def save_pixels(self):
        if not self.image_path:
            QMessageBox.warning(self, "Warning" if self.language=="English" else "Uyarı",
                                "Please select an image first." if self.language=="English" else "Lütfen önce bir resim seçin.")
            return

        txt_filename = self.txt_filename_input.text()
        if not txt_filename.endswith('.txt'):
            txt_filename += ".txt"

        self.status_label.setText("Processing..." if self.language=="English" else "İşleniyor...")
        QApplication.processEvents()

        try:
            img = QPixmap(self.image_path).toImage()
            width = img.width()
            height = img.height()

            if self.metot == 1:
                self.save_metot_1(img, width, height, txt_filename)
            elif self.metot == 2:
                self.save_metot_2(img, width, height, txt_filename)

            self.status_label.setText("Successful!" if self.language=="English" else "Başarılı!")
            self.status_label.setStyleSheet("color: green;")
        except Exception as e:
            self.status_label.setText("Unsuccessful!" if self.language=="English" else "Başarısız!")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Error" if self.language=="English" else "Hata", str(e))

        QTimer.singleShot(3000, lambda: self.status_label.clear())

    def save_metot_1(self, img, width, height, filename):
        with open(filename, 'w') as file:
            file.write("Method 1\n" if self.language=="English" else "Metot 1\n")
            for y in range(height):
                for x in range(width):
                    color = img.pixelColor(x, y)
                    file.write(f'{x},{y} - {color.red()},{color.green()},{color.blue()}\n')

    def save_metot_2(self, img, width, height, filename):
        pixels = {}
        for y in range(height):
            for x in range(width):
                color = img.pixelColor(x, y)
                rgb = (color.red(), color.green(), color.blue())
                if rgb not in pixels:
                    pixels[rgb] = []
                pixels[rgb].append((x, y))

        with open(filename, 'w') as file:
            file.write("Method 2\n" if self.language=="English" else "Metot 2\n")
            for rgb, coords in pixels.items():
                file.write(f'{rgb}:\n')
                for coord in coords:
                    file.write(f'  {coord}\n')

# ----- ImageReconstructor (Txt'den Görüntü Oluşturucu) -----
class ImageReconstructor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "English"
        self.txt_filename = None
        self.image = None
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 700, 400)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 1px solid #333333;")

        self.btn_load_file = QPushButton(self)
        self.btn_load_file.setGeometry(50, 470, 150, 50)
        self.btn_load_file.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.btn_load_file.setStyleSheet("background-color: #2196F3; color: white; border-radius: 5px;")
        self.btn_load_file.clicked.connect(self.open_file_dialog)

        self.btn_save_image = QPushButton(self)
        self.btn_save_image.setGeometry(250, 470, 200, 50)
        self.btn_save_image.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.btn_save_image.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px;")
        self.btn_save_image.clicked.connect(self.save_image)

        self.status_label = QLabel(self)
        self.status_label.setGeometry(500, 530, 250, 30)
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.status_label.setStyleSheet("color: green;")

        self.file_type_combo = QComboBox(self)
        self.file_type_combo.setGeometry(500, 470, 100, 50)
        self.file_type_combo.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.file_type_combo.addItems(["PNG", "JPEG", "BMP", "JPG"])

        self.metot_yazisi = QLabel(self)
        self.metot_yazisi.setGeometry(50, 530, 150, 30)
        self.metot_yazisi.setFont(QFont('Segoe UI', 10))
        self.metot_yazisi.hide()

        self.updateLanguage(self.language)

    def updateLanguage(self, lang):
        self.language = lang
        if lang == "English":
            self.setWindowTitle("Image Reconstructor")
            self.btn_load_file.setText("Select Txt File")
            self.btn_save_image.setText("Save Image")
        else:
            self.setWindowTitle("Yeniden Görüntü Oluşturucu")
            self.btn_load_file.setText("Txt Dosyasını Seç")
            self.btn_save_image.setText("Resmi Kaydet")
        # Eğer metot yazısı görünürse, diline uygun güncelleyin.
        if self.metot_yazisi.isVisible():
            if lang=="English":
                if self.metot_yazisi.text() in ["Metot 1", "Method 1"]:
                    self.metot_yazisi.setText("Method 1")
                elif self.metot_yazisi.text() in ["Metot 2", "Method 2"]:
                    self.metot_yazisi.setText("Method 2")
            else:
                if self.metot_yazisi.text() in ["Method 1", "Metot 1"]:
                    self.metot_yazisi.setText("Metot 1")
                elif self.metot_yazisi.text() in ["Method 2", "Metot 2"]:
                    self.metot_yazisi.setText("Metot 2")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        fileTitle = "Select Txt File" if self.language=="English" else "Txt Dosyasını Seç"
        fileName, _ = QFileDialog.getOpenFileName(self, fileTitle, "", 
                                                  "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            self.txt_filename = fileName
            self.load_pixels()

    def load_pixels(self):
        if not self.txt_filename:
            QMessageBox.warning(self, "Warning" if self.language=="English" else "Uyarı",
                                "Please select a txt file first." if self.language=="English" else "Lütfen önce bir txt dosyası seçin.")
            return

        self.status_label.setText("Processing..." if self.language=="English" else "İşleniyor...")
        QApplication.processEvents()

        try:
            with open(self.txt_filename, 'r') as file:
                metot_line = file.readline().strip()
                if metot_line in ["Method 1", "Metot 1"]:
                    self.load_metot_1(file)
                    self.metot_yazisi.setText("Method 1" if self.language=="English" else "Metot 1")
                    self.metot_yazisi.show()
                elif metot_line in ["Method 2", "Metot 2"]:
                    self.load_metot_2(file)
                    self.metot_yazisi.setText("Method 2" if self.language=="English" else "Metot 2")
                    self.metot_yazisi.show()
                else:
                    raise ValueError("Invalid method information" if self.language=="English" else "Geçersiz yöntem bilgisi")

            self.status_label.setText("Successful!" if self.language=="English" else "Başarılı!")
            self.status_label.setStyleSheet("color: green;")
        except Exception as e:
            self.status_label.setText("Unsuccessful!" if self.language=="English" else "Başarısız!")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Error" if self.language=="English" else "Hata", str(e))
        QTimer.singleShot(3000, lambda: self.status_label.clear())

    def load_metot_1(self, file):
        data = file.readlines()
        if not data:
            raise ValueError("Empty or invalid file format" if self.language=="English" else "Dosya boş veya geçersiz format")

        coords = [line.strip() for line in data[1:]]
        if not coords:
            raise ValueError("No pixels found" if self.language=="English" else "Pikseller bulunamadı")

        x_max = max(int(line.split(' - ')[0].split(',')[0]) for line in coords) + 1
        y_max = max(int(line.split(' - ')[0].split(',')[1]) for line in coords) + 1

        img = QImage(x_max, y_max, QImage.Format_RGB888)
        img.fill(Qt.white)

        for line in coords:
            coord, color = line.split(' - ')
            x, y = map(int, coord.split(','))
            r, g, b = map(int, color.split(','))
            img.setPixelColor(x, y, QColor(r, g, b))

        self.image = img
        self.display_image()

    def load_metot_2(self, file):
        pixels = {}
        rgb = None
        for line in file:
            line = line.strip()
            if line.endswith(':'):
                rgb = tuple(map(int, line[:-1].strip('()').split(',')))
                pixels[rgb] = []
            elif rgb is not None:
                coord = tuple(map(int, line.strip().strip('()').split(',')))
                pixels[rgb].append(coord)

        if not pixels:
            raise ValueError("No pixels found" if self.language=="English" else "Pikseller bulunamadı")

        x_max = max(x for coords in pixels.values() for x, y in coords) + 1
        y_max = max(y for coords in pixels.values() for x, y in coords) + 1

        img = QImage(x_max, y_max, QImage.Format_RGB888)
        img.fill(Qt.white)

        for rgb, coords in pixels.items():
            r, g, b = rgb
            for x, y in coords:
                img.setPixelColor(x, y, QColor(r, g, b))

        self.image = img
        self.display_image()

    def display_image(self):
        if self.image:
            pixmap = QPixmap.fromImage(self.image)
            self.label.setPixmap(pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))

    def save_image(self):
        if not self.image:
            QMessageBox.warning(self, "Warning" if self.language=="English" else "Uyarı",
                                "Please load the pixels first." if self.language=="English" else "Lütfen önce pikselleri yükleyin.")
            return

        options = QFileDialog.Options()
        file_filter = f"Images (*.{self.file_type_combo.currentText().lower()});;All Files (*)"
        fileTitle = "Save Image" if self.language=="English" else "Resmi Kaydet"
        fileName, _ = QFileDialog.getSaveFileName(self, fileTitle, "", file_filter, options=options)
        if fileName:
            if not fileName.endswith(f'.{self.file_type_combo.currentText().lower()}'):
                fileName += f".{self.file_type_combo.currentText().lower()}"
            self.image.save(fileName)

# ----- Settings Page (Ayarlar Ekranı) -----
class SettingsPage(QWidget):
    backClicked = pyqtSignal()
    languageChanged = pyqtSignal(str)
    
    def __init__(self, current_language="English"):
        super().__init__()
        self.current_language = current_language
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet("background-color: #f7f7f7;")
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        self.label = QLabel("Select Language:" if self.current_language=="English" else "Dil Seçiniz:")
        self.label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.label.setStyleSheet("color: #333333;")
        
        self.combo_language = QComboBox()
        self.combo_language.setFont(QFont('Segoe UI', 12))
        self.combo_language.addItems(["English", "Türkçe"])
        index = self.combo_language.findText(self.current_language)
        if index != -1:
            self.combo_language.setCurrentIndex(index)
        self.combo_language.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        
        self.back_button = QPushButton("Back" if self.current_language=="English" else "Geri")
        self.back_button.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.back_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;")
        
        layout.addWidget(self.label)
        layout.addWidget(self.combo_language)
        layout.addWidget(self.back_button)
        layout.addStretch()
        self.setLayout(layout)
        
        self.back_button.clicked.connect(self.on_back)
        self.combo_language.currentTextChanged.connect(self.on_language_changed)
        
    def on_back(self):
        self.backClicked.emit()
        
    def on_language_changed(self, lang):
        self.current_language = lang
        self.languageChanged.emit(lang)
        
    def updateLanguage(self, lang):
        self.current_language = lang
        if lang == "English":
            self.label.setText("Select Language:")
            self.back_button.setText("Back")
        else:
            self.label.setText("Dil Seçiniz:")
            self.back_button.setText("Geri")
        index = self.combo_language.findText(lang)
        if index != -1:
            self.combo_language.setCurrentIndex(index)

# ----- Main Window (Arayüz Geçişi ve Ayarlar Butonları) -----
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "English"
        self.previous_index = 0  # Ayarlar ekranından çıkarken geri dönülecek arayüz indeksi
        self.initUI()

    def initUI(self):
        # Pencere boyutunu %20 daha büyük ve sabit olarak ayarla (900x720)
        self.setFixedSize(900, 720)
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowTitle("Image Processing Application")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Üst Bar: Sol – arayüz geçişi, Sağ – ayarlar butonu
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        
        self.interfaceCombo = QComboBox()
        self.interfaceCombo.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.interfaceCombo.addItems(["Image Processor", "Image Reconstructor"])
        top_layout.addWidget(self.interfaceCombo, alignment=Qt.AlignLeft)
        
        top_layout.addStretch()
        
        self.settingsButton = QPushButton("Settings")
        self.settingsButton.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.settingsButton.setStyleSheet("background-color: #000000; color: white; padding: 8px 12px; border-radius: 5px;")
        top_layout.addWidget(self.settingsButton, alignment=Qt.AlignRight)
        
        main_layout.addWidget(top_bar)
        
        # Stacked Widget: Sayfalar arası geçiş
        self.stackedWidget = QStackedWidget()
        main_layout.addWidget(self.stackedWidget)

        # Sayfa 0: ImageProcessor, Sayfa 1: ImageReconstructor, Sayfa 2: SettingsPage
        self.pageProcessor = ImageProcessor()
        self.pageReconstructor = ImageReconstructor()
        self.pageSettings = SettingsPage(self.language)
        
        self.stackedWidget.addWidget(self.pageProcessor)
        self.stackedWidget.addWidget(self.pageReconstructor)
        self.stackedWidget.addWidget(self.pageSettings)
        
        # Sinyalleri bağla
        self.interfaceCombo.currentIndexChanged.connect(self.switchInterface)
        self.settingsButton.clicked.connect(self.openSettings)
        self.pageSettings.backClicked.connect(self.closeSettings)
        self.pageSettings.languageChanged.connect(self.changeLanguage)
        
        self.updateLanguage(self.language)
        self.stackedWidget.setCurrentIndex(0)  # Varsayılan olarak ImageProcessor

    def switchInterface(self, index):
        # Sadece ana arayüzler arasında geçiş (index 0 veya 1)
        self.stackedWidget.setCurrentIndex(index)

    def openSettings(self):
        # Şu anki arayüzü kaydet, ayarlar ekranına geç
        self.previous_index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(2)

    def closeSettings(self):
        # Ayarlar ekranından çıkıp önceki sayfaya dön
        self.stackedWidget.setCurrentIndex(self.previous_index)

    def changeLanguage(self, lang):
        self.language = lang
        self.updateLanguage(lang)

    def updateLanguage(self, lang):
        if lang == "English":
            self.interfaceCombo.clear()
            self.interfaceCombo.addItems(["Image Processor", "Image Reconstructor"])
            self.settingsButton.setText("Settings")
            self.setWindowTitle("Image Processing Application")
        else:
            self.interfaceCombo.clear()
            self.interfaceCombo.addItems(["Görüntüyü Yazıya Çevirici", "Yeniden Görüntü Oluşturucu"])
            self.settingsButton.setText("Ayarlar")
            self.setWindowTitle("Görüntü İşleme Uygulaması")
        if hasattr(self.pageProcessor, "updateLanguage"):
            self.pageProcessor.updateLanguage(lang)
            self.pageProcessor.language = lang
        if hasattr(self.pageReconstructor, "updateLanguage"):
            self.pageReconstructor.updateLanguage(lang)
            self.pageReconstructor.language = lang
        if hasattr(self.pageSettings, "updateLanguage"):
            self.pageSettings.updateLanguage(lang)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
