from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTextEdit, QFormLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QPalette, QColor, QIntValidator, QPixmap, QIcon
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
        """Wyświetla ekran powitalny w spójnym stylu z innymi instrukcjami."""
        # Czyszczenie głównego layoutu
        self.clear_layout(self.main_layout)

        # Tytuł
        title_label = QLabel("Welcome to the Attention Concentration Study")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Instrukcja
        instructions_label = QLabel()
        instructions_label.setTextFormat(Qt.TextFormat.RichText)  # Użycie HTML dla formatowania
        instructions_label.setText(
            "<p style='font-size: 20px; color: #BBBBBB; text-align: center;'>"
            "Thank you for participating in the <b>Attention Concentration Study</b>, which uses "
            "Eye-Tracking and EEG to better understand focus and cognitive engagement.<br><br>"
            "Before starting, you will complete a short survey where we will ask you to provide details such as:"
            "<ul style='text-align: left;'>"
            "<li>Your <b>gender</b> and <b>age</b>.</li>"
            "<li>Your <b>nationality</b> and <b>native language</b>.</li>"
            "<li>Any <b>relevant information</b> about your mood or recent experiences, "
            "such as exams, stress, achievements, or personal milestones.</li>"
            "</ul>"
            "Your data will remain <b>anonymous</b> and <b>confidential</b>, and will help us improve our understanding "
            "of attention and concentration.<br><br>"
            "<b>Press any key to continue to the survey.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(instructions_label)

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

        # Narodowość
        nationality_label = QLabel("Nationality:")
        nationality_label.setStyleSheet("color: white; font-size: 16px;")
        self.nationality_combo = QComboBox()
        self.nationality_combo.addItem("Select")  # Dodanie opcji "Select" jako pierwszej
        self.add_countries_with_flags(
            self.nationality_combo,
            ["Poland", "Ukraine", "Belarus", "Germany", "Spain", "France", "Italy", "China", "India", "Turkey",
             "Brazil", "Iran", "Other"]
        )
        self.nationality_combo.currentIndexChanged.connect(self.check_form_completion)
        self.custom_nationality_input = QLineEdit()
        self.custom_nationality_input.setPlaceholderText("Enter your nationality")
        self.custom_nationality_input.setVisible(False)
        form_layout.addRow(nationality_label, self.nationality_combo)
        form_layout.addRow(self.custom_nationality_input)

        # Język ojczysty
        modern_tongue_label = QLabel("Modern Tongue Language:")
        modern_tongue_label.setStyleSheet("color: white; font-size: 16px;")
        self.tongue_combo = QComboBox()
        self.tongue_combo.addItem("Select")  # Dodanie opcji "Select" jako pierwszej
        self.tongue_combo.addItems(
            ["Polish", "English", "Russian", "Ukrainian", "Belarusian", "German", "Spanish", "French", "Italian",
             "Chinese", "Hindi", "Turkish", "Portuguese", "Arabic", "Persian (Farsi)", "Other"]
        )
        self.tongue_combo.currentIndexChanged.connect(self.check_form_completion)
        self.custom_tongue_input = QLineEdit()
        self.custom_tongue_input.setPlaceholderText("Enter your language")
        self.custom_tongue_input.setVisible(False)
        form_layout.addRow(modern_tongue_label, self.tongue_combo)
        form_layout.addRow(self.custom_tongue_input)

        # Dodatkowe informacje
        additional_info_label = QLabel("Additional Information:")
        additional_info_label.setStyleSheet("color: white; font-size: 16px;")
        self.additional_info_input = QTextEdit()
        self.additional_info_input.setPlaceholderText(
            "Feel free to share any relevant information about your current mood, "
            "recent significant events such as exams, stress, excitement about an upcoming concert or football match, "
            "achievements like a good grade on an exam, or personal experiences like falling in love. "
            "Your input will help us better understand your context."
        )

        self.additional_info_input.setFixedSize(450, 100)
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

    def add_countries_with_flags(self, combo_box, countries):
        """
        Dodaje kraje z flagami do QComboBox. Jeśli flaga nie istnieje, dodaje tylko nazwę kraju.
        """
        for country in countries:
            # Tworzenie ścieżki do obrazu flagi
            flag_path = f"flags/{country.lower().replace(' ', '_')}.png"
            if os.path.exists(flag_path):
                # Ładowanie obrazu flagi
                pixmap = QPixmap(flag_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # Tworzenie ikony i dodawanie do combo box
                combo_box.addItem(QIcon(pixmap), country)
            else:
                # Jeśli flaga nie istnieje, dodaj tylko nazwę kraju
                combo_box.addItem(country)

    def check_form_completion(self):
        """Sprawdza, czy wszystkie wymagane pola są wypełnione, aby aktywować przycisk Next."""
        age_filled = self.age_input.hasAcceptableInput()
        gender_selected = self.gender_combo.currentText() != "Select"
        nationality_selected = (
                self.nationality_combo.currentText() != "Select" and
                (self.nationality_combo.currentText() != "Other" or self.custom_nationality_input.text().strip())
        )
        tongue_selected = (
                self.tongue_combo.currentText() != "Select" and
                (self.tongue_combo.currentText() != "Other" or self.custom_tongue_input.text().strip())
        )
        # Ustawienie widoczności przycisku Next
        self.next_button.setVisible(age_filled and gender_selected and nationality_selected and tongue_selected)

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

    def toggle_custom_nationality_field(self):
        """Pokazuje lub ukrywa pole tekstowe dla własnej narodowości i sprawdza wypełnienie formularza."""
        is_other_selected = self.nationality_combo.currentText() == "Other"
        self.custom_nationality_input.setVisible(is_other_selected)
        self.custom_nationality_input.textChanged.connect(self.check_form_completion)

    def toggle_custom_tongue_field(self):
        """Pokazuje lub ukrywa pole tekstowe dla własnego języka ojczystego i sprawdza wypełnienie formularza."""
        is_other_selected = self.tongue_combo.currentText() == "Other"
        self.custom_tongue_input.setVisible(is_other_selected)
        self.custom_tongue_input.textChanged.connect(self.check_form_completion)

    def save_survey_data_to_csv(self, file_path):
        """Zapisuje dane ankiety do pliku CSV."""
        # Pobieranie danych z formularza
        gender = self.gender_combo.currentText()
        age = self.age_input.text()
        nationality = self.custom_nationality_input.text() if self.nationality_combo.currentText() == "Other" else self.nationality_combo.currentText()
        modern_tongue = self.custom_tongue_input.text() if self.tongue_combo.currentText() == "Other" else self.tongue_combo.currentText()
        additional_info = self.additional_info_input.toPlainText()

        # Informacja o grupie
        group = "ASMR" if self.main_app.asmr_enabled else "Control"

        # Dane do zapisania (Group jako pierwsze)
        data = [
            ["Field", "Value"],
            ["Group", group],
            ["Gender", gender],
            ["Age", age],
            ["Nationality", nationality],
            ["Modern Tongue Language", modern_tongue],
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
        if self.main_layout.count() == 2:  # Jeśli wyświetlany jest ekran powitalny
            self.show_survey_form()

    def clear_layout(self, layout):
        # Usuwanie wszystkich widgetów z layoutu
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
