# model.py

class Model:
    # Inisialisasi State Aplikasi
    def __init__(self):
        self.ph = 0.0
        self.temperature = 0.0
        self.humidity = 0.0
        self.light = 0
        self.water_level = 0.0
        
        self.water_pump_on = False
        self.light_on = False
        self.fan_on = False
        self.is_refilling = False

        self.ph_history = []
        self.temp_history = []
        self.water_level_history = []
        self.max_history_points = 50

        self.automation_enabled = False
        
        self.active_profile_name = "Tidak Ada"
        self.active_profile_data = None
        
        self.notification_message = "Otomatisasi nonaktif."

    # Pembaruan Data Sensor
    def update_sensor_data(self, data: dict):
        self.ph = data.get("ph", self.ph)
        self.temperature = data.get("temperature", self.temperature)
        self.humidity = data.get("humidity", self.humidity)
        self.light = data.get("light", self.light)
        self.water_level = data.get("water_level", self.water_level)
        self.is_refilling = data.get("is_refilling", self.is_refilling)
        
        self._add_to_history(self.ph_history, self.ph)
        self._add_to_history(self.temp_history, self.temperature)
        self._add_to_history(self.water_level_history, self.water_level)

    # Fungsi Bantuan: Menambah Data ke Riwayat
    def _add_to_history(self, history_list, value):
        history_list.append(value)
        if len(history_list) > self.max_history_points:
            history_list.pop(0)

    # Mengubah Status Lampu
    def toggle_light(self):
        self.light_on = not self.light_on
        return self.light_on

    # Mengubah Status Kipas
    def toggle_fan(self):
        self.fan_on = not self.fan_on
        return self.fan_on

    # Mengubah Status Pompa Air
    def toggle_water_pump(self):
        self.water_pump_on = not self.water_pump_on
        return self.water_pump_on
    
    # Mengubah Status Otomatisasi
    def toggle_automation(self):
        self.automation_enabled = not self.automation_enabled
        return self.automation_enabled

    # Memuat Profil Tanaman
    def load_profile(self, profile_name, profile_data):
        self.active_profile_name = profile_name
        self.active_profile_data = profile_data
        print(f"Profil '{profile_name}' dimuat.")

    # Mengatur Pesan Notifikasi
    def set_notification(self, message):
        self.notification_message = message