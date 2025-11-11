# main.py
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox,
    QComboBox, QDialog
)
from modules import (
    setup_database, add_pigeon, get_all_pigeons, update_pigeon, delete_pigeon,
    add_capture, get_captures_by_pigeon,
    add_breeding_pair, get_all_pairs, add_offspring, get_offspring_by_pair
)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("REGISTRYPLM 🕊️")
        self.setFixedSize(700, 800)
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

        self.selected_id = None
        layout = QVBoxLayout()

        # Formulario de paloma
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

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Añadir / Actualizar")
        self.add_button.clicked.connect(self.add_or_update_pigeon)
        button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_selected_pigeon)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        # Lista de palomas
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.load_pigeon)
        layout.addWidget(QLabel("Palomas registradas:"))
        layout.addWidget(self.list_widget)

        # Formulario de captura
        self.capture_location = QLineEdit()
        self.capture_location.setPlaceholderText("Lugar de captura")
        layout.addWidget(self.capture_location)

        self.capture_date = QLineEdit()
        self.capture_date.setPlaceholderText("Fecha (YYYY-MM-DD)")
        layout.addWidget(self.capture_date)

        self.capture_count = QLineEdit()
        self.capture_count.setPlaceholderText("Número de veces capturada")
        layout.addWidget(self.capture_count)

        self.capture_button = QPushButton("Registrar captura")
        self.capture_button.clicked.connect(self.register_capture)
        layout.addWidget(self.capture_button)

        self.capture_area = QTextEdit()
        self.capture_area.setReadOnly(True)
        layout.addWidget(QLabel("Historial de capturas:"))
        layout.addWidget(self.capture_area)

        # Botón para abrir módulo de cría
        self.breeding_button = QPushButton("Abrir módulo de cría")
        self.breeding_button.clicked.connect(self.open_breeding)
        layout.addWidget(self.breeding_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.refresh_list()

    def add_or_update_pigeon(self):
        data = {
            "ring_number": self.ring_input.text(),
            "color": self.color_input.text(),
            "breed": self.breed_input.text(),
            "notes": self.notes_input.toPlainText()
        }
        if self.selected_id:
            update_pigeon(self.selected_id, data)
        else:
            add_pigeon(data)
        self.clear_form()
        self.refresh_list()

    def load_pigeon(self, item):
        pigeon = item.data(100)
        self.selected_id = pigeon.id
        self.ring_input.setText(pigeon.ring_number)
        self.color_input.setText(pigeon.color)
        self.breed_input.setText(pigeon.breed)
        self.notes_input.setText(pigeon.notes)
        self.refresh_captures()

    def delete_selected_pigeon(self):
        if self.selected_id:
            confirm = QMessageBox.question(self, "Confirmar eliminación",
                "¿Estás seguro de que deseas eliminar esta paloma?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                delete_pigeon(self.selected_id)
                self.clear_form()
                self.refresh_list()
                self.capture_area.clear()

    def register_capture(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Sin selección", "Selecciona una paloma primero.")
            return
        location = self.capture_location.text()
        date = self.capture_date.text()
        try:
            count = int(self.capture_count.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "El número de veces debe ser un entero.")
            return
        add_capture(self.selected_id, location, date, count)
        self.capture_location.clear()
        self.capture_date.clear()
        self.capture_count.clear()
        self.refresh_captures()

    def refresh_captures(self):
        if not self.selected_id:
            self.capture_area.setText("")
            return
        captures = get_captures_by_pigeon(self.selected_id)
        text = "\n".join([f"{c.date} - {c.location} ({c.count} veces)" for c in captures])
        self.capture_area.setText(text)

    def clear_form(self):
        self.selected_id = None
        self.ring_input.clear()
        self.color_input.clear()
        self.breed_input.clear()
        self.notes_input.clear()

    def refresh_list(self):
        self.list_widget.clear()
        for p in get_all_pigeons():
            item = QListWidgetItem(f"{p.ring_number} - {p.color} - {p.breed}")
            item.setData(100, p)
            self.list_widget.addItem(item)

    def open_breeding(self):
        pigeons = get_all_pigeons()
        dialog = BreedingWindow(pigeons)
        dialog.exec()
    
from PyQt6.QtWidgets import QFileDialog
from modules import export_pigeon_pdf

def export_pdf(self):
    if not self.selected_id:
        QMessageBox.warning(self, "Sin selección", "Selecciona una paloma primero.")
        return

    pigeon = next(p for p in get_all_pigeons() if p.id == self.selected_id)
    captures = get_captures_by_pigeon(self.selected_id)

    path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", f"{pigeon.ring_number}.pdf", "PDF Files (*.pdf)")
    if path:
        export_pigeon_pdf(pigeon, captures, path)
        QMessageBox.information(self, "Éxito", "Ficha exportada correctamente.")
        
if __name__ == "__main__":
    setup_database()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()