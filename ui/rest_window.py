from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPalette, QColor, QPixmap, QKeyEvent
from PySide6.QtCore import Qt, QTimer, QEvent, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class RestWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Przechowuje referencję do MainApp

        # Ustawienia ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#000000"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Header
        self.header_label = QLabel("Faza relaksacji")
        self.header_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white; padding: 10px;")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)

        # Introductory message
        self.label = QLabel()
        self.label.setTextFormat(Qt.TextFormat.RichText)  # Set QLabel to interpret HTML
        self.label.setText(
            "Zaraz rozpocznie się faza relaksacji.<br><br>"
            "Twoim zadaniem jest odpoczynek i skupienie wzroku na białym krzyżu wyświetlonym na ekranie.<br><br>"
            "Gdy usłyszysz sygnał dźwiękowy, zamknij oczy, zrelaksuj się i czekaj na kolejny sygnał,<br>"
            "który będzie oznaczał otwarcie oczu.<br><br>"
            "<b>Naciśnij dowolny klawisz, aby kontynuować.</b>"
        )
        self.label.setStyleSheet("font-size: 24px; font-weight: normal; color: white; padding: 20px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.step = 0  # Tracking steps for different phases

        # Ustawienie odtwarzacza audio dla pliku MP3
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile("assets/sound_signal.mp3"))  # Podaj pełną ścieżkę do pliku

    def play_sound(self):
        self.player.stop()  # Zatrzymuje poprzednie odtwarzanie, jeśli istnieje
        self.player.play()  # Odtwórz plik MP3

    def keyPressEvent(self, event: QKeyEvent):
        if self.step == 0:
            # Usuń nagłówek
            self.layout.removeWidget(self.header_label)
            self.header_label.deleteLater()

            # Pierwsze naciśnięcie klawisza – wyświetl krzyż
            self.layout.removeWidget(self.label)
            self.label.deleteLater()

            self.cross_label = QLabel(self)
            pixmap = QPixmap("images/plus_white.png")
            pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio)
            self.cross_label.setPixmap(pixmap)
            self.cross_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.cross_label)

            # Start timer for 2.5 minutes (150000 ms)
            QTimer.singleShot(10000, self.show_close_eyes_message)
            self.step = 1

    def show_close_eyes_message(self):
        # Usunięcie krzyża i pokazanie komunikatu o zamknięciu oczu
        self.layout.removeWidget(self.cross_label)
        self.cross_label.deleteLater()

        # Odtwórz dźwięk
        self.play_sound()

        # Wyświetl komunikat o zamknięciu oczu
        self.label = QLabel("Zamknij oczy i zrelaksuj się aż do kolejnego sygnału dźwiękowego.")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Start timer for another 2.5 minutes
        QTimer.singleShot(10000, self.show_final_message)
        self.step = 2

    def show_final_message(self):
        # Odtwórz dźwięk
        self.play_sound()

        # Zaktualizuj komunikat końcowy
        self.layout.removeWidget(self.label)
        self.label.deleteLater()

        self.label = QLabel(
            "Dziękujemy za udział w fazie relaksacji.\n"
            "Za chwilę wypełnisz krótki kwestionariusz dotyczący Twojego samopoczucia.\n\n"
            "Naciśnij dowolny klawisz, aby kontynuować."
        )
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.step = 3  # End of sequence

    def event(self, event: QEvent):
        if event.type() == QEvent.KeyPress and self.step == 3:
            self.main_app.show_stai_post_ant()  # Przełączenie na ekran instrukcji ANT
        return super().event(event)
