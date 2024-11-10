from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QHBoxLayout, QScrollArea, \
    QPushButton, QFormLayout
from PySide6.QtCore import Qt


class StaiWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Tworzenie głównego layoutu i tytułu
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Tytuł okna
        title_label = QLabel("STAI Questionnaire")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; padding: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Etykieta do wyświetlania statusu ASMR
        self.asm_label = QLabel()
        self.asm_label.setStyleSheet("font-size: 16px; color: #555; padding: 5px;")
        self.asm_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.asm_label)

        # Lista pytań STAI
        questions = [
            "I feel calm", "I feel secure", "I feel tense", "I feel strained", "I feel at ease",
            "I feel upset", "I am presently worrying over possible misfortunes", "I feel satisfied",
            "I feel frightened", "I feel uncomfortable", "I feel self-confident", "I feel nervous",
            "I feel jittery", "I feel indecisive", "I am relaxed", "I feel content", "I am worried",
            "I feel confused", "I feel steady", "I feel pleasant"
        ]

        # Tworzenie form layout do pytań
        form_layout = QFormLayout()

        # Dodanie pytań i opcji odpowiedzi
        self.button_groups = []  # Przechowywanie grup przycisków dla każdej odpowiedzi
        for i, question in enumerate(questions, start=1):
            question_label = QLabel(f"{i}. {question}")
            question_label.setStyleSheet("color: #333; font-size: 18px; padding-right: 10px;")

            # Grupa przycisków radiowych
            button_group = QButtonGroup(self)
            button_layout = QHBoxLayout()
            button_layout.setSpacing(20)  # Większy odstęp między opcjami

            for j in range(1, 5):
                radio_button = QRadioButton(str(j))
                radio_button.setStyleSheet("font-size: 16px; padding: 5px;")
                button_group.addButton(radio_button)
                button_layout.addWidget(radio_button)

            self.button_groups.append(button_group)

            # Dodanie pytania do form layout
            form_layout.addRow(question_label, button_layout)

        # Dodanie form layout do scroll area (jeśli pytań jest dużo)
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Przycisk "Submit" do zapisania odpowiedzi
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        submit_button.clicked.connect(self.submit_answers)
        main_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        # Ustawienie głównego layoutu
        self.setLayout(main_layout)

    def update_asmr_status(self, asmr_enabled):
        # Aktualizacja etykiety z informacją o statusie ASMR
        asmr_status = "ASMR Mode is ON" if asmr_enabled else "ASMR Mode is OFF"
        self.asm_label.setText(f"ASMR Status: {asmr_status}")

    def submit_answers(self):
        # Zbieranie odpowiedzi z pytań STAI
        answers = []
        for group in self.button_groups:
            selected_button = group.checkedButton()
            if selected_button:
                answers.append(selected_button.text())
            else:
                answers.append("No response")  # Obsługa braku odpowiedzi

        # Wyświetlenie odpowiedzi w konsoli (lub można zapisać do pliku/bazy danych)
        print("STAI Answers:", answers)
