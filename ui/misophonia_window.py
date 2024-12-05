import csv
import os

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QScrollArea, QPushButton, QFormLayout, QFrame, QMessageBox
from PySide6.QtCore import Qt

class MisophoniaWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia okna
        self.setWindowTitle("Misophonia Questionnaire")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Tytuł
        title_label = QLabel("Misophonia Questionnaire")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Instrukcje
        instructions_label = QLabel(
            "Please rate your experience with the following questions about trigger sounds.\n"
            "Move the slider to select the value that best describes your reaction to each question."
        )
        instructions_label.setStyleSheet("font-size: 16px; color: #BBBBBB; padding: 10px;")
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        # Layout formularza
        form_layout = QFormLayout()

        # Lista pytań
        questions = [
            "How uncomfortable do you feel when you hear whispering sounds?",
            "How distressing are soft-spoken voices for you?",
            "How annoying or upsetting do you find sounds like tapping or crinkling?",
            "How strong is your emotional reaction to mouth sounds (e.g., chewing, lip smacking, clicking)?",
            "How tense or anxious do repetitive sounds like whispering or crisp noises make you feel?",
            "How often do you feel a physical reaction (e.g., discomfort, irritation) to these types of sounds?",
            "How likely are you to avoid situations or content with these sounds?",
            "How much do these sounds interfere with your ability to focus or relax?",
            "How strong is your urge to leave or cover your ears when hearing these sounds?",
            "How negatively do these sounds impact your mood (e.g., causing frustration or anger)?"
        ]

        self.responses = []  # Przechowywanie odpowiedzi użytkownika
        self.add_questions(form_layout, questions, self.responses)

        # Dodanie formularza do scroll area
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(form_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Layout dla przycisków
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
        back_button.clicked.connect(self.main_app.show_start)  # Powrót do poprzedniego okna
        button_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Przycisk "Submit"
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("""
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
        submit_button.clicked.connect(self.submit_answers)
        button_layout.addWidget(submit_button, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def add_questions(self, layout, questions, response_list):
        """Dodaje pytania ze sliderami i etykietami wartości do układu."""
        for question in questions:
            question_label = QLabel(question)
            question_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 5px;")

            # Layout dla suwaka i wartości
            slider_layout = QHBoxLayout()

            # Suwak
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(10)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(1)
            slider_layout.addWidget(slider)

            # Etykieta wartości
            value_label = QLabel("0")
            value_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 5px;")
            slider.valueChanged.connect(lambda value, label=value_label: label.setText(str(value)))
            slider_layout.addWidget(value_label)

            response_list.append(slider)

            # Dodanie pytania i suwaka do układu
            layout.addRow(question_label, slider_layout)

            # Linia pozioma
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #BBBBBB;")
            layout.addRow(line)

    def submit_answers(self):
        """Przesyła odpowiedzi użytkownika."""
        scores = self.get_scores(self.responses)

        # Wypisywanie wyników w konsoli
        print("Misophonia Answers:", scores)

        # Zapisywanie wyników do pliku CSV
        self.save_misophonia_data_to_csv(scores)

        # Obliczanie średniego wyniku
        average_score = sum(scores) / len(scores)

        if average_score > 7:
            # Przejście do okna z informacją o wykluczeniu
            self.main_app.show_misophonia_fail()
        else:
            # Przejście do następnego okna
            self.main_app.show_stai_instructions()

    def save_misophonia_data_to_csv(self, scores):
        """Zapisuje odpowiedzi Misophonia do pliku CSV w katalogu o najwyższym numerze."""
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
        csv_file_path = os.path.join(target_folder, "misophonia_data.csv")

        # Zapis danych do pliku CSV
        with open(csv_file_path, mode="w", newline='', encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, delimiter=';')  # Separator na ';'
            writer.writerow(["Question", "Score"])  # Nagłówki
            for i, score in enumerate(scores, start=1):
                writer.writerow([f"Q{i}", score])  # Zapis pytań i odpowiedzi

        print(f"Misophonia data saved to {csv_file_path}")

    def get_scores(self, response_list):
        """Zbiera wyniki z suwaków."""
        return [slider.value() for slider in response_list]