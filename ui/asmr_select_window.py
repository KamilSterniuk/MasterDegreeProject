from random import choice
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QLabel, QSlider, QSizePolicy
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl
from ui.asmr_play_window import AsmrPlayWindow

class AsmrSelectWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Etykieta instrukcji
        instruction_label = QLabel("Please play the ASMR videos and rate each one from 0 to 10.")
        instruction_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        instruction_label.setAlignment(Qt.AlignCenter)

        # Główny layout siatki
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(10, 10, 10, 10)  # Marginesy wokół siatki
        grid_layout.setSpacing(5)  # Odstęp między elementami

        # Ścieżki do plików wideo i miniatur
        video_urls = [
            "videos/ASMR_short1.mp4",
            "videos/ASMR_short2.mp4",
            "videos/ASMR_short3.mp4",
            "videos/ASMR_short4.mp4",
            "videos/ASMR_short5.mp4",
            "videos/ASMR_short6.mp4",
            "videos/ASMR_short7.mp4",
        ]
        thumbnail_paths = [
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb2.png",
            "videos/thumbnails/thumb3.png",
            "videos/thumbnails/thumb4.png",
            "videos/thumbnails/thumb5.png",
            "videos/thumbnails/thumb6.png",
            "videos/thumbnails/thumb7.png",
        ]

        # Lista ocen wideo
        self.ratings = [0] * len(video_urls)

        # Tworzenie komponentów dla każdego filmu
        self.players = []
        self.rating_labels = []

        for i in range(7):
            # Odtwarzacz wideo
            player = QMediaPlayer(self)
            audio_output = QAudioOutput(self)
            player.setAudioOutput(audio_output)
            audio_output.setVolume(1.0)

            video_widget = QVideoWidget(self)
            video_widget.setMinimumSize(400, 225)  # Minimalny rozmiar
            video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Dynamiczne dopasowanie
            video_widget.hide()

            player.setVideoOutput(video_widget)

            # Miniaturka
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(QPixmap(thumbnail_paths[i]).scaled(400, 225, Qt.KeepAspectRatio))
            thumbnail_label.setAlignment(Qt.AlignCenter)

            # Przycisk Play i Pause
            play_button = QPushButton("Play")
            play_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 5px;")
            play_button.clicked.connect(lambda _, p=player, url=video_urls[i], t=thumbnail_label, v=video_widget: self.play_video(p, url, t, v))

            pause_button = QPushButton("Pause")
            pause_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 5px;")
            pause_button.clicked.connect(player.pause)

            # Pole oceny z etykietą
            rating_label = QLabel(f"Rating: 0")
            rating_label.setStyleSheet("color: white; font-size: 14px;")
            self.rating_labels.append(rating_label)

            rating_input = QSlider(Qt.Horizontal, self)
            rating_input.setRange(0, 10)
            rating_input.setValue(0)
            rating_input.valueChanged.connect(lambda value, index=i: self.update_rating(index, value))

            # Layout dla przycisków sterujących
            button_layout = QHBoxLayout()
            button_layout.addWidget(play_button)
            button_layout.addWidget(pause_button)

            # Layout pionowy dla każdego filmu
            video_layout = QVBoxLayout()
            video_layout.addWidget(thumbnail_label)
            video_layout.addWidget(video_widget)
            video_layout.addLayout(button_layout)
            video_layout.addWidget(rating_label)
            video_layout.addWidget(rating_input)

            # Dodaj do siatki
            row = i // 3
            col = i % 3
            grid_layout.addLayout(video_layout, row, col)

            self.players.append((player, audio_output, video_widget))

        # Rozciąganie kolumn i wierszy
        for row in range(3):
            grid_layout.setRowStretch(row, 1)
        for col in range(3):
            grid_layout.setColumnStretch(col, 1)

        # Przycisk Confirm
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px;")
        self.confirm_button.clicked.connect(self.confirm_selection)
        grid_layout.addWidget(self.confirm_button, 3, 2, alignment=Qt.AlignRight | Qt.AlignBottom)

        # Główny układ
        main_layout = QVBoxLayout()
        main_layout.addWidget(instruction_label, alignment=Qt.AlignTop)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def play_video(self, player, video_url, thumbnail_label, video_widget):
        for p, _, _ in self.players:
            if p != player and p.playbackState() == QMediaPlayer.PlayingState:
                p.pause()

        thumbnail_label.hide()
        video_widget.show()

        if player.playbackState() != QMediaPlayer.PausedState:
            player.setSource(QUrl.fromLocalFile(video_url))
        player.play()

    def update_rating(self, index, value):
        # Aktualizuje ocenę i tekst etykiety
        self.ratings[index] = value
        self.rating_labels[index].setText(f"Rating: {value}")

    def confirm_selection(self):
        for player, _, _ in self.players:
            player.stop()

        # Znajdź najwyższą ocenę
        max_rating = max(self.ratings)
        best_videos = [i for i, rating in enumerate(self.ratings) if rating == max_rating]

        # Wybierz losowy film spośród najlepszych
        selected_index = choice(best_videos)
        long_video_url = f"videos/ASMR_long{selected_index + 1}.mp4"

        # Otwórz wybrany film w AsmrPlayWindow
        self.play_window = AsmrPlayWindow(self.main_app, long_video_url)
        self.play_window.showFullScreen()
        self.close()
