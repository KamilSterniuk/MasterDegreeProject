from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, QFormLayout, QPushButton
from PySide6.QtGui import QPalette, QColor, QIntValidator
from PySide6.QtCore import Qt
import os
import csv


class SurveyWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Wyświetl ekran powitalny
        self.show_welcome_screen()

        # Ustawienie głównego layoutu
        self.setLayout(self.main_layout)

    def show_welcome_screen(self):
        # Czyszczenie głównego layoutu
        self.clear_layout(self.main_layout)

        # Wiadomość powitalna
        welcome_label = QLabel()
        welcome_label.setTextFormat(Qt.TextFormat.RichText)  # Ustawienie obsługi RichText (HTML)
        welcome_label.setText(
            "<b>Welcome to the Attention Concentration Study using Eye-Tracking and EEG.</b><br><br>"
            "At the beginning, you will be asked to complete a survey where we will ask for your gender and age.<br>"
            "Optionally, you can share additional information about your day or life.<br><br>"
            "All your data will remain anonymous and protected.<br><br>"
            "<b>Press any key to continue.</b>"
        )
        welcome_label.setStyleSheet("color: white; font-size: 18px; padding: 20px;")
        welcome_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(welcome_label)

    def show_survey_form(self):
        # Czyszczenie głównego layoutu
        self.clear_layout(self.main_layout)

        # Nagłówek ankiety
        header_label = QLabel("User Survey")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(header_label)

        # Layout formularza ankiety
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Płeć
        gender_label = QLabel("Gender:")
        gender_label.setStyleSheet("color: white; font-size: 16px;")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Select", "Female", "Male", "Prefer not to say"])
        self.gender_combo.setFixedWidth(120)
        self.gender_combo.currentIndexChanged.connect(self.check_form_completion)
        form_layout.addRow(gender_label, self.gender_combo)

        # Wiek
        age_label = QLabel("Age:")
        age_label.setStyleSheet("color: white; font-size: 16px;")
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter your age")
        self.age_input.setFixedWidth(120)

        # Validator ograniczający wartości tylko do liczb w przedziale 7-100
        age_validator = QIntValidator(7, 100, self)
        self.age_input.setValidator(age_validator)
        self.age_input.textChanged.connect(self.check_form_completion)

        form_layout.addRow(age_label, self.age_input)

        # Dodatkowe informacje
        additional_info_label = QLabel("Additional Information:")
        additional_info_label.setStyleSheet("color: white; font-size: 16px;")
        self.additional_info_input = QTextEdit()
        self.additional_info_input.setPlaceholderText(
            "Any relevant information about your current mood, "
            "recent significant events (e.g., upcoming exams, stress), "
            "or what you're studying or working on if you wish to share."
        )
        self.additional_info_input.setFixedSize(450, 80)
        form_layout.addRow(additional_info_label, self.additional_info_input)

        # Dodanie formularza do głównego layoutu
        form_container = QWidget()
        form_container.setLayout(form_layout)
        form_container.setFixedWidth(650)
        self.main_layout.addWidget(form_container, alignment=Qt.AlignCenter)

        # Przyciski nawigacyjne (Next i Back)
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        # Przycisk "Next"
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.next_button.setFixedWidth(100)
        self.next_button.clicked.connect(self.go_to_next_view)
        self.next_button.setVisible(False)
        button_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        # Przycisk "Back"
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        back_button.setFixedWidth(100)
        back_button.clicked.connect(self.on_back)
        button_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # Dodanie układu przycisków do głównego layoutu
        self.main_layout.addLayout(button_layout)

    def check_form_completion(self):
        age_filled = self.age_input.hasAcceptableInput()
        gender_selected = self.gender_combo.currentIndex() != 0
        self.next_button.setVisible(age_filled and gender_selected)

    def go_to_next_view(self):
        """Przejście do widoku instrukcji STAI, utworzenie nowego katalogu w results i zapisanie danych do CSV."""
        # Tworzenie nowego katalogu w 'results'
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Szukanie najwyższego numeru katalogu
        existing_folders = [
            folder for folder in os.listdir(results_dir) if folder.startswith("example") and folder[7:].isdigit()
        ]
        if existing_folders:
            max_number = max(int(folder[7:]) for folder in existing_folders)
        else:
            max_number = 0

        # Tworzenie nowego katalogu
        new_folder_name = f"example{max_number + 1}"
        new_folder_path = os.path.join(results_dir, new_folder_name)
        os.makedirs(new_folder_path)
        print(f"Created new directory: {new_folder_path}")

        # Zapisywanie danych do pliku CSV
        csv_file_path = os.path.join(new_folder_path, "survey_data.csv")
        self.save_survey_data_to_csv(csv_file_path)

        # Przejście do kolejnego widoku
        self.main_app.show_misophonia_instructions()

    def save_survey_data_to_csv(self, file_path):
        """Zapisuje dane ankiety do pliku CSV."""
        # Pobieranie danych z formularza
        gender = self.gender_combo.currentText()
        age = self.age_input.text()
        additional_info = self.additional_info_input.toPlainText()

        # Informacja o grupie
        group = "ASMR" if self.main_app.asmr_enabled else "Control"

        # Dane do zapisania (Group jako pierwsze)
        data = [
            ["Field", "Value"],
            ["Group", group],
            ["Gender", gender],
            ["Age", age],
            ["Additional Information", additional_info]
        ]

        # Tworzenie pliku CSV
        with open(file_path, mode="w", newline='', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerows(data)

        print(f"Survey data saved to {file_path}")

    def on_back(self):
        # Powrót do ekranu głównego
        self.main_app.show_main()

    def keyPressEvent(self, event):
        # Obsługa naciśnięcia dowolnego klawisza
        if self.main_layout.count() == 1:  # Jeśli wyświetlany jest ekran powitalny
            self.show_survey_form()

    def clear_layout(self, layout):
        # Usuwanie wszystkich widgetów z layoutu
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
