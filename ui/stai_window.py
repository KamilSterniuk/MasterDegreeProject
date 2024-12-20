import csv
import os

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QButtonGroup, QScrollArea, \
    QPushButton, QFormLayout, QFrame
from PySide6.QtCore import Qt


class StaiWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła dla całego okna (z wyjątkiem form_layout)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Tytuł
        title_label = QLabel("STAI Questionnaire")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Etykieta statusu ASMR
        self.asm_label = QLabel()
        self.asm_label.setStyleSheet("font-size: 16px; color: #BBBBBB; padding: 5px;")  # Jaśniejszy szary kolor
        self.asm_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.asm_label)

        # Instrukcja ogólna nad oznaczeniami
        general_instruction_label = QLabel(
            "Answer the questions according to the following scale, indicating how you feel.")
        general_instruction_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #BBBBBB; padding: 10px;")
        general_instruction_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(general_instruction_label)

        # Instrukcja dla przycisków radiowych jako jeden wiersz
        instruction_label = QLabel("1: Not at all    2: A little    3: Somewhat    4: Very Much So")
        instruction_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #BBBBBB; padding: 5px;")
        instruction_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instruction_label)

        # Lista pytań STAI
        questions = [
            "I feel calm", "I feel secure", "I feel tense", "I feel strained", "I feel at ease",
            "I feel upset", "I am presently worrying over possible misfortunes", "I feel satisfied",
            "I feel frightened", "I feel uncomfortable", "I feel self-confident", "I feel nervous",
            "I feel jittery", "I feel indecisive", "I am relaxed", "I feel content", "I am worried",
            "I feel confused", "I feel steady", "I feel pleasant"
        ]

        # Layout formularza - pozostaje bez zmian
        form_layout = QFormLayout()

        # Dodanie pytań, opcji odpowiedzi i poziomej linii
        self.button_groups = []
        for i, question in enumerate(questions, start=1):
            question_label = QLabel(f"{i}. {question}")
            question_label.setStyleSheet(
                "color: #333333; font-size: 18px; padding-right: 10px;")  # Kolor tekstu pytań w ciemnym odcieniu

            button_group = QButtonGroup(self)
            button_layout = QHBoxLayout()
            button_layout.setSpacing(20)

            for j in range(1, 5):
                radio_button = QRadioButton(str(j))
                radio_button.setStyleSheet(
                    "color: #333333; font-size: 16px; padding: 3px;")  # Kolor tekstu przycisków radiowych
                radio_button.toggled.connect(self.check_all_answers_filled)  # Połącz z funkcją sprawdzającą
                button_group.addButton(radio_button)
                button_layout.addWidget(radio_button)

            self.button_groups.append(button_group)

            # Dodanie pytania i opcji do layoutu
            form_layout.addRow(question_label, button_layout)

            # Dodanie poziomej linii
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #CCCCCC;")  # Szara linia oddzielająca pytania
            form_layout.addRow(line)

        # Dodanie form layout do scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Layout dla przycisków "Back" i "Submit"
        button_layout = QHBoxLayout()

        # Przycisk "Back"
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        back_button.clicked.connect(self.main_app.show_start)  # Zmiana, aby wracać do okna Survey
        button_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Przycisk "Submit" (ukryty do czasu wypełnienia wszystkich odpowiedzi)
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_button.clicked.connect(self.submit_answers)
        self.submit_button.setVisible(False)  # Ukryj przycisk na początku
        button_layout.addWidget(self.submit_button, alignment=Qt.AlignRight)

        # Dodanie układu przycisków do głównego layoutu
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def update_asmr_status(self, asmr_enabled):
        asmr_status = "ASMR Mode is ON" if asmr_enabled else "ASMR Mode is OFF"
        self.asm_label.setText(f"ASMR Status: {asmr_status}")

    def check_all_answers_filled(self):
        # Sprawdzenie, czy wszystkie pytania mają odpowiedź
        all_answered = all(group.checkedButton() is not None for group in self.button_groups)
        self.submit_button.setVisible(all_answered)  # Pokaż przycisk tylko, jeśli wszystkie odpowiedzi są udzielone

    def submit_answers(self):
        # Zbieranie odpowiedzi
        answers = []
        for group in self.button_groups:
            selected_button = group.checkedButton()
            if selected_button:
                answers.append(selected_button.text())
            else:
                answers.append("No response")

        print("STAI Answers:", answers)

        # Zapisywanie odpowiedzi do pliku CSV
        self.save_stai_data_to_csv(answers)

        # Przeniesienie do odpowiedniego okna w zależności od stanu ASMR
        self.main_app.show_rest_or_asmr()

    def save_stai_data_to_csv(self, answers):
        """Zapisuje odpowiedzi STAI do pliku CSV w katalogu o najwyższym numerze."""
        results_dir = "results"

        if not os.path.exists(results_dir):
            print("Results directory does not exist.")
            return

        # Znalezienie katalogu o najwyższym numerze
        existing_folders = [
            folder for folder in os.listdir(results_dir) if folder.startswith("example") and folder[7:].isdigit()
        ]
        if not existing_folders:
            print("No example directories found in results.")
            return

        max_number = max(int(folder[7:]) for folder in existing_folders)
        target_folder = os.path.join(results_dir, f"example{max_number}")

        # Ścieżka do pliku CSV
        csv_file_path = os.path.join(target_folder, "stai_data.csv")

        # Zapis danych do pliku CSV
        with open(csv_file_path, mode="w", newline='', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=';')  # Ustawienie separatora na ';'
            writer.writerow(["Question", "Answer"])  # Nagłówki
            for i, answer in enumerate(answers, start=1):
                writer.writerow([f"Q{i}", answer])  # Zapis pytań i odpowiedzi

        print(f"STAI data saved to {csv_file_path}")