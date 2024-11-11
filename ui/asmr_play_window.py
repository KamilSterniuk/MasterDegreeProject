from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt

class AsmrPlayWindow(QWidget):
    def __init__(self, main_app, video_url):  # Upewnij się, że konstruktor przyjmuje dwa argumenty: `main_app` i `video_url`
        super().__init__()
        self.main_app = main_app  # Zapiszmy referencję do głównego okna
        self.setWindowTitle("ASMR Full Play")
        self.showFullScreen()  # Pełny ekran

        # Ścieżka do wideo
        self.video_url = video_url

        # Tworzenie playera i audio
        self.player = QMediaPlayer(self)
        audio_output = QAudioOutput(self)
        self.player.setAudioOutput(audio_output)
        audio_output.setVolume(1.0)  # Maksymalna głośność

        # Tworzenie widgetu wideo i ustawienie go jako wyjście wideo
        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        # Stylizacja tła i etykiety z instrukcją
        self.setStyleSheet("background-color: #2E2E2E;")  # Ciemnoszare tło
        self.instruction_label = QLabel(
            "The ASMR video will be displayed shortly.\nPlease watch it entirely and focus.\n\nPress any key to start.",
            self
        )
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 20px;")

        # Etykieta wyświetlana po zakończeniu filmu
        self.end_message_label = QLabel(
            "Thank you for watching the video.\nYou will soon perform a task to check your concentration.\n\nPress any key to continue.",
            self
        )
        self.end_message_label.setAlignment(Qt.AlignCenter)
        self.end_message_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 20px;")
        self.end_message_label.setVisible(False)  # Ukryj na początku

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.instruction_label)
        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.end_message_label)
        self.setLayout(self.layout)

        # Ukryj widget wideo na początku
        self.video_widget.hide()

        # Po zakończeniu filmu wywołaj metodę `on_video_finished`
        self.player.mediaStatusChanged.connect(self.on_video_finished)

    def keyPressEvent(self, event):
        """Rozpoczyna odtwarzanie wideo po naciśnięciu dowolnego klawisza lub kontynuuje po zakończeniu filmu."""
        if self.instruction_label.isVisible():
            # Ukryj instrukcje początkowe i pokaż wideo
            self.instruction_label.hide()
            self.video_widget.show()

            # Ustaw źródło wideo i rozpocznij odtwarzanie
            self.player.setSource(QUrl.fromLocalFile(self.video_url))
            self.player.play()
        elif self.end_message_label.isVisible():
            # Przejście do ekranu instrukcji ANT
            self.main_app.show_ant_instructions()
            self.close()

    def on_video_finished(self, status):
        """Wywoływana po zakończeniu odtwarzania wideo."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.video_widget.hide()  # Ukryj widget wideo po zakończeniu filmu
            self.end_message_label.setVisible(True)  # Pokaż wiadomość końcową
