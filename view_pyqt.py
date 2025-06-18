# view_pyqt.py
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QGroupBox, QComboBox, QFrame, QApplication)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import ui_config

SUCCESS_COLOR = ui_config.SUCCESS_COLOR
DANGER_COLOR = ui_config.DANGER_COLOR
OFF_COLOR = ui_config.OFF_COLOR
WARNING_COLOR = ui_config.WARNING_COLOR
WATER_COLOR = ui_config.WATER_COLOR


class View(QWidget):

    # Inisialisasi Tampilan
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        if not hasattr(self.controller, 'adjust_ph'):
            self.controller.adjust_ph = lambda amount: print(f"Adjust pH by {amount}")
        if not hasattr(self.controller, 'adjust_water_level'):
            self.controller.adjust_water_level = lambda amount: print(f"Adjust water by {amount}")
            
        self._create_widgets()
        self._init_profile_dropdown()

    # Pembuatan Widget Utama
    def _create_widgets(self):
        main_layout = QHBoxLayout(self)
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_panel_layout = QVBoxLayout()
        
        main_layout.addLayout(left_panel_layout, 2)
        main_layout.addLayout(right_panel_layout, 5)

        left_panel_layout.addWidget(self._create_control_group())
        left_panel_layout.addWidget(self._create_dashboard_group())
        left_panel_layout.addWidget(self._create_manual_control_group())
        
        right_panel_layout.addWidget(self._create_visualization_group())

    # Grup Panel Kontrol
    def _create_control_group(self):
        control_group = QGroupBox("Panel Kontrol")
        layout = QVBoxLayout()

        self.automation_button = QPushButton("Otomatisasi: OFF")
        self.automation_button.clicked.connect(self.controller.toggle_automation)
        
        profile_selection_layout = QHBoxLayout()
        profile_selection_layout.addWidget(QLabel("Pilih Profil:"))
        self.profile_dropdown = QComboBox()
        self.profile_dropdown.currentTextChanged.connect(self.controller.change_plant_profile)
        profile_selection_layout.addWidget(self.profile_dropdown)

        profile_crud_layout = QHBoxLayout()
        add_btn = QPushButton("Tambah")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Hapus")
        add_btn.clicked.connect(self.controller.add_profile)
        edit_btn.clicked.connect(self.controller.edit_profile)
        delete_btn.clicked.connect(self.controller.delete_profile)
        profile_crud_layout.addWidget(add_btn)
        profile_crud_layout.addWidget(edit_btn)
        profile_crud_layout.addWidget(delete_btn)

        layout.addWidget(self.automation_button)
        layout.addLayout(profile_selection_layout)
        layout.addLayout(profile_crud_layout) # Tambahkan layout tombol CRUD
        control_group.setLayout(layout)
        return control_group

    # Grup Dashboard Sensor
    def _create_dashboard_group(self):
        dashboard_group = QGroupBox("Dashboard Sensor")
        layout = QGridLayout()

        self.profile_label = self._add_dashboard_row(layout, 0, "Profil Aktif:")
        self.ph_target_label = self._add_dashboard_row(layout, 1, "Target pH:")
        self.temp_target_label = self._add_dashboard_row(layout, 2, "Target Suhu:")
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator, 3, 0, 1, 2)

        self.ph_label = self._add_dashboard_row(layout, 4, "pH Air Aktual:")
        self.temp_label = self._add_dashboard_row(layout, 5, "Suhu Aktual:")
        self.humidity_label = self._add_dashboard_row(layout, 6, "Kelembapan:")
        self.light_label = self._add_dashboard_row(layout, 7, "Cahaya:")
        self.water_level_label = self._add_dashboard_row(layout, 8, "Level Air:")

        self.notification_label = QLabel("Memuat...")
        self.notification_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notification_label.setWordWrap(True)
        layout.addWidget(self.notification_label, 9, 0, 1, 2)
        
        dashboard_group.setLayout(layout)
        return dashboard_group

    # Fungsi Bantuan: Menambah Baris Dashboard
    def _add_dashboard_row(self, layout, row, label_text):
        layout.addWidget(QLabel(label_text), row, 0)
        value_label = QLabel("N/A")
        value_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(value_label, row, 1)
        return value_label

    # Grup Kontrol Manual
    def _create_manual_control_group(self):
        manual_group = QGroupBox("Kontrol Manual")
        layout = QVBoxLayout()
        
        ph_layout = QHBoxLayout()
        ph_layout.addWidget(QLabel("Kontrol pH:"))
        ph_down_btn = QPushButton("pH Down (-)")
        ph_up_btn = QPushButton("pH Up (+)")
        ph_down_btn.clicked.connect(lambda: self.controller.adjust_ph(-0.1))
        ph_up_btn.clicked.connect(lambda: self.controller.adjust_ph(0.1))
        ph_layout.addWidget(ph_down_btn)
        ph_layout.addWidget(ph_up_btn)
        
        water_layout = QHBoxLayout()
        water_layout.addWidget(QLabel("Kontrol Air:"))
        water_down_btn = QPushButton("Kurangi Air (-)")
        water_up_btn = QPushButton("Isi Air (+)")
        water_down_btn.clicked.connect(lambda: self.controller.adjust_water_level(-10))
        water_up_btn.clicked.connect(lambda: self.controller.adjust_water_level(10))
        water_layout.addWidget(water_down_btn)
        water_layout.addWidget(water_up_btn)

        self.light_button = QPushButton("Lampu: OFF")
        self.light_button.clicked.connect(self.controller.toggle_light)
        
        self.fan_button = QPushButton("Kipas: OFF")
        self.fan_button.clicked.connect(self.controller.toggle_fan)

        layout.addLayout(ph_layout)
        layout.addLayout(water_layout)
        layout.addWidget(self.light_button)
        layout.addWidget(self.fan_button)
        
        manual_group.setLayout(layout)
        return manual_group
    
    # Grup Visualisasi Data
    def _create_visualization_group(self):
        vis_group = QGroupBox("Visualisasi Data")
        layout = QHBoxLayout()

        self.fig_vis = Figure(figsize=(9, 5)) 
        self.canvas_vis = FigureCanvas(self.fig_vis)

        self.ax_ph = self.fig_vis.add_subplot(1, 3, 1)
        self.ax_temp = self.fig_vis.add_subplot(1, 3, 2)
        self.ax_water = self.fig_vis.add_subplot(1, 3, 3)

        layout.addWidget(self.canvas_vis)
        
        vis_group.setLayout(layout)
        return vis_group

    # Inisialisasi Dropdown Profil
    def _init_profile_dropdown(self):
        profile_names = self.controller.get_profile_names()
        if self.profile_dropdown.count() == 0:
            self.profile_dropdown.addItems(profile_names)
    
    def refresh_profile_dropdown(self):
        current_selection = self.profile_dropdown.currentText()
        self.profile_dropdown.blockSignals(True) # Hentikan sinyal sementara
        
        self.profile_dropdown.clear()
        profile_names = self.controller.get_profile_names()
        self.profile_dropdown.addItems(profile_names)
        
        # Coba set kembali ke pilihan sebelumnya jika masih ada
        if current_selection in profile_names:
            self.profile_dropdown.setCurrentText(current_selection)
        
        self.profile_dropdown.blockSignals(False)

    # Pembaruan Tampilan Terpusat
    def update_dashboard(self, model):
        self.update_labels(model)
        self.update_buttons(model)
        self.update_notification(model)
        self.update_ph_bar(model)
        self.update_temp_bar(model)
        self.update_water_bar(model)
        
        self.fig_vis.tight_layout(pad=3.0)
        self.canvas_vis.draw()

    # Pembaruan Grafik Batang pH
    def update_ph_bar(self, model):
        self.ax_ph.clear()
        ph = model.ph; ph_range_min, ph_range_max = 5.0, 8.0
        self.ax_ph.set_ylim(ph_range_min, ph_range_max)
        if model.active_profile_data:
            ph_min_target = model.active_profile_data['ph_min']; ph_max_target = model.active_profile_data['ph_max']
            self.ax_ph.axhspan(ph_min_target, ph_max_target, color=SUCCESS_COLOR, alpha=0.2)
            bar_color = SUCCESS_COLOR if ph_min_target <= ph <= ph_max_target else DANGER_COLOR
        else: bar_color = OFF_COLOR
        bar_height = ph - ph_range_min; bar_bottom = ph_range_min
        self.ax_ph.bar(0, height=bar_height, bottom=bar_bottom, color=bar_color, width=0.5)
        self.ax_ph.set_xticks([]); self.ax_ph.set_title("pH Saat Ini")
        text_y_position = bar_bottom + (bar_height / 2)
        self.ax_ph.text(0, text_y_position, f'{ph:.2f}', ha='center', va='center', color='white', weight='bold', fontsize=12)

    # Pembaruan Grafik Batang Suhu
    def update_temp_bar(self, model):
        self.ax_temp.clear()
        temp = model.temperature; temp_range_min, temp_range_max = 18.0, 35.0
        self.ax_temp.set_ylim(temp_range_min, temp_range_max)
        if model.active_profile_data:
            temp_min_target = model.active_profile_data['temp_min']; temp_max_target = model.active_profile_data['temp_max']
            self.ax_temp.axhspan(temp_min_target, temp_max_target, color=SUCCESS_COLOR, alpha=0.2)
            bar_color = SUCCESS_COLOR if temp_min_target <= temp <= temp_max_target else DANGER_COLOR
        else: bar_color = OFF_COLOR
        bar_height = temp - temp_range_min; bar_bottom = temp_range_min
        self.ax_temp.bar(0, height=bar_height, bottom=bar_bottom, color=bar_color, width=0.5)
        self.ax_temp.set_xticks([]); self.ax_temp.set_title("Suhu Saat Ini (°C)")
        text_y_position = bar_bottom + (bar_height / 2)
        self.ax_temp.text(0, text_y_position, f'{temp:.1f}°C', ha='center', va='center', color='white', weight='bold', fontsize=12)
    
    # Pembaruan Grafik Batang Air
    def update_water_bar(self, model):
        self.ax_water.clear()
        level = model.water_level
        if level > 50: bar_color = WATER_COLOR
        elif level > 20: bar_color = WARNING_COLOR
        else: bar_color = DANGER_COLOR
        self.ax_water.bar(0, level, color=bar_color, width=0.5)
        self.ax_water.set_ylim(0, 100); self.ax_water.set_xticks([])
        self.ax_water.set_title("Level Air")
        text_y_position = level / 2
        self.ax_water.text(0, text_y_position, f'{level:.0f}%', ha='center', va='center', color='white', weight='bold', fontsize=14)

    # Pembaruan Label Dashboard
    def update_labels(self, model):
        self.ph_label.setText(f"{model.ph:.2f}")
        self.temp_label.setText(f"{model.temperature:.1f} °C")
        self.humidity_label.setText(f"{model.humidity:.1f} %")
        self.light_label.setText(f"{model.light} Lux")
        self.water_level_label.setText(f"{model.water_level:.1f} %")
        if model.active_profile_data:
            profile = model.active_profile_data
            self.profile_label.setText(model.active_profile_name)
            self.ph_target_label.setText(f"{profile['ph_min']} - {profile['ph_max']}")
            self.temp_target_label.setText(f"{profile['temp_min']}°C - {profile['temp_max']}°C")
        else:
            self.profile_label.setText("Tidak Ada"); self.ph_target_label.setText("N/A"); self.temp_target_label.setText("N/A")

    # Pembaruan Tampilan Tombol
    def update_buttons(self, model):
        self._update_button_status(self.automation_button, "Otomatisasi", model.automation_enabled)
        self._update_button_status(self.light_button, "Lampu", model.light_on)
        self._update_button_status(self.fan_button, "Kipas", model.fan_on)

    # Fungsi Bantuan: Mengubah Status Tombol
    def _update_button_status(self, button, name, status):
        text = f"{name}: {'ON' if status else 'OFF'}"
        button.setText(text)
        button.setProperty("status", "on" if status else "off")
        button.style().unpolish(button)
        button.style().polish(button)
        
    # Pembaruan Pesan Notifikasi
    def update_notification(self, model):
        self.notification_label.setText(model.notification_message)
        if "HINT" in model.notification_message.upper():
            self.notification_label.setProperty("status", "warning")
        elif "PERINGATAN" in model.notification_message.upper():
            self.notification_label.setProperty("status", "warning2")
        else:
            self.notification_label.setProperty("status", "success")
        self.notification_label.style().unpolish(self.notification_label)
        self.notification_label.style().polish(self.notification_label)
    