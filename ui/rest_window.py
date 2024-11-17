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
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # Wstępny komunikat
        self.label = QLabel(
            "Please rest and relax.\nA cross will appear on the screen. "
            "Please look at it until you hear the sound signal.\nPress any key to continue."
        )
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
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
            # Pierwsze naciśnięcie klawisza – wyświetl krzyż
            self.layout.removeWidget(self.label)
            self.label.deleteLater()

            self.cross_label = QLabel(self)
            pixmap = QPixmap("images/plus.png")
            pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio)
            self.cross_label.setPixmap(pixmap)
            self.cross_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.cross_label)

            # Start timer for 2.5 minutes (150000 ms)
            QTimer.singleShot(1500, self.show_close_eyes_message)
            self.step = 1

    def show_close_eyes_message(self):
        # Usunięcie krzyża i pokazanie komunikatu o zamknięciu oczu
        self.layout.removeWidget(self.cross_label)
        self.cross_label.deleteLater()

        # Odtwórz dźwięk
        self.play_sound()

        # Wyświetl komunikat o zamknięciu oczu
        self.label = QLabel("Please close your eyes until you hear the next sound signal.")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Start timer for another 2.5 minutes
        QTimer.singleShot(1500, self.show_final_message)
        self.step = 2

    def show_final_message(self):
        # Odtwórz dźwięk
        self.play_sound()

        # Zaktualizuj komunikat końcowy
        self.layout.removeWidget(self.label)
        self.label.deleteLater()

        self.label = QLabel(
            "Thank you for completing the relaxation phase.\n"
            "You will soon perform a task to check your concentration.\n\nPress any key to continue."
        )
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.step = 3  # End of sequence

    def event(self, event: QEvent):
        if event.type() == QEvent.KeyPress and self.step == 3:
            self.main_app.show_ant_instructions()  # Przełączenie na ekran instrukcji ANT
        return super().event(event)
