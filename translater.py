import setuptools
import sys
import speech_recognition as sr
from googletrans import LANGUAGES, Translator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from langdetect import detect

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('TRANSLATE')
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('icon.png'))  # Özel ikon ayarla

        # Arayüz düzeni
        self.layout = QVBoxLayout()

        # Metin giriş alanı
        self.input_label = QLabel('Çevirmek istediğiniz metni girin - Enter the text you want to translate')
        self.layout.addWidget(self.input_label)
        self.input_text = QTextEdit()
        self.layout.addWidget(self.input_text)

        # Kaynak dil seçimi
        self.source_lang_label = QLabel('Kaynak Dil - Source language')
        self.layout.addWidget(self.source_lang_label)
        self.source_lang_combo = QComboBox()
        self.populate_language_combobox(self.source_lang_combo)
        self.layout.addWidget(self.source_lang_combo)

        # Hedef dil seçimi
        self.target_lang_label = QLabel('Hedef Dil - Target language')
        self.layout.addWidget(self.target_lang_label)
        self.target_lang_combo = QComboBox()
        self.populate_language_combobox(self.target_lang_combo)
        self.layout.addWidget(self.target_lang_combo)

        # Çeviri sonucu gösterme alanı
        self.output_label = QLabel('Çeviri - Translation')
        self.layout.addWidget(self.output_label)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Metin çevirme düğmesi
        self.translate_button = QPushButton('Metni Çevir - Translate Text')
        self.translate_button.clicked.connect(self.translate_text)
        self.layout.addWidget(self.translate_button)

        # Sesli çeviri düğmesi
        self.speech_button = QPushButton('Sesli Çeviri(mikrofon gereklidir) - Voice Translation (microphone required)')
        self.speech_button.clicked.connect(self.speech_to_text)
        self.layout.addWidget(self.speech_button)

        self.setLayout(self.layout)

    def populate_language_combobox(self, combobox):
        for lang_code, lang_name in LANGUAGES.items():
            combobox.addItem(lang_name, lang_code)

    def translate_text(self):
        text = self.input_text.toPlainText()
        source_lang = self.source_lang_combo.currentData()
        target_lang = self.target_lang_combo.currentData()
        translator = Translator()
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        self.output_text.setPlainText(translation.text)

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Lütfen konuşun...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='tr-TR')
            self.input_text.setPlainText(text)
        except sr.UnknownValueError:
            print("Anlaşılamadı")
        except sr.RequestError as e:
            print("Hata oluştu; {0}".format(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
