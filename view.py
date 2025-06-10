# view.py - VERSI DENGAN LAYOUT GRAFIK & BAR AIR TERPISAH

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
        self.parent.geometry("1100x650")
        
        self.selected_profile = tk.StringVar(self)
        
        self._create_widgets()
        self._init_profile_dropdown()

    def _create_widgets(self):
        # Struktur utama 2 kolom (kiri untuk kontrol, kanan untuk visualisasi) tetap sama
        main_frame = tk.Frame(self, bg=config.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel Kiri: Kontrol & Dashboard (TIDAK BERUBAH)
        left_frame = tk.Frame(main_frame, bg=config.BG_COLOR)
        left_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        
        # Panel Kanan: Sekarang akan berisi semua visualisasi (grafik & bar)
        right_frame = tk.Frame(main_frame, bg=config.FRAME_COLOR, bd=2, relief=tk.SOLID)
        right_frame.grid(row=0, column=1, sticky="nsew")

        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Menempatkan widget-widget ke dalam frame yang sesuai
        self._create_control_widgets(left_frame)
        self._create_dashboard_widgets(left_frame)
        # Fungsi ini sekarang akan mengatur layout internal di panel kanan
        self._create_visualization_widgets(right_frame)

    def _create_dashboard_widgets(self, parent):
        # ... (Tidak ada perubahan di sini, hanya memastikan warna background konsisten) ...
        dashboard_frame = tk.LabelFrame(parent, text="📊 Dashboard Sensor", font=config.FONT_BOLD, 
                                        bg=config.BG_COLOR, fg=config.TEXT_COLOR, relief="flat", borderwidth=0)
        dashboard_frame.pack(fill=tk.X, pady=(0, 10), anchor='n')
        
        # ... (Sisa kode widget dashboard sama persis)
        tk.Label(dashboard_frame, text="Profil Aktif:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=0, column=0, sticky="w", pady=2)
        self.profile_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.profile_label.grid(row=0, column=1, sticky="w", pady=2)
        tk.Label(dashboard_frame, text="Target pH:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=1, column=0, sticky="w", pady=2)
        self.ph_target_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.ph_target_label.grid(row=1, column=1, sticky="w", pady=2)
        tk.Label(dashboard_frame, text="Target Suhu:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=2, column=0, sticky="w", pady=2)
        self.temp_target_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.temp_target_label.grid(row=2, column=1, sticky="w", pady=2)
        ttk.Separator(dashboard_frame, orient='horizontal').grid(row=3, columnspan=2, sticky='ew', pady=10)
        tk.Label(dashboard_frame, text="📊 pH Air Aktual:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=4, column=0, sticky="w", pady=2)
        self.ph_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.ph_label.grid(row=4, column=1, sticky="w", pady=2)
        tk.Label(dashboard_frame, text="🌡 Suhu Aktual:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=5, column=0, sticky="w", pady=2)
        self.temp_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.temp_label.grid(row=5, column=1, sticky="w", pady=2)
        tk.Label(dashboard_frame, text="💧 Kelembapan:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=6, column=0, sticky="w", pady=2)
        self.humidity_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.humidity_label.grid(row=6, column=1, sticky="w", pady=2)
        tk.Label(dashboard_frame, text="💡 Cahaya:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=7, column=0, sticky="w", pady=2)
        self.light_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.light_label.grid(row=7, column=1, sticky="w", pady=2)
        tk.Label(dashboard_frame, text="🌊 Level Air:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).grid(row=8, column=0, sticky="w", pady=2)
        self.water_level_label = tk.Label(dashboard_frame, text="N/A", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR)
        self.water_level_label.grid(row=8, column=1, sticky="w", pady=2)
        self.notification_label = tk.Label(dashboard_frame, text="Memuat...", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.TEXT_COLOR, wraplength=300, justify="center")
        self.notification_label.grid(row=9, columnspan=2, sticky='ew', pady=(15, 5))


    def _create_control_widgets(self, parent):
        # ... (Tidak ada perubahan di sini, hanya memastikan warna background konsisten) ...
        control_frame = tk.LabelFrame(parent, text="⚙️ Panel Kontrol", font=config.FONT_BOLD, 
                                      bg=config.BG_COLOR, fg=config.TEXT_COLOR, relief="flat", borderwidth=0)
        control_frame.pack(fill=tk.X, pady=10, anchor='n')

        self.automation_button = tk.Button(control_frame, text="Otomatisasi: OFF", command=self.controller.toggle_automation, bg=config.OFF_COLOR, font=config.FONT_BOLD, fg=config.BUTTON_TEXT_COLOR, relief='flat')
        self.automation_button.pack(fill=tk.X, pady=5, ipady=4)
        profile_frame = tk.Frame(control_frame, bg=config.BG_COLOR)
        profile_frame.pack(fill=tk.X, pady=5)
        tk.Label(profile_frame, text="Pilih Profil:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).pack(side=tk.LEFT, padx=(0,10))
        self.profile_dropdown = ttk.OptionMenu(profile_frame, self.selected_profile, "Memuat...")
        self.profile_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        manual_control_frame = tk.LabelFrame(parent, text="🕹️ Kontrol Manual", font=config.FONT_BOLD, bg=config.BG_COLOR, fg=config.TEXT_COLOR, relief="flat", borderwidth=0)
        manual_control_frame.pack(fill=tk.X, padx=10, pady=10, anchor='n')
        air_control_frame = tk.Frame(manual_control_frame, bg=config.BG_COLOR)
        air_control_frame.pack(fill=tk.X, pady=5)
        tk.Label(air_control_frame, text="Kontrol Level Air:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(air_control_frame, text="Isi Air (+)", command=lambda: self.controller.adjust_water_level(10), bg=config.BUTTON_COLOR, fg=config.BUTTON_TEXT_COLOR, relief='flat').pack(side=tk.LEFT, padx=2)
        tk.Button(air_control_frame, text="Kurangi Air (-)", command=lambda: self.controller.adjust_water_level(-10), bg=config.BUTTON_COLOR, fg=config.BUTTON_TEXT_COLOR, relief='flat').pack(side=tk.LEFT, padx=2)
        ph_control_frame = tk.Frame(manual_control_frame, bg=config.BG_COLOR)
        ph_control_frame.pack(fill=tk.X, pady=5)
        tk.Label(ph_control_frame, text="Kontrol pH:", font=config.FONT_NORMAL, bg=config.BG_COLOR, fg=config.LABEL_COLOR).pack(side=tk.LEFT, padx=(0,10))
        tk.Button(ph_control_frame, text="pH Down (-)", command=lambda: self.controller.adjust_ph(-0.1), bg=config.BUTTON_COLOR, fg=config.BUTTON_TEXT_COLOR, relief='flat').pack(side=tk.LEFT, padx=2)
        tk.Button(ph_control_frame, text="pH Up (+)", command=lambda: self.controller.adjust_ph(0.1), bg=config.BUTTON_COLOR, fg=config.BUTTON_TEXT_COLOR, relief='flat').pack(side=tk.LEFT, padx=2)
        self.light_button = tk.Button(manual_control_frame, text="Lampu: OFF", command=self.controller.toggle_light, bg=config.OFF_COLOR, fg=config.BUTTON_TEXT_COLOR, relief='flat')
        self.light_button.pack(fill=tk.X, pady=5, ipady=4)
        self.fan_button = tk.Button(manual_control_frame, text="Kipas: OFF", command=self.controller.toggle_fan, bg=config.OFF_COLOR, fg=config.BUTTON_TEXT_COLOR, relief='flat')
        self.fan_button.pack(fill=tk.X, pady=5, ipady=4)

    def _init_profile_dropdown(self):
        # ... (Tidak ada perubahan di sini)
        profile_names = self.controller.get_profile_names()
        self.selected_profile.set("Tidak Ada")
        menu = self.profile_dropdown["menu"]
        menu.delete(0, "end")
        for name in profile_names:
            menu.add_command(label=name, command=lambda value=name: self.selected_profile.set(value))
        self.selected_profile.trace("w", lambda *args: self.controller.change_plant_profile(self.selected_profile.get()))

    def update_dashboard(self, model):
        # Memanggil fungsi-fungsi update individual
        self.update_labels(model)
        self.update_buttons(model)
        self.update_notification(model)
        self.update_line_graphs(model)
        self.update_water_bar(model)

    def update_labels(self, model):
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

    def update_buttons(self, model):
        self._update_button_status(self.automation_button, "Otomatisasi", model.automation_enabled, font=config.FONT_BOLD)
        self._update_button_status(self.light_button, "Lampu", model.light_on)
        self._update_button_status(self.fan_button, "Kipas", model.fan_on)

    def update_notification(self, model):
        self.notification_label.config(text=model.notification_message)
        if "PERINGATAN" not in model.notification_message.upper():
            self.notification_label.config(fg=config.TEXT_COLOR)
        else:
            self.notification_label.config(fg=config.WARNING_COLOR)

    def _update_button_status(self, button, name, status, font=config.FONT_NORMAL):
        text = f"{name}: {'ON' if status else 'OFF'}"
        color = config.SUCCESS_COLOR if status else config.OFF_COLOR
        button.config(text=text, bg=color, font=font)
    
    # ## FUNGSI INI DIUBAH MENJADI _create_visualization_widgets ##
    def _create_visualization_widgets(self, parent):
        # parent sekarang adalah right_frame
        parent.config(bg=config.BG_COLOR) # Samakan warna background parent
        parent.grid_rowconfigure(0, weight=1)
        # Buat 2 kolom di dalam panel kanan
        parent.grid_columnconfigure(0, weight=3) # Kolom untuk grafik garis
        parent.grid_columnconfigure(1, weight=1) # Kolom untuk bar air

        # Frame untuk grafik garis
        line_graph_frame = tk.Frame(parent, bg=config.FRAME_COLOR)
        line_graph_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Frame untuk bar air
        bar_graph_frame = tk.Frame(parent, bg=config.FRAME_COLOR)
        bar_graph_frame.grid(row=0, column=1, sticky="nsew")

        # Membuat canvas untuk masing-masing frame
        self._create_line_graph_canvas(line_graph_frame)
        self._create_water_bar_canvas(bar_graph_frame)

    def _create_line_graph_canvas(self, parent):
        # Hanya membuat 2 grafik riwayat
        self.fig_graphs = Figure(figsize=(6, 6), dpi=100)
        self.fig_graphs.patch.set_facecolor(config.FRAME_COLOR)
        
        self.ax_ph = self.fig_graphs.add_subplot(211)
        self.ax_ph.set_facecolor(config.BG_COLOR)
        self.ax_ph.set_title("Riwayat pH", color=config.TEXT_COLOR)
        self.ax_ph.tick_params(colors=config.TEXT_COLOR)
        
        self.ax_temp = self.fig_graphs.add_subplot(212)
        self.ax_temp.set_facecolor(config.BG_COLOR)
        self.ax_temp.set_title("Riwayat Suhu (°C)", color=config.TEXT_COLOR)
        self.ax_temp.tick_params(colors=config.TEXT_COLOR)

        self.fig_graphs.tight_layout(pad=3.0)
        
        self.canvas_graphs = FigureCanvasTkAgg(self.fig_graphs, master=parent)
        self.canvas_graphs.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _create_water_bar_canvas(self, parent):
        # Membuat figure dan canvas terpisah untuk bar air
        self.fig_water = Figure(figsize=(2, 6), dpi=100)
        self.fig_water.patch.set_facecolor(config.FRAME_COLOR)
        
        self.ax_water = self.fig_water.add_subplot(111)
        self.ax_water.set_facecolor(config.FRAME_COLOR)

        self.fig_water.tight_layout(pad=2.0)

        self.canvas_water = FigureCanvasTkAgg(self.fig_water, master=parent)
        self.canvas_water.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # ## FUNGSI UPDATE DIPISAH ##
    def update_line_graphs(self, model):
        self.ax_ph.clear()
        self.ax_ph.plot(model.ph_history, color=config.LABEL_COLOR, label='Aktual')
        self.ax_ph.set_title("Riwayat pH", color=config.TEXT_COLOR)
        self.ax_ph.set_ylim(5, 8)
        if model.active_profile_data:
            self.ax_ph.axhspan(model.active_profile_data['ph_min'], model.active_profile_data['ph_max'], color=config.SUCCESS_COLOR, alpha=0.3, label='Target')
        self.ax_ph.legend(loc='upper right')

        self.ax_temp.clear()
        self.ax_temp.plot(model.temp_history, color="#EBCB8B", label='Aktual')
        self.ax_temp.set_title("Riwayat Suhu (°C)", color=config.TEXT_COLOR)
        self.ax_temp.set_ylim(18, 35)
        if model.active_profile_data:
            self.ax_temp.axhspan(model.active_profile_data['temp_min'], model.active_profile_data['temp_max'], color=config.SUCCESS_COLOR, alpha=0.3, label='Target')
        self.ax_temp.legend(loc='upper right')

        self.canvas_graphs.draw()

    def update_water_bar(self, model):
        # Fungsi baru untuk mengupdate bar air dengan "batasan"
        self.ax_water.clear()
        self.ax_water.set_title("Level Air", color=config.TEXT_COLOR)
        self.ax_water.set_xlim(-1, 1) 
        self.ax_water.set_ylim(0, 100)
        self.ax_water.axis('off')

        level = model.water_level
        if level > 50:
            bar_color = config.SUCCESS_COLOR  # Hijau (Aman)
        elif level > 20:
            bar_color = config.WARNING_COLOR # Kuning (Peringatan)
        else:
            bar_color = config.DANGEOR_COLOR   # Merah (Bahaya)

        # Menggambar "wadah" atau "batasan" terlebih dahulu
        self.ax_water.bar(0, 100, width=0.8, color=config.BG_COLOR, edgecolor=config.TEXT_COLOR, linewidth=1.5)
        
        # Menggambar bar isian di atasnya
        self.ax_water.bar(0, level, width=0.8, color=bar_color)

        # Menambahkan label persentase
        self.ax_water.text(0, 50, f"{level:.0f}%", ha='center', va='center', color=config.BUTTON_TEXT_COLOR, fontsize=14, fontweight='bold')
        
        self.canvas_water.draw()