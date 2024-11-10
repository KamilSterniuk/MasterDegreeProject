from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTextEdit, QFormLayout
from PySide6.QtGui import QPalette, QColor, QIntValidator
from PySide6.QtCore import Qt


class SurveyWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout centrowany
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Nagłówek ankiety
        header_label = QLabel("User Survey")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Layout formularza ankiety, aby był mniejszy i centrowany
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
        additional_info_label = QLabel("Additional Informations:")
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
        main_layout.addWidget(form_container, alignment=Qt.AlignCenter)

        # Przycisk "Next" do przejścia do kolejnego widoku
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
        main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        # Przycisk Powrót
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
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # Ustawienie głównego layoutu
        self.setLayout(main_layout)

    def check_form_completion(self):
        age_filled = self.age_input.hasAcceptableInput()
        gender_selected = self.gender_combo.currentIndex() != 0
        self.next_button.setVisible(age_filled and gender_selected)

    def go_to_next_view(self):
        # Przejście do StaiWindow
        self.main_app.show_stai()

    def on_back(self):
        # Powrót do ekranu głównego
        self.main_app.show_main()
