from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class TrialInProgressView(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.is_trial = True  # Domyślnie uruchamiany jest test próbny

        # Ustawienie tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#C0C0C0"))  # Szare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Wiadomość o trwającym teście
        self.message_label = QLabel("Test in progress, please wait...")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 24px; color: #333333; font-weight: bold; padding: 20px;")
        self.layout.addWidget(self.message_label)

    def show_completion_message(self):
        """Zmienia tekst na wiadomość o zakończeniu całego testu."""
        self.message_label.setText(
            "Thank you for completing the ANT test.\n\n"
            "Now, I would like to ask you to complete the STAI questionnaire once more\n"
            "to evaluate how your mood has changed.\n\n"
            "Please take your time and answer the questions thoughtfully.\n\n"
            "Press any key to continue."
        )

    def keyPressEvent(self, event):
        """Obsługuje naciśnięcie klawisza po zakończeniu testu."""
        if "Thank you for completing the ANT test" in self.message_label.text():
            self.main_app.show_stai_post_ant()  # Przejście do STAI Post-ANT Window

    def start_test(self):
        """Uruchamia test próbny, który automatycznie przejdzie do głównego testu."""
        print("Starting ANT test (trial + main)...")
        try:
            from ant_test import trial_ant_test
            trial_ant_test()  # Uruchamia oba testy
        except Exception as e:
            print(f"Error during ANT tests: {e}")
        self.show_completion_message()

