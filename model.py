# model.py

class Model:
    """Menyimpan data dan state dari aplikasi hidroponik."""
    def __init__(self):
        # Data sensor saat ini
        self.ph = 0.0
        self.temperature = 0.0
        self.humidity = 0.0
        self.light = 0
        self.water_level = 0.0
        # Status kontrol
        self.water_pump_on = False
        self.light_on = False
        self.fan_on = False

        # Data historis untuk grafik (menyimpan 50 titik data terakhir)
        self.ph_history = []
        self.temp_history = []
        self.water_level_history = []
        self.max_history_points = 50

        self.automation_enabled = False # Master switch untuk semua otomatisasi
        
        # Profil Tanaman
        self.active_profile_name = "Tidak Ada"
        self.active_profile_data = None
        
        # Notifikasi
        self.notification_message = "Otomatisasi nonaktif."

    def update_sensor_data(self, data: dict):
        """Memperbarui data sensor dari sumber (lingkungan atau sensor asli)."""
        self.ph = data.get("ph", self.ph)
        self.temperature = data.get("temperature", self.temperature)
        self.humidity = data.get("humidity", self.humidity)
        self.light = data.get("light", self.light)
        self.water_level = data.get("water_level", self.water_level)
        # Tambahkan ke riwayat untuk grafik
        self._add_to_history(self.ph_history, self.ph)
        self._add_to_history(self.temp_history, self.temperature)
        self._add_to_history(self.water_level_history, self.water_level)

    def _add_to_history(self, history_list, value):
        """Helper untuk menambahkan data ke list riwayat."""
        history_list.append(value)
        if len(history_list) > self.max_history_points:
            history_list.pop(0)

    def toggle_light(self):
        self.light_on = not self.light_on
        return self.light_on

    def toggle_fan(self):
        self.fan_on = not self.fan_on
        return self.fan_on

    def toggle_water_pump(self):
        self.water_pump_on = not self.water_pump_on
        return self.water_pump_on
    
    def toggle_automation(self):
        """Mengaktifkan atau menonaktifkan master switch otomatisasi."""
        self.automation_enabled = not self.automation_enabled
        return self.automation_enabled

    def load_profile(self, profile_name, profile_data):
        """Memuat data dari profil tanaman yang dipilih."""
        self.active_profile_name = profile_name
        self.active_profile_data = profile_data
        print(f"Profil '{profile_name}' dimuat.")

    def set_notification(self, message):
        """Mengatur pesan notifikasi yang akan ditampilkan di UI."""
        self.notification_message = message