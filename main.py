from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QListWidget, QComboBox, QTabWidget,
    QFileDialog, QMessageBox
)
from modules import (
    setup_database, get_all_pigeons, get_captures_by_pigeon,
    add_pigeon, update_pigeon, delete_pigeon, export_pigeon_pdf
)

PIGEON_COLORS = ["Todos", "Bayo", "Azul", "Blanco", "Cenizo", "Pinto", "Negro", "Rojo", "Moteado"]
PIGEON_BREEDS = ["Todas", "Mensajera", "De fantasía", "De carrera", "De carne", "De exhibición"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("REGISTRYPLM 🕊️")
        self.setFixedSize(800, 700)
        self.selected_id = None

        self.tabs = QTabWidget()
        self.tab_pigeons = QWidget()
        self.tabs.addTab(self.tab_pigeons, "Palomas")

        layout = QVBoxLayout()

        # 🔍 Filtros
        filter_layout = QHBoxLayout()
        self.search_ring = QLineEdit()
        self.search_ring.setPlaceholderText("Buscar por anillo")
        self.search_ring.textChanged.connect(self.refresh_list)

        self.color_filter = QComboBox()
        self.color_filter.addItems(PIGEON_COLORS)
        self.color_filter.currentTextChanged.connect(self.refresh_list)

        self.breed_filter = QComboBox()
        self.breed_filter.addItems(PIGEON_BREEDS)
        self.breed_filter.currentTextChanged.connect(self.refresh_list)

        filter_layout.addWidget(self.search_ring)
        filter_layout.addWidget(self.color_filter)
        filter_layout.addWidget(self.breed_filter)
        layout.addLayout(filter_layout)

        # 📋 Lista
        self.pigeon_list = QListWidget()
        self.pigeon_list.itemClicked.connect(self.load_pigeon)
        layout.addWidget(QLabel("Palomas registradas:"))
        layout.addWidget(self.pigeon_list)

        # 🕊️ Formulario
        form_layout = QVBoxLayout()
        self.ring_input = QLineEdit()
        self.ring_input.setPlaceholderText("Número de anillo")
        self.color_input = QComboBox()
        self.color_input.addItems(PIGEON_COLORS[1:])  # sin "Todos"
        self.breed_input = QComboBox()
        self.breed_input.addItems(PIGEON_BREEDS[1:])  # sin "Todas"
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notas")

        form_layout.addWidget(self.ring_input)
        form_layout.addWidget(self.color_input)
        form_layout.addWidget(self.breed_input)
        form_layout.addWidget(self.notes_input)

        # 🎯 Botones
        button_row = QHBoxLayout()
        self.add_button = QPushButton("Añadir / Actualizar")
        self.delete_button = QPushButton("Eliminar")
        self.export_button = QPushButton("Exportar PDF")
        self.add_button.clicked.connect(self.add_or_update)
        self.delete_button.clicked.connect(self.delete_selected)
        self.export_button.clicked.connect(self.export_pdf)
        button_row.addWidget(self.add_button)
        button_row.addWidget(self.delete_button)
        button_row.addWidget(self.export_button)
        form_layout.addLayout(button_row)

        layout.addLayout(form_layout)
        self.tab_pigeons.setLayout(layout)
        self.setCentralWidget(self.tabs)
        self.refresh_list()

    def refresh_list(self):
        self.pigeon_list.clear()
        ring_filter = self.search_ring.text().lower()
        color_selected = self.color_filter.currentText()
        breed_selected = self.breed_filter.currentText()

        for p in get_all_pigeons():
            if (ring_filter in p.ring_number.lower() and
                (color_selected == "Todos" or p.color.lower() == color_selected.lower()) and
                (breed_selected == "Todas" or p.breed.lower() == breed_selected.lower())):
                self.pigeon_list.addItem(f"{p.ring_number} - {p.color} - {p.breed}")

    def load_pigeon(self, item):
        text = item.text().split(" - ")
        self.ring_input.setText(text[0])
        self.color_input.setCurrentText(text[1])
        self.breed_input.setCurrentText(text[2])
        self.selected_id = next(p.id for p in get_all_pigeons() if p.ring_number == text[0])
        self.notes_input.setText(next(p.notes for p in get_all_pigeons() if p.id == self.selected_id))

    def add_or_update(self):
        ring = self.ring_input.text().strip()
        color = self.color_input.currentText()
        breed = self.breed_input.currentText()
        notes = self.notes_input.toPlainText().strip()

        if not ring or not color or not breed:
            QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos obligatorios.")
            return

        data = {
            "ring_number": ring,
            "color": color,
            "breed": breed,
            "notes": notes
        }

        if self.selected_id:
            update_pigeon(self.selected_id, data)
        else:
            add_pigeon(data)

        self.clear_form()
        self.refresh_list()

    def delete_selected(self):
        if self.selected_id:
            delete_pigeon(self.selected_id)
            self.clear_form()
            self.refresh_list()

    def export_pdf(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Sin selección", "Selecciona una paloma primero.")
            return
        pigeon = next(p for p in get_all_pigeons() if p.id == self.selected_id)
        captures = get_captures_by_pigeon(pigeon.id)
        path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", f"{pigeon.ring_number}.pdf", "PDF Files (*.pdf)")
        if path:
            export_pigeon_pdf(pigeon, captures, path)
            QMessageBox.information(self, "Éxito", "Ficha exportada correctamente.")

    def clear_form(self):
        self.selected_id = None
        self.ring_input.clear()
        self.color_input.setCurrentIndex(0)
        self.breed_input.setCurrentIndex(0)
        self.notes_input.clear()

if __name__ == "__main__":
    setup_database()
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()