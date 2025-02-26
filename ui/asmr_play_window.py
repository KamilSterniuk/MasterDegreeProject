# asmr_play_window.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QFont
from global_eye_tracker import global_eye_tracker  # Importujemy globalną instancję

class AsmrPlayWindow(QWidget):
    def __init__(self, main_app, video_url, asmr_enabled=True):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("ASMR Full Play")
        self.showFullScreen()  # Pełny ekran

        self.video_url = video_url
        self.asmr_enabled = asmr_enabled
        self.eye_tracker_recorder = global_eye_tracker  # Używamy globalnej instancji

        # Konfiguracja odtwarzacza wideo i audio
        self.player = QMediaPlayer(self)
        audio_output = QAudioOutput(self)
        self.player.setAudioOutput(audio_output)
        if asmr_enabled:
            audio_output.setVolume(1.0)
        else:
            audio_output.setVolume(0.0)

        # Konfiguracja dodatkowego odtwarzacza dźwięku (BB)
        self.bb_player = QMediaPlayer(self)
        bb_audio_output = QAudioOutput(self)
        self.bb_player.setAudioOutput(bb_audio_output)
        self.bb_player.setSource(QUrl.fromLocalFile("assets/BB.mp3"))
        bb_audio_output.setVolume(0.5)

        # Ustawienie widgetu wideo
        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        self.setStyleSheet("background-color: #2E2E2E;")

        # Etykiety instrukcji
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
        self.end_message_label.setVisible(False)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.instruction_label)
        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.end_message_label)
        self.setLayout(self.layout)
        self.video_widget.hide()

        # Po zakończeniu filmu wywołujemy metodę on_video_finished
        self.player.mediaStatusChanged.connect(self.on_video_finished)

    def keyPressEvent(self, event):
        """Rozpoczyna odtwarzanie wideo po naciśnięciu dowolnego klawisza."""
        if self.instruction_label.isVisible():
            self.instruction_label.hide()
            self.video_widget.show()
            self.player.setSource(QUrl.fromLocalFile(self.video_url))
            self.player.play()
            if not self.asmr_enabled:
                self.bb_player.play()
            # Rozpoczynamy rejestrację – globalna instancja już została zainicjalizowana
            self.eye_tracker_recorder.start()
        elif self.end_message_label.isVisible():
            self.main_app.show_ant_instructions()
            self.close()

    def on_video_finished(self, status):
        """Wywoływana po zakończeniu wideo."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.video_widget.hide()
            self.end_message_label.setVisible(True)
            if not self.asmr_enabled:
                self.bb_player.stop()
            self.eye_tracker_recorder.process_session("asmr_play")