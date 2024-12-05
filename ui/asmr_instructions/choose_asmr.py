from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor


class IntroChooseWindow(QWidget):
    def __init__(self, main_app, best_videos, video_urls, thumbnails):
        super().__init__()
        self.main_app = main_app
        self.best_videos = best_videos
        self.video_urls = video_urls
        self.thumbnails = thumbnails

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Usuń marginesy wokół layoutu
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)  # Wyśrodkowanie wszystkiego

        # Nagłówek
        header_label = QLabel("Final Selection of the Best ASMR Video")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: white; font-weight: bold;")
        header_label.setFont(QFont("Arial", 22))
        layout.addWidget(header_label)

        # Treść instrukcji z użyciem HTML
        instructions = """
        <p style='font-size: 18px; color: #BBBBBB; text-align: center;'>
        You have rated several ASMR videos with the <b>highest score</b>. Now, in this final step,<br>
        you are asked to select <b>one video</b> that you believe is the best among them.<br><br>
        Carefully review the available options and make your selection.<br><br>
        <b>Press any key to proceed to the final selection screen.</b>
        </p>
        """
        instruction_label = QLabel()
        instruction_label.setTextFormat(Qt.TextFormat.RichText)  # Włączenie obsługi HTML
        instruction_label.setText(instructions)
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: white;")
        layout.addWidget(instruction_label)

        # Ustawienie layoutu
        self.setLayout(layout)

    def keyPressEvent(self, event):
        """Obsługa naciśnięcia klawisza."""
        self.main_app.show_best_videos(self.best_videos, self.video_urls, self.thumbnails)
        self.close()
