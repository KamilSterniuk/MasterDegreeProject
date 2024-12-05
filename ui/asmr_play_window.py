from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QFont


class AsmrPlayWindow(QWidget):
    def __init__(self, main_app, video_url, asmr_enabled=True):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("ASMR Full Play")
        self.showFullScreen()  # Pełny ekran

        # Ścieżka do wideo i ustawienie trybu ASMR
        self.video_url = video_url
        self.asmr_enabled = asmr_enabled

        # Tworzenie playera i audio
        self.player = QMediaPlayer(self)
        audio_output = QAudioOutput(self)
        self.player.setAudioOutput(audio_output)

        if asmr_enabled:
            audio_output.setVolume(1.0)  # Maksymalna głośność dla ASMR
        else:
            audio_output.setVolume(0.0)  # Wyciszenie dźwięku wideo

        # Dodatkowy dźwięk BB dla grupy z BB
        self.bb_player = QMediaPlayer(self)
        bb_audio_output = QAudioOutput(self)
        self.bb_player.setAudioOutput(bb_audio_output)
        self.bb_player.setSource(QUrl.fromLocalFile("assets/BB.mp3"))
        bb_audio_output.setVolume(0.5)  # Głośność dźwięku binauralnego

        # Tworzenie widgetu wideo i ustawienie go jako wyjście wideo
        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        # Stylizacja tła
        self.setStyleSheet("background-color: #2E2E2E;")

        # Instrukcja początkowa
        self.instruction_label = QLabel(self)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("color: white; padding: 20px;")
        self.instruction_label.setFont(QFont("Arial", 20, QFont.Bold))

        if asmr_enabled:
            self.instruction_label.setText(
                "<p style='text-align: center;'>"
                "Take a deep breath, relax, and get comfortable.<br>"
                "The ASMR video will play shortly.<br><br>"
                "<b>Press any key to start when you're ready.</b>"
                "</p>"
            )
        else:
            self.instruction_label.setText(
                "<p style='text-align: center;'>"
                "Take a deep breath, relax, and get comfortable.<br>"
                "The ASMR video will play shortly, accompanied by <b>Binaural Beats</b> in the background.<br><br>"
                "Binaural Beats are auditory illusions that may enhance relaxation and focus.<br><br>"
                "<b>Press any key to start when you're ready.</b>"
                "</p>"
            )

        # Wiadomość końcowa
        self.end_message_label = QLabel(self)
        self.end_message_label.setAlignment(Qt.AlignCenter)
        self.end_message_label.setStyleSheet("color: white; padding: 20px;")
        self.end_message_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.end_message_label.setText(
            "<p style='text-align: center;'>"
            "Thank you for watching the video.<br>"
            "You will soon perform a task to check your concentration.<br><br>"
            "<b>Press any key to continue.</b>"
            "</p>"
        )
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

            # Rozpocznij odtwarzanie BB, jeśli ASMR jest wyłączone
            if not self.asmr_enabled:
                self.bb_player.play()
        elif self.end_message_label.isVisible():
            # Przejście do ekranu instrukcji ANT
            self.main_app.show_ant_instructions()
            self.close()

    def on_video_finished(self, status):
        """Wywoływana po zakończeniu odtwarzania wideo."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.video_widget.hide()  # Ukryj widget wideo po zakończeniu filmu
            self.end_message_label.setVisible(True)  # Pokaż wiadomość końcową

            # Zatrzymaj dźwięk BB, jeśli grał
            if not self.asmr_enabled:
                self.bb_player.stop()
