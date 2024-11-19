import os
import csv
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QLabel, QSlider, QSizePolicy
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QUrl


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
            video_widget.setMinimumSize(400, 225)
            video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            video_widget.hide()

            player.setVideoOutput(video_widget)

            # Miniaturka
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(QPixmap(thumbnail_paths[i]).scaled(400, 225, Qt.KeepAspectRatio))
            thumbnail_label.setAlignment(Qt.AlignCenter)
            thumbnail_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            thumbnail_label.setMinimumSize(400, 225)

            # Przycisk Play i Pause
            play_button = QPushButton("Play")
            play_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 5px;")
            play_button.clicked.connect(
                lambda _, p=player, url=video_urls[i], t=thumbnail_label, v=video_widget: self.play_video(p, url, t, v))

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

        max_rating = max(self.ratings)
        best_videos = [i for i, rating in enumerate(self.ratings) if rating == max_rating]

        # Zapisz oceny do pliku
        csv_file_path = self.save_ratings_to_file(self.ratings, best_videos)

        if len(best_videos) > 1:
            # Przekazanie ścieżki do pliku do innej sceny programu
            self.main_app.csv_file_path = csv_file_path
            self.main_app.show_choose_asmr_instructions(best_videos)
            self.close()
        else:
            selected_index = best_videos[0]
            self.main_app.show_selected_video(selected_index)

    def save_ratings_to_file(self, ratings, best_videos, results_dir="results"):
        """Zapisuje oceny i (opcjonalnie) najlepszy film do pliku w katalogu o najwyższym numerze."""
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Znalezienie katalogu o najwyższym numerze
        existing_folders = [
            folder for folder in os.listdir(results_dir) if folder.startswith("example") and folder[7:].isdigit()
        ]
        if existing_folders:
            max_number = max(int(folder[7:]) for folder in existing_folders)
        else:
            max_number = 1

        target_folder = os.path.join(results_dir, f"example{max_number}")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Ścieżka do pliku CSV
        csv_file_path = os.path.join(target_folder, "asmr_ratings.csv")

        # Zapis danych
        with open(csv_file_path, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Video Index", "Rating"])
            for i, rating in enumerate(ratings, start=1):
                writer.writerow([f"Video {i}", rating])

            if len(best_videos) == 1:
                writer.writerow([])
                writer.writerow(["Best Video", f"Video {best_videos[0] + 1}"])

        print(f"Ratings saved to {csv_file_path}")
        return csv_file_path
