import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QVBoxLayout, QWidget
from ui.main_window import MainWindow
from ui.settings_window import SettingsWindow
from ui.survey_window import SurveyWindow
from ui.stai_window import StaiWindow
from ui.rest_window import RestWindow
from ui.asmr_select_window import AsmrSelectWindow
from ui.ant_instruction_window import AntInstructionWindow
from ui.ant_trial_in_progress_window import TrialInProgressView


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attention Concentration Test with EEG and Eye-Tracking")
        self.showFullScreen()

        # Dodanie atrybutu ASMR
        self.asmr_enabled = False  # Domyślnie ASMR jest wyłączone

        # Tworzenie widgetu do przełączania ekranów
        self.stacked_widget = QStackedWidget()

        # Dodanie tytułu na górze aplikacji
        title_label = QLabel("Attention Concentration Test with EEG and Eye-Tracking")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        title_widget = QWidget()
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.stacked_widget)
        title_widget.setLayout(title_layout)
        self.setCentralWidget(title_widget)

        # Inicjalizacja ekranów
        self.main_window = MainWindow(self)
        self.settings_window = SettingsWindow(self)
        self.survey_window = SurveyWindow(self)
        self.stai_window = StaiWindow(self)
        self.rest_window = RestWindow(self)
        self.asm_select_window = AsmrSelectWindow(self)
        self.ant_instruction_window = AntInstructionWindow(self)
        self.trial_in_progress_view = TrialInProgressView(self)

        # Dodanie ekranów do widgetu stosu
        self.stacked_widget.addWidget(self.main_window)
        self.stacked_widget.addWidget(self.settings_window)
        self.stacked_widget.addWidget(self.survey_window)
        self.stacked_widget.addWidget(self.stai_window)
        self.stacked_widget.addWidget(self.rest_window)
        self.stacked_widget.addWidget(self.asm_select_window)
        self.stacked_widget.addWidget(self.ant_instruction_window)
        self.stacked_widget.addWidget(self.trial_in_progress_view)

        # Wyświetlenie ekranu głównego
        self.stacked_widget.setCurrentWidget(self.main_window)

    def show_main(self):
        """Przełącza na ekran główny."""
        self.stacked_widget.setCurrentWidget(self.main_window)

    def show_settings(self):
        """Przełącza na ekran ustawień."""
        self.stacked_widget.setCurrentWidget(self.settings_window)

    def show_start(self):
        """Przełącza na ekran ankiety."""
        self.stacked_widget.setCurrentWidget(self.survey_window)

    def show_stai(self):
        """Przełącza na ekran STAI."""
        self.stacked_widget.setCurrentWidget(self.stai_window)

    def show_rest_or_asmr(self):
        """Przełącza na ekran odpoczynku lub wybór ASMR."""
        if self.asmr_enabled:
            self.stacked_widget.setCurrentWidget(self.asm_select_window)
        else:
            self.stacked_widget.setCurrentWidget(self.rest_window)

    def show_ant_instructions(self):
        """Przełącza na ekran instrukcji ANT."""
        self.stacked_widget.setCurrentWidget(self.ant_instruction_window)

    def show_trial_in_progress(self, is_trial=True):
        """Przełącza na ekran oczekiwania na zakończenie testu próbnego."""
        self.trial_in_progress_view.is_trial = is_trial
        self.stacked_widget.setCurrentWidget(self.trial_in_progress_view)

    def start_trial_ant_test(self):
        """Rozpoczyna test próbny ANT, który automatycznie przejdzie do głównego testu."""
        print("Starting trial ANT test...")
        self.show_trial_in_progress(is_trial=True)
        self.trial_in_progress_view.start_test()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
