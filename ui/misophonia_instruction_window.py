from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class MisophoniaInstructionWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Tytuł
        title_label = QLabel("Instrukcje do Kwestionariusza Mizofonii")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Instrukcja
        instructions_label = QLabel()
        instructions_label.setTextFormat(Qt.TextFormat.RichText)  # Użycie HTML dla formatowania
        instructions_label.setText(
            "<p style='font-size: 20px; color: #BBBBBB; text-align: center;'>"
            "The <b>Kwestionariusz Mizofonii</b> został zaprojektowany w celu oceny Twoich emocjonalnych "
            "i fizycznych reakcji na typowe dźwięki wyzwalające.<br> Zostanie Ci przedstawiona seria pytań dotyczących Twoich doświadczeń.<br><br>"
            "Dla każdego pytania użyj suwaka, aby ocenić swoją reakcję w skali od <b>0</b> to <b>10</b>, gdzie:"
            "<ul style='text-align: left;'>"
            "<li><b>0:</b> Brak reakcji lub dyskomfortu.</li>"
            "<li><b>5:</b> Umiarkowana reakcja lub dyskomfort.</li>"
            "<li><b>10:</b> Skrajna reakcja lub dyskomfort, w tym objawy fizyczne.</li>"
            "</ul>"
            "Prosimy o udzielanie odpowiedzi jak najbardziej szczerze, na podstawie swoich obecnych lub niedawnych doświadczeń.<br><br>"
            "<b>Naciśnij dowolny klawisz, aby przejść do kwestionariusza.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        """Przechodzenie do widoku Misophonia po naciśnięciu dowolnego klawisza."""
        self.main_app.show_misophonia()

