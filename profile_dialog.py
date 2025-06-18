# profile_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QDoubleSpinBox, QSpinBox, QDialogButtonBox)

class ProfileDialog(QDialog):
    def __init__(self, parent=None, profile_data=None):
        super().__init__(parent)
        
        self.is_edit_mode = profile_data is not None
        title = "Edit Profil" if self.is_edit_mode else "Tambah Profil Baru"
        self.setWindowTitle(title)
        self.setObjectName("ProfileDialog")
        # Buat input fields
        self.name_input = QLineEdit()
        self.ph_min_input = QDoubleSpinBox(decimals=1, singleStep=0.1)
        self.ph_max_input = QDoubleSpinBox(decimals=1, singleStep=0.1)
        self.temp_min_input = QDoubleSpinBox(decimals=1, singleStep=0.1)
        self.temp_max_input = QDoubleSpinBox(decimals=1, singleStep=0.1)
        self.light_on_input = QSpinBox(minimum=0, maximum=23)
        self.light_off_input = QSpinBox(minimum=0, maximum=23)

        # Atur rentang nilai
        for spinbox in [self.ph_min_input, self.ph_max_input]:
            spinbox.setRange(0.0, 14.0)
        for spinbox in [self.temp_min_input, self.temp_max_input]:
            spinbox.setRange(0.0, 50.0)

        # Jika mode edit, isi field dengan data yang ada
        if self.is_edit_mode:
            self.name_input.setText(profile_data.get("name", ""))
            self.name_input.setReadOnly(True) # Nama profil tidak bisa diubah
            self.ph_min_input.setValue(profile_data.get("ph_min", 6.0))
            self.ph_max_input.setValue(profile_data.get("ph_max", 6.5))
            self.temp_min_input.setValue(profile_data.get("temp_min", 20.0))
            self.temp_max_input.setValue(profile_data.get("temp_max", 25.0))
            self.light_on_input.setValue(profile_data.get("auto_light_on_hour", 6))
            self.light_off_input.setValue(profile_data.get("auto_light_off_hour", 22))

        # Buat tombol OK dan Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Tata letak form
        form_layout = QFormLayout()
        form_layout.addRow("Nama Profil:", self.name_input)
        form_layout.addRow("pH Minimum:", self.ph_min_input)
        form_layout.addRow("pH Maksimum:", self.ph_max_input)
        form_layout.addRow("Suhu Minimum (°C):", self.temp_min_input)
        form_layout.addRow("Suhu Maksimum (°C):", self.temp_max_input)
        form_layout.addRow("Lampu Nyala (Jam):", self.light_on_input)
        form_layout.addRow("Lampu Mati (Jam):", self.light_off_input)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        
    def get_profile_data(self):
        """Mengambil data dari form dan mengembalikannya sebagai dictionary."""
        name = self.name_input.text()
        return {
            "name": name,
            "ph_min": self.ph_min_input.value(),
            "ph_max": self.ph_max_input.value(),
            "temp_min": self.temp_min_input.value(),
            "temp_max": self.temp_max_input.value(),
            "auto_light_on_hour": self.light_on_input.value(),
            "auto_light_off_hour": self.light_off_input.value()
        }