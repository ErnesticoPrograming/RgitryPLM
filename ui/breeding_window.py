from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QMessageBox
)
from modules import add_breeding_pair, add_offspring, get_offspring_by_pair

class BreedingWindow(QDialog):
    def __init__(self, pigeons):
        super().__init__()
        self.setWindowTitle("Cría y pichones")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        self.male_select = QComboBox()
        self.female_select = QComboBox()
        for p in pigeons:
            self.male_select.addItem(f"{p.ring_number} ({p.color})", p.id)
            self.female_select.addItem(f"{p.ring_number} ({p.color})", p.id)

        layout.addWidget(QLabel("Macho:"))
        layout.addWidget(self.male_select)
        layout.addWidget(QLabel("Hembra:"))
        layout.addWidget(self.female_select)

        self.pair_button = QPushButton("Registrar pareja")
        self.pair_button.clicked.connect(self.save_pair)
        layout.addWidget(self.pair_button)

        self.offspring_ring = QLineEdit()
        self.offspring_ring.setPlaceholderText("Anillo del pichón")
        layout.addWidget(self.offspring_ring)

        self.offspring_notes = QTextEdit()
        self.offspring_notes.setPlaceholderText("Notas del pichón")
        layout.addWidget(self.offspring_notes)

        self.offspring_button = QPushButton("Añadir pichón")
        self.offspring_button.clicked.connect(self.save_offspring)
        layout.addWidget(self.offspring_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(QLabel("Pichones registrados:"))
        layout.addWidget(self.result_area)

        self.setLayout(layout)
        self.refresh_offspring()

    def save_pair(self):
        male_id = self.male_select.currentData()
        female_id = self.female_select.currentData()
        add_breeding_pair(male_id, female_id)
        QMessageBox.information(self, "Éxito", "Pareja registrada.")

    def save_offspring(self):
        ring = self.offspring_ring.text()
        notes = self.offspring_notes.toPlainText()
        add_offspring(ring, None, notes)
        self.offspring_ring.clear()
        self.offspring_notes.clear()
        self.refresh_offspring()

    def refresh_offspring(self):
        offspring = get_offspring_by_pair(None)
        text = "\n".join([f"{o.ring_number} - {o.notes}" for o in offspring])
        self.result_area.setText(text)