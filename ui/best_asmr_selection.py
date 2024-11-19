import os
import csv
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtGui import QPixmap, QPalette, QColor
from PySide6.QtCore import Qt


class BestVideosGridWindow(QWidget):
    def __init__(self, main_app, video_urls, thumbnails, best_videos):
        """
        Tworzy siatkę wyświetlającą filmy z najlepszymi ocenami.
        :param main_app: Referencja do głównej aplikacji.
        :param video_urls: Lista URL-ów filmów.
        :param thumbnails: Lista ścieżek do miniatur filmów.
        :param best_videos: Lista indeksów filmów z najlepszymi ocenami.
        """
        super().__init__()
        self.main_app = main_app
        self.video_urls = video_urls
        self.thumbnails = thumbnails
        self.best_videos = best_videos
        self.selected_index = None

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        instruction_label = QLabel("Please select the video you liked the most:")
        instruction_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        instruction_label.setAlignment(Qt.AlignCenter)

        # Główny layout siatki
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(5)

        # Tworzenie siatki z filmami o najlepszych ocenach
        for idx, video_idx in enumerate(best_videos):
            row = idx // 3
            col = idx % 3

            # Miniaturka filmu
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(QPixmap(self.thumbnails[video_idx]).scaled(400, 225, Qt.KeepAspectRatio))
            thumbnail_label.setAlignment(Qt.AlignCenter)

            # Przycisk wyboru filmu
            select_button = QPushButton(f"Select Video {video_idx + 1}")
            select_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 5px;")
            select_button.clicked.connect(lambda _, idx=video_idx: self.select_video(idx))

            # Layout pionowy dla każdego filmu
            video_layout = QVBoxLayout()
            video_layout.setSpacing(5)
            video_layout.addWidget(thumbnail_label)
            video_layout.addWidget(select_button, alignment=Qt.AlignTop)

            grid_layout.addLayout(video_layout, row, col)

        # Rozciąganie kolumn i wierszy
        for row in range((len(best_videos) + 2) // 3):  # Liczba rzędów zależy od liczby filmów
            grid_layout.setRowStretch(row, 1)
        for col in range(3):
            grid_layout.setColumnStretch(col, 1)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(instruction_label, alignment=Qt.AlignTop)
        main_layout.addLayout(grid_layout)

        # Przycisk powrotu
        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; padding: 10px;")
        back_button.clicked.connect(self.go_back)
        main_layout.addWidget(back_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def select_video(self, video_index):
        """Wybór filmu i dopisanie informacji do pliku CSV."""
        # Dopisanie wybranego najlepszego filmu do pliku CSV
        if hasattr(self.main_app, 'csv_file_path') and self.main_app.csv_file_path:
            self.append_best_video_to_file(self.main_app.csv_file_path, video_index)

        # Przejście do odtwarzania wybranego filmu
        self.main_app.show_selected_video(video_index)
        self.close()

    def append_best_video_to_file(self, csv_file_path, selected_video):
        """Dopisuje informację o wybranym najlepszym filmie do istniejącego pliku CSV."""
        with open(csv_file_path, mode="a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([])
            writer.writerow(["Best Video", f"Video {selected_video + 1}"])
        print(f"Final best video appended to {csv_file_path}")

    def go_back(self):
        """Powrót do okna wyboru ASMR."""
        self.main_app.show_asmr_select_window()
        self.close()
