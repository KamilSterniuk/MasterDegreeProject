from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QLabel, QRadioButton, QButtonGroup
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
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główna etykieta instrukcji z mniejszym rozmiarem
        instruction_label = QLabel("Please play the ASMR videos and select the one that triggers you the most.")
        instruction_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        instruction_label.setAlignment(Qt.AlignCenter)

        # Główny layout siatki do wyświetlania 7 odtwarzaczy wideo
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Utwórz listę przechowującą obiekty QMediaPlayer, QAudioOutput i QVideoWidget
        self.players = []

        # Ścieżki do plików wideo i miniatur
        video_urls = [
            "videos/ASMR_short1.mp4",  # Zakładając, że tylko ten plik jest dostępny na razie
            "videos/ASMR_short1.mp4",
            "videos/ASMR_short1.mp4",
            "videos/ASMR_short1.mp4",
            "videos/ASMR_short1.mp4",
            "videos/ASMR_short1.mp4",
            "videos/ASMR_short1.mp4",
        ]
        thumbnail_paths = [
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb1.png",
            "videos/thumbnails/thumb1.png",
        ]

        # Grupa przycisków radiowych, aby tylko jedno z 7 mogło być zaznaczone
        self.radio_button_group = QButtonGroup(self)
        self.radio_button_group.setExclusive(True)
        self.radio_button_group.buttonClicked.connect(self.show_confirm_button)  # Połącz z funkcją wyświetlającą przycisk

        for i in range(7):
            # Inicjalizuj odtwarzacz multimediów i wyjście audio
            player = QMediaPlayer(self)
            audio_output = QAudioOutput(self)  # Dodaj wyjście audio
            player.setAudioOutput(audio_output)  # Połącz wyjście audio z odtwarzaczem
            audio_output.setVolume(1.0)  # Ustaw głośność na 100% (1.0 to maksymalna głośność)

            video_widget = QVideoWidget(self)
            video_widget.hide()  # Ukryj QVideoWidget na początku

            # Ustaw wideo widget jako widoczny odtwarzacz wideo dla playera
            player.setVideoOutput(video_widget)

            # Utwórz przycisk radiowy do wyboru ulubionego filmu
            radio_button = QRadioButton(f"Select Film {i+1}")
            radio_button.setStyleSheet("color: white; font-size: 14px;")
            self.radio_button_group.addButton(radio_button, i)  # Dodaj do grupy radiobuttonów

            # Utwórz miniaturkę jako QLabel z pixmapą
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(QPixmap(thumbnail_paths[i]).scaled(400, 225, Qt.KeepAspectRatio))  # Większa miniaturka
            thumbnail_label.setAlignment(Qt.AlignCenter)

            # Utwórz przyciski Play i Pause
            play_button = QPushButton("Play")
            play_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 5px;")
            play_button.clicked.connect(lambda _, p=player, url=video_urls[i], t=thumbnail_label, v=video_widget: self.play_video(p, url, t, v))

            pause_button = QPushButton("Pause")
            pause_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 5px;")
            pause_button.clicked.connect(player.pause)

            # Layout dla przycisków sterujących
            button_layout = QHBoxLayout()
            button_layout.addWidget(play_button)
            button_layout.addWidget(pause_button)

            # Layout pionowy dla każdego pola wideo (przycisk radiowy, miniaturka, wideo + przyciski)
            video_layout = QVBoxLayout()
            video_layout.addWidget(radio_button)      # Dodaj przycisk radiowy na górze
            video_layout.addWidget(thumbnail_label)   # Dodaj miniaturkę jako kolejny element
            video_layout.addWidget(video_widget)
            video_layout.addLayout(button_layout)

            # Dodaj do siatki
            row = i // 3  # obliczanie wiersza (3 elementy na wiersz)
            col = i % 3  # obliczanie kolumny
            grid_layout.addLayout(video_layout, row, col)

            # Przechowaj player, audio_output i video_widget w liście, by móc kontrolować odtwarzanie
            self.players.append((player, audio_output, video_widget))

        # Dodaj przycisk Confirm do siatki w prawym dolnym rogu
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px;")
        self.confirm_button.setVisible(False)
        self.confirm_button.clicked.connect(self.confirm_selection)  # Połącz przycisk z funkcją potwierdzenia

        # Umieść przycisk Confirm w siatce na pozycji (2, 2) - prawy dolny róg
        grid_layout.addWidget(self.confirm_button, 2, 2, alignment=Qt.AlignRight | Qt.AlignBottom)

        # Ustawienie rozciągania dla wierszy i kolumn siatki, aby zajmowała całe dostępne miejsce
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setRowStretch(2, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(2, 1)

        # Główny układ, który zawiera etykietę instrukcji oraz siatkę wideo
        main_layout = QVBoxLayout()
        main_layout.addWidget(instruction_label, alignment=Qt.AlignTop)  # Dodaj etykietę instrukcji na górze
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def play_video(self, player, video_url, thumbnail_label, video_widget):
        # Zatrzymaj wszystkie pozostałe odtwarzacze
        for p, _, _ in self.players:
            if p != player and p.playbackState() == QMediaPlayer.PlayingState:
                p.pause()  # Wstrzymaj inne odtwarzające się wideo

        # Ukryj miniaturkę i pokaż widget wideo
        thumbnail_label.hide()  # Ukrywa miniaturkę przed rozpoczęciem odtwarzania
        video_widget.show()  # Pokazuje widget wideo

        # Sprawdź, czy wideo jest już wstrzymane - jeśli tak, nie ustawiaj źródła ponownie
        if player.playbackState() != QMediaPlayer.PausedState:
            player.setSource(
                QUrl.fromLocalFile(video_url))  # Ustaw źródło tylko, jeśli odtwarzacz nie jest w stanie pauzy

        # Rozpocznij lub kontynuuj odtwarzanie
        player.play()  # Wznów lub rozpocznij odtwarzanie

    def show_confirm_button(self):
        # Pokaż przycisk Confirm po wybraniu opcji
        self.confirm_button.setVisible(True)

    def confirm_selection(self):
        # Zatrzymujemy wszystkie odtwarzacze wideo przed zamknięciem okna
        for player, _, _ in self.players:
            player.stop()

        # Pobieramy wybrany film i otwieramy go w AsmrPlayWindow
        selected_button = self.radio_button_group.checkedButton()
        if selected_button:
            selected_index = self.radio_button_group.id(selected_button) + 1
            long_video_url = f"videos/ASMR_long{selected_index}.mp4"
            # Teraz przekazujemy `self.main_app` jako pierwszy argument
            self.play_window = AsmrPlayWindow(self.main_app, long_video_url)
            self.play_window.showFullScreen()
            self.close()
