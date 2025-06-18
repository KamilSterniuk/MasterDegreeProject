from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QScrollArea, \
    QPushButton, QFormLayout, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
import csv
import os




class StaiPostAntWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)


        # Tytuł
        title_label = QLabel("Kwestionariusz STAI Post-ASMR")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Etykieta informacyjna przed ankietą
        self.info_label = QLabel(
            "<p style='text-align: center; font-size: 18px; color: white;'>"
            "Proszę ponownie wypełnić kwestionariusz STAI,<br>"
            "aby sprawdzić, jak zmieniło się Twoje samopoczucie.<br><br>"
            "<b>Naciśnij dowolny klawisz, aby kontynuować.</b>"
            "</p>"
        )
        self.info_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.info_label)

        # Instrukcja ogólna nad oznaczeniami
        self.general_instruction_label = QLabel(
            "Odpowiedz na pytania zgodnie z poniższą skalą, wskazując, jak się czujesz.")
        self.general_instruction_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #BBBBBB; padding: 0px;")
        self.general_instruction_label.setVisible(False)
        self.general_instruction_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.general_instruction_label)

        # Instrukcja dla przycisków radiowych
        self.instruction_label = QLabel("1: Wcale 2: Trochę 3: Umiarkowanie 4: Bardzo")
        self.instruction_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #BBBBBB; padding: 5px;")
        self.instruction_label.setVisible(False)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.instruction_label)

        # Layout dla ankiety (początkowo ukryty)
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.form_layout = QFormLayout()
        self.scroll_widget.setLayout(self.form_layout)
        self.scroll_widget.setStyleSheet("background-color: #BBBBBB;")
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVisible(False)  # Ukrywamy formularz na początku
        self.main_layout.addWidget(self.scroll_area)

        # Lista pytań STAI
        questions = [
            "Czuję się spokojny", "Czuję się bezpiecznie", "Czuję się spięty", "Czuję się nienaturalnie", "Czuję się swobodnie",
            "Czuję się zdenerwowany", "Obecnie martwię się możliwymi niepowodzeniami", "Czuję się usatysfakcjonowany",
            "Czuję się przestraszony", "Czuję się niekomfortowo", "Czuję się pewny siebie", "Czuję się nerwowo",
            "Czuję się roztrzęsiony", "Czuję się niezdecydowany", "Jestem zrelaksowany", "Czuję się zadowolony", "Jestem zmartwiony",
            "Czuję się zdezorientowany", "Czuję się stabilnie", "Czuję się przyjemnie"
        ]

        # Tworzenie pytań i odpowiedzi
        self.button_groups = []
        for i, question in enumerate(questions, start=1):
            question_label = QLabel(f"{i}. {question}")
            question_label.setStyleSheet("color: #333333; font-size: 18px; padding-right: 10px; background-color: #BBBBBB")

            button_group = QButtonGroup(self)
            button_layout = QHBoxLayout()
            button_layout.setSpacing(20)

            for j in range(1, 5):
                radio_button = QRadioButton(str(j))
                radio_button.setStyleSheet("color: #333333; font-size: 16px; padding: 3px;")
                radio_button.toggled.connect(self.check_all_answers_filled)
                button_group.addButton(radio_button)
                button_layout.addWidget(radio_button)

            self.button_groups.append(button_group)
            self.form_layout.addRow(question_label, button_layout)

            # Linia oddzielająca pytania
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #CCCCCC;")
            self.form_layout.addRow(line)

        # Layout dla przycisków "Back" i "Submit"
        self.button_layout = QHBoxLayout()

        # Przycisk "Back"
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("""
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
        self.back_button.clicked.connect(self.main_app.show_trial_in_progress)
        self.button_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        self.back_button.setVisible(False)  # Ukrywamy przycisk na początku

        # Przycisk "Submit"
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
        self.submit_button.setVisible(False)
        self.button_layout.addWidget(self.submit_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def keyPressEvent(self, event):
        """Obsługuje naciśnięcie klawisza, aby przejść do ankiety."""
        self.show_questionnaire()

    def show_questionnaire(self):
        """Ukrywa ekran informacyjny i pokazuje kwestionariusz."""
        self.info_label.setVisible(False)
        self.general_instruction_label.setVisible(True)
        self.instruction_label.setVisible(True)
        self.scroll_area.setVisible(True)
        self.back_button.setVisible(False)
        self.submit_button.setVisible(False)

    def check_all_answers_filled(self):
        """Sprawdzenie, czy wszystkie pytania mają odpowiedź."""
        all_answered = all(group.checkedButton() is not None for group in self.button_groups)
        self.submit_button.setVisible(all_answered)

    def submit_answers(self):
        """Zapisanie odpowiedzi i przejście do ekranu końcowego."""
        answers = [group.checkedButton().text() if group.checkedButton() else "No response" for group in self.button_groups]
        self.save_stai_data_to_csv(answers)
        self.main_app.show_ant_instructions()
        # self.main_app.show_end_of_study()

    def save_stai_data_to_csv(self, answers):
        """Zapisuje odpowiedzi STAI do pliku CSV."""
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        existing_folders = [folder for folder in os.listdir(results_dir) if folder.startswith("example") and folder[7:].isdigit()]
        max_number = max([int(folder[7:]) for folder in existing_folders], default=0)
        target_folder = os.path.join(results_dir, f"example{max_number}")

        csv_file_path = os.path.join(target_folder, "stai_post_ant_data.csv")

        with open(csv_file_path, "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(["Question", "Answer"])
            for i, answer in enumerate(answers, start=1):
                writer.writerow([f"Q{i}", answer])

        print(f"STAI data saved to {csv_file_path}")
