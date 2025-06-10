# view.py - VERSI FINAL DENGAN PERBAIKAN GRAFIK & DASHBOARD

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ui_config as config

class View(tk.Frame):
    """Kelas untuk tampilan antarmuka (GUI)."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=config.BG_COLOR)
        self.parent = parent
        self.controller = controller
        
        self.parent.title("Dashboard Hidroponik Cerdas")
        self.parent.geometry("950x700")
        
        self.selected_profile = tk.StringVar(self)
        
        self._create_widgets()
        self._init_profile_dropdown()

    def _create_widgets(self):
        main_frame = tk.Frame(self, bg=config.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame, bg=config.FRAME_COLOR, bd=2, relief=tk.SOLID)
        left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        
        right_frame = tk.Frame(main_frame, bg=config.FRAME_COLOR, bd=2, relief=tk.SOLID)
        right_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self._create_control_widgets(left_frame)
        self._create_dashboard_widgets(left_frame)
        self._create_graph_widgets(right_frame)

    def _create_dashboard_widgets(self, parent):
        dashboard_frame = tk.LabelFrame(parent, text="📊 Dashboard Sensor", font=config.FONT_BOLD, 
                                        bg=config.FRAME_COLOR, fg=config.TEXT_COLOR, padx=10, pady=10)
        dashboard_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # --- Bagian Target ---
        tk.Label(dashboard_frame, text="Profil Aktif:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=0, column=0, sticky="w", pady=2)
        self.profile_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.profile_label.grid(row=0, column=1, sticky="w", pady=2)
        
        tk.Label(dashboard_frame, text="Target pH:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=1, column=0, sticky="w", pady=2)
        self.ph_target_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.ph_target_label.grid(row=1, column=1, sticky="w", pady=2)

        tk.Label(dashboard_frame, text="Target Suhu:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=2, column=0, sticky="w", pady=2)
        self.temp_target_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.temp_target_label.grid(row=2, column=1, sticky="w", pady=2)
        
        ttk.Separator(dashboard_frame, orient='horizontal').grid(row=3, columnspan=2, sticky='ew', pady=10)
        
        # --- Bagian Data Aktual ---
        tk.Label(dashboard_frame, text="pH Air Aktual:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=4, column=0, sticky="w", pady=2)
        self.ph_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.ph_label.grid(row=4, column=1, sticky="w", pady=2)

        tk.Label(dashboard_frame, text="🌡️ Suhu Aktual:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=5, column=0, sticky="w", pady=2)
        self.temp_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.temp_label.grid(row=5, column=1, sticky="w", pady=2)

        tk.Label(dashboard_frame, text="💧 Kelembapan:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=6, column=0, sticky="w", pady=2)
        self.humidity_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.humidity_label.grid(row=6, column=1, sticky="w", pady=2)

        tk.Label(dashboard_frame, text="💡 Cahaya:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=7, column=0, sticky="w", pady=2)
        self.light_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.light_label.grid(row=7, column=1, sticky="w", pady=2)

        tk.Label(dashboard_frame, text="🌊 Level Air:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).grid(row=8, column=0, sticky="w", pady=2)
        self.water_level_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.FRAME_COLOR, fg=config.TEXT_COLOR)
        self.water_level_label.grid(row=8, column=1, sticky="w", pady=2)

        # Pindahkan "Notifikasi" ke baris 9
        self.notification_label = tk.Label(dashboard_frame, text="Memuat...", font=config.FONT_NORMAL, 
                                           bg=config.FRAME_COLOR, fg=config.TEXT_COLOR, wraplength=280, justify="center")
        self.notification_label.grid(row=9, columnspan=2, sticky='ew', pady=(15, 5))

    def _create_control_widgets(self, parent):
        # ... (Tidak ada perubahan di fungsi ini) ...
        control_frame = tk.LabelFrame(parent, text="⚙️ Panel Kontrol Utama", font=config.FONT_BOLD, 
                                      bg=config.FRAME_COLOR, fg=config.TEXT_COLOR, padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.automation_button = tk.Button(control_frame, text="Otomatisasi: OFF", command=self.controller.toggle_automation, bg=config.DANGER_COLOR, font=config.FONT_BOLD)
        self.automation_button.pack(fill=tk.X, pady=5)
        
        profile_frame = tk.Frame(control_frame, bg=config.FRAME_COLOR)
        profile_frame.pack(fill=tk.X, pady=5)
        tk.Label(profile_frame, text="Pilih Profil:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).pack(side=tk.LEFT, padx=(0,10))
        self.profile_dropdown = ttk.OptionMenu(profile_frame, self.selected_profile, "Memuat...")
        self.profile_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)

        manual_control_frame = tk.LabelFrame(parent, text="🕹️ Kontrol Manual", font=config.FONT_BOLD, 
                                             bg=config.FRAME_COLOR, fg=config.TEXT_COLOR, padx=10, pady=10)
        manual_control_frame.pack(fill=tk.X, padx=10, pady=10)

        ph_control_frame = tk.Frame(manual_control_frame, bg=config.FRAME_COLOR)
        ph_control_frame.pack(fill=tk.X, pady=5)
        tk.Label(ph_control_frame, text="Kontrol pH:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(ph_control_frame, text="pH Down (-)", command=lambda: self.controller.adjust_ph(-0.1), bg=config.BUTTON_COLOR).pack(side=tk.LEFT, padx=2)
        tk.Button(ph_control_frame, text="pH Up (+)", command=lambda: self.controller.adjust_ph(0.1), bg=config.BUTTON_COLOR).pack(side=tk.LEFT, padx=2)

        air_control_frame = tk.Frame(manual_control_frame, bg=config.FRAME_COLOR)
        air_control_frame.pack(fill=tk.X, pady=5)
        tk.Label(air_control_frame, text="Kontrol Level Air:", font=config.FONT_NORMAL, bg=config.FRAME_COLOR, fg=config.LABEL_COLOR).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(air_control_frame, text="Isi Air (+)", command=lambda: self.controller.adjust_water_level(10), bg=config.BUTTON_COLOR).pack(side=tk.LEFT, padx=2)
        tk.Button(air_control_frame, text="Kurangi Air (-)", command=lambda: self.controller.adjust_water_level(-10), bg=config.BUTTON_COLOR).pack(side=tk.LEFT, padx=2)

        self.light_button = tk.Button(manual_control_frame, text="Lampu: OFF", command=self.controller.toggle_light, bg=config.DANGER_COLOR, width=25)
        self.light_button.pack(fill=tk.X, pady=5)

        self.fan_button = tk.Button(manual_control_frame, text="Kipas: OFF", command=self.controller.toggle_fan, bg=config.DANGER_COLOR, width=25)
        self.fan_button.pack(fill=tk.X, pady=5)

    def _init_profile_dropdown(self):
        # ... (Tidak ada perubahan di fungsi ini) ...
        profile_names = self.controller.get_profile_names()
        self.selected_profile.set("Tidak Ada")
        
        menu = self.profile_dropdown["menu"]
        menu.delete(0, "end")
        
        for name in profile_names:
            menu.add_command(label=name, command=lambda value=name: self.selected_profile.set(value))
        
        self.selected_profile.trace("w", lambda *args: self.controller.change_plant_profile(self.selected_profile.get()))

    def update_dashboard(self, model):
        self.ph_label.config(text=f"{model.ph:.2f}")
        self.temp_label.config(text=f"{model.temperature:.1f} °C")
        self.humidity_label.config(text=f"{model.humidity:.1f} %")
        self.light_label.config(text=f"{model.light} Lux")
        self.water_level_label.config(text=f"{model.water_level:.1f} %")

        if model.active_profile_data:
            profile = model.active_profile_data
            self.profile_label.config(text=model.active_profile_name)
            self.ph_target_label.config(text=f"{profile['ph_min']} - {profile['ph_max']}")
            self.temp_target_label.config(text=f"{profile['temp_min']}°C - {profile['temp_max']}°C")
        else:
            self.profile_label.config(text="Tidak Ada")
            self.ph_target_label.config(text="N/A")
            self.temp_target_label.config(text="N/A")

        self._update_button_status(self.automation_button, "Otomatisasi", model.automation_enabled, font=config.FONT_BOLD)
        self._update_button_status(self.light_button, "Lampu", model.light_on)
        self._update_button_status(self.fan_button, "Kipas", model.fan_on)

        self.notification_label.config(text=model.notification_message)
        if "PERINGATAN" not in model.notification_message.upper():
            self.notification_label.config(fg=config.TEXT_COLOR)
        else:
            self.notification_label.config(fg=config.WARNING_COLOR)

    def _update_button_status(self, button, name, status, font=config.FONT_NORMAL):
        text = f"{name}: {'ON' if status else 'OFF'}"
        color = config.SUCCESS_COLOR if status else config.DANGER_COLOR
        button.config(text=text, bg=color, font=font)
    
    def _create_graph_widgets(self, parent):
        self.fig = Figure(figsize=(6, 6), dpi=100) # Membuat figure sedikit lebih tinggi
        self.fig.patch.set_facecolor(config.FRAME_COLOR)
        
        # ## PERBAIKAN 3: Mengubah Layout Subplot ##
        # Menggunakan 3 baris, 1 kolom
        self.ax_ph = self.fig.add_subplot(311)
        self.ax_ph.set_facecolor(config.BG_COLOR)
        self.ax_ph.set_title("Riwayat pH", color=config.TEXT_COLOR)
        self.ax_ph.tick_params(axis='x', colors=config.TEXT_COLOR)
        self.ax_ph.tick_params(axis='y', colors=config.TEXT_COLOR)
        
        self.ax_temp = self.fig.add_subplot(312)
        self.ax_temp.set_facecolor(config.BG_COLOR)
        self.ax_temp.set_title("Riwayat Suhu (°C)", color=config.TEXT_COLOR)
        self.ax_temp.tick_params(axis='x', colors=config.TEXT_COLOR)
        self.ax_temp.tick_params(axis='y', colors=config.TEXT_COLOR)

        # Plot baru untuk Level Air di posisi ke-3
        self.ax_water = self.fig.add_subplot(313)
        self.ax_water.set_facecolor(config.BG_COLOR)
        self.ax_water.set_title("Level Air (%)", color=config.TEXT_COLOR)
        self.ax_water.tick_params(axis='x', colors=config.TEXT_COLOR)
        self.ax_water.tick_params(axis='y', colors=config.TEXT_COLOR)

        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def update_graphs(self, model):
        # ## PERBAIKAN 4: Memperbaiki Logika Update Grafik ##

        # Grafik pH
        self.ax_ph.clear()
        self.ax_ph.plot(model.ph_history, color=config.LABEL_COLOR, label='Aktual')
        self.ax_ph.set_title("Riwayat pH", color=config.TEXT_COLOR)
        self.ax_ph.set_ylim(5, 8)
        if model.active_profile_data:
            self.ax_ph.axhspan(model.active_profile_data['ph_min'], model.active_profile_data['ph_max'], color=config.SUCCESS_COLOR, alpha=0.2, label='Target')
        self.ax_ph.legend(loc='upper right')

        # Grafik Suhu
        self.ax_temp.clear()
        self.ax_temp.plot(model.temp_history, color="#EBCB8B", label='Aktual') # Warna berbeda
        self.ax_temp.set_title("Riwayat Suhu (°C)", color=config.TEXT_COLOR)
        self.ax_temp.set_ylim(18, 35)
        if model.active_profile_data:
            self.ax_temp.axhspan(model.active_profile_data['temp_min'], model.active_profile_data['temp_max'], color=config.SUCCESS_COLOR, alpha=0.2, label='Target')
        self.ax_temp.legend(loc='upper right')

        # Grafik Level Air (sebelumnya Air)
        self.ax_water.clear()
        self.ax_water.plot(model.water_level_history, color=config.SUCCESS_COLOR, label='Aktual')
        self.ax_water.set_title("Riwayat Air (%)", color=config.TEXT_COLOR)
        self.ax_water.set_ylim(0, 105) # Batas 0-100%
        # Contoh target level air bisa ditambahkan di profil jika perlu
        # if model.active_profile_data and 'water_level_min' in model.active_profile_data:
        #     self.ax_water.axhspan(model.active_profile_data['water_level_min'], 100, color=config.SUCCESS_COLOR, alpha=0.2, label='Aman')
        self.ax_water.legend(loc='upper right')

        self.canvas.draw()