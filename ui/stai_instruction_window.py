from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class StaiInstructionWindow(QWidget):
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
        title_label = QLabel("Instructions for the STAI Questionnaire")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Instrukcja
        instructions_label = QLabel()
        instructions_label.setTextFormat(Qt.TextFormat.RichText)  # Użycie HTML dla formatowania
        instructions_label.setText(
            "<p style='font-size: 20px; color: #BBBBBB; text-align: center;'>"
            "The <b>State-Trait Anxiety Inventory (STAI)</b> is a self-evaluation questionnaire designed to assess "
            "how you feel at the moment.<br><br>"
            "You will answer <b>20 questions</b> about your current feelings. "
            "For each question, select the answer that best describes your experience, using the following scale:<br>"
            "<ul style='text-align: left;'>"
            "<li><b>1:</b> Not at all</li>"
            "<li><b>2:</b> A little</li>"
            "<li><b>3:</b> Somewhat</li>"
            "<li><b>4:</b> Very much so</li>"
            "</ul>"
            "Please answer all questions honestly to ensure accurate results.<br><br>"
            "<b>Press any key to proceed to the questionnaire.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        """Przechodzenie do widoku STAI po naciśnięciu dowolnego klawisza."""
        self.main_app.show_stai()
