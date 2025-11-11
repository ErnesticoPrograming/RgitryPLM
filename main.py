# main.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from db.modules import setup_database, add_pigeon, get_all_pigeons

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("REGISTRYPLM 🕊️")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QLineEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4f46e5;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QLabel {
                font-weight: bold;
                color: #4f46e5;
            }
        """)

        layout = QVBoxLayout()

        self.ring_input = QLineEdit()
        self.ring_input.setPlaceholderText("Número de anillo")
        layout.addWidget(self.ring_input)

        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Color")
        layout.addWidget(self.color_input)

        self.breed_input = QLineEdit()
        self.breed_input.setPlaceholderText("Raza")
        layout.addWidget(self.breed_input)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notas")
        layout.addWidget(self.notes_input)

        self.add_button = QPushButton("Añadir Paloma")
        self.add_button.clicked.connect(self.add_pigeon)
        layout.addWidget(self.add_button)

        self.result_label = QLabel("Palomas registradas:")
        layout.addWidget(self.result_label)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.refresh_pigeons()

    def add_pigeon(self):
        data = {
            "ring_number": self.ring_input.text(),
            "color": self.color_input.text(),
            "breed": self.breed_input.text(),
            "notes": self.notes_input.toPlainText()
        }
        add_pigeon(data)
        self.ring_input.clear()
        self.color_input.clear()
        self.breed_input.clear()
        self.notes_input.clear()
        self.refresh_pigeons()

    def refresh_pigeons(self):
        pigeons = get_all_pigeons()
        text = "\n".join([f"{p.ring_number} - {p.color} - {p.breed}" for p in pigeons])
        self.result_area.setText(text)

if __name__ == "__main__":
    setup_database()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()