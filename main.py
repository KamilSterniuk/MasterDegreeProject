import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QVBoxLayout, QWidget
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from ui.survey_window import SurveyWindow
from ui.stai_window import StaiWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attention Concentration Test with EEG and Eye-Tracking")
        self.showFullScreen()

        # Przechowywanie stanu ASMR
        self.asmr_enabled = False

        # Stwórz widget do przełączania pomiędzy ekranami
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Inicjalizacja ekranów
        self.main_window = MainWindow(self)
        self.settings_window = SettingsWindow(self)
        self.survey_window = SurveyWindow(self)
        self.stai_window = StaiWindow(self)

        # Dodaj tytuł na górze
        title_label = QLabel("Attention Concentration Test with EEG and Eye-Tracking")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        title_widget = QWidget()
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.stacked_widget)
        title_widget.setLayout(title_layout)
        self.setCentralWidget(title_widget)

        # Dodaj ekrany do stosu widgetów
        self.stacked_widget.addWidget(self.main_window)
        self.stacked_widget.addWidget(self.settings_window)
        self.stacked_widget.addWidget(self.survey_window)
        self.stacked_widget.addWidget(self.stai_window)

        # Wyświetl ekran główny
        self.stacked_widget.setCurrentWidget(self.main_window)

    def show_main(self):
        self.stacked_widget.setCurrentWidget(self.main_window)

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_window)

    def show_start(self):
        self.stacked_widget.setCurrentWidget(self.survey_window)

    def show_stai(self):
        # Sprawdzenie aktualnego stanu ASMR przed przejściem do STAI
        print(f"Switching to STAI view with ASMR Mode: {self.asmr_enabled}")
        self.stai_window.update_asmr_status(self.asmr_enabled)
        self.stacked_widget.setCurrentWidget(self.stai_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
