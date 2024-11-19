from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # Marginesy wokół całego okna
        main_layout.setSpacing(10)

        # Layout dla górnego paska
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignRight)

        # Napis "Choose Language"
        language_label = QLabel("Choose Language")
        language_label.setStyleSheet("color: white; font-size: 16px; margin-right: 10px;")
        language_label.setAlignment(Qt.AlignCenter)
        top_bar_layout.addWidget(language_label)

        # Przycisk zmiany języka
        self.language_button = QPushButton("English")
        self.language_button.setCheckable(True)
        self.language_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                margin: 5px;
            }
            QPushButton:checked {
                background-color: #0056b3;
            }
        """)
        self.language_button.toggled.connect(self.toggle_language)
        top_bar_layout.addWidget(self.language_button)

        # Dodanie górnego paska do głównego layoutu
        main_layout.addLayout(top_bar_layout)

        # Środkowy układ dla przycisków
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(20)

        # Styl przycisków
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 10px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        # Przycisk Start
        start_button = QPushButton("Start")
        start_button.setStyleSheet(button_style)
        start_button.clicked.connect(self.on_start)
        center_layout.addWidget(start_button)

        # Przycisk Settings
        settings_button = QPushButton("Settings")
        settings_button.setStyleSheet(button_style)
        settings_button.clicked.connect(self.on_settings)
        center_layout.addWidget(settings_button)

        # Przycisk Exit
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 10px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        exit_button.clicked.connect(self.on_exit)
        center_layout.addWidget(exit_button)

        # Dodanie środkowego układu do głównego layoutu
        main_layout.addLayout(center_layout)

        # Ustawienie głównego layoutu
        self.setLayout(main_layout)

    def toggle_language(self, checked):
        # Zmiana etykiety na przycisku języka
        self.language_button.setText("Polish" if checked else "English")

    def on_start(self):
        # Przejdź do ekranu ankiety
        self.main_app.show_start()

    def on_settings(self):
        # Wyświetlenie dialogu hasła
        password_dialog = PasswordDialog(self)
        if password_dialog.exec() == QDialog.Accepted:
            # Jeśli hasło poprawne, przejście do ustawień
            self.main_app.show_settings()
        else:
            # Jeśli hasło niepoprawne lub anulowane, nic się nie dzieje
            pass

    def on_exit(self):
        # Zamyka aplikację
        self.main_app.close()


from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter Password")
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)  # Usuń domyślną ramkę okna

        # Stylizacja tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Informacja o dostępie
        info_label = QLabel("Access to the settings is restricted to project staff only.")
        info_label.setStyleSheet("color: #FFDD44; font-size: 20px; font-weight: bold;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        # Nagłówek
        self.label = QLabel("Please enter the password")
        self.label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Pole do wpisania hasła
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #444;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #555;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #007BFF;
            }
        """)
        layout.addWidget(self.password_input)

        # Layout dla przycisków
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # Przycisk Zatwierdź
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("""
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
        self.submit_button.clicked.connect(self.check_password)
        button_layout.addWidget(self.submit_button)

        # Przycisk Anuluj
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
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
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        # Dodanie układu przycisków do głównego układu
        layout.addLayout(button_layout)

        # Ustawienie głównego layoutu
        self.setLayout(layout)

    def check_password(self):
        # Sprawdzenie poprawności hasła
        if self.password_input.text() == "eeg2025":  # Przykładowe hasło
            self.accept()  # Zamknij dialog i zwróć sukces
        else:
            self.label.setText("Incorrect password. Try again.")
            self.label.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
